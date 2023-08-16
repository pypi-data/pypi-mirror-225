/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_gig.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"
#include "libLSS/samplers/core/gig_sampler.hpp"

using std::cout;
using std::endl;
using namespace LibLSS;

int main()
{
  double a = 10.;
  double b = 5.;

  double p = 1 - 30.;

  GSL_RandomNumber rgen;

  for (int i = 0; i < 100000; i++) {
    cout << GIG_sampler_3params(a, b, p, rgen) << endl;
  }

  return 0;

}

