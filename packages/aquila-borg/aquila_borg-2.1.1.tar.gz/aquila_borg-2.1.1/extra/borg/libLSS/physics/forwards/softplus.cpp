/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/softplus.cpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/cconfig.h"
#include <string>
#include "libLSS/tools/console.hpp"
#include "libLSS/physics/model_io.hpp"
#include "libLSS/physics/forwards/softplus.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/physics/forwards/registry.hpp"
#include "libLSS/tools/ptree_proxy.hpp"

using namespace LibLSS;

void ForwardSoftPlus::forwardModel_v2(ModelInput<3> delta_init) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  // Setup the IO basis that is required for this forward.
  delta_init.setRequestedIO(PREFERRED_REAL);

  hold_input = std::move(delta_init);
}

void ForwardSoftPlus::getDensityFinal(ModelOutput<3> delta_output) {
  delta_output.setRequestedIO(PREFERRED_REAL);
  auto w_delta_init = fwrap(hold_input.getRealConst()) + bias_value; 
  auto w_delta_output = fwrap(delta_output.getRealOutput());

  auto basic_softplus =
      std::log(1.0 + std::exp(hardness * w_delta_init)) / hardness;

  w_delta_output =
      mask((hardness * w_delta_init) > 10.0, w_delta_init, basic_softplus) - bias_value;
}

void ForwardSoftPlus::setHardness(double h) { hardness = h; }

void ForwardSoftPlus::setBiasValue(double b) { bias_value = b; }

void ForwardSoftPlus::adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  // Build strict range views (we do not want to see the
  // the FFTW padding, ensure that the view object lives till the end of this function.

  in_gradient_delta.setRequestedIO(PREFERRED_REAL);
  hold_ag_input = std::move(in_gradient_delta);
}

void ForwardSoftPlus::getAdjointModelOutput(
    ModelOutputAdjoint<3> out_gradient_delta) {
  out_gradient_delta.setRequestedIO(PREFERRED_REAL);
  auto w_in_gradient = fwrap(hold_ag_input.getRealConst());
  auto w_out_gradient = fwrap(out_gradient_delta.getRealOutput());
  auto w_delta_init = fwrap(hold_input.getRealConst()) + bias_value;

  // FIXME: Being lazy and abusing the autowrap API here.
  auto constantGradient =
      fwrap(b_fused_idx<double, 3>([](auto... x) { return 1.0; }));
  auto basic_gradient = 1.0 / (1.0 + std::exp(-hardness * w_delta_init));

  w_out_gradient =
      mask((hardness * w_delta_init) > 10.0, constantGradient, basic_gradient) *
      w_in_gradient;
}

static std::shared_ptr<BORGForwardModel> build_softplus(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params) {
  auto hardness = params.get<double>("hardness");
  auto bias_value = params.get<double>("bias_value", 1.0);

  // TODO: Setup transfer function
  auto model = std::make_shared<ForwardSoftPlus>(comm, box);

  model->setBiasValue(bias_value);
  model->setHardness(hardness);
  return model;
}

LIBLSS_REGISTER_FORWARD_IMPL(Softplus, build_softplus);

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
