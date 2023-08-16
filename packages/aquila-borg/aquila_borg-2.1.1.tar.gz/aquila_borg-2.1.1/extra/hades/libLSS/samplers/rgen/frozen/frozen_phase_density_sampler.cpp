/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/samplers/rgen/frozen/frozen_phase_density_sampler.cpp
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
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/samplers/rgen/frozen/frozen_phase_density_sampler.hpp"
#include "libLSS/tools/uninitialized_type.hpp"
#include "libLSS/tools/hermiticity_fixup.hpp"
#include <fstream>
#include <iostream>
#include <H5Cpp.h>

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

FrozenPhaseDensitySampler::FrozenPhaseDensitySampler(
    MPI_Communication *comm, Likelihood_t likelihood)
    : analysis_plan(0), synthesis_plan(0), comm(comm) {
  this->likelihood = likelihood;
}

void FrozenPhaseDensitySampler::generateMockData(MarkovState &state) {
  likelihood->updateMetaParameters(state);

  auto &rgen = state.get<RandomGen>("random_generator")->get();

  {
    auto tmp_real = base_mgr->allocate_array();
    double const inv_sqN = 1.0 / std::sqrt(N0 * N1 * N2);

    // Generate a bunch of gaussian distributed random number (variance 1)
    fwrap(tmp_real.get_array()) =
        rgen.gaussian(ones<double, 3>(base_mgr->extents_real()) * inv_sqN);

    base_mgr->execute_r2c(
        analysis_plan, tmp_real.get_array().data(), x_hat_field->array->data());

    fwrap(*s_hat_field->array) = fwrap(*x_hat_field->array);
  }
  auto tmp_complex = base_mgr->allocate_complex_array();
  fwrap(tmp_complex.get_array()) = fwrap(*s_hat_field->array) / volume;

  base_mgr->execute_c2r(
      synthesis_plan, tmp_complex.get_array().data(), s_field->array->data());

  likelihood->generateMockData(*s_hat_field->array, state);
}

void FrozenPhaseDensitySampler::initialize(MarkovState &state) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  restore(state);

  // Now load phases
  if (phaseFilename) {
    H5::H5File f(*phaseFilename, H5F_ACC_RDONLY);

    ctx.print("Read-in phase data");
    {
      U_Array<double, 3> tmp_x(
          base_mgr
              ->extents_real_strict()); // We need to allocate this temporary array to adapt shape.
      CosmoTool::hdf5_read_array(f, dataName, tmp_x.get_array(), false, true);

      // FS: updated according to GL, 6/23/20
      fwrap(array::slice_array(*x_field->array, base_mgr->strict_range())) = fwrap(tmp_x.get_array());
    }

    auto tmp_field = base_mgr->allocate_array();
    fwrap(tmp_field.get_array()) = fwrap(*x_field->array) * volNorm;

    ctx.print("Fourier transform");
    base_mgr->execute_r2c(
        analysis_plan, tmp_field.get_array().data(),
        x_hat_field->array->data());

    fwrap(*s_hat_field->array) = fwrap(*x_hat_field->array);
    // WARNING: s_field/s_hat_field are not consistent at that moment. They will become at the first
    //          call to sample here.
  }
}

void FrozenPhaseDensitySampler::restore(MarkovState &state) {
  Console &cons = Console::instance();
  ConsoleContext<LOG_DEBUG> ctx("Initialize frozen density sampler");

  N0 = state.getScalar<long>("N0");
  N1 = state.getScalar<long>("N1");
  N2 = state.getScalar<long>("N2");

  base_mgr = std::unique_ptr<DFT_Manager>(new DFT_Manager(N0, N1, N2, comm));
  size_t Ntot = N0 * N1 * N2;

  L0 = state.getScalar<double>("L0");
  L1 = state.getScalar<double>("L1");
  L2 = state.getScalar<double>("L2");

  startN0 = base_mgr->startN0;
  localN0 = base_mgr->localN0;
  endN0 = startN0 + localN0;

  cons.print<LOG_DEBUG>("Allocating s field");
  s_hat_field =
      new CArrayType(base_mgr->extents_complex(), base_mgr->allocator_complex);
  s_hat_field->setRealDims(ArrayDimension(N0, N1, base_mgr->N2_HC));
  x_hat_field =
      new CArrayType(base_mgr->extents_complex(), base_mgr->allocator_complex);
  x_hat_field->setRealDims(ArrayDimension(N0, N1, base_mgr->N2_HC));
  x_field = new ArrayType(base_mgr->extents_real(), base_mgr->allocator_real);
  x_field->setRealDims(ArrayDimension(N0, N1, base_mgr->N2real));
  s_field = new ArrayType(base_mgr->extents_real(), base_mgr->allocator_real);
  s_field->setRealDims(ArrayDimension(N0, N1, base_mgr->N2real));

  cons.print<LOG_DEBUG>("Allocating momentum field");

  // Pass the ownership to state
  state.newElement("s_hat_field", s_hat_field, true);
  state.newElement("s_field", s_field);
  state.newElement("x_hat_field", x_hat_field);
  state.newElement("x_field", x_field);

  fwrap(*x_hat_field->array) = 0;
  fwrap(*x_field->array) = 0;

  volume = L0 * L1 * L2;
  volNorm = volume / Ntot;

  state.newScalar("hmc_force_save_final", true);

  auto tmp_field = base_mgr->allocate_array();
  synthesis_plan = base_mgr->create_c2r_plan(
      x_hat_field->array->data(), tmp_field.get_array().data());
  analysis_plan = base_mgr->create_r2c_plan(
      tmp_field.get_array().data(), x_hat_field->array->data());

  likelihood->initializeLikelihood(state);
}

FrozenPhaseDensitySampler::~FrozenPhaseDensitySampler() {
  if (base_mgr) {
    MFCalls::destroy_plan(analysis_plan);
    MFCalls::destroy_plan(synthesis_plan);
  }
}

void FrozenPhaseDensitySampler::sample(MarkovState &state) {
  ConsoleContext<LOG_INFO_SINGLE> ctx("hades density field sampler");

  fwrap(*s_hat_field->array) =
      fwrap(*state.get<CArrayType>("x_hat_field")->array);

  auto tmp_complex = base_mgr->allocate_complex_array();
  fwrap(tmp_complex.get_array()) = fwrap(*s_hat_field->array) / volume;

  base_mgr->execute_c2r(
      synthesis_plan, tmp_complex.get_array().data(), s_field->array->data());

  likelihood->updateMetaParameters(state);
  likelihood->logLikelihood(*s_hat_field->array, false);
  likelihood->commitAuxiliaryFields(state);
}
