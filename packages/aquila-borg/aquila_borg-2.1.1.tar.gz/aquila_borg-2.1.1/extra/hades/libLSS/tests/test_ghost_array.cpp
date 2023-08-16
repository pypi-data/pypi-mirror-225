#include <boost/format.hpp>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/mpi/ghost_array.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/string_tools.hpp"

using namespace LibLSS;

int main(int argc, char **argv) {
  MPI_Communication *comm = setupMPI(argc, argv);

  StaticInit::execute();

  Console::instance().outputToFile(
      boost::str(boost::format("ghost_test.txt_%d") % comm->rank()));
  ;

  GhostArray<int> ghost;

  int Ncomm = comm->size();

  boost::multi_array<double, 1> test_array(boost::extents[2]);
  boost::multi_array<int, 1> test_idx(boost::extents[2]);

  if (comm->size() > 1) {
    test_idx[0] = comm->rank();
    test_idx[1] = (comm->rank() + 1) % comm->size();
  } else {
    test_idx[0] = 0;
    test_idx[1] = 1;
  }

  test_array[0] = 0.5;
  test_array[1] = 0.5;

  ghost.setup(comm, test_idx);

  int rank = comm->rank();
  int rank_next = (comm->rank() + 1) % comm->size();
  ghost.synchronize(test_array, [rank, rank_next](size_t i) {
    if (i == rank)
      return 0;
    else if (i == rank_next)
      return 1;
    else {
      Console::instance().print<LOG_ERROR>("Invalid index");
      MPI_Communication::instance()->abort();
      return 0;
    }
  });

  Console::instance().print<LOG_VERBOSE>(
      "Result: " + LibLSS::to_string(test_array));

  doneMPI();

  return 0;
}