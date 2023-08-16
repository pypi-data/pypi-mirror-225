/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/borg_splash.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_BORG_SPLASH_HPP
#define __LIBLSS_BORG_SPLASH_HPP

#include <string>
#include "libLSS/tools/color_mod.hpp"
#include "libLSS/borg_version.hpp"

namespace LibLSS {

  namespace BORG {
    using namespace LibLSS::Color;

    static void splash_borg() {

      static std::string splash_str[] = {
          "    ___________                              ",
          "   /-/_\"/-/_/-/|     __________________________ ",
          "  /\"-/-_\"/-_//||                " + fg(BLUE, "BORG3", BRIGHT) +
              " model",
          " /__________/|/|     (c) Jens Jasche 2012 - 2019",
          " |\"|_'='-]:+|/||        Guilhem Lavaux 2014 - 2019",
          " |-+-|.|_'-\"||//     __________________________ ",
          " |[\".[:!+-'=|//     ",
          " |='!+|-:]|-|/       ",
          "  ----------         ",
          "",
          "Please acknowledge the following papers:",
          "  - Jasche & Lavaux (A&A, 2019, arXiv 1806.11117)",
          "  - Jasche & Wandelt (MNRAS, 2012, arXiv 1203.3639)",
          "  - Jasche & Kitaura (MNRAS, 2010, arXiv 0911.2496)",
          "  - And relevant papers depending on the used sub-module/contribution",
          "\n",
          "This is BORG version " + BORG_GIT_VERSION};

      static const int numSplashStr =
          sizeof(splash_str) / sizeof(splash_str[0]);

      for (int i = 0; i < numSplashStr; i++)
        Console::instance().print<LOG_STD>(splash_str[i]);
    }

  } // namespace BORG
};  // namespace LibLSS


#endif
// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2014-2020
// ARES TAG: name(1) = Jens Jasche
// ARES TAG: email(1) = jens.jasche@fysik.su.se
// ARES TAG: year(1) = 2009-2020
