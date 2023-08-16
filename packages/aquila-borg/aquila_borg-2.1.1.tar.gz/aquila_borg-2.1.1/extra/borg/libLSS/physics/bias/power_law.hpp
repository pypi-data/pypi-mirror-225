/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/bias/power_law.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHYSICS_POWER_LAW_BIAS_HPP
#define __LIBLSS_PHYSICS_POWER_LAW_BIAS_HPP

// This header provides the implementations of a simple power law bias model.
// A generic bias model must implement the following concept:
//     a "selection_adaptor" functor, available from the object
//     a "compute_density(final_density)" function accepting a virtual array and returning a tuple of virtual array.
//     a "apply_adjoint_gradient(final_density,gradient_likelihood_array)" also accepting virtual arrays and returning a virtual array
//     a "prepare" function which is called before the other two calls, to allow for precomputing auxiliary complex fields.
//     a "cleanup" which allows for tearing down any auxiliary fields and memory allocated in the prepare phase.

#include <cmath>
#include <boost/bind.hpp>
#include "libLSS/tools/fused_array.hpp"
#include <tuple>
#include "libLSS/tools/phoenix_vars.hpp"
#include <boost/phoenix/operator.hpp>
#include <boost/phoenix/stl/cmath.hpp>
#include "libLSS/tools/tuple_helper.hpp"
#include "libLSS/physics/bias/base.hpp"

namespace LibLSS {

  namespace bias {

    namespace detail {

      inline double dummy_lambda(double) { return 0; }

      struct PowerLaw {
        static constexpr double EPSILON_VOIDS = 1e-6;
        static constexpr int numParams = 2;
        static constexpr const bool NmeanIsBias = true;

        double alpha;
        double nmean;

        // This adaptor transforms an unselected galaxy density (with appropriate
        // auxiliary arrays) to a selected array. It must be a functor accepting two
        // parameters: a selection virtual array and a bias density virtual array.
        selection::SimpleAdaptor selection_adaptor;

        PowerLaw(LikelihoodInfo const& = LikelihoodInfo()) {}

        template <typename BiasParameters>
        static inline void setup_default(BiasParameters &params) {
          params[0] = 10;
          params[1] = 0.2;
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
          // No need for complex preparation. Just copy parameters.
          nmean = params[0];
          alpha = params[1];
        }

        inline void cleanup() {
          // No need for cleanup
        }

        static inline double gradient_density_lambda(
            double nmean, double alpha, double v, double g) {
          return alpha * nmean * std::pow(1 + v + EPSILON_VOIDS, alpha - 1) * g;
        }

        static inline double
        density_lambda(double nmean, double alpha, double v) {
          double v0 = nmean * std::pow(1 + EPSILON_VOIDS + v, alpha);
          Console::instance().c_assert(!std::isinf(v0), "V is infinite");
          return v0;
        }

        inline double get_linear_bias() const { return alpha; }

        template <typename Array>
        static inline bool check_bias_constraints(Array &&a) {
          return a[0] > 0 && a[1] > 0 && a[1] < 5; // alpha can take any value
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
              std::bind(
                  density_lambda, nmean, alpha, std::placeholders::_1),
              array));
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
              std::bind(
                  gradient_density_lambda, nmean, alpha,
                  std::placeholders::_1, std::placeholders::_2),
              array, std::move(std::get<0>(grad_array))));
        }
      };

    } // namespace detail

    using detail::PowerLaw;

  } // namespace bias

} // namespace LibLSS

#endif
