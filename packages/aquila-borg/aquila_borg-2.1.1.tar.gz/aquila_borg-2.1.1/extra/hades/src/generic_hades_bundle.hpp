#ifndef __TOOLS_GENERIC_HADES_BUNDLE_HPP
#define __TOOLS_GENERIC_HADES_BUNDLE_HPP

#include <string>

#include "libLSS/samplers/hades/hades_linear_likelihood.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"

#include "libLSS/physics/forward_model.hpp"

#include "libLSS/samplers/rgen/density_sampler.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"

#include "likelihood_info.hpp"

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
      } else if (scheme == "CG_89") {
        return CG_89;
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

  struct GenericHadesBundle {
    std::shared_ptr<HadesBaseDensityLikelihood> likelihood;
    std::shared_ptr<MarkovSampler> hades_meta;

    virtual ~GenericHadesBundle() {}
  };

  template <typename DensityLikelihood>
  struct HadesBundle : public GenericHadesBundle {
    typedef DensityLikelihood likelihood_t;
    typedef typename DensityLikelihood::grid_t grid_t;

    std::shared_ptr<DensityLikelihood> hades_likelihood;

    typedef typename grid_t::GridSizes GridSizes;
    typedef typename grid_t::GridLengths GridLengths;

    HadesBundle(LikelihoodInfo &info)
        : hades_likelihood(std::make_shared<likelihood_t>(info)) {
      this->hades_meta = std::make_shared<HadesMetaSampler>(
          Likelihood::getMPI(info), hades_likelihood);
      this->likelihood = hades_likelihood;
    }

    virtual ~HadesBundle() {}
  };

}

#endif
