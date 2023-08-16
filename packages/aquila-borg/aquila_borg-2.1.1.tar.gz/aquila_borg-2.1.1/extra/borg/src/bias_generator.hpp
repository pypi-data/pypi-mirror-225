/*+
    ARES/HADES/BORG Package -- ./extra/borg/src/bias_generator.hpp
    Copyright (C) 2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_BORG_BIAS_GENERATOR_HPP
#define __LIBLSS_BORG_BIAS_GENERATOR_HPP

#include <functional>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include <H5Cpp.h>
#include <sys/types.h>
#include <string>
#include "libLSS/mcmc/global_state.hpp"
#include <tuple>
#include "libLSS/physics/likelihoods/base.hpp"

namespace LibLSS {

  typedef std::function<void(
      MPI_Communication *, MarkovState &state, BORGForwardModel &, ArrayType &,
      H5::H5File &, size_t)>
      BiasedDensityGenerator_t;

  typedef std::function<void(
      MPI_Communication *, MarkovState &state, LikelihoodInfo& , BORGForwardModel &, ArrayType &,
      H5::H5File &, size_t, long, size_t)> SystematicMapper_t;
  typedef std::tuple<BiasedDensityGenerator_t, SystematicMapper_t> BiasInfo_t;

  BiasInfo_t
  setup_biased_density_generator(std::string const &likelihood_name);

} // namespace LibLSS

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2018
