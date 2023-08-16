/*+
    ARES/HADES/BORG Package -- ./extra/python/src/python_mock_gen.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __HADES_PYTHON_MOCK_GEN_HPP
#define __HADES_PYTHON_MOCK_GEN_HPP

#include <CosmoTool/algo.hpp>
#include <cmath>
#include "common/preparation_types.hpp" 

namespace LibLSS {

  void prepareMockData(
      LibLSS_prepare::ptree &ptree, MPI_Communication *comm, MarkovState &state,
      CosmologicalParameters &cosmo_params, SamplerBundle &bundle);
} // namespace LibLSS

#endif
