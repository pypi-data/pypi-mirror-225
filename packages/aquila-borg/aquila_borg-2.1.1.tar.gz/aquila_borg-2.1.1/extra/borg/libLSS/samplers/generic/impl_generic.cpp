/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/generic/impl_generic.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/cconfig.h"
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/physics/bias/broken_power_law.hpp"
#include "libLSS/physics/adapt_classic_to_nb.hpp"
#include "libLSS/physics/likelihoods/negative_binomial.hpp"
#include "libLSS/physics/likelihoods/negative_binomial_alt.hpp"
#include "libLSS/physics/likelihoods/eft.hpp"
#include "libLSS/physics/bias/double_power_law.hpp"
#include "impl_skeleton.hpp"

using namespace LibLSS;

FORCE_INSTANCE(AdaptBias_NB<bias::PowerLaw>, NegativeBinomialLikelihood, 3);
FORCE_INSTANCE(
    AdaptBias_NB<bias::BrokenPowerLaw>, NegativeBinomialLikelihood, 5);

FORCE_INSTANCE(AdaptBias_NB<bias::PowerLaw>, AltNegativeBinomialLikelihood, 3);
FORCE_INSTANCE(
    AdaptBias_NB<bias::BrokenPowerLaw>, AltNegativeBinomialLikelihood, 5);
