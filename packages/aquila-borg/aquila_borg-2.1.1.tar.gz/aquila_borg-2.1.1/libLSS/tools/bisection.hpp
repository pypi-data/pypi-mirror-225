/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/bisection.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_BISECTION_HPP
#define __LIBLSS_BISECTION_HPP

#include <cmath>

namespace LibLSS {

  template <typename Function>
  double
  bisection(double a, double b, double feps, double ftarget, Function f) {
    double c = 0;
    // Bisection Method
    double epsilon = 1e-6;
    double f_a = f(a);
    double f_b = f(b);

    if ((f_a < f_b && f_b < ftarget) || (f_a > f_b && f_b > ftarget)) {
      return b;
    }

    if ((f_a < f_b && f_a > ftarget) || (f_a > f_b && f_a < ftarget)) {
      return a;
    }

    while (std::abs(a - b) > 2 * epsilon) {
      // Calculate midpoint of domain
      c = (a + b) / 2.;
      double f_c = f(c);
      double fc = ftarget - f_c;
      double fa = ftarget - f_a;

      if (std::abs(fc) < feps)
        break; //break if tolerance has been reached
      if ((fa * fc) < 0.)
        b = c;
      else {
        a = c;
        f_a = f_c;
      }
    }
    return c;
  }

} // namespace LibLSS

#endif

