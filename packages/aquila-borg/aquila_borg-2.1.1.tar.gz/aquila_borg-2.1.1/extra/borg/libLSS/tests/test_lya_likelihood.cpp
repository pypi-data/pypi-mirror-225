/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_lya_likelihood.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/physics/forwards/borg_lpt.hpp"
//#include "libLSS/physics/forwards/borg_pm.hpp"
#include "libLSS/samplers/generic/generic_hmc_likelihood.hpp"
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/physics/adapt_classic_to_gauss.hpp"
#include "libLSS/physics/likelihoods/gaussian.hpp"
#include "libLSS/physics/likelihoods/voxel_poisson.hpp"
#include "libLSS/samplers/lya/hades_lya_likelihood.hpp"
//#include "libLSS/samplers/lya_rsd_qlpt/hades_lya_likelihood_rsd.hpp"

#define BORG_SUPERSAMPLING 2
#define BORG_FORCESAMPLING 4
#define BORG_NSTEPS 20
#define BORG_ZSTART 69
#define BORG_RSD false
#define BORG_PARTFACTOR 2
//#define BORG_SUPERSAMPLING 1

auto makeModel(LibLSS::MPI_Communication * comm, LibLSS::MarkovState& state, LibLSS::BoxModel box, LibLSS::BoxModel box2) {
  using namespace LibLSS;
  auto m = std::make_shared<LibLSS::BorgLptModel<>>(
      comm, box, box, false /* norsd
*/
      ,
      2 /* ss factor */, 2.0, 0.001, 1.0, false);
  return m;
}

#define LIKELIHOOD_TO_TEST_INFO(obj, info) BorgLyAlphaLikelihood obj(LikelihoodInfo like_info)

