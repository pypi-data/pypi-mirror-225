/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/bias/passthrough.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHYSICS_PASSTHROUGH_HPP
#define __LIBLSS_PHYSICS_PASSTHROUGH_HPP

#include <cmath>
#include <tuple>
#include "libLSS/physics/bias/base.hpp"

namespace LibLSS {

  namespace bias {

    namespace detail_passthrough {

      /**
        * Noop bias
        */
      struct Passthrough {

        static constexpr const bool NmeanIsBias = true;
        static const auto numParams = 0;

        // This adaptor transforms an unselected galaxy density (with appropriate
        // auxiliary arrays) to a selected array. It must be a functor accepting two
        // parameters: a selection virtual array and a bias density virtual array.
        selection::SimpleAdaptor selection_adaptor;

        template <typename BiasParameters>
        static inline void setup_default(BiasParameters &params) {}

        Passthrough(LikelihoodInfo const& = LikelihoodInfo()) {}

        // Nota: fwd_model and final_density arrays cannot be stored in this step. But
        // they can be used.
        template <
            class ForwardModel, typename FinalDensityArray,
            typename BiasParameters, typename MetaSelect = NoSelector>
        inline void prepare(
            ForwardModel &fwd_model, const FinalDensityArray &final_density,
            double const _nmean, const BiasParameters &params,
            bool density_updated, MetaSelect _select = MetaSelect()) {}

        inline void cleanup() {
          // No need for cleanup
        }

        inline double get_linear_bias() const { return 1; }

        template <typename Array>
        static inline bool check_bias_constraints(Array &&a) {
          return true;
        }

        template <typename FinalDensityArray>
        inline auto compute_density(const FinalDensityArray &array) {
          return std::make_tuple(std::cref(array));
        }

        template <
            typename FinalDensityArray, typename TupleGradientLikelihoodArray>
        inline auto apply_adjoint_gradient(
            const FinalDensityArray &array,
            TupleGradientLikelihoodArray grad_array) {
          return grad_array;
        }
      };

    } // namespace detail_passthrough

    /// Import the Noop class into LibLSS::bias
    using detail_passthrough::Passthrough;

  } // namespace bias

} // namespace LibLSS

#endif
