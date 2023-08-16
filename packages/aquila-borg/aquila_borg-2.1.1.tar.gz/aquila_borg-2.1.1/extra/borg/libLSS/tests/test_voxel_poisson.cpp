/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_voxel_poisson.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include <boost/multi_array.hpp>
#include <boost/tuple/tuple.hpp>
#define BOOST_TEST_MODULE voxel_poisson
#include <boost/test/included/unit_test.hpp>
#include <boost/test/data/test_case.hpp>

#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_reduce.hpp"
#include "libLSS/physics/likelihoods/voxel_poisson.hpp"

using boost::extents;
using LibLSS::b_fused;
using LibLSS::b_fused_idx;
typedef LibLSS::VoxelPoissonLikelihood Likelihood;

namespace utf = boost::unit_test;

boost::multi_array<double, 2> data(extents[4][8]);
boost::multi_array<double, 2> lambda(extents[4][8]);

auto const_lambda = [](int i, int j) -> double { return 2; };
auto vmodel = b_fused_idx<double, 2>(const_lambda);
auto mask = b_fused_idx<bool, 2>([](int, int) -> bool { return true; });
auto data_gen =
    b_fused_idx<double, 2>([](int i, int j) -> double { return 1; });

BOOST_AUTO_TEST_CASE(likelihood_init) {
  LibLSS::copy_array(lambda, vmodel);
  LibLSS::copy_array(data, data_gen);
}

BOOST_AUTO_TEST_CASE(likelihood1, *utf::depends_on("likelihood_init")) {
  double L = Likelihood::log_probability(data, std::make_tuple(lambda), mask);
  double ref_L = 32 * (-2 + std::log(2.));

  BOOST_CHECK_CLOSE(L, ref_L, 1e-6);
}

BOOST_AUTO_TEST_CASE(likelihood2, *utf::depends_on("likelihood_init")) {
  double L = Likelihood::log_probability(
      data, std::make_tuple(std::cref(vmodel)), mask);
  double ref_L = 32 * (-2 + std::log(2.));

  BOOST_CHECK_CLOSE(L, ref_L, 1e-6);
}

BOOST_AUTO_TEST_CASE(likelihood_diff, *utf::depends_on("likelihood_init")) {
  double ref_gradient = -1 + 1.0 / 2.;
  auto dlog = Likelihood::diff_log_probability(
      data, std::make_tuple(std::cref(vmodel)), mask);

  for (int i = 0; i < 4; i++)
    for (int j = 0; j < 8; j++) {
      double value = std::get<0>(dlog)[i][j];
      BOOST_CHECK_CLOSE(value, ref_gradient, 1e-6);
    }
}
