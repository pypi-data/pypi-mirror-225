/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/data/lyman_alpha.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_LYMAN_ALPHA_HPP
#define __LIBLSS_LYMAN_ALPHA_HPP

#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/physics/projector.hpp"

namespace LibLSS {
    
    struct BaseLymanAlphaDescriptor {
        unsigned long long id;
        double phi, theta;
        double zo;
        double z;
        double r;
    };
    
};

  /* HDF5 complex type */
  CTOOL_STRUCT_TYPE(LibLSS::BaseLymanAlphaDescriptor, HDF5T_BaseLymanAlphaDescriptor,
    ((unsigned long long, id))
    ((double, phi))
    ((double, theta))
    ((double, zo))
    ((double, z))
    ((double, r))
  );
  
#endif
