/*+
    ARES/HADES/BORG Package -- ./src/common/sampler_base.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/cconfig.h"
#include "libLSS/mpi/generic_mpi.hpp"
#include <boost/optional.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>
#include <boost/function.hpp>
#include <boost/random/random_device.hpp>
#include <CosmoTool/algo.hpp>
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/hdf5_error.hpp"
#include "libLSS/samplers/core/main_loop.hpp"
#include "libLSS/mcmc/state_element.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"

#include "preparation_types.hpp"
#include "preparation_tools.hpp"
#include "configuration.hpp"

#ifdef SAMPLER_BUNDLE
#  include SAMPLER_BUNDLE
#endif

#ifndef ARES_EXTRA_CATCH_CLAUSE
#  define ARES_EXTRA_CATCH_CLAUSE
#endif

#include "preparation.hpp"
#include "preparation_simulation.hpp"
#include "mock_gen.hpp"
#include "projection.hpp"
#include "libLSS/ares_version.hpp"
#include "libLSS/tools/string_tools.hpp"
#include "libLSS/tools/cpu/feature_check.hpp"

#include SAMPLER_DATA_INIT

#ifdef SAMPLER_BUNDLE
#  include SAMPLER_BUNDLE_INIT
#endif

using namespace LibLSS;
using namespace LibLSS_prepare;

using boost::format;
using boost::optional;
using boost::str;
using CosmoTool::square;
using std::string;

namespace {
#if defined(ARES_MPI_FFTW)
  RegisterStaticInit reg0(fftw_mpi_init, fftw_mpi_cleanup, 9, "MPI/FFTW");
#endif
  // WISDOM must come at the end. Otherwise it is reset
  RegisterStaticInit reg1(
      CosmoTool::init_fftw_wisdom, CosmoTool::save_fftw_wisdom, 12,
      "FFTW/WISDOM");
#if !defined(ARES_MPI_FFTW) &&                                                 \
    defined(                                                                   \
        _OPENMP) // Do not use MPI and Threaded FFTW at the same time for the moment.
  RegisterStaticInit
      reg2(fftw_init_threads, fftw_cleanup_threads, 11, "FFTW/THREADS");
#endif
} // namespace

template <typename RandGen>
void reseed(RandGen &rgen) {
  rgen.seed(rgen.get());
}

int main(int argc, char **argv) {
  using std::string;
  MPI_Communication *mpi_world = setupMPI(argc, argv);
  Console &cons = Console::instance();

  StaticInit::execute();
#if !defined(ARES_MPI_FFTW) && defined(_OPENMP)
  fftw_plan_with_nthreads(smp_get_max_threads());
#endif

  cons.print<LOG_INFO>(
      format("Starting " SAMPLER_NAME ". rank=%d, size=%d") %
      mpi_world->rank() % mpi_world->size());
  cons.print<LOG_INFO_SINGLE>("ARES3 base version " + ARES_GIT_VERSION);
  cons.print<LOG_INFO_SINGLE>(LibLSS::tokenize(ARES_GIT_REPORT, "\n"));
  {
    std::string cpu_features;
    bool result = LibLSS::check_compatibility(cpu_features);
    cons.format<LOG_INFO>("CPU features: %s", cpu_features);
    if (!result) {
      cons.print<LOG_ERROR>("Binary is incompatible with your CPU. Stop here.");
      mpi_world->abort();
      return 1;
    }
  }

  try {
    MainLoop loop;

    if (argc != 3) {
      cons.print<LOG_ERROR>(
          SAMPLER_NAME
          " requires exactly two parameters: INIT or RESUME as first"
          " parameter and the configuration file as second parameter.");
      return 1;
    }

    LibLSS_prepare::ptree params;
    cons.print<LOG_DEBUG>("Parsing ini file");
    try {
      read_ini(argv[2], params);
    } catch (const boost::property_tree::ini_parser::ini_parser_error &e) {
      error_helper<ErrorParams>(
          string("I could not read INI file. Error was: ") + e.what());
    }
    cons.print<LOG_DEBUG>("Retrieving system tree");
    ptree system_params = params.get_child("system");
    cons.print<LOG_DEBUG>("Retrieving run tree");
    ptree run_params = params.get_child("run");

    if (optional<string> console_output_file =
            system_params.get_optional<string>("console_output")) {
      cons.outputToFile(
          str(format("%s_rank_%d") % *console_output_file % mpi_world->rank()));
    }

    string action = argv[1];

    SamplerBundle bundle(mpi_world);
    MarkovState &state = loop.get_state();

    state.newScalar("ARES_version", ARES_GIT_VERSION);

    // Load common configuration file options
    loadConfigurationFile(*mpi_world, loop, params);
    setupProjection(*mpi_world, loop, params);

    CosmologicalParameters &cosmo =
        state.getScalar<CosmologicalParameters>("cosmology");
    RGenType randgen(mpi_world, -1);

    randgen.seed(system_params.get<unsigned long int>("seed", 24032015));

    bool furiousSeed;
    int Ncat, savePeriodicity;
    long N_MC_LOOP;
    long N0, N1, N2, localN0, startN0;
    SLong *mcmc_step;

    boost::random::random_device rng_dev;

    // furious seeding disables deterministic seeding and use a true source
    // of entropy to reseed the Pseudo-RNG at each MCMC loop.
    // This could deprive quickly the amount of available entropy for small runs
    // and could actually cause a stale and performance reduction in that
    // case.
    // furiousSeeding is thus not enabled by default.
    furiousSeed = system_params.get<bool>("furious_seeding", false);

    Ncat = adapt<long>(state, run_params, "NCAT", true);

    // Initialize the input data structures. They need to be in place
    // in state to have the RESUME action functioning correctly.
    sampler_init_data(mpi_world, state, params);

    savePeriodicity = system_params.get<int>("savePeriodicity", 1);
    N_MC_LOOP = params.get<long>("mcmc.number_to_generate");
    cons.print<LOG_VERBOSE>(
        format("We will compute %d MCMC samples") % N_MC_LOOP);
    N0 = state.getScalar<long>("N0");
    N1 = state.getScalar<long>("N1");
    N2 = state.getScalar<long>("N2");
    localN0 = state.getScalar<long>("localN0");
    startN0 = state.getScalar<long>("startN0");

    // MCMC step id
    state.newElement("MCMC_STEP", mcmc_step = new SLong());

    // Create growth factor field
    ArrayType *growth;
    state.newElement(
        "growth_factor",
        growth = new ArrayType(
            boost::extents[range(startN0, startN0 + localN0)][N1][N2]));
    growth->setRealDims(PrepareDetail::ArrayDimension(N0, N1, N2));

    // Insert random number generator into the state variable
    state.newElement(
        "random_generator", new RandomStateElement<RandomNumber>(&randgen));

    // Initialize the program bundle.
    sampler_bundle_init(
        mpi_world, params, bundle, loop,
        (action == "SPECIAL_RESUME") or (action == "RESUME") or
            (action == "RESUME_RESEED"));
    sampler_setup_data(mpi_world, state, params, loop);

    // Here we have the different action. We can either reload a previous
    // run or start from scratch.
    if (action == "SPECIAL_RESUME") {
      loop.restore("restart.h5", true);
      reseed(state.get<RandomStateElement<RandomNumber>>("random_generator")
                 ->get());
      loop.setStepID(mcmc_step->value);
    } else if (action == "RESUME" || action == "RESUME_RESEED") {
      loop.restore("restart.h5", false);
      if (action == "RESUME_RESEED") {
        // Force reseeding after restart
        state.get<RandomStateElement<RandomNumber>>("random_generator")
            ->get()
            .seed(system_params.get<unsigned long int>("seed", 24032015));
      }
      loop.setStepID(mcmc_step->value);
    } else if (action == "INIT") {
      // Load survey data.
      sampler_load_data(mpi_world, state, params, loop);
      sampler_prepare_data(mpi_world, state, params, loop);
      mcmc_step->value = 0;
    } else {
      error_helper<ErrorParams>("Invalid parameter " + action);
    }

    buildGrowthFactor(state, cosmo);

    // Initiate samplers
    loop.initialize();
    // Save some wisdom here just in case.
    CosmoTool::save_fftw_wisdom();

    loop.save();

    if (action == "INIT" && system_params.get<bool>("test_mode", false)) {
      cons.print<LOG_INFO_SINGLE>("Prepare mock data");
      if (furiousSeed) {
        randgen.seed(rng_dev());
      }
      prepareMockData(params, mpi_world, state, cosmo, bundle);
    }

    // Powerspectrum is not sampled that way anymore.
    //    if (system_params.get<bool>("seed_cpower", false)) {
    //      createCosmologicalPowerSpectrum(state, cosmo);
    //    } else {
    //      Console::instance().print<LOG_INFO_SINGLE>("Reseting powerspectrum");
    //      createCosmologicalPowerSpectrum(state, cosmo, 10);
    //    }

    if (action == "INIT")
      sampler_setup_ic(bundle, loop, params);

    loop.save();

    int last_save = 0;
    try {
      for (int i = 0; i < N_MC_LOOP; i++) {
        if (furiousSeed) {
          randgen.seed(rng_dev());
        }
        loop.run();
        loop.snap();
        if ((i % savePeriodicity) == 0) {
          last_save = i;
          loop.save();
        }
        mcmc_step->value++;
        timings::trigger_dump();
      }
    } catch (const ErrorBase &e) {
      loop.save_crash();
      throw;
    }
    if (last_save < N_MC_LOOP) {
      cons.print<LOG_STD>("Reached end of the loop. Writing restart file.");
      loop.save();
    }
  } catch (const ErrorBase &e) {
    cons.print<LOG_ERROR>(
        "An error was raised (msg=" + std::string(e.what()) + "). Exiting.");

    MPI_Communication::instance()->abort();
  } catch (const boost::property_tree::ptree_bad_path &e) {
    cons.print<LOG_ERROR>(
        "Missing option in configuration " + e.path<ptree::path_type>().dump());
  } catch (const boost::property_tree::ptree_bad_data &e) {
    cons.print<LOG_ERROR>(
        "Error converting this parameter " + e.data<string>());
  }
  ARES_EXTRA_CATCH_CLAUSE

  sampler_bundle_cleanup();

  StaticInit::finalize();

  doneMPI();

  return 0;
}
