/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/tests/test_dense_mass.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#define BOOST_TEST_MODULE mass_matrix
#define BOOST_TEST_NO_MAIN
#define BOOST_TEST_ALTERNATIVE_INIT_API
#include <boost/test/included/unit_test.hpp>
#include <boost/test/data/test_case.hpp>

#include "libLSS/tools/console.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"
#include "libLSS/mpi/generic_mpi.hpp"
#include <CosmoTool/algo.hpp>
#include <memory>
#include <H5Cpp.h>
#include "libLSS/hmclet/dense_mass.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"

namespace utf = boost::unit_test;

using namespace LibLSS;

BOOST_AUTO_TEST_CASE(dense_mass) {
  MPI_Communication *comm = MPI_Communication::instance();
  RandomNumberMPI<GSL_RandomNumber> rgen(comm, -1);

  HMCLet::DenseMassMatrix M(3);

  boost::multi_array<double, 1> numbers(boost::extents[3]);
  auto numbers_w = fwrap(numbers);
  double a[3];

  auto& cons = Console::instance();
  for (int i = 0; i < 20; i++) {
    a[0] = rgen.gaussian();
    a[1] = rgen.gaussian();
    a[2] = rgen.gaussian();
    numbers[0] = (a[0]+a[2])/std::sqrt(2.0);
    numbers[1] = (a[0]-a[2])/std::sqrt(2.0);
    numbers[2] = a[1];
  
    M.addMass(numbers);
    M.computeMainComponents();
    auto C = M.components();
    auto mean = M.getMean();
    cons.format<LOG_DEBUG>("c00 = %g, c01 = %g, c02 = %g", C(0,0), C(0,1), C(0,2));
    cons.format<LOG_DEBUG>("c10 = %g, c11 = %g, c12 = %g", C(1,0), C(1,1), C(1,2));
    cons.format<LOG_DEBUG>("c20 = %g, c21 = %g, c22 = %g", C(2,0), C(2,1), C(2,2));
    cons.format<LOG_DEBUG>("mean = %g,%g,%g", mean(0), mean(1), mean(2));
  }


}

int main(int argc, char *argv[]) {
  setupMPI(argc, argv);
  StaticInit::execute();

  int ret = utf::unit_test_main(&init_unit_test, argc, argv);

  StaticInit::finalize();
  doneMPI();
  return ret;
}

