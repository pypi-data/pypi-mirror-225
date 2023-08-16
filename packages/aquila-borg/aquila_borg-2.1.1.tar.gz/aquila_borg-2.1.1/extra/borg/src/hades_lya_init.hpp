/*+
    ARES/HADES/BORG Package -- ./extra/borg/src/hades_lya_init.hpp
    Copyright (C) 2020 Natalia Porqueres <n.porqueres@imperial.ac.uk>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HADES_LYA_COMMON_INIT_HPP
#define __LIBLSS_HADES_LYA_COMMON_INIT_HPP

#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/samplers/core/main_loop.hpp"
#include "libLSS/mcmc/state_element.hpp"
#include "common/foreground.hpp"
#include "common/preparation_lyman_alpha.hpp"

namespace LibLSS_prepare {
	
  template<typename PTree>
  static void sampler_init_data(
        MPI_Communication *mpi_world,
        MarkovState& state, PTree& params)
  {
  	long Ncat = state.getScalar<long>("NCAT");
    
    // ==================
    
    for (int i = 0; i < Ncat; i++){
    	initializeLymanAlphaSurveyCatalog(state, i);
    }

  }

  template<typename PTree>
  static void sampler_load_data(
        MPI_Communication *mpi_world,
        MarkovState& state, PTree& params, MainLoop& loop)
  {
    long Ncat = state.getScalar<long>("NCAT");
    CosmologicalParameters& cosmo = state.getScalar<CosmologicalParameters>("cosmology");
	
	for (int i = 0; i < Ncat; i++) { 
        loadLymanAlpha(state,params,i);
        prepareLOS(mpi_world, state, i, cosmo);
    }

  }

  template<typename PTree>
  static void sampler_setup_data(
        MPI_Communication *mpi_world,
        MarkovState& state, PTree& params, MainLoop& loop)
  {}

  template<typename PTree>
  static void sampler_prepare_data(
        MPI_Communication *mpi_world,
        MarkovState& state, PTree& params, MainLoop& loop)
  {}
  
  
}

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Natalia Porqueres
// ARES TAG: email(0) = n.porqueres@imperial.ac.uk
// ARES TAG: year(0) = 2020

