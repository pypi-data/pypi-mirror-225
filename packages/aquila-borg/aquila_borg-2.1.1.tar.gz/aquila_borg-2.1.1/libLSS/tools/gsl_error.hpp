/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/gsl_error.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_GSL_ERROR_HPP
#define __LIBLSS_GSL_ERROR_HPP

#include "libLSS/tools/static_auto.hpp"

namespace LibLSS {
  void setGSLFatality(bool on);
}

AUTO_REGISTRATOR_DECL(GSL_Error);

#endif
