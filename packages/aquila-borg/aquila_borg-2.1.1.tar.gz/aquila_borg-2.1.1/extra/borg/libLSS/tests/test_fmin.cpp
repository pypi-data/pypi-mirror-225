#define BOOST_TEST_MODULE fmin
#define BOOST_TEST_NO_MAIN
#define BOOST_TEST_ALTERNATIVE_INIT_API
#include <boost/test/included/unit_test.hpp>
#include <boost/test/data/test_case.hpp>

#include <memory>
#include <type_traits>

#include "libLSS/tools/optimization/array_helper.hpp"
#include "libLSS/tools/optimization/line_search.hpp"
#include "libLSS/tools/optimization/newton.hpp"
#include "libLSS/tools/optimization/fmin.hpp"
#include "libLSS/tools/optimization/bfgs.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/string_tools.hpp"
#include "CosmoTool/hdf5_array.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"

namespace utf = boost::unit_test;
using namespace LibLSS;

BOOST_AUTO_TEST_CASE(test_array_helper) {
  using namespace LibLSS::Optimization;
  typedef BoostArrayAllocator<double, 2> allocator_t;
  boost::multi_array<double, 2> ref_a(boost::extents[100][50]);

  auto b = allocator_t().new_like(ref_a);

  typedef std::remove_reference<decltype(b.get())>::type return_array;
  static_assert(
      return_array::dimensionality == 2,
      "Dimensionality of the returned array should be 2");
  BOOST_CHECK_EQUAL(b.get().shape()[0], 100);
  BOOST_CHECK_EQUAL(b.get().shape()[1], 50);

  *b = 1;
  for (size_t i = 0; i < 100; i++)
    for (size_t j = 0; j < 50; j++)
      BOOST_CHECK_EQUAL(b.get()[i][j], 1);
}

void myGradient(
    boost::multi_array_ref<double, 1> &g,
    boost::multi_array_ref<double, 1> &x) {
  g[0] = 0.2 * (x[0] - 1);
}

void myHessian(
    boost::multi_array_ref<double, 1> &H_g,
    boost::multi_array_ref<double, 1> const &x) {
  H_g[0] = 5 * H_g[0];
}

void myLargeGradient(boost::multi_array_ref<double, 1>& g, boost::multi_array_ref<double, 1>& x, boost::multi_array_ref<double, 2>& H) {
   for (size_t i = 0; i < g.shape()[0]; i++) {
      g[i] = 0;
      for (size_t j = 0; j < g.shape()[0]; j++) {
        g[i] += H[i][j] * (x[j] - 1.);
      }
   }
}

BOOST_AUTO_TEST_CASE(lbfgs_test) {
  using namespace LibLSS::Optimization;
  typedef BoostArrayAllocator<double, 1> allocator_t;
  allocator_t alloc;
  size_t const M = 15;
  size_t const N = 10;
  auto sz = boost::extents[N];
  auto sz2 = sz[N];
  boost::multi_array<double, 1> p(sz), x(sz), g(sz);
  boost::multi_array<double, 2>  H(sz2);

  lbfgs<allocator_t> dir(M, alloc);
  LibLSS::GSL_RandomNumber rng;

  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      if (i != j)
        H[i][j] = 0;
      else
        H[i][j] = (i+1.0)/N;
    }
  }

  for (int q = 0; q < 5*M; q++) {
    myLargeGradient(g, x, H);
    dir.storeNewStep(g, x);
    dir.computeNextDirection(MPI_Communication::instance(), p, g, x);
    fwrap(x) = fwrap(x) + 0.1*fwrap(p);
    for (int i = 0; i < N; i++) x[i] += 0.02*rng.gaussian();
  }

  for (int i = 0; i < N; i++) {
    x[i] = 2.0;
    g[i] = x[i];
  }
  dir.computeNextDirection(MPI_Communication::instance(), p, g, x);

  H5::H5File ff("bfgs_test.h5",H5F_ACC_TRUNC);
  CosmoTool::hdf5_write_array(ff, "x", p);
  for (int i = 0; i < N; i++) {
    x[i] = -2.0*N/(i+1.0);
  }
  CosmoTool::hdf5_write_array(ff, "ref", x);
}

BOOST_AUTO_TEST_CASE(line_search) {
  using namespace LibLSS::Optimization;
  typedef BoostArrayAllocator<double, 1> allocator_t;
  allocator_t alloc;

  auto ls = lineSearchOnlyGrad(0.9, 0.5, 10);

  boost::multi_array<double, 1> x0(boost::extents[1]);

  auto x = alloc.new_like(x0);
  auto pk = alloc.new_like(x0);
  auto pktmp = alloc.new_like(x0);

  x.get()[0] = 1000;

  for (int i = 0; i < 100; i++) {
    myGradient(pktmp.get(), x.get());
    myGradient(pk.get(), x.get());
    *pk = -(*pk);
    double alpha = ls.lineSearch(myGradient, x, pk, pktmp, alloc);
    *x = (*x) + alpha * (*pk);
  }

  BOOST_CHECK_CLOSE(x.get()[0], 1, 0.1);
}

void myGradient2(
    boost::multi_array_ref<double, 1> &g,
    boost::multi_array_ref<double, 1> &x) {
  g[0] = 0.2 * (x[0] - 1) + std::pow(x[0] - 1, 3);
}

void myGradient3(
    boost::multi_array_ref<double, 1> &g,
    boost::multi_array_ref<double, 1> &x) {
  double dx = x[0] - 1, dy = x[1] - 2;

  g[0] = 2*dx + 2*dy;
  g[1] = 2*dx + 4*dy;
}

void myHessian2(
    boost::multi_array_ref<double, 1> &H_g,
    boost::multi_array_ref<double, 1> const &x) {
  double coef = 0.2 + 3 * std::pow(x[0] - 1, 2);
  H_g[0] = H_g[0] / coef;
}

void myGradient4(boost::multi_array_ref<double, 1> &g, boost::multi_array_ref<double, 1> &x)
{
  g[0] = (x[0]-1)*std::exp(-0.5*std::pow(x[0]-1,2));
}

BOOST_AUTO_TEST_CASE(test_fmin_newton) {
  using namespace LibLSS::Optimization;
  typedef BoostArrayAllocator<double, 1> allocator_t;
  allocator_t alloc;

  newton<allocator_t> dir(myHessian2, alloc);
  auto ls = lineSearchOnlyGrad(0.9, 0.5, 20);

  boost::multi_array<double, 1> x0(boost::extents[1]);
  x0[0] = 1000.0;

  auto x = fmin(MPI_Communication::instance(), ls, dir, myGradient2, x0, alloc, 1e-5, 25);

  BOOST_CHECK_CLOSE(x.get()[0], 1, 1e-3);
}

BOOST_AUTO_TEST_CASE(test_fmin_lbfgs) {
  using namespace LibLSS::Optimization;
  typedef BoostArrayAllocator<double, 1> allocator_t;
  allocator_t alloc;

  lbfgs<allocator_t> dir(2, alloc);
  auto ls = lineSearchOnlyGrad(0.9, 0.5, 20);

  boost::multi_array<double, 1> x0(boost::extents[1]);
  x0[0] = 1000.0;

  auto x = fmin(MPI_Communication::instance(), ls, dir, myGradient2, x0, alloc, 1e-10, 100);

  BOOST_CHECK_CLOSE(x.get()[0], 1, 1e-3);
}


BOOST_AUTO_TEST_CASE(test_fmin_lbfgs_nonconvex) {
  using namespace LibLSS::Optimization;
  typedef BoostArrayAllocator<double, 1> allocator_t;
  allocator_t alloc;
  Console::instance().print<LOG_DEBUG>("Non convex optimization");

  lbfgs<allocator_t> dir(2, alloc);
  auto ls = lineSearchOnlyGrad(0.9, 0.5, 20); // 0.9 is advocated for Newton or quasi Newton

  boost::multi_array<double, 1> x0(boost::extents[1]);
  x0[0] = 1.9;

  auto x = fmin(MPI_Communication::instance(), ls, dir, myGradient4, x0, alloc, 1e-10, 50);

  BOOST_CHECK_CLOSE(x.get()[0], 1, 1e-3);
}


BOOST_AUTO_TEST_CASE(test_fmin_lbfgs_2d) {
  using namespace LibLSS::Optimization;
  typedef BoostArrayAllocator<double, 1> allocator_t;
  allocator_t alloc;

  lbfgs<allocator_t> dir(5, alloc);
  auto ls = lineSearchOnlyGrad(0.9, 0.5, 20);

  boost::multi_array<double, 1> x0(boost::extents[2]);
  x0[0] = 10.0;
  x0[1] = 10.0;

  auto x = fmin(MPI_Communication::instance(), ls, dir, myGradient3, x0, alloc, 1e-10, 100);

  BOOST_CHECK_CLOSE(x.get()[0], 1, 1e-3);
  BOOST_CHECK_CLOSE(x.get()[1], 2, 1e-3);
}

int main(int argc, char **argv) {
  setupMPI(argc, argv);
  LibLSS::QUIET_CONSOLE_START = false;
  StaticInit::execute();
  LibLSS::Console::instance().setVerboseLevel<LOG_DEBUG>();

  int ret = utf::unit_test_main(&init_unit_test, argc, argv);

  StaticInit::finalize();
  doneMPI();
  return ret;
}
