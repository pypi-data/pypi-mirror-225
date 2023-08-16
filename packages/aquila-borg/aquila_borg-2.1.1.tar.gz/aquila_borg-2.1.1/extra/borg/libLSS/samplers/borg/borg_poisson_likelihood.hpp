/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/borg/borg_poisson_likelihood.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_BORG_POISSON_DENSITY_HPP
#define __LIBLSS_BORG_POISSON_DENSITY_HPP

#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/tools/fftw_allocator.hpp"
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/samplers/hades/base_likelihood.hpp"
#include "libLSS/physics/likelihoods/base.hpp"

namespace LibLSS {

  class BorgPoissonLikelihood : public HadesBaseDensityLikelihood {
  public:
    typedef HadesBaseDensityLikelihood super_t;
    typedef HadesBaseDensityLikelihood::super_t grid_t;

  public:
    BorgPoissonLikelihood(LikelihoodInfo &info);
    virtual ~BorgPoissonLikelihood();

    void initializeLikelihood(MarkovState &state) override;
    void updateMetaParameters(MarkovState &state) override;
    void setupDefaultParameters(MarkovState &state, int catalog) override;

    void generateMockSpecific(
        ArrayRef const &parameters, MarkovState &state) override;

    double logLikelihoodSpecific(ArrayRef const &parameters) override;
    void gradientLikelihoodSpecific(
        ArrayRef const &parameters, ArrayRef &gradient_parameters) override;
  };

}; // namespace LibLSS

#endif
