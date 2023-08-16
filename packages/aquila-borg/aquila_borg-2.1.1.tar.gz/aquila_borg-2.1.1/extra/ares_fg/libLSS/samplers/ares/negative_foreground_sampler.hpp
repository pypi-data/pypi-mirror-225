/*+
    ARES/HADES/BORG Package -- ./extra/ares_fg/libLSS/samplers/ares/negative_foreground_sampler.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_NEGATIVE_FOREGROUND_HPP
#define __LIBLSS_NEGATIVE_FOREGROUND_HPP

#include <boost/multi_array.hpp>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"

namespace LibLSS {

    class NegativeForegroundSampler: public MarkovSampler {
    protected:
        int Ncat;
        long Ntot, localNtot;
        int catalog, fg_id;
        long N0, N1, N2, localN0, startN0;
        RandomGen *rng;
        MPI_Communication *comm;
    public:
        NegativeForegroundSampler(MPI_Communication *comm, int catalog, int foreground_id);
        
        virtual void initialize(MarkovState& state);
        virtual void restore(MarkovState& state);
        virtual void sample(MarkovState& state);
    };
    
};

#endif
