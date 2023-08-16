/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/generic/generic_sigma8_second.hpp
    Copyright (C) 2014-2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2018 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef _LIBLSS_BORG_SIGMA8_SECOND_SAMPLER_HPP
#  define _LIBLSS_BORG_SIGMA8_SECOND_SAMPLER_HPP

#  include <memory>
#  include "libLSS/samplers/core/markov.hpp"
#  include "libLSS/tools/mpi_fftw_helper.hpp"
#  include "libLSS/samplers/core/gridLikelihoodBase.hpp"
#  include "libLSS/physics/likelihoods/base.hpp"

namespace LibLSS {

  class GenericSigma8SecondVariantSampler : public MarkovSampler {
  public:
    typedef FFTW_Manager_3d<double> DFT_Manager;
    typedef std::shared_ptr<GridDensityLikelihoodBase<3>> Likelihood_t;

  protected:
    MPI_Communication *comm;
    double L0, L1, L2, Volume;
    size_t N0, N1, N2;
    Likelihood_t likelihood;
    std::unique_ptr<DFT_Manager> mgr;
    double step_ansatz, sigma8_min, sigma8_max;
    bool use_double;

  public:
    GenericSigma8SecondVariantSampler(
        MPI_Communication *comm_, Likelihood_t likelihood_,
        LikelihoodInfo info = LikelihoodInfo());
    virtual ~GenericSigma8SecondVariantSampler();

    virtual void initialize(MarkovState &state);
    virtual void restore(MarkovState &state);
    virtual void sample(MarkovState &state);
  };

} // namespace LibLSS

#endif
// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2014-2018
// ARES TAG: name(1) = Jens Jasche
// ARES TAG: email(1) = jens.jasche@fysik.su.se
// ARES TAG: year(1) = 2009-2018
