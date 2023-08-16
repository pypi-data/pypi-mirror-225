/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/log_traits.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_LOG_TRAITS_HPP
#define __LIBLSS_LOG_TRAITS_HPP

#include <string>
#include <iostream>
#include "libLSS/tools/static_auto.hpp"

namespace LibLSS {

    struct LOG_STD {
        static const int verboseLevel = 1;
        static const bool mainRankOnly = true;
        static const int numOutput = 1;
        static std::string prefix;
        static std::string prefix_c;
        static std::ostream *os[numOutput];
    };

    struct LOG_WARNING {
        static const int verboseLevel = 1;
        static const bool mainRankOnly = false;
        static const int numOutput = 2;
        static std::string prefix;
        static std::string prefix_c;
        static std::ostream *os[numOutput];
    };

    struct LOG_ERROR {
        static const int verboseLevel = 0;
        static const bool mainRankOnly = false;
        static const int numOutput = 1;
        static std::string prefix;
        static std::string prefix_c;
        static std::ostream *os[numOutput];
    };

    struct LOG_INFO {
        static const int verboseLevel = 2;
        static const bool mainRankOnly = false;
        static const int numOutput = 1;
        static std::string prefix;
        static std::string prefix_c;
        static std::ostream *os[numOutput];
    };

    struct LOG_INFO_SINGLE {
        static const int verboseLevel = 2;
        static const bool mainRankOnly = true;
        static const int numOutput = 1;
        static std::string prefix;
        static std::string prefix_c;
        static std::ostream *os[numOutput];
    };

    struct LOG_VERBOSE {
        static const int verboseLevel = 3;
        static const bool mainRankOnly = false;
        static const int numOutput = 1;
        static std::string prefix;
        static std::string prefix_c;
        static std::ostream *os[numOutput];
    };

    struct LOG_DEBUG {
        static const int verboseLevel = 4;
        static const bool mainRankOnly = false;
        static const int numOutput = 1;
        static std::string prefix;
        static std::string prefix_c;
        static std::ostream *os[numOutput];
    };


    typedef LOG_DEBUG DEFAULT_LOG_LEVEL;

    extern bool QUIET_CONSOLE_START;
};

AUTO_REGISTRATOR_DECL(LogTraits);

#endif
