/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/string_tools.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_STRING_TOOLS_HPP
#define __LIBLSS_STRING_TOOLS_HPP

#include <string>
#include <iostream>
#include <algorithm>
#include <sstream>
#include <vector>
#include <boost/format.hpp>
#include <boost/multi_array.hpp>
#include "libLSS/tools/is_stl_container.hpp"

namespace LibLSS {

  using std::to_string;

  template <typename T>
  typename std::enable_if<is_stl_container_like<T>::value, std::string>::type
  to_string(T const &V) {
    std::ostringstream s;

    std::copy(
        V.begin(), V.end(),
        std::ostream_iterator<typename T::value_type>(s, ","));
    return s.str();
  }

  std::vector<std::string>
  tokenize(std::string const &in, std::string const &separator);

  namespace lssfmt {

    namespace format_detail {

      static void _format_expansion(boost::format &f) {}

      template <typename A, typename... U>
      static void _format_expansion(boost::format &f, A &&a, U &&...u) {
        _format_expansion(f % a, u...);
      }

      template <typename... U>
      std::string format(std::string const &s, U &&...args) {
        boost::format f(s);
        _format_expansion(f, std::forward<U>(args)...);
        return boost::str(f);
      }

    } // namespace format_detail

    using format_detail::format;

  } // namespace lssfmt
  /*  template<typename T>
  std::string to_string(boost::multi_array_ref<T,1> const& V) {
    std::ostringstream s;

    std::copy(V.begin(), V.end(), std::ostream_iterator<T>(s, ","));
    return s.str();
  }*/
} // namespace LibLSS

#endif
