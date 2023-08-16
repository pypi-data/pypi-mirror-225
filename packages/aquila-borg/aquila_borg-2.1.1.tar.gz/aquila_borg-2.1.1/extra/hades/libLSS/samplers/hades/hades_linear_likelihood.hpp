/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/samplers/hades/hades_linear_likelihood.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HADES_LINEAR_DENSITY_HPP
#define __LIBLSS_HADES_LINEAR_DENSITY_HPP

#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/tools/fftw_allocator.hpp"
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/core/gridLikelihoodBase.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/samplers/hades/base_likelihood.hpp"

namespace LibLSS {

  class HadesLinearDensityLikelihood : public HadesBaseDensityLikelihood {
  public:
    typedef HadesBaseDensityLikelihood super_t;
    typedef HadesBaseDensityLikelihood::super_t grid_t;

  public:
    HadesLinearDensityLikelihood(LikelihoodInfo &info);
    virtual ~HadesLinearDensityLikelihood();

    virtual void setupDefaultParameters(MarkovState &state, int catalog);
    virtual void
    generateMockSpecific(ArrayRef const &parameters, MarkovState &state);
    virtual double logLikelihoodSpecific(ArrayRef const &parameters);
    virtual void gradientLikelihoodSpecific(
        ArrayRef const &parameters, ArrayRef &gradient_parameters);
    virtual void initializeLikelihood(MarkovState &state);
  };

}; // namespace LibLSS

#endif
