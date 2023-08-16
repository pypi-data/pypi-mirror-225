/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/patch_model.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <memory>
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/physics/chain_forward_model.hpp"
#include "libLSS/physics/forwards/patch_model.hpp"
#include "libLSS/physics/forwards/transfer.hpp"
#include "libLSS/physics/forwards/borg_lpt.hpp"
#include "libLSS/physics/forwards/downgrade.hpp"
#include "libLSS/physics/hades_pt.hpp"
#include "libLSS/physics/hades_log.hpp"
#include "libLSS/tools/overload.hpp"
#include "libLSS/physics/forwards/transfer_ehu.hpp"
#include "libLSS/physics/forwards/primordial.hpp"
#include "libLSS/tools/ptree_proxy_map.hpp"

#include "libLSS/physics/forwards/adapt_generic_bias.hpp"

using namespace LibLSS;

namespace {
  class Scaler : public BORGForwardModel {
  public:
    ModelInput<3> hold_input;
    ModelInputAdjoint<3> hold_ag_input;
    std::string pName;

    Scaler(
        MPI_Communication *comm, BoxModel const &box, std::string const &pName_)
        : BORGForwardModel(comm, box), pName(pName_) {
      setModelParams({{pName, 0.05}});
    }

    PreferredIO getPreferredInput() const override { return PREFERRED_REAL; }
    PreferredIO getPreferredOutput() const override { return PREFERRED_REAL; }

    void forwardModel_v2(ModelInput<3> input) override {
      LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
      input.setRequestedIO(PREFERRED_REAL);
      hold_input = std::move(input);
    }

    void getDensityFinal(ModelOutput<3> output) override {
      LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
      output.setRequestedIO(PREFERRED_REAL);
      if (params.find(pName) == params.end()) {
        error_helper<ErrorParams>("Missing " + pName + " parameter.");
      }
      double const aux = boost::any_cast<double>(params[pName]);
      ctx.format("Using scaling %s=%g", pName, aux);

      fwrap(output.getRealOutput()) = aux * fwrap(hold_input.getRealConst());
    }

    void adjointModel_v2(ModelInputAdjoint<3> input) override {
      LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
      input.setRequestedIO(PREFERRED_REAL);
      hold_ag_input = std::move(input);
    }

    void getAdjointModelOutput(ModelOutputAdjoint<3> output) override {
      LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
      output.setRequestedIO(PREFERRED_REAL);
      if (params.find(pName) == params.end()) {
        error_helper<ErrorParams>("Missing " + pName + " parameter.");
      }
      double const aux = boost::any_cast<double>(params[pName]);
      fwrap(output.getRealOutput()) = aux * fwrap(hold_ag_input.getRealConst());
    }
  };

  class FrozenCache : public BORGForwardModel {
  public:
    ModelOutput<3> hold_output;
    std::shared_ptr<BORGForwardModel> alt_model;
    bool invalid;

    FrozenCache(
        MPI_Communication *comm, std::shared_ptr<BORGForwardModel> alt_model_)
        : BORGForwardModel(
              comm, alt_model_->get_box_model(),
              alt_model_->get_box_model_output()),
          alt_model(alt_model_) {
      invalid = true;
    }

    PreferredIO getPreferredInput() const override {
      return hold_output ? PREFERRED_NONE : alt_model->getPreferredInput();
    }
    PreferredIO getPreferredOutput() const override {
      return hold_output ? hold_output.current
                         : alt_model->getPreferredOutput();
    }

    bool densityInvalidated() const override { return invalid; }

    void forwardModel_v2(ModelInput<3> input) override {
      LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
      if (!hold_output)
        alt_model->forwardModel_v2(std::move(input));
    }

    void getDensityFinal(ModelOutput<3> output) override {
      LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
      invalid = false;
      if (!hold_output) {
        ctx.print("Cache invalid. Recompute");
        hold_output = output.makeTempLike();
        alt_model->getDensityFinal(hold_output.shallowClone());
      } else {
        ctx.print("Cache valid. Reuse.");
        output.setRequestedIO(hold_output.current);
        ctx.format(
            "output.active = %d, hold.active = %d", output.active,
            hold_output.current);
      }
      output.copyFrom(hold_output);
    }

    void adjointModel_v2(ModelInputAdjoint<3> input) override {}

    void getAdjointModelOutput(ModelOutputAdjoint<3> output) override {
      LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
      ctx.print("Clear adjoint output");
      boost::apply_visitor(
          overload([](auto const *v) {}, [](auto *v) { fwrap(*v) = 0.0; }),
          output.getHolder());
    }

    void setModelParams(ModelDictionnary const &params) override {
      alt_model->setModelParams(params);
    }

    boost::any
    getModelParam(std::string const &n, std::string const &param) override {
      LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
      return alt_model->getModelParam(n, param);
    }

    void updateCosmo() override {
      LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
      alt_model->setCosmoParams(cosmo_params);
      if (alt_model->densityInvalidated()) {
        ctx.print("Submodel has invalidated its density field.");
        invalid = true;
        hold_output = ModelOutput<3>();
      }
    }
  };
} // namespace

static std::shared_ptr<BORGForwardModel> new_patch_model(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params) {
  /*  auto transfer_filename = params.get_optional<std::string>("transfer");
  auto transfer_cic = params.get_optional<bool>("use_invert_cic");
  auto transfer_sharp = params.get_optional<bool>("use_sharpk");*/
  auto ai = params.get<double>("ai");
  auto af = params.get<double>("af");
  auto k_transition = params.get<double>("k_transition");
  auto part_factor = params.get<double>("part_factor", 1.2);

  BoxModel box2 = box;
  box2.N0 *= 2;
  box2.N1 *= 2;
  box2.N2 *= 2;

  auto transfer1 = std::make_shared<ForwardTransfer>(comm, box);
  auto transfer2 = std::make_shared<ForwardTransfer>(comm, box);
  auto inverse_cic = std::make_shared<ForwardTransfer>(comm, box2);

  auto lpt = std::make_shared<BorgLptModel<>>(
      comm, box, box, false, 2, part_factor, ai, af, false);
  auto sum = std::make_shared<SumForwardModel>(comm, box);

  transfer1->setupSharpKcut(k_transition, false);
  transfer2->setupSharpKcut(k_transition, true);
  inverse_cic->setupInverseCIC(0.95);

  auto chain1 = std::make_shared<ChainForwardModel>(comm, box);
  auto chain1_1 = std::make_shared<ChainForwardModel>(comm, box);
  chain1->addModel(std::make_shared<ForwardPrimordial>(comm, box, ai));
  chain1->addModel(std::make_shared<ForwardEisensteinHu>(comm, box));
  chain1->addModel(transfer1);
  chain1->addModel(lpt);
  //chain1->addModel(inverse_cic);
  //chain1->addModel(std::make_shared<ForwardDowngrade>(comm, box2));
  //chain1->addModel(transfer3);
  //auto biasModel = ForwardRegistry::instance().get("bias::LinearBias")(
  //    comm, box, PropertyFromMap());
  //  auto biasModel = ForwardRegistry::instance().get("bias::PowerLaw")(
  //      comm, box, PropertyFromMap());
  auto biasModel = ForwardRegistry::instance().get("bias::ManyPower_1^2")(
      comm, box, PropertyFromMap());
  biasModel->setName("bias");
  chain1_1->addModel(chain1); //std::make_shared<FrozenCache>(comm, chain1));
  chain1_1->addModel(biasModel);

  auto chain2 = std::make_shared<ChainForwardModel>(comm, box);
  chain2->addModel(transfer2);
  chain2->addModel(std::make_shared<Scaler>(comm, box, "aux"));
  chain2->addModel(std::make_shared<HadesLog>(comm, box, ai, false));
  chain2->addModel(std::make_shared<Scaler>(comm, box, "aux2"));
  //chain2->addModel(std::make_shared<HadesLinear>(comm, box, box, ai, af));

  sum->addModel(chain1_1);
  sum->addModel(chain2);

  return sum;
}

LIBLSS_REGISTER_FORWARD_IMPL(PATCH_MODEL, new_patch_model);

