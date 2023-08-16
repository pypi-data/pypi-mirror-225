/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/core/ran_gig.h
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_RANGIG_H
#define __LIBLSS_RANGIG_H

namespace LibLSS {

double ran_gig(double chi, double psi, double lambda,gsl_rng * SEED);

}

#endif
