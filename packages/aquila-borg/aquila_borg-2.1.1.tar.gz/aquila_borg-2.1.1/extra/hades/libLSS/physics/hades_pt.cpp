/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/hades_pt.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

#include "libLSS/physics/forward_model.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/tools/errors.hpp"
#include "libLSS/physics/hades_pt.hpp"
#include "libLSS/physics/forwards/registry.hpp"

using namespace LibLSS;

HadesLinear::HadesLinear(
    MPI_Communication *comm, const BoxModel &box, const BoxModel &box_out,
    double ai_, double af_)
    : BORGForwardModel(comm, box, box_out), ai(ai_), af(af_), D_init(0) {
  ensureInputEqualOutput();
  setupDefault();
}

void HadesLinear::forwardModelSimple(CArrayRef &delta_init) {
  error_helper<ErrorNotImplemented>(
      "No forwardModelSimple in Linear forward model");
}

PreferredIO HadesLinear::getPreferredInput() const { return PREFERRED_NONE; }
PreferredIO HadesLinear::getPreferredOutput() const { return PREFERRED_NONE; }

void HadesLinear::forwardModel_v2(ModelInput<3> delta_init) {
  LIBLSS_AUTO_DEBUG_CONTEXT2(ctx, "HadesLinear::forwardModel_v2");

  double G = 1; // Growth TBI
  // Only bother of real values (no padding)
  ctx.print(boost::format("D_init=%g") % D_init);
  // Compute zero mean density.
  PreferredIO choice = delta_init.current;
  delta_init.setRequestedIO(choice);
  switch (choice) {
  case PREFERRED_REAL: {
    auto strict_field = tmp_real_field->get_array()[lo_mgr->strict_range()];
    fwrap(strict_field) = fwrap(delta_init.getRealConst()[lo_mgr->strict_range()]) / D_init;
    break;
  }
  case PREFERRED_FOURIER: {
    auto &strict_field = tmp_complex_field->get_array();
    fwrap(strict_field) = fwrap(delta_init.getFourierConst()) / D_init;
    break;
  }
  default:
    error_helper<ErrorNotImplemented>("Invalid IO");
  }
  lastInput = currentOutput = choice;
}

void HadesLinear::getDensityFinal(ModelOutput<3> delta_output) {
  delta_output.setRequestedIO(currentOutput);
  switch (currentOutput) {
  case PREFERRED_REAL:
    fwrap(delta_output.getRealOutput()) = tmp_real_field->get_array();
    break;
  case PREFERRED_FOURIER:
    fwrap(delta_output.getFourierOutput()) = tmp_complex_field->get_array();
    break;
  default:
    error_helper<ErrorNotImplemented>("Invalid IO");
    break;
  }
}

void HadesLinear::updateCosmo() {
  ConsoleContext<LOG_DEBUG> ctx("HadesLinear::updateCosmo");

  Cosmology cosmo(cosmo_params);

  D_init = cosmo.d_plus(ai) /
           cosmo.d_plus(af); // Scale factor for initial conditions
}

void HadesLinear::forwardModelRsdField(ArrayRef &deltaf, double *vobs_ext) {
  error_helper<ErrorNotImplemented>("No RSD support in Linear forward model");
}

void HadesLinear::adjointModel_v2(ModelInputAdjoint<3> ag_delta_input) {
  ConsoleContext<LOG_DEBUG> ctx("HadesLinear::adjointModel_v2");

  ag_delta_input.setRequestedIO(currentOutput);

  // Compute zero mean density.
  switch (currentOutput) {
  case PREFERRED_REAL: {
    auto strict_field = tmp_real_field->get_array()[lo_mgr->strict_range()];
    fwrap(strict_field) =
        fwrap(ag_delta_input.getRealConst()[lo_mgr->strict_range()]) / D_init;
    break;
  }
  case PREFERRED_FOURIER: {
    auto &strict_field = tmp_complex_field->get_array();
    fwrap(strict_field) = fwrap(ag_delta_input.getFourierConst()) / D_init;
    break;
  }
  default:
    error_helper<ErrorNotImplemented>("Invalid IO");
  }
}

void HadesLinear::getAdjointModelOutput(ModelOutputAdjoint<3> ag_delta_output) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  //if (lastInput != ag_delta_output.current) {
  //  error_helper<ErrorBadState>(
  //      "The forward and adjoint gradient pipeline is inconsistent.");
  //}

  ag_delta_output.setRequestedIO(currentOutput);

  switch (currentOutput) {
  case PREFERRED_REAL: {
    auto strict_field = tmp_real_field->get_array()[lo_mgr->strict_range()];
    auto w_gradient2 =
        fwrap(ag_delta_output.getRealOutput()[lo_mgr->strict_range()]);
    w_gradient2 = strict_field;
    break;
  }
  case PREFERRED_FOURIER: {
    auto strict_field = tmp_complex_field->get_array();
    auto w_gradient2 = fwrap(ag_delta_output.getFourierOutput());
    w_gradient2 = strict_field;
    break;
  }
  default:
    error_helper<ErrorNotImplemented>("Invalid IO");
  }
}

void HadesLinear::releaseParticles() {}

static std::shared_ptr<BORGForwardModel> build_hades_linear(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params) {
  double ai = params.get<double>("a_initial");
  double af = params.get<double>("a_final");
  return std::make_shared<HadesLinear>(comm, box, box, ai, af);
}

LIBLSS_REGISTER_FORWARD_IMPL(HADES_PT, build_hades_linear);
