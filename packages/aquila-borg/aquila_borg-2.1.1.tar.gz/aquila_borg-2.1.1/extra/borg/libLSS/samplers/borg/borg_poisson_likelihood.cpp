/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/borg/borg_poisson_likelihood.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/cconfig.h"
#include <CosmoTool/algo.hpp>
#include <cmath>
#include <Eigen/Core>
#include <boost/format.hpp>
#include <boost/bind.hpp>
#include <CosmoTool/hdf5_array.hpp>
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/samplers/borg/borg_poisson_likelihood.hpp"
#include "libLSS/samplers/borg/borg_poisson_meta.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/tools/hermiticity_fixup.hpp"

using namespace LibLSS;
using boost::extents;
using boost::format;

using CosmoTool::hdf5_write_array;
using CosmoTool::square;

using boost::c_storage_order;
typedef boost::multi_array_types::extent_range range;

typedef Eigen::Map<Eigen::ArrayXd, Eigen::Aligned> MappedArray;

static const int ROOT_RANK = 0;
static const bool VERBOSE_WRITE_BORG = false;
static const double EPSILON_VOIDS = 1e-6;
static const bool OVERWRITE_BIAS_PARAMETER = false;

namespace L = LibLSS::Likelihood;

BorgPoissonLikelihood::BorgPoissonLikelihood(LikelihoodInfo &info)
    : HadesBaseDensityLikelihood(info, 3) {}

void BorgPoissonLikelihood::initializeLikelihood(MarkovState &state) {
  super_t::initializeLikelihood(state);
}

void BorgPoissonLikelihood::updateMetaParameters(MarkovState &state) {
  super_t::updateMetaParameters(state);
}

void BorgPoissonLikelihood::setupDefaultParameters(
    MarkovState &state, int catalog) {
  auto &local_bias =
      *state.formatGet<ArrayType1d>("galaxy_bias_%d", catalog)->array;
  state.formatGetScalar<double>("galaxy_nmean_%d", catalog) = 100.0;
  local_bias[0] = 1.0;
  local_bias[1] = 1.5;
  local_bias[2] = 0.4;
}

BorgPoissonLikelihood::~BorgPoissonLikelihood() {}

double
BorgPoissonLikelihood::logLikelihoodSpecific(ArrayRef const &out_density) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  using CosmoTool::square;
  double Epoisson = 0;

  for (int c = 0; c < Ncat; c++) {
    auto &sel_array = *sel_field[c];
    auto &g_field = *data[c];
    double nmean_c = nmean[c];
    auto &local_bias = *(bias[c]);
    double bias_c = local_bias[0], rho_g = local_bias[1], eps_g = local_bias[2];

    size_t const startN0 = g_field.index_bases()[0];
    size_t const endN0 = startN0 + g_field.shape()[0];
    size_t const N1 = g_field.shape()[1];
    size_t const N2 = g_field.shape()[2];

#pragma omp parallel for collapse(3) schedule(static) reduction(+ : Epoisson)
    for (size_t n0 = startN0; n0 < endN0; n0++) {
      for (size_t n1 = 0; n1 < N1; n1++) {
        for (size_t n2 = 0; n2 < N2; n2++) {
          double selection = sel_array[n0][n1][n2];

          if (selection > 0) {
            double Nobs = g_field[n0][n1][n2];
            double rho = 1. + EPSILON_VOIDS + out_density[n0][n1][n2];
            double lambda = selection * nmean_c * pow(rho, bias_c) *
                            exp(-rho_g * pow(rho, -eps_g));

            double value =
                lambda - Nobs * (log(selection * nmean_c) + bias_c * log(rho) -
                                 rho_g * pow(rho, -eps_g));
            Epoisson += value;
            if (std::isnan(value)) {
              ctx.format(
                  "(%d,%d,%d)=>lambda = %g, Nobs=%g, rho=%g", n0, n1, n2,
                  lambda, Nobs, rho);
            }
          }
        }
      }
    }
  }
  return Epoisson;
}

void BorgPoissonLikelihood::gradientLikelihoodSpecific(
    ArrayRef const &out_density, ArrayRef &real_gradient) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  using CosmoTool::square;
  size_t startN0 = model->out_mgr->startN0, endN0 = model->out_mgr->startN0 + model->out_mgr->localN0;
  size_t N1 = model->out_mgr->N1, N2 = model->out_mgr->N2;

  fwrap(real_gradient) = 0;

  for (int c = 0; c < Ncat; c++) {
    auto const &sel_array = *sel_field[c];
    auto const &g_field = *data[c];
    double const nmean_c = nmean[c];
    auto const &local_bias = *(bias[c]);
    double const bias_c = local_bias[0], rho_g = local_bias[1],
                 eps_g = local_bias[2];

#pragma omp parallel for collapse(3)
    for (size_t n0 = startN0; n0 < endN0; n0++) {
      for (size_t n1 = 0; n1 < N1; n1++) {
        for (size_t n2 = 0; n2 < N2; n2++) {
          double selection = sel_array[n0][n1][n2];

          if (selection <= 0)
            continue;

          double rho = 1. + EPSILON_VOIDS + out_density[n0][n1][n2];
          double Nobs = g_field[n0][n1][n2];
          double lambda = selection * nmean_c * pow(rho, bias_c) *
                          exp(-rho_g * pow(rho, -eps_g));

          real_gradient[n0][n1][n2] +=
              1. / rho * (bias_c + eps_g * rho_g * pow(rho, -eps_g)) *
              (lambda - Nobs);
        }
      }
    }
  }
}

void BorgPoissonLikelihood::generateMockSpecific(
    ArrayRef const &out_density, MarkovState &state) {
  LIBLSS_AUTO_CONTEXT(LOG_INFO, ctx);

  RandomGen *rgen = state.get<RandomGen>("random_generator");

  size_t startN0 = model->out_mgr->startN0, endN0 = model->out_mgr->startN0 + model->out_mgr->localN0;
  size_t N1 = model->out_mgr->N1, N2 = model->out_mgr->N2;

  for (int c = 0; c < Ncat; c++) {
    ctx.format(
        "Generating mock data %d (startN0=%d, endN0=%d, N1=%d, N2=%d)", c,
        startN0, endN0, N1, N2);
    auto &sel_array = *sel_field[c];
    auto &g_field = *data[c];
    double nmean_c = nmean[c];
    auto &local_bias = *(bias[c]);
    double bias_c = local_bias[0], rho_g = local_bias[1], eps_g = local_bias[2];

#pragma omp parallel for schedule(static) collapse(3)
    for (size_t n0 = startN0; n0 < endN0; n0++) {
      for (size_t n1 = 0; n1 < N1; n1++) {
        for (size_t n2 = 0; n2 < N2; n2++) {
          double R = nmean_c * sel_array[n0][n1][n2];
          double rho_m = (1 + EPSILON_VOIDS + out_density[n0][n1][n2]);
          double rho_gm = pow(rho_m, bias_c) * exp(-rho_g * pow(rho_m, -eps_g));
          double lambda = R * rho_gm;
          g_field[n0][n1][n2] = rgen->get().poisson(lambda);
        }
      }
    }
  }
}
