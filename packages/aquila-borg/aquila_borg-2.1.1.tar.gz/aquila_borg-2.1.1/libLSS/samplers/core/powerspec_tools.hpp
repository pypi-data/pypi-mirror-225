/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/core/powerspec_tools.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_POWER_SPECTRUM_TOOLS_HPP
#define __LIBLSS_POWER_SPECTRUM_TOOLS_HPP

#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/mcmc/state_sync.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/array_tools.hpp"

namespace LibLSS {

  template <typename ArrayType>
  typename ArrayType::value_type norm_v(const ArrayType &x) {
    typename ArrayType::value_type ret = 0;

    for (size_t i = 0; i < x.size(); i++)
      ret += x[i] * x[i];

    return std::sqrt(ret);
  }

  static inline int ifftfreq(int i, int N) {
    return ((i > N / 2) ? (i - N) : i);
  }

  template <typename T>
  T kmode(int i, int N, T L) {
    return 2 * M_PI / L * ifftfreq(i, N);
  }

  template <typename IKArray, typename LArray>
  int power_key(
      const IKArray &N, const IKArray &ik, const LArray &L, double kmin,
      double dk, int Nbin) {
    ///calculate kmodes
    boost::array<double, 3> k;
    double kmod;

    // 0 mode is specific
    if (ik[0] == 0 && ik[1] == 0 && ik[2] == 0)
      return 0;

    for (int i = 0; i < 3; i++)
      k[i] = kmode(ik[i], N[i], L[i]);

    kmod = norm_v(k); /// units k [h/Mpc]

    int ll = 1 + int(std::floor((kmod - kmin) / dk));

    Console::instance().c_assert(
        (ll >= 0) && (ll < Nbin), "Over/Underflow binning in powerspectrum");
    return ll;
  }

  namespace init_helpers {

    template <
        typename Manager, typename ArrayKey, typename ArrayKeyCounts,
        typename ArrayAdjust, typename ArrayNmode>
    void initialize_powerspectrum_keys(
        Manager &manager, ArrayKey &array_key, ArrayKeyCounts &array_key_counts,
        ArrayAdjust &adjust, ArrayNmode &nmode_array,
        boost::array<double, 3> const &L, double kmin, double kmax,
        size_t N_k) {
      using boost::format;
      Console &cons = Console::instance();
      size_t N0 = manager.N0;
      size_t startN0 = manager.startN0;
      size_t localN0 = manager.localN0;
      size_t N1 = manager.N1;
      size_t N2_HC = manager.N2_HC;

      // FIX: Manager sizes should size_t.
      boost::array<size_t, 3> iN{N0, N1, size_t(manager.N2)};

      array::fill(nmode_array, 0);
      array::fill(array_key_counts, 0);

      for (size_t ikx = startN0; ikx < startN0 + localN0; ikx++) {
        for (size_t iky = 0; iky < N1; iky++) {
          for (size_t ikz = 0; ikz < N2_HC; ikz++) {
            boost::array<size_t, 3> ik{ikx, iky, ikz};
            int p_key = power_key(iN, ik, L, kmin, (kmax - kmin) / N_k, N_k);

            array_key_counts[p_key]++;
            array_key[ikx][iky][ikz] = p_key;
            assert(p_key < N_k);
            nmode_array[p_key] +=
                2; // Put everybody at 2. There will be a fix after the loop.
            adjust[ikx][iky][ikz] = 2;
          }
        }
      }

      // Only one mode and it is not sampling.
      array_key_counts[0] = 0;

      if (startN0 == 0 && localN0 > 0) {
        adjust[0][0][0] = 0;
        adjust[0][N1 / 2][0] = 1;
        adjust[0][0][N2_HC - 1] = 1;
        adjust[0][N1 / 2][N2_HC - 1] = 1;

        nmode_array[array_key[0][0][0]] -= 2; // No mode for k=0
        nmode_array[array_key[0][N1 / 2][0]] -= 1;
        nmode_array[array_key[0][0][N2_HC - 1]] -= 1;
        nmode_array[array_key[0][N1 / 2][N2_HC - 1]] -= 1;
      }

      if (startN0 <= N0 / 2 && localN0 + startN0 > N0 / 2) {
        adjust[N0 / 2][0][0] = 1;
        adjust[N0 / 2][N1 / 2][0] = 1;
        adjust[N0 / 2][0][N2_HC - 1] = 1;
        adjust[N0 / 2][N1 / 2][N2_HC - 1] = 1;

        nmode_array[array_key[N0 / 2][0][0]] -=
            1; // Hermiticity removes one free mode
        nmode_array[array_key[N0 / 2][N1 / 2][0]] -= 1;
        nmode_array[array_key[N0 / 2][0][N2_HC - 1]] -= 1;
        nmode_array[array_key[N0 / 2][N1 / 2][N2_HC - 1]] -= 1;
      }

      cons.template print<LOG_DEBUG>(
          format("Reducing mode counting: num_elements=%d") %
          nmode_array.num_elements());
      manager.getComm()->all_reduce_t(
          MPI_IN_PLACE, nmode_array.data(), nmode_array.num_elements(),
          MPI_SUM);
      cons.template print<LOG_DEBUG>(
          format("Reducing key counting: num_elements=%d") %
          array_key_counts.num_elements());
      manager.getComm()->all_reduce_t(
          MPI_IN_PLACE, array_key_counts.data(),
          array_key_counts.num_elements(), MPI_SUM);
    }

  } // namespace init_helpers

  class PowerSpectrumSampler_Base : public MarkovSampler {
  protected:
    typedef FFTW_Manager_3d<double> FFTMgr;

    long N0, N1, N2, N2_HC;
    long fourierLocalSize;
    long startN0, localN0;
    long N_fourier_elements, local_fourier_elements;
    long Ntot;
    int N_k;
    double kmin, kmax;
    double volNorm, volume;
    double L0, L1, L2;

    FFTMgr *mgr;

    IArrayType *keys, *adjustMul;
    IArrayType1d *key_counts, *nmode;
    ArrayType1d *P, *k;
    RandomGen *rgen;
    MPI_SyncBundle P_sync;
    MPI_Communication *comm;

  public:
    PowerSpectrumSampler_Base(MPI_Communication *lcomm)
        : mgr(0), keys(0), key_counts(0), nmode(0), P(0), k(0), rgen(0),
          comm(lcomm) {}
    virtual ~PowerSpectrumSampler_Base();

    bool restore_base(MarkovState &state);
    void initialize_base(MarkovState &state);
  };

  class PowerSpectrumSampler_Coloring : public PowerSpectrumSampler_Base {
  protected:
    MFCalls::plan_type analysis_plan, synthesis_plan;
    MFCalls::complex_type *tmp_fourier;
    MFCalls::real_type *tmp_real;
    ArrayType1d sqrt_P_info;

    int Ncatalog;

  public:
    PowerSpectrumSampler_Coloring(MPI_Communication *comm)
        : PowerSpectrumSampler_Base(comm), tmp_fourier(0), tmp_real(0),
          sqrt_P_info(boost::extents[0]) {}
    virtual ~PowerSpectrumSampler_Coloring();

    bool initialize_coloring(MarkovState &state);
    bool restore_coloring(MarkovState &state);

    void update_s_field_from_x(MarkovState &state);
    void
    update_s_field_from_x(MarkovState &state, const ArrayType1d &powerSpectrum);
  };

} // namespace LibLSS

#endif
