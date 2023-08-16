/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/bias/double_power_law.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHYSICS_DOUBLE_POWER_LAW_BIAS_HPP
#define __LIBLSS_PHYSICS_DOUBLE_POWER_LAW_BIAS_HPP

#include <cmath>
#include <boost/bind.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/physics/bias/base.hpp"
#include <boost/tuple/tuple.hpp>

namespace LibLSS {

  namespace bias {

    namespace detail {

      struct DoubleBrokenPowerLaw {
        static constexpr const int numParams = 3;
        static constexpr const bool NmeanIsBias = false;

        // We implement Mo & White Equation 15.38 (page 687)
        double L0, beta, gamma;
        double nmean;

        selection::SimpleAdaptor selection_adaptor;

        DoubleBrokenPowerLaw(LikelihoodInfo const& = LikelihoodInfo()) {}

        template <typename Array>
        static inline bool check_bias_constraints(Array &&a) {
          Console::instance().print<LOG_DEBUG>(
              boost::format("Attempting biases: %g, %g, %g, %g") % a[0] % a[1] %
              a[2] % a[3]);
          return a[0] > 0 && a[0] < 5000 && a[1] > 0 && a[1] < 3 && a[2] > 0 &&
                 a[2] < 3; // The only constraint is that rho_L is positive
        }

        template <typename BiasParameters>
        static inline void setup_default(BiasParameters &params) {
          params[0] = 10;
          params[1] = 1.5;
          params[2] = 0.75;
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
          L0 = params[0];
          beta = params[1];
          gamma = params[2];
          nmean = nmean_;
        }

        inline void cleanup() {
          // No need for cleanup
        }

        // This is a helper function to determine what is the pure linear behaviour. This
        // is helpful for setup initial conditions that are acceptable in order to reduce absurd transients.
        inline double get_linear_bias() const { return beta; }

        static constexpr double EPSILON_VOIDS = 1e-6;

        static inline double gradient_density_lambda(
            double nmean, double L0, double beta, double gamma, double v,
            double g) {
          double rho = 1 + EPSILON_VOIDS + v;
          double x = rho / L0;
          double A = std::pow(x, beta - 1);
          double B = std::pow(x, beta - gamma - 1);
          double C = 1 + x * B;

          return nmean * (beta * C - (beta - gamma) * B * x) * A /
                 (C * C * L0) * g;
        }

        static inline double density_lambda(
            double nmean, double L0, double beta, double gamma, double v) {
          double rho = 1 + EPSILON_VOIDS + v;
          double x = rho / L0;
          return nmean * std::pow(x, beta) / (1 + std::pow(x, beta - gamma));
        }

        template <typename FinalDensityArray>
        inline auto compute_density(const FinalDensityArray &array)
            -> decltype(std::make_tuple(b_va_fused<double>(
                boost::bind(
                    density_lambda, nmean, L0, beta, gamma,
                    boost::placeholders::_1),
                array))) {
          return std::make_tuple(b_va_fused<double>(
              boost::bind(
                  density_lambda, nmean, L0, beta, gamma,
                  boost::placeholders::_1),
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
            TupleGradientLikelihoodArray grad_array)
            -> decltype(std::make_tuple(b_va_fused<double>(
                boost::bind(
                    gradient_density_lambda, nmean, L0, beta, gamma,
                    boost::placeholders::_1, boost::placeholders::_2),
                array, std::move(std::get<0>(grad_array))))) {
          return std::make_tuple(b_va_fused<double>(
              boost::bind(
                  gradient_density_lambda, nmean, L0, beta, gamma,
                  boost::placeholders::_1, boost::placeholders::_2),
              array, std::move(std::get<0>(grad_array))));
        }
      };

    } // namespace detail

    using detail::DoubleBrokenPowerLaw;

  } // namespace bias

} // namespace LibLSS

#endif
