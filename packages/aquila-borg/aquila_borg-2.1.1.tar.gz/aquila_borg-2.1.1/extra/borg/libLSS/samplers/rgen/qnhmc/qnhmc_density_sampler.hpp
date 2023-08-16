/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/rgen/qnhmc/qnhmc_density_sampler.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_QNHMC_DENSITY_HPP
#define __LIBLSS_QNHMC_DENSITY_HPP

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
#include "libLSS/tools/optimization/array_helper.hpp"
#include "libLSS/tools/optimization/bfgs.hpp"
#include "libLSS/samplers/rgen/density_sampler.hpp"

namespace LibLSS {

  namespace QNHMCOption {
    using namespace SymplecticOption;
  };

  class QNHMCDensitySampler : public GenericDensitySampler {
  public:
    typedef ArrayType::ArrayType Array;
    typedef ArrayType::RefArrayType ArrayRef;
    typedef CArrayType::ArrayType CArray;
    typedef CArrayType::RefArrayType CArrayRef;
    typedef IArrayType::ArrayType IArray;

    typedef double HamiltonianType;

    typedef std::shared_ptr<GridDensityLikelihoodBase<3>> Likelihood_t;

  protected:
    typedef boost::multi_array_ref<IArrayType::ArrayType::element, 1>
        FlatIntType;
    typedef FFTW_Manager_3d<double> DFT_Manager;

    MPI_Communication *comm;

    std::shared_ptr<DFT_Manager> base_mgr;
    Likelihood_t likelihood;

    long fourierLocalSize;
    FCalls::plan_type analysis_plan, synthesis_plan;
    size_t N0, N1, N2;
    size_t startN0, localN0, endN0;
    double L0, L1, L2, volume, volNorm;
    int Ncat;
    SLong *attempt_field, *accept_field;
    ScalarStateElement<int> *bad_sample;

    FFTW_Allocator<double> allocator_real;
    FFTW_Allocator<std::complex<double>> allocator_complex;

    ArrayType *s_field;
    IArrayType *adjust_field;
    CArrayType *momentum_field, *s_hat_field;

    int maxTime, lastTime;
    double lastEpsilon, maxEpsilon;
    SymplecticIntegrators symp;

    typedef Optimization::BoostArrayAllocator<std::complex<double>, 3>
        allocator3;
    Optimization::lbfgs<allocator3> B, C;

    void doSympInt(MarkovState &state, CArrayRef &s_hat);
    HamiltonianType computeHamiltonian(
        MarkovState &state, CArrayRef const &s_hat, bool final_call);
    HamiltonianType
    computeHamiltonian_Prior(MarkovState &state, CArrayRef const &s_hat);
    HamiltonianType computeHamiltonian_Kinetic();
    HamiltonianType computeHamiltonian_Likelihood(
        MarkovState &state, CArrayRef const &s_hat, bool final_call);
    void initializeMomenta(MarkovState &state);
    void computeGradientPsi(
        MarkovState &state, CArrayRef const &s, CArrayRef &grad_array);
    void computeGradientPsi_Prior(
        MarkovState &state, CArrayRef const &s, CArrayRef &grad_array);

    void updateMass(MarkovState &state);
    void Hermiticity_fixup(CArrayRef &a);
    void Hermiticity_fixup_plane(int Nplane, CArrayType::ArrayType &a);

    void computeGradientPsi_Likelihood(
        MarkovState &state, CArrayRef const &s, CArrayRef &grad_array,
        bool accumulate);

    typedef boost::multi_array<double, 2> IntegratorCoefficients;
    typedef QNHMCOption::IntegratorScheme IntegratorScheme;

    IntegratorScheme current_scheme;

  public:
    QNHMCDensitySampler(MPI_Communication *comm, Likelihood_t likelihood);
    virtual ~QNHMCDensitySampler();

    virtual void generateMockData(MarkovState &state);

    void setIntegratorScheme(IntegratorScheme scheme);

    double computeHamiltonian(MarkovState &state, bool gradient_next = false);

    void restore(MarkovState &state);
    void initialize(MarkovState &state);

    virtual void sample(MarkovState &state);

    void setMaxEpsilon(double eps) { this->maxEpsilon = eps; }
    void setMaxTimeSteps(int Ntime) { this->maxTime = Ntime; }
  };

}; // namespace LibLSS

#endif
