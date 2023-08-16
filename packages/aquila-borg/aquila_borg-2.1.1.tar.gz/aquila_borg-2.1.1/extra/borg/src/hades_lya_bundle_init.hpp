/*+
    ARES/HADES/BORG Package -- ./extra/borg/src/hades_lya_bundle_init.hpp
    Copyright (C) 2020 Natalia Porqueres <n.porqueres@imperial.ac.uk>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __HADES_LYA_BUNDLE_INIT_HPP
#define __HADES_LYA_BUNDLE_INIT_HPP

#include "hades_lya_bundle.hpp"
#include "libLSS/samplers/rgen/qnhmc/qnhmc_density_sampler.hpp"
#include "libLSS/samplers/core/generate_random_field.hpp"
#include "setup_models.hpp"
//#include "libLSS/samplers/model_params.hpp"

namespace LibLSS {

template<typename ptree>
void sampler_bundle_init(
	MPI_Communication *mpi_world, ptree &params, SamplerBundle &bundle,
    MainLoop &loop,  bool resuming) {
    using boost::format;
    using CosmoTool::square;
    auto system_params = params.get_child("system");
    auto block_loop_params = params.get_child_optional("block_loop");
    auto borg_params = params.get_child("gravity_model");

    int hades_mixing = params.template get<int>("hades.mixing", 20);
    std::string lh_type =
        params.template get<std::string>("hades.likelihood", "BORG_LYA");
    std::shared_ptr<MarkovSampler> nmean, bias;
    MarkovSampler *model_error = 0;
    MarkovState &state = loop.get_state();
    Console &cons = Console::instance();
    typedef GridDensityLikelihoodBase<3> grid_t;
    std::shared_ptr<grid_t> likelihood;
    std::string model_type = borg_params.template get<std::string>("model", "LPT_CIC");

    grid_t::GridSizes N = {size_t(state.getScalar<long>("N0")),
                           size_t(state.getScalar<long>("N1")),
                           size_t(state.getScalar<long>("N2"))};
    grid_t::GridLengths L = {state.getScalar<double>("L0"),
                             state.getScalar<double>("L1"),
                             state.getScalar<double>("L2")};
    grid_t::GridLengths corners = {state.getScalar<double>("corner0"),
                                   state.getScalar<double>("corner1"),
                                   state.getScalar<double>("corner2")};

    LikelihoodInfo like_info;
    BorgModelElement *model = new BorgModelElement();
    loop.get_state().newElement("BORG_model", model);

#ifdef HADES_SUPPORT_BORG
    loop.get_state().newScalar("BORG_version", BORG_GIT_VERSION);
#endif
    LibLSS_prepare::setupLikelihoodInfo(
        mpi_world, loop.get_state(), like_info, params, resuming);
        
    bool rsd = adapt<bool>(state, params, "gravity_model.do_rsd", false);
    
    if (model_type != "") {
      int ss_factor = adapt<int>(state, borg_params, "supersampling", 1);
      int f_factor = adapt<int>(state, borg_params, "forcesampling", ss_factor);
      double ai = adapt<double>(
          state, borg_params, "a_initial", 0.001, RESTORE, "borg_a_initial");
      double af =
          adapt<double>(state, borg_params, "a_final", 1.0, RESTORE, "borg_a_final");
      double z_start = adapt<double>(state, borg_params, "pm_start_z", 69.);
      int pm_nsteps = adapt<int>(state, borg_params, "pm_nsteps", 30);
      double p_factor = adapt<double>(state, borg_params, "part_factor", 1.2);
      bool lightcone = adapt<bool>(state, borg_params, "lightcone", false);
      bool tcola = adapt<bool>(state, borg_params, "tCOLA", false);
      BoxModel box;

      box.xmin0 = state.getScalar<double>("corner0");
      box.xmin1 = state.getScalar<double>("corner1");
      box.xmin2 = state.getScalar<double>("corner2");
      box.L0 = L[0];
      box.L1 = L[1];
      box.L2 = L[2];
      box.N0 = N[0];
      box.N1 = N[1];
      box.N2 = N[2];

      model->obj = buildModel(
        MPI_Communication::instance(), state, box, params, borg_params);
        
    }

	if (lh_type == "BORG_LYALPHA") {
	  auto lya_bundle = std::make_unique<LyAlphaBorgBundle>(like_info);
	  bundle.hades_lya_bundle = std::move(lya_bundle);
      likelihood = bundle.hades_lya_bundle->likelihood;
    } else if (lh_type == "BORG_LYALPHA_RSD") {
	  auto lya_rsd_bundle = std::make_unique<LyAlphaRsdBorgBundle>(like_info);
	  // Hack the bias sampler
      bundle.hades_lya_rsd_bundle = std::move(lya_rsd_bundle);
      likelihood = bundle.hades_lya_rsd_bundle->likelihood;
    } else {
      error_helper<ErrorParams>("Unknown Hades likelihood " + lh_type);
    }

	if (!likelihood) {
      error_helper<ErrorParams>("Unknown Hades likelihood " + lh_type);
    }

    
    cons.print<LOG_STD>("Selected Hades likelihood: " + lh_type);
    
    if (!system_params.template get<bool>("block_sigma8_sampler", true))
      bundle.sigma8_sampler =
          std::make_unique<GenericSigma8Sampler>(bundle.comm);

    std::string algorithm_name = params.template get<std::string>("hades.algorithm","HMC");
    
    if (algorithm_name == "HMC") {
      // -----------------------------------
      // HMC algorithm initialization

      double maxEpsilon = params.template get<double>("hades.max_epsilon", 0.02);
      int maxTimeSteps = params.template get<int>("hades.max_timesteps", 100);
      std::string I_scheme_s =
          params.template get<std::string>("hades.scheme", "SI_2A");
      HMCOption::IntegratorScheme I_scheme = get_Scheme(I_scheme_s);
      auto density_mc = std::make_unique<HMCDensitySampler>(mpi_world, likelihood);
      density_mc->setIntegratorScheme(I_scheme);
      density_mc->setMaxEpsilon(maxEpsilon);
      density_mc->setMaxTimeSteps(maxTimeSteps);
      // HMC algorithm initialization - end
      // -----------------------------------
      bundle.density_mc = std::move(density_mc);
    
    } else if (algorithm_name == "QN-HMC") {
      double maxEpsilon = params.template get<double>("hades.max_epsilon", 0.02);
      int maxTimeSteps = params.template get<int>("hades.max_timesteps", 100);
      std::string I_scheme_s =
          params.template get<std::string>("hades.scheme", "SI_2A");
      HMCOption::IntegratorScheme I_scheme = get_Scheme(I_scheme_s);
      auto density_mc = std::make_unique<QNHMCDensitySampler>(mpi_world, likelihood);
      density_mc->setIntegratorScheme(I_scheme);
      density_mc->setMaxEpsilon(maxEpsilon);
      density_mc->setMaxTimeSteps(maxTimeSteps);
      bundle.density_mc = std::move(density_mc);
    } else {
      error_helper<ErrorBadState>("Invalid algorithm name: " + algorithm_name + " (choice is HMC or QN-HMC)");
    }
    
    bool hblock = adapt_optional<bool>(
        loop.get_state(), block_loop_params, "hades_sampler_blocked", false, DO_NOT_RESTORE);
    adapt_optional<bool>(loop.get_state(), block_loop_params, "bias_sampler_blocked", false, DO_NOT_RESTORE);
    adapt_optional<bool>(
        loop.get_state(), block_loop_params, "nmean_sampler_blocked", false, DO_NOT_RESTORE);

    Console::instance().print<LOG_INFO_SINGLE>(
        format("Hades mixing per mcmc step is %d") % hades_mixing);
    Console::instance().print<LOG_INFO_SINGLE>(
        format("Hades density is blocked: %s") % (hblock ? "YES" : "NO"));

	//loop << bundle.dummy_ps << bundle.sel_updater;
	
    // ==================
    // MAIN LOOP PROGRAM
    if (nmean != 0 && bias) {
      auto bias_loop = new BlockLoop(10);
      if (nmean != 0)
        *bias_loop << *nmean;
      if (bias)
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

    if (model_error != 0)
      loop << *model_error;

    // Only do observer vobs sampling  if we know how to sample vobs and rsd is
    // activated.
    if (rsd && bundle.borg_vobs)
      loop << *bundle.borg_vobs;

#ifdef HADES_SUPPORT_BORG
    // If active, sample sigma8
    if (bundle.sigma8_sampler != 0)
      loop << *bundle.sigma8_sampler;
#endif

}

template <typename ptree>
  void
  sampler_setup_ic(SamplerBundle &bundle, MainLoop &loop, ptree const &params) {
    MarkovState &state = loop.get_state();

    generateRandomField(bundle.comm, state);
    double initialRandomScaling =
        params.template get<double>("mcmc.init_random_scaling", 0.1);
    state.get<CArrayType>("s_hat_field")->eigen() *= initialRandomScaling;
    state.get<ArrayType>("s_field")->eigen() *= initialRandomScaling;
  }

void sampler_bundle_cleanup() {}

} // namespace

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Natalia Porqueres
// ARES TAG: email(0) = n.porqueres@imperial.ac.uk
// ARES TAG: year(0) = 2020

