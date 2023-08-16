/*+
    ARES/HADES/BORG Package -- ./extra/python/src/python_bundle.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef _HADES_PYTHON_BUNDLE_HPP
#  define _HADES_PYTHON_BUNDLE_HPP
#  include "libLSS/samplers/core/powerspec_tools.hpp"
#  include "libLSS/samplers/ares/synthetic_selection.hpp"
#  include "libLSS/samplers/rgen/density_sampler.hpp"
#  include "libLSS/physics/forward_model.hpp"
#  include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#  include "libLSS/samplers/core/main_loop.hpp"

#  include <boost/algorithm/string.hpp>
#  include <pybind11/pybind11.h>

#define ARES_EXTRA_CATCH_CLAUSE \
  catch (pybind11::error_already_set const& e) { \
    Console::instance().print<LOG_ERROR>(LibLSS::tokenize(e.what(),"\n")); \
  }

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
    //    std::shared_ptr<JuliaDensityLikelihood> julia_likelihood;
    bool delegate_ic_to_python;
    std::shared_ptr<LibLSS::GridDensityLikelihoodBase<3>> python_likelihood;

    BlockLoop foreground_block;
    SyntheticSelectionUpdater sel_updater;

    SamplerBundle(MPI_Communication *comm)
        : comm(comm), dummy_ps(comm), delegate_ic_to_python(false) {}

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
