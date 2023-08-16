/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_cg.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <boost/multi_array.hpp>
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/optimization/cg.hpp"
#include <CosmoTool/algo.hpp>
#include <CosmoTool/hdf5_array.hpp>
#include <boost/preprocessor/cat.hpp>
#include <boost/preprocessor/stringize.hpp>
#include <boost/preprocessor/seq/for_each.hpp>
#include <algorithm>
#include "libLSS/tools/optimization/array_helper.hpp"

using namespace LibLSS;
using boost::extents;
using namespace CosmoTool;
using namespace std;

typedef Optimization::BoostArrayAllocator<double, 1> allocator_t;
typedef allocator_t::array_t Array;

void A(Array &out, Array const &in) {
  int N = in.shape()[0];
  //initialize values
  for (int i = 0; i < N; i++) {
    out[i] = 0;
    for (int j = 0; j < N; j++) {
      //test with simple correlation function
      double Mij = 0.5 * exp(-0.5 * (i - j) * (i - j));
      out[i] += Mij * in[j];
    }
  }
}

int main(int argc, char **argv) {
  setupMPI(argc, argv);
  LibLSS::Console &console = LibLSS::Console::instance();
  LibLSS::StaticInit::execute();

  allocator_t allocator;
  CG<allocator_t> cg(allocator);

  int N = 2000;
  boost::multi_array<double, 1> b(boost::extents[N]);
  boost::multi_array<double, 1> x0(boost::extents[N]);
  boost::multi_array<double, 1> x(boost::extents[N]);

  fwrap(b) = 1;
  fwrap(x) = 0;

  for (int i = 0; i < b.size(); i++)
    x0[i] = i;

  A(b, x0);

  cg.run(A, b, x);

  double max = 0;
  int imax = 0;
  double eps = 0.;
  for (int i = 0; i < b.size(); i++) {
    double diff = fabs(x[i] - x0[i]);
    if (max < diff)
      max = diff;
    imax = i;

    eps += diff * diff;
  }

  if (eps < 1e-5)
    std::cout << std::endl << "CG matrix inversion test passed!" << std::endl;
  else
    std::cout << "CG matrix inversion test failed!" << std::endl << std::endl;

  std::cout << "Distance between truth and solution  = " << eps << std::endl;
  std::cout << "Largest deviation  = " << max << " at element imax =" << imax
            << std::endl;

  LibLSS::StaticInit::finalize();

  doneMPI();
  return 0;
}
