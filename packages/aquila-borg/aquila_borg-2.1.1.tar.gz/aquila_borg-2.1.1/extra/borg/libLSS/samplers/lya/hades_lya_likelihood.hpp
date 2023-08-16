/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/lya/hades_lya_likelihood.hpp
    Copyright (C) 2020 Natalia Porqueres <n.porqueres@imperial.ac.uk>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

#ifndef __LIBLSS_BORG_LYALPHA_DENSITY_HPP
#define __LIBLSS_BORG_LYALPHA_DENSITY_HPP

#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/tools/fftw_allocator.hpp"
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/samplers/lya/base_lya_likelihood.hpp"
#include "libLSS/physics/likelihoods/base.hpp"

#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/data/lyman_alpha.hpp"
#include "libLSS/data/lyman_alpha_qso.hpp"
#include "libLSS/tools/mpi/ghost_planes.hpp"

namespace LibLSS {

  class BorgLyAlphaLikelihood : public HadesBaseDensityLyaLikelihood {
  public:
    typedef HadesBaseDensityLyaLikelihood super_t;
    typedef HadesBaseDensityLyaLikelihood::super_t grid_t;
    typedef LymanAlphaSurvey<BaseLymanAlphaDescriptor> LymanAlphaSurveyType;
  
  protected:
        bool need_init_ghosts;
        bool mock_data_generated;
		GhostPlanes<double, 2> ghosts;
		MarkovState *state;
		
  private: 
        void smooth(MarkovState& state, Uninit_FFTW_Real_Array::array_type& in, Uninit_FFTW_Real_Array::array_type& out, double sigmaKernel);
        void smooth(MarkovState* state, Uninit_FFTW_Real_Array::array_type& in, Uninit_FFTW_Real_Array::array_type& out, double sigmaKernel);
        void smooth_gradient(MarkovState* state, Uninit_FFTW_Real_Array::array_type& in, Uninit_FFTW_Real_Array::array_type& out, double sigmaKernel);
        
  public:
    BorgLyAlphaLikelihood(LikelihoodInfo &info);
    virtual ~BorgLyAlphaLikelihood();
    
    virtual void updateMetaParameters(MarkovState &state);
	virtual void setupDefaultParameters(MarkovState &state, int catalog);
	
    virtual void initializeLikelihood(MarkovState &state);
   	
    virtual void
    generateMockSpecific(ArrayRef const &parameters, MarkovState &state);

    virtual double logLikelihoodSpecific(ArrayRef const &parameters);
    virtual void gradientLikelihoodSpecific(
        ArrayRef const &parameters, ArrayRef &gradient_parameters);
    
    void initialize_ghosts(LymanAlphaSurveyType &survey);
    void updateBiasParameters(int catalog, BiasArray const &params); 
    void sampleMeta(MarkovState &state);
  };

}; // namespace LibLSS

#endif

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Natalia Porqueres
// ARES TAG: email(0) = n.porqueres@imperial.ac.uk
// ARES TAG: year(0) = 2020

