/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/src/julia_bundle_init.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __HADES_JULIA_BUNDLE_INIT_HPP
#define __HADES_JULIA_BUNDLE_INIT_HPP

#include "julia_bundle.hpp"
#include "libLSS/hmclet/julia_slice.hpp"
#include "libLSS/hmclet/julia_hmclet.hpp"
#include "likelihood_info.hpp"
#include "libLSS/samplers/rgen/qnhmc/qnhmc_density_sampler.hpp"
#include "libLSS/samplers/core/generate_random_field.hpp"
#include "setup_models.hpp"

namespace LibLSS {

  template <typename ptree>
  void sampler_bundle_init(
      MPI_Communication *mpi_world, ptree &params, SamplerBundle &bundle,
      MainLoop &loop, bool resuming) {
    using boost::format;
    using CosmoTool::square;
    using std::string;
    ptree system_params = params.get_child("system");
    ptree julia_params = params.get_child("julia");
    auto block_loop_params = params.get_child_optional("block_loop");

    auto borg_params = params.get_child("gravity");

    int hades_mixing = params.template get<int>("hades.mixing", 20);
    std::string lh_type =
        params.template get<std::string>("hades.likelihood", "LINEAR");
    std::shared_ptr<MarkovSampler> nmean, bias;
    typedef GridDensityLikelihoodBase<3> grid_t;
    std::shared_ptr<grid_t> likelihood;

    MarkovState &state = loop.get_state();
    auto &cons = Console::instance();

    BorgModelElement *model = new BorgModelElement();
    model->obj = 0;
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

    model->obj = buildModel(
        MPI_Communication::instance(), state, box, params, borg_params);

    string code_path = julia_params.template get<string>("likelihood_path");
    string module_name = julia_params.template get<string>("likelihood_module");
    string bias_sampler_type =
        julia_params.template get<string>("bias_sampler_type");
    //  string bias_sampler = julia_params.template get<string>("bias_sampler");

    LikelihoodInfo like_info;
    LibLSS_prepare::setupLikelihoodInfo(
        mpi_world, loop.get_state(), like_info, params, resuming);

    likelihood = bundle.julia_likelihood =
        std::make_shared<JuliaDensityLikelihood>(
            bundle.comm, like_info, code_path, module_name);
    bundle.delegate_ic_to_julia =
        julia_params.template get<bool>("ic_in_julia", false);

    auto burnin = julia_params.template get<size_t>("mass_burnin", 300);
    auto memory = julia_params.template get<size_t>("mass_burnin_memory", 50);
    if (bias_sampler_type == "hmclet") {
      auto hmclet_maxEpsilon =
          julia_params.template get_optional<double>("hmclet_maxEpsilon");
      auto hmclet_maxNtime =
          julia_params.template get_optional<int>("hmclet_maxNtime");
      auto hmcMatrix =
          julia_params.template get<std::string>("hmclet_matrix", "DIAGONAL");
      auto massScaling =
          julia_params.template get<double>("hmclet_massScale", 0.);
      auto limiter =
          julia_params.template get<double>("hmclet_correlationLimiter", 0.5);
      auto frozen = julia_params.template get<bool>("hmclet_frozen", false);
      JuliaHmclet::types::MatrixType matrixType = JuliaHmclet::types::DIAGONAL;

      if (hmcMatrix == "DIAGONAL")
        matrixType = JuliaHmclet::types::DIAGONAL;
      else if (hmcMatrix == "DENSE")
        matrixType = JuliaHmclet::types::DENSE;
      else if (hmcMatrix == "QN_DIAGONAL")
        matrixType = JuliaHmclet::types::QN_DIAGONAL;
      else {
        error_helper<ErrorBadState>(
            "Invalid matrix type for HMC: " + hmcMatrix);
      }

      Console::instance().print<LOG_INFO>("Build hmclet");

      auto julia_hmclet = std::make_shared<JuliaHmcletMeta>(
          bundle.comm, bundle.julia_likelihood, module_name, matrixType, burnin,
          memory, limiter, frozen);
      julia_hmclet->postinit().ready(
          [julia_hmclet, hmclet_maxEpsilon, hmclet_maxNtime,
           massScaling]() -> void {
            Console &cons = Console::instance();
            cons.print<LOG_VERBOSE>(
                format("Number of hmclets = %d") %
                julia_hmclet->hmclets().size());
            for (auto &hmc : julia_hmclet->hmclets()) {
              if (hmclet_maxEpsilon) {
                cons.print<LOG_VERBOSE>(
                    format("Setup hmclet epsilon=%g") % *hmclet_maxEpsilon);
                hmc->setMaxEpsilon(*hmclet_maxEpsilon);
              }
              if (hmclet_maxNtime) {
                cons.print<LOG_VERBOSE>(
                    format("Setup hmclet ntime=%d") % *hmclet_maxNtime);
                hmc->setMaxNtime(*hmclet_maxNtime);
              }
              hmc->setMassScaling(massScaling);
            }
          });
      bias = bundle.bias = julia_hmclet;
    } else if (bias_sampler_type == "slice") {
      bias = bundle.bias = std::make_shared<JuliaMetaSlice>(
          bundle.comm, module_name, bundle.julia_likelihood, burnin, memory);
    } else if (bias_sampler_type == "none") {
    } else {
      error_helper<ErrorParams>("Unknown bias sampler type");
    }

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

      double maxEpsilon =
          params.template get<double>("hades.max_epsilon", 0.02);
      int maxTimeSteps = params.template get<int>("hades.max_timesteps", 100);
      std::string I_scheme_s =
          params.template get<std::string>("hades.scheme", "SI_2A");
      HMCOption::IntegratorScheme I_scheme = get_Scheme(I_scheme_s);
      auto density_mc =
          std::make_unique<HMCDensitySampler>(mpi_world, likelihood);
      density_mc->setIntegratorScheme(I_scheme);
      density_mc->setMaxEpsilon(maxEpsilon);
      density_mc->setMaxTimeSteps(maxTimeSteps);
      // HMC algorithm initialization - end
      // -----------------------------------
      bundle.density_mc = std::move(density_mc);
    } else if (algorithm_name == "QN-HMC") {
      double maxEpsilon =
          params.template get<double>("hades.max_epsilon", 0.02);
      int maxTimeSteps = params.template get<int>("hades.max_timesteps", 100);
      std::string I_scheme_s =
          params.template get<std::string>("hades.scheme", "SI_2A");
      HMCOption::IntegratorScheme I_scheme = get_Scheme(I_scheme_s);
      auto density_mc =
          std::make_unique<QNHMCDensitySampler>(mpi_world, likelihood);
      density_mc->setIntegratorScheme(I_scheme);
      density_mc->setMaxEpsilon(maxEpsilon);
      density_mc->setMaxTimeSteps(maxTimeSteps);
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

    // ==================
    // MAIN LOOP PROGRAM
    if (bias != 0) {
      auto bias_loop = new BlockLoop(1);
      if (bias != 0)
        *bias_loop << *bias;

      loop
          << (BlockLoop(hades_mixing)
              << *bundle.density_mc << *bias_loop
              << (BlockLoop(10) << bundle.foreground_block));
      delete bias_loop;
    } else {
      loop << (BlockLoop(hades_mixing) << *bundle.density_mc)
           << (BlockLoop(10) << bundle.foreground_block);
    }

    // If active, sample sigma8
    //    if (bundle.sigma8_sampler != 0)
    //      loop << *bundle.sigma8_sampler;
  }

  template <typename ptree>
  void
  sampler_setup_ic(SamplerBundle &bundle, MainLoop &loop, ptree const &params) {
    MarkovState &state = loop.get_state();

    if (bundle.delegate_ic_to_julia)
      bundle.julia_likelihood->generateInitialConditions(state);
    else {
      generateRandomField(bundle.comm, state);
      double initialRandomScaling =
          params.template get<double>("mcmc.init_random_scaling", 0.1);

      state.get<CArrayType>("s_hat_field")->eigen() *= initialRandomScaling;
      state.get<ArrayType>("s_field")->eigen() *= initialRandomScaling;
    }
  }

  void sampler_bundle_cleanup() {}

} // namespace LibLSS

#endif
