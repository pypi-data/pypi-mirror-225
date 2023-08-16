/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/julia/julia_ghosts.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_JULIA_GHOST_HPP
#define __LIBLSS_JULIA_GHOST_HPP

#include "libLSS/julia/julia.hpp"
#include "libLSS/tools/mpi/ghost_planes.hpp"

namespace LibLSS {
  namespace Julia {

    Object newGhostManager(GhostPlanes<double, 2> *planes, size_t maxN2);
  }
} // namespace LibLSS

#endif
