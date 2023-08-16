/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/likelihoods/eft.hpp
    Copyright (C) 2018-2019 Franz Elsner <>
    Copyright (C) 2019-2021 Fabian Schmidt <fabians@mpa-garching.mpg.de>
    Copyright (C) 2019-2021 Martin Reinecke <martin@mpa-garching.mpg.de>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_EFT_LIKELIHOOD_HPP
#define __LIBLSS_EFT_LIKELIHOOD_HPP

#include <gsl/gsl_sf_gamma.h>
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/fused_reduce.hpp"
#include <CosmoTool/algo.hpp>
#include "libLSS/physics/likelihoods/base.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"

namespace LibLSS {

  namespace detail_EFT {

    namespace ph = std::placeholders;
    using DFT_Manager = FFTW_Manager_3d<double>;
    using U_Array = Uninit_FFTW_Real_Array;
    using U_CArray = Uninit_FFTW_Complex_Array;
    using U_ArrayRef = U_Array::array_type;
    using U_CArrayRef = U_CArray::array_type;

    template <typename T>
    struct myarr {
      T arr;
      typename T::array_type ref;
      template <typename T1, typename T2>
      myarr(const T1 &extent, const T2 &alloc)
          : arr(extent, alloc), ref(arr.get_array()) {}
    };

    class EFTLikelihood {
    protected:
      bool have_sharpk_data;
      long N0, N1, N2, N2_HC, startN0, localN0;
      double L0, L1, L2;
      double lambda;
      double ctmpmean; // \vec k=0 value obtained in sharpk_filter

      struct Arrs {
        MPI_Communication &comm;
        DFT_Manager mgr;
        myarr<U_Array> tmp;
        myarr<U_CArray> ctmp;
        myarr<U_Array> sharpk_data, sharpk_mu;
        FCalls::plan_type analysis_plan;
        FCalls::plan_type synthesis_plan;

        Arrs(MPI_Communication &comm_, size_t N0, size_t N1, size_t N2)
            : comm(comm_), mgr(N0, N1, N2, &comm),
              tmp(mgr.extents_real(), mgr.allocator_real),
              ctmp(mgr.extents_complex(), mgr.allocator_complex),
              sharpk_data(mgr.extents_real(), mgr.allocator_real),
              sharpk_mu(mgr.extents_real(), mgr.allocator_real) {
          myarr<U_Array> tmp(mgr.extents_real(), mgr.allocator_real);
          analysis_plan = mgr.create_r2c_plan(tmp.ref.data(), ctmp.ref.data());
          synthesis_plan = mgr.create_c2r_plan(ctmp.ref.data(), tmp.ref.data());
        }
      };
      std::unique_ptr<Arrs> arrs;
      static constexpr size_t numberLikelihoodParams =
          3; // density, sigma_0, lnPprior

      // apply sharp-k cut to field: modes with k > limit are set to zero
      // - also sets to zero \vec k==0 mode -> subtract mean
      size_t sharpk_filter(U_ArrayRef &in, U_ArrayRef &out, double limit) {
        auto ctmp = arrs->ctmp.ref;
        double norm = 1.0 / (N0 * N1 * N2);
        arrs->mgr.execute_r2c(arrs->analysis_plan, in.data(), ctmp.data());

        // save mean of field, i.e. \vec k=0 value divided by N^3, needed
        // for data
        if (startN0 == 0 && localN0 > 0) {
          ctmpmean = ctmp[0][0][0].real() * norm;
        }

        size_t cnt = 0;
#pragma omp parallel for collapse(3) reduction(+ : cnt)
        for (size_t i = startN0; i < startN0 + localN0; i++)
          for (size_t j = 0; j < N1; j++)
            for (size_t k = 0; k < N2_HC; k++) {
              double kk[3] = {
                  kmode(i, N0, L0), kmode(j, N1, L1), kmode(k, N2, L2)};

              double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
              if (ksquared > limit * limit || ksquared < 1.e-15)
                ctmp[i][j][k] = 0.;
              else {
                cnt += ((k == 0) || (k == N2_HC - 1)) ? 1 : 2;
                ctmp[i][j][k] *= norm;
              }
            }

        arrs->mgr.execute_c2r(arrs->synthesis_plan, ctmp.data(), out.data());

        // return _local_ mode count
        return cnt;
      }

      // copied from gaussian.hpp: equally applicable here
      static inline double log_proba(double d, double rho, double sigma_0) {
        return CosmoTool::square((d - rho) / sigma_0);
      }

      static inline double
      diff_log_proba(double d, double rho, double sigma_0, bool mask) {
        return mask ? ((d - rho) / (sigma_0 * sigma_0)) : 0;
      }

      template <typename RandomGen>
      static inline double
      gen_sample(RandomGen &rgen, double rho, double sigma_0) {
        // add trivial mean, which will be divided by in data preparation
        return 1. + rgen.gaussian() * sigma_0 + rho;
      }

    public:
      EFTLikelihood(LikelihoodInfo const &info = LikelihoodInfo())
          : have_sharpk_data(false) {
        auto comm(Likelihood::getMPI(info));
        auto grid =
            Likelihood::query<Likelihood::GridSize>(info, Likelihood::GRID);
        N0 = grid[0];
        N1 = grid[1];
        N2 = grid[2];
        N2_HC = N2 / 2 + 1;
        arrs.reset(new Arrs(*comm, N0, N1, N2));
        startN0 = arrs->mgr.startN0;
        localN0 = arrs->mgr.localN0;
        L0 = Likelihood::gridSide(info)[0];
        L1 = Likelihood::gridSide(info)[1];
        L2 = Likelihood::gridSide(info)[2];
        lambda = Likelihood::query<double>(info, "EFT_Lambda");
      }

      template <typename RandomGen, typename TupleLike>
      auto sample(RandomGen &rgen, TupleLike tuple_data) {
        static_assert(
            std::tuple_size<TupleLike>::value == numberLikelihoodParams);

        // same procedure as to get 'sharpk_mu' in log_probability:
        // take tuple_data<0>, apply sharp-k filter in Fourier space and IFT
        auto mu = std::get<0>(
            tuple_data); // is delta_lambda of EFTbias, multiplied by mask array
        auto tmp = arrs->tmp.ref;
#pragma omp parallel for collapse(3)
        for (size_t i = startN0; i < startN0 + localN0; i++)
          for (size_t j = 0; j < N1; j++)
            for (size_t k = 0; k < N2; k++)
              tmp[i][j][k] = mu[i][j][k];
        sharpk_filter(tmp, arrs->sharpk_mu.ref, lambda);

        // this is a 3D array now.
        auto sigma_0 = std::get<1>(tuple_data);

        // only OK if sigma_0 has constant value everywhere
        // - take care of zero-width slabs
        double sigma0_value = localN0 ? sigma_0[startN0][0][0] : 1.;
        // debug output
        Console::instance().format<LOG_DEBUG>(
            "Sampling with sigma_0 = %g.", sigma0_value);

        return b_va_fused<double>(
            std::bind(gen_sample<RandomGen>, std::ref(rgen), ph::_1, ph::_2),
            arrs->sharpk_mu.ref, std::move(sigma_0));
      }

      template <typename DataArray, typename TupleLike, typename MaskArray>
      double log_probability(
          const DataArray &data, TupleLike tuple_data, MaskArray &&mask) {
        static_assert(
            std::tuple_size<TupleLike>::value == numberLikelihoodParams);

        // The tuple from the bias model currently holds
        // mu=delta_lambda, sigma_0, prior(bias)
        auto mu = std::get<0>(
            tuple_data); // is delta_lambda of EFTbias, multiplied by mask array
        auto sigma_0 = std::get<1>(tuple_data);
        // this is prior on bias parameters:
        auto lnPprior = std::get<2>(tuple_data);

        // obtain sharp-k filtered data, if we don't have them already
        if (!have_sharpk_data) {
          auto tmp = arrs->tmp.ref;
#pragma omp parallel for collapse(3)
          for (size_t i = startN0; i < startN0 + localN0; i++)
            for (size_t j = 0; j < N1; j++)
              for (size_t k = 0; k < N2; k++) {
                tmp[i][j][k] = data[i][j][k];
              }

          sharpk_filter(tmp, arrs->sharpk_data.ref, lambda);

          // divide data by mean to obtain \delta_g
          // - first, broadcast ctmpmean computed in sharpk_filter to all threads
          arrs->comm.broadcast_t(&ctmpmean, 1, 0);
          Console::instance().format<LOG_DEBUG>(
              "Mean of data: %.6e.", ctmpmean);
#pragma omp parallel for collapse(3)
          for (size_t i = startN0; i < startN0 + localN0; i++)
            for (size_t j = 0; j < N1; j++)
              for (size_t k = 0; k < N2; k++) {
                arrs->sharpk_data.ref[i][j][k] /= ctmpmean;
              }

          have_sharpk_data = true;
        }

        // Fourier-transform mu, apply sharp-k filter and Fourier-transform back
        // result is in sharpk_mu
        auto tmp = arrs->tmp.ref;
#pragma omp parallel for collapse(3)
        for (size_t i = startN0; i < startN0 + localN0; i++)
          for (size_t j = 0; j < N1; j++)
            for (size_t k = 0; k < N2; k++)
              tmp[i][j][k] = mu[i][j][k];
        // Nmodes is the number of modes that pass sharp-k filter;
        // needed for correct normalization
        size_t Nmodes_local = sharpk_filter(tmp, arrs->sharpk_mu.ref, lambda);

        // Now evaluate likelihood, following gaussian.hpp

        // I. Normalization
        // - note that this form of likelihood ONLY works for trivial mask
        // - desired _global_ normalization is
        //      Nmodes * ln( N_g^3 sigma_0^2 )
        // - hence take Nmodes = N_modes(slab) here

        // only OK if sigma_0 has constant value everywhere
        // - take care of zero-width slabs
        double sigma0_value = localN0 ? sigma_0[startN0][0][0] : 1.;
        double norm = -0.5 * double(Nmodes_local) *
                      std::log(
                          double(N0) * double(N1) * double(N2) * sigma0_value *
                          sigma0_value);

        // II. Likelihood proper
        // - compute chi2
        double chi2 = 0;
        size_t cntmask = 0; // count pixels after mask (for check)
#pragma omp parallel for collapse(3) reduction(+ : chi2, cntmask)
        for (size_t i = startN0; i < startN0 + localN0; i++)
          for (size_t j = 0; j < N1; j++)
            for (size_t k = 0; k < N2; k++) {
              if (mask[i][j][k]) {
                chi2 += log_proba(
                    arrs->sharpk_data.ref[i][j][k],
                    arrs->sharpk_mu.ref[i][j][k], sigma_0[i][j][k]);
                cntmask++;
              }
            }

        // convert from chi2 to ln(likelihood)
        chi2 *= -0.5;

        // if in thread 0, add prior
        double lpp = 0.;
        if (arrs->comm.rank() == 0)
          lpp = lnPprior[0][0][0];

        Console::instance().format<LOG_DEBUG>(
            "chi2 = %.7e, norm = %g, lnPprior = %.7e (sigma_0 = %g; Nmodes = "
            "%zu, startN0 = %zu, localN0 = %zu, cntmask = %zu)",
            chi2, norm, lpp, sigma0_value, Nmodes_local, startN0, localN0,
            cntmask);

        return chi2 + norm + lpp;
      }

      // Compute the gradient of the log probability, convention is that this function
      // accepts a tuple, the first element being the poisson intensity.
      // Other elements are discarded.
      // The gradient is written in the output array, which must have the same shape
      // as the input virtual arrays.
      // L(b_0, b_1, ...)
      // param is the i index in b_i.
      // tuple_data must have the adequate tuple size to account for all "b_i".
      template <typename DataArray, typename TupleLike, typename Mask>
      auto diff_log_probability(
          const DataArray &data, TupleLike tuple_data, const Mask &mask) {
        static_assert(
            std::tuple_size<TupleLike>::value == numberLikelihoodParams);

        // The tuple from the bias model currently holds
        // mu=delta_lambda, sigma_0
        auto mu = std::get<0>(tuple_data); // is delta_lambda of EFTbias
        auto sigma_0 = std::get<1>(tuple_data);

        auto tmp = arrs->tmp.ref;
        // apply sharp-k cut as in log_probability
        if (!have_sharpk_data) {
#pragma omp parallel for collapse(3)
          for (size_t i = startN0; i < startN0 + localN0; i++)
            for (size_t j = 0; j < N1; j++)
              for (size_t k = 0; k < N2; k++)
                tmp[i][j][k] = data[i][j][k];
          sharpk_filter(tmp, arrs->sharpk_data.ref, lambda);
          have_sharpk_data = true;
        }

#pragma omp parallel for collapse(3)
        for (size_t i = startN0; i < startN0 + localN0; i++)
          for (size_t j = 0; j < N1; j++)
            for (size_t k = 0; k < N2; k++)
              tmp[i][j][k] = mu[i][j][k];
        sharpk_filter(tmp, arrs->sharpk_mu.ref, lambda);

        return std::make_tuple(b_va_fused<double>(
            &diff_log_proba, arrs->sharpk_data.ref, arrs->sharpk_mu.ref,
            std::move(sigma_0), mask));

        // FS: notice that in general (in the presence of non-binary mask) we  would also have
        //     sharp-k filter the resulting array before returning; we will skip this for now
      }
    };
  } // namespace detail_EFT

  using detail_EFT::EFTLikelihood;

} // namespace LibLSS

#endif
// ARES TAG: authors_num = 3
// ARES TAG: name(0) = Franz Elsner
// ARES TAG: year(0) = 2018-2019
// ARES TAG: email(0) = 
// ARES TAG: name(1) = Fabian Schmidt
// ARES TAG: year(1) = 2019-2021
// ARES TAG: email(1) = fabians@mpa-garching.mpg.de
// ARES TAG: name(2) = Martin Reinecke
// ARES TAG: year(2) = 2019-2021
// ARES TAG: email(2) = martin@mpa-garching.mpg.de
