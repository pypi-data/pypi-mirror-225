/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/bias/base.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_GENERIC_BIAS_BASE_HPP
#define __LIBLSS_GENERIC_BIAS_BASE_HPP

#include <functional>
#include <tuple>
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/phoenix_vars.hpp"
#include <boost/phoenix/operator.hpp>
#include <boost/phoenix/stl/cmath.hpp>
#include "libLSS/tools/tuple_helper.hpp"
#include "libLSS/tools/phoenix_vars.hpp"
#include "libLSS/tools/array_concepts.hpp"
#include "libLSS/physics/likelihoods/base.hpp"
#include <CosmoTool/hdf5_array.hpp>

namespace LibLSS {

  struct NoSelector {};
  class MarkovState;

  namespace bias {
    namespace optional_feature_details {
      MEMBER_FUNC_CHECKER(
          has_log_prior_params, log_prior_params, ((double *)0));
      MEMBER_FUNC_CHECKER(has_dump_fields, dump_fields, ((void *)0));

      template <typename Bias, typename BiasParameters>
      typename std::enable_if<
          has_log_prior_params<Bias, double>::value, double>::type
      bias_get_log_prior(Bias const &b, BiasParameters const &params) {
        return b.log_prior_params(params);
      }

      template <typename Bias, typename BiasParameters>
      typename std::enable_if<
          !has_log_prior_params<Bias, double>::value, double>::type
      bias_get_log_prior(Bias const &b, BiasParameters const &params) {
        return 0;
      }

      template <typename Bias>
      typename std::enable_if<has_dump_fields<Bias, void>::value, void>::type
      bias_dump_fields(Bias const &b, MarkovState &state) {
        return b.dump_fields(state);
      }

      template <typename Bias>
      typename std::enable_if<!has_dump_fields<Bias, void>::value, void>::type
      bias_dump_fields(Bias const &b, MarkovState &state) {}
    } // namespace optional_feature_details

    using optional_feature_details::bias_dump_fields;
    using optional_feature_details::bias_get_log_prior;
  } // namespace bias

  namespace selection {

    struct SimpleAdaptor {
      template <typename SelectArray, typename BiasedArray>
      inline auto apply(SelectArray &&select, BiasedArray const &bias)
          -> decltype(std::tuple_cat(
              std::make_tuple(b_va_fused<double>(
                  _p1 * _p2, std::forward<SelectArray>(select),
                  std::move(std::get<0>(bias)))),
              last_of_tuple<1>(bias))) {
        return std::tuple_cat(
            std::make_tuple(b_va_fused<double>(
                _p1 * _p2, std::forward<SelectArray>(select),
                std::move(std::get<0>(bias)))),
            last_of_tuple<1>(bias));
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

  } // namespace selection

} // namespace LibLSS

#endif
