/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_ghost_planes.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#define BOOST_TEST_MODULE julia_likelihood
#define BOOST_TEST_NO_MAIN
#define BOOST_TEST_ALTERNATIVE_INIT_API
#include <boost/test/included/unit_test.hpp>
#include <boost/test/data/test_case.hpp>

#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/console.hpp"

#include "libLSS/tests/setup_hades_test_run.hpp"
#include "libLSS/tools/mpi/ghost_planes.hpp"
#include "libLSS/tools/static_init.hpp"

namespace utf = boost::unit_test;

using namespace LibLSS;
using namespace LibLSS_test;

BOOST_AUTO_TEST_CASE(fully_ghost) {
  GhostPlanes<double, 1> ghosts;
  MPI_Communication *comm = MPI_Communication::instance();

  Console::instance().print<LOG_VERBOSE>("Init test");
  std::list<int> required_planes, here_planes;
  boost::multi_array<double, 2> A(boost::extents[2][128]);
  size_t idMin, idMax;

  if (comm->rank() == 0) {
    required_planes = {0, 1};
    here_planes = {2, 3};
    idMin = 2;
    idMax = 4;
  } else if (comm->rank() == 1) {
    required_planes = {2, 3};
    here_planes = {0, 1};
    idMin = 0;
    idMax = 2;
  } else if (comm->rank() == 2) {
    here_planes = {};
    required_planes = {0, 1, 2, 3};
    idMin = 0;
    idMax = 0;
  }
  Console::instance().print<LOG_VERBOSE>("Setup ghosts");
  ghosts.setup(
      comm, required_planes, here_planes, boost::array<int, 1>{128}, 4);

  ghosts.synchronize(A);
}

int main(int argc, char **argv) {
  auto comm = setupMPI(argc, argv);
  LibLSS::StaticInit::execute();

  Console::instance().outputToFile(
      boost::str(boost::format("ghost_test.txt_%d") % comm->rank()));

  int ret = utf::unit_test_main(&init_unit_test, argc, argv);

  LibLSS::StaticInit::finalize();
  LibLSS::doneMPI();
  return ret;
}
