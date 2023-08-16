/*+
    ARES/HADES/BORG Package -- ./extra/hades/src/hades_bundle_init.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __HADES_BUNDLE_INIT_HPP
#define __HADES_BUNDLE_INIT_HPP

#include "hades_bundle.hpp"
#ifdef HADES_SUPPORT_BORG
#  include "libLSS/samplers/rgen/qnhmc/qnhmc_density_sampler.hpp"
#  include "libLSS/physics/bias/passthrough.hpp"
#  include "libLSS/samplers/altair/altair_meta_sampler.hpp"
#endif
#include "libLSS/samplers/core/generate_random_field.hpp"
#include "libLSS/samplers/rgen/frozen/frozen_phase_density_sampler.hpp"
#include "libLSS/samplers/generic/generic_sigma8_second.hpp"
#include "libLSS/physics/likelihoods/eft.hpp"
#include "setup_models.hpp"
#include "libLSS/samplers/model_params.hpp"
#include "libLSS/physics/haar.hpp"
#include "libLSS/samplers/bias_model_params.hpp"

namespace LibLSS {

  template <typename ptree>
  void sampler_bundle_init(
      MPI_Communication *mpi_world, ptree &params, SamplerBundle &bundle,
      MainLoop &loop, bool resuming) {
    LIBLSS_AUTO_CONTEXT(LOG_INFO_SINGLE, ctx);
    using boost::format;
    using CosmoTool::square;
    auto system_params = params.get_child("system");
    auto block_loop_params = params.get_child_optional("block_loop");
    auto borg_params = params.get_child("gravity");

    int hades_mixing = params.template get<int>("hades.mixing", 20);
    int bias_mixing = params.template get<int>("hades.bias_mixing", 10);
    std::string lh_type =
        params.template get<std::string>("hades.likelihood", "LINEAR");
    std::shared_ptr<MarkovSampler> nmean, bias;
    MarkovSampler *model_error = 0;
    MarkovState &state = loop.get_state();
    Console &cons = Console::instance();
    typedef GridDensityLikelihoodBase<3> grid_t;
    std::shared_ptr<grid_t> likelihood;

    grid_t::GridSizes N = {
        size_t(state.getScalar<long>("N0")),
        size_t(state.getScalar<long>("N1")),
        size_t(state.getScalar<long>("N2"))};
    grid_t::GridLengths L = {
        state.getScalar<double>("L0"), state.getScalar<double>("L1"),
        state.getScalar<double>("L2")};
    grid_t::GridLengths corners = {
        state.getScalar<double>("corner0"), state.getScalar<double>("corner1"),
        state.getScalar<double>("corner2")};

    LikelihoodInfo like_info;
    BorgModelElement *model = new BorgModelElement();
    loop.get_state().newElement("BORG_model", model);

#ifdef HADES_SUPPORT_BORG
    loop.get_state().newScalar("BORG_version", BORG_GIT_VERSION);
#endif
    LibLSS_prepare::setupLikelihoodInfo(
        mpi_world, loop.get_state(), like_info, params, resuming);
    bool rsd = adapt<bool>(state, params, "gravity.do_rsd", true);

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

    if (lh_type == "LINEAR") {
      bundle.hades_bundle = std::make_unique<LinearBundle>(like_info);
      likelihood = bundle.hades_bundle->likelihood;
    }
#ifdef HADES_SUPPORT_BORG
    else if (lh_type == "BORG_POISSON") {
      auto poisson_bundle = std::make_unique<PoissonBorgBundle>(like_info);
      // Hack the bias sampler
      poisson_bundle->hades_meta =
          std::make_shared<BorgPoissonBiasSampler>(bundle.comm);
      nmean = std::make_shared<BorgPoissonNmeanSampler>(bundle.comm);
      bundle.hades_bundle = std::move(poisson_bundle);
      bundle.borg_vobs = std::make_unique<BorgPoissonVobsSampler>(bundle.comm);
      likelihood = bundle.hades_bundle->likelihood;
    } else {
      typedef std::shared_ptr<MarkovSampler> markov_ptr;
      std::map<
          std::string,
          std::function<std::shared_ptr<VirtualGenericBundle>(
              ptree &, std::shared_ptr<GridDensityLikelihoodBase<3>> &,
              markov_ptr &, markov_ptr &, markov_ptr &,
              std::function<MarkovSampler *(int, int)> &, LikelihoodInfo &)>>
          generic_map{
              {"GAUSSIAN_BROKEN_POWERLAW_BIAS",
               create_generic_bundle<
                   AdaptBias_Gauss<bias::BrokenPowerLaw>, GaussianLikelihood,
                   ptree &>},
              {"GAUSSIAN_MO_WHITE_BIAS",
               create_generic_bundle<
                   AdaptBias_Gauss<bias::DoubleBrokenPowerLaw>,
                   GaussianLikelihood, ptree &>},
              {"GAUSSIAN_POWERLAW_BIAS", create_generic_bundle<
                                             AdaptBias_Gauss<bias::PowerLaw>,
                                             GaussianLikelihood, ptree &>},
              {"POISSON",
               create_generic_bundle<
                   bias::Passthrough, VoxelPoissonLikelihood, ptree &>},
              // FS: for now, disallow bundling of EFTBias to GaussianLikelihood
              // {"EFT_BIAS_WITH_THRESHOLDER",
              //  create_generic_bundle<
              //      bias::EFTBias<true>, GaussianLikelihood,
              //      ptree &>},
              {"GENERIC_POISSON_POWERLAW_BIAS",
               create_generic_bundle<
                   bias::PowerLaw, VoxelPoissonLikelihood, ptree &>},
              {"GENERIC_POISSON_POWERLAW_BIAS_DEGRADE4",
               create_generic_bundle<
                   bias::Downgrader<bias::PowerLaw>, VoxelPoissonLikelihood,
                   ptree &>},
              {"GENERIC_POISSON_BROKEN_POWERLAW_BIAS_DEGRADE4",
               create_generic_bundle<
                   bias::Downgrader<bias::BrokenPowerLaw>,
                   VoxelPoissonLikelihood, ptree &>},
              {"GENERIC_POISSON_BROKEN_POWERLAW_BIAS",
               create_generic_bundle<
                   bias::BrokenPowerLaw, VoxelPoissonLikelihood, ptree &>},
              {"GENERIC_GAUSSIAN_LINEAR_BIAS",
               create_generic_bundle<
                   AdaptBias_Gauss<bias::LinearBias>, GaussianLikelihood,
                   ptree &>},
              {"GENERIC_GAUSSIAN_MANY_POWER_1^1",
               create_generic_bundle<
                   AdaptBias_Gauss<
                       bias::ManyPower<bias::ManyPowerLevels<double, 1>>>,
                   GaussianLikelihood, ptree &>},
              {"GENERIC_GAUSSIAN_MANY_POWER_1^2",
               create_generic_bundle<
                   AdaptBias_Gauss<
                       bias::ManyPower<bias::ManyPowerLevels<double, 1, 1>>>,
                   GaussianLikelihood, ptree &>},
              {"GENERIC_GAUSSIAN_MANY_POWER_1^4",
               create_generic_bundle<
                   AdaptBias_Gauss<bias::ManyPower<
                       bias::ManyPowerLevels<double, 1, 1, 1, 1>>>,
                   GaussianLikelihood, ptree &>},
              {"GENERIC_POISSON_POWER_LAW",
               create_generic_bundle<
                   bias::PowerLaw, VoxelPoissonLikelihood, ptree &>},
              {"GENERIC_POISSON_MANY_POWER_1^1",
               create_generic_bundle<
                   bias::ManyPower<bias::ManyPowerLevels<double, 1>>,
                   VoxelPoissonLikelihood, ptree &>},
              {"GENERIC_POISSON_MANY_POWER_1^2",
               create_generic_bundle<
                   bias::ManyPower<bias::ManyPowerLevels<double, 1, 1>>,
                   VoxelPoissonLikelihood, ptree &>},
              {"GENERIC_POISSON_MANY_POWER_2^2",
               create_generic_bundle<
                   bias::ManyPower<bias::ManyPowerLevels<double, 2, 2>>,
                   VoxelPoissonLikelihood, ptree &>},
              {"GENERIC_POISSON_MANY_POWER_1^4",
               create_generic_bundle<
                   bias::ManyPower<bias::ManyPowerLevels<double, 1, 1, 1, 1>>,
                   VoxelPoissonLikelihood, ptree &>},
              {"GENERIC_POISSON_MANY_POWER_2^4",
               create_generic_bundle<
                   bias::ManyPower<bias::ManyPowerLevels<double, 2, 2, 2, 2>>,
                   VoxelPoissonLikelihood, ptree &>},
              {"ROBUST_POISSON_POWERLAW_BIAS",
               create_generic_bundle<
                   bias::PowerLaw, RobustPoissonLikelihood, ptree &>},
              {"ROBUST_POISSON_BROKEN_POWERLAW_BIAS",
               create_generic_bundle<
                   bias::BrokenPowerLaw, RobustPoissonLikelihood, ptree &>},
              {"ROBUST_POISSON_MANY_POWER_1^1",
               create_generic_bundle<
                   bias::ManyPower<bias::ManyPowerLevels<double, 1>>,
                   RobustPoissonLikelihood, ptree &, true>},
              {"ROBUST_POISSON_MANY_POWER_1^2",
               create_generic_bundle<
                   bias::ManyPower<bias::ManyPowerLevels<double, 1, 1>>,
                   RobustPoissonLikelihood, ptree &, true>},
              {"ROBUST_POISSON_MANY_POWER_2^2",
               create_generic_bundle<
                   bias::ManyPower<bias::ManyPowerLevels<double, 2, 2>>,
                   RobustPoissonLikelihood, ptree &, true>},
              {"GENERIC_POISSON_MANY_POWER_4^1",
               create_generic_bundle<
                   bias::ManyPower<bias::ManyPowerLevels<double, 4>>,
                   VoxelPoissonLikelihood, ptree &>},
              {"GENERIC_POISSON_MANY_POWER_1^2_DEGRADE2",
               create_generic_bundle<
                   bias::Downgrader<
                       bias::ManyPower<bias::ManyPowerLevels<double, 1, 1>>,
                       bias::DegradeGenerator<1, 1>>,
                   VoxelPoissonLikelihood, ptree &>},
              {"GENERIC_POISSON_MANY_POWER_2^2_DEGRADE4",
               create_generic_bundle<
                   bias::Downgrader<
                       bias::ManyPower<bias::ManyPowerLevels<double, 2, 2>>,
                       bias::DegradeGenerator<1, 1, 1>>,
                   VoxelPoissonLikelihood, ptree &>},
              // FS: for now, disallow bundling of EFTBias to GaussianLikelihood
              // {"EFT_BIAS_GAUSS", create_generic_bundle<bias::EFTBiasDefault, GaussianLikelihood,ptree &>},
              {"EFT_BIAS_LIKE",
               create_generic_bundle<
                   bias::EFTBiasDefault, EFTLikelihood, ptree &>}};

      auto iter = generic_map.find(lh_type);
      if (iter != generic_map.end()) {
        bundle.borg_generic = iter->second(
            system_params, likelihood, nmean, bias, bundle.borg_vobs,
            bundle.foreground_sampler_generator, like_info);
        bundle.borg_vobs.reset();
      } else {
        error_helper<ErrorParams>(
            "Unknown Generic Hades likelihood " + lh_type);
      }
    }
#endif

    if (!likelihood) {
      error_helper<ErrorParams>("Unknown Hades likelihood " + lh_type);
    }

    if (!bias && bundle.hades_bundle && bundle.hades_bundle->hades_meta) {
      bias = bundle.hades_bundle->hades_meta;
    }

    cons.print<LOG_STD>("Selected Hades likelihood: " + lh_type);

    // Initialize foregrounds
    LibLSS_prepare::initForegrounds(
        mpi_world, state,
        [&bundle](int c, int a) { bundle.newForeground(c, a); }, params);

#ifdef HADES_SUPPORT_BORG
    bool sigma8block = adapt_optional<bool>(
        loop.get_state(), block_loop_params, "sigma8_sampler_blocked", true,
        DO_NOT_RESTORE);

    if (!sigma8block) {
      ctx.print("Sampling sigma8");
      bundle.sigma8_sampler =
          std::make_unique<GenericSigma8SecondVariantSampler>(
              bundle.comm, likelihood, like_info);
    }
#endif

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
      double kmax = params.template get<double>("hades.kmax", 0);
      HMCOption::IntegratorScheme I_scheme = get_Scheme(I_scheme_s);
      auto density_mc =
          std::make_unique<HMCDensitySampler>(mpi_world, likelihood, kmax);
      density_mc->setIntegratorScheme(I_scheme);
      density_mc->setMaxEpsilon(maxEpsilon);
      density_mc->setMaxTimeSteps(maxTimeSteps);
      if (auto phase_file =
              params.template get_optional<std::string>("hades.phases")) {
        // A file containing phases is providing. Schedule for loading.
        density_mc->setPhaseFile(
            *phase_file,
            params.template get<std::string>("hades.phasesDataKey"));
      }
      // HMC algorithm initialization - end
      // -----------------------------------
      if (params.template get("hades.haar", false)) {
        auto haar = std::make_shared<ForwardHaar>(bundle.comm, box, false);
        auto inverse_haar =
            std::make_shared<ForwardHaar>(bundle.comm, box, true);
        density_mc->setTransforms(haar, inverse_haar);
      }
      bundle.density_mc = std::move(density_mc);
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
#ifdef HADES_SUPPORT_BORG
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
#endif
    } else {
      error_helper<ErrorBadState>(
          "Invalid algorithm name: " + algorithm_name +
          " (choice is HMC, FROZEN-PHASE or QN-HMC)");
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

    //loop << bundle.dummy_ps;
    loop << bundle.sel_updater;

    // ==================
    // MAIN LOOP PROGRAM
    {
      auto bias_loop = new BlockLoop(bias_mixing);
      if (nmean &&
          loop.get_state().getScalar<bool>("nmean_sampler_blocked") == false)
        *bias_loop << nmean;
      if (bias)
        *bias_loop << bias;

      loop
          << (BlockLoop(hades_mixing)
              << *bundle.density_mc << *bias_loop
              << (BlockLoop(10) << bundle.foreground_block));
      delete bias_loop;
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
    if (params.template get<bool>("hades.altair", false)) {
      CosmologicalParameters bound_min, bound_max;
      bound_min.w = -1.5;
      bound_max.w = -0.5;
      bound_min.wprime = -1.5;
      bound_max.wprime = 1.5;
      bound_min.omega_m = 0.1;
      bound_max.omega_m = 0.9;
      bundle.ap_sampler = std::make_shared<AltairMetaSampler>(
          mpi_world, likelihood, model->obj, bound_min, bound_max, 0.01);
      loop << *bundle.ap_sampler;
    }
#endif
    {
      auto model_param_list = params.template get_optional<std::string>(
          "hades.model_params_to_set");
      if (model_param_list) {
        auto params_list =
            string_as_vector<std::string>(*model_param_list, ",");
        ModelDictionnary param_map;
        for (auto const &p : params_list) {
          auto equal = p.find("=");
          double value = 0.1;
          std::string name = p;
          if (equal != std::string::npos) {
            value = boost::lexical_cast<double>(p.substr(equal + 1));
            name = p.substr(0, equal);
          }
          param_map[name] = value;
        }
        model->obj->setModelParams(param_map);
      }
    }
    auto model_param_list = params.template get_optional<std::string>(
        "hades.model_params_to_sample");
    if (model_param_list) {
      auto params_list = string_as_vector<std::string>(*model_param_list, ",");
      std::vector<std::string> params_list2;

      ModelDictionnary param_map;
      for (auto const &p : params_list) {
        if (p.find("cosmology.", 0) == 0)
          continue;
        auto equal = p.find("=");
        double value = 0.1;
        std::string name = p;
        if (equal != std::string::npos) {
          value = boost::lexical_cast<double>(p.substr(equal + 1));
          name = p.substr(0, equal);
        }
        param_map[name] = value;
        params_list2.push_back(name);
      }
      loop << std::shared_ptr<MarkovSampler>(new ModelParamsSampler(
          bundle.comm, "", params_list2, likelihood, model->obj, param_map));
    }
    auto model_bias = params.template get_optional<int>("hades.model_bias");
    if (model_bias && *model_bias > 0) {
      loop << std::shared_ptr<MarkovSampler>(new BiasModelParamsSampler(
          bundle.comm, likelihood, model->obj, *model_bias, ""));
    }
  } // namespace LibLSS

  template <typename ptree>
  void
  sampler_setup_ic(SamplerBundle &bundle, MainLoop &loop, ptree const &params) {
    MarkovState &state = loop.get_state();
    double initialRandomScaling =
        params.template get<double>("mcmc.init_random_scaling", 0.1);

    bool random_ic = params.template get<bool>("mcmc.random_ic", true);
    if (random_ic)
      generateRandomField(bundle.comm, state);
    state.get<CArrayType>("s_hat_field")->eigen() *= initialRandomScaling;
    state.get<ArrayType>("s_field")->eigen() *= initialRandomScaling;

    bool scramble_bias = params.template get<bool>("mcmc.scramble_bias", false);
    if (scramble_bias) {
      int Ncat = state.getScalar<long>("NCAT");
      for (int i = 0; i < Ncat; i++) {
        auto &a = *(state.formatGet<ArrayType1d>("galaxy_bias_%d", i)->array);
        fwrap(a) = 0.01;
        a[0] = 1;
      }
    }
  }

  void sampler_bundle_cleanup() {}

} // namespace LibLSS

#endif
