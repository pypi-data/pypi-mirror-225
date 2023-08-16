/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/cpu/feature_check.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TOOLS_CPUCHECK_HPP
#define __LIBLSS_TOOLS_CPUCHECK_HPP

#if defined(__GNUC__) && !defined(__INTEL_COMPILER)
#  include "feature_check_gnuc.hpp"
#else
#  include "feature_check_other.hpp"
#endif

#endif
