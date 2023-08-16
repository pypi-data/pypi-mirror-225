/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/likelihoods/voxel_poisson.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_VOXEL_POISSON_HPP
#define __LIBLSS_VOXEL_POISSON_HPP

#include <boost/static_assert.hpp>
#include <boost/bind.hpp>
#include <boost/bind/placeholders.hpp>
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_reduce.hpp"
#include "libLSS/physics/likelihoods/base.hpp"

// This is the voxel poisson generic likelihood. It allows for capturing a N-d array and
// compress it to likelihood scalar or evaluate the gradient.
// It relies on the fused_array concept, the virtual arrays are
// fully supported.

namespace LibLSS {

  class VoxelPoissonLikelihood {
  public:
    VoxelPoissonLikelihood(LikelihoodInfo const & = LikelihoodInfo()) {}

    static const size_t numberLikelihoodParams = 1;

    static inline double log_poisson_proba(double d, double lambda) {
      return -lambda +
             d * std::log(lambda); // normalization log(d!) goes away here
      // An optimization would accept to use log(lambda) directly maybe
      // This could be done with expression patching in log_probability
    }

    static inline double diff_log_poisson_proba(double d, double lambda) {
      // Masking is not yet done properly for gradient.
      if (lambda == 0)
        return 0;
      return -1 + d / lambda;
    }

    template <typename RandomGen>
    static inline double gen_poisson_sample(RandomGen &rgen, double lambda) {
      return rgen.poisson(lambda);
    }

    template <typename RandomGen, typename TupleLike>
    static auto sample(RandomGen &rgen, TupleLike tuple_data)
        -> decltype(b_va_fused<double>(
            boost::bind(
                gen_poisson_sample<RandomGen>, boost::ref(rgen),
                boost::placeholders::_1),
            std::move(std::get<0>(tuple_data)))) {
      BOOST_STATIC_ASSERT(
          (std::tuple_size<TupleLike>::value == numberLikelihoodParams));

      return b_va_fused<double>(
          boost::bind(
              gen_poisson_sample<RandomGen>, boost::ref(rgen),
              boost::placeholders::_1),
          std::move(std::get<0>(tuple_data)));
    }

    // Compute the log probability, convention is that this function
    // accepts a tuple, the first element being the data and the second
    // the poisson intensity. Other elements are discarded.
    template <typename DataArray, typename TupleLike, typename MaskArray>
    static double log_probability(
        const DataArray &data, TupleLike tuple_data, MaskArray &&mask) {
      BOOST_STATIC_ASSERT(
          (std::tuple_size<TupleLike>::value == numberLikelihoodParams));

      const auto &intensity = std::get<0>(tuple_data);

      return LibLSS::reduce_sum<double>(
          b_va_fused<double>(log_poisson_proba, data, intensity), mask);
    }

    // Compute the gradient of the log probability, convention is that this function
    // accepts a tuple, the first element being the data and the second
    // the poisson intensity. Other elements are discarded.
    // The gradient is written in the output array, which must have the same shape
    // as the input virtual arrays.
    // L(b_0, b_1, ...)
    // param is the i index in b_i.
    // tuple_data must have the adequate tuple size to account for all "b_i".
    template <typename DataArray, typename TupleLike, typename MaskArray>
    static auto diff_log_probability(
        const DataArray &data, TupleLike tuple_data, const MaskArray &)
        -> decltype(std::make_tuple(b_va_fused<double>(
            diff_log_poisson_proba, data,
            std::move(std::get<0>(tuple_data))))) {
      BOOST_STATIC_ASSERT(
          (std::tuple_size<TupleLike>::value == numberLikelihoodParams));

      return std::make_tuple(b_va_fused<double>(
          diff_log_poisson_proba, data, std::move(std::get<0>(tuple_data))));
    }
  };

} // namespace LibLSS

#endif
