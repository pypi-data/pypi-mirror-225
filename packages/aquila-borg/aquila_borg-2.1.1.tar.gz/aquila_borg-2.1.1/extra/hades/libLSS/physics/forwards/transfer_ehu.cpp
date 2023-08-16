/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/forwards/transfer_ehu.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <set>
#include <map>
#include "libLSS/physics/forwards/transfer_ehu.hpp"
#include "libLSS/physics/forwards/registry.hpp"
#include "libLSS/physics/model_io.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "libLSS/tools/itertools.hpp"
#include <CosmoTool/cosmopower.hpp>

using namespace LibLSS;
ForwardEisensteinHu::ForwardEisensteinHu(
    MPI_Communication *comm, const BoxModel &box)
    : BORGForwardModel(comm, box), powerSpectrumKeys(lo_mgr->extents_complex()),
      powerSpectrum(boost::extents[1]), lazyInit(false), sign_k2(1),
      invalid(true) {
  ensureInputEqualOutput();

  // First look at the number of different keys
  size_t endN0 = startN0 + localN0;
  std::set<double> keyset;
  std::map<double, int> keymap;
  for (size_t i = startN0; i < endN0; i++) {
    for (size_t j = 0; j < N1; j++) {
      for (size_t k = 0; k < N2_HC; k++) {
        double kx = kmode(i, N0, L0);
        double ky = kmode(j, N1, L1);
        double kz = kmode(k, N2, L2);

        double key2 = (kx * kx + ky * ky + kz * kz);
        keyset.insert(key2);
      }
    }
  }

  // Build inverse map
  for (auto iter : itertools::enumerate(keyset)) {
    keymap[iter.get<1>()] = iter.get<0>();
  }

  keyTranslate.resize(boost::extents[keymap.size()]);

  // Assign each k mode its unique identifier
  for (size_t i = startN0; i < endN0; i++) {
    for (size_t j = 0; j < N1; j++) {
      for (size_t k = 0; k < N2_HC; k++) {
        double kx = kmode(i, N0, L0);
        double ky = kmode(j, N1, L1);
        double kz = kmode(k, N2, L2);

        double key2 = (kx * kx + ky * ky + kz * kz);
        int key = keymap[key2];
        powerSpectrumKeys[i][j][k] = key;
        keyTranslate[key] = std::sqrt(key2);
      }
    }
  }
  powerSpectrum.resize(boost::extents[keymap.size()]);
}

auto ForwardEisensteinHu::getPowerSpectrumArray() {
  auto &local_keys = powerSpectrumKeys;

  return fwrap(
      b_fused_idx<double, 3>([this, &local_keys](size_t i, size_t j, size_t k) {
        return powerSpectrum[local_keys[i][j][k]];
      }));
}

void ForwardEisensteinHu::forwardModel_v2(ModelInput<3> delta_init) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  // Setup the IO basis that is required for this forward.
  delta_init.setRequestedIO(PREFERRED_FOURIER);

  hold_input = std::move(delta_init);
}

void ForwardEisensteinHu::getDensityFinal(ModelOutput<3> delta_output) {
  delta_output.setRequestedIO(PREFERRED_FOURIER);
  auto w_delta_init = fwrap(hold_input.getFourierConst());
  auto w_delta_output = fwrap(delta_output.getFourierOutput());

  w_delta_output = (w_delta_init)*getPowerSpectrumArray();

  invalid = false;
}

void ForwardEisensteinHu::updateCosmo() {
  LIBLSS_AUTO_CONTEXT(LOG_VERBOSE, ctx);

  if (cosmo_params == old_cosmo_params)
    return;

  invalid = true;

  old_cosmo_params = cosmo_params;

  Cosmology cosmo(cosmo_params);
  CosmoTool::CosmoPower cpower;

  double h = cpower.h = cosmo_params.h;
  cpower.OMEGA_B = cosmo_params.omega_b;
  cpower.OMEGA_C = cosmo_params.omega_m - cosmo_params.omega_b;
  cpower.SIGMA8 = cosmo_params.sigma8;
  cpower.n = cosmo_params.n_s;
  cpower.updateCosmology();
  cpower.setFunction(CosmoTool::CosmoPower::HU_WIGGLES);
  cpower.normalize();
  cpower.setFunction(CosmoTool::CosmoPower::MATTER_TK);

  // TODO: For future we will generate the power spectrum here, inline
  size_t endN0 = startN0 + localN0;

#pragma omp parallel for collapse(3)
  for (size_t i = startN0; i < endN0; i++) {
    for (size_t j = 0; j < N1; j++) {
      for (size_t k = 0; k < N2_HC; k++) {
        int key = powerSpectrumKeys[i][j][k];
        double k_mode = keyTranslate[key];
        double Qk_delta =
            -sign_k2 * cpower.power(k_mode * h) * (k_mode * k_mode);
        powerSpectrum[key] = Qk_delta;
      }
    }
  }
}

void ForwardEisensteinHu::adjointModel_v2(
    ModelInputAdjoint<3> in_gradient_delta) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  // Build strict range views (we do not want to see the
  // the FFTW padding, ensure that the view object lives till the end of this function.

  in_gradient_delta.setRequestedIO(PREFERRED_FOURIER);
  hold_ag_input = std::move(in_gradient_delta);
}

void ForwardEisensteinHu::getAdjointModelOutput(
    ModelOutputAdjoint<3> out_gradient_delta) {
  out_gradient_delta.setRequestedIO(PREFERRED_FOURIER);
  auto w_in_gradient = fwrap(hold_ag_input.getFourierConst());
  auto w_out_gradient = fwrap(out_gradient_delta.getFourierOutput());

  w_out_gradient = w_in_gradient * getPowerSpectrumArray();
}

void ForwardEisensteinHu::clearAdjointGradient() {
  hold_ag_input.clear();
  hold_input.clear();
}

void ForwardEisensteinHu::forwardModelRsdField(ArrayRef &, double *) {}

void ForwardEisensteinHu::releaseParticles() {}

bool ForwardEisensteinHu::densityInvalidated() const { return invalid; }

static std::shared_ptr<BORGForwardModel> build_eisenstein_hu(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params) {
  //  double ai = params.get<double>("a_initial");
  auto reverse_sign = params.get_optional<bool>("reverse_sign");
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  auto v = std::make_shared<ForwardEisensteinHu>(comm, box);
  if (reverse_sign)
    v->setReverseSign(*reverse_sign);
  return v;
}

LIBLSS_REGISTER_FORWARD_IMPL(TRANSFER_EHU, build_eisenstein_hu);
