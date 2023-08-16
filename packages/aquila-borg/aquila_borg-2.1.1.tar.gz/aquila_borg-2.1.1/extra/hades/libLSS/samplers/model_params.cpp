/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/samplers/model_params.cpp
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
#include "libLSS/samplers/model_params.hpp"
#include "libLSS/samplers/rgen/slice_sweep.hpp"

using namespace LibLSS;

ModelParamsSampler::ModelParamsSampler(
    MPI_Communication *comm_, std::string const& prefix_, std::vector<std::string> const &params,
    std::shared_ptr<GridDensityLikelihoodBase<3>> likelihood_,
    std::shared_ptr<BORGForwardModel> model_, ModelDictionnary init)
    : MarkovSampler(), comm(comm_), paramsToSample(params),
      likelihood(likelihood_), model(model_), init_state(init), prefix(prefix_) {}

ModelParamsSampler::~ModelParamsSampler() {}

void ModelParamsSampler::initialize(MarkovState &state) { restore(state); }

void ModelParamsSampler::restore(MarkovState &state) {
  for (auto const &p : paramsToSample) {
    std::string pName = std::string("model_params_") + prefix + p;
    state
        .newScalar<double>(pName, boost::any_cast<double>(init_state[p]), true)
        ->subscribeLoaded([this, p, pName, &state]() {
          model->setModelParams({{p, state.getScalar<double>(pName)}});
        });
  }
  model->setModelParams(init_state);
}

void ModelParamsSampler::sample(MarkovState &state) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  auto const &x_density = *state.get<CArrayType>("s_hat_field")->array;
  double const ares_heat = state.getScalar<double>("ares_heat");

  RandomGen *rng = state.get<RandomGen>("random_generator");

  likelihood->updateMetaParameters(state);

  for (auto const &p : paramsToSample) {
    double &value = state.getScalar<double>(std::string("model_params_") + prefix + p);
    ctx.format2<LOG_VERBOSE>("Sampling model parameter '%s'", p);
    value = slice_sweep_double(
        comm, rng->get(),
        [&](double x) {
          ctx.format2<LOG_VERBOSE>("try x[%s] = %g", p, x);
          if (x < 0)
            return -std::numeric_limits<double>::infinity();
          ModelDictionnary this_param_map;
          this_param_map[p] = x;
          model->setModelParams(this_param_map);
          double log_L = -likelihood->logLikelihood(x_density, false);
          ctx.format2<LOG_VERBOSE>("log_L = %g", log_L);
          return ares_heat * log_L;
        },
        value, 1.);

    comm->broadcast_t(&value, 1, 0);

    ModelDictionnary this_param_map;
    this_param_map[p] = value;
    model->setModelParams(this_param_map);
  }
  likelihood->logLikelihood(x_density, false);
  likelihood->commitAuxiliaryFields(state);
}
