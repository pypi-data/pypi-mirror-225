/*+
    ARES/HADES/BORG Package -- ./extra/hades/src/hades_bundle.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef _HADES_BUNDLE_HPP
#define _HADES_BUNDLE_HPP
#include "libLSS/samplers/hades/hades_linear_likelihood.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "hades_option.hpp"
#include "libLSS/samplers/ares/synthetic_selection.hpp"

#include "libLSS/physics/forward_model.hpp"
#include "libLSS/physics/hades_log.hpp"
#include "libLSS/physics/hades_pt.hpp"

#include "libLSS/samplers/rgen/density_sampler.hpp"

#ifdef HADES_SUPPORT_BORG
#  include "libLSS/borg_version.hpp"

#  include "libLSS/physics/forwards/all_models.hpp"
#  include "libLSS/physics/modified_ngp.hpp"
#  include "libLSS/physics/modified_ngp_smooth.hpp"

#  include "libLSS/samplers/borg/borg_poisson_likelihood.hpp"
#  include "libLSS/samplers/borg/borg_poisson_meta.hpp"

#  include "libLSS/samplers/generic/generic_sigma8.hpp"

#  ifdef HADES_SUPPORT_JULIA
#    include "libLSS/samplers/julia/julia_likelihood.hpp"
#  endif

#  include "borg_generic_bundle.hpp"

#  include "likelihood_info.hpp"

#endif

#include <boost/algorithm/string.hpp>
#include "generic_hades_bundle.hpp"

namespace LibLSS {

  typedef HadesBundle<HadesLinearDensityLikelihood> LinearBundle;

#ifdef HADES_SUPPORT_BORG
  typedef HadesBundle<BorgPoissonLikelihood> PoissonBorgBundle;

#  ifdef HADES_SUPPORT_JULIA
  struct JuliaBundle {
    JuliaDensitySampler borg_sampler;

    JuliaBundle(
        MPI_Communication *comm, std::string code_path, std::string module_name)
        : borg_sampler(comm, code_path, module_name) {}
  };
#  endif

#endif

  struct SamplerBundle {
    //BlockLoop foreground_block;
    typedef std::list<MarkovSampler *> SamplerList;
    std::function<MarkovSampler *(int, int)> foreground_sampler_generator;
    DummyPowerSpectrum dummy_ps;
    SamplerList foreground_samplers;
    MPI_Communication *comm;
    std::shared_ptr<GenericHadesBundle> hades_bundle;
    std::shared_ptr<GenericDensitySampler> density_mc;
    std::shared_ptr<MarkovSampler> borg_vobs, ap_sampler;
    std::unique_ptr<MarkovSampler> sigma8_sampler;
#ifdef HADES_SUPPORT_BORG
    std::shared_ptr<VirtualGenericBundle> borg_generic;
#  ifdef HADES_SUPPORT_JULIA
    std::unique_ptr<JuliaBundle> borg_julia;
#  endif
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

} // namespace LibLSS

#endif
