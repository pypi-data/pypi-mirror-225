/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/core/gig_sampler.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LSS_GIG_SAMPLER_HPP
#define __LSS_GIG_SAMPLER_HPP

#include "random_number.hpp"

namespace LibLSS {
  double GIG_sampler_3params(double a,double b,double p, RandomNumber& rng);
}

#endif
