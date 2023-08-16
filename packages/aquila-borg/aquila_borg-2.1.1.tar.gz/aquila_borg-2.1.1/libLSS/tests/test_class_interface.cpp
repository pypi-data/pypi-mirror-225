/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_class_interface.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

#include <iostream>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/physics/class_cosmo.hpp"

using namespace LibLSS;

int main(int argc, char **argv) {
  setupMPI(argc, argv);
  StaticInit::execute();
  CosmologicalParameters params;

  params.omega_r = 0.0;
  params.omega_k = 0.0;
  params.omega_m = 0.30;
  params.omega_q = 0.70;
  params.omega_b = 0.049;
  params.w = -1;
  params.n_s = 1.0;
  params.fnl = 0;
  params.wprime = 0;
  params.sigma8 = 0.8;
  params.h = 0.8;
  params.a0 = 1.0;
  params.sum_mnu = 0.1; // in eV

  ClassCosmo cc(params);

  // here we output the primordial power-spectrum

  int Nbin = 100;

  double kmin = -6;
  double kmax = 0.;
  double dk = (kmax - kmin) / (Nbin - 1);

  std::ofstream f("interpolate_Tk.txt");

  for (int i = 0; i < Nbin; i++) {
    double k = std::pow(10.0, kmin + dk * i);

    double Pk = cc.primordial_Pk(k);
    double Tk = cc.get_Tk(k);

    f << k << " " << Pk << " " << Tk << std::endl;
  }

  StaticInit::finalize();
  doneMPI();
  return 0;
}
