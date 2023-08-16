/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/julia/julia_mcmc.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TOOLS_JULIA_MCMC_HPP
#define __LIBLSS_TOOLS_JULIA_MCMC_HPP

#include "libLSS/julia/julia.hpp"
#include "libLSS/mcmc/global_state.hpp"

namespace LibLSS {

  namespace Julia {

    Object pack(MarkovState &state);
  }

} // namespace LibLSS

#endif
