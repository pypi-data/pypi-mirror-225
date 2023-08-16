/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/altair/altair_meta_sampler.hpp
    Copyright (C) 2018-2020 Doogesh Kodi Ramanah <ramanah@iap.fr>
    Copyright (C) 2018-2021 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_ALTAIR_META_SAMPLER_HPP
#define __LIBLSS_ALTAIR_META_SAMPLER_HPP

#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/tools/fftw_allocator.hpp"
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/core/gridLikelihoodBase.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/physics/likelihoods/base.hpp"
#include "libLSS/hmclet/mass_burnin.hpp"
#include "libLSS/hmclet/dense_mass.hpp"
#include "libLSS/hmclet/mass_saver.hpp"
#include "libLSS/physics/cosmo.hpp"

namespace LibLSS {

  class AltairMetaSampler : public MarkovSampler {
  protected:
    typedef std::shared_ptr<GridDensityLikelihoodBase<3>> likelihood_t;
    typedef std::shared_ptr<BORGForwardModel> forward_t;
    int Ncat;
    MPI_Communication *comm;
    likelihood_t likelihood;
    forward_t model;

    typedef HMCLet::MassMatrixWithBurnin<HMCLet::DenseMassMatrix> mass_t;
    std::shared_ptr<mass_t> covariances;
    size_t numCosmoParams;
    long burnin_buffer;

    long Ntot, localNtot;
    double corner0, corner1, corner2;
    double L[3], delta[3], corner[3];
    CosmologicalParameters bound_min, bound_max;
    std::function<void()> limiter_cb, unlimiter_cb;
    double slice_factor;

  public:
    AltairMetaSampler(
        MPI_Communication *comm_, likelihood_t likelihood_, forward_t model_,
        CosmologicalParameters const &bound_min_,
        CosmologicalParameters const &bound_max_, double slice_factor_)
        : comm(comm_), likelihood(likelihood_), model(model_),
          bound_min(bound_min_), bound_max(bound_max_), slice_factor(slice_factor_) {}
    virtual ~AltairMetaSampler() {}

    void setLimiter(std::function<void()> cb);
    void setUnlimiter(std::function<void()> cb);

    void initialize(MarkovState &state) override;
    void restore(MarkovState &state) override;
    void sample(MarkovState &state) override;
  };

}; // namespace LibLSS

#endif
// ARES TAG: num_authors = 2
// ARES TAG: name(0) = Doogesh Kodi Ramanah
// ARES TAG: year(0) = 2018-2020
// ARES TAG: email(0) = ramanah@iap.fr
// ARES TAG: name(1) = Guilhem Lavaux
// ARES TAG: email(1) = guilhem.lavaux@iap.fr
// ARES TAG: year(1) = 2018-2021
