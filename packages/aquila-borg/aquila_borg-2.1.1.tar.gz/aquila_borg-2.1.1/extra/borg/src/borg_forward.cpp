/*+
    ARES/HADES/BORG Package -- ./extra/borg/src/borg_forward.cpp
    Copyright (C) 2016-2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2016-2017 Jens Jasche <j.jasche@tum.de>
    Copyright (C) 2017 Franz Elsner <f.elsner@mpa-garching.mpg.de>
    Copyright (C) 2018-2019 Florent Leclercq <florent.leclercq@polytechnique.org>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <boost/algorithm/string/find_iterator.hpp>
#include <boost/algorithm/string/finder.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/exception/all.hpp>
#include <boost/type_traits.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>
#include <boost/program_options.hpp>
#include <boost/format.hpp>
#include <boost/optional.hpp>
#include <CosmoTool/algo.hpp>
#include <CosmoTool/hdf5_array.hpp>
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include <functional>
#include <cstdio>
#include <unistd.h>
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/samplers/core/main_loop.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/physics/forwards/pm/plane_xchg.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "common/configuration.hpp"
#include "common/foreground.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/tools/string_tools.hpp"
#include "libLSS/tools/hdf5_scalar.hpp"
#include "healpix_cxx/healpix_map.h"

//JJ new includes
#include <CosmoTool/cosmopower.hpp>
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "libLSS/tools/fftw_allocator.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"
#include "common/preparation.hpp"
#include "common/preparation_simulation.hpp"
#include "ares_init.hpp"

#include "libLSS/physics/cosmo_power.hpp"
#include "libLSS/physics/forwards/particle_balancer/particle_distribute.hpp"

#include "libLSS/tools/hdf5_buffered_write.hpp"
#include "libLSS/physics/forwards/all_models.hpp"

using namespace LibLSS;

using boost::c_storage_order;
using boost::extents;
using boost::format;
using boost::optional;
using boost::str;
using namespace std;
using namespace CosmoTool;

static const bool CIC_WEIGHING = true;

namespace po = boost::program_options;

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

typedef boost::multi_array<double, 3> DensityType;
typedef UninitializedArray<DensityType> U_DensityType;

typedef boost::multi_array<double, 4> VFieldType;
typedef UninitializedArray<VFieldType> U_VFieldType;

typedef boost::multi_array_types::extent_range range;

typedef RandomNumberMPI<GSL_RandomNumber> RGenType;
typedef RefArrayStateElement<std::complex<double>, 3> ComplexRefArray;

class DummyPowerSpectrum : public PowerSpectrumSampler_Base {
public:
  DummyPowerSpectrum(MPI_Communication *comm)
      : PowerSpectrumSampler_Base(comm) {}

  virtual void initialize(MarkovState &state) { initialize_base(state); }
  virtual void restore(MarkovState &state) { restore_base(state); }

  virtual void sample(MarkovState &state) {}
};

void generateRandomField(MPI_Communication *comm, MarkovState &state) {
  ConsoleContext<LOG_INFO_SINGLE> ctx(
      "borg_forward random initial conditions generation");

  ArrayType1d::ArrayType &pspec =
      *state.get<ArrayType1d>("powerspectrum")->array;
  IArrayType::ArrayType &adjust_array =
      *state.get<IArrayType>("adjust_mode_multiplier")->array;
  IArrayType::ArrayType &key_array = *state.get<IArrayType>("k_keys")->array;
  CArrayType::ArrayType &s_hat0 = *state.get<CArrayType>("s_hat_field")->array;
  RandomGen *rgen = state.get<RandomGen>("random_generator");

  long N0, N1, N2;
  double L0, L1, L2;

  N0 = state.getScalar<long>("N0");
  N1 = state.getScalar<long>("N1");
  N2 = state.getScalar<long>("N2");

  size_t Ntot = N0 * N1 * N2;

  L0 = state.getScalar<double>("L0");
  L1 = state.getScalar<double>("L1");
  L2 = state.getScalar<double>("L2");

  FFTW_Manager_3d<double> mgr(N0, N1, N2, comm);

  double volume = L0 * L1 * L2;

  FFTW_Real_Array tmp_real_field(
      mgr.extents_real(), c_storage_order(), mgr.allocator_real);
  FFTW_Complex_Array s_hat(
      mgr.extents_complex(), c_storage_order(), mgr.allocator_complex);
  FCalls::plan_type analysis_plan, synthesis_plan;

  analysis_plan = mgr.create_r2c_plan(tmp_real_field.data(), s_hat.data());

  double invsqN = 1.0 / std::sqrt(double(N0) * N1 * N2);
  ///generate grf field in real space
  fwrap(tmp_real_field) =
      b_fused_idx<double, 3>([rgen, invsqN](int, int, int) -> double {
        return rgen->get().gaussian() * invsqN;
      });

  ///transform to f-space
  mgr.execute_r2c(analysis_plan, tmp_real_field.data(), s_hat.data());

  // Apply coloring
  fwrap(s_hat0) = s_hat;

  //kill the zero mode
  if (mgr.startN0 == 0 && mgr.localN0 > 0)
    s_hat0[0][0][0] = 0.;

  mgr.destroy_plan(analysis_plan);
}

template <typename T>
T periodicity(T x, T L) {
  while (x < 0)
    x += L;
  while (x >= L)
    x -= L;
  return x;
}

#include "likelihood_info.hpp"
#include "mcmcfile_parsing.hpp"
#include "bias_generator.hpp"
#include "dmsheet_output.hpp"
#include "cic_output.hpp"
#include "model_generator.hpp"

template <typename T, typename PTree>
void ensure_default(PTree &params, std::string const &key, T const &value) {
  if (params.find(key) == params.not_found())
    params.add(key, value);
}

static void ensure_defaults(LibLSS_prepare::ptree &params) {
  ensure_default<double>(params, "gravity.a_initial", 0.001);
  ensure_default<long>(params, "gravity.supersampling", 1);
  ensure_default<long>(params, "gravity.forcesampling", 1);
  ensure_default<double>(params, "gravity.a_final", 1);
}

int main(int argc, char **argv) {
  using boost::format;
  using LibLSS_prepare::ptree;
  using std::string;
  MPI_Communication *mpi_world = setupMPI(argc, argv);
  Console &cons = Console::instance();
  typedef boost::multi_array_types::extent_range range;
  namespace ph = std::placeholders;

  StaticInit::execute();
#if !defined(ARES_MPI_FFTW) && defined(_OPENMP)
  fftw_plan_with_nthreads(smp_get_max_threads());
#endif
  bool savepos = false, savevel = false, savevfield = false,
       all_timesteps = false, dmsheet = false, random = false,
       output_split = false, invert_ic = false, biased_densities = false,
       robust_maps = false, cosmo_from_config = false;
  size_t rayshoot;

  po::options_description desc("BORG_FORWARD allowed options");
  desc.add_options()("help,h", "produce help message")(
      "config", po::value<string>(), "BORG configuration file")(
      "cosmo-from-config", po::bool_switch(&cosmo_from_config),
      "Flag controling whether cosmology is read in from the ini file or from "
      "the h5")(
      "restart", po::value<string>(), "BORG restart file base prefix")(
      "mcmc", po::value<std::vector<string>>(), "MCMC file to resimulate")(
      "output", po::value<string>(),
      "Output file pattern (default is output_%04d.h5)")(
      "pos", po::bool_switch(&savepos), "save particle positions")(
      "vel", po::bool_switch(&savevel), "save particle velocities")(
      "vfield", po::bool_switch(&savevfield),
      "compute and save velocity field")(
      "all-timesteps", po::bool_switch(&all_timesteps),
      "save all timesteps and not just the last one")(
      "random", po::bool_switch(&random), "compute unconstrained simulation")(
      "output_split", po::bool_switch(&output_split),
      "leave files split according to MPI")(
      "invert_ic", po::bool_switch(&invert_ic),
      "transform the initial conditions in their opposite")(
      "biased_densities", po::bool_switch(&biased_densities),
      "generate biased densities too (only valid for BORG Generic biases)")(
      "robust_maps", po::bool_switch(&robust_maps),
      "generate summary statistics of maps inferred through robust likelihood")(
      "dmsheet", po::bool_switch(&dmsheet),
      "generate density fields using tetrahedra")(
      "dmsheet_grid", po::value<string>(),
      "dimensions specified with the syntax N0xN1xN2")(
      "robust_maps_nside", po::value<long>(),
      "Healpix Nside dimension for summaries of the systematic map")(
      "ray-count", po::value<size_t>(&rayshoot)->default_value(8),
      "number of rays to shoot");

  po::positional_options_description p;
  p.add("mcmc", -1);

  po::variables_map vm;

  try {
    po::store(
        po::command_line_parser(argc, argv).options(desc).positional(p).run(),
        vm);
  } catch (const boost::exception &e) {
    cons.print<LOG_ERROR>(
        format("Error while parsing command line: %s") %
        boost::diagnostic_information(e));
    if (mpi_world->rank() == 0) {
      // At the moment use cout
      cout << desc << endl;
    }
    return 1;
  }
  po::notify(vm);

  if (vm.count("help")) {
    if (mpi_world->rank() == 0) {
      // At the moment use cout
      cout << desc << endl;
    }
    return 1;
  }

  cons.print<LOG_INFO>(
      format("Starting BORG_FORWARD, rank=%d, size=%d") % mpi_world->rank() %
      mpi_world->size());

  try {
    MainLoop loop;
    string output_pattern;
    long N0, N1, N2;
    LikelihoodInfo info;

    if (vm.count("config") == 0) {
      cons.print<LOG_ERROR>("Need a configuration file");
      return 2;
    }

    if (vm.count("output") == 0) {
      output_pattern = "output_%04d.h5";
      if (random)
        output_pattern = "output_random_%04d.h5";

    } else {
      output_pattern = vm["output"].as<string>();
    }

    ptree params;
    cons.print<LOG_DEBUG>("Parsing ini file");
    try {
      read_ini(vm["config"].as<string>(), params);
    } catch (const boost::property_tree::ini_parser::ini_parser_error &e) {
      error_helper<ErrorParams>(
          string("Could read INI file. Error was: ") + e.what());
    } catch (const boost::bad_any_cast &e) {
      error_helper<ErrorParams>(string("Bad cast. Error was: ") + e.what());
    }

    ensure_defaults(params);

    cons.print<LOG_VERBOSE>("Grabbing mcmc files");
    std::vector<string> mcmc_files = vm["mcmc"].as<std::vector<string>>();

    cons.print<LOG_DEBUG>("Retrieving system tree");
    ptree system_params = params.get_child("system");
    cons.print<LOG_DEBUG>("Retrieving run tree");
    ptree run_params = params.get_child("run");

    if (optional<string> console_output_file =
            system_params.get_optional<string>("console_output")) {
      cons.outputToFile(
          str(format("%s_rank_%d") % *console_output_file % mpi_world->rank()));
    }

    MarkovState &state = loop.get_state();

    // Load common configuration file options
    loadConfigurationFile(*mpi_world, loop, params);

    CosmologicalParameters cosmo;

    if (cosmo_from_config) {
      ptree config_cosmo = params.get_child("cosmology");
      cosmo.sigma8 = config_cosmo.get<double>("sigma8");
      cosmo.z0 = config_cosmo.get<double>("z0");
      cosmo.omega_r = config_cosmo.get<double>("omega_r");
      cosmo.omega_k = config_cosmo.get<double>("omega_k");
      cosmo.omega_b = config_cosmo.get<double>("omega_b");
      cosmo.omega_q = config_cosmo.get<double>("omega_q");
      cosmo.omega_m = config_cosmo.get<double>("omega_m");
      cosmo.w = config_cosmo.get<double>("w");
      cosmo.wprime = config_cosmo.get<double>("wprime");
      cosmo.n_s = config_cosmo.get<double>("n_s");
      cosmo.h = config_cosmo.get<double>("h100");
      cosmo.fnl = config_cosmo.get<double>("fnl");
      cosmo.beta = config_cosmo.get<double>("beta");

      cons.format<LOG_DEBUG>("Testing whether params are read in correctly\n");
      cons.format<LOG_DEBUG>(
          "sigma8: %.10f\t omega_r: %.10f\t omega_k: %.10f\t omega_b: %.10f\t"
          "omega_q: %.10f\t omega_m: %.10f\t w: %.10f\t wprime: %.10f\t"
          "n_s: %.10f\t h100: %.10f\t fnl: %.10f\t beta: %.10f\b",
          cosmo.sigma8, cosmo.omega_r, cosmo.omega_k, cosmo.omega_b,
          cosmo.omega_q, cosmo.omega_m, cosmo.w, cosmo.wprime, cosmo.n_s,
          cosmo.h, cosmo.fnl, cosmo.beta);
    } else {
      cosmo = state.getScalar<CosmologicalParameters>("cosmology");
    }

    Cosmology cosmo_model(cosmo);

    N0 = state.getScalar<long>("N0");
    N1 = state.getScalar<long>("N1");
    N2 = state.getScalar<long>("N2");

    long N2_HC;
    N2_HC = N2 / 2 + 1;

    RGenType randgen(mpi_world, -1);
    randgen.seed(2348098);
    state.newElement(
        "random_generator", new RandomStateElement<RandomNumber>(&randgen));

    string model_type = params.get<string>("gravity.model");
    string lh_name = params.get<string>("hades.likelihood");
    long ncat = run_params.get<int>("NCAT");
    double lightcone_boost = system_params.get<double>(
        "borg_lightcone_boost",
        1.0); // This is an artificial factor just to make cool plots.
    BoxModel box;
    std::shared_ptr<ChainForwardModel> model;

    adapt<long>(state, run_params, "NCAT", true);

    box.xmin0 = state.getScalar<double>("corner0");
    box.xmin1 = state.getScalar<double>("corner1");
    box.xmin2 = state.getScalar<double>("corner2");
    box.L0 = state.getScalar<double>("L0");
    box.L1 = state.getScalar<double>("L1");
    box.L2 = state.getScalar<double>("L2");
    box.N0 = state.getScalar<long>("N0");
    box.N1 = state.getScalar<long>("N1");
    box.N2 = state.getScalar<long>("N2");

    double volume = box.L0 * box.L1 * box.L2;
    double dVol = volume / (box.N0 * box.N1 * box.N2);

    LibLSS_prepare::setupLikelihoodInfo(mpi_world, state, info, params, false);

    ParticleSaver_t save_particles;
    TimingSaver_t save_timing;
    std::function<void(U_VFieldType::array_type &)> build_vfield;
    BiasInfo_t save_biased_densities;
    long nside = 0;

    if (biased_densities || robust_maps) {
      save_biased_densities = setup_biased_density_generator(lh_name);
    }

    // Initialize robust map post-treatment.
    if (robust_maps) {
      if (vm.count("restart") == 0) {
        cons.print<LOG_ERROR>("inference of systematic maps requires the "
                              "restart file. check '--restart'.");
        mpi_world->abort();
      }

      LibLSS_prepare::sampler_init_data(mpi_world, state, params);

      if (vm.count("robust_maps_nside") == 0) {
        cons.print<LOG_ERROR>(
            "inference of systematic map summaries requires you to specify the "
            "resolution of the maps with robust_maps_nside.");
        mpi_world->abort();
      }

      nside = vm["robust_maps_nside"].as<long>();

      // Initialize the dummy entry for foregrounds.
      LibLSS_prepare::initForegrounds(
          mpi_world, state, [](int, int) {}, params);

      // Restore all the registered entries from the restart file.
      std::string restart_name =
          vm["restart"].as<std::string>() + "_" + to_string(mpi_world->rank());
      H5::H5File f(restart_name, H5F_ACC_RDONLY);
      state.restoreState(f, false);
    }

    // Construct the gravity forward model.
    model =
        buildModel(mpi_world, state, box, params, params.get_child("gravity"));

    model->setAdjointRequired(false);

    // FIXME: Do something less brute force to assign build_vfield

    if (auto real_model = model->queryModel("dynamics")) {
      if (auto pmodel =
              dynamic_pointer_cast<ParticleBasedForwardModel>(real_model)) {
        build_vfield = std::bind(
            build_velocity_field, pmodel.get(), box, std::placeholders::_1);
      }
    }

    model->setCosmoParams(state.getScalar<CosmologicalParameters>("cosmology"));

    CArrayType *s_hat_field = new CArrayType(
        model->lo_mgr->extents_complex(), model->lo_mgr->allocator_complex);
    s_hat_field->setRealDims(ArrayDimension(N0, N1, N2_HC));
    //pass ownership to state
    state.newElement("s_hat_field", s_hat_field, false);

    ArrayType out_field(
        model->out_mgr->extents_real_strict(), model->out_mgr->allocator_real);
    ArrayType1d::ArrayType vobs(boost::extents[3]);
    BoxModel out_box = model->get_box_model_output();
    out_field.setRealDims(ArrayDimension(out_box.N0, out_box.N1, out_box.N2));
    out_field.unsafeSetName("final_density");

    for (auto mcmc_file : mcmc_files) {
      int iteration = find_iteration(mcmc_file, random);

      if (!random) {
        H5::H5File f(mcmc_file, H5F_ACC_RDONLY);
        cons.print<LOG_STD>(
            format("Found iteration %d, from file %s") % iteration % mcmc_file);

        try {
          hdf5_read_array(f, "/scalars/BORG_vobs", vobs);
        } catch (H5::Exception const &e) {
          cons.print<LOG_WARNING>("No BORG_vobs in MCMC.");
        }
        hdf5_read_array(
            f, "/scalars/s_hat_field", *s_hat_field->array, false, true);

        for (int cat = 0; cat < ncat; cat++) {
          ArrayType1d *elt;
          state.newElement(
              "galaxy_bias_" + to_string(cat),
              elt = new ArrayType1d(boost::extents[0]), true);
          elt->setAutoResize(true);
          state.newScalar<double>("galaxy_nmean_" + to_string(cat), 0);
        }
        // No partial load, load from snapshot , accept failure if missing field.
        state.restoreState(f, false, true, true);

        if (invert_ic) {
          auto w_shat = fwrap(*s_hat_field->array);

          w_shat = w_shat * double(-1);
        }
      } else {
        cons.print<LOG_STD>(
            format("Generate random simulation %d") % iteration);

        //generate power-spectrum
        DummyPowerSpectrum dummy_p(mpi_world);
        dummy_p.init_markov(state);

        //generate random field
        generateRandomField(mpi_world, state);

        for (int cat = 0; cat < ncat; cat++) {
          ArrayType1d *elt;
          state.newElement(
              "galaxy_bias_" + to_string(cat),
              elt = new ArrayType1d(boost::extents[1]), true);
          elt->setAutoResize(true);
          state.newScalar<double>("galaxy_nmean_" + to_string(cat), 0);

          ArrayType1d::ArrayType &gbias = *elt->array;
          if (boost::optional<std::string> bvalue =
                  params.get_optional<std::string>(
                      boost::str(boost::format("catalog_%d.bias") % cat))) {
            auto bias_double = string_as_vector<double>(*bvalue, ", ");
            gbias.resize(boost::extents[bias_double.size()]);
            std::copy(bias_double.begin(), bias_double.end(), gbias.begin());
            cons.print<LOG_STD>("Set the bias to [" + to_string(gbias) + "]");
          } else {
            cons.format<LOG_STD>("No bias values found for %d", cat);
          }
        }
      }

      unsigned int step = 0;
      double ai = params.template get<double>("gravity.a_initial");
      double ss_factor = params.template get<double>("gravity.supersampling");

      string output_file;

      std::shared_ptr<H5::H5File> f;
      if (!output_split) {
        output_file = str(format(output_pattern) % iteration);
        if (mpi_world->rank() == 0)
          f = std::make_shared<H5::H5File>(output_file, H5F_ACC_TRUNC);
      } else {
        output_file =
            str(format("%s_%d") % str(format(output_pattern) % iteration) %
                mpi_world->rank());
        f = std::make_shared<H5::H5File>(output_file, H5F_ACC_TRUNC);
      }

      model->setObserver(vobs);
      model->setCosmoParams(cosmo);
      model->holdParticles();
      if (all_timesteps) {
        auto pmodel = dynamic_pointer_cast<ParticleBasedForwardModel>(model);
        if (pmodel) {
          pmodel->setStepNotifier(
              [&cons, &f, &step](
                  double a, size_t pNum,
                  ParticleBasedForwardModel::IdSubArray ids,
                  ParticleBasedForwardModel::PhaseSubArray pos,
                  ParticleBasedForwardModel::PhaseSubArray vel) {
                H5::Group g = f->createGroup(str(format("step_%d") % step));
                cons.print<LOG_STD>(
                    format("Saving snapshot %d (a=%g)") % step % a);
                LibLSS::hdf5_write_buffered_array(g, "indices", ids);
                LibLSS::hdf5_write_buffered_array(g, "positions", pos);
                LibLSS::hdf5_write_buffered_array(g, "velocities", vel);
                step++;
              });
        }
      }

      model->forwardModel_v2(ModelInput<3>(
          model->lo_mgr, model->get_box_model(),
          LibLSS::ModelInputBase<3>::rdonly(*s_hat_field->array)));
      model->getDensityFinal(ModelOutput<3>(
          model->out_mgr, model->get_box_model_output(), *out_field.array));

      cons.format<LOG_INFO>("Writing borg_forward output in '%s'", output_file);

      out_field.saveTo2(f, mpi_world, output_split);
      s_hat_field->saveTo2(f, mpi_world, output_split);
      cons.print<LOG_VERBOSE>("Done basic saving");

      if (biased_densities) {
        cons.print<LOG_VERBOSE>("Biased densities");
        if (!std::get<0>(save_biased_densities))
          error_helper<ErrorParams>("Do not know how to generate biased "
                                    "densities with that setup.");
        std::get<0>(save_biased_densities)(
            mpi_world, state, *model, out_field, *f, ncat);
      }
      if (robust_maps) {
        cons.print<LOG_VERBOSE>("Robust map");
        std::get<1>(save_biased_densities)(
            mpi_world, state, info, *model, out_field, *f, ncat, nside,
            rayshoot);
      }
      if (dmsheet) {
        auto real_model = model->queryModel("dynamics");
        if (!real_model)
          error_helper<ErrorBadState>(
              "No element called dynamics. Set a name in ini");
        handle_dmsheet(vm, f, real_model.get());
      }
      if (savevfield && build_vfield) {
        cons.print<LOG_VERBOSE>("VField");
        U_VFieldType vfield(boost::extents[3][box.N0][box.N1][box.N2]);
        build_vfield(vfield.get_array());
        if (mpi_world->rank() == 0)
          hdf5_write_array(*f, "v_field", vfield.get_array());
      }
      if (auto p_model =
              dynamic_pointer_cast<ParticleBasedForwardModel>(model)) {
        if (savepos) {
          auto v_positions = p_model->getParticlePositions();
          auto size = LibLSS::array::make_extent_from(v_positions);
          U_Array<double, 2> loc_positions(size);
          fwrap(loc_positions) = v_positions;
          CosmoTool::hdf5_write_array(*f, "u_pos", loc_positions.get_array());
        }
      }
      if (save_timing)
        save_timing(*f);

      if (f) {
        H5::Group g = f->createGroup("scalars");
        LibLSS::hdf5_save_scalar(g, "corner0", box.xmin0);
        LibLSS::hdf5_save_scalar(g, "corner1", box.xmin1);
        LibLSS::hdf5_save_scalar(g, "corner2", box.xmin2);
        LibLSS::hdf5_save_scalar(g, "L0", box.L0);
        LibLSS::hdf5_save_scalar(g, "L1", box.L1);
        LibLSS::hdf5_save_scalar(g, "L2", box.L2);
        LibLSS::hdf5_save_scalar(g, "N0", box.N0);
        LibLSS::hdf5_save_scalar(g, "N1", box.N1);
        LibLSS::hdf5_save_scalar(g, "N2", box.N2);
        LibLSS::hdf5_save_scalar(
            g, "Np", box.N0 * box.N1 * box.N2 * pow(ss_factor, 3));
        LibLSS::hdf5_save_scalar(g, "cosmo", cosmo);
      }

      model->releaseParticles();

      cons.print<LOG_INFO>("Done");
      if (f)
        f->close();
    }
  } catch (const H5::Exception &e) {
    cons.print<LOG_ERROR>("An HDF5 error was triggered.");
  } catch (const ErrorBase &e) {
    cons.print<LOG_ERROR>("An error was raised. Exiting.");
    mpi_world->abort();
  } catch (const boost::property_tree::ptree_bad_path &e) {
    cons.print<LOG_ERROR>(
        "Missing option in configuration " + e.path<ptree::path_type>().dump());
  } catch (const boost::property_tree::ptree_bad_data &e) {
    cons.print<LOG_ERROR>(
        "Error converting this parameter " + e.data<string>());
  }

  StaticInit::finalize();

  doneMPI();

  return 0;
}

// ARES TAG: authors_num = 4
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2016-2018
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: name(1) = Jens Jasche
// ARES TAG: year(1) = 2016-2017
// ARES TAG: email(1) = j.jasche@tum.de
// ARES TAG: name(2) = Franz Elsner
// ARES TAG: year(2) = 2017
// ARES TAG: email(2) = f.elsner@mpa-garching.mpg.de
// ARES TAG: name(3) = Florent Leclercq
// ARES TAG: year(3) = 2018-2019
// ARES TAG: email(3) = florent.leclercq@polytechnique.org
