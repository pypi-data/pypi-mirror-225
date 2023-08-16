/*+
    ARES/HADES/BORG Package -- ./extra/hades/src/setup_models.hpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __BORG_FORWARD_MODELS_HPP
#  define __BORG_FORWARD_MODELS_HPP

#  include <memory>
#  include "libLSS/tools/console.hpp"
#  include "libLSS/physics/forward_model.hpp"
#  include "libLSS/tools/ptree_vectors.hpp"
#  include "libLSS/tools/string_tools.hpp"
#  include "libLSS/tools/itertools.hpp"
#  include "libLSS/physics/chain_forward_model.hpp"
#  include "libLSS/physics/forwards/registry.hpp"
#  include "libLSS/physics/forwards/primordial.hpp"
#  include "libLSS/physics/forwards/transfer_ehu.hpp"
#  include "libLSS/physics/hermitic.hpp"

namespace LibLSS {

  typedef std::function<void(CosmoTool::H5_CommonFileGroup &, bool, bool, int)>
      ParticleSaver_t;
  typedef std::function<void(CosmoTool::H5_CommonFileGroup &)> TimingSaver_t;

  /**
   * @brief Build a new complete forward model from configuration.
   * 
   * This function construct a new complete forward model from
   * the provided property tree holding configuration.
   * 
   * @tparam ptree Property tree type
   * @param comm MPI communicator
   * @param box Basic box size
   * @param params Property tree root parameter
   * @param current Current sub-property-tree
   * @return std::shared_ptr<BORGForwardModel> the forward model
  */
  template <typename ptree>
  std::shared_ptr<ChainForwardModel> buildModel(
      MPI_Communication *comm, MarkovState &state, BoxModel box, ptree &params,
      ptree &current) {
    std::string model_type = current.template get<std::string>("model");
    double ai = adapt<double>(
        state, current, "a_initial", 0.001, RESTORE, "borg_a_initial");
    double af =
        adapt<double>(state, current, "a_final", 1.0, RESTORE, "borg_a_final");

    Console::instance().print<LOG_VERBOSE>("Init borg model: " + model_type);

    ParticleSaver_t save_particles;
    TimingSaver_t save_timing;
    if (model_type == "CHAIN") {
      auto model = std::make_shared<ChainForwardModel>(comm, box);
      auto split_models = string_as_vector<std::string>(
          current.template get<std::string>("models"), ",");
      model->addModel(std::make_shared<ForwardHermiticOperation>(comm, box));
      for (auto this_model : itertools::enumerate(split_models)) {
        Console::instance().print<LOG_VERBOSE>(
            "Chaining with " + this_model.template get<1>());
        auto setup = setup_forward_model(this_model.template get<1>());
        std::string sub_name = std::string("gravity_chain_") +
                               to_string(this_model.template get<0>());
        auto new_model = setup(
            comm, box,
            make_proxy_property_tree(params.get_child_optional(sub_name)));

        if (auto name = params.template get_optional<std::string>(sub_name + ".name")) {
          model->addModel(new_model, *name);
        } else {
          model->addModel(new_model);
        }
        box = new_model->get_box_model_output();
      }
      return model;
    } else {
      auto setup = setup_forward_model(model_type);

      auto model = std::make_shared<ChainForwardModel>(comm, box);
      auto real_model = setup(comm, box, make_proxy_property_tree(current));

      model->addModel(std::make_shared<ForwardHermiticOperation>(comm, box));
      model->addModel(std::make_shared<ForwardPrimordial>(comm, box, ai));
      model->addModel(std::make_shared<ForwardEisensteinHu>(comm, box));
      model->addModel(real_model, "dynamics");
      return model;
      ;
    }
  }

} // namespace LibLSS
#endif
// ARES TAG: num_authors = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
