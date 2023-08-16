/*+
    ARES/HADES/BORG Package -- ./src/ares_bundle.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef _ARES_BUNDLE_HPP
#define _ARES_BUNDLE_HPP
#include "libLSS/samplers/ares/powerspectrum_a_sampler.hpp"
#include "libLSS/samplers/ares/powerspectrum_b_sampler.hpp"
#include "libLSS/samplers/ares/powerspectrum_c_sampler.hpp"
#include "libLSS/samplers/ares/gibbs_messenger.hpp"
#include "libLSS/samplers/ares/linbias_sampler.hpp"
#include "libLSS/samplers/ares/synthetic_selection.hpp"
#ifdef ARES_FOREGROUND_SUPPORT
#include "libLSS/samplers/ares/negative_foreground_sampler.hpp"
#endif

namespace LibLSS {

    struct SamplerBundle {
        PowerSpectrumSampler_a spectrum_a;
        PowerSpectrumSampler_b spectrum_b;
        PowerSpectrumSampler_c spectrum_c;
        MessengerSampler sampler_t;
        MessengerSignalSampler sampler_s;
        CatalogProjectorSampler sampler_catalog_projector;
        LinearBiasSampler lb_sampler;
        BlockLoop foreground_block;
        SyntheticSelectionUpdater sel_updater;
        typedef std::list<MarkovSampler *> SamplerList;
        SamplerList foreground_samplers;

        SamplerBundle(MPI_Communication* comm)
            : spectrum_a(comm), spectrum_b(comm), spectrum_c(comm), sampler_t(comm),
              sampler_s(comm),
              sampler_catalog_projector(comm), lb_sampler(comm), foreground_block(1) {}

        void newForeground(int catalog, int fgmap) {
            Console::instance().print<LOG_VERBOSE>("Adding new foreground sampler");
#ifdef ARES_FOREGROUND_SUPPORT
            MarkovSampler *fg =
              new NegativeForegroundSampler(comm, c, fgmap);
            foreground_samplers.push_back(fg);
            foreground_block << (*fg);
#endif
        }

        ~SamplerBundle() {
            for (SamplerList::iterator i = foreground_samplers.begin(); i != foreground_samplers.end();
                ++i) {
                delete (*i);
            }
        }
    };

}

#endif
