/*+
    ARES/HADES/BORG Package -- ./libLSS/data/angtools.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_ANGTOOLS_HPP
#define __LIBLSS_ANGTOOLS_HPP

#include <cmath>

namespace LibLSS {

  template <typename T, typename Array>
  void ang2vec(T ra, T dec, Array &xyz) {
    T c_ra = std::cos(ra), s_ra = std::sin(ra), c_dec = std::cos(dec),
      s_dec = std::sin(dec);

    xyz[0] = c_ra * c_dec;
    xyz[1] = s_ra * c_dec;
    xyz[2] = s_dec;
  }

  template <typename T, typename Array>
  void vec2ang(Array xyz, T &ra, T &dec) {

    T c_r = std::sqrt(xyz[0] * xyz[0] + xyz[1] * xyz[1] + xyz[2] * xyz[2]);

    ra = std::atan2(xyz[1], xyz[0]);

    dec = 0.;

    if (c_r > 0)
      dec = std::asin(xyz[2] / c_r);
  }

  template <typename T, typename Array>
  void vec2ang(Array xyz, T &ra, T &dec, T &r) {

    r = std::sqrt(xyz[0] * xyz[0] + xyz[1] * xyz[1] + xyz[2] * xyz[2]);

    ra = std::atan2(xyz[1], xyz[0]);

    dec = 0.;

    if (r > 0)
      dec = std::asin(xyz[2] / r);
  }

}; // namespace LibLSS

#endif
