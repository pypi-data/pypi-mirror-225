/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/ares/powerspectrum_c_sampler.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_POWERSPECTRUM_C_SAMPLER_HPP
#define __LIBLSS_POWERSPECTRUM_C_SAMPLER_HPP

#include <iostream>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"

namespace LibLSS {

    class PowerSpectrumSampler_c: public PowerSpectrumSampler_Coloring {
    protected:
        typedef boost::multi_array_ref< IArrayType::ArrayType::element, 1> FlatIntType;

        long localNtot;
        int total_accepted, total_tried;

        bool init_sampler;
        IArrayType1d *counter_evaluations;
        ArrayType1d *sigma_init;

        void base_init(MarkovState& state);
        
        double log_likelihood(MarkovState& state, int k, double P_trial);
        
    public:
        PowerSpectrumSampler_c(MPI_Communication *comm);
        virtual ~PowerSpectrumSampler_c();

        virtual void restore(MarkovState& state);
        virtual void initialize(MarkovState& state);
        virtual void sample(MarkovState& state);    
    };

}

#endif
