/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/bias/noop.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHYSICS_NOOP_HPP
#define __LIBLSS_PHYSICS_NOOP_HPP

/**
  * This header provides the implementations of a simple power law bias model.
  * A generic bias model must implement the following concept:
  *     a "selection_adaptor" functor, available from the object
  *     a "compute_density(final_density)" function accepting a virtual array and returning a tuple of virtual array.
  *     a "apply_adjoint_gradient(final_density,gradient_likelihood_array)" also accepting virtual arrays and returning a virtual array
  *     a "prepare" function which is called before the other two calls, to allow for precomputing auxiliary complex fields.
  *     a "cleanup" which allows for tearing down any auxiliary fields and memory allocated in the prepare phase.
  */
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

    namespace detail_noop {
      namespace ph = std::placeholders;

      /**
        * Noop bias
        */
      struct Noop {

        static constexpr const bool NmeanIsBias = true;
        static constexpr const int numParams = 1;

        // This adaptor transforms an unselected galaxy density (with appropriate
        // auxiliary arrays) to a selected array. It must be a functor accepting two
        // parameters: a selection virtual array and a bias density virtual array.
        selection::SimpleAdaptor selection_adaptor;

        double nmean;

        Noop(LikelihoodInfo const& = LikelihoodInfo()) {}

        template <typename BiasParameters>
        static inline void setup_default(BiasParameters &params) {}

        // Nota: fwd_model and final_density arrays cannot be stored in this step. But
        // they can be used.
        template <
            class ForwardModel, typename FinalDensityArray,
            typename BiasParameters, typename MetaSelect = NoSelector>
        inline void prepare(
            ForwardModel &fwd_model, const FinalDensityArray &final_density,
            double const _nmean, const BiasParameters &params,
            bool density_updated, MetaSelect _select = MetaSelect()) {
          //nmean = _nmean;
          nmean = params[0];
        }

        inline void cleanup() {
          // No need for cleanup
        }

        static inline double gradient_density_lambda(double nmean, double g) {
          return nmean * g;
        }

        static inline double density_lambda(double nmean, double v) {
          return nmean * (1 + v);
        }

        inline double get_linear_bias() const { return 1; }

        template <typename Array>
        static inline bool check_bias_constraints(Array &&a) {
          return true;
        }

        // The compute density takes a physical matter density field
        // and produce a set of fields that can be consumed by a likelihood.
        // For example if can be a biased density field and the allowed variance
        // per voxel.
        // Formally that generates a vector a_i = f_i({delta})
        //
        // This function returns a tuple of array-like objects. That array
        // depends on the existence of the final density array.
        // The return type is quite complex as it can be an abstract expression
        // and not a real array. Here we let the compiler decides with an auto
        // type.
        template <typename FinalDensityArray>
        inline auto compute_density(const FinalDensityArray &array) {
          return std::make_tuple(b_va_fused<double>(
              std::bind(density_lambda, nmean, ph::_1), array));
        }

        // This function returns a tuple of array-like array. 
        // That array depends on the existence of the final density 
        // array and the gradient likelihood array. That is the job of 
        // the caller to ensure that temporary variables are not cleared
        // before the final use.
        //
        // The return type may be quite complex depending on the detail of the
        // implementation of the gradient. If one decides to use a real
        // array then the return type is just a tuple of arrays. However
        // it is allowed to be also a tuple of expressions acting on arrays.
        // In practice we let the compiler decides here.
        // The "biased fields" are assumed to be a_i = f_i({delta})
        // The adjoint gradient of the density field must be returned as a 1-tuple
        template <
            typename FinalDensityArray, typename TupleGradientLikelihoodArray>
        inline auto apply_adjoint_gradient(
            const FinalDensityArray &array,
            TupleGradientLikelihoodArray grad_array) {
          BOOST_STATIC_ASSERT(
              (std::tuple_size<TupleGradientLikelihoodArray>::value == 1));
          return std::make_tuple(b_va_fused<double>(
              std::bind(gradient_density_lambda, nmean, ph::_1),
              std::move(std::get<0>(grad_array))));
        }

        /**
          * This function computes the adjoint gradient  
          * of the bias coefficient i. The adjoint gradient is provided with
          * the same information as for apply_adjoint_gradient.
          * It is expected to return an array-like object.
          */
        template <
            typename FinalDensityArray, typename TupleGradientLikelihoodArray>
        inline auto apply_adjoint_gradient_bias(const FinalDensityArray& array, TupleGradientLikelihoodArray grad_array, unsigned int i) {
          Console::instance().c_assert(i < 1, "Invalid range of bias parameter");
          boost::multi_array<double, 1> output_grad(boost::extents[1]);
          output_grad[0] = ((1.0 + fwrap(array)) * fwrap(std::get<0>(grad_array))).sum();
          return output_grad;
        }
      };

    } // namespace detail_noop

    /// Import the Noop class into LibLSS::bias
    using detail_noop::Noop;

  } // namespace bias

} // namespace LibLSS

#endif
