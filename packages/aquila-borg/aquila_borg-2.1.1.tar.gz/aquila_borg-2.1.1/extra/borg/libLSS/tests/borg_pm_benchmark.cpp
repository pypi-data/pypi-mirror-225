/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/borg_pm_benchmark.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/samplers/borg/borg_poisson_likelihood.hpp"
#include "libLSS/physics/forwards/borg_multi_pm.hpp"

#define BORG_SUPERSAMPLING 2
#define BORG_FORCESAMPLING 2
#define BORG_NSTEPS 20
#define BORG_ZSTART 69
#define BORG_RSD false
#define BORG_PARTFACTOR 2.0
#define BORG_RESOLUTION 32
#define MIN_RANK 8

#define LIKELIHOOD_TO_TEST(obj) auto obj = std::make_shared<BorgPoissonLikelihood>(info)
#define MODEL_TO_TEST(obj, box)                                                \
  MetaBorgPMModel<> *obj = new MetaBorgPMModel<>(                                      \
      comm, box, box, BORG_SUPERSAMPLING /* ss factor */, BORG_FORCESAMPLING,       \
      BORG_NSTEPS, BORG_PARTFACTOR, BORG_RSD, 0.001, 1.0, BORG_ZSTART)

#include "libLSS/tests/generic_gradient_benchmark.cpp"
