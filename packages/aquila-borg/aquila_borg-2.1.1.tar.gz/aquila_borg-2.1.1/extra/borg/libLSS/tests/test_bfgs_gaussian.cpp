#define BOOST_TEST_MODULE fmin
#define BOOST_TEST_NO_MAIN
#define BOOST_TEST_ALTERNATIVE_INIT_API
#include <boost/test/included/unit_test.hpp>
#include <boost/test/data/test_case.hpp>

#include <memory>
#include <type_traits>

#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/optimization/array_helper.hpp"
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/tools/optimization/line_search.hpp"
#include "libLSS/tools/optimization/fmin.hpp"
#include "libLSS/tools/optimization/bfgs.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/string_tools.hpp"

namespace utf = boost::unit_test;
using namespace LibLSS;

BOOST_AUTO_TEST_CASE(test_fmin_wiener) {
  using namespace LibLSS::Optimization;
  typedef BoostArrayAllocator<double, 2> allocator_t;
  allocator_t alloc;

  newton<allocator_t> dir(myHessian2, alloc);
  auto ls = lineSearchOnlyGrad(0.9, 0.5, 5);

  booost::multi_array<double, 2> x0(boost::extents[Ng][Ng]);
  FFTW_Manager<double, 2> mgr(Ng, Ng, MPI_Communication::instance());
  auto real_field = mgr.allocate_array();
  auto complex_field = mgr.allocate_complex_array();

  auto analysis = mgr.create_plan_r2c(real_field.get_array().data(), complex_field.get_array().data());
  auto synthesis = mgr.create_plan_c2r(complex_field.get_array().data, real_field.get_array().data());


  auto inv_noise = fwrap(
    b_fused_idx<double, 2>([](int,int) { return 1.0; }, boost::extents[Ng][Ng]));

  auto myGradient = [&](allocator_t::array_t &g, allocator_t::array_t &s) {
     auto ws = fwrap(s);
     auto wg = fwrap(g);
     auto wr = fwrap(real_field.get_array());
     auto wc = fwrap(complex_field.get_array());

     wg = inv_noise*(data - ws);

     wr = ws;
     mgr.execute_r2c((*wr).data(), (*wc).data());
     wc *= inv_prior;
     mgr.execute_c2r((*wc).data(), (*wr).data());
     wg += wr;
  }

  auto x = fmin(ls, dir, myGradient, x0, alloc, 1e-5, 25);

  H5::File f("lbgfs_solve.h5", H5_ACC_TRUNCATE);
  hdf5_write_array(f, "solution", x.get());
}

int main(int argc, char **argv) {
  LibLSS::QUIET_CONSOLE_START = true;
  startMPI(argc, argv);
  StaticInit::execute();

  int ret = utf::unit_test_main(&init_unit_test, argc, argv);

  StaticInit::finalize();
  doneMPI()
  return ret;
}
