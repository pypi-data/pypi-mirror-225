/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/bias/eft_bias.hpp
    Copyright (C) 2018-2019 Franz Elsner <>
    Copyright (C) 2019-2021 Fabian Schmidt <fabians@mpa-garching.mpg.de>
    Copyright (C) 2019-2021 Martin Reinecke <martin@mpa-garching.mpg.de>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
/*
       Key features:
       - implements bias fields \delta, \delta^2, (K_ij)^2, \laplace\delta
       - bias fields are precomputed for speed up during bias block sampling
       - biased field is returned in real space but BEFORE sharp-k filter
       - sharp-k filtered density is available in arrs->deltaLambda
       - Gaussian priors on bias parameters can be set using
         "bias_prior_mean", "bias_prior_sigma" in "likelihood" section of ini file,
         as comma-separated float values

       A word on numParams = 6: we have
         nmean (should be fixed to 1),
	 4 bias parameters,
	 sigma_0 (sqrt of constant noise variance).

    This program is free software; you can redistribute it and/or modify it
    under the terms of either the CeCILL license or the GNU General Public
    license, as included with the software package.

    The text of the license is located in Licence_CeCILL_V2.1-en.txt
    and GPL.txt in the root directory of the source package.

*/
#ifndef __LIBLSS_PHYSICS_EFT_BIAS_HPP
#  define __LIBLSS_PHYSICS_EFT_BIAS_HPP

// This header provides the implementation of the LSS bias model to second order PT.

#  include <cmath>
#  include "libLSS/tools/fused_array.hpp"
#  include <tuple>
#  include "libLSS/tools/phoenix_vars.hpp"
#  include <boost/phoenix/operator.hpp>
#  include <boost/phoenix/stl/cmath.hpp>
#  include "libLSS/tools/tuple_helper.hpp"
#  include "libLSS/tools/ptree_vectors.hpp"
#  include "libLSS/tools/string_tools.hpp"
#  include "libLSS/physics/bias/base.hpp"
#  include "libLSS/physics/bias/power_law.hpp"
#  include "libLSS/tools/fftw_allocator.hpp"
#  include "libLSS/samplers/core/powerspec_tools.hpp"

namespace LibLSS {

  namespace bias {

    namespace detail_EFTBias {

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

      template <bool SHARP_THRESHOLDER>
      class EFTBias {
      public:
        static constexpr const bool NmeanIsBias = true;
        static constexpr int numParams = 6;

      protected:
        struct Arrs {
          MPI_Communication &comm;
          DFT_Manager &mgr;
          myarr<U_Array> deltaLambda, delta_sqr, tidal_sqr, laplace_delta,
              dlogL_ddelta;
          myarr<U_Array> tidal_00, tidal_01, tidal_02, tidal_11, tidal_12,
              tidal_22;
          FCalls::plan_type analysis_plan;
          FCalls::plan_type synthesis_plan;
          template <class Mgr>
          Arrs(MPI_Communication &comm_, Mgr &mgr_)
              : comm(comm_), mgr(mgr_),
                deltaLambda(mgr.extents_real(), mgr.allocator_real),
                delta_sqr(mgr.extents_real(), mgr.allocator_real),
                tidal_sqr(mgr.extents_real(), mgr.allocator_real),
                laplace_delta(mgr.extents_real(), mgr.allocator_real),
                dlogL_ddelta(mgr.extents_real(), mgr.allocator_real),
                tidal_00(mgr.extents_real(), mgr.allocator_real),
                tidal_01(mgr.extents_real(), mgr.allocator_real),
                tidal_02(mgr.extents_real(), mgr.allocator_real),
                tidal_11(mgr.extents_real(), mgr.allocator_real),
                tidal_12(mgr.extents_real(), mgr.allocator_real),
                tidal_22(mgr.extents_real(), mgr.allocator_real) {
            myarr<U_Array> tmp(mgr.extents_real(), mgr.allocator_real);
            myarr<U_CArray> ctmp(mgr.extents_complex(), mgr.allocator_complex);
            analysis_plan =
                mgr.create_r2c_plan(tmp.ref.data(), ctmp.ref.data());
            synthesis_plan =
                mgr.create_c2r_plan(ctmp.ref.data(), tmp.ref.data());
          }
        };
        std::unique_ptr<Arrs> arrs;

        static constexpr double EPSILON_VOIDS = 1e-6; // for thresholder

        long N0, N1, N2, N2_HC;
        long startN0, localN0;
        double L0, L1, L2;
        // nmean and bias/likelihood parameter:
        double nmean;
        double b1, b2;
        double bk;
        double r2;
        double sigma_0;
        // cutoff:
        double EFT_Lambda;
        // sigma0 limits
        double sigma0min, sigma0max;

        // priors on bias/likelihood parameters
        // - if priorsigma <= 0, means no prior
        std::vector<double> priormean;
        std::vector<double> priorsigma;
        // store prior ln P
        double lnPprior;

        // hard-coded renormalization; this should correspond to RMS of
        // Eulerian density field AFTER cut
        // - no renorm:
        static constexpr double rmsdelta_renorm = 0.;
        // - 2LPT, Lambda=0.1:
        // static constexpr double rmsdelta_renorm = 0.413;

        // FS: disable thresholders; in future, should be removed properly
        static inline double thresholder(double a, double b) {
          return a;
          // if (a>=b) return a;
          // return SHARP_THRESHOLDER ? b : b * std::exp((-b/a + 1));
        }
        static inline double adjoint_thresholder(double a, double b, double g) {
          return g;
          // if (a>=b) return g;
          // return SHARP_THRESHOLDER ? 0 : ( b*b / (a*a) * std::exp((1-b/a)) * g);
        }

        // construct bias field
        static inline double density_lambda(
            double nmean, double b1eff, double b2, double bk, double r2,
            double delta, double delta_sqr, double tidal_sqr,
            double laplace_delta) {
          double rho = b1eff * delta + b2 * delta_sqr + bk * tidal_sqr +
                       r2 * laplace_delta;
          return nmean * thresholder(1.0 + rho, EPSILON_VOIDS);
        }

        void fix_symmetry(myarr<U_CArray> &ctmp) const {
          if ((startN0 == 0) && (localN0 > 0)) {
            ctmp.ref[0][0][0] = 0.0;
            ctmp.ref[0][0][N2_HC - 1] = 0.0;
            ctmp.ref[0][N1 / 2][0] = 0.0;
            ctmp.ref[0][N1 / 2][N2_HC - 1] = 0.0;
          }

          if ((startN0 <= N0 / 2) && (startN0 + localN0 > N0 / 2)) {
            ctmp.ref[N0 / 2][0][0] = 0.0;
            ctmp.ref[N0 / 2][0][N2_HC - 1] = 0.0;
            ctmp.ref[N0 / 2][N1 / 2][0] = 0.0;
            ctmp.ref[N0 / 2][N1 / 2][N2_HC - 1] = 0.0;
          }
        }

        // computes (axis0,axis1) component of tidal field:
        // K_ij = \Del_ij \delta
        // where
        //     \Del_ij \equiv \partial_i \partial_j/\nabla^2 - 1/3 \delta_ij
        //
        // and i-1 = axis0, j-1 = axis1, \delta = array_complex_in
        // - input array is in Fourier space (complex)
        // - output array is in real space
        void get_spatial_derivative_array3d_tidal(
            U_ArrayRef &deriv_array_real_out,
            const U_CArrayRef &array_complex_in, const int axis0,
            const int axis1) const {

          myarr<U_CArray> ctmp(
              arrs->mgr.extents_complex(), arrs->mgr.allocator_complex);
          double fft_normalization = 1.0 / (N0 * N1 * N2);

          Console::instance().print<LOG_DEBUG>("Spatial derivative: dtidal");
          array::copyArray3d(ctmp.ref, array_complex_in);

          Console::instance().c_assert(
              (axis0 >= 0) && (axis0 <= 2) && (axis1 >= 0) && (axis1 <= 2),
              "Invalid 'axis0/1' argument in "
              "'get_spatial_derivative_array3d'");

          double delta_ij = (axis0 == axis1) ? 1.0 / 3.0 : 0.0;

#  pragma omp parallel for collapse(3)
          for (size_t i = startN0; i < startN0 + localN0; i++)
            for (size_t j = 0; j < N1; j++)
              for (size_t k = 0; k < N2_HC; k++) {
                double kk[3] = {
                    kmode(i, N0, L0), kmode(j, N1, L1), kmode(k, N2, L2)};

                double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
                double factor = (kk[axis0] * kk[axis1] / ksquared - delta_ij) *
                                fft_normalization;
                ctmp.ref[i][j][k] *= factor;
              }

          fix_symmetry(ctmp);

          // transform ctmp array to real space -> deriv_array_real_out
          arrs->mgr.execute_c2r(
              arrs->synthesis_plan, ctmp.ref.data(),
              deriv_array_real_out.data());
        }

        // computes Laplacian of density field, \nabla^2 \delta
        // where \delta = array_complex_in
        // - input array is in Fourier space (complex)
        // - output array is in real space
        void get_spatial_derivative_array3d_laplace(
            U_ArrayRef &deriv_array_real_out,
            const U_CArrayRef &array_complex_in) const {

          myarr<U_CArray> ctmp(
              arrs->mgr.extents_complex(), arrs->mgr.allocator_complex);
          double fft_normalization = 1.0 / (N0 * N1 * N2);

          Console::instance().print<LOG_DEBUG>("Spatial derivative: dlaplace");
          array::copyArray3d(ctmp.ref, array_complex_in);

#  pragma omp parallel for collapse(3)
          for (size_t i = startN0; i < startN0 + localN0; i++)
            for (size_t j = 0; j < N1; j++)
              for (size_t k = 0; k < N2_HC; k++) {
                double kk[3] = {
                    kmode(i, N0, L0), kmode(j, N1, L1), kmode(k, N2, L2)};

                double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
                ctmp.ref[i][j][k] *= -1.0 * ksquared * fft_normalization;
              }

          fix_symmetry(ctmp);

          arrs->mgr.execute_c2r(
              arrs->synthesis_plan, ctmp.ref.data(),
              deriv_array_real_out.data());
        }

        // computes \Del_ij (a_1 a_2), where
        // a_1 = array1_real_in, a_2 = array2_real_in, and i-1 = axis0, j-1 = axis1
        // - both input arrays and output array are real
        void get_density_derivative_array3d_dtidal(
            U_ArrayRef &deriv_array_real_out, const U_ArrayRef &array1_real_in,
            const U_ArrayRef &array2_real_in, const int axis0,
            const int axis1) const {
          myarr<U_Array> tmp(
              arrs->mgr.extents_real(), arrs->mgr.allocator_real);
          myarr<U_CArray> ctmp(
              arrs->mgr.extents_complex(), arrs->mgr.allocator_complex);
          fwrap(tmp.ref) = fwrap(array1_real_in) * fwrap(array2_real_in);

          arrs->mgr.execute_r2c(
              arrs->analysis_plan, tmp.ref.data(), ctmp.ref.data());

          get_spatial_derivative_array3d_tidal(
              deriv_array_real_out, ctmp.ref, axis0, axis1);
        }

        // computes \nabla^2 a, where a = array1_real_in
        // - both input arrays and output array are real
        // - copy operations necessary to preserve input array (r2c destroys input array)
        void get_density_derivative_array3d_dlaplace(
            U_ArrayRef &deriv_array_real_out,
            const U_ArrayRef &array1_real_in) const {

          myarr<U_Array> tmp(
              arrs->mgr.extents_real(), arrs->mgr.allocator_real);
          myarr<U_CArray> ctmp(
              arrs->mgr.extents_complex(), arrs->mgr.allocator_complex);
          array::copyArray3d(tmp.ref, array1_real_in);

          arrs->mgr.execute_r2c(
              arrs->analysis_plan, tmp.ref.data(), ctmp.ref.data());

          get_spatial_derivative_array3d_laplace(
              deriv_array_real_out, ctmp.ref);
        }

        // apply sharp-k cut to field: modes with k > limit are set to zero
        // - also sets to zero \vec k==0 mode -> subtract mean
        void
        sharpk_filter(U_CArrayRef &field, double limit, double norm) const {
#  pragma omp parallel for collapse(3)
          for (size_t i = startN0; i < startN0 + localN0; i++)
            for (size_t j = 0; j < N1; j++)
              for (size_t k = 0; k < N2_HC; k++) {
                double kk[3] = {
                    kmode(i, N0, L0), kmode(j, N1, L1), kmode(k, N2, L2)};

                double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
                if (ksquared > limit * limit || ksquared < 1.e-15)
                  field[i][j][k] = 0.;
                else {
                  field[i][j][k] *= norm;
                }
              }
        }

        // evaluate prior for current parameter values
        template <typename BiasParameters>
        double getPriorLogProbability(const BiasParameters &par) const {
          double f = 0.;
          // note: start from i=1, since nmean is ignored throughout
          for (size_t i = 1; i < numParams; i++) {
            if (priorsigma[i] > 0.) {
              double D = par[i] - priormean[i];
              double sig2 = priorsigma[i] * priorsigma[i];
              f += D * D / sig2;
              f += log(sig2); // normalization (modulo 2pi)
            }
          }

          return -0.5 * f;
        }

        // fill bias fields in 'arrs'
        void prepare_bias_model_arrays(const U_ArrayRef &delta) {
          //          myarr<U_Array> tmp(arrs->mgr.extents_real(), arrs->mgr.allocator_real);
          myarr<U_CArray> ctmp(
              arrs->mgr.extents_complex(), arrs->mgr.allocator_complex);

          fwrap(LibLSS::array::slice_array(
              arrs->deltaLambda.ref, arrs->mgr.strict_range())) = fwrap(delta);

          // ctmp contains delta in Fourier space
          arrs->mgr.execute_r2c(
              arrs->analysis_plan, arrs->deltaLambda.ref.data(),
              ctmp.ref.data());

          // Eulerian sharpk filter
          sharpk_filter(ctmp.ref, EFT_Lambda, 1.);

          // compute \nabla^2 \delta and components of tidal field, all in real space
          get_spatial_derivative_array3d_laplace(
              arrs->laplace_delta.ref, ctmp.ref);
          get_spatial_derivative_array3d_tidal(
              arrs->tidal_00.ref, ctmp.ref, 0, 0);
          get_spatial_derivative_array3d_tidal(
              arrs->tidal_01.ref, ctmp.ref, 0, 1);
          get_spatial_derivative_array3d_tidal(
              arrs->tidal_02.ref, ctmp.ref, 0, 2);
          get_spatial_derivative_array3d_tidal(
              arrs->tidal_11.ref, ctmp.ref, 1, 1);
          get_spatial_derivative_array3d_tidal(
              arrs->tidal_12.ref, ctmp.ref, 1, 2);
          get_spatial_derivative_array3d_tidal(
              arrs->tidal_22.ref, ctmp.ref, 2, 2);

          // iFFT of ctmp to get sharp-k filtered density itself -> deltaLambda
          // -- normalization is applied below
          arrs->mgr.execute_c2r(
              arrs->synthesis_plan, ctmp.ref.data(),
              arrs->deltaLambda.ref.data());
          const double fft_normalization = 1.0 / (N0 * N1 * N2);

          // (K_ij)^2, delta^2
          // -- FS hand-looped version:
#  pragma omp parallel for collapse(3)
          for (size_t n0 = startN0; n0 < startN0 + localN0; n0++)
            for (size_t n1 = 0; n1 < N1; n1++)
              for (size_t n2 = 0; n2 < N2; n2++) {
                // K^2
                // - notice the factor of 2 in front of off-diagonal terms
                double K2 = arrs->tidal_00.ref[n0][n1][n2] *
                                arrs->tidal_00.ref[n0][n1][n2] +
                            arrs->tidal_11.ref[n0][n1][n2] *
                                arrs->tidal_11.ref[n0][n1][n2] +
                            arrs->tidal_22.ref[n0][n1][n2] *
                                arrs->tidal_22.ref[n0][n1][n2] +
                            2. * (arrs->tidal_01.ref[n0][n1][n2] *
                                      arrs->tidal_01.ref[n0][n1][n2] +
                                  arrs->tidal_02.ref[n0][n1][n2] *
                                      arrs->tidal_02.ref[n0][n1][n2] +
                                  arrs->tidal_12.ref[n0][n1][n2] *
                                      arrs->tidal_12.ref[n0][n1][n2]);
                arrs->tidal_sqr.ref[n0][n1][n2] = K2;

                // delta
                arrs->deltaLambda.ref[n0][n1][n2] *= fft_normalization;

                // delta^2
                double d = arrs->deltaLambda.ref[n0][n1][n2];
                arrs->delta_sqr.ref[n0][n1][n2] = d * d;
              }
        }

      public:
        // This adaptor transforms an unselected galaxy density (with appropriate
        // auxiliary arrays) to a selected array. It must be a functor accepting two
        // parameters: a selection virtual array and a bias density virtual array.
        // - SimpleAdaptor multiplies first returned field of compute_density with mask/selection array
        //   leaving other return values untouched
        selection::SimpleAdaptor selection_adaptor;

        EFTBias(LikelihoodInfo const &info = LikelihoodInfo()) {
          ConsoleContext<LOG_DEBUG> ctx("EFTBias constructor");

          // get Lambda
          EFT_Lambda = Likelihood::query<double>(info, "EFT_Lambda");

          // get sigma0 limits
          sigma0min = Likelihood::query<double>(info, "sigma0_min");
          if (!(sigma0min > 0.))
            sigma0min = 0.;
          sigma0max = Likelihood::query<double>(info, "sigma0_max");
          if (!(sigma0max > sigma0min))
            sigma0max = 1.e30;
          ctx.format("sigma0 limits: [%g, %g]", sigma0min, sigma0max);

          // reset priors
          lnPprior = 0.;
          priormean.resize(numParams);
          priorsigma.resize(numParams);
          for (size_t i = 0; i < numParams; i++) {
            priormean[i] = 0.;
            priorsigma[i] = -1.;
          }

          // get prior mean, sigma if available
          std::string smean =
              Likelihood::query<std::string>(info, "bias_prior_mean");
          if (smean.length()) {
            auto bias_double = string_as_vector<double>(smean, ", ");
            for (size_t i = 0; i < numParams; i++) {
              priormean[i] = i < bias_double.size() ? bias_double[i] : 0.;
            }
            ctx.print(
                "EFTBias: Set the bias prior mean to [" + to_string(priormean) +
                "]");
          }

          std::string ssigma =
              Likelihood::query<std::string>(info, "bias_prior_sigma");
          if (ssigma.length()) {
            auto bias_double = string_as_vector<double>(ssigma, ", ");
            for (size_t i = 0; i < numParams; i++) {
              priorsigma[i] = i < bias_double.size() ? bias_double[i] : 0.;
            }
            ctx.print(
                "EFTBias: Set the bias prior sigma to [" +
                to_string(priorsigma) + "]");
          }
        }

        template <typename BiasParameters>
        static inline void setup_default(BiasParameters &params) {
          params[0] = 1.;
          params[1] = 1.4;
          params[2] = 0.8;
          params[3] = 0.5;
          params[4] = 0.2;
          params[5] = 1.; //sigma_0
        }

        // Note: fwd_model and final_density arrays cannot be stored in this step. But
        // they can be used.
        template <
            class ForwardModel, typename FinalDensityArray,
            typename BiasParameters, typename MetaSelect = NoSelector>
        inline void prepare(
            ForwardModel &fwd_model, const FinalDensityArray &final_density,
            double const _nmean, const BiasParameters &params,
            bool density_changed, MetaSelect _select = MetaSelect()) {
          ConsoleContext<LOG_DEBUG> ctx("EFTBias preparation");

          // allocate bias fields
          if (arrs == nullptr)
            arrs.reset(new Arrs(
                *(fwd_model.lo_mgr->getComm()), *(fwd_model.lo_mgr.get())));

          // fill variables
          N0 = arrs->mgr.N0;
          N1 = arrs->mgr.N1;
          N2 = arrs->mgr.N2;
          N2_HC = N2 / 2 + 1;
          startN0 = arrs->mgr.startN0;
          localN0 = arrs->mgr.localN0;
          L0 = fwd_model.get_box_model().L0;
          L1 = fwd_model.get_box_model().L1;
          L2 = fwd_model.get_box_model().L2;
          nmean = params[0];
          b1 = params[1];
          b2 = params[2];
          bk = params[3];
          r2 = params[4];
          sigma_0 = params[5];

          // compute prior
          lnPprior = getPriorLogProbability(params);

          ctx.format("Got a box %dx%dx%d (%gx%gx%g)", N0, N1, N2, L0, L1, L2);
          if (density_changed) {
            // prepare density squared, Laplace delta, and tidal field squared
            // - note that these fields have nonzero mean, but this is removed in likelihood eft::sharpk_filter
            ctx.print("Prepare the arrays");
            prepare_bias_model_arrays(final_density);

            // compute variance of delta, delta^2, K^2 for checking
            // (note this is BEFORE sharp-k cut)
            double Md = 0., Md2 = 0., MK2 = 0.;
            double Vd = 0., Vd2 = 0., VK2 = 0.;
#  pragma omp parallel for collapse(3) reduction(+ : Md, Md2, MK2, Vd, Vd2, VK2)
            for (size_t n0 = startN0; n0 < startN0 + localN0; n0++)
              for (size_t n1 = 0; n1 < N1; n1++)
                for (size_t n2 = 0; n2 < N2; n2++) {
                  Md += final_density[n0][n1][n2];
                  Md2 += arrs->delta_sqr.ref[n0][n1][n2];
                  MK2 += arrs->tidal_sqr.ref[n0][n1][n2];
                  Vd += pow(final_density[n0][n1][n2], 2.);
                  Vd2 += pow(arrs->delta_sqr.ref[n0][n1][n2], 2.);
                  VK2 += pow(arrs->tidal_sqr.ref[n0][n1][n2], 2.);
                }
            double Md_glob = 0., Md2_glob = 0., MK2_glob = 0.;
            arrs->comm.all_reduce_t(&Md, &Md_glob, 1, MPI_SUM);
            arrs->comm.all_reduce_t(&Md2, &Md2_glob, 1, MPI_SUM);
            arrs->comm.all_reduce_t(&MK2, &MK2_glob, 1, MPI_SUM);
            Md_glob /= double(N0 * N1 * N2);
            Md2_glob /= double(N0 * N1 * N2);
            MK2_glob /= double(N0 * N1 * N2);
            double Vd_glob = 0., Vd2_glob = 0., VK2_glob = 0.;
            arrs->comm.all_reduce_t(&Vd, &Vd_glob, 1, MPI_SUM);
            arrs->comm.all_reduce_t(&Vd2, &Vd2_glob, 1, MPI_SUM);
            arrs->comm.all_reduce_t(&VK2, &VK2_glob, 1, MPI_SUM);
            Vd_glob = Vd_glob / double(N0 * N1 * N2) - Md_glob * Md_glob;
            Vd2_glob = Vd2_glob / double(N0 * N1 * N2) - Md2_glob * Md2_glob;
            VK2_glob = VK2_glob / double(N0 * N1 * N2) - MK2_glob * MK2_glob;
            ctx.format(
                "Mean of delta (BEFORE), delta^2, K^2 (AFTER Eulerian sharp-k "
                "cut): %.5e, %.5e, %.5e (Lambda = %.2e)",
                Md_glob, Md2_glob, MK2_glob, EFT_Lambda);
            ctx.format(
                "Variance of delta (BEFORE), delta^2, K^2 (AFTER Eulerian "
                "sharp-k cut): %.5e, %.5e, %.5e (Lambda = %.2e)",
                Vd_glob, Vd2_glob, VK2_glob, EFT_Lambda);
          }
        }

        inline void cleanup() {
          // Array deallocation only in final destructor
        }

        template <typename Array>
        inline bool check_bias_constraints(Array &&params) {
          // enforce sigma0 within parameter limits
          // FS: - while testing, also force b1 > 0;
          //       just remember to remove this before running on voids ;-)
          return (
              params[5] < sigma0max && params[5] > sigma0min && params[1] > 0.);
        }

        // This function returns an array-like array. That array
        // depends on the existence of the final density array.
        // The return type is quite complex. Let the compiler decide.
        template <typename FinalDensityArray>
        inline auto compute_density(const FinalDensityArray &array) const {
          // add rough renormalization
          double b1eff =
              (b1 - (b2 + 2. / 3. * bk) * 68. / 21. * rmsdelta_renorm *
                        rmsdelta_renorm);
          return std::make_tuple(
              b_va_fused<double>(
                  std::bind(
                      // bind biased-field function density_lambda to bias
                      // parameters and bias fields
                      density_lambda, nmean, b1eff, b2, bk, r2, ph::_1, ph::_2,
                      ph::_3, ph::_4),
                  // Notice no sharp-k cut on bias fields, including array = density, applied here.
                  // This cut is applied in EFTlikelihood.
                  array, arrs->delta_sqr.ref, arrs->tidal_sqr.ref,
                  arrs->laplace_delta.ref),
              *LibLSS::constant<double, 3>(
                  sigma_0, arrs->mgr.extents_real_strict()),
              *LibLSS::constant<double, 3>(
                  lnPprior, arrs->mgr.extents_real_strict()));
        }

        // This function returns an array-like array. That array
        // depends on the existence of the final density array and the gradient likelihood array.
        // That is the job of the caller to ensure that temporary variables are not cleared
        // before the final use.
        // The return type is quite complex. Let the compiler decide.
        // L(b_0(delta, p), b_1(delta, p), ..., b_n(delta, p))
        // Now we take a tuple of gradient and collapse this to a gradient of delta.
        //
        // FS: we pre-compute the bias fields (see prepare( )) but not their adjoints.
        //     Does this make sense? I guess adjoint is only called when phases are changed,
        //     in which case we anyway have to recompute; bias fields are also needed in
        //     block sampling of bias parameters, where their precomputation helps.
        template <
            typename FinalDensityArray, typename TupleGradientLikelihoodArray>
        auto apply_adjoint_gradient(
            const FinalDensityArray &final_density,
            TupleGradientLikelihoodArray grad_array) {
          ConsoleContext<LOG_DEBUG> ctx("EFTBias gradient computation");

          ctx.print("Transfer the input gradient");

          myarr<U_Array> dlogL_drho(
              arrs->mgr.extents_real(), arrs->mgr.allocator_real);
          LibLSS::copy_array_rv(
              array::slice_array((dlogL_drho.ref), arrs->mgr.strict_range()),
              std::get<0>(grad_array));
          ctx.print("Data backed up");

          myarr<U_Array> tmp(
              arrs->mgr.extents_real(), arrs->mgr.allocator_real),
              // this will contain functional derivative of K^2 term:
              deriv_sum(arrs->mgr.extents_real(), arrs->mgr.allocator_real),
              // this will contain functional derivative of \nabla^2\delta term:
              dlaplace_delta(
                  arrs->mgr.extents_real(), arrs->mgr.allocator_real);

          // Functional derivatives of fields under derivative operators are
          // treated through integration by parts. See pt_borg/notes/borg_implementation_notes.

          // derivative of K^2 term:
          // compute \Del_ij ( dlogL_drho K^ij )
          // - component by component and sum up
          // - notice the factor of 2 in front of off-diagonal terms
          // - overall factor of 2 from product rule added in loop below
          get_density_derivative_array3d_dtidal(
              tmp.ref, dlogL_drho.ref, arrs->tidal_01.ref, 0, 1);
          fwrap(deriv_sum.ref) = 2 * fwrap(tmp.ref);
          get_density_derivative_array3d_dtidal(
              tmp.ref, dlogL_drho.ref, arrs->tidal_02.ref, 0, 2);
          fwrap(deriv_sum.ref) = fwrap(deriv_sum.ref) + 2 * fwrap(tmp.ref);
          get_density_derivative_array3d_dtidal(
              tmp.ref, dlogL_drho.ref, arrs->tidal_12.ref, 1, 2);
          fwrap(deriv_sum.ref) = fwrap(deriv_sum.ref) + 2 * fwrap(tmp.ref);
          get_density_derivative_array3d_dtidal(
              tmp.ref, dlogL_drho.ref, arrs->tidal_00.ref, 0, 0);
          fwrap(deriv_sum.ref) = fwrap(deriv_sum.ref) + fwrap(tmp.ref);
          get_density_derivative_array3d_dtidal(
              tmp.ref, dlogL_drho.ref, arrs->tidal_11.ref, 1, 1);
          fwrap(deriv_sum.ref) = fwrap(deriv_sum.ref) + fwrap(tmp.ref);
          get_density_derivative_array3d_dtidal(
              tmp.ref, dlogL_drho.ref, arrs->tidal_22.ref, 2, 2);
          fwrap(deriv_sum.ref) = fwrap(deriv_sum.ref) + fwrap(tmp.ref);

          // derivative of \nabla^2 \delta: take Laplacian of dlogL_drho times (-1)^2
          get_density_derivative_array3d_dlaplace(
              dlaplace_delta.ref, dlogL_drho.ref);

          // now assemble total adjoint gradient
          double b1eff =
              (b1 - (b2 + 2. / 3. * bk) * 68. / 21. * rmsdelta_renorm *
                        rmsdelta_renorm);
          ctx.print("Computing the transform.");
#  pragma omp parallel for collapse(3)
          for (size_t n0 = startN0; n0 < startN0 + localN0; n0++)
            for (size_t n1 = 0; n1 < N1; n1++)
              for (size_t n2 = 0; n2 < N2; n2++) {
                double rho = b1eff * final_density[n0][n1][n2] +
                             b2 * arrs->delta_sqr.ref[n0][n1][n2] +
                             bk * arrs->tidal_sqr.ref[n0][n1][n2] +
                             r2 * arrs->laplace_delta.ref[n0][n1][n2];
                double dmu_drho = adjoint_thresholder(
                    1 + rho, EPSILON_VOIDS, dlogL_drho.ref[n0][n1][n2]);

                double drho_ddelta = b1 + 2. * b2 * final_density[n0][n1][n2];

                arrs->dlogL_ddelta.ref[n0][n1][n2] =
                    nmean * (dmu_drho * drho_ddelta +
                             2. * bk * deriv_sum.ref[n0][n1][n2] +
                             r2 * dlaplace_delta.ref[n0][n1][n2]);
              }

          // apply sharp-k filter to dlogL_ddelta.
          myarr<U_CArray> ctmp(
              arrs->mgr.extents_complex(), arrs->mgr.allocator_complex);
          arrs->mgr.execute_r2c(
              arrs->analysis_plan, arrs->dlogL_ddelta.ref.data(),
              ctmp.ref.data());
          double fft_normalization = 1.0 / (N0 * N1 * N2);
          sharpk_filter(ctmp.ref, EFT_Lambda, fft_normalization);
          arrs->mgr.execute_c2r(
              arrs->synthesis_plan, ctmp.ref.data(),
              arrs->dlogL_ddelta.ref.data());

          return std::make_tuple(std::ref(arrs->dlogL_ddelta.ref));
        }
      };

    } // namespace detail_EFTBias

    using detail_EFTBias::EFTBias;

    // define type names for convenience
    using EFTBiasThresh = EFTBias<true>;
    using EFTBiasDefault = EFTBias<false>;

  } // namespace bias

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
