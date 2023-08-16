#ifndef __LIBLSS_PREPARE_LIKELIHOOD_INFO_HPP
#define __LIBLSS_PREPARE_LIKELIHOOD_INFO_HPP

#include "common/preparation_types.hpp"
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/physics/likelihoods/base.hpp"
#include "libLSS/mcmc/global_state.hpp"

namespace LibLSS_prepare {

  void setupLikelihoodInfo(
      MPI_Communication *comm, LibLSS::MarkovState &state,
      LibLSS::LikelihoodInfo &info, ptree &params, bool resuming);
}

#endif
