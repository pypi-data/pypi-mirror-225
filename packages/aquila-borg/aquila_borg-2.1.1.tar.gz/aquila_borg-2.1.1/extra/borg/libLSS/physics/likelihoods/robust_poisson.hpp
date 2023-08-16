/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/likelihoods/robust_poisson.hpp
    Copyright (C) 2018 Natalia Porqueres <natalia_porqueres@hotmail.com>
    Copyright (C) 2018 Doogesh Kodi Ramanah <ramanah@iap.fr>
    Copyright (C) 2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2018 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_ROBUST_POISSON_HPP
#  define __LIBLSS_ROBUST_POISSON_HPP

#  include <boost/static_assert.hpp>
#  include <boost/bind.hpp>
#  include <boost/bind/placeholders.hpp>
#  include "libLSS/physics/likelihoods/base.hpp"
#  include "libLSS/tools/fused_array.hpp"
#  include "libLSS/tools/fused_reduce.hpp"
#  include "libLSS/physics/likelihoods/robust_poisson.hpp"
#  include "libLSS/tools/mpi/ghost_planes.hpp"
#  include <boost/phoenix/core.hpp>
#  include <boost/phoenix/operator.hpp>
#  include <tuple>
#  include <cmath>
#  include "libLSS/tools/mpi/ghost_array.hpp"

// This is the voxel poisson generic likelihood. It allows for capturing a N-d array and
// compress it to likelihood scalar or evaluate the gradient.
// It relies on the fused_array concept, the virtual arrays are
// fully supported.

namespace LibLSS {

  class RobustPoissonLikelihood {
  public:
    typedef std::tuple<double, double, uint32_t> ColorTuple;

  private:
    static const bool ROBUST_OLD_NON_PARALLEL = false;
    typedef boost::multi_array<double, 3> GradientArray;
    typedef UninitializedArray<GradientArray> U_GradientArray;

    GhostPlanes<double, 2> ghosts;
    GhostArray<int32_t> ghost_colors;
    MPI_Communication *comm;
    std::shared_ptr<boost::multi_array_ref<long, 3>> color_map;
    size_t N0, N1, N2, N_colors, startN0, endN0;

    std::unique_ptr<U_GradientArray> out_gradient_p;
    void setup(LikelihoodInfo const &info);

    typedef U_Array<ColorTuple, 1> U_ArrayLambdaInfo;
    typedef U_ArrayLambdaInfo::array_type ArrayLambdaInfo;

    typedef boost::array<ssize_t, 3> Index3d;
    typedef std::tuple<Index3d, int32_t> FlatArray;
    std::shared_ptr<LibLSS::U_Array<FlatArray, 1>> color_flat;
    std::shared_ptr<LibLSS::U_Array<size_t, 1>> key_shift;
    size_t Nkeys;

    static const int ROOT_RANK = 0;

  public:
    RobustPoissonLikelihood(LikelihoodInfo const &info) {
      ConsoleContext<LOG_DEBUG> ctx(
          "RobustPoissonLikelihood::RobustPoissonLikelihood");
      ctx.print("Grabbing MPI");
      comm = Likelihood::getMPI(info);
      ctx.print("Grabbing colormap");
      setup(info);
    }

    static const size_t numberLikelihoodParams = 1;

    template <typename RandomGen>
    static inline double gen_poisson_sample(RandomGen &rgen, double lambda) {
#  ifndef NDEBUG
      if (lambda > std::numeric_limits<int>::max())
        MPI_Communication::instance()->abort();
#  endif
      return rgen.poisson(lambda);
    }

    template <typename RandomGen, typename TupleLike>
    static auto sample(RandomGen &rgen, TupleLike tuple_data) {
      static_assert(
          std::tuple_size<TupleLike>::value == numberLikelihoodParams,
          "the data tuple must have the same number elements as the number of "
          "likelihood parameters");

      return b_va_fused<double>(
          std::bind(
              gen_poisson_sample<RandomGen>, std::ref(rgen),
              std::placeholders::_1),
          std::move(std::get<0>(tuple_data)));
    }

    template <typename DataArray, typename LambdaArray, typename MaskArray>
    void compute_lambdas(
        ArrayLambdaInfo &sum_lambda_info, DataArray &&data,
        LambdaArray &&intensity, MaskArray &&mask) {
      ConsoleContext<LOG_DEBUG> ctx("RobustLikelihood::compute_lambdas");
      Console::instance().c_assert(
          startN0 >= data.index_bases()[0],
          "Bad input data, startN0=%d, data.index_bases()[0]=%d", startN0,
          data.index_bases()[0]);
      Console::instance().c_assert(
          endN0 <= data.index_bases()[0] + data.shape()[0],
          "Bad input data, endN0=%d,  data.index_bases()[0] + "
          "data.shape()[0]=%d",
          endN0, data.index_bases()[0] + data.shape()[0]);
      auto &c_map = *color_map;
      auto &cflat = color_flat->get_array();
      auto getColor = [&](size_t k) { return std::get<1>(cflat[k]); };
      auto const &ckey = key_shift->get_array();
      auto get_lambda = [&](int32_t color) -> double & {
        return std::get<0>(sum_lambda_info[color]);
      };
      auto get_Nobs = [&](int32_t color) -> double & {
        return std::get<1>(sum_lambda_info[color]);
      };
      auto get_count = [&](int32_t color) -> uint32_t & {
        return std::get<2>(sum_lambda_info[color]);
      };

#  pragma omp parallel for
      for (size_t i = 0; i < Nkeys; i++) {
        int32_t color = getColor(ckey[i]);
        sum_lambda_info[color] = std::make_tuple(0., 0., 0);
      }

      if (ROBUST_OLD_NON_PARALLEL) {
        for (size_t n0 = startN0; n0 < endN0; n0++) {
          for (size_t n1 = 0; n1 < N1; n1++) {
            for (size_t n2 = 0; n2 < N2; n2++) {
              if (!mask[n0][n1][n2])
                continue;

              long color = c_map[n0][n1][n2];
              double &loc_sum_lambda = get_lambda(color);
              double &loc_sum_Nobs = get_Nobs(color);
              double lambda = intensity[n0][n1][n2];
              loc_sum_lambda += lambda;
              loc_sum_Nobs += data[n0][n1][n2];
              get_count(color)++;
            }
          }
        }
      } else {

#  pragma omp parallel
        {
#  pragma omp for
          for (size_t key = 0; key < Nkeys; key++) {
            int32_t color = std::get<1>(cflat[ckey[key]]);
            get_count(color) = ckey[key + 1] - ckey[key];
          }
          size_t keyStart =
              (ckey[Nkeys] * smp_get_thread_id()) / smp_get_num_threads();
          size_t keyEnd =
              (ckey[Nkeys] * (1 + smp_get_thread_id())) / smp_get_num_threads();

          if (keyStart < keyEnd) {
            int32_t lastColor = getColor(keyEnd - 1);
            // Try to ensure firstColor is none of the existing ones in that slice if we are first.
            int32_t firstColor = keyStart > 0 ? getColor(keyStart - 1)
                                              : (getColor(keyStart) - 1);
            double accumLambdaLastColor = 0, accumNobsLastColor = 0;
            double accumLambdaFirstColor = 0, accumNobsFirstColor = 0;

            for (size_t i = keyStart; i < keyEnd; i++) {
              boost::array<ssize_t, 3> n;
              int32_t color;

              std::tie(n, color) = cflat[i];
              if (!mask(n))
                continue;

              double const I = intensity(n);
              double const D = data(n);

              if (color == firstColor) {
                accumLambdaFirstColor += I;
                accumNobsFirstColor += D;
              } else if (color == lastColor) {
                accumLambdaLastColor += I;
                accumNobsLastColor += D;
              } else {
                get_lambda(color) += I;
                get_Nobs(color) += D;
              }
            }
            // Now handle thread edge effects
            if (firstColor >= sum_lambda_info.index_bases()[0]) {
#  pragma omp critical
              {
                get_lambda(firstColor) += accumLambdaFirstColor;
                get_Nobs(firstColor) += accumNobsFirstColor;
              }
            }
            {
#  pragma omp critical
              {
                get_lambda(lastColor) += accumLambdaLastColor;
                get_Nobs(lastColor) += accumNobsLastColor;
              }
            }
          }
        }
      }

      auto identity_mapper = [](auto i) { return i; };
      {
        ConsoleContext<LOG_DEBUG> ctx(
            "RobustLikelihood::synchronize ghost colors");
        ghost_colors.synchronize(
            sum_lambda_info, identity_mapper, [](auto &x, auto const &y) {
              std::get<0>(x) += std::get<0>(y);
              std::get<1>(x) += std::get<1>(y);
              std::get<2>(x) += std::get<2>(y);
            });
      }
    }

    // Compute the log probability, convention is that this function
    // accepts a tuple, the first element being the data and the second
    // the poisson intensity. Other elements are discarded.
    template <typename DataArray, typename TupleLike, typename MaskArray>
    double log_probability(
        const DataArray &data, TupleLike tuple_data, MaskArray &&mask) {
      ConsoleContext<LOG_DEBUG> ctx("RobustPoissonLikelihood::log_probability");
      static_assert(
          std::tuple_size<TupleLike>::value == numberLikelihoodParams,
          "the data tuple must have the same number elements as the number of "
          "likelihood parameters");
      static_assert(DataArray::dimensionality == 3, "Only 3d array supported");
      using boost::phoenix::arg_names::arg1;

      const auto &bare_intensity = std::get<0>(tuple_data);
      auto intensity = b_va_fused<double>(arg1 + 1e-5, bare_intensity);
      auto &c_map = *color_map;

      auto e_Nc = boost::extents[N_colors];
      U_ArrayLambdaInfo u_sum_lambda_info(e_Nc);
      auto &sum_lambda_info = u_sum_lambda_info.get_array();
      ssize_t startN0 = data.index_bases()[0];
      ssize_t endN0 = startN0 + data.shape()[0];

      compute_lambdas(
          sum_lambda_info, data, intensity, std::forward<MaskArray>(mask));

      double log_L = 0;
#  pragma omp parallel for collapse(3) reduction(+ : log_L)
      for (size_t n0 = startN0; n0 < endN0; n0++) {
        for (size_t n1 = 0; n1 < N1; n1++) {
          for (size_t n2 = 0; n2 < N2; n2++) {
            if (!mask[n0][n1][n2])
              continue;

            int32_t color = c_map[n0][n1][n2];
            double lambda = intensity[n0][n1][n2];
            double Nobs = data[n0][n1][n2];
            double previous_log_L = log_L;
            log_L +=
                Nobs * std::log(lambda / std::get<0>(sum_lambda_info[color]));
            Console::instance().c_assert(
                std::get<0>(sum_lambda_info[color]) > 0, "sum_lambda not > 0");
            Console::instance().c_assert(
                !std::isnan(log_L), "NaN in hamiltonian");
          }
        }
      }
      return log_L;
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
    auto diff_log_probability(
        const DataArray &data, TupleLike tuple_data, MaskArray &&mask)
        -> decltype(std::make_tuple(out_gradient_p->get_array())) {
      ConsoleContext<LOG_DEBUG> ctx(
          "RobustPoissonLikelihood::diff_log_probability");
      static_assert(
          std::tuple_size<TupleLike>::value == numberLikelihoodParams,
          "the data tuple must have the same number elements as the number of "
          "likelihood parameters");
      using boost::phoenix::arg_names::arg1;

      static_assert(DataArray::dimensionality == 3, "Only 3d array supported");

      const auto &bare_intensity = std::get<0>(tuple_data);
      auto intensity = b_va_fused<double>(arg1 + 1e-5, bare_intensity);
      auto &out_gradient = out_gradient_p->get_array();

      auto e_Nc = boost::extents[N_colors];
      U_ArrayLambdaInfo u_sum_lambda_info(e_Nc);
      auto &sum_lambda_info = u_sum_lambda_info.get_array();
      ssize_t startN0 = data.index_bases()[0];
      ssize_t endN0 = startN0 + data.shape()[0];
      auto &c_map = *color_map;

      compute_lambdas(
          sum_lambda_info, data, intensity, std::forward<MaskArray>(mask));

#  pragma omp parallel for collapse(3)
      for (size_t n0 = startN0; n0 < endN0; n0++) {
        for (size_t n1 = 0; n1 < N1; n1++) {
          for (size_t n2 = 0; n2 < N2; n2++) {
            if (!mask[n0][n1][n2]) {
              out_gradient[n0][n1][n2] = 0;
              continue;
            }

            int32_t color = c_map[n0][n1][n2];
            double loc_sum_lambda = std::get<0>(sum_lambda_info[color]);
            double loc_sum_Nobs = std::get<1>(sum_lambda_info[color]);
            double Nobs = data[n0][n1][n2];
            double lambda = intensity[n0][n1][n2];

            out_gradient[n0][n1][n2] =
                Nobs / lambda - loc_sum_Nobs / loc_sum_lambda;
          }
        }
      }

      return std::make_tuple(std::cref(out_gradient_p->get_array()));
    }
  };

  MPI_FORCE_COMPOUND_TYPE(RobustPoissonLikelihood::ColorTuple);

} // namespace LibLSS

#endif

// ARES TAG: authors_num = 4
// ARES TAG: name(0) = Natalia Porqueres
// ARES TAG: name(1) = Doogesh Kodi Ramanah
// ARES TAG: name(2) = Guilhem Lavaux
// ARES TAG: name(3) = Jens Jasche
// ARES TAG: email(0) = natalia_porqueres@hotmail.com
// ARES TAG: email(1) = ramanah@iap.fr
// ARES TAG: email(2) = guilhem.lavaux@iap.fr
// ARES TAG: email(3) = jens.jasche@fysik.su.se
// ARES TAG: year(0) = 2018
// ARES TAG: year(1) = 2018
// ARES TAG: year(2) = 2018
// ARES TAG: year(3) = 2018
