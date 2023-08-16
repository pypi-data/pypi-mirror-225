/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/branch.cpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <boost/multi_array.hpp>
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/physics/forward_model.hpp"
#include <list>
#include <boost/variant.hpp>
#include "libLSS/tools/errors.hpp"
#include "libLSS/physics/branch.hpp"

using namespace LibLSS;

BranchForwardModel::BranchForwardModel(
    MPI_Communication *comm, const BoxModel &box)
    : BORGForwardModel(comm, box) {}

BranchForwardModel::BranchForwardModel(
    MPI_Communication *comm, const BoxModel &box, const BoxModel &outbox)
    : BORGForwardModel(comm, box, outbox) {}

BranchForwardModel::~BranchForwardModel() {}

void BranchForwardModel::forwardModelSimple(CArrayRef &delta_init) {}

void BranchForwardModel::forwardModel_v2(ModelInput<3> delta_init) {
  LIBLSS_AUTO_CONTEXT(LOG_VERBOSE, ctx);

  for (auto &model : model_list) {
    model->forwardModel_v2(delta_init.shallowClone());
  }
}

void BranchForwardModel::getDensityFinal(ModelOutput<3> output) {
  error_helper<ErrorNotImplemented>(
      "getDensityFinal does not exist for BranchForwardModel.");
}

void BranchForwardModel::clear_chain() {
  auto cleaner = [](auto &u) { u.reset(); };
  boost::apply_visitor(cleaner, previous);
  boost::apply_visitor(cleaner, next);
}

void BranchForwardModel::forwardModelRsdField(
    ArrayRef &deltaf, double *vobs_ext) {}

// adjointModel auto release particles. Beware !

void BranchForwardModel::adjointModel_v2(ModelInputAdjoint<3> gradient_delta) {
  LIBLSS_AUTO_CONTEXT(LOG_VERBOSE, ctx);

  if (gradient_delta) {
    error_helper<ErrorParams>(
        "Input to adjointModel_v2 must be null for branch.");
  }
}

void BranchForwardModel::getAdjointModelOutput(
    ModelOutputAdjoint<3> ag_output) {
  // FIXME: Very dumb choice at the moment, first one has the right of choice.
  ag_output.setRequestedIO((*model_list.begin())->getPreferredInput());

  ModelOutputAdjoint<3> common_output = ag_output.makeTempLike();

  for (auto &model : model_list) {
    ModelOutputAdjoint<3> tmp_output = common_output.shallowClone();

    model->getAdjointModelOutput(std::move(tmp_output));
    switch (ag_output.current) {
    case PREFERRED_REAL:
      fwrap(ag_output.getRealOutput()) =
          fwrap(ag_output.getRealOutput()) + common_output.getRealOutput();
      break;
    case PREFERRED_FOURIER:
      fwrap(ag_output.getFourierOutput()) =
          fwrap(ag_output.getFourierOutput()) + common_output.getRealOutput();
      break;
    default:
      error_helper<ErrorBadState>("Unknown ModelIO type");
      break;
    }
    clearAdjointGradient();
  }
}

void BranchForwardModel::releaseParticles() {
  // Fill up with the chain
  for (auto model : model_list) {
    model->releaseParticles();
  }
}

void BranchForwardModel::addModel(std::shared_ptr<BORGForwardModel> model) {
  if (get_box_model() != model->get_box_model()) {
    error_helper<ErrorParams>(
        "Invalid model configuration with IO of the chain.");
  }
  model_list.push_back(model);
}

void BranchForwardModel::setAdjointRequired(bool required) {
  for (auto model : model_list) {
    model->setAdjointRequired(required);
  }
}

void BranchForwardModel::updateCosmo() {
  // Fill up with the chain
  for (auto model : model_list) {
    model->setCosmoParams(cosmo_params);
  }
}

void BranchForwardModel::clearAdjointGradient() {
  for (auto model : model_list) {
    model->clearAdjointGradient();
  }
}

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2020
