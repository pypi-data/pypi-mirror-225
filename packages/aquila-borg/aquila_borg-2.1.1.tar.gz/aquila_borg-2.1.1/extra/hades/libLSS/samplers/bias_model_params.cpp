/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/samplers/bias_model_params.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/tools/fftw_allocator.hpp"
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/physics/forward_model.hpp"
#include <vector>
#include "libLSS/samplers/bias_model_params.hpp"
#include "libLSS/samplers/rgen/slice_sweep.hpp"

using namespace LibLSS;

BiasModelParamsSampler::BiasModelParamsSampler(
    MPI_Communication *comm_,
    std::shared_ptr<GridDensityLikelihoodBase<3>> likelihood_,
    std::shared_ptr<BORGForwardModel> model_, int numBias_,
    std::string const &prefix_)
    : MarkovSampler(), comm(comm_), likelihood(likelihood_), model(model_),
      numBias(numBias_), biasElement(0), prefix(prefix_) {}

BiasModelParamsSampler::~BiasModelParamsSampler() {}

void BiasModelParamsSampler::initialize(MarkovState &state) { restore(state); }

void BiasModelParamsSampler::restore(MarkovState &state) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  if (!model) {
    error_helper<ErrorBadState>("Model for BiasModelParams is invalid");
  }
  state.newElement(
      prefix + "model_params_bias",
      biasElement = new ArrayType1d(boost::extents[numBias]), true);
  auto default_values = boost::any_cast<LibLSS::multi_array<double, 1>>(
      model->getModelParam("bias", "biasParameters"));
  fwrap(*biasElement->array) = default_values;
  biasElement->subscribeLoaded([this]() {
    model->setModelParams({{"biasParameters", *biasElement->array}});
  });
}

void BiasModelParamsSampler::sample(MarkovState &state) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  auto const &x_density = *state.get<CArrayType>("s_hat_field")->array;
  double const ares_heat = state.getScalar<double>("ares_heat");

  RandomGen *rng = state.get<RandomGen>("random_generator");

  if (pre_hook)
    pre_hook();

  likelihood->updateMetaParameters(state);

  auto &biasParams = *biasElement->array;

  for (size_t i = 0; i < numBias; i++) {
    if (bias_to_freeze.find(i) != bias_to_freeze.end())
      continue;

    auto tmpParams = biasParams;
    ctx.format2<LOG_VERBOSE>("Sampling bias model %d", i);
    biasParams[i] = slice_sweep_double(
        comm, rng->get(),
        [&](double x) {
          ModelDictionnary this_param_map;
          tmpParams[i] = x;
          this_param_map["biasParameters"] = tmpParams;
          try {
            model->setModelParams(this_param_map);
          } catch (outOfBoundParam const &) {
            return -std::numeric_limits<double>::infinity();
          }
          double log_L = -likelihood->logLikelihood(x_density, false);
          ctx.format2<LOG_VERBOSE>("log_L = %g", log_L);
          return ares_heat * log_L;
        },
        biasParams[i], 1.);

    comm->broadcast_t(&biasParams[i], 1, 0);
  }

  ModelDictionnary this_param_map;
  this_param_map["biasParameters"] = biasParams;
  model->setModelParams(this_param_map);
  likelihood->logLikelihood(x_density, false);
  likelihood->commitAuxiliaryFields(state);

  if (post_hook)
    post_hook();
}
