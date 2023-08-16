/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HMC_DENSITY_HPP
#define __LIBLSS_HMC_DENSITY_HPP

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
#include "libLSS/tools/hermiticity_fixup.hpp"

namespace LibLSS {

  namespace HMC_Details {

    template <typename Function>
    void accumulateHamiltonian(
        int n0, int n1, int n2, const IArrayType::ArrayType &adjust_array,
        const Function &f, double &E) {
      E += f(n0, n1, n2, adjust_array);
    }

  } // namespace HMC_Details

  namespace HMCOption {
    using namespace SymplecticOption;
  };

  class HMCDensitySampler : public GenericDensitySampler {
  public:
    typedef ArrayType::ArrayType Array;
    typedef ArrayType::RefArrayType ArrayRef;
    typedef CArrayType::ArrayType CArray;
    typedef CArrayType::RefArrayType CArrayRef;
    typedef IArrayType::ArrayType IArray;

    typedef double HamiltonianType;

    typedef std::shared_ptr<GridDensityLikelihoodBase<3>> Likelihood_t;
    typedef std::shared_ptr<BORGForwardModel> Model_t;

  protected:
    typedef boost::multi_array_ref<IArrayType::ArrayType::element, 1>
        FlatIntType;
    typedef FFTW_Manager_3d<double> DFT_Manager;

    MPI_Communication *comm;

    std::shared_ptr<DFT_Manager> base_mgr;
    Model_t pretransform, posttransform;
    Likelihood_t likelihood;

    long fourierLocalSize;
    FCalls::plan_type analysis_plan, synthesis_plan;
    size_t N0, N1, N2;
    size_t startN0, localN0, endN0;
    double L0, L1, L2, volume, volNorm;
    int Ncat;
    SLong *attempt_field, *accept_field;
    ScalarStateElement<int> *bad_sample;

    ArrayType *mass_field, *s_field;
    IArrayType *adjust_field;
    CArrayType *momentum_field, *s_hat_field;

    int maxTime, lastTime;
    double lastEpsilon, maxEpsilon;
    SymplecticIntegrators symp;

    boost::optional<std::string> phaseFilename;
    std::string dataName;

    std::string momentum_field_name, s_hat_field_name, s_field_name,
        hades_attempt_count_name, hades_accept_count_name, hmc_bad_sample_name,
        hmc_force_save_final_name, hmc_Elh_name, hmc_Eprior_name;

    void setupNames(std::string const &prefix);

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

    void computeGradientPsi_Likelihood(
        MarkovState &state, CArrayRef const &s, CArrayRef &grad_array,
        bool accumulate);

    typedef boost::multi_array<double, 2> IntegratorCoefficients;
    typedef HMCOption::IntegratorScheme IntegratorScheme;

    IntegratorScheme current_scheme;
    std::shared_ptr<Hermiticity_fixer<double, 3>> fixer;
    double k_max;

    auto free_phase_mask();

  public:
    HMCDensitySampler(
        MPI_Communication *comm, Likelihood_t likelihood, double k_max_ = 1000,
        std::string const &prefix = std::string());
    virtual ~HMCDensitySampler();

    void
    setPhaseFile(std::string const &filename, std::string const &objectName) {
      phaseFilename = filename;
      dataName = objectName;
    }

    virtual void generateMockData(MarkovState &state);
    void generateRandomField(MarkovState &state);

    void setTransforms(Model_t pretransform_, Model_t posttransform_);
    void setIntegratorScheme(IntegratorScheme scheme);

    double computeHamiltonian(MarkovState &state, bool gradient_next = false);

    void restore(MarkovState &state);
    void initialize(MarkovState &state);

    virtual void sample(MarkovState &state);

    void checkGradient(MarkovState &state, int step = 10);
    void checkGradientReal(MarkovState &state, int step = 10);

    void setMaxEpsilon(double eps) { this->maxEpsilon = eps; }
    void setMaxTimeSteps(int Ntime) { this->maxTime = Ntime; }

    // Codelet generic functions
    template <typename Function>
    void codeletGeneral(IArray &adjust_array, Function codelet) {
      size_t N2_HC = base_mgr->N2_HC;
#pragma omp parallel for schedule(static) collapse(3)
      for (size_t n0 = startN0; n0 < endN0; n0++) {
        for (size_t n1 = 0; n1 < N1; n1++) {
          for (size_t n2 = 1; n2 < N2_HC - 1; n2++) {
            codelet(n0, n1, n2, adjust_array);
          }
        }
      }

      codeletNyquist(0, adjust_array, codelet);
      codeletNyquist(base_mgr->N2_HC - 1, adjust_array, codelet);
    }

    template <typename Function>
    void codeletNyquist(int n2, const IArray &adjust_array, Function codelet) {
      size_t N0end = std::min(endN0, N0);
      size_t N0start = std::max(startN0, size_t(0));
#pragma omp parallel for schedule(static) collapse(2)
      for (size_t n0 = N0start; n0 < N0end; n0++) {
        for (size_t n1 = 0; n1 < N1; n1++) {
          codelet(n0, n1, n2, adjust_array);
        }
      }

      if (startN0 == 0 && localN0 > 0)
        for (size_t n1 = 0; n1 < N1; n1++)
          codelet(0, n1, n2, adjust_array);

      if (startN0 <= N0 / 2 && startN0 + localN0 > N0 / 2)
        for (size_t n1 = 0; n1 < N1; n1++)
          codelet(N0 / 2, n1, n2, adjust_array);
    }

    template <typename Function>
    HamiltonianType codeletNyquistHamiltonian(
        int n2, const IArray &adjust_array, Function codelet) {
      size_t N0end = std::min(endN0, N0);
      size_t N0start = std::max(startN0, size_t(0));
      HamiltonianType E = 0;

#pragma omp parallel for schedule(static) collapse(2) reduction(+ : E)
      for (size_t n0 = N0start; n0 < N0end; n0++) {
        for (size_t n1 = 0; n1 < N1; n1++) {
          E += codelet(n0, n1, n2, adjust_array);
        }
      }

      if (startN0 == 0 && localN0 > 0)
#pragma omp parallel for schedule(static) reduction(+ : E)
        for (size_t n1 = 0; n1 < N1; n1++)
          E += codelet(0, n1, n2, adjust_array);

      if (startN0 <= N0 / 2 && startN0 + localN0 > N0 / 2)
#pragma omp parallel for schedule(static) reduction(+ : E)
        for (size_t n1 = 0; n1 < N1; n1++)
          E += codelet(N0 / 2, n1, n2, adjust_array);

      return E;
    }

    template <typename Function>
    HamiltonianType
    codeletGeneralHamiltonian(const IArray &adjust_array, Function codelet) {
      HamiltonianType E = 0;
      namespace ph = std::placeholders;
      size_t N2_HC = base_mgr->N2_HC;

#pragma omp parallel for schedule(static) collapse(3) reduction(+ : E)
      for (size_t n0 = startN0; n0 < startN0 + localN0; n0++) {
        for (size_t n1 = 0; n1 < N1; n1++) {
          for (size_t n2 = 1; n2 < N2_HC - 1; n2++) {
            E += codelet(n0, n1, n2, adjust_array);
          }
        }
      }

      E += codeletNyquistHamiltonian(
          0, adjust_array, std::bind(codelet, ph::_1, ph::_2, ph::_3, ph::_4));
      E += codeletNyquistHamiltonian(
          base_mgr->N2_HC - 1, adjust_array,
          std::bind(codelet, ph::_1, ph::_2, ph::_3, ph::_4));

      return E;
    }
  };

}; // namespace LibLSS

#endif
