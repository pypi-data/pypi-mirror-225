/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/julia/julia_mcmc.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/julia/julia.hpp"
#include "libLSS/julia/julia_mcmc.hpp"
#include "libLSS/mcmc/global_state.hpp"

LibLSS::Julia::Object LibLSS::Julia::pack(MarkovState &state) {
  using namespace LibLSS::Julia;

  return invoke("libLSS._setup_state", (void *)&state);
}
