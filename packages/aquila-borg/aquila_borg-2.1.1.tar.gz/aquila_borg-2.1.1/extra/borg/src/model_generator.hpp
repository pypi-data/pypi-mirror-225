/*+
    ARES/HADES/BORG Package -- ./extra/borg/src/model_generator.hpp
    Copyright (C) 2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_BORG_MODEL_GENERATOR_HPP
#  define __LIBLSS_BORG_MODEL_GENERATOR_HPP

#  include <functional>
#  include <map>
#  include "libLSS/tools/ptree_proxy.hpp"
#  include "setup_models.hpp"

namespace LibLSS {

  // typedef std::function<std::shared_ptr<BORGForwardModel>(
  //     MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params,
  //     ParticleSaver_t &, TimingSaver_t &, int &)>
  //     ModelSetup_t;

  // ModelSetup_t setup_forward_model(std::string const &model_name);

} // namespace LibLSS

#endif

// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2018
