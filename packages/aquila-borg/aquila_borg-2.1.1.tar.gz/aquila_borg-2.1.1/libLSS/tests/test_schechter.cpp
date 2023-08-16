/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_schechter.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include <boost/format.hpp>
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/data/schechter_completeness.hpp"

using std::cout;
using std::endl;
using namespace LibLSS;

int main() {
  StaticInit::execute();
  Console::instance().setVerboseLevel<LOG_STD>();
  CosmologicalParameters cosmo_params;

  cosmo_params.omega_m = 0.30;
  cosmo_params.omega_b = 0.045;
  cosmo_params.omega_q = 0.70;
  cosmo_params.w = -1;
  cosmo_params.n_s = 0.97;
  cosmo_params.sigma8 = 0.8;
  cosmo_params.h = 0.68;
  cosmo_params.a0 = 1.0;
  Cosmology cosmo(cosmo_params);
  GalaxySampleSelection selection;
  SchechterParameters params;

  params.Mstar = -23.17;
  params.alpha = -0.9;
  selection.bright_apparent_magnitude_cut = -100;
  selection.faint_apparent_magnitude_cut = 11.5;
  selection.bright_absolute_magnitude_cut = -26;
  selection.faint_absolute_magnitude_cut = -20;

  double zlist[] = {0.001, 0.005, 0.01, 0.02, 0.03};
  double E[] = {1, 0.929577, 0.455884, 0.0966858, 0.013993};

  for (int i = 0; i < sizeof(zlist) / sizeof(zlist[0]); i++) {
    double d_comoving;
    d_comoving = cosmo.a2com(cosmo.z2a(zlist[i]));

    cout << "C = "
         << details::computeSchechterCompleteness(
                cosmo, zlist[i], d_comoving, selection, params)
         << " expect = " << E[i] << endl;
  }
  return 0;
}
