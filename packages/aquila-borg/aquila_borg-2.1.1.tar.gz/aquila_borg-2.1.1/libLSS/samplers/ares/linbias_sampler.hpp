/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/ares/linbias_sampler.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_LINEAR_BIAS_SAMPLER_HPP
#define __LIBLSS_LINEAR_BIAS_SAMPLER_HPP

#include <boost/multi_array.hpp>
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"

namespace LibLSS {

    class LinearBiasSampler: public MarkovSampler {
    protected:
        int Ncat;
        long Ntot, localNtot;
        boost::multi_array<SDouble *, 1> biases;
        MPI_Communication *comm;
    public:
        LinearBiasSampler(MPI_Communication *comm0) : comm(comm0) {}
        virtual ~LinearBiasSampler() {}
        
        virtual void initialize(MarkovState& state);
        virtual void restore(MarkovState& state);
        virtual void sample(MarkovState& state);
    };
    
}

#endif
