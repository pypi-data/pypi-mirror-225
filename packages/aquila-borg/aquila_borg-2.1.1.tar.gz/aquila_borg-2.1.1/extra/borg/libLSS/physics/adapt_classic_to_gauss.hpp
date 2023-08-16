/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/adapt_classic_to_gauss.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_ADAPT_CLASSIC_TO_GAUSS_HPP
#define __LIBLSS_ADAPT_CLASSIC_TO_GAUSS_HPP

#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/physics/bias/base.hpp"
#include "libLSS/physics/bias/power_law.hpp"

// This class extends a classic bias function to support negative binomial. It does so by adding
// a parameter and repackaging the tuples
#include <cxxabi.h>

namespace LibLSS {

  namespace bias {

    template <typename T>
    inline T copy_if_rref(T const &&x) {
      return x;
    }
    template <typename T>
    inline auto copy_if_rref(T &x) -> decltype(std::ref(x)) {
      return std::ref(x);
    }

    struct NoiseModulatedAdaptor {
      template <typename SelectArray, typename BiasedArray>
      inline auto apply(SelectArray &&select, BiasedArray const &bias)
          -> decltype(std::make_tuple(
              b_va_fused<double>(
                  _p1 * _p2, std::forward<SelectArray>(select),
                  std::move(std::get<0>(bias))),
              b_va_fused<double>(
                  _p1 *_p2, std::forward<SelectArray>(select),
                  std::move(std::get<1>(bias))))) {
        // Take a biased density x noise and multiply both by selection
        return std::make_tuple(
            b_va_fused<double>(
                _p1 * _p2, std::forward<SelectArray>(select),
                std::move(std::get<0>(bias))),
            b_va_fused<double>(
                _p1 * _p2, std::forward<SelectArray>(select),
                std::move(std::get<1>(bias))));
      }

      template <
          typename LikelihoodGradient, typename SelectArray,
          typename BiasedArray>
      inline auto adjoint_gradient(
          LikelihoodGradient ag_like, SelectArray &&select, BiasedArray const &)
          -> decltype(std::tuple_cat(
              std::make_tuple(b_va_fused<double>(
                  _p1 * _p2, std::forward<SelectArray>(select),
                  std::move(std::get<0>(ag_like)))),
              last_of_tuple<1>(ag_like))) {
        // In practice the adjoint gradient operator is the same as simple selection
        return std::tuple_cat(
            std::make_tuple(b_va_fused<double>(
                _p1 * _p2, std::forward<SelectArray>(select),
                std::move(std::get<0>(ag_like)))),
            last_of_tuple<1>(ag_like));
      }
    };
  } // namespace bias

  template <typename T>
  struct AdaptBias_Gauss {
    static const auto numParams = 1 + T::numParams;
    static constexpr const bool NmeanIsBias = T::NmeanIsBias;

    T classic;
    double r;

    bias::NoiseModulatedAdaptor selection_adaptor;
    //        bias::SimpleAdaptor selection_adaptor;
    //
    AdaptBias_Gauss(LikelihoodInfo const& info = LikelihoodInfo()) : classic(info) {}

    template <typename BiasParameters>
    static inline void setup_default(BiasParameters &params) {
      T::setup_default(params);
      params[T::numParams] = 3.; //0.002;
    }

    template <typename BiasParameters>
    inline double log_prior_params(BiasParameters const &params) const {
      return bias::bias_get_log_prior(classic, params);
    }

    // This adapt to copy the adequate Gaussian bias parameter before going further down
    // in the bias model.
    // It does not need to optimize away anything based on selector.
    // Argument:
    //    * fwd_model: current full forward model
    //    * final_density: final matter density obtained by the forward model
    //    * params: current bias parameters
    //    * select: currently sampled bias parameter, it is by default NoSelector. This argument allow to do optimization in the
    //              generation of the bias function (i.e. trim components, or avoid some reevaluation upon further calls).
    template <
        class ForwardModel, typename FinalDensityArray, typename BiasParameters,
        typename MetaSelector = NoSelector>
    inline void prepare(
        ForwardModel &fwd_model, const FinalDensityArray &final_density,
        double const nmean_, const BiasParameters &params, bool density_updated,
        MetaSelector select = MetaSelector()) {
      classic.prepare(
          fwd_model, final_density, nmean_, params, density_updated, select);
      r = params[T::numParams];
    }

    inline void cleanup() { classic.cleanup(); }

    inline double get_linear_bias() const { return classic.get_linear_bias(); }

    template <typename Array>
    inline bool check_bias_constraints(Array &&a) {
      return T::check_bias_constraints(a) && (a[T::numParams] > 0) &&
             (a[T::numParams] < 10000);
    }

    template <typename FinalDensityArray>
    inline auto compute_density(const FinalDensityArray &array)
        -> decltype(std::make_tuple(
            std::move(std::get<0>(classic.compute_density(array))),
            b_va_fused<double, 3>(
                FuseWrapper_detail::constantFunctor<double>(r)))) {
      return std::make_tuple(
          std::move(std::get<0>(classic.compute_density(
              array))), // Grab the biased density from the parent bias function.
          b_va_fused<double, 3>(FuseWrapper_detail::constantFunctor<double>(
              r)) // Add a constant noise array
      );
    }

    template <typename FinalDensityArray, typename TupleGradientLikelihoodArray>
    inline auto apply_adjoint_gradient(
        const FinalDensityArray &array, TupleGradientLikelihoodArray grad_array)
        -> decltype(classic.apply_adjoint_gradient(
            array, std::make_tuple(std::move(std::get<0>(grad_array))))) {
      BOOST_STATIC_ASSERT(
          (std::tuple_size<TupleGradientLikelihoodArray>::value == 1));
      return classic.apply_adjoint_gradient(
          array,
          std::make_tuple(std::move(std::get<0>(
              grad_array)))); // Pass down the first component of the AG to the bias function.
    }
  };
} // namespace LibLSS

#endif
