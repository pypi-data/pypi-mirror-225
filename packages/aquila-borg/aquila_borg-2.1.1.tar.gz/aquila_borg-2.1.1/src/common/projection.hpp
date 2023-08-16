/*+
    ARES/HADES/BORG Package -- ./src/common/projection.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef _ARES_PROJECTION_SETUP_HPP
#define _ARES_PROJECTION_SETUP_HPP

#include <CosmoTool/algo.hpp>
#include <cmath>
#include <string>
#include <boost/property_tree/ptree.hpp>
#include <boost/algorithm/string.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/samplers/core/main_loop.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/data/projection.hpp"

namespace LibLSS {
  template <typename PTree>
  inline void
  setupProjection(MPI_Communication &comm, MainLoop &loop, PTree &params) {
    using boost::to_lower_copy;

    PTree system_params = params.get_child("system");
    std::string projtype =
        to_lower_copy(system_params.template get<std::string>(
            "projection_model", "number_ngp"));
    ProjectionDataModel projmodel = NGP_PROJECTION;
    std::string projmodel_name;
    Console &cons = Console::instance();
    MarkovState &state = loop.get_state();

    if (projtype == "number_ngp") {
      projmodel = NGP_PROJECTION;
      projmodel_name = "Nearest Grid point number count";
    } else if (projtype == "luminosity_cic") {
      projmodel = LUMINOSITY_CIC_PROJECTION;
      projmodel_name = "Luminosity weighted CIC field";
    } else {
      error_helper<ErrorParams>("Unknown specified projection model");
    }

    cons.print<LOG_INFO_SINGLE>(
        boost::format("Data and model will use the folllowing method: '%s'") %
        projmodel_name);

    state.newScalar<ProjectionDataModel>("projection_model", projmodel);
  }
} // namespace LibLSS

#endif
