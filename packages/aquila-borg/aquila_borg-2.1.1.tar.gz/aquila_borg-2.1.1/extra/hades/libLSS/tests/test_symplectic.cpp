/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/tests/test_symplectic.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <H5Cpp.h>
#include <boost/multi_array.hpp>
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/symplectic_integrator.hpp"
#include <CosmoTool/algo.hpp>
#include <CosmoTool/hdf5_array.hpp>
#include <boost/preprocessor/cat.hpp>
#include <boost/preprocessor/stringize.hpp>
#include <boost/preprocessor/seq/for_each.hpp>
#include <algorithm>

using namespace LibLSS;
using boost::extents;
using namespace CosmoTool;

void force_func(
    boost::multi_array<double, 1> &x, boost::multi_array<double, 1> &grad) {
  grad[0] = x[0];
}

int main(int argc, char **argv) {
  using namespace SymplecticOption;
  setupMPI(argc, argv);

  LibLSS::Console &console = LibLSS::Console::instance();
  LibLSS::StaticInit::execute();
  SymplecticIntegrators F;
  boost::multi_array<double, 1> mass(extents[1]), position(extents[1]),
      momentum(extents[1]), gradient(extents[1]);
  double epsilon = 0.1;
  double Einit;
  int Ntime = 2 * M_PI / epsilon;
  boost::multi_array<double, 1> E(boost::extents[Ntime]),
      p(boost::extents[Ntime]), m(boost::extents[Ntime]);

#define BUILD_SCHEME(r, data, elem)                                            \
  std::make_pair(elem, BOOST_PP_STRINGIZE(elem)),

  std::pair<IntegratorScheme, std::string> schemes[] = {BOOST_PP_SEQ_FOR_EACH(
      BUILD_SCHEME, _,
      (SI_2A)(SI_2B)(SI_2C)(SI_3A)(SI_4B)(SI_4C)(SI_4D)(SI_6A))};
  int numSchemes = sizeof(schemes) / sizeof(schemes[0]);
  H5::H5File f("symplectic.h5", H5F_ACC_TRUNC);

  for (int s = 0; s < numSchemes; s++) {

    F.setIntegratorScheme(schemes[s].first);
    mass[0] = 1;
    position[0] = 0;
    momentum[0] = 1;

    Einit = 0.5 * square(position[0]) + 0.5 * square(momentum[0]) / mass[0];
    for (int i = 0; i < Ntime; i++) {
      F.integrate(force_func, mass, epsilon, 1, position, momentum, gradient);
      p[i] = position[0];
      m[i] = momentum[0] / mass[0];
      E[i] = 0.5 * square(position[0]) + 0.5 * square(momentum[0]) / mass[0] -
             Einit;
    }

    H5::Group g = f.createGroup(schemes[s].second);
    hdf5_write_array(g, "energy", E);
    hdf5_write_array(g, "position", p);
    hdf5_write_array(g, "velocity", m);
  }
  LibLSS::StaticInit::finalize();

  return 0;
}
