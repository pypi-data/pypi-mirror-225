/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/tests/generic_gradient_benchmark.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/tools/static_init.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include <CosmoTool/cosmopower.hpp>
#include <CosmoTool/algo.hpp>
#include <boost/format.hpp>
#include <fstream>
#include <iostream>
#include "libLSS/tests/setup_hades_test_run.hpp"

using namespace LibLSS;
using boost::format;
using CosmoTool::square;
using std::endl;
using std::ios;
using std::ofstream;
using std::string;

typedef boost::multi_array_types::extent_range range;

typedef RandomNumberThreaded<GSL_RandomNumber> RGenType;

static constexpr size_t BORG_RESOLUTION = 128; //128;

#ifndef BORG_SUPERSAMPLING
#  define BORG_SUPERSAMPLING 1
#endif

#ifndef BORG_FORCESAMPLING
#  define BORG_FORCESAMPLING 1
#endif

namespace {
#if defined(ARES_MPI_FFTW)
  RegisterStaticInit reg0(fftw_mpi_init, fftw_mpi_cleanup, 9, "MPI/FFTW");
#endif
  RegisterStaticInit reg1(
      CosmoTool::init_fftw_wisdom, CosmoTool::save_fftw_wisdom, 10,
      "FFTW/WISDOM");
#if !defined(ARES_MPI_FFTW) &&                                                 \
    defined(                                                                   \
        _OPENMP) // Do not use MPI and Threaded FFTW at the same time for the moment.
  RegisterStaticInit
      reg2(fftw_init_threads, fftw_cleanup_threads, 11, "FFTW/THREADS");
#endif
}; // namespace

class DummyPowerSpectrum : public PowerSpectrumSampler_Base {
public:
  DummyPowerSpectrum(MPI_Communication *comm)
      : PowerSpectrumSampler_Base(comm) {}

  virtual void initialize(MarkovState &state) { initialize_base(state); }
  virtual void restore(MarkovState &state) { restore_base(state); }

  virtual void sample(MarkovState &state) {}
};

void createCosmologicalPowerSpectrum(
    MarkovState &state, CosmologicalParameters &cosmo_params,
    double adjust = 1) {
  double h;
  CosmoTool::CosmoPower cpower;

  h = cpower.h = cosmo_params.h;
  cpower.OMEGA_B = cosmo_params.omega_b;
  cpower.OMEGA_C = cosmo_params.omega_m - cosmo_params.omega_b;
  cpower.SIGMA8 = cosmo_params.sigma8;
  cpower.setFunction(CosmoTool::CosmoPower::HU_WIGGLES);
  cpower.updateCosmology();
  cpower.normalize();

  ArrayType1d::ArrayType &k = *state.get<ArrayType1d>("k_modes")->array;
  ArrayType1d::ArrayType &Pk = *state.get<ArrayType1d>("powerspectrum")->array;
  for (long i = 0; i < k.num_elements(); i++) {
    Pk[i] = cpower.power(k[i] * h) * h * h * h * adjust;
  }
}

#ifndef MIN_RANK
#  define MIN_RANK 1
#endif

static const int INIT_RANK = MIN_RANK;

int main(int argc, char **argv) {
  MPI_Communication *comm_base = setupMPI(argc, argv);
  StaticInit::execute();
  Console &cons = Console::instance();
  cons.setVerboseLevel<LOG_DEBUG>();
  int rankThreshold = INIT_RANK;
  int k = 0, kmax;
  using boost::chrono::system_clock;

  cons.outputToFile(
      boost::str(format("gradient_bench_rank_%d.txt") % comm_base->rank()));

  for (kmax = 0; rankThreshold < comm_base->size(); kmax++)
    rankThreshold *= 2;
  kmax++;

  rankThreshold = INIT_RANK;

  cons.print<LOG_DEBUG>(format("kmax = %d") % kmax);

  while (k < kmax) {
    int color = (comm_base->rank() < rankThreshold) ? 0 : 1;
    //    int color;
    //    int groupper = comm_base->size() / rankThreshold;
    //    if (groupper > 1)
    //      color =
    //       ((comm_base->rank() % groupper) == 0) ? 0 : 1;
    //    else
    //      color = comm_base->rank() == 0 ? 0 : 1;
    cons.format<LOG_DEBUG>("Color is %d", color);
    MPI_Communication *comm = comm_base->split(color, comm_base->rank());
    boost::chrono::system_clock::time_point start_context_forward,
        start_context_adjoint;
    boost::chrono::duration<double> duration_forward, duration_adjoint;

    if (color == 1) {
      comm_base->barrier();
      rankThreshold = std::min(comm_base->size(), 2 * rankThreshold);
      k++;
      delete comm;
      continue;
    }

    {
      MarkovState state;
      RGenType randgen(-1);
      int M;
      BoxModel box;
      BoxModel box2;
      LikelihoodInfo info;

      randgen.seed(2348098);

      state.newElement(
          "random_generator", new RandomStateElement<RandomNumber>(&randgen));

      LibLSS_test::setup_hades_test_run(comm, BORG_RESOLUTION, 600, state);
      LibLSS_test::setup_box(state, box);

      state.newScalar<long>("Ndata0", box.N0 / DOWNGRADE_DATA);
      state.newScalar<long>("Ndata1", box.N1 / DOWNGRADE_DATA);
      state.newScalar<long>("Ndata2", box.N2 / DOWNGRADE_DATA);
      // FIXME!
      state.newScalar<long>("localNdata0", state.getScalar<long>("startN0"));
      state.newScalar<long>(
          "localNdata1",
          state.getScalar<long>("startN0") + state.getScalar<long>("localN0"));
      state.newScalar<long>("localNdata2", 0);
      state.newScalar<long>("localNdata3", box.N1 / DOWNGRADE_DATA);
      state.newScalar<long>("localNdata4", 0);
      state.newScalar<long>("localNdata5", box.N2 / DOWNGRADE_DATA);

      LibLSS_test::setup_likelihood_info(state, info, comm);

      box2 = box;
      box2.N0 *= 2;
      box2.N1 *= 2;
      box2.N2 *= 2;

      DummyPowerSpectrum dummy_p(comm);
      HMCDensitySampler::Likelihood_t likelihood = makeLikelihood(info);

      auto model = buildModel(comm, state, box, box2);
      BorgModelElement *model_element = new BorgModelElement();

      model_element->obj = model;
      state.newElement("BORG_model", model_element);

      HMCDensitySampler hmc(comm, likelihood);

      // Initialize (data,s)->t sampler
      dummy_p.init_markov(state);
      hmc.init_markov(state);

      createCosmologicalPowerSpectrum(
          state, state.getScalar<CosmologicalParameters>("cosmology"));

      // Build some mock field
      {
        ConsoleContext<LOG_INFO> ctx("Generation performance");
        timings::set_file_pattern("timing_generation_N_" + to_string(rankThreshold) + "_%d.txt");
        timings::reset();
        hmc.generateMockData(state);
        timings::trigger_dump();
        timings::set_file_pattern("timing_stats_N_" + to_string(rankThreshold) + "_%d.txt");
      }

      typedef FFTW_Manager<double, 3> DFT_Manager;
      std::unique_ptr<DFT_Manager> mgr_p = std::make_unique<DFT_Manager>(
          BORG_RESOLUTION, BORG_RESOLUTION, BORG_RESOLUTION, comm);
      auto &mgr = *mgr_p;
      CArrayType *s_hat_field = state.get<CArrayType>("s_hat_field");
      auto gradient_field_p = mgr.allocate_complex_array();
      auto &gradient_field = gradient_field_p.get_array();
      auto tmp_field_p = mgr.allocate_complex_array();
      auto delta_out_p = mgr.allocate_array();
      auto &delta_out = delta_out_p.get_array();

      double volume = box.L0 * box.L1 * box.L2;
      double ai = state.getScalar<double>("borg_a_initial");
      Cosmology cosmo(state.getScalar<CosmologicalParameters>("cosmology"));
      double D_init = cosmo.d_plus(ai) /
                      cosmo.d_plus(1.0); // Scale factor for initial conditions

      array::scaleAndCopyArray3d(
          tmp_field_p.get_array(), *s_hat_field->array, D_init);

      {
        ConsoleContext<LOG_INFO> ctx("Forward-Gradient performance");
        timings::set_file_pattern("timing_forward_N_" + to_string(rankThreshold) + "_%d.txt");
        timings::reset();

        start_context_forward = system_clock::now();
        //model->forwardModel(tmp_field_p.get_array(), delta_out, true);
        likelihood->logLikelihood(tmp_field_p.get_array());
        duration_forward = system_clock::now() - start_context_forward;
        timings::trigger_dump();
      }

      if (RUN_RSD_TEST) {
        {
          ConsoleContext<LOG_INFO> ctx("Forward RSD performance");

          double vobsext[3] = {100, 100, 100};
          start_context_adjoint = system_clock::now();
          model->forwardModelRsdField(delta_out, vobsext);
          duration_adjoint = system_clock::now() - start_context_adjoint;
        }

        {
          double vobsext[3] = {0, 0, 0};
          model->forwardModelRsdField(delta_out, vobsext);
        }
      }

      {
        ConsoleContext<LOG_INFO> ctx("Gradient performance");
        timings::set_file_pattern("timing_gradient_N_" + to_string(rankThreshold) + "_%d.txt");
        timings::reset();
        start_context_adjoint = system_clock::now();
        fwrap(gradient_field) = 1.0;
        likelihood->gradientLikelihood(
            tmp_field_p.get_array(), gradient_field, false, 1.0);
        duration_adjoint = system_clock::now() - start_context_adjoint;
        timings::trigger_dump();
      }
    }

    if (comm_base->rank() == 0) {
      ofstream f_performance("bench_performance.txt", ios::app);
      f_performance << format("%s % 5d % 5d % 5d % .5lf % .5lf") % testName %
                           BORG_RESOLUTION % rankThreshold %
                           smp_get_max_threads() % duration_forward.count() %
                           duration_adjoint.count()
                    << endl;
    }
    comm_base->barrier();
    rankThreshold = std::min(comm_base->size(), 2 * rankThreshold);
    k++;
    delete comm;
  }

  StaticInit::finalize();
  doneMPI();

  return 0;
}
