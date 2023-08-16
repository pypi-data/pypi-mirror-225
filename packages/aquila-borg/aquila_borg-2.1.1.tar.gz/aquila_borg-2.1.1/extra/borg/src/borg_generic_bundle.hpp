/*+
    ARES/HADES/BORG Package -- ./extra/borg/src/borg_generic_bundle.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __BORG_GENERIC_BUNDLE_HPP
#define __BORG_GENERIC_BUNDLE_HPP

#include <type_traits>
#include <functional>
#include "libLSS/samplers/generic/generic_hmc_likelihood.hpp"
#include "libLSS/samplers/core/main_loop.hpp"
#include "libLSS/physics/likelihoods/base.hpp"

#include "libLSS/physics/adapt_classic_to_nb.hpp"
#include "libLSS/physics/adapt_classic_to_gauss.hpp"
#include "libLSS/physics/bias/double_power_law.hpp"
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/physics/bias/broken_power_law.hpp"
#include "libLSS/physics/bias/broken_power_law_sigmoid.hpp"
#include "libLSS/physics/likelihoods/gaussian.hpp"
#include "libLSS/physics/likelihoods/voxel_poisson.hpp"
#include "libLSS/physics/likelihoods/robust_poisson.hpp"
#include "libLSS/physics/bias/eft_bias.hpp"
#include "libLSS/physics/bias/linear_bias.hpp"
#include "libLSS/physics/bias/many_power.hpp"
#include "libLSS/physics/bias/downgrader.hpp"
#include "libLSS/physics/likelihoods/base.hpp"

namespace LibLSS {

  class VirtualGenericBundle {
  public:
    virtual ~VirtualGenericBundle() {}
  };

  template <
      typename Likelihood, unsigned int NumPars, bool bias0Anchored,
      int current = int(NumPars) - 1>
  class GenericAllBias : public MarkovSampler {
  public:
    typedef GenericAllBias<Likelihood, NumPars, bias0Anchored, current - 1>
        nextSampler;
    typedef GenericMetaSampler<Likelihood, BiasParamSelector<current>>
        thisSampler;

    thisSampler sampler;
    nextSampler next;
    bool blocked;

    template <typename PropertyTree>
    GenericAllBias(
        MPI_Communication *mpi, std::shared_ptr<Likelihood> &likelihood,
        PropertyTree &&ptree)
        : sampler(mpi, likelihood), next(mpi, likelihood, ptree) {
      blocked = ptree.template get<bool>(
          str(boost::format("bias_%d_sampler_generic_blocked") % current),
          false);
    }

    virtual void initialize(MarkovState &state) {
      next.init_markov(state);
      sampler.init_markov(state);
    }

    virtual void restore(MarkovState &state) {
      next.restore_markov(state);
      sampler.restore_markov(state);
    }

    virtual void sample(MarkovState &state) {
      next.sample(state);
      if (!blocked)
        sampler.sample(state);
    }
  };

  template <typename Likelihood, bool anchor, int current>
  class GenericAllBias<Likelihood, 0, anchor, current> : public MarkovSampler {
  public:
    template <typename PropertyTree>
    GenericAllBias(
        MPI_Communication *mpi, std::shared_ptr<Likelihood> &likelihood,
        PropertyTree &&ptree) {}
    virtual void initialize(MarkovState &state) {}
    virtual void restore(MarkovState &state) {}
    virtual void sample(MarkovState &state) {}
  };

  template <typename Likelihood, unsigned int NumPars>
  class GenericAllBias<Likelihood, NumPars, true, 0> : public MarkovSampler {
  public:
    template <typename PropertyTree>
    GenericAllBias(
        MPI_Communication *mpi, std::shared_ptr<Likelihood> &likelihood,
        PropertyTree &&ptree) {}
    virtual void initialize(MarkovState &state) {}
    virtual void restore(MarkovState &state) {}
    virtual void sample(MarkovState &state) {}
  };

  template <typename Likelihood, unsigned int NumPars>
  class GenericAllBias<Likelihood, NumPars, false, 0> : public MarkovSampler {
  public:
    typedef GenericMetaSampler<Likelihood, BiasParamSelector<0>> thisSampler;

    thisSampler sampler;
    bool blocked;

    template <typename PropertyTree>
    GenericAllBias(
        MPI_Communication *mpi, std::shared_ptr<Likelihood> &likelihood,
        PropertyTree &&ptree)
        : sampler(mpi, likelihood) {
      blocked =
          ptree.template get<bool>("bias_0_sampler_generic_blocked", false);
    }

    virtual void initialize(MarkovState &state) { sampler.init_markov(state); }
    virtual void restore(MarkovState &state) { sampler.restore_markov(state); }
    virtual void sample(MarkovState &state) {
      if (!blocked)
        sampler.sample(state);
    }
  };

  template <typename Bias, typename Likelihood, bool bias0Anchored>
  class GenericBundle : virtual public VirtualGenericBundle {
  public:
    typedef Bias bias_t;
    typedef Likelihood voxel_likelihood;

    typedef GenericHMCLikelihood<bias_t, voxel_likelihood> baseLikelihood;
    typedef GenericMetaSampler<
        baseLikelihood, LibLSS::NmeanSelector, !bias_t::NmeanIsBias>
        nmeanSampler;
    typedef GenericAllBias<baseLikelihood, Bias::numParams, bias0Anchored>
        biasSampler;
    typedef GenericVobsSampler<baseLikelihood> vobsSampler;

    // HMC is destroyed by the master bundle. This
    // will have to change.
    MPI_Communication *comm;
    std::shared_ptr<baseLikelihood> likelihood;
    std::shared_ptr<nmeanSampler> nmean;
    std::shared_ptr<biasSampler> bias;
    std::shared_ptr<vobsSampler> vobs;

    std::map<int, MarkovSampler *> catalog_fg_sampler;

    template <typename PropertyTree>
    GenericBundle(PropertyTree &&ptree, LikelihoodInfo &info)
        : comm(LibLSS::Likelihood::getMPI(info)),
          likelihood(std::make_shared<baseLikelihood>(info)),
          nmean(std::make_shared<nmeanSampler>(comm, likelihood)),
          bias(std::make_shared<biasSampler>(comm, likelihood, ptree)),
          vobs(std::make_shared<vobsSampler>(comm, likelihood)) {}
  };

  namespace {
    template <typename Bias, typename Likelihood, bool bias0Anchored>
    MarkovSampler *add_generic_foreground(
        MPI_Communication *comm,
        std::shared_ptr<GenericBundle<Bias, Likelihood, bias0Anchored>> &bundle,
        int catalog, int fgmap) {
      typedef typename GenericBundle<
          Bias, Likelihood, bias0Anchored>::baseLikelihood bundle_t;
      typedef GenericForegroundSampler<bundle_t> fg_t;

      fg_t *ret = 0, *fgsampler;
      auto iter = bundle->catalog_fg_sampler.find(catalog);
      // We are creating only one foreground sampler per catalog to optimize
      // some of the computations.
      if (iter == bundle->catalog_fg_sampler.end()) {
        bundle->catalog_fg_sampler[catalog] = ret = fgsampler =
            new fg_t(comm, bundle->likelihood, catalog);
      } else {
        fgsampler = dynamic_cast<fg_t *>(iter->second);
      }

      fgsampler->addMap(fgmap);
      return ret;
    }

    template <
        typename Bias, typename Likelihood, typename PropertyTree,
        bool bias0Anchored = false>
    std::shared_ptr<VirtualGenericBundle> create_generic_bundle(
        PropertyTree &&ptree,
        std::shared_ptr<GridDensityLikelihoodBase<3>> &likelihood,
        std::shared_ptr<MarkovSampler> &nmean,
        std::shared_ptr<MarkovSampler> &bias,
        std::shared_ptr<MarkovSampler> &vobs,
        std::function<MarkovSampler *(int, int)> &generator,
        LikelihoodInfo &info) {
      auto bundle =
          std::make_shared<GenericBundle<Bias, Likelihood, bias0Anchored>>(
              ptree, info);
      auto mpi = LibLSS::Likelihood::getMPI(info);

      likelihood = bundle->likelihood;
      nmean = bundle->nmean;
      bias = bundle->bias;
      vobs = bundle->vobs;
      generator = std::bind(
          &add_generic_foreground<Bias, Likelihood, bias0Anchored>, mpi, bundle,
          std::placeholders::_1, std::placeholders::_2);
      return bundle;
    }

  } // namespace

} // namespace LibLSS

#endif
