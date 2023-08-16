/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/tests/setup_hades_test_run.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_SETUP_HADES_TEST_HPP
#define __LIBLSS_SETUP_HADES_TEST_HPP

#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/physics/likelihoods/base.hpp"

namespace LibLSS_test {
  void setup_box(LibLSS::MarkovState &state, LibLSS::BoxModel &box);
  void setup_hades_test_run(
      LibLSS::MPI_Communication *comm, size_t Nbase, double L,
      LibLSS::MarkovState &state,
      boost::multi_array_ref<double, 1> *bias_params = 0);

  void setup_likelihood_info(
      LibLSS::MarkovState &state, LibLSS::LikelihoodInfo &info, LibLSS::MPI_Communication *comm = LibLSS::MPI_Communication::instance());
} // namespace LibLSS_test

#endif
