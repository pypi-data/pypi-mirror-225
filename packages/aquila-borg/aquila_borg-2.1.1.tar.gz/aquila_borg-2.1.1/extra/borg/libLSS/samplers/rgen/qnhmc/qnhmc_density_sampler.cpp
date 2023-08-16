/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/rgen/qnhmc/qnhmc_density_sampler.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <CosmoTool/algo.hpp>
#include <cmath>
#include <Eigen/Core>
#include <boost/format.hpp>
#include <functional>
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/samplers/rgen/qnhmc/qnhmc_density_sampler.hpp"
#include "libLSS/tools/uninitialized_type.hpp"
#include "libLSS/tools/hermiticity_fixup.hpp"
#include <fstream>
#include <iostream>
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/samplers/core/generate_random_field.hpp"

static const bool ULTRA_VERBOSE = false;
static const bool HMC_PERF_TEST = true;
static const bool FIXED_INTEGRATION_PATH = false;

using namespace LibLSS;
using boost::extents;
using boost::format;

using CosmoTool::square;

using boost::c_storage_order;
typedef boost::multi_array_types::extent_range range;

typedef Eigen::Map<Eigen::ArrayXd, Eigen::Aligned> MappedArray;

static const int ROOT_RANK = 0;

namespace ph = std::placeholders;

QNHMCDensitySampler::QNHMCDensitySampler(
    MPI_Communication *comm, Likelihood_t likelihood)
    : momentum_field(0), analysis_plan(0), synthesis_plan(0), attempt_field(0),
      accept_field(0), bad_sample(0), comm(comm), B(20), C(20) {
  this->maxTime = 50;
  this->maxEpsilon = 0.01;
  this->likelihood = likelihood;
  B.setStrictMode(false);
  C.setStrictMode(false);
  setIntegratorScheme(QNHMCOption::SI_2A);
}

void QNHMCDensitySampler::generateMockData(MarkovState &state) {
  likelihood->updateMetaParameters(state);
  generateRandomField(comm, state);
  Console::instance().print<LOG_VERBOSE>(
      format("Max of s_field = %g") % fwrap(*s_field->array).max());
  likelihood->generateMockData(*s_hat_field->array, state);
}

double QNHMCDensitySampler::computeHamiltonian_Prior(
    MarkovState &state, CArrayRef const &s) {
  auto sr = std::real(fwrap(s));
  auto si = std::imag(fwrap(s));
  return (sr * sr + si * si).sum();
}

void QNHMCDensitySampler::computeGradientPsi_Prior(
    MarkovState &state, CArrayRef const &s, CArrayRef &grad_array) {
  fwrap(grad_array) = 2.0 * fwrap(s);
}

void QNHMCDensitySampler::computeGradientPsi_Likelihood(
    MarkovState &state, CArrayRef const &s, CArrayRef &grad_array,
    bool accumulate) {
  double temp = state.getScalar<double>("ares_heat");
  likelihood->gradientLikelihood(s, grad_array, accumulate, temp);
}

double QNHMCDensitySampler::computeHamiltonian_Likelihood(
    MarkovState &state, CArrayRef const &s_hat, bool final_call) {
  double temp = state.getScalar<double>("ares_heat");
  Console::instance().print<LOG_VERBOSE>(
      format("[LIKELIHOOD] Temperature is %lg") % temp);

  return likelihood->logLikelihood(s_hat, !final_call) * temp;
}

void QNHMCDensitySampler::restore(MarkovState &state) { initialize(state); }

void QNHMCDensitySampler::initialize(MarkovState &state) {
  Console &cons = Console::instance();
  ConsoleContext<LOG_INFO_SINGLE> ctx("Initialize hades density sampler");

  N0 = state.getScalar<long>("N0");
  N1 = state.getScalar<long>("N1");
  N2 = state.getScalar<long>("N2");

  base_mgr = std::make_shared<DFT_Manager>(N0, N1, N2, comm);
  size_t Ntot = N0 * N1 * N2;

  L0 = state.getScalar<double>("L0");
  L1 = state.getScalar<double>("L0");
  L2 = state.getScalar<double>("L0");
  Ncat = state.getScalar<long>("NCAT");

  startN0 = base_mgr->startN0;
  localN0 = base_mgr->localN0;
  endN0 = startN0 + localN0;

  cons.print<LOG_DEBUG>("Allocating s field");
  s_hat_field = new CArrayType(base_mgr->extents_complex(), allocator_complex);
  s_hat_field->setRealDims(ArrayDimension(N0, N1, base_mgr->N2_HC));
  s_field = new ArrayType(extents[range(startN0, startN0 + localN0)][N1][N2]);
  s_field->setRealDims(ArrayDimension(N0, N1, N2));
  cons.print<LOG_DEBUG>("Allocating momentum field");
  momentum_field =
      new CArrayType(base_mgr->extents_complex(), allocator_complex);
  momentum_field->setRealDims(ArrayDimension(N0, N1, base_mgr->N2_HC));

  // Pass the ownership to state
  state.newElement("momentum_field", momentum_field);
  state.newElement("s_hat_field", s_hat_field, true);
  state.newElement("s_field", s_field, true);
  state.newElement("hades_attempt_count", attempt_field = new SLong(), true);
  state.newElement("hades_accept_count", accept_field = new SLong(), true);
  bad_sample = state.newScalar<int>("hmc_bad_sample", 0);

  attempt_field->value = 0;
  accept_field->value = 0;
  attempt_field->setResetOnSave(0);
  accept_field->setResetOnSave(0);
  bad_sample->setResetOnSave(0);

  s_hat_field->eigen().fill(0);
  s_field->eigen().fill(0);
  momentum_field->eigen().fill(0);

  volume = L0 * L1 * L2;
  volNorm = volume / Ntot;

  state.newScalar("hmc_force_save_final", true);
  state.newScalar("hmc_Elh", 0.0, true);
  state.newScalar("hmc_Eprior", 0.0, true);

  auto tmp_field = base_mgr->allocate_array();
  synthesis_plan = base_mgr->create_c2r_plan(
      s_hat_field->array->data(), tmp_field.get_array().data());
  analysis_plan = base_mgr->create_r2c_plan(
      tmp_field.get_array().data(), s_hat_field->array->data());

  likelihood->initializeLikelihood(state);
}

QNHMCDensitySampler::~QNHMCDensitySampler() {
  if (base_mgr) {
    Console::instance().print<LOG_INFO_SINGLE>(
        "Cleaning up QNHMCDensitySampler");

    MFCalls::destroy_plan(analysis_plan);
    MFCalls::destroy_plan(synthesis_plan);
  }
}

void QNHMCDensitySampler::Hermiticity_fixup(CArrayRef &a) {
  Hermiticity_fixer<double, 3> fixer(base_mgr);

  fixer.forward(a);
}

QNHMCDensitySampler::HamiltonianType
QNHMCDensitySampler::computeHamiltonian_Kinetic() {
  CArrayType::ArrayType &momentum_array = *momentum_field->array;

  auto m_w = fwrap(momentum_array);
  auto r = std::real(m_w);
  auto i = std::imag(m_w);

  double Ekin = (r * r + i * i).sum() / (2.);
  comm->all_reduce_t(MPI_IN_PLACE, &Ekin, 1, MPI_SUM);
  return 0.5 * Ekin;
}

void QNHMCDensitySampler::initializeMomenta(MarkovState &state) {
  CArrayType::ArrayType &momentum_array = *momentum_field->array;
  RandomGen *rgen = state.get<RandomGen>("random_generator");

  fwrap(momentum_array) = make_complex(
      rgen->get().gaussian(
          constant<double, 3>(M_SQRT2, base_mgr->extents_complex())),
      rgen->get().gaussian(
          constant<double, 3>(M_SQRT2, base_mgr->extents_complex())));

  //fwrap(momentum_array) = fwrap(momentum_array) * free_phase_mask();
}

void QNHMCDensitySampler::computeGradientPsi(
    MarkovState &state, CArrayRef const &s, CArrayRef &grad_array) {
  computeGradientPsi_Prior(state, s, grad_array);
  computeGradientPsi_Likelihood(state, s, grad_array, true);
}

QNHMCDensitySampler::HamiltonianType QNHMCDensitySampler::computeHamiltonian(
    MarkovState &state, CArrayRef const &s_hat, bool final_call) {
  ConsoleContext<LOG_DEBUG> ctx("hamiltonian computation");

  HamiltonianType Ekin = computeHamiltonian_Kinetic();
  HamiltonianType Eprior = computeHamiltonian_Prior(state, s_hat);
  HamiltonianType Elh = computeHamiltonian_Likelihood(state, s_hat, final_call);

  ctx.print(format("Ekin = %lg") % double(Ekin));
  ctx.print(format("Eprior = %lg") % double(Eprior));
  ctx.print(format("Elh = %lg") % double(Elh));

  return Ekin + Eprior + Elh;
}

void QNHMCDensitySampler::setIntegratorScheme(IntegratorScheme scheme) {
  current_scheme = scheme;
  symp.setIntegratorScheme(scheme);
}

void QNHMCDensitySampler::doSympInt(MarkovState &state, CArrayRef &s_hat) {
  ConsoleContext<LOG_INFO_SINGLE> ctx("Symplectic integration");
  RandomGen *rgen = state.get<RandomGen>("random_generator");
  int Ntime;
  double epsilon;
  CArrayType::ArrayType &momentum_array = *momentum_field->array;

  if (comm->rank() == ROOT_RANK) {
    lastEpsilon = epsilon = maxEpsilon * rgen->get().uniform();
    do {
      lastTime = Ntime = int(rgen->get().uniform() * maxTime);
    } while (Ntime == 0);
  }

  if (HMC_PERF_TEST && FIXED_INTEGRATION_PATH) {
    epsilon = maxEpsilon;
    Ntime = maxTime;
  }

  comm->broadcast_t(&epsilon, 1, ROOT_RANK);
  comm->broadcast_t(&Ntime, 1, ROOT_RANK);

  ctx.print(format("epsilon = %lg, Ntime = %d") % epsilon % Ntime);

  auto gradient_psi_p = base_mgr->allocate_complex_array();
  auto &gradient_psi = gradient_psi_p.get_array();

  symp.integrate_dense(
      [this, &state](auto const &position, auto &p) {
        this->computeGradientPsi(state, position, p);
        B.storeNewStep(p, position);
        C.computeNextDirection(comm, p, p, p);
      },
      [this](auto const &p, auto &ptmp) {
        fwrap(ptmp) = 0.5*fwrap(p);
        C.computeNextDirection(comm, ptmp, ptmp, ptmp);
        return fwrap(ptmp);
      },
      epsilon, Ntime, s_hat, momentum_array, gradient_psi);
}

void QNHMCDensitySampler::sample(MarkovState &state) {
  RandomGen *rgen = state.get<RandomGen>("random_generator");
  double HamiltonianInit, HamiltonianFinal, deltaH;
  ConsoleContext<LOG_INFO_SINGLE> ctx("QN-HMC density field sampler");

  if (state.get<SBool>("hades_sampler_blocked")->value)
    return;

  auto s_hat_p = base_mgr->allocate_complex_array();
  auto &s_hat = s_hat_p.get_array();

  array::copyArray3d(s_hat, *state.get<CArrayType>("s_hat_field")->array);
  //    checkHermiticity(s_hat);

  likelihood->updateMetaParameters(state);
  initializeMomenta(state);

  HamiltonianType init_Ekin = computeHamiltonian_Kinetic();
  HamiltonianType init_Eprior = computeHamiltonian_Prior(state, s_hat);
  HamiltonianType init_Elh = computeHamiltonian_Likelihood(state, s_hat, false);
  HamiltonianInit = init_Ekin + init_Eprior +
                    init_Elh; //computeHamiltonian(state, s_hat, false);
  // If we are the very first step, save the result of the forward model for the other samplers.
  bool &force_save = state.getScalar<bool>("hmc_force_save_final");
  if (state.get<SLong>("MCMC_STEP")->value == 0 || force_save) {
    likelihood->commitAuxiliaryFields(state);
    force_save = false;
  }

  boost::chrono::system_clock::time_point time_start;
  if (HMC_PERF_TEST) {
    time_start = boost::chrono::system_clock::now();
  }

  HamiltonianType final_Ekin = 0;
  HamiltonianType final_Eprior = 0;
  HamiltonianType final_Elh = 0;

  try {
    if (std::isnan(HamiltonianInit)) {
      error_helper<ErrorBadState>("NaN in hamiltonian initial");
    }
    doSympInt(state, s_hat);
    final_Ekin = computeHamiltonian_Kinetic();
    final_Eprior = computeHamiltonian_Prior(state, s_hat);
    final_Elh = computeHamiltonian_Likelihood(state, s_hat, true);
    HamiltonianFinal = final_Ekin + final_Eprior + final_Elh;
  } catch (const ErrorLoadBalance &) {
    // Stop everything now
    state.getScalar<int>("hmc_bad_sample")++;
    return;
  }
  double log_u;

  deltaH = HamiltonianFinal - HamiltonianInit;
  if (HMC_PERF_TEST && comm->rank() == ROOT_RANK) {
    std::ofstream f("hmc_performance.txt", std::ios::app);
    boost::chrono::duration<double> compute_time =
        boost::chrono::system_clock::now() - time_start;

    f << format("% 10.5le % 6d % 15.15le % 15.15le %d % 15.15le") %
             lastEpsilon % lastTime % deltaH % compute_time.count() %
             int(current_scheme) % HamiltonianFinal
      << std::endl;
  }

  if (comm->rank() == ROOT_RANK)
    log_u = log(rgen->get().uniform());

  comm->broadcast_t(&log_u, 1, ROOT_RANK);

  if (attempt_field)
    attempt_field->value++;
  ctx.print2<LOG_VERBOSE>(
      boost::format("init_Ekin = %g, final_Ekin = %g") % init_Ekin %
      final_Ekin);
  ctx.print2<LOG_INFO_SINGLE>(
      format("log_u = %lg, deltaH = %lg, deltaH_kin = %lg, deltaH_prior = %lg, "
             "deltaH_likelihood = %lg") %
      log_u % deltaH % (final_Ekin - init_Ekin) % (final_Eprior - init_Eprior) %
      (final_Elh - init_Elh));
  if (log_u <= -deltaH) {
    // Accept the move
    ctx.print2<LOG_INFO_SINGLE>("accepting the move");

    likelihood->commitAuxiliaryFields(state);

    state.getScalar<double>("hmc_Elh") = final_Elh;
    state.getScalar<double>("hmc_Eprior") = final_Eprior;

    ctx.print2<LOG_VERBOSE>("Hermiticity fixup");
    Hermiticity_fixup(s_hat);

    auto tmp_real_field = base_mgr->allocate_array();
    ctx.print2<LOG_VERBOSE>("Building s_field");
    array::copyArray3d(*state.get<CArrayType>("s_hat_field")->array, s_hat);
    base_mgr->execute_c2r(
        synthesis_plan, s_hat.data(), tmp_real_field.get_array().data());

    // This one handles padded and unpadded data through multi_array
    array::scaleAndCopyArray3d(
        *state.get<ArrayType>("s_field")->array, tmp_real_field.get_array(),
        1. / volume, true);

    ctx.print2<LOG_VERBOSE>("Saving B matrix");
    C = B;
    ctx.print2<LOG_VERBOSE>("Done");

    if (accept_field)
      accept_field->value++;
  } else {
    state.getScalar<double>("hmc_Elh") = init_Elh;
    state.getScalar<double>("hmc_Eprior") = init_Eprior;
    B = C;
  }
}

QNHMCDensitySampler::HamiltonianType QNHMCDensitySampler::computeHamiltonian(
    MarkovState &state, bool gradient_next) {
  auto s_hat_p = base_mgr->allocate_complex_array();
  auto &s_hat = s_hat_p.get_array();

  array::copyArray3d(s_hat, *state.get<CArrayType>("s_hat_field")->array);

  return computeHamiltonian_Likelihood(state, s_hat, gradient_next);
}
