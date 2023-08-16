/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/generic/generic_sigma8_second.cpp
    Copyright (C) 2014-2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2018 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <CosmoTool/hdf5_array.hpp>
#include <CosmoTool/algo.hpp>
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/physics/cosmo_power.hpp"
#include "libLSS/samplers/generic/generic_sigma8_second.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/samplers/rgen/slice_sweep.hpp"
#include "libLSS/tools/fusewrapper.hpp"

using CosmoTool::square;
using namespace LibLSS;

GenericSigma8SecondVariantSampler::~GenericSigma8SecondVariantSampler() {}

GenericSigma8SecondVariantSampler::GenericSigma8SecondVariantSampler(
    MPI_Communication *comm_, Likelihood_t likelihood_, LikelihoodInfo info)
    : MarkovSampler(), comm(comm_), likelihood(likelihood_) {
  step_ansatz = Likelihood::query_default(info, "sigma8_step", 0.02);
  sigma8_min = Likelihood::query_default(info, "sigma8_min", 0.4);
  sigma8_max = Likelihood::query_default(info, "sigma8_max", 1.6);
  use_double = Likelihood::query_default<bool>(info, "sigma8_sample_double", true);
}

void GenericSigma8SecondVariantSampler::initialize(MarkovState &state) {
  N0 = state.getScalar<long>("N0");
  N1 = state.getScalar<long>("N1");
  N2 = state.getScalar<long>("N2");

  L0 = state.getScalar<double>("L0");
  L1 = state.getScalar<double>("L1");
  L2 = state.getScalar<double>("L2");

  Volume = L0 * L1 * L2;

  mgr = std::make_unique<DFT_Manager>(N0, N1, N2, comm);
}

void GenericSigma8SecondVariantSampler::restore(MarkovState &state) {
  initialize(state);
}

void GenericSigma8SecondVariantSampler::sample(MarkovState &state) {
  using boost::format;
  ConsoleContext<LOG_VERBOSE> ctx("sampling of sigma8 (likelihood variant)");
  auto &rgen = state.get<RandomGen>("random_generator")->get();
  CosmologicalParameters &cosmo_params =
      state.getScalar<CosmologicalParameters>("cosmology");

  CArrayType::ArrayType &s_hat_array =
      *state.get<CArrayType>("s_hat_field")->array;
  ArrayType::ArrayType &s_array = *state.get<ArrayType>("s_field")->array;

  double const step = step_ansatz;
  double next;
  double current = cosmo_params.sigma8;

  likelihood->updateMetaParameters(state);

  auto log_posterior = [&](double A) -> double {
    if (A < sigma8_min || A > sigma8_max) {
      ctx.format(
          "Failure with A=%g (sigma8_min=%g, sigma8_max=%g)", A, sigma8_min,
          sigma8_max);
      return -std::numeric_limits<double>::infinity();
    }
    CosmologicalParameters tmp_params = cosmo_params;
    tmp_params.sigma8 = A;
    ctx.format("Attempting sigma8 = %g", tmp_params.sigma8);
    likelihood->updateCosmology(tmp_params);
    double const L = -likelihood->logLikelihood(s_hat_array, false);
    ctx.format("log_L = %g", L);
    return L - std::log(A);
  };
  if (use_double)
    next = slice_sweep_double(comm, rgen, log_posterior, current, step);
  else
    next = slice_sweep(comm, rgen, log_posterior, current, step);

  cosmo_params.sigma8 = next;
  comm->broadcast_t(&cosmo_params.sigma8, 1, 0);
  ctx.format("New sigma8 is %g", cosmo_params.sigma8);

  likelihood->updateCosmology(cosmo_params);
  likelihood->logLikelihood(s_hat_array, false);
  likelihood->commitAuxiliaryFields(state);
}
// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2014-2018
// ARES TAG: name(1) = Jens Jasche
// ARES TAG: email(1) = jens.jasche@fysik.su.se
// ARES TAG: year(1) = 2009-2018
