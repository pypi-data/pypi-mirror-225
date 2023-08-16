/*+
    ARES/HADES/BORG Package -- ./src/ares_bundle_init.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef _ARES_BUNDLE_INIT_HPP
#define _ARES_BUNDLE_INIT_HPP

#include "ares_bundle.hpp"

namespace LibLSS {

  template <typename ptree>
  void sampler_bundle_init(
      MPI_Communication *mpi_world, ptree &params, SamplerBundle &bundle,
      MainLoop &loop, bool) {
    int messenger_mixing =
        params.template get<int>("system.messenger_mixing", 20);
    int bias_mixing = params.template get<int>(
        "system.bias_mixing",
        6); //Push down. We are doing a 3 loop on FG+Nbar 20);
    MarkovState &state = loop.get_state();
    ptree system_params = params.get_child("system");

    // Initialize foregrounds
    LibLSS_prepare::initForegrounds(mpi_world, state, [&bundle](int c, int a) { bundle.newForeground(c, a); }, params);

    adapt<bool>(state, system_params, "power_sampler_a_blocked", false);
    adapt<bool>(state, system_params, "power_sampler_b_blocked", false);
    adapt<bool>(state, system_params, "power_sampler_c_blocked", false);
    adapt<bool>(state, system_params, "messenger_signal_blocked", false);
    adapt<bool>(state, system_params, "bias_sampler_blocked", false);

    // ==================
    // MAIN LOOP PROGRAM
    loop << bundle.sel_updater << bundle.sampler_catalog_projector
         << (BlockLoop(messenger_mixing)
             << bundle.sampler_t << bundle.sampler_s << bundle.spectrum_a
             << bundle.sampler_t << bundle.sampler_s << bundle.spectrum_b)
         << (BlockLoop(10) << bundle.foreground_block << bundle.sel_updater
                           << (BlockLoop(bias_mixing) << bundle.lb_sampler))
         << bundle.spectrum_c;
  }

  template<typename ptree>
  void sampler_setup_ic(SamplerBundle &bundle, MainLoop &loop, ptree const& params) {}

  void sampler_bundle_cleanup() {}

} // namespace LibLSS

#endif
