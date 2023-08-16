/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/likelihoods/eftmarg.hpp
    Copyright (C) 2019-2021 Fabian Schmidt <fabians@mpa-garching.mpg.de>
    Copyright (C) 2019-2021 Martin Reinecke <martin@mpa-garching.mpg.de>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
/*
    =================================================================================

    Implements the /marginalized/ EFT likelihood as described in
      F. Elsner, F. Schmidt, J. Jasche, G. Lavaux and N.-M. Nguyen [1906.07143].
      G. Cabass and F. Schmidt, [1909.04022],
    however without higher-derivative stochasticity. This allows us to evaluate the
    likelihood in real space.

    Preparation: Fourier transform (FT) data, apply sharp-k cut, inverse FT (IFT) back

    Likelihood:
    1) Obtain individual bias fields from eft_bias_marg (in real space, AFTER sharp-k cut)
    2) Compute scalar products of these weighted by sigma (distributed memory)
       -- currently, sigma is constant; future: mask
    3) Evaluate marginalized Gaussian likelihood (only on root thread)
       -- Gaussian priors on bias parameters are included; obtained from
          "bias_prior_mean", "bias_prior_sigma" in "likelihood" section of ini
	  file, as comma-separated float values

    Gradient: same procedure as in likelihood.

    Sampling: use EFTLikelihood version with hard-coded dummy bias parameter values

    =================================================================================

    This program is free software; you can redistribute it and/or modify it
    under the terms of either the CeCILL license or the GNU General Public
    license, as included with the software package.

    The text of the license is located in Licence_CeCILL_V2.1-en.txt
    and GPL.txt in the root directory of the source package.

*/
#ifndef __LIBLSS_EFT_LIKELIHOOD_MARG_HPP
#  define __LIBLSS_EFT_LIKELIHOOD_MARG_HPP

#  include <gsl/gsl_sf_gamma.h>
#  include "libLSS/tools/fused_array.hpp"
#  include "libLSS/tools/console.hpp"
#  include "libLSS/tools/fused_reduce.hpp"
#  include "libLSS/tools/string_tools.hpp"
#  include "libLSS/tools/ptree_vectors.hpp"
#  include "libLSS/tools/mpi_fftw_helper.hpp"
#  include <CosmoTool/algo.hpp>
#  include "libLSS/physics/likelihoods/base.hpp"
#  include "libLSS/samplers/core/powerspec_tools.hpp"
#  include "eft.hpp"
#  include "Eigen/Dense"

namespace LibLSS {

  namespace detail_EFT {

    typedef size_t st;
    using Eigen::MatrixXd;
    using Eigen::VectorXd;
    // define which matrix decomposition to use:
    // Householder rank-revealing QR decomposition of a matrix with column-pivoting.
    // - need to replace function call 'determinant' with 'absDeterminant'
    typedef Eigen::ColPivHouseholderQR<MatrixXd> matrixDecomp;

    class EFTMargLikelihood : public EFTLikelihood {
      // prior parameters as obtained from ini file (could be empty)
      std::vector<double> priormean, priorsigma;
      // bias prior mean, inverse variance, and normalization
      // - prepared in prepare_like (since we only know size of bias vector during runtime)
      std::vector<double> priorB, priorIC;
      double priornorm;
      double sigmaprior_mean, sigmaprior_IC;

      std::vector<std::shared_ptr<myarr<U_Array>>> gradvec;

      template <typename DataArray>
      void prepare_like(const DataArray &data, const st Nbias) {
        // obtain sharp-k filtered data, if we don't have them already
        if (!have_sharpk_data) {
          auto tmp = arrs->tmp.ref;
#  pragma omp parallel for collapse(3)
          for (size_t i = startN0; i < startN0 + localN0; i++)
            for (size_t j = 0; j < N1; j++)
              for (size_t k = 0; k < N2; k++)
                tmp[i][j][k] = data[i][j][k];
          sharpk_filter(tmp, arrs->sharpk_data.ref, lambda);

          // divide data by mean to obtain \delta_g
          // - first, broadcast ctmpmean computed in sharpk_filter to all threads
          arrs->comm.broadcast_t(&ctmpmean, 1, 0);
          Console::instance().format<LOG_DEBUG>(
              "Mean of data: %.6e.", ctmpmean);
#  pragma omp parallel for collapse(3)
          for (size_t i = startN0; i < startN0 + localN0; i++)
            for (size_t j = 0; j < N1; j++)
              for (size_t k = 0; k < N2; k++) {
                arrs->sharpk_data.ref[i][j][k] /= ctmpmean;
              }

          have_sharpk_data = true;
        }

        // generate vectors with prior mean and inverse variance
        priorB.resize(Nbias);
        priorIC.resize(Nbias);
        priornorm = 0.;
        for (st i = 0; i < Nbias; ++i) {
          // inverse variance; 0 <==> uniform prior
          st ip = i + 1; // ignore prior on nmean
          double IC = (ip < priorsigma.size() && priorsigma[ip] > 0.)
                          ? 1. / (priorsigma[ip] * priorsigma[ip])
                          : 0.;
          priorB[i] = ip < priormean.size() ? priormean[ip] * IC : 0.;
          priorIC[i] = IC;
          priornorm -= IC > 0. ? log(IC) : 0.;
        }

        // in case there is a prior on sigma_0, assign values
        st ip = Nbias + 1;
        sigmaprior_mean = ip < priormean.size() ? priormean[ip] : 0.;
        sigmaprior_IC = (ip < priorsigma.size() && priorsigma[ip] > 0.)
                            ? 1. / (priorsigma[ip] * priorsigma[ip])
                            : 0.;
        priornorm -= sigmaprior_IC > 0. ? log(sigmaprior_IC) : 0.;
      }

    protected:
      // number of likelihood parameters: 2
      // - sigma0 field and vector of bias fields
      static constexpr size_t numberLikelihoodParams = 2;

      // computes and returns \sum_x g(x) h(x) / sigma^2(x)
      // - this does an MPI reduce over all threads
      // - implement mask here in the future
      template <typename SigmaArray>
      double scalar_product(
          const U_ArrayRef &g, const U_ArrayRef &h,
          SigmaArray const &sigma) const {
        double S_local = 0.;
#  pragma omp parallel for collapse(3) reduction(+ : S_local)
        for (size_t i = startN0; i < startN0 + localN0; i++)
          for (size_t j = 0; j < N1; j++)
            for (size_t k = 0; k < N2; k++) {
              double s = sigma[i][j][k];
              if (!(s > 0.))
                continue;
              S_local += g[i][j][k] * h[i][j][k] / (s * s);
            }

        // now MPI reduce (adjoint needs scalar product results in all threads,
        //    hence all_reduce)
        double S = 0.;
        arrs->comm.all_reduce_t(&S_local, &S, 1, MPI_SUM);
        return S;
      }

      // locally count modes that pass sharp-k cut limit, for normalization
      size_t mode_count(double limit) const {
        size_t cnt = 0;
#  pragma omp parallel for collapse(3) reduction(+ : cnt)
        for (size_t i = startN0; i < startN0 + localN0; i++)
          for (size_t j = 0; j < N1; j++)
            for (size_t k = 0; k < N2_HC; k++) {
              double kk[3] = {
                  kmode(i, N0, L0), kmode(j, N1, L1), kmode(k, N2, L2)};

              double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
              if (ksquared > limit * limit || ksquared < 1.e-15)
                continue;

              cnt += ((k == 0) || (k == N2_HC - 1)) ? 1 : 2;
            }

        // return _local_ mode count
        return cnt;
      }

    public:
      EFTMargLikelihood(LikelihoodInfo const &info = LikelihoodInfo())
          : EFTLikelihood(info) {
        ConsoleContext<LOG_DEBUG> ctx("EFTMargLikelihood constructor");

        // set likelihood Lambda cut to kmax (if kmax > 0 and < lambda)
        double kmax = Likelihood::query<double>(info, "EFT_kmax");
        if (kmax > 0. && kmax < lambda)
          lambda = kmax;

        // get prior mean, sigma as set of doubles (priormean, priorsigma),
        // if available
        std::string smean =
            Likelihood::query<std::string>(info, "bias_prior_mean");
        if (smean.length()) {
          auto bias_double = string_as_vector<double>(smean, ", ");
          priormean.resize(bias_double.size());
          std::copy(bias_double.begin(), bias_double.end(), priormean.begin());
          ctx.print(
              "EFTMargLikelihood: Set the bias prior mean to [" +
              to_string(priormean) + "]");
        }
        std::string ssigma =
            Likelihood::query<std::string>(info, "bias_prior_sigma");
        if (ssigma.length()) {
          auto bias_double = string_as_vector<double>(ssigma, ", ");
          priorsigma.resize(bias_double.size());
          std::copy(bias_double.begin(), bias_double.end(), priorsigma.begin());
          ctx.print(
              "EFTMargLikelihood: Set the bias prior sigma to [" +
              to_string(priorsigma) + "]");
        }
      }

      // sample: use return tuple from EFTBiasMarg, and assemble mean density field using
      //         hard-coded default values
      template <typename RandomGen, typename TupleLike>
      auto sample(RandomGen &rgen, TupleLike tuple_data) {
        static_assert(
            std::tuple_size<TupleLike>::value == numberLikelihoodParams);

        // get data from EFTBiasMarg
        auto &gbias = std::get<1>(tuple_data);
        auto &gsigma = std::get<0>(tuple_data);

        // get sigma_0 ; only for debug output here
        // - take care of zero-width slabs
        double sigma0_value = localN0 ? gsigma[startN0][0][0] : 1.;

        // assemble bias field into tmp
        // - already sharp-k filtered
        // - we do not have access to the params of the bias model here,
        //   so we have to make do with our own numbers...

        Console::instance().format<LOG_DEBUG>(
            "INFO in EFTMargLikelihood::sample: sampling with "
            "fixed bias parameters; sigma_0 = %g.",
            sigma0_value);

        auto mu = arrs->sharpk_mu.ref;
#  pragma omp parallel for collapse(3)
        for (size_t i = startN0; i < startN0 + localN0; i++)
          for (size_t j = 0; j < N1; j++)
            for (size_t k = 0; k < N2; k++) {
              mu[i][j][k] = 1.5 * (gbias[0])[i][j][k]    // delta
                            + 0.5 * (gbias[1])[i][j][k]  // delta^2
                            + 0.3 * (gbias[2])[i][j][k]  // K^2
                            + 20. * (gbias[3])[i][j][k]; // lapl delta
            }

        return b_va_fused<double>(
            std::bind(
                EFTLikelihood::gen_sample<RandomGen>, std::ref(rgen), ph::_1,
                ph::_2),
            arrs->sharpk_mu.ref, std::move(gsigma));
      }

      template <typename DataArray, typename TupleLike, typename MaskArray>
      double log_probability(
          const DataArray &data, TupleLike tuple_data, MaskArray &&mask) {
        static_assert(
            std::tuple_size<TupleLike>::value == numberLikelihoodParams);

        // The return vector (tuple element 1) from EFTBiasMarg contains
        // 0: delta
        // 1: delta^2
        // 2: K^2
        // 3: lapl delta
        // 4: sigma
        // -- all in real space after sharp-k filter
        // -- worry about mask later

        // get data
        auto &gbias = std::get<1>(tuple_data);
        auto &gsigma = std::get<0>(tuple_data);
        const st Nbias = gbias.size();

        // prepare sharp-k data and priors
        prepare_like(data, Nbias);

        // now compute scalar products

        // construct A
        MatrixXd A(Nbias, Nbias);
        for (st i = 0; i < Nbias; i++) {
          for (st j = 0; j <= i; j++) {
            A(i, j) = scalar_product(gbias[i], gbias[j], gsigma);

            // add prior inverse variance to diagonal
            if (j == i)
              A(i, j) += priorIC[j];
          }
        }
        // other components through symmetry
        for (st i = 0; i < Nbias; i++) {
          for (st j = i + 1; j < Nbias; j++) {
            A(i, j) = A(j, i);
          }
        }

        // construct B (note no unmarginalized bias fields here)
        VectorXd B(Nbias);
        for (st i = 0; i < Nbias; i++) {
          B(i) = scalar_product(arrs->sharpk_data.ref, gbias[i], gsigma);
          // add prior
          B(i) += priorB[i];
        }

        // construct C (note no unmarginalized bias fields here)
        double C = scalar_product(
            arrs->sharpk_data.ref, arrs->sharpk_data.ref, gsigma);

        Console::instance().format<LOG_DEBUG>(
            "[%d] Done with scalar products; marginalizing over "
            "%zu bias parameters (A(0,0) = %.5e).",
            arrs->comm.rank(), Nbias, A(0, 0));
        // compute normalization
        // -- assume constant value for sigma_0 here; can be easily generalized to sum over
        //    sigma field
        st Nmodes_local = mode_count(lambda);
        double sigma0_value = 0., norm = 0.;
        if (Nmodes_local) { // take care of zero-width slabs
          sigma0_value = gsigma[startN0][0][0];
          norm = -0.5 * double(Nmodes_local) *
                 (std::log(sigma0_value * sigma0_value) +
                  std::log(double(N0) * double(N1) * double(N2)));
        }

        // the rest should only run on master thread 0 to avoid duplication over MPI threads
        if (arrs->comm.rank() != 0) {
          Console::instance().format<LOG_DEBUG>(
              "[%d] (no chi2) norm = %g (sigma_0 = %g; Nmodes = %zu, "
              "startN0 = %zu, localN0 = %zu, Lambda(like) = %.4f)",
              arrs->comm.rank(), norm, sigma0_value, Nmodes_local,
              startN0 % localN0, lambda);
          return norm;
        }

        // main part of pseudo-chi^2
        double chi2 = C;
        // - more efficient (and accurate?) solution via matrix decomposition
        // -- see above for selection of decomposition
        matrixDecomp AD(A);
        VectorXd X(Nbias);
        X = AD.solve(B);
        double QT = B.transpose() * X;
        chi2 -= QT;

        // add log-determinant of A
        // - using Cholesky decomposition;
        //   see https://gist.github.com/redpony/fc8a0db6b20f7b1a3f23
        // Eigen::LLT<MatrixXd> chol(A);
        // chi2 += 2. * chol.matrixL().toDenseMatrix().diagonal().array().log().sum();
        // - using matrix decomposition itself (this seems to be more accurate numerically):
        // chi2 += log(fabs(AD.determinant()));
        chi2 += log(AD.absDeterminant());

        // add prior on sigma_0
        if (sigmaprior_IC > 0.) {
          double D = sigma0_value - sigmaprior_mean;
          chi2 += sigmaprior_IC * D * D;
        }

        // to conclude, add prior normalization (usually least relevant term)
        chi2 += priornorm;

        Console::instance().format<LOG_DEBUG>(
            "[%d] chi2 = %.7e, norm = %g, priornorm = %g (sigma_0 = %g; "
            "Nmodes = %zu, startN0 = %zu, localN0 = %zu)",
            arrs->comm.rank(), chi2, norm, priornorm, sigma0_value,
            Nmodes_local, startN0, localN0);

        // convert from chi^2 to ln P and add normalization
        return -0.5 * chi2 + norm;
      }

      // Compute the gradient of the log probability, convention is that this function
      // accepts a tuple, the first element being the poisson intensity.
      // Other elements are discarded.
      // The gradient is written in the output array, which must have the same shape
      // as the input virtual arrays.
      // L(b_0, b_1, ...)
      // param is the i index in b_i.
      // tuple_data must have the adequate tuple size to account for all "b_i".
      //
      // returns tuple which contains
      // 0: dlogL/ddelta
      // 1: dlogL/ddelta^2
      // 2: dlogL/dK^2
      // 3: dlogL/d(lapl delta)
      //
      // while debugging gradient:
      template <typename DataArray, typename TupleLike, typename Mask>
      auto diff_log_probability(
          const DataArray &data, TupleLike tuple_data, const Mask &mask) {

        static_assert(
            std::tuple_size<TupleLike>::value == numberLikelihoodParams);

        // this is the return vector
        std::vector<U_ArrayRef> gradref;

        // =======
        // PREPARATION

        // The return tuple from EFTBiasMarg contains
        // 0: delta
        // 1: delta^2
        // 2: K^2
        // 3: lapl delta
        // 4: sigma
        // -- all in real space after sharp-k filter
        // -- worry about mask later

        // get data
        auto &gbias = std::get<1>(tuple_data);
        auto &gsigma = std::get<0>(tuple_data);
        const st Nbias = gbias.size();

        // prepare sharp-k data and priors
        prepare_like(data, Nbias);

        // allocate gradient arrays, if we don't have them already
        if (gradvec.size() < Nbias) {
          gradvec.clear();
          Console::instance().format<LOG_DEBUG>(
              "[%d] EFTMargLikelihood gradient: allocating %zu "
              "gradient arrays.",
              arrs->comm.rank(), Nbias);
          for (st I = 0; I < Nbias; I++) {
            gradvec.push_back(std::make_shared<myarr<U_Array>>(
                arrs->mgr.extents_real(), arrs->mgr.allocator_real));
          }
        }

        // now compute scalar products

        // construct A
        MatrixXd A(Nbias, Nbias);
        for (st i = 0; i < Nbias; i++) {
          for (st j = 0; j <= i; j++) {
            A(i, j) = scalar_product(gbias[i], gbias[j], gsigma);

            // add prior inverse variance to diagonal
            if (j == i)
              A(i, j) += priorIC[j];
          }
        }
        // other components through symmetry
        for (st i = 0; i < Nbias; i++) {
          for (st j = i + 1; j < Nbias; j++) {
            A(i, j) = A(j, i);
          }
        }

        // construct B
        VectorXd B(Nbias);
        for (st i = 0; i < Nbias; i++) {
          B(i) = scalar_product(arrs->sharpk_data.ref, gbias[i], gsigma);
          // add prior
          B(i) += priorB[i];
        }

        // no need for 'C' in gradient

        Console::instance().format<LOG_DEBUG>(
            "[%d] EFTMargLikelihood gradient: Done with scalar "
            "products; marginalizing over %zu bias parameters.",
            arrs->comm.rank(), Nbias);

        // now compute the constant matrix components we need
        // - note these need to be available in all threads
        matrixDecomp AD(A);
        VectorXd X(Nbias);
        X = AD.solve(B);
        MatrixXd Ainv(A.inverse()); // need this explicitly this time

        // GRADIENT PROPER

        // loop over bias fields for which to compute gradient
        for (st ip = 0; ip < Nbias; ip++) {
          auto gradp = gradvec[ip]->ref;

          // part 1 (assign propto data)
#  pragma omp parallel for collapse(3)
          for (size_t i = startN0; i < startN0 + localN0; i++)
            for (size_t j = 0; j < N1; j++)
              for (size_t k = 0; k < N2; k++) {
                double s = gsigma[i][j][k];
                if (!(s > 0.))
                  continue;
                double is2 = 1. / (s * s);
                gradp[i][j][k] = is2 * X(ip) * arrs->sharpk_data.ref[i][j][k];
              }

          // part 2 (add bias operators)
          for (st iO = 0; iO < Nbias; iO++) {
#  pragma omp parallel for collapse(3)
            for (size_t i = startN0; i < startN0 + localN0; i++)
              for (size_t j = 0; j < N1; j++)
                for (size_t k = 0; k < N2; k++) {
                  double s = gsigma[i][j][k];
                  if (!(s > 0.))
                    continue;
                  double is2 = 1. / (s * s);
                  gradp[i][j][k] -= is2 * (X(ip) * X(iO) + Ainv(ip, iO)) *
                                    (gbias[iO])[i][j][k];
                }
          }

          gradref.push_back(gradp);
        } // end loop over bias

        // return tuple (first element actually not used; it is multiplied by gradient of
        //  selector)
        return std::make_tuple(gsigma, gradref);
      }
    };
  } // namespace detail_EFT

  using detail_EFT::EFTMargLikelihood;

} // namespace LibLSS

#endif
// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Fabian Schmidt
// ARES TAG: year(0) = 2019-2021
// ARES TAG: email(0) = fabians@mpa-garching.mpg.de
// ARES TAG: name(1) = Martin Reinecke
// ARES TAG: year(1) = 2019-2021
// ARES TAG: email(1) = martin@mpa-garching.mpg.de
