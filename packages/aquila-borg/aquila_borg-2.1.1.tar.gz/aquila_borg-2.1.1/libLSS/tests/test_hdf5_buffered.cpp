#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/hdf5_error.hpp"
#include <H5Cpp.h>
#include "libLSS/tools/hdf5_buffered_write.hpp"
#include "libLSS/tools/fusewrapper.hpp"

using namespace LibLSS;

int main(int argc, char **argv)
{
  LibLSS::MPI_Communication *mpi_world = LibLSS::setupMPI(argc, argv);
  StaticInit::execute();

  H5::H5File f("test.h5", H5F_ACC_TRUNC);
  auto& cons = Console::instance();


  boost::multi_array<double, 3> a(boost::extents[1000][2][3]);

  fwrap(a) = fwrap(b_fused_idx<double,3>([](int q, int r, int s) { return q+2*s; }));

  cons.format<LOG_VERBOSE>("a[5][0] = %g", a[5][0][0]);

  hdf5_write_buffered_array(f, "test", a, true, true, [&](size_t p) { 
    cons.format<LOG_STD>("Wrote %d", p);
  });
  CosmoTool::hdf5_write_array(f, "test2", a);

  StaticInit::finalize();

  return 0;
}
