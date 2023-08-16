/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/bias/2nd_order_bias.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHYSICS_2ND_ORDER_BIAS_HPP
#define __LIBLSS_PHYSICS_2ND_ORDER_BIAS_HPP

// This header provides the implementation of the LSS bias model to second order PT.

#include <cmath>
#include <boost/bind.hpp>
#include <boost/format.hpp>
#include "libLSS/tools/fused_array.hpp"
#include <tuple>
#include "libLSS/tools/phoenix_vars.hpp"
#include <boost/phoenix/operator.hpp>
#include <boost/phoenix/stl/cmath.hpp>
#include "libLSS/tools/tuple_helper.hpp"
#include "libLSS/physics/bias/base.hpp"
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/tools/fftw_allocator.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"

namespace LibLSS {

  namespace bias {

    namespace detail_SecondOrderBias {

      using boost::format;
      namespace ph = std::placeholders;

      typedef FFTW_Manager_3d<double> DFT_Manager;
      typedef Uninit_FFTW_Real_Array U_Array;
      typedef Uninit_FFTW_Complex_Array U_CArray;
      typedef Uninit_FFTW_Real_Array::array_type U_ArrayRef;
      typedef Uninit_FFTW_Complex_Array::array_type U_CArrayRef;

      struct SecondOrderBias {

        // By default just do truncation, otherwise a smooth cut can be applied
        static constexpr const bool NmeanIsBias = false;
        static const bool SHARP_THRESHOLDER = true;
        static constexpr double EPSILON_VOIDS = 1e-6;
        static const auto numParams = 4;
        long N0;
        long N1;
        long N2;
        long N2_HC;
        long startN0;
        long localN0;
        double L0;
        double L1;
        double L2;
        double nmean;
        double b1;
        double b2;
        double bk;
        double r2;

        MPI_Communication *comm;
        DFT_Manager *mgr;
        FCalls::plan_type analysis_plan;
        FCalls::plan_type synthesis_plan;

        U_Array *delta_sqr_arr;
        U_Array *tidal_00_arr, *tidal_11_arr, *tidal_22_arr, *tidal_01_arr,
            *tidal_02_arr, *tidal_12_arr, *tidal_sqr_arr;
        U_Array *laplace_delta_arr;
        U_ArrayRef *delta_sqr_ref;
        U_ArrayRef *tidal_00_ref, *tidal_11_ref, *tidal_22_ref, *tidal_01_ref,
            *tidal_02_ref, *tidal_12_ref, *tidal_sqr_ref;
        U_ArrayRef *laplace_delta_ref;

        U_Array *t00_dt00_arr, *t11_dt11_arr, *t22_dt22_arr, *t01_dt01_arr,
            *t02_dt02_arr, *t12_dt12_arr;
        U_Array *dlaplace_delta_arr;
        U_ArrayRef *t00_dt00_ref, *t11_dt11_ref, *t22_dt22_ref, *t01_dt01_ref,
            *t02_dt02_ref, *t12_dt12_ref;
        U_ArrayRef *dlaplace_delta_ref;

        U_Array *dlogL_drho_arr;
        U_Array *dlogL_ddelta_arr;
        U_ArrayRef *dlogL_drho_ref;
        U_ArrayRef *dlogL_ddelta_ref;

        U_Array *tmp_array_real_arr;
        U_ArrayRef *tmp_array_real_ref;
        U_CArray *tmp_array_complex_arr;
        U_CArrayRef *tmp_array_complex_ref;

        // This adaptor transforms an unselected galaxy density (with appropriate
        // auxiliary arrays) to a selected array. It must be a functor accepting two
        // parameters: a selection virtual array and a bias density virtual array.
        selection::SimpleAdaptor selection_adaptor;

        SecondOrderBias() {
          delta_sqr_arr = 0;
          tidal_00_arr = 0;
          tidal_11_arr = 0;
          tidal_22_arr = 0;
          tidal_01_arr = 0;
          tidal_02_arr = 0;
          tidal_12_arr = 0;
          laplace_delta_arr = 0;
          dlaplace_delta_arr = 0;
          t00_dt00_arr = 0;
          t11_dt11_arr = 0;
          t22_dt22_arr = 0;
          t01_dt01_arr = 0;
          t02_dt02_arr = 0;
          t12_dt12_arr = 0;
          tidal_sqr_arr = 0;

          dlogL_drho_arr = 0;
          dlogL_ddelta_arr = 0;

          tmp_array_real_arr = 0;
          tmp_array_complex_arr = 0;

          analysis_plan = 0;
          synthesis_plan = 0;
        }

        template <typename BiasParameters>
        static inline void setup_default(BiasParameters &params) {
          params[0] = 1.4;
          params[1] = 0.8;
          params[2] = 0.5;
          params[3] = 0.2;
        };

        // Note: fwd_model and final_density arrays cannot be stored in this step. But
        // they can be used.
        template <
            class ForwardModel, typename FinalDensityArray,
            typename BiasParameters, typename MetaSelect = NoSelector>
        inline void prepare(
            ForwardModel &fwd_model, const FinalDensityArray &final_density,
            double const _nmean, const BiasParameters &params,
            bool density_changed, MetaSelect _select = MetaSelect()) {

          ConsoleContext<LOG_DEBUG> ctx("bias model preparation");

          comm = fwd_model.lo_mgr->getComm();
          mgr = fwd_model.lo_mgr.get();
          N0 = mgr->N0;
          N1 = mgr->N1;
          N2 = mgr->N2;
          N2_HC = N2 / 2 + 1;
          startN0 = mgr->startN0;
          localN0 = mgr->localN0;
          L0 = fwd_model.get_box_model().L0;
          L1 = fwd_model.get_box_model().L1;
          L2 = fwd_model.get_box_model().L2;
          nmean = _nmean;
          b1 = params[0];
          b2 = params[1];
          bk = params[2];
          r2 = params[3];

          ctx.print(
              boost::format("Got a box %dx%dx%d (%gx%gx%g)") % N0 % N1 % N2 %
              L0 % L1 % L2);
          ctx.print("Allocating temporary arrays");
          if (delta_sqr_arr == NULL) {
            ctx.print("...delta_sqr_arr");
            delta_sqr_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            delta_sqr_ref = &delta_sqr_arr->get_array();
          }

          if (tidal_00_arr == NULL) {
            ctx.print("...tidal_00_arr");
            tidal_00_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            tidal_00_ref = &tidal_00_arr->get_array();
          }

          if (tidal_11_arr == NULL) {
            ctx.print("...tidal_11_arr");
            tidal_11_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            tidal_11_ref = &tidal_11_arr->get_array();
          }

          if (tidal_22_arr == NULL) {
            ctx.print("...tidal_22_arr");
            tidal_22_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            tidal_22_ref = &tidal_22_arr->get_array();
          }

          if (tidal_01_arr == NULL) {
            ctx.print("...tidal_01_arr");
            tidal_01_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            tidal_01_ref = &tidal_01_arr->get_array();
          }

          if (tidal_02_arr == NULL) {
            ctx.print("...tidal_02_arr");
            tidal_02_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            tidal_02_ref = &tidal_02_arr->get_array();
          }

          if (tidal_12_arr == NULL) {
            ctx.print("...tidal_12_arr");
            tidal_12_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            tidal_12_ref = &tidal_12_arr->get_array();
          }

          if (tidal_sqr_arr == NULL) {
            ctx.print("...tidal_sqr_arr");
            tidal_sqr_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            tidal_sqr_ref = &tidal_sqr_arr->get_array();
          }

          if (laplace_delta_arr == NULL) {
            ctx.print("...laplace_delta_arr");
            laplace_delta_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            laplace_delta_ref = &laplace_delta_arr->get_array();
          }

          if (t00_dt00_arr == NULL) {
            ctx.print("...t00_dt00_arr");
            t00_dt00_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            t00_dt00_ref = &t00_dt00_arr->get_array();
          }

          if (t11_dt11_arr == NULL) {
            ctx.print("...t11_dt11_arr");
            t11_dt11_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            t11_dt11_ref = &t11_dt11_arr->get_array();
          }

          if (t22_dt22_arr == NULL) {
            ctx.print("...t22_dt22_arr");
            t22_dt22_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            t22_dt22_ref = &t22_dt22_arr->get_array();
          }

          if (t01_dt01_arr == NULL) {
            ctx.print("...t01_dt01_arr");
            t01_dt01_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            t01_dt01_ref = &t01_dt01_arr->get_array();
          }

          if (t02_dt02_arr == NULL) {
            ctx.print("...t02_dt02_arr");
            t02_dt02_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            t02_dt02_ref = &t02_dt02_arr->get_array();
          }

          if (t12_dt12_arr == NULL) {
            ctx.print("...t12_dt12_arr");
            t12_dt12_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            t12_dt12_ref = &t12_dt12_arr->get_array();
          }

          if (dlaplace_delta_arr == NULL) {
            ctx.print("...dlaplace_delta_arr");
            dlaplace_delta_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            dlaplace_delta_ref = &dlaplace_delta_arr->get_array();
          }

          if (dlogL_drho_arr == NULL) {
            ctx.print("...dlogL_drho_arr");
            dlogL_drho_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            dlogL_drho_ref = &dlogL_drho_arr->get_array();
          }

          if (dlogL_ddelta_arr == NULL) {
            ctx.print("...dlogL_ddelta_arr");
            dlogL_ddelta_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            dlogL_ddelta_ref = &dlogL_ddelta_arr->get_array();
          }

          if (tmp_array_real_arr == NULL) {
            ctx.print("...tmp_array_real_arr");
            tmp_array_real_arr =
                new U_Array(mgr->extents_real(), mgr->allocator_real);
            tmp_array_real_ref = &tmp_array_real_arr->get_array();
          }

          if (tmp_array_complex_arr == NULL) {
            ctx.print("...tmp_array_complex_arr");
            tmp_array_complex_arr =
                new U_CArray(mgr->extents_complex(), mgr->allocator_complex);
            tmp_array_complex_ref = &tmp_array_complex_arr->get_array();
          }
          ctx.print("FFT plans now");

          if (analysis_plan == NULL) {
            ctx.print("...analysis");
            analysis_plan = mgr->create_r2c_plan(
                tmp_array_real_ref->data(), tmp_array_complex_ref->data());
          }

          if (synthesis_plan == NULL) {
            ctx.print("...synthesis");
            synthesis_plan = mgr->create_c2r_plan(
                tmp_array_complex_ref->data(), tmp_array_real_ref->data());
          }

          ctx.print("Prepare the arrays");
          if (density_changed)
            prepare_bias_model_arrays(
                *delta_sqr_ref, *tidal_00_ref, *tidal_11_ref, *tidal_22_ref,
                *tidal_01_ref, *tidal_02_ref, *tidal_12_ref, *tidal_sqr_ref,
                *laplace_delta_ref, final_density);
          ctx.print("Done preparation");
        };

        inline void cleanup(){
            // Array deallocation only in final destructor
        };

        inline double get_linear_bias() const { return b1; };

        template <typename Array>
        static inline bool check_bias_constraints(Array &&a) {
          return true;
        };

        void subtract_mean_array3d(U_ArrayRef &data_ref) {
          ConsoleContext<LOG_DEBUG> ctx("subtract_mean_array3d");

          double mean_data = 0.0;

#pragma omp parallel for collapse(3) reduction(+ : mean_data)
          for (size_t n0 = startN0; n0 < startN0 + localN0; n0++)
            for (size_t n1 = 0; n1 < N1; n1++)
              for (size_t n2 = 0; n2 < N2; n2++) {
                mean_data += data_ref[n0][n1][n2];
              }

          comm->all_reduce_t(MPI_IN_PLACE, &mean_data, 1, MPI_SUM);
          mean_data /= N0 * N1 * N2;

#pragma omp parallel for collapse(3)
          for (size_t n0 = startN0; n0 < startN0 + localN0; n0++)
            for (size_t n1 = 0; n1 < N1; n1++)
              for (size_t n2 = 0; n2 < N2; n2++) {
                data_ref[n0][n1][n2] -= mean_data;
              }
        };

        void get_spatial_derivative_array3d(
            U_ArrayRef &deriv_array_real_out,
            const U_CArrayRef &array_complex_in, const int axis0,
            const int axis1, const std::string type) {

          double fft_normalization = 1.0 / (N0 * N1 * N2);

          Console::instance().print<LOG_DEBUG>("Spatial derivative: " + type);
          array::copyArray3d(*tmp_array_complex_ref, array_complex_in);

          if (type == "laplace") {
#pragma omp parallel for collapse(3)
            for (size_t i = startN0; i < startN0 + localN0; i++)
              for (size_t j = 0; j < N1; j++)
                for (size_t k = 0; k < N2_HC; k++) {
                  double kk[3] = {kmode(i, N0, L0), kmode(j, N1, L1),
                                  kmode(k, N2, L2)};

                  double ksquared =
                      kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
                  double factor = -1.0 * ksquared * fft_normalization;
                  (*tmp_array_complex_ref)[i][j][k] *= factor;
                }
          } else if (type == "tidal") {
            Console::instance().c_assert(
                (axis0 >= 0) && (axis0 <= 2) && (axis1 >= 0) && (axis1 <= 2),
                "Invalid 'axis0/1' argument in "
                "'get_spatial_derivative_array3d'");

            double delta_ij = (axis0 == axis1) ? 1.0 / 3.0 : 0.0;

#pragma omp parallel for collapse(3)
            for (size_t i = startN0; i < startN0 + localN0; i++)
              for (size_t j = 0; j < N1; j++)
                for (size_t k = 0; k < N2_HC; k++) {
                  double kk[3] = {kmode(i, N0, L0), kmode(j, N1, L1),
                                  kmode(k, N2, L2)};

                  double ksquared =
                      kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
                  double factor =
                      (kk[axis0] * kk[axis1] / ksquared - delta_ij) *
                      fft_normalization;
                  (*tmp_array_complex_ref)[i][j][k] *= factor;
                }
          } else {
            Console::instance().c_assert(
                false,
                "Invalid 'type' argument in 'get_spatial_derivative_array3d'");
          }

          if ((startN0 == 0) && (localN0 > 0)) {
            (*tmp_array_complex_ref)[0][0][0] = 0.0;
            (*tmp_array_complex_ref)[0][0][N2_HC - 1] = 0.0;
            (*tmp_array_complex_ref)[0][N1 / 2][0] = 0.0;
            (*tmp_array_complex_ref)[0][N1 / 2][N2_HC - 1] = 0.0;
          }

          if ((startN0 <= N0 / 2) && (startN0 + localN0 > N0 / 2)) {
            (*tmp_array_complex_ref)[N0 / 2][0][0] = 0.0;
            (*tmp_array_complex_ref)[N0 / 2][0][N2_HC - 1] = 0.0;
            (*tmp_array_complex_ref)[N0 / 2][N1 / 2][0] = 0.0;
            (*tmp_array_complex_ref)[N0 / 2][N1 / 2][N2_HC - 1] = 0.0;
          }

          mgr->execute_c2r(
              synthesis_plan, tmp_array_complex_ref->data(),
              deriv_array_real_out.data());
        };

        void get_density_derivative_array3d(
            U_ArrayRef &deriv_array_real_out, const U_ArrayRef &array1_real_in,
            const U_ArrayRef &array2_real_in, const int axis0, const int axis1,
            const std::string type) {

          if (type == "dlaplace") {

            array::copyArray3d(*tmp_array_real_ref, array1_real_in);

            mgr->execute_r2c(
                analysis_plan, tmp_array_real_ref->data(),
                tmp_array_complex_ref->data());

            get_spatial_derivative_array3d(
                deriv_array_real_out, *tmp_array_complex_ref, -1, -1,
                "laplace");

          } else if (type == "dtidal") {

#pragma omp parallel for collapse(3)
            for (size_t i = startN0; i < startN0 + localN0; i++)
              for (size_t j = 0; j < N1; j++)
                for (size_t k = 0; k < N2; k++) {
                  (*tmp_array_real_ref)[i][j][k] =
                      array1_real_in[i][j][k] * array2_real_in[i][j][k];
                }

            mgr->execute_r2c(
                analysis_plan, tmp_array_real_ref->data(),
                tmp_array_complex_ref->data());

            get_spatial_derivative_array3d(
                deriv_array_real_out, *tmp_array_complex_ref, axis0, axis1,
                "tidal");

          } else {
            Console::instance().c_assert(
                false,
                "Invalid 'type' argument in 'get_density_derivative_array3d'");
          }
        };

        void prepare_bias_model_arrays(
            U_ArrayRef &delta_sqr_ref, U_ArrayRef &tidal_00_ref,
            U_ArrayRef &tidal_11_ref, U_ArrayRef &tidal_22_ref,
            U_ArrayRef &tidal_01_ref, U_ArrayRef &tidal_02_ref,
            U_ArrayRef &tidal_12_ref, U_ArrayRef &tidal_sqr_ref,
            U_ArrayRef &laplace_delta_ref, const U_ArrayRef &delta) {

#pragma omp parallel for collapse(3)
          for (size_t n0 = startN0; n0 < startN0 + localN0; n0++)
            for (size_t n1 = 0; n1 < N1; n1++)
              for (size_t n2 = 0; n2 < N2; n2++) {
                (*tmp_array_real_ref)[n0][n1][n2] = delta[n0][n1][n2];
              }
          Console::instance().print<LOG_DEBUG>("Input backuped");

          mgr->execute_r2c(
              analysis_plan, tmp_array_real_ref->data(),
              tmp_array_complex_ref->data());
          Console::instance().print<LOG_DEBUG>("Transformed");

          get_spatial_derivative_array3d(
              laplace_delta_ref, *tmp_array_complex_ref, -1, -1, "laplace");

          get_spatial_derivative_array3d(
              tidal_00_ref, *tmp_array_complex_ref, 0, 0, "tidal");
          get_spatial_derivative_array3d(
              tidal_01_ref, *tmp_array_complex_ref, 0, 1, "tidal");
          get_spatial_derivative_array3d(
              tidal_02_ref, *tmp_array_complex_ref, 0, 2, "tidal");

          get_spatial_derivative_array3d(
              tidal_11_ref, *tmp_array_complex_ref, 1, 1, "tidal");
          get_spatial_derivative_array3d(
              tidal_12_ref, *tmp_array_complex_ref, 1, 2, "tidal");

          get_spatial_derivative_array3d(
              tidal_22_ref, *tmp_array_complex_ref, 2, 2, "tidal");

#pragma omp parallel for collapse(3)
          for (size_t n0 = startN0; n0 < startN0 + localN0; n0++)
            for (size_t n1 = 0; n1 < N1; n1++)
              for (size_t n2 = 0; n2 < N2; n2++) {
                delta_sqr_ref[n0][n1][n2] =
                    delta[n0][n1][n2] * delta[n0][n1][n2];
                tidal_sqr_ref[n0][n1][n2] =
                    tidal_00_ref[n0][n1][n2] * tidal_00_ref[n0][n1][n2] +
                    tidal_11_ref[n0][n1][n2] * tidal_11_ref[n0][n1][n2] +
                    tidal_22_ref[n0][n1][n2] * tidal_22_ref[n0][n1][n2] +
                    2.0 * (tidal_01_ref[n0][n1][n2] * tidal_01_ref[n0][n1][n2] +
                           tidal_02_ref[n0][n1][n2] * tidal_02_ref[n0][n1][n2] +
                           tidal_12_ref[n0][n1][n2] * tidal_12_ref[n0][n1][n2]);
              }

          subtract_mean_array3d(delta_sqr_ref);

          subtract_mean_array3d(tidal_sqr_ref);
        };

        void prepare_bias_model_derivative_arrays(
            U_ArrayRef &t00_dt00_ref, U_ArrayRef &t11_dt11_ref,
            U_ArrayRef &t22_dt22_ref, U_ArrayRef &t01_dt01_ref,
            U_ArrayRef &t02_dt02_ref, U_ArrayRef &t12_dt12_ref,
            U_ArrayRef &dlaplace_delta_ref, const U_ArrayRef &dlogL_drho_ref,
            const U_ArrayRef &tidal_00_ref, const U_ArrayRef &tidal_11_ref,
            const U_ArrayRef &tidal_22_ref, const U_ArrayRef &tidal_01_ref,
            const U_ArrayRef &tidal_02_ref, const U_ArrayRef &tidal_12_ref) {

          U_ArrayRef *NULL_ref;

          get_density_derivative_array3d(
              t00_dt00_ref, dlogL_drho_ref, tidal_00_ref, 0, 0, "dtidal");
          get_density_derivative_array3d(
              t01_dt01_ref, dlogL_drho_ref, tidal_01_ref, 0, 1, "dtidal");
          get_density_derivative_array3d(
              t02_dt02_ref, dlogL_drho_ref, tidal_02_ref, 0, 2, "dtidal");

          get_density_derivative_array3d(
              t11_dt11_ref, dlogL_drho_ref, tidal_11_ref, 1, 1, "dtidal");
          get_density_derivative_array3d(
              t12_dt12_ref, dlogL_drho_ref, tidal_12_ref, 1, 2, "dtidal");

          get_density_derivative_array3d(
              t22_dt22_ref, dlogL_drho_ref, tidal_22_ref, 2, 2, "dtidal");

          get_density_derivative_array3d(
              dlaplace_delta_ref, dlogL_drho_ref, *NULL_ref, -1, -1,
              "dlaplace");
        };

        static inline double thresholder(double a, double b) {
          if (a < b) {
            if (SHARP_THRESHOLDER) {
              return b;
            } else {
              return b * std::exp((-b / a + 1));
            }
          } else {
            return a;
          }
        }

        static inline double adjoint_thresholder(double a, double b, double g) {
          if (a < b) {
            if (SHARP_THRESHOLDER) {
              return 0;
            } else {
              return b * b / (a * a) * std::exp((1 - b / a)) * g;
            }
          } else {
            return g;
          }
        }

        static inline double density_lambda(
            double nmean, double b1, double b2, double bk, double r2,
            double delta, double delta_sqr, double tidal_sqr,
            double laplace_delta) {
          double rho = b1 * delta + 0.5 * b2 * delta_sqr +
                       0.5 * bk * tidal_sqr + r2 * laplace_delta;
          double nu = nmean * thresholder(1.0 + rho, EPSILON_VOIDS);
          return nu;
        };

        // This function returns an array-like array. That array
        // depends on the existence of the final density array.
        // The return type is quite complex. Let the compiler decides.
        // C++11 does not allow automatic return type deduction. C++14 would be
        // needed for that. So we have to rely on an auxiliary function that
        // allow for a compact decltype to be written.
        template <typename FinalDensityArray>
        inline auto compute_density(const FinalDensityArray &array)
            -> decltype(std::make_tuple(b_va_fused<double>(
                std::bind(
                    density_lambda, nmean, b1, b2, bk, r2, ph::_1, ph::_2,
                    ph::_3, ph::_4),
                array, *delta_sqr_ref, *tidal_sqr_ref, *laplace_delta_ref))) {
          return std::make_tuple(b_va_fused<double>(
              std::bind(
                  density_lambda, nmean, b1, b2, bk, r2, ph::_1, ph::_2, ph::_3,
                  ph::_4),
              array, *delta_sqr_ref, *tidal_sqr_ref, *laplace_delta_ref));
        };

        // This function returns an array-like array. That array
        // depends on the existence of the final density array and the gradient likelihood array.
        // That is the job of the caller to ensure that temporary variables are not cleared
        // before the final use.
        // The return type is quite complex. Let the compiler decides.
        // L(b_0(delta, p), b_1(delta, p), ..., b_n(delta, p))
        // Now we take a tuple of gradient and collapse this to a gradient of delta.
        template <
            typename FinalDensityArray, typename TupleGradientLikelihoodArray>
        auto apply_adjoint_gradient(
            const FinalDensityArray &final_density,
            TupleGradientLikelihoodArray grad_array)
            -> decltype(std::make_tuple(std::ref(*dlogL_ddelta_ref))) {
          ConsoleContext<LOG_DEBUG> ctx("bias model gradient computation");

          ctx.print("Zero output array");

          array::fill(*dlogL_ddelta_ref, 0.0);

          ctx.print("Transfer the input gradient");

          const double epsilon = EPSILON_VOIDS;
          LibLSS::copy_array_rv(
              array::slice_array((*dlogL_drho_ref), mgr->strict_range()),
              std::get<0>(grad_array));
          ctx.print("Data backuped");

          prepare_bias_model_derivative_arrays(
              *t00_dt00_ref, *t11_dt11_ref, *t22_dt22_ref, *t01_dt01_ref,
              *t02_dt02_ref, *t12_dt12_ref, *dlaplace_delta_ref,
              *dlogL_drho_ref, *tidal_00_ref, *tidal_11_ref, *tidal_22_ref,
              *tidal_01_ref, *tidal_02_ref, *tidal_12_ref);

          ctx.print("Computing the transform.");
#pragma omp parallel for collapse(3)
          for (size_t n0 = startN0; n0 < startN0 + localN0; n0++)
            for (size_t n1 = 0; n1 < N1; n1++)
              for (size_t n2 = 0; n2 < N2; n2++) {

                double delta = (final_density)[n0][n1][n2];
                double delta_sqr = (*delta_sqr_ref)[n0][n1][n2];
                double tidal_sqr = (*tidal_sqr_ref)[n0][n1][n2];
                double laplace_delta = (*laplace_delta_ref)[n0][n1][n2];

                double rho = b1 * delta + 0.5 * b2 * delta_sqr +
                             0.5 * bk * tidal_sqr + r2 * laplace_delta;
                double dmu_drho = adjoint_thresholder(
                    1 + rho, EPSILON_VOIDS, (*dlogL_drho_ref)[n0][n1][n2]);

                double dlaplace_delta = (*dlaplace_delta_ref)[n0][n1][n2];
                double t00_dt00 = (*t00_dt00_ref)[n0][n1][n2];
                double t11_dt11 = (*t11_dt11_ref)[n0][n1][n2];
                double t22_dt22 = (*t22_dt22_ref)[n0][n1][n2];
                double t01_dt01 = (*t01_dt01_ref)[n0][n1][n2];
                double t02_dt02 = (*t02_dt02_ref)[n0][n1][n2];
                double t12_dt12 = (*t12_dt12_ref)[n0][n1][n2];

                double drho_ddelta = b1 + b2 * delta;

                (*dlogL_ddelta_ref)[n0][n1][n2] =
                    nmean * (dmu_drho * drho_ddelta +
                             bk * (t00_dt00 + t11_dt11 + t22_dt22 +
                                   2.0 * (t01_dt01 + t02_dt02 + t12_dt12)) +
                             r2 * dlaplace_delta);
              }

          return std::make_tuple(std::ref(*dlogL_ddelta_ref));
        };

        virtual ~SecondOrderBias() {
          delete delta_sqr_arr;
          delete tidal_00_arr;
          delete tidal_11_arr;
          delete tidal_22_arr;
          delete tidal_01_arr;
          delete tidal_02_arr;
          delete tidal_12_arr;
          delete tidal_sqr_arr;
          delete laplace_delta_arr;
          delete t00_dt00_arr;
          delete t11_dt11_arr;
          delete t22_dt22_arr;
          delete t01_dt01_arr;
          delete t02_dt02_arr;
          delete t12_dt12_arr;
          delete dlaplace_delta_arr;
          delete dlogL_drho_arr;
          delete dlogL_ddelta_arr;
          delete tmp_array_real_arr;
          delete tmp_array_complex_arr;
          mgr->destroy_plan(analysis_plan);
          mgr->destroy_plan(synthesis_plan);
        };
      };

    }; // namespace detail_SecondOrderBias

    using detail_SecondOrderBias::SecondOrderBias;

  }; // namespace bias

}; // namespace LibLSS

#endif
