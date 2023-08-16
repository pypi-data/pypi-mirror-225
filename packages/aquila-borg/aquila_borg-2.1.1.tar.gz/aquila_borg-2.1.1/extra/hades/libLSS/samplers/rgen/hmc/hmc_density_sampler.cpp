/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/samplers/rgen/hmc/hmc_density_sampler.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/cconfig.h"
#include <CosmoTool/algo.hpp>
#include <cmath>
#include <Eigen/Core>
#include <boost/format.hpp>
#include <functional>
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/tools/uninitialized_type.hpp"
#include <fstream>
#include <iostream>
#include "libLSS/samplers/core/generate_random_field.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"

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

HMCDensitySampler::HMCDensitySampler(
    MPI_Communication *comm, Likelihood_t likelihood, double k_max_,
    std::string const &prefix)
    : momentum_field(0), analysis_plan(0), synthesis_plan(0), attempt_field(0),
      accept_field(0), bad_sample(0), comm(comm), k_max(k_max_) {
  this->maxTime = 50;
  this->maxEpsilon = 0.01;
  this->likelihood = likelihood;
  setIntegratorScheme(HMCOption::SI_2A);
  setupNames(prefix);
}

void HMCDensitySampler::setupNames(std::string const &prefix) {
  momentum_field_name = prefix + "momentum_field";
  s_hat_field_name = prefix + "s_hat_field";
  s_field_name = prefix + "s_field";
  hades_attempt_count_name = prefix + "hades_attempt_count";
  hades_accept_count_name = prefix + "hades_accept_count";
  hmc_bad_sample_name = prefix + "hmc_bad_sample";
  hmc_force_save_final_name = prefix + "hmc_force_save_final";
  hmc_Elh_name = prefix + "hmc_Elh";
  hmc_Eprior_name = prefix + "hmc_Eprior";
}

void HMCDensitySampler::generateMockData(MarkovState &state) {
  likelihood->updateMetaParameters(state);
  if (!phaseFilename) {
    generateRandomField(state);
  }
  Console::instance().print<LOG_VERBOSE>(
      format("Max of s_field = %g") % fwrap(*s_field->array).max());
  likelihood->generateMockData(*s_hat_field->array, state);
}

void HMCDensitySampler::computeGradientPsi_Likelihood(
    MarkovState &state, CArrayRef const &s, CArrayRef &grad_array,
    bool accumulate) {
  double temp = state.getScalar<double>("ares_heat");
  if (posttransform) {
    BoxModel box = posttransform->get_box_model();
    posttransform->forwardModel_v2(ModelInput<3>(base_mgr, box, s));
    auto tmp_s = base_mgr->allocate_ptr_complex_array();
    posttransform->getDensityFinal(
        ModelOutput<3>(base_mgr, box, tmp_s->get_array()));

    likelihood->gradientLikelihood(*tmp_s, grad_array, accumulate, temp);
    tmp_s.reset();

    posttransform->adjointModel_v2(
        ModelInputAdjoint<3>(base_mgr, box, grad_array));
    posttransform->getAdjointModelOutput(
        ModelOutputAdjoint<3>(base_mgr, box, grad_array));
  } else {
    likelihood->gradientLikelihood(s, grad_array, accumulate, temp);
  }
}

double HMCDensitySampler::computeHamiltonian_Likelihood(
    MarkovState &state, CArrayRef const &s_hat, bool final_call) {
  double temp = state.getScalar<double>("ares_heat");
  Console::instance().print<LOG_VERBOSE>(
      format("[LIKELIHOOD] Temperature is %lg") % temp);

  if (posttransform) {
    BoxModel box = posttransform->get_box_model();
    posttransform->forwardModel_v2(ModelInput<3>(base_mgr, box, s_hat));
    auto tmp_s = base_mgr->allocate_ptr_complex_array();
    posttransform->getDensityFinal(
        ModelOutput<3>(base_mgr, box, tmp_s->get_array()));
    return likelihood->logLikelihood(tmp_s->get_array(), !final_call) * temp;
  } else

    return likelihood->logLikelihood(s_hat, !final_call) * temp;
}

void HMCDensitySampler::restore(MarkovState &state) { initialize(state); }

void HMCDensitySampler::initialize(MarkovState &state) {
  Console &cons = Console::instance();
  ConsoleContext<LOG_INFO_SINGLE> ctx("Initialize hades density sampler");

  N0 = state.getScalar<long>("N0");
  N1 = state.getScalar<long>("N1");
  N2 = state.getScalar<long>("N2");

  base_mgr = std::make_shared<DFT_Manager>(N0, N1, N2, comm);
  size_t Ntot = N0 * N1 * N2;

  L0 = state.getScalar<double>("L0");
  L1 = state.getScalar<double>("L1");
  L2 = state.getScalar<double>("L2");
  Ncat = state.getScalar<long>("NCAT");

  startN0 = base_mgr->startN0;
  localN0 = base_mgr->localN0;
  endN0 = startN0 + localN0;

  fixer = std::make_shared<Hermiticity_fixer<double, 3>>(base_mgr);

  ctx.format("Allocating s_hat_field field: %dx%dx%d", N0, N1, base_mgr->N2_HC);
  s_hat_field =
      new CArrayType(base_mgr->extents_complex(), base_mgr->allocator_complex);
  s_hat_field->setRealDims(ArrayDimension(N0, N1, base_mgr->N2_HC));
  s_field = new ArrayType(extents[range(startN0, startN0 + localN0)][N1][N2]);
  s_field->setRealDims(ArrayDimension(N0, N1, N2));
  cons.print<LOG_DEBUG>("Allocating momentum field");
  momentum_field =
      new CArrayType(base_mgr->extents_complex(), base_mgr->allocator_complex);
  momentum_field->setRealDims(ArrayDimension(N0, N1, base_mgr->N2_HC));

  // Pass the ownership to state
  state.newElement(momentum_field_name, momentum_field);
  state.newElement(s_hat_field_name, s_hat_field, true);
  state.newElement(s_field_name, s_field, true);
  state.newElement(hades_attempt_count_name, attempt_field = new SLong(), true);
  state.newElement(hades_accept_count_name, accept_field = new SLong(), true);
  bad_sample = state.newScalar<int>(hmc_bad_sample_name, 0);

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

  mass_field =
      new ArrayType(base_mgr->extents_complex(), base_mgr->allocator_real);
  mass_field->setRealDims(ArrayDimension(N0, N1, base_mgr->N2_HC));
  mass_field->eigen().fill(0);
  state.newElement("hades_mass", mass_field);

  state.newScalar(hmc_force_save_final_name, true);
  state.newScalar(hmc_Elh_name, 0.0, true);
  state.newScalar(hmc_Eprior_name, 0.0, true);

  auto tmp_field = base_mgr->allocate_array();
  synthesis_plan = base_mgr->create_c2r_plan(
      s_hat_field->array->data(), tmp_field.get_array().data());
  analysis_plan = base_mgr->create_r2c_plan(
      tmp_field.get_array().data(), s_hat_field->array->data());

  likelihood->initializeLikelihood(state);

  // Now load phases
  if (phaseFilename) {
    H5::H5File f(*phaseFilename, H5F_ACC_RDONLY);

    ctx.print("Read-in phase data");
    {
      U_Array<double, 3> tmp_x(
          base_mgr
              ->extents_real_strict()); // We need to allocate this temporary array to adapt shape.
      CosmoTool::hdf5_read_array(f, dataName, tmp_x.get_array(), false, true);

      ctx.print("Saving and Rescaling");
      fwrap(array::slice_array(*s_field->array, base_mgr->strict_range())) =
          fwrap(tmp_x.get_array());
    }

    auto tmp_field = base_mgr->allocate_array();
    fwrap(array::slice_array(tmp_field.get_array(), base_mgr->strict_range())) =
        fwrap(*s_field->array) * volNorm;

    ctx.print("Fourier transform");
    base_mgr->execute_r2c(
        analysis_plan, tmp_field.get_array().data(),
        s_hat_field->array->data());
  }
}

HMCDensitySampler::~HMCDensitySampler() {
  if (base_mgr) {
    Console::instance().print<LOG_INFO_SINGLE>("Cleaning up HMCDensitySampler");

    MFCalls::destroy_plan(analysis_plan);
    MFCalls::destroy_plan(synthesis_plan);
  }
}

auto HMCDensitySampler::free_phase_mask() {
  double kmax2 = k_max * k_max;

  return fwrap(b_fused_idx<double, 3>([this, kmax2](int a, int b, int c) {
    double kx = kmode(a, N0, L0);
    double ky = kmode(b, N1, L1);
    double kz = kmode(c, N2, L2);

    return (kx * kx + ky * ky + kz * kz) > kmax2;
  }));
}

void HMCDensitySampler::initializeMomenta(MarkovState &state) {
  CArrayType::ArrayType &momentum_array = *momentum_field->array;
  RandomGen *rgen = state.get<RandomGen>("random_generator");
  fwrap(momentum_array) = make_complex(
      rgen->get().gaussian(
          constant<double, 3>(M_SQRT2, base_mgr->extents_complex())),
      rgen->get().gaussian(
          constant<double, 3>(M_SQRT2, base_mgr->extents_complex())));

  fwrap(momentum_array) = fwrap(momentum_array) * free_phase_mask();
}

#include "hmc_kinetic.tcc"
#include "hmc_prior.tcc"

void HMCDensitySampler::computeGradientPsi(
    MarkovState &state, CArrayRef const &s, CArrayRef &grad_array) {
  array::fill(grad_array, 0);
  computeGradientPsi_Prior(state, s, grad_array);
  computeGradientPsi_Likelihood(state, s, grad_array, true);
  fwrap(grad_array) = fwrap(grad_array) * free_phase_mask();
}

HMCDensitySampler::HamiltonianType HMCDensitySampler::computeHamiltonian(
    MarkovState &state, CArrayRef const &s_hat, bool final_call) {
  ConsoleContext<LOG_DEBUG> ctx("hamiltonian computation");

  HamiltonianType Ekin = computeHamiltonian_Kinetic();
  ctx.print(format("Ekin = %lg") % double(Ekin));
  HamiltonianType Eprior = computeHamiltonian_Prior(state, s_hat);
  ctx.print(format("Eprior = %lg") % double(Eprior));
  HamiltonianType Elh = computeHamiltonian_Likelihood(state, s_hat, final_call);
  ctx.print(format("Elh = %lg") % double(Elh));

  return Ekin + Eprior + Elh;
}

void HMCDensitySampler::setTransforms(
    Model_t pretransform_, Model_t posttransform_) {
  pretransform = pretransform_;
  posttransform = posttransform_;
}

void HMCDensitySampler::setIntegratorScheme(IntegratorScheme scheme) {
  current_scheme = scheme;
  symp.setIntegratorScheme(scheme);
}

void HMCDensitySampler::doSympInt(MarkovState &state, CArrayRef &s_hat) {
  ConsoleContext<LOG_INFO_SINGLE> ctx("Symplectic integration");
  RandomGen *rgen = state.get<RandomGen>("random_generator");
  int Ntime;
  double epsilon;
  ArrayType::ArrayType &mass = *mass_field->array;
  CArrayType::ArrayType &momentum_array = *momentum_field->array;

  if (comm->rank() == ROOT_RANK) {
    lastEpsilon = epsilon = maxEpsilon * rgen->get().uniform();
    do {
      lastTime = Ntime = 1 + int(std::floor(rgen->get().uniform() * maxTime));
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

  symp.integrate(
      std::bind(
          &HMCDensitySampler::computeGradientPsi, this, std::ref(state), ph::_1,
          ph::_2),
      mass, epsilon, Ntime, s_hat, momentum_array, gradient_psi);
}

void HMCDensitySampler::updateMass(MarkovState &state) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  ArrayType::ArrayType &mass = *mass_field->array;

  fwrap(mass) = 1 / 2.0 * free_phase_mask();
}

void HMCDensitySampler::sample(MarkovState &state) {
  RandomGen *rgen = state.get<RandomGen>("random_generator");
  double HamiltonianInit, HamiltonianFinal, deltaH;
  ConsoleContext<LOG_INFO_SINGLE> ctx("hades density field sampler");
  //adjust_field = state.get<IArrayType>("adjust_mode_multiplier");

  auto s_hat_p = base_mgr->allocate_complex_array();
  auto &s_hat = s_hat_p.get_array();

  if (pretransform) {
    BoxModel box = pretransform->get_box_model();
    // We explicitly protect the input here.
    pretransform->forwardModel_v2(ModelInput<3>(
        base_mgr, box,
        (CArrayRef const &)*state.get<CArrayType>("s_hat_field")->array));
    pretransform->getDensityFinal(ModelOutput<3>(base_mgr, box, s_hat));
  } else
    array::copyArray3d(s_hat, *state.get<CArrayType>("s_hat_field")->array);

  updateMass(state);

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

  if (state.get<SBool>("hades_sampler_blocked")->value)
    return;

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
    //if (std::isnan(HamiltonianFinal)) { error_helper<ErrorBadState>("NaN in hamiltonian final"); }

  } catch (const ErrorLoadBalance &) {
    // Stop everything now
    state.getScalar<int>(hmc_bad_sample_name)++;
    if (HMC_PERF_TEST && comm->rank() == ROOT_RANK) {
      std::ofstream f("hmc_performance.txt", std::ios::app);
      boost::chrono::duration<double> compute_time =
          boost::chrono::system_clock::now() - time_start;

      f << format("% 10.5le % 6d % 15.15le % 15.15le %d 0 0") % lastEpsilon %
               lastTime % 0 % compute_time.count() % int(current_scheme)
        << std::endl;
    }
    return;
  }
  double log_u;

  ctx.format(
      "init_Ekin=%g, init_Eprior=%g, init_Elh=%g, final_Ekin=%g, "
      "final_Eprior=%g, final_Elh=%g",
      init_Ekin, init_Eprior, init_Elh, final_Ekin, final_Eprior, final_Elh);

  deltaH = HamiltonianFinal - HamiltonianInit;
  if (comm->rank() == ROOT_RANK)
    log_u = log(rgen->get().uniform());

  comm->broadcast_t(&log_u, 1, ROOT_RANK);

  if (attempt_field)
    attempt_field->value++;
  ctx.print2<LOG_INFO_SINGLE>(
      format("log_u = %lg, deltaH = %lg") % log_u % deltaH);
  if (HMC_PERF_TEST && comm->rank() == ROOT_RANK) {
    std::ofstream f("hmc_performance.txt", std::ios::app);
    boost::chrono::duration<double> compute_time =
        boost::chrono::system_clock::now() - time_start;

    f << format("% 10.5le % 6d % 15.15le % 15.15le %d % 15.15le 0 %d") %
             lastEpsilon % lastTime % deltaH % compute_time.count() %
             int(current_scheme) % HamiltonianFinal % (log_u <= -deltaH)
      << std::endl;
  }

  if (log_u <= -deltaH) {
    // Accept the move
    if (comm->rank() == ROOT_RANK)
      ctx.print("accepting the move");

    likelihood->commitAuxiliaryFields(state);

    state.getScalar<double>(hmc_Elh_name) = final_Elh;
    state.getScalar<double>(hmc_Eprior_name) = final_Eprior;

    auto tmp_real_field = base_mgr->allocate_array();
    fixer->forward(s_hat);
    if (posttransform) {
      BoxModel box = posttransform->get_box_model();
      posttransform->forwardModel_v2(ModelInput<3>(base_mgr, box, s_hat));
      posttransform->getDensityFinal(ModelOutput<3>(
          base_mgr, box, *state.get<CArrayType>(s_hat_field_name)->array));
      LibLSS::copy_array(
          s_hat, *state.get<CArrayType>(s_hat_field_name)->array);
    } else {
      LibLSS::copy_array(
          *state.get<CArrayType>(s_hat_field_name)->array, s_hat);
    }
    base_mgr->execute_c2r(
        synthesis_plan, s_hat.data(), tmp_real_field.get_array().data());

    // This one handles padded and unpadded data through multi_array
    array::scaleAndCopyArray3d(
        *state.get<ArrayType>(s_field_name)->array, tmp_real_field.get_array(),
        1. / volume, true);

    if (accept_field)
      accept_field->value++;
  } else {
    state.getScalar<double>(hmc_Elh_name) = init_Elh;
    state.getScalar<double>(hmc_Eprior_name) = init_Eprior;
  }
}

void HMCDensitySampler::checkGradientReal(MarkovState &state, int step) {
  ConsoleContext<LOG_DEBUG> ctx("checkGradientReal");
  HamiltonianType H0, H1, H2;
  HamiltonianType H0prior, H1prior, H2prior;
  HamiltonianType H0poisson, H1poisson, H2poisson;
  auto s_hat_p = base_mgr->allocate_complex_array();
  auto &s_hat = s_hat_p.get_array();
  double epsilon = 0.001;

  ArrayType *gradient_field_lh, *gradient_field_lh_ref;
  ArrayType *s_field = state.get<ArrayType>(s_field_name);

  if (state.exists("gradient_array_lh_real")) {
    gradient_field_lh = state.get<ArrayType>("gradient_array_lh_real");
    gradient_field_lh_ref = state.get<ArrayType>("gradient_array_lh_ref_real");
  } else {
    auto real_dim =
        ArrayDimension(base_mgr->N0, base_mgr->N1, base_mgr->N2real);

    state.newElement(
        "gradient_array_lh_real",
        gradient_field_lh =
            new ArrayType(base_mgr->extents_real(), base_mgr->allocator_real));
    gradient_field_lh->setRealDims(real_dim);

    state.newElement(
        "gradient_array_lh_ref_real",
        gradient_field_lh_ref =
            new ArrayType(base_mgr->extents_real(), base_mgr->allocator_real));
    gradient_field_lh_ref->setRealDims(real_dim);
  }

  auto &gradient_array_lh = *gradient_field_lh->array;
  auto &gradient_array_lh_ref = *gradient_field_lh_ref->array;
  auto &s = *s_field->array;

  double log_L0, log_L1, log_L2;
  likelihood->gradientLikelihood(s, gradient_array_lh, false, 1.0);

  log_L0 = likelihood->logLikelihood(s, false);
  Progress<LOG_INFO_SINGLE> &progress =
      Console::instance().start_progress<LOG_INFO_SINGLE>(
          "doing numerical gradient (real)",
          base_mgr->N0 * base_mgr->N1 * base_mgr->N2, 5);

  for (int n0 = 0; n0 < N0; n0 += step) {
    for (int n1 = 0; n1 < N1; n1++) {
      for (int n2 = 0; n2 < base_mgr->N2; n2++) {
        double backup;
        double pert;
        double n_backup;

        bool oncore = base_mgr->on_core(n0);

        if (n0 == 0 && n1 == 0 && n2 == 0)
          continue;

        if (oncore) {
          backup = s[n0][n1][n2];
          n_backup = abs(backup);
          if (n_backup == 0)
            n_backup = 1;
          pert = backup + n_backup * epsilon;
          s[n0][n1][n2] = pert;
        }

        log_L1 = likelihood->logLikelihood(s, false);

        if (oncore) {
          gradient_array_lh_ref[n0][n1][n2] =
              (log_L1 - log_L0) / (n_backup * epsilon);
          s[n0][n1][n2] = backup;
        }

        long n = ((n0 - startN0) * N1 + n1) * base_mgr->N2 + n2;
        progress.update(n);
      }
    }
  }
}

void HMCDensitySampler::checkGradient(MarkovState &state, int step) {
  ConsoleContext<LOG_DEBUG> ctx("checkGradient");
  HamiltonianType H0, H1, H2;
  HamiltonianType H0prior, H1prior, H2prior;
  HamiltonianType H0poisson, H1poisson, H2poisson;
  auto s_hat_p = base_mgr->allocate_complex_array();
  auto &s_hat = s_hat_p.get_array();
  double epsilon = 0.01;

  CArrayType *gradient_field, *gradient_field_ref;
  CArrayType *gradient_field_prior, *gradient_field_prior_ref;
  CArrayType *gradient_field_poisson, *gradient_field_poisson_ref;
  CArrayType *s_hat_field = state.get<CArrayType>(s_hat_field_name);

  if (state.exists("gradient_array")) {
    gradient_field = state.get<CArrayType>("gradient_array");
    gradient_field_prior = state.get<CArrayType>("gradient_array_prior");
    gradient_field_poisson = state.get<CArrayType>("gradient_array_lh");
    gradient_field_ref = state.get<CArrayType>("gradient_array_ref");
    gradient_field_prior_ref =
        state.get<CArrayType>("gradient_array_prior_ref");
    gradient_field_poisson_ref = state.get<CArrayType>("gradient_array_lh_ref");
  } else {
    auto complex_dim =
        ArrayDimension(base_mgr->N0, base_mgr->N1, base_mgr->N2_HC);
    state.newElement(
        "gradient_array",
        gradient_field = new CArrayType(
            base_mgr->extents_complex(), base_mgr->allocator_complex));
    gradient_field->setRealDims(complex_dim);

    state.newElement(
        "gradient_array_ref",
        gradient_field_ref = new CArrayType(
            base_mgr->extents_complex(), base_mgr->allocator_complex));
    gradient_field_ref->setRealDims(complex_dim);

    state.newElement(
        "gradient_array_prior",
        gradient_field_prior = new CArrayType(
            base_mgr->extents_complex(), base_mgr->allocator_complex));
    gradient_field_prior->setRealDims(complex_dim);

    state.newElement(
        "gradient_array_prior_ref",
        gradient_field_prior_ref = new CArrayType(
            base_mgr->extents_complex(), base_mgr->allocator_complex));
    gradient_field_prior_ref->setRealDims(complex_dim);

    state.newElement(
        "gradient_array_lh",
        gradient_field_poisson = new CArrayType(
            base_mgr->extents_complex(), base_mgr->allocator_complex));
    gradient_field_poisson->setRealDims(complex_dim);

    state.newElement(
        "gradient_array_lh_ref",
        gradient_field_poisson_ref = new CArrayType(
            base_mgr->extents_complex(), base_mgr->allocator_complex));
    gradient_field_poisson_ref->setRealDims(complex_dim);
  }
  FFTW_Complex_Array &grad_array = *gradient_field->array;
  FFTW_Complex_Array &grad_array_ref = *gradient_field_ref->array;
  FFTW_Complex_Array &grad_array_prior = *gradient_field_prior->array;
  FFTW_Complex_Array &grad_array_prior_ref = *gradient_field_prior_ref->array;
  FFTW_Complex_Array &grad_array_poisson = *gradient_field_poisson->array;
  FFTW_Complex_Array &grad_array_poisson_ref =
      *gradient_field_poisson_ref->array;
  //adjust_field = state.get<IArrayType>("adjust_mode_multiplier");

  updateMass(state);
  if (startN0 == 0 && localN0 > 0)
    grad_array[0][0][0] = 0;
  ctx.print("Initialize momenta");
  initializeMomenta(state);

  ctx.print("Compute for prior");
  computeGradientPsi_Prior(state, *s_hat_field->array, grad_array_prior);
  ctx.print("Compute for likelihood");
  computeGradientPsi_Likelihood(
      state, *s_hat_field->array, grad_array_poisson, false);
  ctx.print("Compute for both");
  computeGradientPsi(state, *s_hat_field->array, grad_array);

  gradient_field_ref->eigen().fill(0);
  gradient_field_prior_ref->eigen().fill(0);
  gradient_field_poisson_ref->eigen().fill(0);

  Progress<LOG_INFO_SINGLE> &progress =
      Console::instance().start_progress<LOG_INFO_SINGLE>(
          "doing numerical gradient",
          base_mgr->N0 * base_mgr->N1 * base_mgr->N2_HC, 5);
  array::copyArray3d(s_hat, *s_hat_field->array);
  H0 = computeHamiltonian(state, s_hat, false);
  H0prior = computeHamiltonian_Prior(state, s_hat);
  H0poisson = computeHamiltonian_Likelihood(state, s_hat, false);
  for (int n0 = 0; n0 < N0; n0 += step) {
    for (int n1 = 0; n1 < N1; n1++) {
      for (int n2 = 0; n2 < base_mgr->N2_HC; n2++) {
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

        H1 = computeHamiltonian(state, s_hat, false);
        H1prior = computeHamiltonian_Prior(state, s_hat);
        H1poisson = computeHamiltonian_Likelihood(state, s_hat, false);

        if (oncore) {
          pert_i = backup + std::complex<double>(0, n_backup * epsilon);
          s_hat[n0][n1][n2] = pert_i;
        }

        H2 = computeHamiltonian(state, s_hat, false);
        H2prior = computeHamiltonian_Prior(state, s_hat);
        H2poisson = computeHamiltonian_Likelihood(state, s_hat, false);

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

        long n = ((n0 - startN0) * N1 + n1) * base_mgr->N2_HC + n2;
        progress.update(n);
      }
    }
  }

  progress.destroy();
}

void HMCDensitySampler::generateRandomField(MarkovState &state) {
  LibLSS::generateRandomField(comm, state);
}

HMCDensitySampler::HamiltonianType
HMCDensitySampler::computeHamiltonian(MarkovState &state, bool gradient_next) {
  auto s_hat_p = base_mgr->allocate_complex_array();
  auto &s_hat = s_hat_p.get_array();

  array::copyArray3d(s_hat, *state.get<CArrayType>(s_hat_field_name)->array);

  return computeHamiltonian_Likelihood(state, s_hat, gradient_next);
}
