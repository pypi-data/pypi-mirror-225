/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/chain_forward_model.cpp
    Copyright (C) 2018-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2018-2019 Doogesh Kodi Ramanah <ramanah@iap.fr>

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
#include "libLSS/physics/chain_forward_model.hpp"
#include <boost/variant.hpp>
#include "libLSS/tools/overload.hpp"

using namespace LibLSS;

ChainForwardModel::ChainForwardModel(
    MPI_Communication *comm, const BoxModel &box)
    : BORGForwardModel(comm, box), accumulate(false) {}

ChainForwardModel::ChainForwardModel(
    MPI_Communication *comm, const BoxModel &box, const BoxModel &outbox)
    : BORGForwardModel(comm, box, outbox), accumulate(false) {}

ChainForwardModel::~ChainForwardModel() {}

void ChainForwardModel::accumulateAdjoint(bool do_accumulate) {
  accumulate = do_accumulate;
}

bool ChainForwardModel::densityInvalidated() const {
  bool r = false;

  for (auto const &model : model_list) {
    r = r || model->densityInvalidated();
  }
  return r;
}

void ChainForwardModel::forwardModelSimple(CArrayRef &delta_init) {}

void ChainForwardModel::forwardModel_v2(ModelInput<3> delta_init) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  ModelInput<3> input_array;
  ModelInput<3> next_input(std::move(delta_init));
  ModelOutput<3> next_output;
  S_U_ArrayReal tmp_real;
  S_U_ArrayFourier tmp_fourier;
  BoxModel box_in, box_out;

  // Fill up with the chain
  auto iter = model_list.begin();
  while (iter != model_list.end()) {
    auto model = *iter;
    ++iter;

    bool final_pass = (iter == model_list.end());
    input_array = std::move(next_input);
    PreferredIO nextIO =
        final_pass ? model->getPreferredOutput() : (*iter)->getPreferredInput();
    if (nextIO == PREFERRED_NONE) {
      nextIO = model->getPreferredOutput();
      if (nextIO == PREFERRED_NONE) {
        nextIO = input_array.current;
      }
    }

    box_in = model->get_box_model();
    box_out = model->get_box_model_output();
    // TODO: check box compatibilities

    switch (nextIO) {
    case PREFERRED_REAL:
      tmp_real.reset();
      tmp_real = std::move(model->out_mgr->allocate_ptr_array());
      next_output = std::move(ModelOutput<3>(
          model->out_mgr, box_out, tmp_real->get_array(), tmp_real));
      next_input = std::move(ModelInput<3>(
          model->out_mgr, box_out, tmp_real->get_array(), tmp_real));
      if (final_pass) {
        final_real = tmp_real;
        final_output = std::move(ModelOutput<3>(
            model->out_mgr, box_out, final_real->get_array(), final_real));
      }
      next = tmp_real;
      break;
    case PREFERRED_FOURIER:
      tmp_fourier.reset();
      tmp_fourier = std::move(model->out_mgr->allocate_ptr_complex_array());
      next_output = std::move(ModelOutput<3>(
          model->out_mgr, box_out, tmp_fourier->get_array(), tmp_fourier));
      next_input = std::move(ModelInput<3>(
          model->out_mgr, box_out, tmp_fourier->get_array(), tmp_fourier));
      if (final_pass) {
        final_fourier = tmp_fourier;
        final_output = std::move(ModelOutput<3>(
            model->out_mgr, box_out, final_fourier->get_array(),
            final_fourier));
      }
      next = tmp_fourier;
      break;
    default:
      error_helper<ErrorNotImplemented>("Invalid IO type.");
      break;
    }
    model->forwardModel_v2(std::move(input_array));
    model->getDensityFinal(std::move(next_output));
    previous = next;
  }
}

void ChainForwardModel::getDensityFinal(ModelOutput<3> output) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  output.setRequestedIO(final_output.active);
  output.copyFrom(final_output);
  // Try to save some memory by releasing early the temporary allocation.
  final_real.reset();
  final_fourier.reset();
  clear_chain();
}

void ChainForwardModel::clear_chain() {
  auto cleaner = [](auto &u) { u.reset(); };
  boost::apply_visitor(cleaner, previous);
  boost::apply_visitor(cleaner, next);
}

void ChainForwardModel::forwardModelRsdField(
    ArrayRef &deltaf, double *vobs_ext) {}

static void accumulator(ModelInputBase<3> &accum, ModelInputBase<3> &input) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  typedef ModelIO<3>::CArrayRef CArrayRef;
  typedef ModelIO<3>::ArrayRef ArrayRef;

  // This ensures that we capture incompatibilities.

  accum.needDestroyInput();
  boost::apply_visitor(
      overload(
          [&input](CArrayRef *v) {
            // The preference is applied to the one being accumulated on the first ag.
            input.setRequestedIO(PREFERRED_FOURIER);
            fwrap(*v) = input.getFourierConst();
          },
          [&input](ArrayRef *v) {
            // The preference is applied to the one being accumulated on the first ag.
            input.setRequestedIO(PREFERRED_REAL);
            fwrap(*v) = input.getRealConst();
          },
          [&](auto const *v) {
            Console::instance().c_assert(false, "Impossible situation");
          }),
      accum.getHolder());
}

// adjointModel auto release particles. Beware !

void ChainForwardModel::adjointModel_v2(ModelInputAdjoint<3> gradient_delta) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);

  if (accumulate) {
    if (!accumulateAg) {
      accumulateAg = std::move(gradient_delta);
    } else {
      accumulator(accumulateAg, gradient_delta);
    }
    return;
  } else {
    accumulateAg = std::move(gradient_delta);
  }

  trigger_ag();
}

void ChainForwardModel::trigger_ag() {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  ModelInputAdjoint<3> next_ag_input(std::move(accumulateAg)), ag_input;
  ModelOutputAdjoint<3> ag_output;
  std::shared_ptr<DFT_Manager::U_ArrayReal> tmp_real;
  std::shared_ptr<DFT_Manager::U_ArrayFourier> tmp_fourier;
  BoxModel box_in, box_out;
  PreferredIO nextIO;

  // Fill up with the chain
  // Ordering here should be opposite to that in Forward model
  auto iter = model_list_adjoint.begin();
  while (iter != model_list_adjoint.end()) {
    auto model = *iter;

    ++iter;
    bool final_pass = (iter == model_list_adjoint.end());

    box_in = model->get_box_model_output();
    box_out = model->get_box_model();

    nextIO =
        final_pass ? model->getPreferredInput() : (*iter)->getPreferredOutput();
    if (nextIO == PREFERRED_NONE) {
      nextIO = model->getPreferredInput();
      if (nextIO == PREFERRED_NONE) {
        nextIO = next_ag_input.current;
      }
    }

    ag_input = std::move(next_ag_input);

    switch (nextIO) {
    case PREFERRED_REAL:
      ctx.print("Next wants real");
      tmp_real.reset();
      tmp_real = std::move(model->lo_mgr->allocate_ptr_array());
      ag_output = std::move(ModelOutputAdjoint<3>(
          model->lo_mgr, box_out, tmp_real->get_array(), tmp_real));
      next_ag_input = std::move(ModelInputAdjoint<3>(
          model->lo_mgr, box_out, tmp_real->get_array(), tmp_real));
      if (final_pass) {
        ag_final_real = tmp_real;
        ag_final_output = std::move(ModelOutputAdjoint<3>(
            model->lo_mgr, box_out, ag_final_real->get_array(), ag_final_real));
      }
      next = tmp_real;
      break;
    case PREFERRED_FOURIER:
      ctx.print("Next wants Fourier");
      tmp_fourier.reset();
      tmp_fourier = std::move(model->lo_mgr->allocate_ptr_complex_array());
      ag_output = std::move(ModelOutputAdjoint<3>(
          model->lo_mgr, box_out, tmp_fourier->get_array(), tmp_fourier));
      next_ag_input = std::move(ModelInputAdjoint<3>(
          model->lo_mgr, box_out, tmp_fourier->get_array(), tmp_fourier));
      if (final_pass) {
        ag_final_fourier = tmp_fourier;
        ag_final_output = std::move(ModelOutputAdjoint<3>(
            model->lo_mgr, box_out, ag_final_fourier->get_array(),
            ag_final_fourier));
      }
      next = tmp_fourier;
      break;
    default:
      error_helper<ErrorNotImplemented>("Invalid IO type");
      break;
    }

    model->adjointModel_v2(std::move(ag_input));
    model->getAdjointModelOutput(std::move(ag_output));
    previous = next;
  }
}

void ChainForwardModel::getAdjointModelOutput(ModelOutputAdjoint<3> ag_output) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  if (accumulate && accumulateAg) {
    trigger_ag();
  }

  ag_output.setRequestedIO(ag_final_output.active);
  ag_output.copyFrom(ag_final_output);

  ag_final_fourier.reset();
  ag_final_real.reset();
  clear_chain();
}

void ChainForwardModel::releaseParticles() {
  // Fill up with the chain
  for (auto model : model_list) {
    model->releaseParticles();
  }
}

void ChainForwardModel::addModel(
    std::shared_ptr<BORGForwardModel> model, std::string const &n) {
  named_models[n] = model;
  addModel(model);
}

std::shared_ptr<BORGForwardModel>
ChainForwardModel::queryModel(std::string const &n) {
  return named_models[n];
}

void ChainForwardModel::addModel(std::shared_ptr<BORGForwardModel> model) {
  if (model_list.size() == 0) {
    if (box_input != model->get_box_model()) {
      error_helper<ErrorParams>(
          "Invalid model configuration with IO of the chain.");
    }
  } else {
    if (box_output != model->get_box_model()) {
      error_helper<ErrorParams>(
          "Invalid model configuration with IO of the chain.");
    }
  }
  model_list.push_back(model);
  model_list_adjoint.insert(model_list_adjoint.begin(), model);

  box_output = model->get_box_model_output();
  out_mgr = model->out_mgr;
}

void ChainForwardModel::setAdjointRequired(bool required) {
  for (auto &model : model_list) {
    model->setAdjointRequired(required);
  }
}

void ChainForwardModel::updateCosmo() {
  // Fill up with the chain
  for (auto &model : model_list) {
    model->setCosmoParams(cosmo_params);
  }
}

void ChainForwardModel::setModelParams(ModelDictionnary const &params) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  for (auto &model : model_list) {
    model->setModelParams(params);
  }
}

void ChainForwardModel::clearAdjointGradient() {
  for (auto &model : model_list) {
    model->clearAdjointGradient();
  }
}

boost::any ChainForwardModel::getModelParam(
    std::string const &name, std::string const &parameter) {
  // Nothing to return here
  if (name == modelName)
    return boost::any();

  for (auto &model : model_list) {
    auto ret = model->getModelParam(name, parameter);
    if (!ret.empty())
      return ret;
  }
  return boost::any();
}

// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2018-2020
// ARES TAG: name(1) = Doogesh Kodi Ramanah
// ARES TAG: email(1) = ramanah@iap.fr
// ARES TAG: year(1) = 2018-2019
