/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_aux_attributes.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#define BOOST_TEST_NO_MAIN
#define BOOST_TEST_ALTERNATIVE_INIT_API
#define BOOST_TEST_MODULE part_attributes
#include <boost/test/included/unit_test.hpp>
#include <boost/test/data/test_case.hpp>

#include <iostream>
#include <boost/format.hpp>
#include <boost/multi_array.hpp>
#include "libLSS/mpi/generic_mpi.hpp"

#include "libLSS/physics/forwards/particle_balancer/attributes.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/static_init.hpp"
//#include "libLSS/physics/forwards/pm/particle_distribute.hpp"

namespace utf = boost::unit_test;
using boost::extents;
using boost::format;

BOOST_AUTO_TEST_CASE(part_attribute_scalar_element) {
  boost::multi_array<double, 1> p(extents[10]);
  LibLSS::Particles::ScalarAttribute<decltype(p) &> attr(p);

  for (int i = 0; i < 10; i++) {
    p[i] = 10 - i;
  }

  BOOST_TEST_CHECKPOINT("Allocate temporary attrs");
  auto new_attr = attr.allocateTemporary(8);

  for (int j = 0; j < 8; j++) {
    BOOST_TEST_CHECKPOINT("Store " << (20 - j) << " at " << j);
    new_attr.store(j, 20 - j);
  }

  for (int i = 0; i < 8; i++) {
    BOOST_CHECK_EQUAL(p[i], 10 - i);
    BOOST_CHECK_EQUAL(*(new_attr.getArrayData(i)), (20 - i));
  }

  new_attr.swap(0, 7);
  BOOST_CHECK_EQUAL(new_attr.getArrayData(0)[0], 20 - 7);
  BOOST_CHECK_EQUAL(new_attr.getArrayData(0)[7], 20);
}

BOOST_AUTO_TEST_CASE(part_attribute_vector_element) {
  boost::multi_array<double, 2> p(extents[10][3]);
  LibLSS::Particles::VectorAttribute<decltype(p) &> attr(p);

  for (int i = 0; i < 10; i++) {
    p[i][0] = 10 - i;
  }

  BOOST_TEST_CHECKPOINT("Allocate temporary attrs");
  auto new_attr = attr.allocateTemporary(8);

  for (int j = 0; j < 8; j++) {
    BOOST_TEST_CHECKPOINT("Store " << (20 - j) << " at " << j);
    new_attr.store(j, std::array<int, 3>{20 - j, 30 - j, 40 - j});
  }

  for (int i = 0; i < 8; i++) {
    BOOST_CHECK_EQUAL(p[i][0], 10 - i);

    double *data = new_attr.getArrayData(i);
    BOOST_CHECK_EQUAL(data[0], (20 - i));
    BOOST_CHECK_EQUAL(data[1], (30 - i));
    BOOST_CHECK_EQUAL(data[2], (40 - i));
  }

  new_attr.swap(0, 7);
  BOOST_CHECK_EQUAL(new_attr.getArrayData(0)[0], 20 - 7);
  BOOST_CHECK_EQUAL(new_attr.getArrayData(7)[0], 20);
  BOOST_CHECK_EQUAL(new_attr.getArrayData(0)[1], 30 - 7);
  BOOST_CHECK_EQUAL(new_attr.getArrayData(7)[1], 30);
  BOOST_CHECK_EQUAL(new_attr.getArrayData(0)[2], 40 - 7);
  BOOST_CHECK_EQUAL(new_attr.getArrayData(7)[2], 40);
}

int main(int argc, char *argv[]) {
  LibLSS::QUIET_CONSOLE_START = false; //true;
  LibLSS::setupMPI(argc, argv);
  LibLSS::StaticInit::execute();

  int ret = utf::unit_test_main(&init_unit_test, argc, argv);

  LibLSS::StaticInit::finalize();
  LibLSS::doneMPI();
  return ret;
}
