/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_power_law_1.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#define BOOST_TEST_MODULE power_law_1
#define BOOST_TEST_NO_MAIN
#define BOOST_TEST_ALTERNATIVE_INIT_API

#include <boost/test/included/unit_test.hpp>
#include <boost/test/data/test_case.hpp>

#include <iostream>
#include <boost/format.hpp>
#include <boost/multi_array.hpp>
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_assign.hpp"
#include "libLSS/tools/static_init.hpp"

namespace utf = boost::unit_test;
using boost::extents;
using boost::format;
using LibLSS::bias::PowerLaw;

struct Model {
} model;
size_t N = 32;
auto d_extents = extents[N][N][N];
boost::array<double, 2> params{1, 2.0};
boost::multi_array<double, 3> final_density(d_extents);
boost::multi_array<double, 3> grad_density(d_extents);
PowerLaw law;
static constexpr auto EPSILON_VOIDS = PowerLaw::EPSILON_VOIDS;

BOOST_AUTO_TEST_CASE(warmup) {
  law.prepare(model, final_density, 1, params, true);

  // Variant using phoenix lambda capabilities
  LibLSS::copy_array(
      final_density, LibLSS::b_fused_idx<double, 3>(
                         [](size_t i, size_t j, size_t k) -> size_t {
                           return ((1 + i) * (1 + j) * (1 + k));
                         }));

  // Variant with C++ lambda, could be emulated with phoenix but quite artificial
  LibLSS::copy_array(
      grad_density, LibLSS::b_fused_idx<double, 3>(
                        [](int i, int j, int k) -> double { return 1; }));
}

BOOST_AUTO_TEST_CASE(shape_test, *utf::depends_on("warmup")) {
  // Derive the galaxy density
  auto density_g = std::get<0>(law.compute_density(final_density));

  BOOST_CHECK(density_g.shape()[0] == N);
  BOOST_CHECK(density_g.shape()[1] == N);
  BOOST_CHECK(density_g.shape()[2] == N);
}

BOOST_AUTO_TEST_CASE(gradient, *utf::depends_on("warmup")) {
  // Derive the galaxy density
  auto density_g = std::get<0>(law.compute_density(final_density));
  // Derive the gradient, note that ref is absolutely necessary to avoid a SEGV.
  // Otherwise there would be a temporary copy construction in the tuple which would be used in building
  // grad_density_g virtual array. Of course, once the expression completes the temporary is not anymore available.
  // This is not necessary if it is a virtual array as the entire expression is copying down in that case.
  auto grad_density_g = std::get<0>(law.apply_adjoint_gradient(
      final_density, std::make_tuple(std::ref(grad_density))));

  for (size_t i = 0; i < density_g.shape()[0]; i++) {
    for (size_t j = 0; j < density_g.shape()[1]; j++) {
      for (size_t k = 0; k < density_g.shape()[2]; k++) {
        double out = grad_density_g[i][j][k];
        double ref = 2.0 *
                     std::pow(1 + final_density[i][j][k] + EPSILON_VOIDS, 1.0) *
                     grad_density[i][j][k];

        BOOST_CHECK_CLOSE(out, ref, 1e-6);
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
