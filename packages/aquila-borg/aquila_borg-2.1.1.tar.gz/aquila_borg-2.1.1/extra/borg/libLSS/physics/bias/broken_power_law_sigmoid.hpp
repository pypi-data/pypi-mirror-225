/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/bias/broken_power_law_sigmoid.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHYSICS_BROKEN_POWER_LAW_SIGMOID_BIAS_HPP
#define __LIBLSS_PHYSICS_BROKEN_POWER_LAW_SIGMOID_BIAS_HPP

#include <cmath>
#include <boost/bind.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/physics/bias/base.hpp"
#include <boost/tuple/tuple.hpp>

namespace LibLSS {

  namespace bias {

    namespace detail {

      struct BrokenPowerLawSigmoid {
        static constexpr const int numParams = 6;
        static constexpr const bool NmeanIsBias = true;

        double alpha, epsilon, rho_g, k, rho_th;
        double nmean;

        selection::SimpleAdaptor selection_adaptor;

        BrokenPowerLawSigmoid(LikelihoodInfo const& = LikelihoodInfo()) {}

        template <typename Array>
        static inline bool check_bias_constraints(Array &&a) {
          return   (a[0] > 0 && a[0] < 1e8
		&& a[1] > 0 && a[1] < 6
		&& a[2] > 0 && a[2] < 3
		&& a[3] > 0 && a[3] < 1e5
		&& a[4] > 0 && a[4] < 100
		&& a[5] > 0 && a[5] < 1e8); // The only constraint are that rho_g,k,rho_th are positive
        }

        template <typename BiasParameters>
        static inline void setup_default(BiasParameters &params) {
          params[0] = 1;
          params[1] = 1.;
          params[2] = 1e-8;
          params[3] = 0.001;
          params[4] = 1.;
          params[5] = 1.;
        }

        // Nota: fwd_model and final_density arrays cannot be stored in this step. But
        // they can be used.
        template <
            class ForwardModel, typename FinalDensityArray,
            typename BiasParameters, typename MetaSelector = NoSelector>
        inline void prepare(
            ForwardModel &fwd_model, const FinalDensityArray &final_density,
            double const nmean_, const BiasParameters &params,
            bool density_updated, MetaSelector _select = MetaSelector()) {
          // No need for complex preparation. Just copy parameters.
	  nmean = params[0];
          alpha = params[1];
          epsilon = params[2];
          rho_g = params[3];
          k     = params[4];
          rho_th = params[5];
        }

        inline void cleanup() {
          // No need for cleanup
        }

        // This is a helper function to determine what is the pure linear behaviour. This
        // is helpful for setup initial conditions that are acceptable in order to reduce absurd transients.
        inline double get_linear_bias() const { return alpha; }

        static inline double gradient_density_lambda(
            double nmean, double alpha, double epsilon, double rho_g, double k, double rho_th, double v,
            double g) {
          double const x = 1 + 1e-6 + v;
          double const rho = x / rho_g;
          double a = std::pow(x, alpha - 1);
          double b = std::pow(rho, -epsilon);
          double f = std::exp(-b);
          double h0 = std::exp(-k*(x-rho_th));
          double h1 = 1./(1. + h0);

          return (alpha + epsilon * b + h1 * h0 * k * x) * a * f * nmean * h1*g;
        }

        static inline double density_lambda(
            double nmean, double alpha, double epsilon, double rho_g, double k, double rho_th,
            double v) {
          double const x = 1 + 1e-6 + v;
          double rho = x / rho_g;
          double ret = nmean * std::pow(x, alpha) *
                 1./(1. + std::exp(-k*(x-rho_th))) *
                 std::exp(-std::pow(rho, -epsilon));
           return 1e-6 + ret;
        }

        template <typename FinalDensityArray>
        inline auto compute_density(const FinalDensityArray &array) {
          return std::make_tuple(b_va_fused<double>(
              std::bind(
                  density_lambda, nmean, alpha, epsilon, rho_g,k,rho_th,
                  std::placeholders::_1),
              array));
        }

        // This function returns an array-like array. That array
        // depends on the existence of the final density array and the gradient likelihood array.
        // That is the job of the caller to ensure that temporary variables are not cleared
        // before the final use.
        // The return type is quite complex. Let the compiler decides.
        template <
            typename FinalDensityArray, typename TupleGradientLikelihoodArray>
        inline auto apply_adjoint_gradient(
            const FinalDensityArray &array,
            TupleGradientLikelihoodArray grad_array) {
          return std::make_tuple(b_va_fused<double>(
              std::bind(
                  gradient_density_lambda, nmean, alpha, epsilon,rho_g,k,rho_th,
                  std::placeholders::_1, std::placeholders::_2),
              array, std::move(std::get<0>(grad_array))));
        }
      };

    } // namespace detail

    using detail::BrokenPowerLawSigmoid;

  } // namespace bias

} // namespace LibLSS

#endif
