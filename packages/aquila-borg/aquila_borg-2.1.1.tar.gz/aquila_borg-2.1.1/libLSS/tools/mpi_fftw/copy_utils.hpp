/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/mpi_fftw/copy_utils.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
template<bool upgrading, typename T> struct copy_utils{};

#include "copy_utils_upgrade.hpp"
#include "copy_utils_degrade.hpp"

