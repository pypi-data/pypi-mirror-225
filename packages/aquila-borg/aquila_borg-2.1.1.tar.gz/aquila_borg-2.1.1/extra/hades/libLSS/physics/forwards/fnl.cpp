/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/forwards/fnl.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <set>
#include <map>
#include "libLSS/physics/forwards/fnl.hpp"
#include "libLSS/physics/forwards/registry.hpp"
#include "libLSS/physics/model_io.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "libLSS/tools/itertools.hpp"
#include <CosmoTool/cosmopower.hpp>

using namespace LibLSS;
ForwardFNL::ForwardFNL(MPI_Communication *comm, const BoxModel &box)
    : BORGForwardModel(comm, box) {
  ensureInputEqualOutput();
}

void ForwardFNL::forwardModel_v2(ModelInput<3> delta_init) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  // Setup the IO basis that is required for this forward.
  delta_init.setRequestedIO(PREFERRED_REAL);

  hold_input = std::move(delta_init);
}

void ForwardFNL::getDensityFinal(ModelOutput<3> delta_output) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  delta_output.setRequestedIO(PREFERRED_REAL);
  auto w_delta_init = fwrap(hold_input.getReal());
  auto w_delta_output = fwrap(delta_output.getRealOutput());

  w_delta_output =
      (w_delta_init * w_delta_init * cosmo_params.fnl + w_delta_init);
}

void ForwardFNL::adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  in_gradient_delta.setRequestedIO(PREFERRED_REAL);
  hold_ag_input = std::move(in_gradient_delta);
}

void ForwardFNL::getAdjointModelOutput(
    ModelOutputAdjoint<3> out_gradient_delta) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  out_gradient_delta.setRequestedIO(PREFERRED_REAL);
  auto w_in_gradient = fwrap(hold_ag_input.getReal());
  auto w_out_gradient = fwrap(out_gradient_delta.getRealOutput());
  auto w_delta_init = fwrap(hold_input.getReal());

  w_out_gradient =
      2 * w_delta_init * cosmo_params.fnl * w_in_gradient + w_in_gradient;
}

void ForwardFNL::clearAdjointGradient() {
  hold_ag_input.clear();
  hold_input.clear();
}

void ForwardFNL::forwardModelRsdField(ArrayRef &, double *) {}

void ForwardFNL::releaseParticles() {}

static std::shared_ptr<BORGForwardModel> build_primordial_FNL(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  return std::make_shared<ForwardFNL>(comm, box);
}

LIBLSS_REGISTER_FORWARD_IMPL(PRIMORDIAL_FNL, build_primordial_FNL);
