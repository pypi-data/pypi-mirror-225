/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/generic/impl_robust.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "impl_skeleton.hpp"
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/physics/bias/broken_power_law.hpp"
#include "libLSS/physics/bias/broken_power_law_sigmoid.hpp"
#include "libLSS/physics/bias/many_power.hpp"
#include "libLSS/physics/likelihoods/robust_poisson.hpp"

using namespace LibLSS;

FORCE_INSTANCE(bias::PowerLaw, RobustPoissonLikelihood, 2);
FORCE_INSTANCE(bias::BrokenPowerLaw, RobustPoissonLikelihood, 4);
FORCE_INSTANCE(bias::BrokenPowerLawSigmoid, RobustPoissonLikelihood, 6);

typedef bias::ManyPower<bias::ManyPowerLevels<double, 1>> Power1;
typedef bias::ManyPower<bias::ManyPowerLevels<double, 1, 1>> Power1_2;
typedef bias::ManyPower<bias::ManyPowerLevels<double, 2, 2>> Power2_2;
FORCE_INSTANCE(Power1, RobustPoissonLikelihood, 3);
FORCE_INSTANCE(Power1_2, RobustPoissonLikelihood, 6);
FORCE_INSTANCE(Power2_2, RobustPoissonLikelihood, 15);
