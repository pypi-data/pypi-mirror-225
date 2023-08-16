/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_borg_many_power_gradient.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/physics/forwards/borg_lpt.hpp"
#include "libLSS/samplers/generic/generic_hmc_likelihood.hpp"
#include "libLSS/physics/bias/many_power.hpp"
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/physics/adapt_classic_to_gauss.hpp"
#include "libLSS/physics/likelihoods/gaussian.hpp"
#include "libLSS/physics/likelihoods/voxel_poisson.hpp"
#include "libLSS/physics/likelihoods/robust_poisson.hpp"

#define BORG_SUPERSAMPLING 2
#define BORG_FORCESAMPLING 4
#define BORG_NSTEPS 20
#define BORG_ZSTART 69
#define BORG_RSD false
#define BORG_PARTFACTOR 2
//#define BORG_SUPERSAMPLING 1

#define LIKELIHOOD_TO_TEST_INFO(obj, info)                                     \
  LibLSS::GenericHMCLikelihood<                                                \
      bias::ManyPower<bias::ManyPowerLevels<double, 2, 2>>,                    \
      RobustPoissonLikelihood>                                                 \
      obj(comm, info)
/*#define LIKELIHOOD_TO_TEST(obj) \
LibLSS::GenericHMCLikelihood< \
  AdaptBias_Gauss<bias::ManyPower<bias::ManyPowerLevels<double, 2,2>> \
  >, GaussianLikelihood>  obj(comm, LikelihoodInfo())*/
#define MODEL_TO_TEST(obj, box)                                                \
  BorgLptModel<> *obj = new BorgLptModel<>(                                    \
      comm, box, BORG_RSD /* norsd*/, BORG_SUPERSAMPLING /* ss factor */, 2.0, \
      0.001, 1.0, false)
#include "generic_gradient_test.cpp"
