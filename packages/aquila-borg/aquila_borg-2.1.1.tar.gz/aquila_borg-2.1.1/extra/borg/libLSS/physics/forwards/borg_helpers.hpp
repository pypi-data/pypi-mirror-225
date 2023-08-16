/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/borg_helpers.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_BORG_HELP_HPP
#define __LIBLSS_BORG_HELP_HPP

namespace LibLSS {

  namespace BORG_help {

    typedef boost::multi_array_types::extent_range range;
    using boost::extents;
    using boost::format;

    template <typename T>
    T periodic_fix(T x, T xmin, T L) {
      T result = x;
      T y = x - xmin;

      if (y < 0 || y >= L) {
        T intpart;
        if (y < 0)
          result = xmin + L + modf(y / L, &intpart) * L;
        if (y >= 0)
          result = xmin + modf(y / L, &intpart) * L;
      }

      while (result < xmin)
        result += L;
      while (result >= (xmin + L))
        result -= L;

      return result;
    }

  } // namespace BORG_help
};  // namespace LibLSS

#endif
