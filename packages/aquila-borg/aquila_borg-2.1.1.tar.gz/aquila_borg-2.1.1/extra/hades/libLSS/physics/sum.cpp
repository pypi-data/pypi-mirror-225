/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/sum.cpp
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
#include "libLSS/physics/sum.hpp"

using namespace LibLSS;

SumForwardModel::SumForwardModel(MPI_Communication *comm, const BoxModel &box)
    : BORGForwardModel(comm, box) {}

SumForwardModel::SumForwardModel(
    MPI_Communication *comm, const BoxModel &box, const BoxModel &outbox)
    : BORGForwardModel(comm, box, outbox) {}

SumForwardModel::~SumForwardModel() {}

void SumForwardModel::forwardModel_v2(ModelInput<3> delta_init) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  for (auto &model : model_list) {
    model->forwardModel_v2(delta_init.shallowClone());
  }
}

void SumForwardModel::getDensityFinal(ModelOutput<3> output) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  {
    auto out_io = (*model_list.begin())->getPreferredOutput();
    if (out_io != PREFERRED_NONE)
      output.setRequestedIO(out_io);
  }

  ModelOutput<3> tmp;

  double num = 1.0; //model_list.size();
  auto accum = [num](auto &a, auto &b) {
    fwrap(a) = fwrap(a) + (1.0 / num) * fwrap(b);
  };

  if (output.active == PREFERRED_REAL) {
    auto tmp_p = out_mgr->allocate_ptr_array();
    auto& tmp_a = tmp_p->get_array();
    tmp = std::move(ModelOutput<3>(out_mgr, get_box_model_output(), tmp_a, std::move(tmp_p)));
    fwrap(output.getRealOutput()) = 0.0;
  } else {
    auto tmp_p = out_mgr->allocate_ptr_complex_array();
    auto& tmp_a = tmp_p->get_array();
    tmp = std::move(ModelOutput<3>(out_mgr, get_box_model_output(), tmp_a, std::move(tmp_p)));
    fwrap(output.getFourierOutput()) = 0.0;
  }

  for (auto &model : model_list) {
    model->getDensityFinal(tmp.shallowClone());

    switch (tmp.active) {
    case PREFERRED_REAL:
      accum(output.getRealOutput(), tmp.getRealOutput());
      break;
    case PREFERRED_FOURIER:
      accum(output.getFourierOutput(), tmp.getFourierOutput());
      break;
    default:
      error_helper<ErrorBadState>("Unknown IO type.");
      break;
    }
  }
}

void SumForwardModel::adjointModel_v2(ModelInputAdjoint<3> gradient_delta) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  for (auto &model : model_list) {
    model->adjointModel_v2(gradient_delta.shallowClone());
  }
}

void SumForwardModel::getAdjointModelOutput(ModelOutputAdjoint<3> ag_output) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  {
    auto in_io = (*model_list.begin())->getPreferredInput();
    if (in_io != PREFERRED_NONE)
      ag_output.setRequestedIO(in_io);
  }

  ModelOutputAdjoint<3> tmp;
  double num = 1.0; //model_list.size();
  auto accum = [num](auto &a, auto &b) {
    fwrap(a) = fwrap(a) + (1.0 / num) * fwrap(b);
  };

  if (ag_output.active == PREFERRED_REAL) {
    auto tmp_p = out_mgr->allocate_ptr_array();
    auto& tmp_a = tmp_p->get_array();
    tmp = std::move(ModelOutputAdjoint<3>(out_mgr, get_box_model_output(), tmp_a, std::move(tmp_p)));
    fwrap(ag_output.getRealOutput()) = 0.0;
  } else {
    auto tmp_p = out_mgr->allocate_ptr_complex_array();
    auto& tmp_a = tmp_p->get_array();
    tmp = std::move(ModelOutputAdjoint<3>(out_mgr, get_box_model_output(), tmp_a, std::move(tmp_p)));
    fwrap(ag_output.getFourierOutput()) = 0.0;
  }

  for (auto &model : model_list) {
    model->getAdjointModelOutput(tmp.shallowClone());

    switch (tmp.active) {
    case PREFERRED_REAL:
      accum(ag_output.getRealOutput(), tmp.getRealOutput());
      break;
    case PREFERRED_FOURIER:
      accum(ag_output.getFourierOutput(), tmp.getFourierOutput());
      break;
    default:
      error_helper<ErrorBadState>("Unknown IO type.");
      break;
    }
  }
}

void SumForwardModel::releaseParticles() {
  // Fill up with the chain
  for (auto model : model_list) {
    model->releaseParticles();
  }
}

void SumForwardModel::addModel(std::shared_ptr<BORGForwardModel> model) {
  if (get_box_model() != model->get_box_model()) {
    error_helper<ErrorParams>(
        "Invalid model configuration with IO of the chain.");
  }
  model_list.push_back(model);
}

void SumForwardModel::setAdjointRequired(bool required) {
  for (auto& model : model_list) {
    model->setAdjointRequired(required);
  }
}

void SumForwardModel::updateCosmo() {
  // Fill up with the chain
  for (auto& model : model_list) {
    model->setCosmoParams(cosmo_params);
  }
}

void SumForwardModel::setModelParams(ModelDictionnary const &params) {
  for (auto& model : model_list) {
    model->setModelParams(params);
  }
}

boost::any SumForwardModel::getModelParam(std::string const& name, std::string const& param) {
  if (name == modelName) {
    return boost::any();
  }

  for (auto& model : model_list) {
    auto ret = model->getModelParam(name, param);
    if (!ret.empty())
      return ret;
  }
  return boost::any();
}

void SumForwardModel::clearAdjointGradient() {
  for (auto model : model_list) {
    model->clearAdjointGradient();
  }
}

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2020
