/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/borg/borg_poisson_meta.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_BORG_POISSON_META_SAMPLER_HPP
#define __LIBLSS_BORG_POISSON_META_SAMPLER_HPP

#include <boost/multi_array.hpp>
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/samplers/ares/ares_bias.hpp"

namespace LibLSS {
  class BorgPoissonVobsSampler : public MarkovSampler {
  protected:
    int Ncat;
    long Ntot, localNtot;
    MPI_Communication *comm;
    std::shared_ptr<BORGForwardModel> model;

    double
    computeLogLikelihood(MarkovState &state, double v0, double v1, double v2);

  public:
    BorgPoissonVobsSampler(MPI_Communication *comm0) : comm(comm0) {}
    virtual ~BorgPoissonVobsSampler() {}

    virtual void initialize(MarkovState &state);
    virtual void restore(MarkovState &state);
    virtual void sample(MarkovState &state);
  };

  class BorgPoissonNmeanSampler : public MarkovSampler {
  protected:
    int Ncat;
    long Ntot, localNtot;
    MPI_Communication *comm;

    double computeLogLikelihood(
        ArrayType::ArrayType &s_array, ArrayType::ArrayType &data_array,
        SelArrayType::ArrayType &selection, double nmean, double b,
        double rho_g, double eps_g, double temp);

  public:
    BorgPoissonNmeanSampler(MPI_Communication *comm0) : comm(comm0) {}
    virtual ~BorgPoissonNmeanSampler() {}

    virtual void initialize(MarkovState &state);
    virtual void restore(MarkovState &state);
    virtual void sample(MarkovState &state);
  };

  class BorgPoissonBiasSampler : public MarkovSampler {
  protected:
    int Ncat;
    long Ntot, localNtot;
    MPI_Communication *comm;

    double computeLogLikelihood(
        ArrayType::ArrayType &s_array, ArrayType::ArrayType &data_array,
        SelArrayType::ArrayType &selection, double nmean, double b,
        double rho_g, double eps_g, double temp);

  public:
    BorgPoissonBiasSampler(MPI_Communication *comm0) : comm(comm0) {}
    virtual ~BorgPoissonBiasSampler() {}

    virtual void initialize(MarkovState &state);
    virtual void restore(MarkovState &state);
    virtual void sample(MarkovState &state);
  };

  namespace BORG {
    using ARES::ensure_bias_size;

    inline void ensure_poisson_bias(MarkovState &s, int c) {
      ensure_bias_size(s, c, boost::array<double, 3>{1, 1.5, 0.4});
    }

    inline void extract_poisson_bias(
        MarkovState &s, int c, double *&alpha, double *&rho, double *&epsilon) {
      using boost::format;
      ArrayType1d::ArrayType &a =
          (*s.get<ArrayType1d>(format("galaxy_bias_%d") % c)->array);

      alpha = &a[0];
      epsilon = &a[2];
      rho = &a[1];
    }

  } // namespace BORG

}; // namespace LibLSS

#endif
