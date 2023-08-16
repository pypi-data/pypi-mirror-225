/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/example/example_likelihood.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_EXAMPLE_DENSITY_HPP
#define __LIBLSS_EXAMPLE_DENSITY_HPP

#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/tools/fftw_allocator.hpp"
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/physics/forward_model.hpp"

namespace LibLSS {

  class ExampleDensitySampler : public HMCDensitySampler {
  protected:
    double xmin0, xmin1, xmin2;
    ArrayType1d *vobs;
    ArrayType *borg_final_density;

    BORGForwardModel *model;

    virtual void initial_density_filter(MarkovState &state);

    virtual HamiltonianType computeHamiltonian_Likelihood(
        MarkovState &state, CArray &s_array, bool final_call);
    virtual void computeGradientPsi_Likelihood(
        MarkovState &state, CArray &s, CArrayRef &grad_array, bool accumulate);

  public:
    ExampleDensitySampler(
        MPI_Communication *comm, int maxTimeIntegration, double maxEpsilon);
    virtual ~ExampleDensitySampler();

    void generateMockData(MarkovState &state, bool only_forward);
    virtual void generateMockData(MarkovState &state) {
      generateMockData(state, false);
    }

    virtual void restore(MarkovState &state);
    virtual void initialize(MarkovState &state);

    virtual void saveAuxiliaryAcceptedFields(MarkovState &state);
  };

}; // namespace LibLSS

#endif
