/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/julia/julia_array.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_JULIA_ARRAY_HPP
#define __LIBLSS_JULIA_ARRAY_HPP

#include <boost/format.hpp>
#include "libLSS/julia/julia.hpp"
#include <vector>
#include <array>
#include <tuple>

namespace LibLSS {

  namespace Julia {

    typedef std::tuple<ssize_t, ssize_t> IndexRange;

    namespace helpers {
      typedef IndexRange _r;
    }

    template <size_t N>
    Object view_array(Object a, std::array<IndexRange, N> const &indexes) {
      using boost::format;
      using boost::str;
      std::vector<Object> args(1 + N);

      args[0] = a;
      for (size_t i = 0; i < N; i++) {
        auto const &t = indexes[i];
        args[1 + i] =
            evaluate(str(format("%d:%d") % std::get<0>(t) % std::get<1>(t)));
      }

      return manual_invoke("view", args);
    }

  } // namespace Julia

} // namespace LibLSS

#endif
