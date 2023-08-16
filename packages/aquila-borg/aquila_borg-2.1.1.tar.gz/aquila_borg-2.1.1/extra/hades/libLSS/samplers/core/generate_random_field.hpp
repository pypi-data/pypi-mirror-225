#ifndef __LIBLSS_GENERATE_RANDOM_FIELD_HPP
#define __LIBLSS_GENERATE_RANDOM_FIELD_HPP

#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/mcmc/global_state.hpp"

namespace LibLSS {

  void generateRandomField(MPI_Communication *comm, MarkovState &state);

}

#endif
