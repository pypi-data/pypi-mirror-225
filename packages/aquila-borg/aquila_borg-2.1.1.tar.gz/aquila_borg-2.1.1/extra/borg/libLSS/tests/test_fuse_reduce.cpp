/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_fuse_reduce.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include <boost/multi_array.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_reduce.hpp"

using boost::extents;
using LibLSS::b_fused;
using LibLSS::b_fused_idx;

int main() {
  LibLSS::StaticInit::execute();
  boost::multi_array<int, 2> a(extents[4][8]);
  double r;
  auto v_array = b_fused_idx<int, 2>(
      [](int i, int j) -> int { return i * j; }, extents[4][8]);
  auto v2_array =
      b_fused<int>(a, v_array, [](int c, int d) -> int { return c + d; });

  std::cout << v_array[2][2] << std::endl;
  std::cout << v2_array[2][2] << std::endl;

  LibLSS::copy_array(a, b_fused_idx<int, 2>([](int, int) -> int { return 3; }));
  r = LibLSS::reduce_sum<double>(a);
  std::cout << r << std::endl;
  r = LibLSS::reduce_sum<int>(v_array);
  std::cout << r << std::endl;
  r = LibLSS::reduce_sum<int>(v2_array);
  std::cout << r << std::endl;
  //  auto c= LibLSS::reduce_sum<std::complex<float>>(v2_array);
  //  std::cout << c << std::endl;

  LibLSS::StaticInit::finalize();
  return r;
}
