#include "libLSS/cconfig.h"
#include "libLSS/samplers/generic/generic_hmc_likelihood.hpp"

using namespace LibLSS;

void LibLSS::GenericDetails::compute_forward(
    std::shared_ptr<FFTW_Manager<double, 3>> &mgr,
    std::shared_ptr<BORGForwardModel> &model,
    const CosmologicalParameters &cosmo_params, double ai,
    boost::multi_array_ref<double, 1> const &vobs, ModelInput<3> ic, ModelOutput<3> out_density,
    bool adjoint_next) {
  ConsoleContext<LOG_DEBUG> ctx("Execute forward model");

  ctx.print("Setup cosmology");
  // Update forward model for maybe new cosmo params
  model->setCosmoParams(cosmo_params);
  ctx.print("Setup observer velocity");
  // Inform about the velocity of the observer
  model->setObserver(vobs);
  // Compute forward model
  ctx.print("Run model");
  model->setAdjointRequired(adjoint_next);
  model->forwardModel_v2(std::move(ic));
  model->getDensityFinal(std::move(out_density));
}

