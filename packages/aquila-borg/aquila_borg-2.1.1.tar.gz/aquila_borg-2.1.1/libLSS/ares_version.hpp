/*+
    ARES/HADES/BORG Package -- ./libLSS/ares_version.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_ARES_VERSION_HPP
#define __LIBLSS_ARES_VERSION_HPP

#include <string>

namespace LibLSS {

  /// This string holds the GIT version of the ARES root module.
  extern const std::string ARES_GIT_VERSION;

  /// Holds a semi-colon separated list of the modules that were compiled in.
  extern const std::string ARES_BUILTIN_MODULES;

  /// Extensive git report on the different git versions used in the final binary.
  extern const std::string ARES_GIT_REPORT;
} // namespace LibLSS

#endif
