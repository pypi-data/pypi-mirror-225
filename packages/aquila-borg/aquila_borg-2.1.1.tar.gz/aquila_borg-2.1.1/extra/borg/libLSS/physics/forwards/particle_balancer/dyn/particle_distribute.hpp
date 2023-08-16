/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/particle_balancer/dyn/particle_distribute.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PARTICLE_DYN_DISTRIBUTE_HPP
#define __LIBLSS_PARTICLE_DYN_DISTRIBUTE_HPP

#include <boost/multi_array.hpp>
#include <boost/format.hpp>
#include <functional>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/uninitialized_type.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/physics/forwards/particle_balancer/particle_distribute.hpp"
#include "libLSS/physics/forwards/particle_balancer/dyn/attributes.hpp"

namespace LibLSS {

  /**
   * @brief Distribute the attributes according to the balance info instructions.
   *
   * @param comm MPI communicator
   * @param info Info for particle balancing
   * @param attrs Vector of attributes
   */
  void dynamic_particle_redistribute(
      MPI_Communication *comm, BalanceInfo const &info,
      std::vector<std::shared_ptr<AbstractParticles::Attribute>> attrs);
} // namespace LibLSS

#endif
