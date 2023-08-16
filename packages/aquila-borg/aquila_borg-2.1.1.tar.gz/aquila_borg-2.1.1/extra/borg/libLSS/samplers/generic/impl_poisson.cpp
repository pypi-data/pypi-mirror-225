/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/generic/impl_poisson.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "impl_skeleton.hpp"
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/physics/bias/broken_power_law.hpp"
#include "libLSS/physics/bias/broken_power_law_sigmoid.hpp"
#include "libLSS/physics/adapt_classic_to_nb.hpp"
#include "libLSS/physics/bias/double_power_law.hpp"
#include "libLSS/physics/bias/double_power_law.hpp"
#include "libLSS/physics/likelihoods/voxel_poisson.hpp"
#include "libLSS/physics/bias/many_power.hpp"
#include "libLSS/physics/bias/downgrader.hpp"
#include "libLSS/physics/bias/passthrough.hpp"


using namespace LibLSS;

typedef bias::Downgrader<bias::BrokenPowerLaw> BrokenPowerLawDowngrade;
typedef bias::Downgrader<bias::PowerLaw> PowerLawDowngrade;
FORCE_INSTANCE(bias::PowerLaw, VoxelPoissonLikelihood, 2);
FORCE_INSTANCE(bias::BrokenPowerLaw, VoxelPoissonLikelihood, 4);
FORCE_INSTANCE(bias::BrokenPowerLawSigmoid, VoxelPoissonLikelihood, 6);
FORCE_INSTANCE(PowerLawDowngrade, VoxelPoissonLikelihood, 2);
FORCE_INSTANCE(BrokenPowerLawDowngrade, VoxelPoissonLikelihood, 4);
FORCE_INSTANCE(bias::DoubleBrokenPowerLaw, VoxelPoissonLikelihood, 3);

FORCE_INSTANCE(bias::Noop, VoxelPoissonLikelihood, 1);
FORCE_INSTANCE(bias::Passthrough, VoxelPoissonLikelihood, 1);

typedef bias::ManyPower<bias::ManyPowerLevels<double, 1>> Power1;
typedef bias::ManyPower<bias::ManyPowerLevels<double, 1, 1>> Power1_2;
typedef bias::ManyPower<bias::ManyPowerLevels<double, 2, 2>> Power2_2;
typedef bias::ManyPower<bias::ManyPowerLevels<double, 1, 1, 1, 1>> Power1_4;
typedef bias::ManyPower<bias::ManyPowerLevels<double, 2, 2, 2, 2>> Power2_4;
typedef bias::ManyPower<bias::ManyPowerLevels<double, 4>> Power4_1;
FORCE_INSTANCE(Power1, VoxelPoissonLikelihood, 3);
FORCE_INSTANCE(Power1_2, VoxelPoissonLikelihood, 6);
FORCE_INSTANCE(Power2_2, VoxelPoissonLikelihood, 15);
FORCE_INSTANCE(Power1_4, VoxelPoissonLikelihood, 15);
FORCE_INSTANCE(Power2_4, VoxelPoissonLikelihood, 45);
FORCE_INSTANCE(Power4_1, VoxelPoissonLikelihood, 15);

typedef bias::Downgrader<bias::ManyPower<bias::ManyPowerLevels<double, 1,1>>, bias::DegradeGenerator<1,1>> ManyDegrader_1_2;
FORCE_INSTANCE(ManyDegrader_1_2, VoxelPoissonLikelihood, 6);
typedef bias::Downgrader<bias::ManyPower<bias::ManyPowerLevels<double, 2,2>>, bias::DegradeGenerator<1,1,1>> ManyDegrader4_2_2;
FORCE_INSTANCE(ManyDegrader4_2_2, VoxelPoissonLikelihood, 15);

//FORCE_INSTANCE(bias::ManyPower<2>, VoxelPoissonLikelihood, 3);
//FORCE_INSTANCE(bias::ManyPower<3>, VoxelPoissonLikelihood, 6);
