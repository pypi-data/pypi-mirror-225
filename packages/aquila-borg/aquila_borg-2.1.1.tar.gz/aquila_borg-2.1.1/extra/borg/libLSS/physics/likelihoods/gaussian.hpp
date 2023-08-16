/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/likelihoods/gaussian.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_GAUSSIAN_LIKELIHOOD_HPP
#define __LIBLSS_GAUSSIAN_LIKELIHOOD_HPP

#include <boost/static_assert.hpp>
#include <boost/bind.hpp>
#include <boost/bind/placeholders.hpp>
#include <gsl/gsl_sf_gamma.h>
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/fused_reduce.hpp"
#include <CosmoTool/algo.hpp>
#include "libLSS/physics/likelihoods/base.hpp"

// This is the negative binomial generic likelihood. It allows for capturing a N-d array and
// compress it to likelihood scalar or evaluate the gradient.
// It relies on the fused_array concept, the virtual arrays are
// fully supported.

namespace LibLSS {

  class GaussianLikelihood {
  public:
    GaussianLikelihood(LikelihoodInfo const & = LikelihoodInfo()) {}

    static const size_t numberLikelihoodParams = 2;

    static inline double log_proba(double d, double rho, double sigma2) {
      return CosmoTool::square(d - rho) / (sigma2);
    }

    static inline double
    diff_log_proba(double d, double rho, double sigma2, bool mask) {
      if (!mask)
        return 0;
      return (d - rho) / (sigma2);
    }

    template <typename RandomGen>
    static inline double
    gen_sample(RandomGen &rgen, double rho, double sigma2) {
      return rgen.gaussian() * std::sqrt(sigma2) + rho;
    }

    template <typename RandomGen, typename TupleLike>
    static auto sample(RandomGen &rgen, TupleLike tuple_data)
        -> decltype(b_va_fused<double>(
            std::bind(
                gen_sample<RandomGen>, std::ref(rgen), std::placeholders::_1,
                std::placeholders::_2),
            std::move(std::get<0>(tuple_data)),
            std::move(std::get<1>(tuple_data)))) {
      BOOST_STATIC_ASSERT(
          (std::tuple_size<TupleLike>::value == numberLikelihoodParams));

      return b_va_fused<double>(
          std::bind(
              gen_sample<RandomGen>, std::ref(rgen), std::placeholders::_1,
              std::placeholders::_2),
          std::move(std::get<0>(tuple_data)),
          std::move(std::get<1>(tuple_data)));
    }

    // Compute the log probability, convention is that this function
    // accepts a tuple, the first element being the data and the second
    // the poisson intensity. Other elements are discarded.
    template <typename DataArray, typename TupleLike, typename MaskArray>
    static double log_probability(
        const DataArray &data, TupleLike tuple_data, MaskArray &&mask) {
      BOOST_STATIC_ASSERT(
          (std::tuple_size<TupleLike>::value == numberLikelihoodParams));

      auto const &intensity = std::get<0>(tuple_data);
      auto const &r = std::get<1>(tuple_data); // Selection * noise array
      double Nmask = 0;

      // Do a sum over voxels not masked.
#if 1
      Nmask = LibLSS::reduce_sum<double>(
          b_va_fused<double>(
              [](double sigma2) -> double { return std::log(sigma2); }, r),
          mask);
#endif

      double chi2 =
          -0.5 * LibLSS::reduce_sum<double>(
                     b_va_fused<double>(log_proba, data, intensity, r), mask);
      double N2 = -0.5 * Nmask;

      Console::instance().print<LOG_DEBUG>(
          boost::format("chi2 = %g, N2 = %g ") % chi2 % N2);

      return chi2 + N2;
    }

    // Compute the gradient of the log probability, convention is that this function
    // accepts a tuple, the first element being the data and the second
    // the poisson intensity. Other elements are discarded.
    // The gradient is written in the output array, which must have the same shape
    // as the input virtual arrays.
    // L(b_0, b_1, ...)
    // param is the i index in b_i.
    // tuple_data must have the adequate tuple size to account for all "b_i".
    template <typename DataArray, typename TupleLike, typename Mask>
    static auto diff_log_probability(
        const DataArray &data, TupleLike tuple_data, const Mask &mask)
        -> decltype(std::make_tuple(b_va_fused<double>(
            diff_log_proba, data, std::move(std::get<0>(tuple_data)),
            std::move(std::get<1>(tuple_data)), mask))) {
      BOOST_STATIC_ASSERT(
          (std::tuple_size<TupleLike>::value == numberLikelihoodParams));

      return std::make_tuple(b_va_fused<double>(
          diff_log_proba, data, std::move(std::get<0>(tuple_data)),
          std::move(std::get<1>(tuple_data)), mask));
    }
  };

} // namespace LibLSS

#endif
