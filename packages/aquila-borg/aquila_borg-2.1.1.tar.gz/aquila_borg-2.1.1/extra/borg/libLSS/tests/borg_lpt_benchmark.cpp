/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/borg_lpt_benchmark.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/samplers/borg/borg_poisson_likelihood.hpp"
#include "libLSS/physics/forwards/borg_lpt.hpp"

#define BORG_SUPERSAMPLING 2
#define BORG_FORCESAMPLING 2
#define BORG_RSD false
#define BORG_PARTFACTOR 2.0
#define BORG_RESOLUTION 256
#define MIN_RANK 8

#define LIKELIHOOD_TO_TEST(obj) BorgPoissonDensitySampler obj(comm, 10, 0.1)
#define MODEL_TO_TEST(obj, box)                                                \
  BorgLptModel<> *obj = new BorgLptModel<>(                                    \
      comm, box, BORG_RSD, BORG_SUPERSAMPLING /* ss factor */, 2.0, 0.001,     \
      1.0, false)

#include "libLSS/tests/generic_gradient_benchmark.cpp"
