/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/ares/synthetic_selection.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_SYNTHETIC_SELECTION_UPDATER_HPP
#define __LIBLSS_SYNTHETIC_SELECTION_UPDATER_HPP

#include <boost/multi_array.hpp>
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"

namespace LibLSS {

    class SyntheticSelectionUpdater: public MarkovSampler {
    protected:
        int Ncat;
        long Ntot, localNtot;
    public:

        virtual void initialize(MarkovState& state);
        virtual void restore(MarkovState& state);
        virtual void sample(MarkovState& state);

    };
    
};

#endif
