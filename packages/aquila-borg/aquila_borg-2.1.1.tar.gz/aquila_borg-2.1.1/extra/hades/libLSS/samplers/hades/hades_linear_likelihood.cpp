/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/samplers/hades/hades_linear_likelihood.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

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
#include "libLSS/samplers/hades/hades_linear_likelihood.hpp"
#include "libLSS/tools/hermiticity_fixup.hpp"

using namespace LibLSS;
using boost::extents;
using boost::format;

using CosmoTool::square;

using boost::c_storage_order;
typedef boost::multi_array_types::extent_range range;

typedef Eigen::Map<Eigen::ArrayXd, Eigen::Aligned> MappedArray;

static const int ROOT_RANK = 0;

HadesLinearDensityLikelihood::HadesLinearDensityLikelihood(LikelihoodInfo &info)
    : super_t(info, 1) {}

HadesLinearDensityLikelihood::~HadesLinearDensityLikelihood() {}

double
HadesLinearDensityLikelihood::logLikelihoodSpecific(ArrayRef const &delta) {
  double L = 0;
  size_t const startN0 = model->out_mgr->startN0;
  size_t const endN0 = startN0 + model->out_mgr->localN0;
  size_t const N1 = model->out_mgr->N1;
  size_t const N2 = model->out_mgr->N2;

  for (int c = 0; c < Ncat; c++) {
    auto &sel_array = *(sel_field[c]);
    double nmean_c = nmean[c];
    double bias_c = (*(bias[c]))[0];
    auto &data_c = *(data[c]);

#pragma omp parallel for schedule(static) collapse(3) reduction(+ : L)
    for (size_t n0 = startN0; n0 < endN0; n0++) {
      for (size_t n1 = 0; n1 < N1; n1++) {
        for (size_t n2 = 0; n2 < N2; n2++) {
          double selection = sel_array[n0][n1][n2];

          if (selection > 0) {
            double Nobs = data_c[n0][n1][n2];
            double d_galaxy = bias_c * delta[n0][n1][n2];

            assert(!isnan(Nobs));
            assert(!isnan(d_galaxy));
            L += square(selection * nmean_c * (1 + d_galaxy) - Nobs) /
                 (selection * nmean_c);
            if (std::isnan(L)) {
              error_helper<ErrorBadState>("NaN in Likelihood");
            }
            if (std::isinf(L)) {
              error_helper<ErrorBadState>(
                  format("Inf in hamiltonian at n0=%d n1=%d n2=%d d_g=%lg "
                         "Nobs=%lg") %
                  n0 % n1 % n2 % d_galaxy % Nobs);
            }
          }
        }
      }
    }
  }

  L *= 0.5;

  return L;
}

void HadesLinearDensityLikelihood::gradientLikelihoodSpecific(
    ArrayRef const &delta, ArrayRef &grad_array) {

  size_t const startN0 = model->out_mgr->startN0;
  size_t const endN0 = startN0 + model->out_mgr->localN0;
  size_t const N1 = model->out_mgr->N1;
  size_t const N2 = model->out_mgr->N2;

  fwrap(grad_array) = 0;

  for (int c = 0; c < Ncat; c++) {
    auto &sel_array = *(sel_field[c]);
    auto &data_c = *(data[c]);
    double bias_c = (*bias[c])[0];
    double nmean_c = nmean[c];

#pragma omp parallel for collapse(3)
    for (size_t n0 = startN0; n0 < endN0; n0++) {
      for (size_t n1 = 0; n1 < N1; n1++) {
        for (size_t n2 = 0; n2 < N2; n2++) {
          double deltaElement = delta[n0][n1][n2];
          double d_galaxy = bias_c * deltaElement;
          double d_galaxy_prime = bias_c;
          double response = sel_array[n0][n1][n2];
          double Nobs = data_c[n0][n1][n2];

          if (response == 0)
            continue;

          grad_array[n0][n1][n2] +=
              (nmean_c * response * (1 + d_galaxy) - Nobs) * d_galaxy_prime;
          assert(!isnan(grad_array[n0][n1][n2]));
        }
      }
    }
  }
}

void HadesLinearDensityLikelihood::generateMockSpecific(
    ArrayRef const &delta, MarkovState &state) {
  LIBLSS_AUTO_CONTEXT(LOG_INFO, ctx);
  RandomGen *rgen = state.get<RandomGen>("random_generator");
  size_t const startN0 = model->out_mgr->startN0;
  size_t const endN0 = startN0 + model->out_mgr->localN0;
  size_t const N1 = model->out_mgr->N1;
  size_t const N2 = model->out_mgr->N2;

  for (int c = 0; c < Ncat; c++) {
    ctx.print(format("Generating mock data %d") % c);
    auto &sel_array = *sel_field[c];
    auto &g_field = *state.get<ArrayType>(format("galaxy_data_%d") % c)->array;
    double nmean_c = nmean[c];
    double bias_c = (*bias[c])[0];

#pragma omp parallel for schedule(static) collapse(3)
    for (size_t n0 = startN0; n0 < endN0; n0++) {
      for (size_t n1 = 0; n1 < N1; n1++) {
        for (size_t n2 = 0; n2 < N2; n2++) {
          double R = nmean_c * sel_array[n0][n1][n2];
          double gmean = R * (1 + bias_c * delta[n0][n1][n2]);
          assert(!isnan(gmean));
          assert(!isnan(R));
          assert(R >= 0);
          g_field[n0][n1][n2] = rgen->get().gaussian() * sqrt(R) + gmean;
          assert(!isnan(g_field[n0][n1][n2]));
        }
      }
    }
  }
}

void HadesLinearDensityLikelihood::initializeLikelihood(MarkovState &state) {
  LIBLSS_AUTO_CONTEXT(LOG_INFO, ctx);
  super_t::initializeLikelihood(state);
}

void HadesLinearDensityLikelihood::setupDefaultParameters(
    MarkovState &state, int catalog) {
  auto &bias_c =
      *state.formatGet<ArrayType1d>("galaxy_bias_%d", catalog)->array;
  auto &nmean_c = state.formatGetScalar<double>("galaxy_nmean_%d", catalog);

  bias_c[0] = 1.0;
  nmean_c = 1;
}
