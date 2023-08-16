/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/samplers/rgen/nuts/nuts_density_sampler.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <CosmoTool/algo.hpp>
#include <Eigen/Core>
#include <boost/format.hpp>
#include <boost/bind.hpp>
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/samplers/rgen/nuts/nuts_density_sampler.hpp"
#include "libLSS/tools/uninitialized_type.hpp"

static const bool ULTRA_VERBOSE = false;

using namespace LibLSS;
using boost::extents;
using boost::format;
using boost::ref;

using CosmoTool::square;

using boost::c_storage_order;
typedef boost::multi_array_types::extent_range range;

typedef Eigen::Map<Eigen::ArrayXd, Eigen::Aligned> MappedArray;

static const int ROOT_RANK = 0;

NUTSDensitySampler::NUTSDensitySampler(
    MPI_Communication *comm, int maxTime, double maxEpsilon)
    : flat_key(0), tmp_real_field(0), tmp_complex_field(0), momentum_field(0),
      analysis_plan(0), synthesis_plan(0), attempt_field(0), accept_field(0),
      comm(comm) {
  this->maxTime = maxTime;
  this->maxEpsilon = maxEpsilon;
  setIntegratorScheme(NUTSOption::SI_2A);
}

void NUTSDensitySampler::restore_NUTS(MarkovState &state, MarkovState &state) {
  initialize_NUTS(state, state);
}

void NUTSDensitySampler::initialize_NUTS(
    MarkovState &state, MarkovState &state) {
  Console &cons = Console::instance();
  ConsoleContext<LOG_INFO> ctx("Initialize hades density sampler");

  N0 = state.get<SLong>("N0")->value;
  N1 = state.get<SLong>("N1")->value;
  N2 = state.get<SLong>("N2")->value;

  N2_HC = N2 / 2 + 1;

  // This for MPI support
  startN0 = state.get<SLong>("startN0")->value;
  localN0 = state.get<SLong>("localN0")->value;
  fourierLocalSize = state.get<SLong>("fourierLocalSize")->value;

  // FFTW decides how much we should allocate at minimum.
  allocator_real.minAllocSize = fourierLocalSize * 2;
  allocator_complex.minAllocSize = fourierLocalSize;

  L0 = state.get<SDouble>("L0")->value;
  L1 = state.get<SDouble>("L1")->value;
  L2 = state.get<SDouble>("L2")->value;
  if (tmp_real_field) {
    error_helper<ErrorBadState>(
        "NUTSDensitySampler has already been initialized.");
  }

  Ncat = state.get<SLong>("NCAT")->value;

  cons.print<LOG_DEBUG>("Allocating s field");
  s_hat_field = new CArrayType(
      extents[range(startN0, startN0 + localN0)][N1][N2_HC], allocator_complex);
  s_hat_field->setRealDims(ArrayDimension(N0, N1, N2_HC));
  s_field = new ArrayType(extents[range(startN0, startN0 + localN0)][N1][N2]);
  s_field->setRealDims(ArrayDimension(N0, N1, N2));
  cons.print<LOG_DEBUG>("Allocating momentum field");
  momentum_field = new CArrayType(
      extents[range(startN0, startN0 + localN0)][N1][N2_HC], allocator_complex);
  momentum_field->setRealDims(ArrayDimension(N0, N1, N2_HC));

  // Pass the ownership to state
  state.newElement("momentum_field", momentum_field);
  state.newElement("s_hat_field", s_hat_field, true);
  state.newElement("s_field", s_field, true);
  state.newElement("hades_attempt_count", attempt_field = new SLong(), true);
  state.newElement("hades_accept_count", accept_field = new SLong(), true);

  attempt_field->value = 0;
  accept_field->value = 0;
  attempt_field->setResetOnSave(0);
  accept_field->setResetOnSave(0);

  s_hat_field->eigen().fill(0);
  s_field->eigen().fill(0);
  momentum_field->eigen().fill(0);

  Ntot = N0 * N1 * N2;
  Ntot_k = N0 * N1 * (N2 / 2 + 1);
  N2_HC = N2 / 2 + 1;

#ifdef ARES_MPI_FFTW
  N2real = 2 * N2_HC;
#else
  N2real = N2;
#endif
  Console::instance().print<LOG_DEBUG>(
      format("Using N2real = %d (N2 was %d)") % N2real % N2);

  localNtot = localN0 * N1 * N2;
  localNtot_k = localN0 * N1 * (N2 / 2 + 1);

  volume = L0 * L1 * L2;
  volNorm = volume / Ntot;

  peer.resize(extents[localN0]);

  // Figure out the peer for each line of Nyquist planes
  {
    // First gather the MPI structure
    boost::multi_array<long, 1> all_N0s(extents[comm->size()]);
    int localAccumN0 = 0;

    comm->all_gather_t(&localN0, 1, all_N0s.data(), 1);

    cons.print<LOG_DEBUG>("Peers: ");

    for (int p = 0; p < comm->size(); p++) {
      cons.print<LOG_DEBUG>(format(" N0[%d] = %d") % p % all_N0s[p]);
      // Find the position of the mirror of this line
      for (int j = 0; j < all_N0s[p]; j++) {
        int reciprocal = N0 - (localAccumN0 + j);

        // If this mirror is within our range then we are concerned
        // to do data I/O with this peer
        if (reciprocal >= startN0 && reciprocal < startN0 + localN0) {
          peer[reciprocal - startN0] = p;
          cons.print<LOG_DEBUG>(format(" %d -> peer %d") % reciprocal % p);
        }
      }
      localAccumN0 += all_N0s[p];
    }
  }

  ctx.print("Creating MPI/FFTW plans for NUTSDensitySampler");
  tmp_real_field = new FFTW_Real_Array(
      extents[range(startN0, startN0 + localN0)][N1][N2real], c_storage_order(),
      allocator_real);
  tmp_complex_field = new FFTW_Complex_Array(
      extents[range(startN0, startN0 + localN0)][N1][N2_HC], c_storage_order(),
      allocator_complex);

  analysis_plan = MFCalls::plan_dft_r2c_3d(
      N0, N1, N2, tmp_real_field->data(),
      (MFCalls::complex_type *)tmp_complex_field->data(),
#ifdef ARES_MPI_FFTW
      comm->comm(),
#endif
      // FFTW_MPI_TRANSPOSED_OUT|
      FFTW_DESTROY_INPUT | FFTW_MEASURE);
  synthesis_plan = MFCalls::plan_dft_c2r_3d(
      N0, N1, N2, (MFCalls::complex_type *)tmp_complex_field->data(),
      tmp_real_field->data(),
#ifdef ARES_MPI_FFTW
      comm->comm(),
#endif
      //FFTW_MPI_TRANSPOSED_IN|
      FFTW_DESTROY_INPUT | FFTW_MEASURE);

  ctx.print("Done creating FFTW plans for NUTSDensitySampler");

  sqrt_mass_field = new ArrayType(
      extents[range(startN0, startN0 + localN0)][N1][N2_HC], allocator_real);
  sqrt_mass_field->setRealDims(ArrayDimension(N0, N1, N2_HC));
  sqrt_mass_field->eigen().fill(0);
  state.newElement("hades_sqrt_mass", sqrt_mass_field);
}

NUTSDensitySampler::~NUTSDensitySampler() {
  if (tmp_real_field) {
    Console::instance().print<LOG_INFO>("Cleaning up NUTSDensitySampler");

    delete flat_key;
    delete tmp_real_field;
    delete tmp_complex_field;
    MFCalls::destroy_plan(analysis_plan);
    MFCalls::destroy_plan(synthesis_plan);
  }
}

template <typename CArray>
void fixupNyquistPlane(CArray &a, int Nyq_0, int N1, int Nplane) {
  // The Nyquist plane of the Nyquist plane is just here.
  for (int n1 = 1; n1 < N1 / 2; n1++) {
    a[Nyq_0][N1 - n1][Nplane] = conj(a[Nyq_0][n1][Nplane]);
  }
  // Pure real there
  a[Nyq_0][0][Nplane].imag() = 0;
  a[Nyq_0][N1 / 2][Nplane].imag() = 0;
}

void NUTSDensitySampler::Hermiticity_fixup(CArrayType::ArrayType &a) {
  ConsoleContext<LOG_DEBUG> ctx("H fixup");
  Hermiticity_fixup_plane(0, a);
  Hermiticity_fixup_plane(N2_HC - 1, a);
}

void NUTSDensitySampler::Hermiticity_fixup_plane(
    int Nplane, CArrayType::ArrayType &a) {

  // First make a sweep to figure out what is the destination and origin of each line
  typedef CArrayType::ArrayType::element CElement;
  RequestArray request_array(extents[localN0]);
  StatusArray status_array(extents[localN0]);
  boost::multi_array<CElement, 2> tmp_line(extents[localN0][N1]);
  ConsoleContext<LOG_DEBUG> ctx("H fixup plane");
  Console &cons = Console::instance();

  for (int n0 = 0; n0 < localN0; n0++) {
    if (startN0 + n0 < N0 / 2) {
      // Copy & conjugate
      if (ULTRA_VERBOSE)
        ctx.print(format("Copying line %d x * x %d") % n0 % Nplane);
      for (int n1 = 0; n1 < N1; n1++)
        tmp_line[n0][n1] = a[startN0 + n0][n1][Nplane];

      if (peer[n0] != comm->rank()) {

        if (ULTRA_VERBOSE)
          ctx.print(format("Scheduling send to peer %d") % peer[n0]);
        request_array[n0] = comm->Isend(
            &tmp_line[n0][0], N1, translateMPIType<CElement>(), peer[n0],
            (N0 - n0 - startN0) % N0);
      }
    } else {
      if (ULTRA_VERBOSE)
        ctx.print(format("Considering line %d x * x %d") % n0 % Nplane);

      if (peer[n0] != comm->rank()) {
        if (ULTRA_VERBOSE)
          ctx.print(
              format("Scheduling recv from peer %d for line %d") % peer[n0] %
              n0);
        request_array[n0] = comm->Irecv(
            &tmp_line[n0][0], N1, translateMPIType<CElement>(), peer[n0],
            n0 + startN0);

      } else {
        int ln0 = n0 + startN0;
        int rn0 = (N0 - ln0) % N0;

        cons.c_assert(rn0 >= startN0 && rn0 < startN0 + localN0, "Invalid rn0");

        for (int n1 = 0; n1 < N1; n1++)
          tmp_line[n0][n1] = a[rn0][n1][Nplane];
        if (ln0 == rn0)
          tmp_line[n0][0].imag() = 0;
      }
    }
  }

  if (startN0 <= N0 / 2 && startN0 + localN0 > N0 / 2) {
    if (ULTRA_VERBOSE)
      ctx.print("Fixup nyquist line N0/2, N1 ");
    cons.c_assert(
        peer[N0 / 2 - startN0] == comm->rank(),
        "Internal error. Peer should be self.");

    fixupNyquistPlane(a, N0 / 2, N1, Nplane);
  }

  if (startN0 == 0 && localN0 > 0) {
    if (ULTRA_VERBOSE)
      ctx.print("Fixup nyquist line 0, N1 ");
    cons.c_assert(
        peer[0] == comm->rank(), "Internal error. Peer should be self.");

    fixupNyquistPlane(a, 0, N1, Nplane);
  }

  for (int n0 = 0; n0 < localN0; n0++) {
    if (peer[n0] != comm->rank()) {
      if (ULTRA_VERBOSE)
        ctx.print(format("For line %d, waiting for peer %d") % n0 % peer[n0]);
      request_array[n0].wait(&status_array[n0]);
      if (status_array[n0].MPI_ERROR != MPI_SUCCESS) {
        error_helper<ErrorBadState>("Error in MPI operations. Stopping.");
      }
    }

    if (startN0 + n0 > N0 / 2) {
      // Copy in place
      for (int n1 = 0; n1 < N1; n1++) {
        int rn1 = (N1 - n1) % N1;
        a[startN0 + n0][n1][Nplane] = conj(tmp_line[n0][rn1]);
      }
    }
  }
}

static void nuts_checkHermiticity(const CArrayType::ArrayType &a) {
  long N0 = a.shape()[0], N1 = a.shape()[1], N2_HC = a.shape()[2];
  typedef CArrayType::ArrayType::element EType;

#ifndef ARES_MPI_FFTW
  // Check hermiticity
#  pragma omp parallel for
  for (long n0 = 0; n0 < N0; n0++) {
    for (long n1 = 0; n1 < N1; n1++) {
      const EType &c0 = a[n0][n1][N2_HC - 1];
      const EType &c1 = conj(a[(N0 - n0) % N0][(N1 - n1) % N1][N2_HC - 1]);
      const EType &c2 = a[n0][n1][0];
      const EType &c3 = conj(a[(N0 - n0) % N0][(N1 - n1) % N1][0]);

      if (abs(c0 - c1) > 0.001 * abs(c1))
        error_helper<ErrorBadState>(
            format("Not conjugate for n0=%d n1=%d n2=%d, V=%g+I%g V_c=%g+I%g") %
            n0 % n1 % (N2_HC - 1) % c0.real() % c0.imag() % c1.real() %
            c1.imag());
      if (abs(c2 - c3) > 0.001 * abs(c2))
        error_helper<ErrorBadState>(
            format("Not conjugate for n0=%d n1=%d n2=%d, V=%g+I%g V_c=%g+I%g") %
            n0 % n1 % (0) % c2.real() % c2.imag() % c3.real() % c3.imag());
    }
  }
#endif
}

inline void codeletGenerateMomenta(
    int n0, int n1, int n2, const IArrayType::ArrayType &adjust_array,
    NUTSDensitySampler::CArray &momentum_array, RandomGen *rgen,
    const NUTSDensitySampler::Array &sqrt_mass) {
  CArrayType::ArrayType::element &e = momentum_array[n0][n1][n2];
  int adjust = adjust_array[n0][n1][n2];
  double Amplitude = sqrt_mass[n0][n1][n2];

  if (adjust == 0) {
    e = 0;
    return;
  }

  Amplitude = sqrt(Amplitude);
  e.real() = rgen->get().gaussian() * Amplitude;
  e.imag() = rgen->get().gaussian() * Amplitude;
}

void NUTSDensitySampler::initializeMomenta(MarkovState &state) {
  CArrayType::ArrayType &momentum_array = *momentum_field->array;
  IArrayType::ArrayType &adjust_array = *adjust_field->array;
  RandomGen *rgen = state.get<RandomGen>("random_generator");
  ArrayType::ArrayType &sqrt_mass = *sqrt_mass_field->array;

  codeletGeneral(
      adjust_array,
      boost::bind(
          &codeletGenerateMomenta, _1, _2, _3, _4, boost::ref(momentum_array),
          rgen, boost::cref(sqrt_mass)));
}

template <bool accumulate>
inline void codeletGradientLikelihood(
    int n0, int n1, int n2, double normalizer,
    NUTSDensitySampler::CArray &c_field,
    const NUTSDensitySampler::IArray &adjust_array,
    NUTSDensitySampler::CArrayRef &grad_array) {
  typedef NUTSDensitySampler::CArray CArray;
  typedef CArray::element etype;
  int adjust = adjust_array[n0][n1][n2];

  etype e = adjust * normalizer * c_field[n0][n1][n2];
  if (accumulate)
    grad_array[n0][n1][n2] += (e);
  else
    grad_array[n0][n1][n2] = (e);
  assert(!isinf(e.real()));
#if 1
  if (isnan(e.real()) || isnan(e.imag())) {
    Console &cons = Console::instance();
    cons.print<LOG_ERROR>(
        format("adjust=%d, norm=%lg, e[%d][%d][%d] = %lg + I %lg") % adjust %
        normalizer % n0 % n1 % n2 % e.real() % e.imag());
    MPI_Communication::instance()->abort();
  }
#endif
}

void NUTSDensitySampler::computeFourierSpace_GradientPsi(
    ArrayRef &real_gradient, CArrayRef &grad_array, bool accumulate) {
  using boost::ref;
  typedef CArray::element etype;
  double normalizer =
      1 /
      volume; // Normalization is like synthesis here, we consider the transpose synthesis
  int N2_HC = N2 / 2 + 1;

  IArrayType::ArrayType &adjust_array = *adjust_field->array;

  // BEWARE: real_gradient is destroyed!
  MFCalls::execute_r2c(
      analysis_plan, real_gradient.data(), tmp_complex_field->data());

  if (accumulate)
    codeletGeneral(
        adjust_array,
        boost::bind(
            &codeletGradientLikelihood<true>, _1, _2, _3, normalizer,
            ref(*tmp_complex_field), _4, ref(grad_array)));
  else
    codeletGeneral(
        adjust_array,
        boost::bind(
            &codeletGradientLikelihood<false>, _1, _2, _3, normalizer,
            ref(*tmp_complex_field), _4, ref(grad_array)));

  if (startN0 == 0 && localN0 > 0) {
    grad_array[0][0][0] = 0;
  }
}

#include "nuts_kinetic.tcc"
#include "nuts_prior.tcc"

void NUTSDensitySampler::computeGradientPsi(
    MarkovState &state, MarkovState &state, CArray &s, CArrayRef &grad_array) {
  computeGradientPsi_Prior(state, state, s, grad_array);
  computeGradientPsi_Likelihood(state, state, s, grad_array, true);
}

NUTSDensitySampler::HamiltonianType NUTSDensitySampler::computeHamiltonian(
    MarkovState &state, MarkovState &state, CArray &s_hat, bool final_call) {
  ConsoleContext<LOG_DEBUG> ctx("hamiltonian computation");

  HamiltonianType Ekin = computeHamiltonian_Kinetic();
  HamiltonianType Eprior = computeHamiltonian_Prior(state, state, s_hat);
  HamiltonianType Elh =
      computeHamiltonian_Likelihood(state, state, s_hat, final_call);

  ctx.print(format("Ekin = %lg") % double(Ekin));
  ctx.print(format("Eprior = %lg") % double(Eprior));
  ctx.print(format("Elh = %lg") % double(Elh));

  return Ekin + Eprior + Elh;
}

void NUTSDensitySampler::updateMomentum(
    MarkovState &state, double dt, CArrayRef &force) {
  CArrayType::ArrayType &momentum_array = *momentum_field->array;
  IArrayType::ArrayType &adjust_array = *adjust_field->array;

#pragma omp parallel for
  for (long n0 = startN0; n0 < startN0 + localN0; n0++) {
    for (long n1 = 0; n1 < N1; n1++) {
      for (long n2 = 0; n2 < N2_HC; n2++) {
        CArrayType::ArrayType::element &m = momentum_array[n0][n1][n2];
        m -= dt * (force[n0][n1][n2]);
        if (isnan(m.real()) || isnan(m.imag())) {
          Console &cons = Console::instance();
          cons.print<LOG_ERROR>(
              format("m = %g + I %g, dt = %lg, force = %lg + I %lg") %
              m.real() % m.imag() % dt % force[n0][n1][n2].real() %
              force[n0][n1][n2].imag());
          comm->abort();
        }
        if (adjust_array[n0][n1][n2] == 0)
          m = 0;
      }
    }
  }
}

void NUTSDensitySampler::updatePosition(double dt, CArray &s_hat) {
  CArrayType::ArrayType &momentum_array = *momentum_field->array;
  IArrayType::ArrayType &adjust_array = *adjust_field->array;
  ArrayType::ArrayType &sqrt_mass = *sqrt_mass_field->array;

  array::copyArray3d(*tmp_complex_field, momentum_array);
  Hermiticity_fixup(*tmp_complex_field);

#pragma omp parallel for
  for (long n0 = startN0; n0 < startN0 + localN0; n0++) {
    for (long n1 = 0; n1 < N1; n1++) {
      for (long n2 = 0; n2 < N2_HC; n2++) {
        double M = (sqrt_mass[n0][n1][n2]);
        CArrayType::ArrayType::element &e = s_hat[n0][n1][n2];
        if (adjust_array[n0][n1][n2] == 0 || M == 0)
          e = 0;
        else
          e += dt * (*tmp_complex_field)[n0][n1][n2] / M;
        //e += dt * momentum_array[n0][n1][n2] / M;
        assert(!isnan(e.real()));
        assert(!isnan(e.imag()));
      }
    }
  }
}

void NUTSDensitySampler::setIntegratorScheme(IntegratorScheme scheme) {
  symp.setIntegratorScheme(scheme);
}

void NUTSDensitySampler::doSympInt(
    MarkovState &state, MarkovState &state, CArray &s_hat) {
  ConsoleContext<LOG_INFO_SINGLE> ctx("Symplectic integration");
  RandomGen *rgen = state.get<RandomGen>("random_generator");
  int Ntime;
  double epsilon;
  ArrayType::ArrayType &sqrt_mass = *sqrt_mass_field->array;
  CArrayType::ArrayType &momentum_array = *momentum_field->array;

  if (comm->rank() == ROOT_RANK) {
    epsilon = maxEpsilon * rgen->get().uniform();
    do {
      Ntime = int(rgen->get().uniform() * maxTime);
    } while (Ntime == 0);
  }

  comm->broadcast_t(&epsilon, 1, ROOT_RANK);
  comm->broadcast_t(&Ntime, 1, ROOT_RANK);

  ctx.print(format("epsilon = %lg, Ntime = %d") % epsilon % Ntime);

  Uninit_FFTW_Complex_Array gradient_psi_p(
      extents[range(startN0, startN0 + localN0)][N1][N2_HC], allocator_complex);
  Uninit_FFTW_Complex_Array::array_type &gradient_psi =
      gradient_psi_p.get_array();

  symp.integrate(
      boost::bind(
          &NUTSDensitySampler::computeGradientPsi, this, ref(state), ref(state),
          _1, _2),
      sqrt_mass, epsilon, Ntime, s_hat, momentum_array, gradient_psi);
}

inline void nuts_codeletMass(
    int n0, int n1, int n2, const IArrayType::ArrayType &adjust_array, double A,
    double volume, const IArrayType::ArrayType &key_array,
    const ArrayType1d::ArrayType &pspec, ArrayType::ArrayType &sqrt_mass) {
  int key = key_array[n0][n1][n2];
  double P = pspec[key];
  int adj = adjust_array[n0][n1][n2];

  if (adj == 0 || P == 0)
    sqrt_mass[n0][n1][n2] = 0;
  else
    sqrt_mass[n0][n1][n2] = (adj * (1 / (volume * P) + A));
  if (isinf(sqrt_mass[n0][n1][n2])) {
    error_helper<ErrorBadState>(
        format("InF in mass at n0=%d n1=%d n2=%d, P=%lg") % n0 % n1 % n2 % P);
  }
  if (isnan(sqrt_mass[n0][n1][n2])) {
    error_helper<ErrorBadState>(
        format("NaN in mass at n0=%d n1=%d n2=%d, P=%lg") % n0 % n1 % n2 % P);
  }
}

void NUTSDensitySampler::updateMass(MarkovState &state, MarkovState &state) {
  ArrayType::ArrayType &sqrt_mass = *sqrt_mass_field->array;
  IArrayType::ArrayType &key_array = *state.get<IArrayType>("k_keys")->array;
  ArrayType1d::ArrayType &pspec =
      *state.get<ArrayType1d>("powerspectrum")->array;
  IArrayType::ArrayType &adjust =
      *state.get<IArrayType>("adjust_mode_multiplier")->array;

  sqrt_mass_field->eigen().fill(0);
  double A = 0;
  for (int c = 0; c < Ncat; c++) {
    double bias = state.get<SDouble>(format("galaxy_bias_%d") % c)->value;
    ArrayType::ArrayType &g_field =
        *state.get<ArrayType>(format("galaxy_data_%d") % c)->array;

#pragma omp parallel for reduction(+ : A)
    for (long n = 0; n < g_field.num_elements(); n++) {
      A += square(bias / volume) * g_field.data()[n];
    }
  }

  double nmean = state.get<SDouble>("galaxy_nmean_0")->value;
  A = 0;
  //A=nmean/(volume*volume) * N0*N1*N2;
  Console::instance().print<LOG_INFO>(
      format("Powerspectrum noise for mass = %lg") % A);

  codeletGeneral(
      adjust, boost::bind(
                  &nuts_codeletMass, _1, _2, _3, _4, A, volume, cref(key_array),
                  cref(pspec), ref(sqrt_mass)));
}

int stop_criterion(
    CArray &thetaminus, CArray &thetaplus, CArray &rminus, CArray &rplus) {
  ""
  " Compute the stop condition in the main loop
      // dot(dtheta, rminus) >= 0 & dot(dtheta, rplus >= 0)

      double a = 0.;
  double b = 0.;
  int s = 0;

#pragma omp parallel for schedule(static) reduction(+ : a, b)
  for (long n0 = startN0; n0 < startN0 + localN0; n0++) {
    for (long n1 = 0; n1 < N1; n1++) {
      for (long n2 = 0; n2 < N2_HC; n2++) {
        CArrayType::ArrayType::element &tm = thetaminus[n0][n1][n2];
        CArrayType::ArrayType::element &tp = thetaplus[n0][n1][n2];
        CArrayType::ArrayType::element &rm = rminus[n0][n1][n2];
        CArrayType::ArrayType::element &rp = rplus[n0][n1][n2];

        a += (tp.real() - tm.real()) * rm.real() +
             (tp.imag() - tm.imag()) * rm.imag();
        b += (tp.real() - tm.real()) * rp.real() +
             (tp.imag() - tm.imag()) * rp.imag();
      }
    }
  }

    if((a>=0.)&&(b>=0.) s=1;
    return s;
}

void NUTSDensitySampler::sample(MarkovState &state, MarkovState &state) {
  //we implement Algorithm 6 of Hoffman & Gelman 2014

  RandomGen *rgen = state.get<RandomGen>("random_generator");
  double HamiltonianInit, HamiltonianFinal, deltaH;
  ConsoleContext<LOG_INFO> ctx("hades density field sampler");
  adjust_field = state.get<IArrayType>("adjust_mode_multiplier");

  if (state.get<SBool>("hades_sampler_blocked")->value)
    return;

  FFTW_Complex_Array s_hat(
      extents[range(startN0, startN0 + localN0)][N1][N2_HC], c_storage_order(),
      allocator_complex);

  array::copyArray3d(s_hat, *state.get<CArrayType>("s_hat_field")->array);
  //    checkHermiticity(s_hat);

  updateMass(state, state);

  //1) Sample momenta
  initializeMomenta(state);

  //2) Resample u uniformely from [0,exp(-H0)]
  // Equivalent to (log(u) - joint) ~ exponential(1).
  double H0 = computeHamiltonian(state, state, s_hat, false);
  double logu;
  if (comm->rank() == ROOT_RANK)
    logu = -H0 - rgen->get().unitexp();
  comm->broadcast_t(&logu, 1, ROOT_RANK);

  //3) initialize the tree
  //3a) allocate arrays for left and right node of tree
  //state fields
  FFTW_Complex_Array thetaminus(
      extents[range(startN0, startN0 + localN0)][N1][N2_HC], c_storage_order(),
      allocator_complex);
  FFTW_Complex_Array thetaplus(
      extents[range(startN0, startN0 + localN0)][N1][N2_HC], c_storage_order(),
      allocator_complex);
  //momentum fields
  FFTW_Complex_Array rminus(
      extents[range(startN0, startN0 + localN0)][N1][N2_HC], c_storage_order(),
      allocator_complex);
  FFTW_Complex_Array rplus(
      extents[range(startN0, startN0 + localN0)][N1][N2_HC], c_storage_order(),
      allocator_complex);
  //3b) fill thetaminus and thetaplus with current state
  array::copyArray3d(thetaminus, *state.get<CArrayType>("s_hat_field")->array);
  array::copyArray3d(thetaplus, *state.get<CArrayType>("s_hat_field")->array);
  array::copyArray3d(rminus, *state.get<CArrayType>("momentum_field")->array);
  array::copyArray3d(rplus, *state.get<CArrayType>("momentum_field")->array);
  //3c) set tree parameter
  int j = 0; // initial heigth j = 0
  int n = 1; // Initially the only valid point is the initial point.
  int s = 1; // Main loop: will keep going until s == 0.

  //4) start building tree
  while (s == 1) {
    //4a) Choose a direction. -1 = backwards, 1 = forwards.
    int v;
    if (comm->rank() == ROOT_RANK)
      v = int(2. * rgen->get().uniform() - 1.);
    comm->broadcast_t(&v, 1, ROOT_RANK);

    //4b) Double the size of the tree.
    if (v == -1) {
      //thetaminus, rminus, gradminus, _, _, _, thetaprime, gradprime, logpprime, nprime, sprime, alpha, nalpha = build_tree(thetaminus, rminus, gradminus, logu, v, j, epsilon, f, joint)
    } else {
      //_, _, _, thetaplus, rplus, gradplus, thetaprime, gradprime, logpprime, nprime, sprime, alpha, nalpha = build_tree(thetaplus, rplus, gradplus, logu, v, j, epsilon, f, joint)
    }

    //4c Use Metropolis-Hastings to decide whether or not to move to a
    // point from the half-tree we just generated.
    double _tmp = min(1, float(nprime) / float(n));

    double ran_aux;
    if (comm->rank() == ROOT_RANK)
      ran_aux = rgen->get().uniform();
    comm->broadcast_t(&ran_aux, 1, ROOT_RANK);

    if ((sprime == 1) && (ran_aux < _tmp)) {
      samples [m, :] = thetaprime[:] lnprob[m] = logpprime logp =
                                         logpprime grad = gradprime
      [:]
    }

    //4d Update number of valid points we've seen.
    n += nprime
        // Decide if it's time to stop.
        s = sprime * stop_criterion(thetaminus, thetaplus, rminus, rplus);
    // Increment depth.
    j += 1
  }
}

HamiltonianInit = computeHamiltonian(state, state, s_hat, false);
// If we are the very first step, save the result of the forward model for the other samplers.
if (state.get<SLong>("MCMC_STEP")->value == 0)
  saveAuxiliaryAcceptedFields(state, state);

if (isnan(HamiltonianInit)) {
  error_helper<ErrorBadState>("NaN in hamiltonian initial");
}
doSympInt(state, state, s_hat);
HamiltonianFinal = computeHamiltonian(state, state, s_hat, true);
if (isnan(HamiltonianFinal)) {
  error_helper<ErrorBadState>("NaN in hamiltonian final");
}

deltaH = HamiltonianFinal - HamiltonianInit;
double log_u;

if (comm->rank() == ROOT_RANK)
  log_u = log(rgen->get().uniform());

comm->broadcast_t(&log_u, 1, ROOT_RANK);

if (attempt_field)
  attempt_field->value++;
ctx.print2<LOG_INFO_SINGLE>(
    format("log_u = %lg, deltaH = %lg") % log_u % deltaH);
if (log_u <= -deltaH) {
  // Accept the move
  if (comm->rank() == ROOT_RANK)
    ctx.print("accepting the move");

  saveAuxiliaryAcceptedFields(state, state);

  Hermiticity_fixup(s_hat);
  array::copyArray3d(*state.get<CArrayType>("s_hat_field")->array, s_hat);
  MFCalls::execute_c2r(synthesis_plan, s_hat.data(), tmp_real_field->data());

  // This one handles padded and unpadded data through multi_array
  array::scaleAndCopyArray3d(
      *state.get<ArrayType>("s_field")->array, *tmp_real_field, 1. / volume,
      true);

  if (accept_field)
    accept_field->value++;
}
}

/* TESTING FRAMEWORK */
void NUTSDensitySampler::checkHermiticityFixup(
    MarkovState &state, MarkovState &state) {
  FFTW_Real_Array s(
      extents[range(startN0, startN0 + localN0)][N1][N2], c_storage_order(),
      allocator_real);

  FFTW_Real_Array s0(
      extents[range(startN0, startN0 + localN0)][N1][N2real], c_storage_order(),
      allocator_real);
  FFTW_Complex_Array s_hat(
      extents[range(startN0, startN0 + localN0)][N1][N2_HC], c_storage_order(),
      allocator_complex);

  srand(rand() + comm->rank());
  MappedArray(s.data(), s.num_elements()).setRandom();

  array::scaleAndCopyArray3d(s0, s, 1.0 / (N0 * N1 * N2), true);
  MFCalls::execute_r2c(analysis_plan, s0.data(), s_hat.data());
  //    Hermiticity_fixup(s_hat);
  {
    std::string fname = str(format("test_%d.h5") % comm->rank());
    H5::H5File f(fname.c_str(), H5F_ACC_TRUNC);

    CosmoTool::hdf5_write_array(f, "input", s_hat);
    Hermiticity_fixup(s_hat);
    CosmoTool::hdf5_write_array(f, "output", s_hat);
  }
  //checkHermiticity(s_hat);
  MFCalls::execute_c2r(synthesis_plan, s_hat.data(), s0.data());

  double Norm = 0;
#pragma omp parallel for
  for (long n0 = startN0; n0 < startN0 + localN0; n0++)
    for (long n1 = 0; n1 < N1; n1++)
      for (long n2 = 0; n2 < N2; n2++)
        Norm += square(s[n0][n1][n2] - s0[n0][n1][n2]);

  comm->all_reduce_t(MPI_IN_PLACE, &Norm, 1, MPI_SUM);

  Console::instance().print<LOG_INFO>(
      format("Hermiticity fixup norm is %lg") % Norm);
}

void NUTSDensitySampler::checkGradient(
    MarkovState &state, MarkovState &state, int step) {
  HamiltonianType H0, H1, H2;
  HamiltonianType H0prior, H1prior, H2prior;
  HamiltonianType H0poisson, H1poisson, H2poisson;
  IArrayType::ArrayType &key_array = *state.get<IArrayType>("k_keys")->array;
  ArrayType1d::ArrayType &pspec =
      *state.get<ArrayType1d>("powerspectrum")->array;

  FFTW_Complex_Array s_hat(
      extents[range(startN0, startN0 + localN0)][N1][N2_HC], c_storage_order(),
      allocator_complex);
  double epsilon = 0.001;

  CArrayType *gradient_field, *gradient_field_ref;
  CArrayType *gradient_field_prior, *gradient_field_prior_ref;
  CArrayType *gradient_field_poisson, *gradient_field_poisson_ref;
  CArrayType *s_hat_field = state.get<CArrayType>("s_hat_field");

  if (state.exists("gradient_array")) {
    gradient_field = state.get<CArrayType>("gradient_array");
    gradient_field_prior = state.get<CArrayType>("gradient_array_prior");
    gradient_field_poisson = state.get<CArrayType>("gradient_array_lh");
    gradient_field_ref = state.get<CArrayType>("gradient_array_ref");
    gradient_field_prior_ref =
        state.get<CArrayType>("gradient_array_prior_ref");
    gradient_field_poisson_ref = state.get<CArrayType>("gradient_array_lh_ref");
  } else {
    state.newElement(
        "gradient_array",
        gradient_field = new CArrayType(
            extents[range(startN0, startN0 + localN0)][N1][N2_HC],
            allocator_complex));
    gradient_field->setRealDims(ArrayDimension(N0, N1, N2_HC));

    state.newElement(
        "gradient_array_ref",
        gradient_field_ref = new CArrayType(
            extents[range(startN0, startN0 + localN0)][N1][N2_HC],
            allocator_complex));
    gradient_field_ref->setRealDims(ArrayDimension(N0, N1, N2_HC));

    state.newElement(
        "gradient_array_prior",
        gradient_field_prior = new CArrayType(
            extents[range(startN0, startN0 + localN0)][N1][N2_HC],
            allocator_complex));
    gradient_field_prior->setRealDims(ArrayDimension(N0, N1, N2_HC));

    state.newElement(
        "gradient_array_prior_ref",
        gradient_field_prior_ref = new CArrayType(
            extents[range(startN0, startN0 + localN0)][N1][N2_HC],
            allocator_complex));
    gradient_field_prior_ref->setRealDims(ArrayDimension(N0, N1, N2_HC));

    state.newElement(
        "gradient_array_lh",
        gradient_field_poisson = new CArrayType(
            extents[range(startN0, startN0 + localN0)][N1][N2_HC],
            allocator_complex));
    gradient_field_poisson->setRealDims(ArrayDimension(N0, N1, N2_HC));

    state.newElement(
        "gradient_array_lh_ref",
        gradient_field_poisson_ref = new CArrayType(
            extents[range(startN0, startN0 + localN0)][N1][N2_HC],
            allocator_complex));
    gradient_field_poisson_ref->setRealDims(ArrayDimension(N0, N1, N2_HC));
  }
  FFTW_Complex_Array &grad_array = *gradient_field->array;
  FFTW_Complex_Array &grad_array_ref = *gradient_field_ref->array;
  FFTW_Complex_Array &grad_array_prior = *gradient_field_prior->array;
  FFTW_Complex_Array &grad_array_prior_ref = *gradient_field_prior_ref->array;
  FFTW_Complex_Array &grad_array_poisson = *gradient_field_poisson->array;
  FFTW_Complex_Array &grad_array_poisson_ref =
      *gradient_field_poisson_ref->array;
  adjust_field = state.get<IArrayType>("adjust_mode_multiplier");

  updateMass(state, state);
  if (startN0 == 0 && localN0 > 0)
    grad_array[0][0][0] = 0;
  initializeMomenta(state);

  computeGradientPsi_Prior(state, state, *s_hat_field->array, grad_array_prior);
  computeGradientPsi_Likelihood(
      state, state, *s_hat_field->array, grad_array_poisson, false);
  computeGradientPsi(state, state, *s_hat_field->array, grad_array);

  gradient_field_ref->eigen().fill(0);
  gradient_field_prior_ref->eigen().fill(0);
  gradient_field_poisson_ref->eigen().fill(0);

  Progress<LOG_INFO> &progress = Console::instance().start_progress<LOG_INFO>(
      "doing numerical gradient", N0 * N1 * N2_HC, 5);
  array::copyArray3d(s_hat, *s_hat_field->array);
  H0 = computeHamiltonian(state, state, s_hat, false);
  H0prior = computeHamiltonian_Prior(state, state, s_hat);
  H0poisson = computeHamiltonian_Likelihood(state, state, s_hat, false);
  for (int n0 = 0; n0 < N0; n0 += step) {
    for (int n1 = 0; n1 < N1; n1++) {
      for (int n2 = 0; n2 < N2_HC; n2++) {
        FFTW_Complex_Array::element backup;
        std::complex<double> pert_r, pert_i;
        double n_backup;

        bool oncore = (n0 >= startN0 && n0 < startN0 + localN0);

        if (n0 == 0 && n1 == 0 && n2 == 0)
          continue;

        if (oncore) {
          backup = s_hat[n0][n1][n2];
          n_backup = abs(backup);
          if (n_backup == 0)
            n_backup = 1;
          Console::instance().print<LOG_DEBUG>(
              format("n_backup=%lg") % n_backup);
          pert_r = backup + std::complex<double>(n_backup * epsilon, 0);
          s_hat[n0][n1][n2] = pert_r;
        }

        H1 = computeHamiltonian(state, state, s_hat, false);
        H1prior = computeHamiltonian_Prior(state, state, s_hat);
        H1poisson = computeHamiltonian_Likelihood(state, state, s_hat, false);

        if (oncore) {
          pert_i = backup + std::complex<double>(0, n_backup * epsilon);
          s_hat[n0][n1][n2] = pert_i;
        }

        H2 = computeHamiltonian(state, state, s_hat, false);
        H2prior = computeHamiltonian_Prior(state, state, s_hat);
        H2poisson = computeHamiltonian_Likelihood(state, state, s_hat, false);

        if (oncore) {
          grad_array_ref[n0][n1][n2] =
              std::complex<double>((H1), (H0)) / (n_backup * epsilon);
          grad_array_prior_ref[n0][n1][n2] =
              std::complex<double>((H1prior - H0prior), (H2prior - H0prior)) /
              (n_backup * epsilon);
          grad_array_poisson_ref[n0][n1][n2] =
              std::complex<double>(
                  (H1poisson - H0poisson), (H2poisson - H0poisson)) /
              (n_backup * epsilon);
          s_hat[n0][n1][n2] = backup;
        }

        long n = (n0 - startN0) * N1 * N2_HC + n1 * N2_HC + n2;
        progress.update(n);
      }
    }
  }

  progress.destroy();
}

void NUTSDensitySampler::generateRandomField(
    MarkovState &state, MarkovState &state) {
  ArrayType1d::ArrayType &pspec =
      *state.get<ArrayType1d>("powerspectrum")->array;
  IArrayType::ArrayType &adjust_array =
      *state.get<IArrayType>("adjust_mode_multiplier")->array;
  IArrayType::ArrayType &key_array = *state.get<IArrayType>("k_keys")->array;
  CArrayType::ArrayType &s_hat0 = *state.get<CArrayType>("s_hat_field")->array;
  ArrayType::ArrayType &s = *state.get<ArrayType>("s_field")->array;
  RandomGen *rgen = state.get<RandomGen>("random_generator");
  ConsoleContext<LOG_INFO> ctx("hades random signal generation");

  FFTW_Complex_Array s_hat(
      extents[range(startN0, startN0 + localN0)][N1][N2_HC], c_storage_order(),
      allocator_complex);

#pragma omp parallel for schedule(static)
  for (long n0 = startN0; n0 < startN0 + localN0; n0++) {
    for (long n1 = 0; n1 < N1; n1++) {
      for (long n2 = 0; n2 < N2_HC; n2++) {
        CArrayType::ArrayType::element &e = s_hat0[n0][n1][n2];
        int adjust = adjust_array[n0][n1][n2];
        if (adjust == 0) {
          e = 0;
          continue;
        }

        e = std::complex<double>(
            rgen->get().gaussian(), rgen->get().gaussian());
        int key = key_array[n0][n1][n2];
        double P = pspec[key];
        e *= sqrt(P * volume / adjust);
      }
    }
  }
  ctx.print("Generated numbers. Fix the Nyquist planes...");
  Hermiticity_fixup(s_hat0);
  if (startN0 == 0 && localN0 > 0)
    s_hat0[0][0][0] = 0;

  ctx.print("Scale and copy");
  array::scaleAndCopyArray3d(s_hat, s_hat0, 1 / volume, true);
  ctx.print("Doing DFT...");
  MFCalls::execute_c2r(synthesis_plan, s_hat.data(), tmp_real_field->data());

  array::scaleAndCopyArray3d(s, *tmp_real_field, 1, true);
}

NUTSDensitySampler::HamiltonianType
NUTSDensitySampler::computeHamiltonian(MarkovState &state, MarkovState &state) {
  FFTW_Complex_Array s_hat(
      extents[range(startN0, startN0 + localN0)][N1][N2_HC], c_storage_order(),
      allocator_complex);

  array::copyArray3d(s_hat, *state.get<CArrayType>("s_hat_field")->array);

  return computeHamiltonian_Likelihood(state, state, s_hat, false);
}
