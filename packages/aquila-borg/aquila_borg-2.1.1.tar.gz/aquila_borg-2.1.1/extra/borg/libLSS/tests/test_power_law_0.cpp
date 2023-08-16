/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_power_law_0.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include <boost/format.hpp>
#include <boost/multi_array.hpp>
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_assign.hpp"
#include "libLSS/tools/static_init.hpp"

using boost::extents;
using boost::format;
using LibLSS::bias::PowerLaw;

int main(int argc, char **argv) {
  LibLSS::QUIET_CONSOLE_START = true;
  LibLSS::setupMPI(argc, argv);
  LibLSS::StaticInit::execute();
  struct Model {
  } model;
  auto d_extents = extents[32][32][32];
  boost::array<double, 2> params{1, 2.0};
  boost::multi_array<double, 3> final_density(d_extents);
  PowerLaw law;
  static constexpr auto EPSILON_VOIDS = PowerLaw::EPSILON_VOIDS;

  law.prepare(model, final_density, 1, params, true);

  // Variant using phoenix lambda capabilities
  LibLSS::copy_array(
      final_density, LibLSS::b_fused_idx<double, 3>(
                         [](size_t i, size_t j, size_t k) -> size_t {
                           return ((1 + i) * (1 + j) * (1 + k));
                         }));

  // Derive the galaxy density
  auto density_g = std::get<0>(law.compute_density(final_density));

  std::cout << density_g.shape()[0] << "x" << density_g.shape()[1] << "x"
            << density_g.shape()[2] << std::endl;
  for (size_t i = 0; i < density_g.shape()[0]; i++) {
    for (size_t j = 0; j < density_g.shape()[1]; j++) {
      for (size_t k = 0; k < density_g.shape()[2]; k++) {
        double ref = std::pow(final_density[i][j][k] + 1 + EPSILON_VOIDS, 2.0);
        double out = density_g[i][j][k];
        if (std::abs(out - ref) > 1e-10) {
          std::cout << format("Error at (%d,%d,%d), ref = %.10f, out = %.10f") %
                           i % j % k % ref % out;
          return 1;
        }
      }
    }
  }
  law.cleanup();

  LibLSS::StaticInit::finalize();

  LibLSS::doneMPI();

  return 0;
}
