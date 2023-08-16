/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/hades_log.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/tools/errors.hpp"
#include "libLSS/physics/hades_log.hpp"

using namespace LibLSS;

HadesLog::HadesLog(
    MPI_Communication *comm, const BoxModel &box, double ai_,
    bool shifted_mean_)
    : BORGForwardModel(comm, box), ai(ai_), D_init(1.0),
      shifted_mean(shifted_mean_) {
  setupDefault();
}

void HadesLog::forwardModelSimple(CArrayRef &delta_init) {
  error_helper<ErrorNotImplemented>(
      "No forwardModelSimple in Log forward model");
}

void HadesLog::clearAdjointGradient() { hold_in_gradient.clear(); }

void HadesLog::forwardModel_v2(ModelInput<3> delta_init) {
  ConsoleContext<LOG_DEBUG> ctx("forward Hades Log");

  delta_init.setRequestedIO(PREFERRED_REAL);

  double G = 1; // Growth TBI
  // Only bother of real values (no padding)
  auto strict_field = delta_init.getRealConst()[lo_mgr->strict_range()];
  // First part of the forward model, exponentiation and rescaling
  auto fdelta = std::exp((G / D_init) * fwrap(strict_field));

  // Compute mean and save it for later

  if (shifted_mean) {
    rho_mean = fdelta.sum() / (N0 * N1 * N2);
    comm->all_reduce_t(MPI_IN_PLACE, &rho_mean, 1, MPI_SUM);
    fwrap(tmp_real_field->get_array()[lo_mgr->strict_range()]) =
        fdelta / rho_mean - 1;
  } else
    fwrap(tmp_real_field->get_array()[lo_mgr->strict_range()]) = fdelta;
}

void HadesLog::getDensityFinal(ModelOutput<3> delta_output) {
  delta_output.setRequestedIO(PREFERRED_REAL);

  // Compute zero mean density.
  fwrap(delta_output.getRealOutput()[lo_mgr->strict_range()]) =
      fwrap(tmp_real_field->get_array()[lo_mgr->strict_range()]);
}

void HadesLog::updateCosmo() {
  ConsoleContext<LOG_DEBUG> ctx("Hades Log cosmo update");

  if (old_params != cosmo_params) {
    Cosmology cosmo(cosmo_params);

    D_init = cosmo.d_plus(ai) /
             cosmo.d_plus(1.0); // Scale factor for initial conditions
    old_params = cosmo_params;
  }
}

void HadesLog::forwardModelRsdField(ArrayRef &deltaf, double *vobs_ext) {
  error_helper<ErrorNotImplemented>("No RSD support in Log forward model");
}

void HadesLog::adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta) {
  ConsoleContext<LOG_DEBUG> ctx("adjoint Hades Log");
  // Build strict range views (we do not want to see the
  // the FFTW padding, ensure that the view object lives till the end of this function.
  in_gradient_delta.setRequestedIO(PREFERRED_REAL);
  auto in_gradient_view =
      in_gradient_delta.getRealConst()[lo_mgr->strict_range()];
  auto input_view = tmp_real_field->get_array()[lo_mgr->strict_range()];
  // Wrap for automated vectorization.
  auto w_gradient = fwrap(in_gradient_view);

  double G = 1.0;
  // Recompute forward transforms
  if (shifted_mean) {
    auto fdelta = (fwrap(input_view) + 1) * rho_mean;

    // Gradient of the denominator
    A_mean = (w_gradient * fdelta).sum() / rho_mean / (N0 * N1 * N2);
    comm->all_reduce_t(MPI_IN_PLACE, &A_mean, 1, MPI_SUM);
    ctx.format(
        "D_init = %g, A_mean = %g, rho_mean = %g", D_init, A_mean, rho_mean);
  }

  hold_in_gradient = std::move(in_gradient_delta);
}

void HadesLog::getAdjointModelOutput(ModelOutputAdjoint<3> ag_delta_output) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  ag_delta_output.setRequestedIO(PREFERRED_REAL);
  auto in_gradient_view =
      hold_in_gradient.getRealConst()[lo_mgr->strict_range()];
  auto out_gradient_view =
      ag_delta_output.getRealOutput()[lo_mgr->strict_range()];
  auto input_view = tmp_real_field->get_array()[lo_mgr->strict_range()];

  // Wrap for automated vectorization.
  double G = 1.0;
  auto w_gradient = fwrap(in_gradient_view);
  if (shifted_mean) {
    auto fdelta = (fwrap(input_view) + 1) * rho_mean;

    // Complete gradient of numerator and denominator
    fwrap(out_gradient_view) =
        (w_gradient - A_mean) * fdelta * (G / (D_init * rho_mean));
  } else {
    auto fdelta = (fwrap(input_view));

    // Complete gradient of numerator and denominator
    fwrap(out_gradient_view) = (w_gradient)*fdelta * (G / D_init);
  }
}

void HadesLog::releaseParticles() {}

static std::shared_ptr<BORGForwardModel> build_hades_log(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params) {
  double ai = params.get<double>("a_initial");
  return std::make_shared<HadesLog>(comm, box, ai);
}

LIBLSS_REGISTER_FORWARD_IMPL(HADES_LOG, build_hades_log);
