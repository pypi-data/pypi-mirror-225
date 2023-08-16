/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/samplers/rgen/frozen/frozen_phase_density_sampler.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_FROZEN_DENSITY_HPP
#define __LIBLSS_FROZEN_DENSITY_HPP

#include <boost/optional.hpp>
#include <functional>
#include <memory>
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/tools/fftw_allocator.hpp"
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/tools/symplectic_integrator.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/samplers/core/gridLikelihoodBase.hpp"
#include "libLSS/samplers/rgen/density_sampler.hpp"

namespace LibLSS {

  class FrozenPhaseDensitySampler : public GenericDensitySampler {
  public:
    typedef ArrayType::ArrayType Array;
    typedef ArrayType::RefArrayType ArrayRef;
    typedef CArrayType::ArrayType CArray;
    typedef CArrayType::RefArrayType CArrayRef;
    typedef IArrayType::ArrayType IArray;

    typedef std::shared_ptr<GridDensityLikelihoodBase<3>> Likelihood_t;

  protected:
    typedef FFTW_Manager_3d<double> DFT_Manager;

    MPI_Communication *comm;
    std::shared_ptr<DFT_Manager> base_mgr;
    Likelihood_t likelihood;

    FCalls::plan_type analysis_plan, synthesis_plan;
    size_t N0, N1, N2;
    size_t startN0, localN0, endN0;
    double L0, L1, L2, volume, volNorm;

    ArrayType *x_field, *s_field;
    CArrayType *x_hat_field, *s_hat_field;

    boost::optional<std::string> phaseFilename;
    std::string dataName;

    auto sqrt_Pk(MarkovState &state);

  public:
    FrozenPhaseDensitySampler(MPI_Communication *comm, Likelihood_t likelihood);
    virtual ~FrozenPhaseDensitySampler();

    virtual void generateMockData(MarkovState &state);
    void generateRandomField(MarkovState &state);

    void
    setPhaseFile(std::string const &filename, std::string const &objectName) {
      phaseFilename = filename;
      dataName = objectName;
    }

    void restore(MarkovState &state);
    void initialize(MarkovState &state);

    virtual void sample(MarkovState &state);
  };
}; // namespace LibLSS

#endif
