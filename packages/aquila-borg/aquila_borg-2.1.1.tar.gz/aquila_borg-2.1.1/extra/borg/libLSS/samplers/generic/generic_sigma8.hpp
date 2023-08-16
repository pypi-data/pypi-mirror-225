/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/generic/generic_sigma8.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef _LIBLSS_BORG_SIGMA8_SAMPLER_HPP
#define _LIBLSS_BORG_SIGMA8_SAMPLER_HPP

#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"

namespace LibLSS {

  class GenericSigma8Sampler : public MarkovSampler {
  public:
    typedef FFTW_Manager_3d<double> DFT_Manager;

  protected:
    int Ncat;
    MPI_Communication *comm;
    double L0, L1, L2, Volume;
    size_t N0, N1, N2;

  public:
    GenericSigma8Sampler(MPI_Communication *comm_)
        : MarkovSampler(), comm(comm_) {}
    virtual ~GenericSigma8Sampler();

    virtual void initialize(MarkovState &state);
    virtual void restore(MarkovState &state);
    virtual void sample(MarkovState &state);
  };

} // namespace LibLSS

#endif
