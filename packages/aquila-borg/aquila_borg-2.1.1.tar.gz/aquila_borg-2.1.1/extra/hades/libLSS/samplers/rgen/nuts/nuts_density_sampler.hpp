/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/samplers/rgen/nuts/nuts_density_sampler.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_NUTS_DENSITY_HPP
#define __LIBLSS_NUTS_DENSITY_HPP

#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/tools/fftw_allocator.hpp"
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/tools/symplectic_integrator.hpp"

namespace LibLSS {

  namespace NUTS_step {

    //1) store some constants that are required during recursion
    struct nuts_util {
      // Constants through each recursion
      double log_u;
      double H0;
      int sign;

      // Aggregators through each recursion
      int n_tree;
      double sum_prob;
      bool criterion;
    };
  } // namespace NUTS_step

  namespace NUTS_Details {

    template <typename Function>
    void accumulateHamiltonian(
        int n0, int n1, int n2, const IArrayType::ArrayType &adjust_array,
        const Function &f, double &E) {
      E += f(n0, n1, n2, adjust_array);
    }

  } // namespace NUTS_Details

  namespace NUTSOption {
    using namespace SymplecticOption;
  };

  class NUTSDensitySampler : public MarkovSampler {
  public:
    typedef ArrayType::ArrayType Array;
    typedef ArrayType::RefArrayType ArrayRef;
    typedef CArrayType::ArrayType CArray;
    typedef CArrayType::RefArrayType CArrayRef;
    typedef IArrayType::ArrayType IArray;

    typedef double HamiltonianType;

  protected:
    typedef boost::multi_array_ref<IArrayType::ArrayType::element, 1>
        FlatIntType;

    MPI_Communication *comm;

    long fourierLocalSize;
    FCalls::plan_type analysis_plan, synthesis_plan;
    FlatIntType *flat_key;
    long N0, N1, N2, N2real, Ntot, Ntot_k, N2_HC;
    long startN0, localN0, localNtot, localNtot_k;
    double L0, L1, L2, volume, volNorm;
    int Ncat;
    SLong *attempt_field, *accept_field;

    FFTW_Allocator<double> allocator_real;
    FFTW_Allocator<std::complex<double>> allocator_complex;

    ArrayType *sqrt_mass_field, *s_field;
    IArrayType *adjust_field;
    CArrayType *momentum_field, *s_hat_field;
    FFTW_Real_Array *tmp_real_field;
    FFTW_Complex_Array *tmp_complex_field;
    boost::multi_array<int, 1> peer;

    int maxTime;
    double maxEpsilon;
    SymplecticIntegrators symp;

    void doSympInt(MarkovState &state, MarkovState &state, CArray &s_hat);
    void updateMomentum(MarkovState &state, double dt, CArrayRef &force);
    void updatePosition(double dt, CArray &s_hat);
    HamiltonianType computeHamiltonian(
        MarkovState &state, MarkovState &state, CArray &s_hat, bool final_call);
    HamiltonianType computeHamiltonian_Prior(
        MarkovState &state, MarkovState &state, CArray &s_hat);
    HamiltonianType computeHamiltonian_Kinetic();
    void initializeMomenta(MarkovState &state);
    void computeGradientPsi(
        MarkovState &state, MarkovState &state, CArray &s,
        CArrayRef &grad_array);
    void computeGradientPsi_Prior(
        MarkovState &state, MarkovState &state, CArray &s,
        CArrayRef &grad_array);

    void updateMass(MarkovState &state, MarkovState &state);
    void Hermiticity_fixup(CArrayType::ArrayType &a);
    void Hermiticity_fixup_plane(int Nplane, CArrayType::ArrayType &a);

    virtual void computeGradientPsi_Likelihood(
        MarkovState &state, MarkovState &state, CArray &s,
        CArrayRef &grad_array, bool accumulate) = 0;
    virtual HamiltonianType computeHamiltonian_Likelihood(
        MarkovState &state, MarkovState &state, CArray &s_hat,
        bool final_call) = 0;

    virtual void
    saveAuxiliaryAcceptedFields(MarkovState &state, MarkovState &state) {}

    void computeFourierSpace_GradientPsi(
        ArrayRef &real_gradient, CArrayRef &grad_array, bool accumulate);

    typedef boost::multi_array<double, 2> IntegratorCoefficients;
    typedef NUTSOption::IntegratorScheme IntegratorScheme;

    IntegratorCoefficients I_coefs;

  public:
    NUTSDensitySampler(
        MPI_Communication *comm, int maxTimeIntegration, double maxEpsilon);
    virtual ~NUTSDensitySampler();

    virtual void generateMockData(MarkovState &state, MarkovState &state) = 0;
    void generateRandomField(MarkovState &state, MarkovState &state);

    void setIntegratorScheme(IntegratorScheme scheme);
    //        void setIntegratorScheme(const IntegratorCoefficients& coefs);

    HamiltonianType computeHamiltonian(MarkovState &state, MarkovState &state);

    void restore_NUTS(MarkovState &state, MarkovState &state);
    void initialize_NUTS(MarkovState &state, MarkovState &state);

    virtual void sample(MarkovState &state, MarkovState &state);

    void checkGradient(MarkovState &state, MarkovState &state, int step = 10);
    void checkHermiticityFixup(MarkovState &state, MarkovState &state);

    void setMaxEpsilon(double eps) { this->maxEpsilon = eps; }
    void setMaxTimeSteps(int Ntime) { this->maxTime = Ntime; }

    // Codelet generic functions
    template <typename Function>
    void codeletGeneral(IArray &adjust_array, Function codelet) {
#pragma omp parallel for schedule(static)
      for (int n0 = startN0; n0 < startN0 + localN0; n0++) {
        for (int n1 = 0; n1 < N1; n1++) {
          for (int n2 = 1; n2 < N2_HC - 1; n2++) {
            codelet(n0, n1, n2, adjust_array);
          }
        }
      }

      codeletNyquist(0, adjust_array, codelet);
      codeletNyquist(N2_HC - 1, adjust_array, codelet);
    }

    template <typename Function>
    void codeletNyquist(int n2, const IArray &adjust_array, Function codelet) {
      int N0end = std::min(startN0 + localN0, N0 / 2);
      int N0start = std::max(startN0, 1L);
#pragma omp parallel for schedule(static)
      for (int n0 = N0start; n0 < N0end; n0++) {
        for (int n1 = 0; n1 < N1; n1++) {
          codelet(n0, n1, n2, adjust_array);
        }
      }

      if (startN0 == 0 && localN0 > 0)
        for (int n1 = 0; n1 <= N1 / 2; n1++)
          codelet(0, n1, n2, adjust_array);

      if (startN0 <= N0 / 2 && startN0 + localN0 > N0 / 2)
        for (int n1 = 0; n1 <= N1 / 2; n1++)
          codelet(N0 / 2, n1, n2, adjust_array);
    }

    template <typename Function>
    HamiltonianType codeletNyquistHamiltonian(
        int n2, const IArray &adjust_array, Function codelet) {
      int N0end = std::min(startN0 + localN0, N0 / 2);
      int N0start = std::max(startN0, 1L);
      HamiltonianType E = 0;

#pragma omp parallel for schedule(static) reduction(+ : E)
      for (int n0 = N0start; n0 < N0end; n0++) {
        for (int n1 = 0; n1 < N1; n1++) {
          E += codelet(n0, n1, n2, adjust_array);
        }
      }

      if (startN0 == 0 && localN0 > 0)
#pragma omp parallel for schedule(static) reduction(+ : E)
        for (int n1 = 0; n1 <= N1 / 2; n1++)
          E += codelet(0, n1, n2, adjust_array);

      if (startN0 <= N0 / 2 && startN0 + localN0 > N0 / 2)
#pragma omp parallel for schedule(static) reduction(+ : E)
        for (int n1 = 0; n1 <= N1 / 2; n1++)
          E += codelet(N0 / 2, n1, n2, adjust_array);

      return E;
    }

    template <typename Function>
    HamiltonianType
    codeletGeneralHamiltonian(const IArray &adjust_array, Function codelet) {
      HamiltonianType E = 0;

#pragma omp parallel for schedule(static) reduction(+ : E)
      for (int n0 = startN0; n0 < startN0 + localN0; n0++) {
        for (int n1 = 0; n1 < N1; n1++) {
          for (int n2 = 1; n2 < N2_HC - 1; n2++) {
            E += codelet(n0, n1, n2, adjust_array);
          }
        }
      }

      E += codeletNyquistHamiltonian(
          0, adjust_array, boost::bind(codelet, _1, _2, _3, _4));
      E += codeletNyquistHamiltonian(
          N2_HC - 1, adjust_array, boost::bind(codelet, _1, _2, _3, _4));

      return E;
    }
  };

}; // namespace LibLSS

#endif
