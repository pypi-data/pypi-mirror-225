/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/src/julia_bundle.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef _HADES_JULIA_BUNDLE_HPP
#define _HADES_JULIA_BUNDLE_HPP
#include "libLSS/samplers/hades/hades_linear_likelihood.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "libLSS/samplers/ares/synthetic_selection.hpp"
#include "libLSS/samplers/rgen/density_sampler.hpp"

#include "libLSS/physics/forward_model.hpp"
#include "libLSS/physics/hades_log.hpp"
#include "libLSS/physics/hades_pt.hpp"
#include "hades_option.hpp"

#include "libLSS/borg_version.hpp"

#include "libLSS/physics/modified_ngp.hpp"
#include "libLSS/physics/modified_ngp_smooth.hpp"

#include "libLSS/physics/forwards/borg_lpt.hpp"
#include "libLSS/physics/forwards/borg_2lpt.hpp"
#include "libLSS/physics/forwards/borg_multi_pm.hpp"

#include "libLSS/samplers/generic/generic_sigma8.hpp"
#include "libLSS/samplers/julia/julia_likelihood.hpp"

#include <boost/algorithm/string.hpp>

namespace LibLSS {

  namespace {

    HMCOption::IntegratorScheme get_Scheme(const std::string &s) {
      std::string scheme = boost::to_upper_copy<std::string>(s);
      using namespace HMCOption;

      if (scheme == "SI_2A" || scheme == "LEAP_FROG") {
        return SI_2A;
      } else if (scheme == "SI_2B") {
        return SI_2B;
      } else if (scheme == "SI_2C") {
        return SI_2C;
      } else if (scheme == "SI_3A") {
        return SI_3A;
      } else if (scheme == "SI_4B") {
        return SI_4B;
      } else if (scheme == "SI_4C") {
        return SI_4C;
      } else if (scheme == "SI_4D") {
        return SI_4D;
      } else if (scheme == "SI_6A") {
        return SI_6A;
      } else {
        error_helper<ErrorBadState>(
            boost::format("Invalid integration scheme %s") % scheme);
      }
    }

  } // namespace

  class DummyPowerSpectrum : public PowerSpectrumSampler_Base {
  public:
    DummyPowerSpectrum(MPI_Communication *comm)
        : PowerSpectrumSampler_Base(comm) {}

    virtual void initialize(MarkovState &state) { initialize_base(state); }
    virtual void restore(MarkovState &state) { restore_base(state); }

    virtual void sample(MarkovState &state) {}
  };

  struct SamplerBundle {
    //BlockLoop foreground_block;
    typedef std::list<MarkovSampler *> SamplerList;
    std::function<MarkovSampler *(int, int)> foreground_sampler_generator;
    DummyPowerSpectrum dummy_ps;
    SamplerList foreground_samplers;
    MPI_Communication *comm;
    std::shared_ptr<GenericDensitySampler> density_mc;
    std::shared_ptr<MarkovSampler> bias;
    std::shared_ptr<JuliaDensityLikelihood> julia_likelihood;
    bool delegate_ic_to_julia;

    BlockLoop foreground_block;
    SyntheticSelectionUpdater sel_updater;

    SamplerBundle(MPI_Communication *comm)
        : comm(comm), dummy_ps(comm), delegate_ic_to_julia(false) {}

    void newForeground(int catalog, int fgmap) {
      Console::instance().print<LOG_VERBOSE>("Adding new foreground sampler");

      MarkovSampler *fgsample = foreground_sampler_generator(catalog, fgmap);
      if (fgsample != 0) {
        foreground_samplers.push_back(fgsample);
        foreground_block << (*fgsample);
      }
    }

    ~SamplerBundle() {
      Console::instance().print<LOG_VERBOSE>("Begin destroying the bundle");
      for (SamplerList::iterator i = foreground_samplers.begin();
           i != foreground_samplers.end(); ++i) {
        delete (*i);
      }
      Console::instance().print<LOG_VERBOSE>("Done destroying the bundle");
    }
  };

} // namespace LibLSS

#endif
