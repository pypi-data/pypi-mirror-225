/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/borg/borg_poisson_meta.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/cconfig.h"
#include <CosmoTool/algo.hpp>
#include <boost/bind.hpp>
#include <boost/format.hpp>
#include "libLSS/tools/errors.hpp"
#include "libLSS/samplers/core/gig_sampler.hpp"
#include "libLSS/samplers/borg/borg_poisson_meta.hpp"
#include "libLSS/samplers/rgen/slice_sweep.hpp"
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/tools/array_tools.hpp"

using namespace LibLSS;
using boost::format;
namespace ph = std::placeholders;

static const double EPSILON_VOIDS = 1e-6;

void BorgPoissonVobsSampler::initialize(MarkovState &state) {
  long N0, N1, N2;
  long localN0, startN0;

  ConsoleContext<LOG_DEBUG> ctx("initialization of BorgVobsSampler");
  // This sampler depends heavily on the rest of the model.
  // First grab the number of catalogs available in the markov chain

  Ncat = static_cast<SLong &>(state["NCAT"]);

  N0 = static_cast<SLong &>(state["N0"]);
  localN0 = static_cast<SLong &>(state["localN0"]);
  startN0 = static_cast<SLong &>(state["startN0"]);
  N1 = static_cast<SLong &>(state["N1"]);
  N2 = static_cast<SLong &>(state["N2"]);

  Ntot = N0 * N1 * N2;
  localNtot = localN0 * N1 * N2;

  model = state.get<BorgModelElement>("BORG_model")->obj;
}

void BorgPoissonVobsSampler::restore(MarkovState &state) {
  ConsoleContext<LOG_DEBUG> ctx("restoration of BorgVobsSampler");
  initialize(state);
}

double BorgPoissonVobsSampler::computeLogLikelihood(
    MarkovState &state, double v0, double v1, double v2) {
  using CosmoTool::square;
  ConsoleContext<LOG_VERBOSE> ctx("likelihood evaluation");

  ctx.print(format("attempting vobs = { %lg,%lg,%lg }") % v0 % v1 % v2);

  //set vobs
  double vobs_ext[] = {v0, v1, v2};
  double temp = state.getScalar<double>("ares_heat");

  ctx.print(format("Temperature is %lg") % temp);

  ///now calculate likelihood over all sub-cats
  typedef ArrayType::ArrayType Array;
  typedef SelArrayType::ArrayType SArray;

  Array &G = *state.get<ArrayType>("growth_factor")->array;

  Array &final_delta = *state.get<ArrayType>("BORG_final_density")->array;

  ///just calculate 3d redshift distorted field
  ///NOTE: The sampler state of the final density field needs to be overwritten
  /// with a new final density field corresponding to vobs

  model->forwardModelRsdField(final_delta, vobs_ext);

  double H = 0.;

  for (int c = 0; c < Ncat; c++) {
    SArray &sel_array =
        *state.get<SelArrayType>(format("galaxy_sel_window_%d") % c)->array;
    Array &g_field = *state.get<ArrayType>(format("galaxy_data_%d") % c)->array;
    SDouble *g_nmean = state.get<SDouble>(format("galaxy_nmean_%d") % c);
    double *g_bias, *g_rho, *g_eps;

    BORG::extract_poisson_bias(state, c, g_bias, g_rho, g_eps);

    double bias = *g_bias;
    double rho_g = *g_rho;
    double eps_g = *g_eps;

    double nmean = g_nmean->value;

    double L = 0, loc_L = 0;

#pragma omp parallel for schedule(dynamic, 10000) reduction(+ : loc_L)
    for (long n = 0; n < final_delta.num_elements(); n++) {
      double S = sel_array.data()[n];

      if (S <= 0)
        continue;

      double rho = 1 + EPSILON_VOIDS + final_delta.data()[n];
      double lambda =
          S * nmean * pow(rho, bias) * exp(-rho_g * pow(rho, -eps_g));
      double Nobs = g_field.data()[n];

      loc_L += lambda - Nobs * (log(S * nmean) + bias * log(rho) -
                                rho_g * pow(rho, -eps_g));
    }

    comm->reduce_t(&loc_L, &L, 1, MPI_SUM, 0);

    H += L;
  }

  ctx.print(format("Hamiltonian =  %lg") % H);
  return -H * temp;
}

void BorgPoissonVobsSampler::sample(MarkovState &state) {
  ConsoleContext<LOG_DEBUG> ctx("SAMPLE V_OBS");
  return;

  if (state.getScalar<bool>("gravity_model.do_rsd") == true) {

    RandomGen *rng = state.get<RandomGen>("random_generator");

    ///why can't i just call the model of the poisson likelihood?????

    ///I don't want to do this
    ///***************************************************************************************
    using CosmoTool::square;
    CosmologicalParameters &cosmo_params =
        state.getScalar<CosmologicalParameters>("cosmology");
    Cosmology cosmo(cosmo_params);

    ArrayType::ArrayType &growth =
        *state.get<ArrayType>("growth_factor")->array;
    double ai = state.get<SDouble>("borg_a_initial")->value;
    double D_init = cosmo.d_plus(ai) /
                    cosmo.d_plus(1.0); // Scale factor for initial conditions

    double L0 = state.getScalar<double>("L0");
    double L1 = state.getScalar<double>("L1");
    double L2 = state.getScalar<double>("L2");
    long N0 = state.getScalar<long>("N0");
    long N1 = state.getScalar<long>("N1");
    long N2 = state.getScalar<long>("N2");

    double volume = L0 * L1 * L2;
    double dVol = volume / (N0 * N1 * N2);

    // Simulate forward model
    Uninit_FFTW_Complex_Array tmp_complex_field(
        model->lo_mgr->extents_complex(), model->lo_mgr->allocator_complex);
    auto out_density = state.get<ArrayType>("BORG_final_density")->array;
    CArrayType::ArrayType &s_array =
        *state.get<CArrayType>("s_hat_field")->array;
    // Protect the input
    array::scaleAndCopyArray3d(
        tmp_complex_field.get_array(), s_array, D_init / volume);
    //Hermiticity_fixup(*tmp_complex_field);

    model->setCosmoParams(state.getScalar<CosmologicalParameters>("cosmology"));
    ArrayType1d::ArrayType &vobs = *state.get<ArrayType1d>("BORG_vobs")->array;
    model->setObserver(vobs);
    model->forwardModel(tmp_complex_field, *out_density, true);
    ///***************************************************************************************

    //if (state.get<SBool>("vobs_sampler_blocked")->value)
    //  return;

    ///sample 0-component of vobs
    ctx.print("Doing slice sweep vobs_0");

    vobs[0] = slice_sweep(
        comm, rng->get(),
        boost::bind(
            &BorgPoissonVobsSampler::computeLogLikelihood, this,
            boost::ref(state), _1, vobs[1], vobs[2]),
        vobs[0], 30.);

    ctx.print(format(" => got vobs_0=%lg") % vobs[0]);

    ///sample 1-component of vobs
    ctx.print("Doing slice sweep vobs_1");

    vobs[1] = slice_sweep(
        comm, rng->get(),
        boost::bind(
            &BorgPoissonVobsSampler::computeLogLikelihood, this,
            boost::ref(state), vobs[0], _1, vobs[2]),
        vobs[1], 30.);

    ctx.print(format(" => got vobs_1=%lg") % vobs[1]);

    ///sample 2-component of vobs
    ctx.print("Doing slice sweep vobs_2");

    vobs[2] = slice_sweep(
        comm, rng->get(),
        boost::bind(
            &BorgPoissonVobsSampler::computeLogLikelihood, this,
            boost::ref(state), vobs[0], vobs[1], _1),
        vobs[2], 30.);

    ctx.print(format(" => got vobs_2=%lg") % vobs[2]);

    //now release particles again
    model->releaseParticles();

    model->setObserver(vobs);
    model->forwardModel(tmp_complex_field, *out_density, false);
  }
}

void BorgPoissonNmeanSampler::initialize(MarkovState &state) {
  long N0, N1, N2;
  long localN0, startN0;

  ConsoleContext<LOG_DEBUG> ctx("initialization of BorgNmeanSampler");
  // This sampler depends heavily on the rest of the model.
  // First grab the number of catalogs available in the markov chain

  Ncat = static_cast<SLong &>(state["NCAT"]);

  N0 = static_cast<SLong &>(state["N0"]);
  localN0 = static_cast<SLong &>(state["localN0"]);
  startN0 = static_cast<SLong &>(state["startN0"]);
  N1 = static_cast<SLong &>(state["N1"]);
  N2 = static_cast<SLong &>(state["N2"]);

  Ntot = N0 * N1 * N2;
  localNtot = localN0 * N1 * N2;
}

void BorgPoissonNmeanSampler::restore(MarkovState &state) {
  ConsoleContext<LOG_DEBUG> ctx("restoration of BorgNmeanSampler");
  initialize(state);
}

double BorgPoissonNmeanSampler::computeLogLikelihood(
    ArrayType::ArrayType &s_array, ArrayType::ArrayType &data_array,
    SelArrayType::ArrayType &selection, double nmean, double b, double rho_g,
    double eps_g, double temp) {
  using CosmoTool::square;
  ConsoleContext<LOG_DEBUG> ctx("likelihood evaluation");

  ctx.print(format("attempting nmean %lg") % nmean);
  if (nmean <= 0)
    return -std::numeric_limits<double>::infinity();

  if (nmean > 100000)
    return -std::numeric_limits<double>::infinity();

  double L = 0, loc_L = 0;

#pragma omp parallel for schedule(dynamic, 10000) reduction(+ : loc_L)
  for (long n = 0; n < s_array.num_elements(); n++) {
    double S = selection.data()[n];

    if (S <= 0)
      continue;

    double rho = 1 + EPSILON_VOIDS + s_array.data()[n];
    double lambda = S * nmean * pow(rho, b) * exp(-rho_g * pow(rho, -eps_g));
    double Nobs = data_array.data()[n];

    loc_L += lambda - Nobs * (log(nmean));
  }

  comm->reduce_t(&loc_L, &L, 1, MPI_SUM, 0);
  ctx.print(
      format("nmean = %lg, bias = %lg, rho_g = %lg, eps_g = %lg, L = %lg, "
             "loc_L=%lg") %
      nmean % b % rho_g % eps_g % (L) % (loc_L));
  return -L * temp;
}

void BorgPoissonNmeanSampler::sample(MarkovState &state) {
  typedef ArrayType::ArrayType Array;
  typedef SelArrayType::ArrayType SArray;
  ConsoleContext<LOG_DEBUG> ctx("sampling of nmean ");

  Array &G = *state.get<ArrayType>("growth_factor")->array;
  Array &final_field = *state.get<ArrayType>("BORG_final_density")->array;
  RandomGen *rng = state.get<RandomGen>("random_generator");

  if (state.get<SBool>("nmean_sampler_blocked")->value)
    return;

  double temp = state.getScalar<double>("ares_heat");
  ctx.print(format("Temperature is %lg") % temp);

  for (int c = 0; c < Ncat; c++) {
    SArray &sel_array =
        *state.get<SelArrayType>(format("galaxy_sel_window_%d") % c)->array;
    Array &g_field = *state.get<ArrayType>(format("galaxy_data_%d") % c)->array;
    double *g_bias, *g_rho_g, *g_eps_g;
    BORG::extract_poisson_bias(state, c, g_bias, g_rho_g, g_eps_g);
    double bias = *g_bias, rho_g = *g_rho_g, eps_g = *g_eps_g;
    SDouble *g_nmean = state.get<SDouble>(format("galaxy_nmean_%d") % c);

    ctx.print(format("catalog %d") % c);

    ctx.print("Doing slice sweep");
    g_nmean->value = slice_sweep_double(
        comm, rng->get(),
        std::bind(
            &BorgPoissonNmeanSampler::computeLogLikelihood, this,
            ref(final_field), ref(g_field), ref(sel_array), ph::_1, *g_bias,
            *g_rho_g, *g_eps_g, temp),
        g_nmean->value, 0.1);
    ctx.print(format(" => got nmean=%lg") % g_nmean->value);
  }
}

void BorgPoissonBiasSampler::initialize(MarkovState &state) {
  long N0, N1, N2;
  long localN0, startN0;

  ConsoleContext<LOG_DEBUG> ctx("initialization of BorgPoissonBiasSampler");
  // This sampler depends heavily on the rest of the model.
  // First grab the number of catalogs available in the markov chain

  Ncat = static_cast<SLong &>(state["NCAT"]);

  N0 = static_cast<SLong &>(state["N0"]);
  localN0 = static_cast<SLong &>(state["localN0"]);
  startN0 = static_cast<SLong &>(state["startN0"]);
  N1 = static_cast<SLong &>(state["N1"]);
  N2 = static_cast<SLong &>(state["N2"]);

  Ntot = N0 * N1 * N2;
  localNtot = localN0 * N1 * N2;
}

void BorgPoissonBiasSampler::restore(MarkovState &state) {
  ConsoleContext<LOG_DEBUG> ctx("restoration of BorgPoissonBiasSampler");
  initialize(state);
}

double BorgPoissonBiasSampler::computeLogLikelihood(
    ArrayType::ArrayType &s_array, ArrayType::ArrayType &data_array,
    SelArrayType::ArrayType &selection, double nmean, double b, double rho_g,
    double eps_g, double temp) {
  using CosmoTool::square;
  ConsoleContext<LOG_DEBUG> ctx("likelihood evaluation");

  ctx.print(format("attempting bias %lg") % b);
  if (b <= 0)
    return -std::numeric_limits<double>::infinity();

  ctx.print(format("attempting rho_g %lg") % rho_g);
  if (rho_g <= 0)
    return -std::numeric_limits<double>::infinity();

  if (rho_g > 1000)
    return -std::numeric_limits<double>::infinity();

  ctx.print(format("attempting eps_g %lg") % eps_g);
  if (eps_g < 0.)
    return -std::numeric_limits<double>::infinity();

  if (eps_g > 10.)
    return -std::numeric_limits<double>::infinity();

  double L = 0, loc_L = 0;

#pragma omp parallel for schedule(dynamic, 10000) reduction(+ : loc_L)
  for (long n = 0; n < s_array.num_elements(); n++) {
    double S = selection.data()[n];

    if (S <= 0)
      continue;

    double rho = 1 + EPSILON_VOIDS + s_array.data()[n];
    double lambda =
        S * nmean * pow(rho, b) * exp(-rho_g * pow(rho, -eps_g)); //+1e-12;
    double Nobs = data_array.data()[n];

    //loc_L += lambda - Nobs*log(lambda);

    loc_L += lambda -
             Nobs * (log(S * nmean) + b * log(rho) - rho_g * pow(rho, -eps_g));
  }

  comm->reduce_t(&loc_L, &L, 1, MPI_SUM, 0);
  ctx.print(
      format("nmean = %lg, bias = %lg, rho_g = %lg, eps_g = %lg, L = %lg, "
             "loc_L=%lg") %
      nmean % b % rho_g % eps_g % (L) % (loc_L));
  double prior = -0.5 * (b - 1) * (b - 1) / 4. +
                 -0.5 * (eps_g - 1.5) * (eps_g - 1.5) / (1.5) / (1.5) -
                 0.5 * (rho_g - 0.4) * (rho_g - 0.4) / 1;
  return -L * temp + prior;
}

void BorgPoissonBiasSampler::sample(MarkovState &state) {

  typedef ArrayType::ArrayType Array;
  typedef SelArrayType::ArrayType SArray;
  ConsoleContext<LOG_DEBUG> ctx("sampling of bias");

  Array &G = *state.get<ArrayType>("growth_factor")->array;
  Array &final_field = *state.get<ArrayType>("BORG_final_density")->array;
  RandomGen *rng = state.get<RandomGen>("random_generator");
  double temp = state.getScalar<double>("ares_heat");

  if (state.get<SBool>("bias_sampler_blocked")->value)
    return;

  ctx.print(format("Temperature is %lg") % temp);

  for (int c = 0; c < Ncat; c++) {
    bool biasRef = state.get<SBool>(format("galaxy_bias_ref_%d") % c)->value;
    SArray &sel_array =
        *state.get<SelArrayType>(format("galaxy_sel_window_%d") % c)->array;
    Array &g_field = *state.get<ArrayType>(format("galaxy_data_%d") % c)->array;
    SDouble *g_nmean = state.get<SDouble>(format("galaxy_nmean_%d") % c);
    double *g_bias, *g_rho, *g_eps;

    BORG::extract_poisson_bias(state, c, g_bias, g_rho, g_eps);

    double &bias = *g_bias;
    double &rho = *g_rho;
    double &eps = *g_eps;

    ctx.print(format("catalog %d") % c);
    if (biasRef)
      continue;

    ctx.print("Doing slice sweep bias");
    bias = slice_sweep(
        comm, rng->get(),
        std::bind(
            &BorgPoissonBiasSampler::computeLogLikelihood, this,
            ref(final_field), ref(g_field), ref(sel_array), g_nmean->value,
            ph::_1, rho, eps, temp),
        bias, 0.1);
    ctx.print(format(" => got b=%lg") % bias);

    ctx.print("Doing slice sweep rho_g");
    rho = slice_sweep_double(
        comm, rng->get(),
        std::bind(
            &BorgPoissonBiasSampler::computeLogLikelihood, this,
            ref(final_field), ref(g_field), ref(sel_array), g_nmean->value,
            bias, ph::_1, eps, temp),
        rho, 0.1);
    ctx.print(format(" => got rho_g=%lg") % rho);

    ctx.print("Doing slice sweep eps_g");
    eps = slice_sweep(
        comm, rng->get(),
        std::bind(
            &BorgPoissonBiasSampler::computeLogLikelihood, this,
            ref(final_field), ref(g_field), ref(sel_array), g_nmean->value,
            bias, rho, ph::_1, temp),
        eps, 0.1);
    ctx.print(format(" => got eps_g=%lg") % eps);
  }
}
