/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/tests/test_hermiticity.cpp
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#define BOOST_TEST_MODULE modelio
#define BOOST_TEST_NO_MAIN
#define BOOST_TEST_ALTERNATIVE_INIT_API
#include <boost/test/included/unit_test.hpp>
#include <boost/test/data/test_case.hpp>
#include <H5Cpp.h>
#include <boost/multi_array.hpp>
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tests/testFramework.hpp"
#include "libLSS/tools/hdf5_error.hpp"
#include "libLSS/tools/hermiticity_fixup.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include <memory>

using namespace LibLSS;
using boost::extents;
using namespace CosmoTool;

namespace utf = boost::unit_test;

BOOST_AUTO_TEST_CASE(hermitic_forward) {
  int const N = 32;
  auto comm = MPI_Communication::instance();
  auto mgr = std::make_shared<FFTW_Manager<double, 3>>(N, N, N, comm);
  typedef boost::multi_array<std::complex<double>, 3> CArray;
  CArray input(mgr->extents_complex());
  CArray input_ref(mgr->extents_complex());
  CArray rebuilt(boost::extents[N][N][N / 2 + 1]);

  LibLSS_tests::loadReferenceInput(N, rebuilt);
  fwrap(input) = 0;
  fwrap(input[mgr->complex_range()]) = fwrap(rebuilt[mgr->complex_range()]);
  fwrap(rebuilt) = 0;

  Hermiticity_fixer<double, 3> fixer(mgr);
  size_t numLines = mgr->localN0;

  fixer.forward(input);


  if (comm->rank() == 0) {
    long numPlanes, q = 0;

    fwrap(rebuilt[mgr->complex_range()]) = fwrap(input[mgr->complex_range()]);
    q+= mgr->localN0;
    for (int r = 1; r < comm->size(); r++) {
      comm->recv(&numPlanes, 1, translateMPIType<long>(), r, r);
      comm->recv(
          &rebuilt[q][0][0], numPlanes * mgr->N1 * mgr->N2_HC,
          translateMPIType<std::complex<double>>(), r, r);
      q += numPlanes;
    }
  } else {
    long numPlanes = mgr->localN0;
    comm->send(&numPlanes, 1, translateMPIType<long>(), 0, comm->rank());
    comm->send(
        &input[mgr->startN0][0][0], numPlanes * mgr->N1 * mgr->N2_HC,
        translateMPIType<std::complex<double>>(), 0, comm->rank());
    H5::H5File f("dump_rank.h5_"+to_string(comm->rank()), H5F_ACC_TRUNC);
    CosmoTool::hdf5_write_array(f, "input", input); 
  }
  if (comm->rank() == 0) {
    CArray input_ref_full(boost::extents[N][N][N / 2 + 1]);
    LibLSS_tests::loadReferenceInput(N, input_ref_full);
    double norm = std::abs(fwrap(input_ref_full)).sum();
    double rel_difference =
        (std::abs(fwrap(rebuilt) - fwrap(input_ref_full)).sum()) / norm;
    BOOST_CHECK_LT(rel_difference, 1e-6);

    H5::H5File f("dump.h5", H5F_ACC_TRUNC);
    CosmoTool::hdf5_write_array(f, "rebuilt", rebuilt);
    CosmoTool::hdf5_write_array(f, "input_ref", input_ref_full);
  }
}

int main(int argc, char **argv) {
  setupMPI(argc, argv);
  LibLSS::QUIET_CONSOLE_START = true;
  StaticInit::execute();
  LibLSS::Console::instance().setVerboseLevel<LOG_DEBUG>();

  int ret = utf::unit_test_main(&init_unit_test, argc, argv);

  StaticInit::finalize();
  doneMPI();
  return 0;
}
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2019-2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
