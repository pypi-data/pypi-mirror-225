/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/bias/linear_bias.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHYSICS_LINEAR_BIAS_HPP
#define __LIBLSS_PHYSICS_LINEAR_BIAS_HPP

#include <cmath>
#include <functional>
#include "libLSS/tools/fused_array.hpp"
#include <tuple>
#include "libLSS/tools/phoenix_vars.hpp"
#include <boost/phoenix/operator.hpp>
#include <boost/phoenix/stl/cmath.hpp>
#include "libLSS/tools/tuple_helper.hpp"
#include "libLSS/physics/bias/base.hpp"

namespace LibLSS {

  namespace bias {

    namespace detail_linear_bias {
      namespace ph = std::placeholders;

      struct LinearBias {

        static constexpr const bool NmeanIsBias = true;
        static constexpr int numParams = 2;

        // This adaptor transforms an unselected galaxy density (with appropriate
        // auxiliary arrays) to a selected array. It must be a functor accepting two
        // parameters: a selection virtual array and a bias density virtual array.
        selection::SimpleAdaptor selection_adaptor;

        double nmean, bias;

        LinearBias(LikelihoodInfo const& = LikelihoodInfo()) {}

        template <typename BiasParameters>
        static inline void setup_default(BiasParameters &params) {
          params[0] = 1;
          params[1] = 1;
        }

        // Nota: fwd_model and final_density arrays cannot be stored in this step. But
        // they can be used.
        template <
            class ForwardModel, typename FinalDensityArray,
            typename BiasParameters, typename MetaSelect = NoSelector>
        inline void prepare(
            ForwardModel &fwd_model, const FinalDensityArray &final_density,
            double const _nmean, const BiasParameters &params,
            bool density_updated, MetaSelect _select = MetaSelect()) {
          nmean = params[0];
          bias = params[1];
        }

        inline void cleanup() {
          // No need for cleanup
        }

        static inline double
        gradient_density_lambda(double nmean, double bias, double g) {
          return nmean * bias * g;
        }

        static inline double
        density_lambda(double nmean, double bias, double v) {
          return nmean * (1 + bias * v);
        }

        inline double get_linear_bias() const { return bias; }

        template <typename Array>
        static inline bool check_bias_constraints(Array &&a) {
          return a[0] > 0 and a[1] > 0;
        }

        // This function returns an array-like array. That array
        // depends on the existence of the final density array.
        // The return type is quite complex. Let the compiler decides.
        // C++11 does not allow automatic return type deduction. C++14 would be
        // needed for that. So we have to rely on an auxiliary function that
        // allow for a compact decltype to be written.
        template <typename FinalDensityArray>
        inline auto compute_density(const FinalDensityArray &array) {
          return std::make_tuple(b_va_fused<double>(
              std::bind(density_lambda, nmean, bias, ph::_1), array));
        }

        // This function returns an array-like array. That array
        // depends on the existence of the final density array and the gradient likelihood array.
        // That is the job of the caller to ensure that temporary variables are not cleared
        // before the final use.
        // The return type is quite complex. Let the compiler decides.
        // L(b_0(delta, p), b_1(delta, p), ..., b_n(delta, p))
        // Now we take a tuple of gradient and collapse this to a gradient of delta.
        template <
            typename FinalDensityArray, typename TupleGradientLikelihoodArray>
        inline auto apply_adjoint_gradient(
            const FinalDensityArray &array,
            TupleGradientLikelihoodArray grad_array) {
          BOOST_STATIC_ASSERT(
              (std::tuple_size<TupleGradientLikelihoodArray>::value == 1));
          return std::make_tuple(b_va_fused<double>(
              std::bind(gradient_density_lambda, nmean, bias, ph::_1),
              std::move(std::get<0>(grad_array))));
        }
      };

    } // namespace detail_linear_bias

    using detail_linear_bias::LinearBias;

  } // namespace bias

} // namespace LibLSS

#endif
