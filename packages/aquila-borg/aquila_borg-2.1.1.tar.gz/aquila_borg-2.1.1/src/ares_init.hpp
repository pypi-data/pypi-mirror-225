/*+
    ARES/HADES/BORG Package -- ./src/ares_init.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_ARES_COMMON_INIT_HPP
#define __LIBLSS_ARES_COMMON_INIT_HPP

#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/samplers/core/main_loop.hpp"
#include "libLSS/mcmc/state_element.hpp"
#include "common/foreground.hpp"

namespace LibLSS_prepare {

  template<typename PTree>
  static bool check_is_simulation(PTree& params) {
    return params.get_child("run").template get<bool>("SIMULATION", false);
  }

  template<typename PTree>
  static void sampler_init_data(
        MPI_Communication *mpi_world,
        MarkovState& state, PTree& params)
  {
    LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
    long Ncat = state.getScalar<long>("NCAT");
    // ==================
    if (check_is_simulation(params)) {
      for (int i = 0; i < Ncat; i++)
           initializeHaloSimulationCatalog(
                   state,
                   params, i);
    } else {
      for (int i = 0; i < Ncat; i++)
           initializeGalaxySurveyCatalog(
                   state,
                   params, i);
    }

  }

  template<typename PTree>
  static void sampler_load_data(
        MPI_Communication *mpi_world,
        MarkovState& state, PTree& params, MainLoop& loop)
  {
    LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
    CosmologicalParameters& cosmo = state.getScalar<CosmologicalParameters>("cosmology");
    long Ncat = state.getScalar<long>("NCAT");

    if (check_is_simulation(params)) {
      for (int i = 0; i < Ncat; i++) {
        loadHaloSimulationCatalog(
          state, params,
          i, cosmo);
      }
    } else {
      for (int i = 0; i < Ncat; i++) {
        loadGalaxySurveyCatalog(
          state, params,
          i, cosmo);
      }
    }

    // Load&Build foregrounds
    loadForegrounds(mpi_world, loop, params);

  }

  template<typename PTree>
  static void sampler_setup_data(MPI_Communication *mpi_world,
          MarkovState& state, PTree& params, MainLoop& loop)
  {
    LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
    long Ncat = state.getScalar<long>("NCAT");
    CosmologicalParameters& cosmo = state.getScalar<CosmologicalParameters>("cosmology");

    if (check_is_simulation(params)) {
      for (int i = 0; i < Ncat; i++) {
        SurveyPreparer preparer;
        setupSimulationCatalog(state, params, i, cosmo, preparer);
        state.newElement(boost::format("galaxy_preparer_%d") % i,
          new TemporaryElement<SurveyPreparer>(preparer)
        );
      }
    } else {
      for (int i = 0; i < Ncat; i++) {
        SurveyPreparer preparer;
        setupGalaxySurveyCatalog(state, params, i, cosmo, preparer);
        state.newElement(boost::format("galaxy_preparer_%d") % i,
          new TemporaryElement<SurveyPreparer>(preparer)
        );
      }
    }

  }


  template<typename PTree>
  static void sampler_prepare_data(MPI_Communication *mpi_world,
          MarkovState& state, PTree& params, MainLoop& loop)
  {
    long Ncat = state.getScalar<long>("NCAT");
    CosmologicalParameters& cosmo = state.getScalar<CosmologicalParameters>("cosmology");

    if (check_is_simulation(params)) {
      for (int i = 0; i < Ncat; i++) {
        auto& preparer = state.get<TemporaryElement<SurveyPreparer>>(boost::format("galaxy_preparer_%d") % i)->get();
        prepareHaloSimulationData(mpi_world, state, i, cosmo, preparer, params);
      }
    } else {
      for (int i = 0; i < Ncat; i++) {
        auto& preparer = state.get<TemporaryElement<SurveyPreparer>>(boost::format("galaxy_preparer_%d") % i)->get();
        prepareData(mpi_world, state, i, cosmo, preparer, params);
      }
    }
  }
}

#endif
