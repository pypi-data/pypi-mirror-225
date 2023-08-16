/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/adapt_classic_to_nb.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_ADAPT_CLASSIC_TO_NB_HPP
#define __LIBLSS_ADAPT_CLASSIC_TO_NB_HPP

#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/physics/bias/base.hpp"

// This class extends a classic bias function to support negative binomial. It does so by adding
// a parameter and repackaging the tuples
#include <cxxabi.h>

namespace LibLSS {

  template <typename T>
  struct AdaptBias_NB {
    static const auto numParams = 1 + T::numParams;
    static constexpr const bool NmeanIsBias = T::NmeanIsBias;

    T classic;
    double r;

    selection::SimpleAdaptor selection_adaptor;

    AdaptBias_NB(LikelihoodInfo const& info = LikelihoodInfo()) : classic(info) {}

    template <typename BiasParameters>
    static inline void setup_default(BiasParameters &params) {
      T::setup_default(params);
      params[T::numParams] = 0.1; //0.002;
    }

    // This adapt to copy the adequate NB bias parameter before going further down
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
          std::move(std::get<0>(classic.compute_density(array))),
          b_va_fused<double, 3>(
              FuseWrapper_detail::constantFunctor<double>(r)));
    }

    template <typename FinalDensityArray, typename TupleGradientLikelihoodArray>
    inline auto apply_adjoint_gradient(
        const FinalDensityArray &array, TupleGradientLikelihoodArray grad_array)
        -> decltype(classic.apply_adjoint_gradient(
            array, std::make_tuple(std::move(std::get<0>(grad_array))))) {
      BOOST_STATIC_ASSERT(
          (std::tuple_size<TupleGradientLikelihoodArray>::value == 1));
      return classic.apply_adjoint_gradient(
          array, std::make_tuple(std::move(std::get<0>(grad_array))));
    }
  };
} // namespace LibLSS

#endif
