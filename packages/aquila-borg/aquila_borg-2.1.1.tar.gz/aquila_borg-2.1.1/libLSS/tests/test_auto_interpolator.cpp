/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_auto_interpolator.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include "libLSS/tools/auto_interpolator.hpp"
#include <boost/lambda/lambda.hpp>
#include <CosmoTool/algo.hpp>

using namespace LibLSS;

int main()
{
  using boost::lambda::_1;
  auto a = build_auto_interpolator(CosmoTool::square<double>, 0., 4., 0.1, 0., 16.);

  for (double i = -2; i < 7; i+=0.01)
    std::cout << i << " " << a(i) << " " << (i*i) << std::endl;

  auto_interpolator<double> b;

  b = a;

  return 0;
}
