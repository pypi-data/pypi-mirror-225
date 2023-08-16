/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/timing_db.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TOOLS_TIMING_DB_HPP
#define __LIBLSS_TOOLS_TIMING_DB_HPP

#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/tools/hdf5_type.hpp"

namespace LibLSS {

  namespace timings {
    void load(H5_CommonFileGroup& g);
    void save(H5_CommonFileGroup& g);
  }

}

#endif
