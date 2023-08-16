/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/ares/powerspectrum_b_sampler.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_POWERSPECTRUM_B_SAMPLER_HPP
#define __LIBLSS_POWERSPECTRUM_B_SAMPLER_HPP

#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"

namespace LibLSS {

    class PowerSpectrumSampler_b: public PowerSpectrumSampler_Coloring {
    protected:
        typedef boost::multi_array_ref< IArrayType::ArrayType::element, 1> FlatIntType;

        MFCalls::complex_type *tmp_fourier, *tmp_fourier_t;
        MFCalls::real_type *tmp_x, *tmp_t;
        MFCalls::plan_type analysis_plan;
        FlatIntType *flat_keys;
        int total_accepted, total_tried;

        ArrayType1d::ArrayType P0_array, P1_array;
        
        void base_init(MarkovState& state);
    public:
        PowerSpectrumSampler_b(MPI_Communication *comm);
        virtual ~PowerSpectrumSampler_b();

        virtual void restore(MarkovState& state);
        virtual void initialize(MarkovState& state);
        virtual void sample(MarkovState& state);    
    };

}

#endif
