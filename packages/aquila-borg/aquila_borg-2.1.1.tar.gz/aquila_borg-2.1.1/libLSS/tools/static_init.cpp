/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/static_init.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/tools/static_init.hpp"

LibLSS::StaticInit& LibLSS::StaticInit::instance() {
    static StaticInit singleton;
        
    return singleton;
}
