/*+
    ARES/HADES/BORG Package -- ./extra/python/src/python_bundle_init.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

#include "python_bundle.hpp"
#include "likelihood_info.hpp"
//#include "libLSS/samplers/rgen/qnhmc/qnhmc_density_sampler.hpp"
#include "libLSS/samplers/rgen/frozen/frozen_phase_density_sampler.hpp"
#include "libLSS/samplers/core/generate_random_field.hpp"
#include "common/preparation_types.hpp"
#include "common/preparation_tools.hpp"
#include <pybind11/embed.h>
#include "pyborg.hpp"
#include "libLSS/samplers/core/main_loop.hpp"
#include "python_bundle_init.hpp"

#include "libLSS/borg_version.hpp"
#include "libLSS/ares_version.hpp"
#include "common/foreground.hpp"
#include "libLSS/physics/cosmo_power.hpp"
#include <pybind11/numpy.h>
#include "libLSS/samplers/core/gridLikelihoodBase.hpp"
#include "libLSS/tools/string_tools.hpp"

using namespace LibLSS;

static std::unique_ptr<Python::py::scoped_interpreter> py_interpret;
namespace py = Python::py;

static py::object gravity_setup;
static py::object likelihood_setup;
static py::object sampler_setup;
static py::object ic_setup;

template <typename T>
std::shared_ptr<T> hold_python_with_ref(py::handle o) {
  auto original_ref = o.cast<std::shared_ptr<T>>();
  // We have to build a new shared_ptr to manage the python reference counting as well
  o.inc_ref();
  auto new_ref =
      std::shared_ptr<T>(original_ref.get(), [original_ref, o](void *) mutable {
        // Decrease the python counter
        o.dec_ref();
        // Decrease the C++ counter
        original_ref.reset();
      });
  return new_ref;
}

PYBIND11_EMBEDDED_MODULE(borg_embed, m) {

  Console::instance().print<LOG_INFO>("Start embedded borg module.");
  Python::bindBORG(m);

  m.def(
      "registerGravityBuilder", [](py::object f) { gravity_setup = f; },
      "Register the function that builds the gravity model for HADES");
  m.def(
      "registerLikelihoodBuilder", [](py::object f) { likelihood_setup = f; },
      "Register the function that builds the likelihood object");
  m.def(
      "registerIcBuilder", [](py::object f) { ic_setup = f; },
      "Register the function in charge of initial condition of the chain");
  m.def(
      "registerSamplerBuilder", [](py::object f) { sampler_setup = f; },
      "Register the function that returns a list of samplers to execute.");
}

static std::shared_ptr<BORGForwardModel>
build_model_from_python(MarkovState &state, BoxModel &box) {
  if (!gravity_setup) {
    error_helper<ErrorBadState>("Gravity builder has not been registered");
  }
  try {
    return gravity_setup(&state, &box)
        .cast<std::shared_ptr<BORGForwardModel>>();
  } catch (pybind11::error_already_set const &e) {
    Console::instance().print<LOG_ERROR>(
        "An error was thrown by python: " + std::string(e.what()));
    error_helper<ErrorBadState>("Python thrown an unrecoverable error.");
  }
}

void LibLSS::sampler_bundle_cleanup()
{
  gravity_setup.release().dec_ref();
  likelihood_setup.release().dec_ref();
  sampler_setup.release().dec_ref();
  ic_setup.release().dec_ref();
  py_interpret.reset();
}

void LibLSS::sampler_bundle_init(
    MPI_Communication *mpi_world, LibLSS_prepare::ptree &params,
    SamplerBundle &bundle, MainLoop &loop, bool resuming) {
  typedef LibLSS_prepare::ptree ptree;
  using boost::format;
  using CosmoTool::square;
  using std::string;

  py_interpret =
      std::unique_ptr<py::scoped_interpreter>(new py::scoped_interpreter());

  py::object scope = py::module::import("__main__").attr("__dict__");
  // Make sure the embedded module is loaded to have the class definitions.
  py::module::import("borg_embed");

  ptree system_params = params.get_child("system");
  ptree python_params = params.get_child("python");
  auto block_loop_params = params.get_child_optional("block_loop");

  int hades_mixing = params.template get<int>("hades.mixing", 20);
  std::string lh_type =
      params.template get<std::string>("hades.likelihood", "LINEAR");
  std::shared_ptr<MarkovSampler> nmean, bias;
  typedef GridDensityLikelihoodBase<3> grid_t;
  std::shared_ptr<grid_t> likelihood;

  MarkovState &state = loop.get_state();
  auto &cons = Console::instance();

  BorgModelElement *model = new BorgModelElement();
  loop.get_state().newElement("BORG_model", model);

  loop.get_state().newScalar("BORG_version", BORG_GIT_VERSION);

  BoxModel box;

  box.xmin0 = state.getScalar<double>("corner0");
  box.xmin1 = state.getScalar<double>("corner1");
  box.xmin2 = state.getScalar<double>("corner2");
  box.L0 = state.getScalar<double>("L0");
  box.L1 = state.getScalar<double>("L1");
  box.L2 = state.getScalar<double>("L2");
  box.N0 = state.getScalar<long>("N0");
  box.N1 = state.getScalar<long>("N1");
  box.N2 = state.getScalar<long>("N2");

  string code_path = python_params.template get<string>("likelihood_path");

  auto like_info = std::make_shared<LikelihoodInfo>();
  LibLSS_prepare::setupLikelihoodInfo(
      mpi_world, loop.get_state(), *like_info, params, resuming);

  // Evaluate the python entry point
  py::eval_file(code_path, scope);

  // Ask python to setup the deterministic forward model chain.
  model->obj = build_model_from_python(state, box);
  if (!model->obj) {
    error_helper<ErrorBadState>("A model needs be setup in python.");
  }

  if (!likelihood_setup) {
    error_helper<ErrorBadState>("Likelihood builder has not been registered");
  }
  try {
    py::object py_likelihood = likelihood_setup(&state, like_info);

    likelihood = bundle.python_likelihood =
        hold_python_with_ref<grid_t>(py_likelihood);
  } catch (pybind11::error_already_set const &e) {
    Console::instance().print<LOG_ERROR>(
        "An error was thrown by python: ");
    Console::instance().print<LOG_ERROR>(LibLSS::tokenize(e.what(), "\n"));
    error_helper<ErrorBadState>("Python thrown an unrecoverable error.");
  }
  bundle.delegate_ic_to_python =
      python_params.template get<bool>("ic_in_python", false);

  // Initialize foregrounds
  LibLSS_prepare::initForegrounds(
      mpi_world, loop.get_state(),
      [&bundle](int a, int b) { bundle.newForeground(a, b); }, params);

  /*    if (!system_params.template get<bool>("block_sigma8_sampler", true))
      bundle.sigma8_sampler = new GenericSigma8Sampler(bundle.comm);
    else
      bundle.sigma8_sampler = 0;
*/

  std::string algorithm_name =
      params.template get<std::string>("hades.algorithm", "HMC");

  if (algorithm_name == "HMC") {
    // -----------------------------------
    // HMC algorithm initialization

    double maxEpsilon = params.template get<double>("hades.max_epsilon", 0.02);
    int maxTimeSteps = params.template get<int>("hades.max_timesteps", 100);
    double kmax = params.template get<double>("hades.kmax", 0);
    std::string I_scheme_s =
        params.template get<std::string>("hades.scheme", "SI_2A");
    HMCOption::IntegratorScheme I_scheme = get_Scheme(I_scheme_s);
    auto density_mc =
        std::make_unique<HMCDensitySampler>(mpi_world, likelihood, kmax);
    density_mc->setIntegratorScheme(I_scheme);
    density_mc->setMaxEpsilon(maxEpsilon);
    density_mc->setMaxTimeSteps(maxTimeSteps);
    // HMC algorithm initialization - end
    // -----------------------------------
    bundle.density_mc = std::move(density_mc);
    //  } else if (algorithm_name == "QN-HMC") {
    //    double maxEpsilon = params.template get<double>("hades.max_epsilon", 0.02);
    //    int maxTimeSteps = params.template get<int>("hades.max_timesteps", 100);
    //    std::string I_scheme_s =
    //        params.template get<std::string>("hades.scheme", "SI_2A");
    //    HMCOption::IntegratorScheme I_scheme = get_Scheme(I_scheme_s);
    //    auto density_mc =
    //        std::make_unique<QNHMCDensitySampler>(mpi_world, likelihood);
    //    density_mc->setIntegratorScheme(I_scheme);
    //    density_mc->setMaxEpsilon(maxEpsilon);
    //    density_mc->setMaxTimeSteps(maxTimeSteps);
    //    bundle.density_mc = std::move(density_mc);
  } else if (algorithm_name == "FROZEN-PHASE") {
      auto density_mc =
          std::make_unique<FrozenPhaseDensitySampler>(mpi_world, likelihood);

      if (auto phase_file =
              params.template get_optional<std::string>("hades.phases")) {
        // A file containing phases is providing. Schedule for loading.
        density_mc->setPhaseFile(
            *phase_file,
            params.template get<std::string>("hades.phasesDataKey"));
      } else {
        if (!params.template get<bool>("hades.noPhasesProvided"))
          error_helper<ErrorParams>("If no phases are provided, "
                                    "noPhasesProvided must be set to true.");
      }
      bundle.density_mc = std::move(density_mc);
  } else {
    error_helper<ErrorBadState>(
        "Invalid algorithm name: " + algorithm_name +
        " (choice is HMC or QN-HMC)");
  }

  bool hblock = adapt_optional<bool>(
      loop.get_state(), block_loop_params, "hades_sampler_blocked", false,
      DO_NOT_RESTORE);
  adapt_optional<bool>(
      loop.get_state(), block_loop_params, "bias_sampler_blocked", false,
      DO_NOT_RESTORE);
  adapt_optional<bool>(
      loop.get_state(), block_loop_params, "nmean_sampler_blocked", false,
      DO_NOT_RESTORE);

  Console::instance().print<LOG_INFO_SINGLE>(
      format("Hades mixing per mcmc step is %d") % hades_mixing);
  Console::instance().print<LOG_INFO_SINGLE>(
      format("Hades density is blocked: %s") % (hblock ? "YES" : "NO"));

  loop << bundle.dummy_ps << bundle.sel_updater;

  py::list samplers;
  if (!sampler_setup) {
    error_helper<ErrorBadState>(
        "Sampler algorithm builder has not been registered");
  }
  try {
    samplers = sampler_setup(&state, like_info);
  } catch (pybind11::error_already_set const &e) {
    Console::instance().print<LOG_ERROR>(
        "An error was thrown by python: ");
    Console::instance().print<LOG_ERROR>(LibLSS::tokenize(e.what(), "\n"));
    error_helper<ErrorBadState>("Python thrown an unrecoverable error.");
  }

  // ==================
  // MAIN LOOP PROGRAM
  if (bias != 0) {
    auto bias_loop = new BlockLoop(1);
    *bias_loop << *bias;

    loop
        << (BlockLoop(hades_mixing)
            << *bundle.density_mc << *bias_loop
            << (BlockLoop(10) << bundle.foreground_block));
    delete bias_loop;
  } else {
    loop
        << (BlockLoop(hades_mixing)
            << *bundle
                    .density_mc); //<< (BlockLoop(10) << bundle.foreground_block);
  }
  for (auto &py_sampler : samplers) {
    auto new_ref = hold_python_with_ref<MarkovSampler>(py_sampler);
    loop << new_ref;
  }

  // If active, sample sigma8
  //    if (bundle.sigma8_sampler != 0)
  //      loop << *bundle.sigma8_sampler;
}

void LibLSS::sampler_setup_ic(
    SamplerBundle &bundle, MainLoop &loop,
    LibLSS_prepare::ptree const &params) {
  MarkovState &state = loop.get_state();

  if (bundle.delegate_ic_to_python) {
    py::object scope = py::module::import("__main__").attr("__dict__");
    try {
      ic_setup(&state);
    } catch (pybind11::error_already_set const &e) {
      Console::instance().print<LOG_ERROR>(
          "An error was thrown by python: " + std::string(e.what()));
      error_helper<ErrorBadState>("Python thrown an unrecoverable error.");
    }
  } else {
    bool random_ic = params.template get<bool>("mcmc.random_ic", true);
    if (random_ic)
      generateRandomField(bundle.comm, state);

    double initialRandomScaling =
        params.template get<double>("mcmc.init_random_scaling", 0.1);

    state.get<CArrayType>("s_hat_field")->eigen() *= initialRandomScaling;
    state.get<ArrayType>("s_field")->eigen() *= initialRandomScaling;
  }
}
