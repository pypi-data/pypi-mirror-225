/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/ptree_vectors.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PTREE_VECTORS_HPP
#define __LIBLSS_PTREE_VECTORS_HPP

#include <string>
#include <boost/lexical_cast.hpp>
#include <vector>
#include "libLSS/tools/string_tools.hpp"

namespace LibLSS {

  template<typename T>
  std::vector<T> string_as_vector(const std::string& s, std::string const& separator)
  {
    auto tokens = tokenize(s, separator);
    std::vector<T> result;
    std::transform(tokens.begin(), tokens.end(), std::back_inserter(result),
		   [](std::string const& s)->T { return boost::lexical_cast<T>(s); });
    return result;
  }
}

#endif
