/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_voxel_poisson_fail.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include <boost/multi_array.hpp>
#include <boost/tuple/tuple.hpp>
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_reduce.hpp"
#include "libLSS/physics/voxel_poisson.hpp"

using boost::extents;
using LibLSS::b_fused;
using LibLSS::b_fused_idx;

int main() {
  typedef LibLSS::VoxelPoissonLikelihood Likelihood;

  boost::multi_array<double, 2> data(extents[4][8]);
  boost::multi_array<double, 2> lambda(extents[4][8]);
  boost::multi_array<double, 2> grad(extents[4][8]);
  auto const_lambda = [](int i, int j) -> double { return 2; };

  LibLSS::copy_array(lambda, b_fused_idx<double, 2>(const_lambda));

  Likelihood::diff_log_probability<1>(
      grad, boost::make_tuple(data, b_fused_idx<double, 2>(const_lambda)));

  return 0;
}
