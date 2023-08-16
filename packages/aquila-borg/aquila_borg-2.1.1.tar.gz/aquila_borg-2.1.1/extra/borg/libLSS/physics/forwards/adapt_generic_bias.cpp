/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/adapt_generic_bias.cpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <string>
#include <boost/core/demangle.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/physics/model_io.hpp"
#include "libLSS/physics/forwards/softplus.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/physics/forwards/registry.hpp"
#include "libLSS/tools/ptree_proxy.hpp"
#include "libLSS/physics/forwards/adapt_generic_bias.hpp"
#include "libLSS/physics/forwards/transfer.hpp"

using namespace LibLSS;

template <typename T>
void ForwardGenericBias<T>::commonSetup() {
  currentBiasParams.resize(boost::extents[bias_t::numParams]);

  dummyModel = std::make_shared<ForwardTransfer>(comm, box_input);

  if (bias)
    bias->setup_default(currentBiasParams);
}

template <typename T>
ForwardGenericBias<T>::~ForwardGenericBias() {
  if (!bias_cleaned)
    bias->cleanup();
}

template <typename T>
void ForwardGenericBias<T>::forwardModel_v2(ModelInput<3> delta_init) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  // Setup the IO basis that is required for this forward.
  delta_init.setRequestedIO(PREFERRED_REAL);

  hold_input = std::move(delta_init);

  if (!bias)
    rebuildBias();

  if (!bias_cleaned)
    bias->cleanup();

  std::ostringstream oss;
  oss << "bias Params = ";
  for (int i = 0; i < bias_t::numParams; i++)
    oss << currentBiasParams[i] << " ";
  ctx.print(oss.str());
  bias->prepare(
      *dummyModel, hold_input.getRealConst(),
      0., /* nmean is ignored generally now, it is only there for backward compatibility */
      currentBiasParams, true); //densityUpdated);
  bias_cleaned = false;
}

template <typename T>
void ForwardGenericBias<T>::getDensityFinal(ModelOutput<3> delta_output) {
  delta_output.setRequestedIO(PREFERRED_REAL);
  invalidDensity = false;
  fwrap(delta_output.getRealOutput()) =
      std::get<0>(bias->compute_density(hold_input.getRealConst()));
}

template <typename T>
void ForwardGenericBias<T>::adjointModel_v2(
    ModelInputAdjoint<3> in_gradient_delta) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  // Build strict range views (we do not want to see the
  // the FFTW padding, ensure that the view object lives till the end of this function.

  in_gradient_delta.setRequestedIO(PREFERRED_REAL);
  hold_ag_input = std::move(in_gradient_delta);
}

template <typename T>
void ForwardGenericBias<T>::getAdjointModelOutput(
    ModelOutputAdjoint<3> out_gradient_delta) {
  out_gradient_delta.setRequestedIO(PREFERRED_REAL);

  fwrap(out_gradient_delta.getRealOutput()) =
      std::get<0>(bias->apply_adjoint_gradient(
          hold_input.getRealConst(),
          std::make_tuple(std::cref(hold_ag_input.getRealConst()))));
}

template <typename T>
boost::any ForwardGenericBias<T>::getModelParam(
    std::string const &n, std::string const &param) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  ctx.format("modelName = %s, n = %s", modelName, n);
  if (n == modelName && param == "biasParameters") {
    if (!bias)
      rebuildBias();
    return currentBiasParams;
  }
  return boost::any();
}
template <typename T>
void ForwardGenericBias<T>::rebuildBias(std::shared_ptr<LikelihoodInfo> info)
{
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  if (!bias_cleaned && bias)
    bias->cleanup();
  if (!info)
    bias = std::make_shared<bias_t>();
  else
    bias = std::make_shared<bias_t>(*info);
  bias_cleaned = true;

  if (!biasSet) {
    bias->setup_default(currentBiasParams);
    biasSet = true;
  }
}

template <typename T>
void ForwardGenericBias<T>::setModelParams(
    ModelDictionnary const &model_params) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  {
    auto location = model_params.find("info");
    if (location != model_params.end()) {
      try {
        auto info =
            boost::any_cast<std::shared_ptr<LikelihoodInfo>>(location->second);

        rebuildBias(info);
      } catch (boost::bad_any_cast const &) {
        error_helper<ErrorBadState>(
            "Bad type in info parameters, was: " +
            std::string(boost::core::demangle(location->second.type().name())));
      }
    }
  }

  // TODO: find a way to disambiguate in case of several bias models...
  {
    auto location = model_params.find("biasParameters");
    if (location != model_params.end()) {
      // Retrieve the array.
      try {
        auto params =
            boost::any_cast<LibLSS::multi_array<double, 1>>(location->second);

        if (params.shape()[0] != bias_t::numParams) {
          throw std::invalid_argument("Invalid number of bias parameters");
        }

        if (!bias->check_bias_constraints(params)) {
          ctx.print("Failing constraints: " + LibLSS::to_string(params));
          throw outOfBoundParam("Fail bias constraints");
        }

        int diff;
        for (diff = 0; diff < bias_t::numParams; diff++)
          if (currentBiasParams[diff] != params[diff])
            break;
        ctx.format("Bias changed (diff=%d, numParams=%d)", diff, bias_t::numParams);
        if (diff != bias_t::numParams) {
          currentBiasParams = params;
          biasSet = true;
          invalidDensity = true;
        }
      } catch (boost::bad_any_cast const &e) {
        error_helper<ErrorBadState>(
            "Bad type in bias parameters, was: " +
            std::string(boost::core::demangle(location->second.type().name())));
      }
    }
  }

  // TODO: Remove the bias from the dictionnary before going upward.
  BORGForwardModel::setModelParams(model_params);
  return;
}

template <typename T>
static std::shared_ptr<BORGForwardModel> create_bias(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params) {
  auto model = std::make_shared<ForwardGenericBias<T>>(comm, box);
  return model;
}

AUTO_REGISTRATOR_IMPL(ForwardGenericBias);

#include "libLSS/physics/bias/noop.hpp"
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/physics/bias/linear_bias.hpp"
#include "libLSS/physics/bias/broken_power_law.hpp"
#include "libLSS/physics/bias/double_power_law.hpp"
#include "libLSS/physics/bias/many_power.hpp"
#include "libLSS/physics/bias/eft_bias.hpp"

namespace {
  void bias_registrator() {
    LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

    ForwardRegistry::instance().registerFactory(
        "bias::Noop", create_bias<bias::Noop>);
    ForwardRegistry::instance().registerFactory(
        "bias::Linear", create_bias<bias::LinearBias>);
    ForwardRegistry::instance().registerFactory(
        "bias::PowerLaw", create_bias<bias::PowerLaw>);
    ForwardRegistry::instance().registerFactory(
        "bias::BrokenPowerLaw", create_bias<bias::BrokenPowerLaw>);
    ForwardRegistry::instance().registerFactory(
        "bias::DoubleBrokenPowerLaw", create_bias<bias::DoubleBrokenPowerLaw>);
    ForwardRegistry::instance().registerFactory(
        "bias::ManyPower_1^1",
        create_bias<bias::ManyPower<bias::ManyPowerLevels<double, 1>>>);
    ForwardRegistry::instance().registerFactory(
        "bias::ManyPower_1^2",
        create_bias<bias::ManyPower<bias::ManyPowerLevels<double, 1, 1>>>);
    ForwardRegistry::instance().registerFactory(
        "bias::ManyPower_1^4",
        create_bias<
            bias::ManyPower<bias::ManyPowerLevels<double, 1, 1, 1, 1>>>);
    ForwardRegistry::instance().registerFactory(
        "bias::ManyPower_2^2",
        create_bias<bias::ManyPower<bias::ManyPowerLevels<double, 2, 2>>>);
    ForwardRegistry::instance().registerFactory(
        "bias::EFT", create_bias<bias::EFTBiasDefault>);
    ForwardRegistry::instance().registerFactory(
        "bias::EFT_Thresh", create_bias<bias::EFTBiasThresh>);
  }

  RegisterStaticInit _initter(
      &bias_registrator,
      StaticInit::MIN_PRIORITY -
          1); // Bad priority patch. Basically we ask it to be run before the registry listing.
} // namespace

// ARES TAG: num_authors = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
