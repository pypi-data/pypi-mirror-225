/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/altair/altair_meta_sampler.cpp
    Copyright (C) 2018-2020 Doogesh Kodi Ramanah <ramanah@iap.fr>
    Copyright (C) 2018-2021 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <CosmoTool/algo.hpp>
#include <cmath>
#include <Eigen/Core>
#include <boost/format.hpp>
#include <boost/bind.hpp>
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/samplers/core/gridLikelihoodBase.hpp"
#include "libLSS/tools/hermiticity_fixup.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/samplers/rgen/slice_sweep.hpp"
#include "libLSS/samplers/altair/altair_meta_sampler.hpp"
#include "libLSS/hmclet/mass_burnin.hpp"
#include "libLSS/hmclet/dense_mass.hpp"
#include "libLSS/hmclet/mass_saver.hpp"
#include <gsl/gsl_sf.h>

using namespace LibLSS;
using LibLSS::fwrap;

using boost::c_storage_order;
using boost::extents;
using CosmoTool::square;

typedef boost::multi_array_types::extent_range range;

void AltairMetaSampler::initialize(MarkovState &state) {

  long localN0, startN0;

  ConsoleContext<LOG_DEBUG> ctx("initialization of AltairMetaSampler");

  localN0 = state.getScalar<long>("localN0");
  startN0 = state.getScalar<long>("startN0");

  long N[3];
  state.getScalarArray<long, 3>("N", N);
  state.getScalarArray<double, 3>("L", L);

  Ntot = N[0] * N[1] * N[2];
  localNtot = localN0 * N[1] * N[2];

  state.getScalarArray<double, 3>("corner", corner);

  delta[0] = L[0] / N[0];
  delta[1] = L[1] / N[1];
  delta[2] = L[2] / N[2];

  // We do not perform cosmo transformation for N_MC < burnin_buffer --> Actually, GL --> smooth weighted transition (set in dense_mass)
  burnin_buffer = 50;

  // For the moment, set the number of cosmo params manually, together with their initial guesses below
  numCosmoParams = 3;
  covariances = std::shared_ptr<mass_t>(new mass_t(numCosmoParams));
  // Set covar to identity matrix initially
  boost::multi_array<double, 2> icMass(
      boost::extents[numCosmoParams][numCosmoParams]);
  for (int j = 0; j < numCosmoParams; j++)
    icMass[j][j] = 1e-8;

  covariances->setCorrelationLimiter(0.1);
  covariances->setBurninMax(200);
  covariances->setMemorySize(50);
  covariances->setInitialMass(icMass);
  state.newElement(
      "cosmo_list", new ArrayType1d(boost::extents[numCosmoParams]), true);

  auto &cosmo = *state.get<ArrayType1d>("cosmo_list")->array;
  cosmo[0] = 0.5; // Initial guess for Omega_Matter
  cosmo[1] =
      -0.8; // Initial guess for w_0, dark energy equation of state parameter
  cosmo[2] =
      0.001; // Initial guess for w_a, dynamical component of CPL parameterization

  auto obj = new ObjectStateElement<HMCLet::MassSaver<mass_t>, true>();
  obj->obj = new HMCLet::MassSaver<mass_t>(*covariances.get());
  state.newElement("cosmo_slice", obj, true);
}

void AltairMetaSampler::restore(MarkovState &state) {
  ConsoleContext<LOG_DEBUG> ctx("restoration of AltairMetaSampler");
  initialize(state);

  // Add an update of the model once the parameters are loaded.
  state["cosmo_slice"].subscribeLoaded([this, &state] {
    // FIXME: We should wait for cosmology to be loaded as well.
    CosmologicalParameters &cosmo_ini =
        state.getScalar<CosmologicalParameters>("cosmology");
    auto &cosmo = *(state.get<ArrayType1d>("cosmo_list")->array);
    CosmologicalParameters cosmo_new;
    cosmo_new = cosmo_ini;
    // Update our cosmology with latest values of Omega_Matter, w_0 and w_a

    cosmo_new.omega_m = cosmo[0];
    cosmo_new.omega_q =
        1 - cosmo_new.omega_m; // Since we assume a flat cosmology
    cosmo_new.w = cosmo[1];
    cosmo_new.wprime = cosmo[2];

    ModelDictionnary all_params;            //FIXME
    all_params["altair_cosmo"] = cosmo_new; //FIXME
    model->setModelParams(all_params);      //FIXME
  });
}

void AltairMetaSampler::setLimiter(std::function<void()> cb) {
  limiter_cb = cb;
}

void AltairMetaSampler::setUnlimiter(std::function<void()> cb) {
  unlimiter_cb = cb;
}

void AltairMetaSampler::sample(MarkovState &state) {
  using namespace Eigen;
  ConsoleContext<LOG_DEBUG> ctx("sampling of cosmo params");
  RandomGen *rng = state.get<RandomGen>("random_generator");

  // Recover s_field and s_hat_field from Markov state
  auto const &density = *state.get<CArrayType>("s_hat_field")->array;

  if (limiter_cb)
    limiter_cb();

  likelihood->updateMetaParameters(state);

  // We need to update the covariance matrix -> Initialized with identity above for 1st iteration
  auto cosmo = Eigen::Map<Eigen::VectorXd>(
      state.get<ArrayType1d>("cosmo_list")->array->data(), numCosmoParams);

  VectorXd transformed_cosmo(numCosmoParams);
  VectorXd new_transformed_cosmo(numCosmoParams);

  CosmologicalParameters &cosmo_ini =
      state.getScalar<CosmologicalParameters>("cosmology");
  CosmologicalParameters cosmo_new;
  cosmo_new = cosmo_ini;
  // Update our cosmology with latest values of Omega_Matter, w_0 and w_a
  cosmo_new.omega_m = cosmo(0);
  cosmo_new.omega_q = 1 - cosmo_new.omega_m; // Since we assume a flat cosmology
  cosmo_new.w = cosmo(1);
  cosmo_new.wprime = cosmo(2);

  // Compute eigenvectors of covariance matrix
  covariances->computeMainComponents();

  Eigen::VectorXd mean = covariances->getMean();
  Eigen::MatrixXd components(numCosmoParams, numCosmoParams);
  //components.setIdentity();
  components = covariances->components();
  //  mean(0) = 0.30;
  //  mean(1) = -1;
  //  mean(2) = 0;
  //mean.setZero();

  // Rotate (Omega_Matter, w_0, w_a) parameter space to improve the decorrelation in (Omega_Matter, w_0, w_a) plane and increase sampling efficiency
  transformed_cosmo.noalias() = components.adjoint() * (cosmo - mean);

  auto local_likelihood = likelihood;
  auto local_model = model;

  double const ares_heat = state.getScalar<double>("ares_heat"); //FIXME: DARK
  auto local_bound_min = bound_min;
  auto local_bound_max = bound_max;

  auto eval_posterior =
      [&local_likelihood, &local_model, &density, &ctx, local_bound_min,
       local_bound_max](CosmologicalParameters const &local_cosmo) -> double {
    // Constrain cosmo parameters within their respective prior ranges (lower and upper bounds)
    if (local_cosmo.omega_m < local_bound_min.omega_m or
        local_cosmo.omega_m > local_bound_max.omega_m)
      return -std::numeric_limits<double>::infinity();
    if (local_cosmo.w < local_bound_min.w or local_cosmo.w > local_bound_max.w)
      return -std::numeric_limits<double>::infinity();
    if (local_cosmo.wprime < local_bound_min.wprime or
        local_cosmo.wprime > local_bound_max.wprime)
      return -std::numeric_limits<double>::infinity();
    //local_likelihood->updateCosmology(local_cosmo); //FIXME
    ModelDictionnary all_params;                                      //FIXME
    all_params["altair_cosmo"] = CosmologicalParameters(local_cosmo); //FIXME
    local_model->setModelParams(all_params);                          //FIXME
    return -local_likelihood->logLikelihood(density);
  };

  // Joint sample cosmo parameters -> Slice sweep while computing new loglikelihood
  for (int j = 0; j < numCosmoParams; j++) {
    transformed_cosmo(j) = slice_sweep_double(
        comm, rng->get(),
        [&](double x) -> double {
          // x is rotated parameter; need to rotate back to original basis for computing log likelihood
          VectorXd tmp_x(numCosmoParams);
          tmp_x = transformed_cosmo;
          tmp_x(j) = x;
          new_transformed_cosmo = components * tmp_x + mean;
          cosmo_new.omega_m = new_transformed_cosmo(0);
          cosmo_new.omega_q = 1 - cosmo_new.omega_m;
          cosmo_new.w = new_transformed_cosmo(1);
          cosmo_new.wprime = new_transformed_cosmo(2);
          ctx.format(
              "Trying omega_m=%lg, omega_q=%lg, w=%lg, wprime=%lg",
              cosmo_new.omega_m, cosmo_new.omega_q, cosmo_new.w,
              cosmo_new.wprime);
          return ares_heat * eval_posterior(cosmo_new);
        },
        transformed_cosmo(j), slice_factor);
  };

  // Rotate back to original frame
  new_transformed_cosmo = components * transformed_cosmo + mean;
  cosmo = new_transformed_cosmo;

  CosmologicalParameters cosmo_ref = cosmo_ini;
  cosmo_ref.omega_m = 0.3089;
  cosmo_ref.omega_q = 1 - 0.3089;
  cosmo_ref.w = -1.0;
  cosmo_ref.wprime = 0.;
  ctx.format("cosmo ref: log_L=%.15g", eval_posterior(cosmo_ref));

  cosmo_ini.omega_m = cosmo(0);
  cosmo_ini.omega_q = 1 - cosmo_ini.omega_m;
  cosmo_ini.w = cosmo(1);
  cosmo_ini.wprime = cosmo(2);

  covariances->addMass(
      *state.get<ArrayType1d>("cosmo_list")
           ->array); //If commented out, rotation matrices should be identity

  //likelihood->updateCosmology(cosmo_ini); //FIXME
  ModelDictionnary all_params;                                    //FIXME
  all_params["altair_cosmo"] = CosmologicalParameters(cosmo_ini); //FIXME
  model->setModelParams(all_params);                              //FIXME
  double end_logL = -likelihood->logLikelihood(density);
  likelihood->commitAuxiliaryFields(state);

  if (unlimiter_cb)
    unlimiter_cb();
}
// ARES TAG: num_authors = 2
// ARES TAG: name(0) = Doogesh Kodi Ramanah
// ARES TAG: year(0) = 2018-2020
// ARES TAG: email(0) = ramanah@iap.fr
// ARES TAG: name(1) = Guilhem Lavaux
// ARES TAG: email(1) = guilhem.lavaux@iap.fr
// ARES TAG: year(1) = 2018-2021
