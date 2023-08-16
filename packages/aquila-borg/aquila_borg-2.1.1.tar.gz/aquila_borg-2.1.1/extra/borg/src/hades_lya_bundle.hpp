/*+
    ARES/HADES/BORG Package -- ./extra/borg/src/hades_lya_bundle.hpp
    Copyright (C) 2020 Natalia Porqueres <n.porqueres@imperial.ac.uk>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef _HADES_LYA_BUNDLE_HPP
#define _HADES_LYA_BUNDLE_HPP

#include "libLSS/samplers/hades/hades_linear_likelihood.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "hades_option.hpp"
#include "libLSS/samplers/ares/synthetic_selection.hpp"

#include "libLSS/samplers/ares/gibbs_messenger.hpp"
#include "libLSS/samplers/ares/linbias_sampler.hpp"

#include "libLSS/samplers/rgen/density_sampler.hpp"

#include "libLSS/samplers/lya_rsd_qlpt/hades_lya_likelihood_rsd.hpp"
#include "libLSS/samplers/lya/hades_lya_likelihood.hpp"

#include "libLSS/borg_version.hpp"



#include "libLSS/physics/modified_ngp.hpp"
#include "libLSS/physics/modified_ngp_smooth.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/physics/hades_log.hpp"
#include "libLSS/physics/forwards/borg_qlpt.hpp"
#include "libLSS/physics/forwards/borg_qlpt_rsd.hpp"
#include "libLSS/physics/forwards/borg_lpt.hpp"
#include "libLSS/physics/forwards/borg_2lpt.hpp"
#include "generic_hades_lya_bundle.hpp"
#include "libLSS/samplers/generic/generic_sigma8.hpp"
#include "borg_generic_bundle.hpp"
#include "likelihood_info.hpp"

namespace LibLSS {

    
  typedef HadesBundle<BorgLyAlphaLikelihood> LyAlphaBorgBundle;
  typedef HadesBundle<BorgLyAlphaRsdLikelihood> LyAlphaRsdBorgBundle;

	struct SamplerBundle {
    //BlockLoop foreground_block;
    typedef std::list<MarkovSampler *> SamplerList;
    std::function<MarkovSampler *(int, int)> foreground_sampler_generator;
    DummyPowerSpectrum dummy_ps;
    SamplerList foreground_samplers;
    MPI_Communication *comm;
    std::shared_ptr<GenericHadesBundle> hades_lya_bundle;
    std::shared_ptr<GenericHadesBundle> hades_lya_rsd_bundle;
    std::shared_ptr<GenericDensitySampler> density_mc;
    std::shared_ptr<MarkovSampler> borg_vobs;
    std::unique_ptr<MarkovSampler> sigma8_sampler;
#ifdef HADES_SUPPORT_BORG
    std::shared_ptr<VirtualGenericBundle> borg_generic;
#endif
    BlockLoop foreground_block;
    SyntheticSelectionUpdater sel_updater;

    SamplerBundle(MPI_Communication *comm) : comm(comm), dummy_ps(comm) {}

    void newForeground(int catalog, int fgmap) {
      Console::instance().print<LOG_VERBOSE>("Adding new foreground sampler");

#ifdef HADES_SUPPORT_BORG
      MarkovSampler *fgsample = foreground_sampler_generator(catalog, fgmap);
      if (fgsample != 0) {
        foreground_samplers.push_back(fgsample);
        foreground_block << (*fgsample);
      }

#endif
    }
    ~SamplerBundle() {
      LIBLSS_AUTO_CONTEXT(LOG_VERBOSE, ctx);
      for (SamplerList::iterator i = foreground_samplers.begin();
           i != foreground_samplers.end(); ++i) {
        delete (*i);
      }

	}
    };
}

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Natalia Porqueres
// ARES TAG: email(0) = n.porqueres@imperial.ac.uk
// ARES TAG: year(0) = 2020

