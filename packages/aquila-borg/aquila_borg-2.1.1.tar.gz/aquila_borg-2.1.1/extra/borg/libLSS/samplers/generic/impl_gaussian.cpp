/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/generic/impl_gaussian.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "impl_skeleton.hpp"
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/physics/bias/broken_power_law.hpp"
#include "libLSS/physics/bias/broken_power_law_sigmoid.hpp"
#include "libLSS/physics/bias/double_power_law.hpp"
#include "libLSS/physics/bias/linear_bias.hpp"

#include "libLSS/physics/likelihoods/gaussian.hpp"
#include "libLSS/physics/likelihoods/eft.hpp"
#include "libLSS/physics/likelihoods/eftmarg.hpp"
#include "libLSS/physics/adapt_classic_to_gauss.hpp"
#include "libLSS/physics/bias/many_power.hpp"
#include "libLSS/physics/bias/passthrough.hpp"
#include "libLSS/physics/bias/eft_bias_marg.hpp"
#include "libLSS/physics/bias/eft_bias.hpp"


using namespace LibLSS;

FORCE_INSTANCE(AdaptBias_Gauss<bias::Passthrough>, GaussianLikelihood, 1);

FORCE_INSTANCE(AdaptBias_Gauss<bias::PowerLaw>, GaussianLikelihood, 3);
FORCE_INSTANCE(AdaptBias_Gauss<bias::BrokenPowerLaw>, GaussianLikelihood, 5);
FORCE_INSTANCE(AdaptBias_Gauss<bias::BrokenPowerLawSigmoid>, GaussianLikelihood, 7);
FORCE_INSTANCE(
    AdaptBias_Gauss<bias::DoubleBrokenPowerLaw>, GaussianLikelihood, 4);
// FS: for now, disallow bundling of EFTBias to GaussianLikelihood
// FORCE_INSTANCE(bias::EFTBiasThresh, GaussianLikelihood, 7);
// FORCE_INSTANCE(bias::EFTBiasDefault, GaussianLikelihood, 7);
FORCE_INSTANCE(bias::EFTBiasDefault, EFTLikelihood, 7);
FORCE_INSTANCE(bias::EFTBiasMarg, EFTMargLikelihood, 7); // !!!
//FORCE_INSTANCE(AdaptBias_Gauss<bias::ManyPower<2>>, GaussianLikelihood, 4);
typedef AdaptBias_Gauss<bias::ManyPower<bias::ManyPowerLevels<double, 1>>>
    Power1;
typedef AdaptBias_Gauss<bias::ManyPower<bias::ManyPowerLevels<double, 1, 1>>>
    Power1_2;
typedef AdaptBias_Gauss<
    bias::ManyPower<bias::ManyPowerLevels<double, 1, 1, 1, 1>>>
    Power1_4;
FORCE_INSTANCE(Power1, GaussianLikelihood, 4);
FORCE_INSTANCE(Power1_2, GaussianLikelihood, 7);
FORCE_INSTANCE(Power1_4, GaussianLikelihood, 16);
FORCE_INSTANCE(AdaptBias_Gauss<bias::LinearBias>, GaussianLikelihood, 3);
