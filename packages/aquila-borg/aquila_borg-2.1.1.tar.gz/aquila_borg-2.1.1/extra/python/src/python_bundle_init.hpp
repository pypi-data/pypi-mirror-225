/*+
    ARES/HADES/BORG Package -- ./extra/python/src/python_bundle_init.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __HADES_PYTHON_BUNDLE_INIT_HPP
#define __HADES_PYTHON_BUNDLE_INIT_HPP

#include "python_bundle.hpp"
#include "likelihood_info.hpp"
#include "setup_models.hpp"
#include "common/preparation_types.hpp"

namespace LibLSS {

  void sampler_bundle_init(
      MPI_Communication *mpi_world, LibLSS_prepare::ptree &params, SamplerBundle &bundle,
      MainLoop &loop, bool resuming);

  void
  sampler_setup_ic(SamplerBundle &bundle, MainLoop &loop, LibLSS_prepare::ptree const &params);

  void sampler_bundle_cleanup();

} // namespace LibLSS

#endif
