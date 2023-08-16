/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/core/markov.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_MARKOV_SAMPLER_HPP
#define __LIBLSS_MARKOV_SAMPLER_HPP

#include "libLSS/mcmc/global_state.hpp"

namespace LibLSS {

    class MarkovSampler {
    protected:
        virtual void initialize(MarkovState& state) = 0;
        virtual void restore(MarkovState& state) = 0;
    private:
        bool yet_init;
    public:
        MarkovSampler() : yet_init(false) {}
        virtual ~MarkovSampler() {}

        virtual void sample(MarkovState& state) = 0;
        
        void init_markov(MarkovState& state) {
            if (!yet_init) {
                yet_init = true;
                initialize(state);
            }
        }

        void restore_markov(MarkovState& state) {
            if (!yet_init) {
                yet_init = true;
                restore(state);
            }
        }

        
    };

}

#endif
