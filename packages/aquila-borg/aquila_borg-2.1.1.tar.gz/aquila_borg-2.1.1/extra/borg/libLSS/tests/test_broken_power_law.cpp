/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_broken_power_law.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#define BOOST_TEST_MODULE broken_power_law
#define BOOST_TEST_NO_MAIN
#define BOOST_TEST_ALTERNATIVE_INIT_API
#include <boost/test/included/unit_test.hpp>
#include <boost/test/data/test_case.hpp>

#include <iostream>
#include <boost/format.hpp>
#include <boost/multi_array.hpp>
#include "libLSS/physics/bias/broken_power_law.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_assign.hpp"
#include "libLSS/tools/static_init.hpp"


namespace utf = boost::unit_test;
using boost::extents;
using boost::format;
using LibLSS::bias::BrokenPowerLaw;

struct Model {
} model;
size_t N = 8;
auto d_extents = extents[N][N][N];
double nmean = 1.0;
boost::array<double, 4> params{1, 2.0, 1.0, 1.0};
boost::multi_array<double, 3> final_density(d_extents);
boost::multi_array<double, 3> grad_density(d_extents);
BrokenPowerLaw law;

static constexpr auto EPSILON_VOIDS = 0; //BrokenPowerLaw::EPSILON_VOIDS;

BOOST_AUTO_TEST_CASE(warmup) {
  law.prepare(model, final_density, nmean, params, true);

  LibLSS::copy_array(
      final_density,
      LibLSS::b_fused_idx<double, 3>([](int i, int j, int k) -> double {
        return (i + 1) * (j + 1) * (k + 1);
      }));

  LibLSS::copy_array(
      grad_density, LibLSS::b_fused_idx<double, 3>(
                        [](int i, int j, int k) -> double { return 1; }));
}

BOOST_AUTO_TEST_CASE(shape_test, *utf::depends_on("warmup")) {
  auto density_g = std::get<0>(law.compute_density(final_density));

  BOOST_CHECK(density_g.shape()[0] == N);
  BOOST_CHECK(density_g.shape()[1] == N);
  BOOST_CHECK(density_g.shape()[2] == N);
}

BOOST_AUTO_TEST_CASE(gradient, *utf::depends_on("warmup")) {
  auto density_g = std::get<0>(law.compute_density(final_density));

  auto grad_density_g = std::get<0>(law.apply_adjoint_gradient(
      final_density, std::make_tuple(std::ref(grad_density))));

  double alpha = params[1], epsilon = params[2], rhog = params[3];

  for (size_t i = 0; i < density_g.shape()[0]; i++) {
    for (size_t j = 0; j < density_g.shape()[1]; j++) {
      for (size_t k = 0; k < density_g.shape()[2]; k++) {
        double out = grad_density_g[i][j][k];
        double v = 1 + final_density[i][j][k] + EPSILON_VOIDS;
        double A = nmean * std::pow(v, alpha) *
                   std::exp(-rhog * std::pow(v, -epsilon));
        double ref = A *
                     (alpha / v + epsilon * rhog * std::pow(v, -epsilon - 1)) *
                     grad_density[i][j][k];

        BOOST_CHECK_CLOSE(out, ref, 1e-4);
      }
    }
  }
}

int main(int argc, char **argv)
{
  LibLSS::QUIET_CONSOLE_START = true;
  LibLSS::setupMPI(argc, argv);
  LibLSS::StaticInit::execute();

  int ret = utf::unit_test_main(&init_unit_test, argc, argv);

  LibLSS::StaticInit::finalize();
  LibLSS::doneMPI();

  return ret;
}
