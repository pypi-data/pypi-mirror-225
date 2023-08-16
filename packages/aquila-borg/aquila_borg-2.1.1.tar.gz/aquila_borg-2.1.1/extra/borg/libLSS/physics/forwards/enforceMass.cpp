/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/enforceMass.cpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <string>
#include "libLSS/tools/console.hpp"
#include "libLSS/physics/model_io.hpp"
#include "libLSS/physics/forwards/enforceMass.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/physics/forwards/registry.hpp"
#include "libLSS/tools/ptree_proxy.hpp"

using namespace LibLSS;

void ForwardEnforceMass::forwardModel_v2(ModelInput<3> delta_init) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  // Setup the IO basis that is required for this forward.
  delta_init.setRequestedIO(PREFERRED_REAL);

  hold_input = std::move(delta_init);
  full_sum =
      (fwrap(hold_input.getRealConst()[lo_mgr->strict_range()]) + 1.0).sum();

  comm->all_reduce_t(MPI_IN_PLACE, &full_sum, 1, MPI_SUM);
}

void ForwardEnforceMass::getDensityFinal(ModelOutput<3> delta_output) {
  delta_output.setRequestedIO(PREFERRED_REAL);
  auto w_delta_init = fwrap(hold_input.getRealConst()) + 1.0;
  auto w_delta_output = fwrap(delta_output.getRealOutput());

  double mean = full_sum / get_box_model().numElements();

  w_delta_output = w_delta_init / mean - 1.0;
}

void ForwardEnforceMass::adjointModel_v2(
    ModelInputAdjoint<3> in_gradient_delta) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  // Build strict range views (we do not want to see the
  // the FFTW padding, ensure that the view object lives till the end of this function.

  in_gradient_delta.setRequestedIO(PREFERRED_REAL);
  hold_ag_input = std::move(in_gradient_delta);
}

void ForwardEnforceMass::getAdjointModelOutput(
    ModelOutputAdjoint<3> out_gradient_delta) {
  out_gradient_delta.setRequestedIO(PREFERRED_REAL);
  auto w_in_gradient = fwrap(hold_ag_input.getRealConst());
  auto w_out_gradient = fwrap(out_gradient_delta.getRealOutput());
  auto w_delta_init = fwrap(hold_input.getRealConst()) + 1.0;

  double mean = full_sum / get_box_model().numElements();

  double full_sum_grad =
      (fwrap(hold_ag_input.getRealConst()[lo_mgr->strict_range()])).sum();

  comm->all_reduce_t(MPI_IN_PLACE, &full_sum_grad, 1, MPI_SUM);

  w_out_gradient =
      1.0 / mean * (w_in_gradient - w_delta_init * full_sum_grad / full_sum);
}

static std::shared_ptr<BORGForwardModel> build_enforcemass(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params) {

  // TODO: Setup transfer function
  auto model = std::make_shared<ForwardEnforceMass>(comm, box);
  return model;
}

LIBLSS_REGISTER_FORWARD_IMPL(EnforceMass, build_enforcemass);

// ARES TAG: num_authors = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
