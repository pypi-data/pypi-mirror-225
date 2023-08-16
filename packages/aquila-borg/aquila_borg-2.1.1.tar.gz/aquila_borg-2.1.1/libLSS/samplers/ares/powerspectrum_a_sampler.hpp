/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/ares/powerspectrum_a_sampler.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_POWERSPECTRUM_A_SAMPLER_HPP
#define __LIBLSS_POWERSPECTRUM_A_SAMPLER_HPP

#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"

namespace LibLSS {

    class PowerSpectrumSampler_a: public PowerSpectrumSampler_Base {
    protected:
        typedef boost::multi_array_ref< IArrayType::ArrayType::element, 1> FlatIntType;

        FCalls::complex_type *tmp_fourier;
        FCalls::plan_type analysis_plan;
        FlatIntType *flat_keys;
        MFCalls::real_type *tmp_s;
        
        void base_init();
    public:
        PowerSpectrumSampler_a(MPI_Communication *comm);
        virtual ~PowerSpectrumSampler_a();

        virtual void restore(MarkovState& state);
        virtual void initialize(MarkovState& state);
        virtual void sample(MarkovState& state);    
    };

}

#endif
