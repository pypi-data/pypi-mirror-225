/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/overload.hpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

/* This particular trick has been taken from stackoverflow.
 * It allows to have overloaded lambda operator in C++11
 * https://stackoverflow.com/questions/32475576/c11-overloaded-lambda-with-variadic-template-and-variable-capture
 * Author: Piotr Skotnicki
* MR FIXME: Is this still needed after ARES has changed to C++14?
 */

#pragma once
#ifndef __LIBLSS_TOOLS_OVERLOAD_HPP
#  define __LIBLSS_TOOLS_OVERLOAD_HPP

namespace LibLSS {

  namespace details_overload {
    template <class... Fs>
    struct _overload;

    template <class F0, class... Frest>
    struct _overload<F0, Frest...> : F0, _overload<Frest...> {
      _overload(F0 f0, Frest... rest) : F0(f0), _overload<Frest...>(rest...) {}

      using F0::operator();
      using _overload<Frest...>::operator();
    };

    template <class F0>
    struct _overload<F0> : F0 {
      _overload(F0 f0) : F0(f0) {}

      using F0::operator();
    };

    template <class... Fs>
    auto overload(Fs... fs) {
      return _overload<Fs...>(fs...);
    }
  } // namespace details_overload

  using details_overload::overload;

} // namespace LibLSS

#endif
// ARES TAG: num_authors = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
