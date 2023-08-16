/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_cosmo_expansion.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/physics/cosmo.hpp"

using namespace LibLSS;

int main(int argc, char **argv) {
  setupMPI(argc, argv);
  StaticInit::execute();
  CosmologicalParameters params;

  params.omega_r = 0;
  params.omega_k = 0;
  params.omega_m = 0.10;
  params.omega_b = 0.049;
  params.omega_q = 0.90;
  params.w = -1;
  params.wprime = 0;
  params.n_s = 1;
  params.sigma8 = 0.8;
  params.rsmooth = 0;
  params.h = 0.7;
  params.beta = 0;
  params.z0 = 0;
  params.a0 = 1;

  Cosmology cosmo(params);
  Cosmology cosmo2(params);

  cosmo.precompute_com2a();
  for (int i = 0; i <= 100; i++) {
    double z = i / 100., znew;
    double d;
    bool pass;

    d = cosmo.com2comph(cosmo.a2com(cosmo.z2a(z)));
    znew = cosmo.a2z(cosmo.com2a(cosmo.comph2com(d)));

    pass = std::abs(z - znew) < 1e-5;

    std::cout << z << " " << znew << " " << d << " " << pass << std::endl;
    if (pass == 0)
      return 1;
  }

  cosmo.precompute_d_plus();
  {
    double Dtest = cosmo.d_plus(0.7);
    double Dtest2 = cosmo2.d_plus(0.7);
    std::cout << Dtest << Dtest2 << std::endl;
  }
  for (int i = 0; i <= 100; i++) {
    double z = i / 100.;
    double D = cosmo.d_plus(cosmo.z2a(z));
    double D2 = cosmo2.d_plus(cosmo2.z2a(z));
    bool pass = std::abs(D - D2) < 1e-5;
    std::cout << z << " " << D << " " << D2 << " " << pass << std::endl;
    if (pass == 0)
      return 1;
  }

  StaticInit::finalize();
  doneMPI();
  return 0;
}
