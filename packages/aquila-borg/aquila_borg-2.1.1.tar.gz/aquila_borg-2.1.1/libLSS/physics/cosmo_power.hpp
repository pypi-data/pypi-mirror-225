/*+
    ARES/HADES/BORG Package -- ./libLSS/physics/cosmo_power.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __ARES_COSMO_POWER_HPP
#define __ARES_COSMO_POWER_HPP

#include <CosmoTool/algo.hpp>
#include <CosmoTool/cosmopower.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/log_traits.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include <boost/format.hpp>
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"

namespace LibLSS {

  inline void createCosmologicalPowerSpectrum(
      MarkovState &state, CosmologicalParameters &cosmo_params,
      double adjust = 1) {
    double h;
    using CosmoTool::square;
    ConsoleContext<LOG_INFO_SINGLE> ctx("filling cosmological power spectrum");

    CosmoTool::CosmoPower cpower;

    double Rsmooth = 0; // 1.6;
    h = cpower.h = cosmo_params.h;
    cpower.OMEGA_B = cosmo_params.omega_b;
    cpower.OMEGA_C = cosmo_params.omega_m - cosmo_params.omega_b;
    cpower.SIGMA8 = cosmo_params.sigma8;
    cpower.n = cosmo_params.n_s;
    ctx.print(
        boost::format(
            "sigma8 = %g, OmegaB = %g, Omega_C = %g, Omega_M = %g, h = %g") %
        cpower.SIGMA8 % cpower.OMEGA_B % cpower.OMEGA_C % cosmo_params.omega_m %
        h);
    cpower.updateCosmology();
    cpower.setFunction(CosmoTool::CosmoPower::HU_WIGGLES);
    cpower.normalize();

    ArrayType1d::ArrayType &k = *state.get<ArrayType1d>("k_modes")->array;
    ArrayType1d::ArrayType &Pk =
        *state.get<ArrayType1d>("powerspectrum")->array;
    for (long i = 0; i < k.num_elements(); i++) {
      Pk[i] = cpower.power(k[i] * h) * h * h * h * adjust *
              std::exp(-square(k[i] * Rsmooth));
    }

    // Notify that the power spectrum is ready.
//    state.get<ArrayType1d>("powerspectrum")->deferInit.submit_ready();
  }
} // namespace LibLSS

#endif
