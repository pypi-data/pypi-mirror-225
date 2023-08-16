/*+
    ARES/HADES/BORG Package -- ./extra/python/src/python_mock_gen.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

#include "libLSS/cconfig.h"
#include <CosmoTool/algo.hpp>
#include "libLSS/tools/string_tools.hpp"
#include <cmath>
#include "python_bundle.hpp"
#include "python_mock_gen.hpp"
#include "libLSS/physics/cosmo_power.hpp"
#include <pybind11/pybind11.h>

using namespace LibLSS;

void LibLSS::prepareMockData(
    LibLSS_prepare::ptree &ptree, MPI_Communication *comm, MarkovState &state,
    CosmologicalParameters &cosmo_params, SamplerBundle &bundle) {
  ConsoleContext<LOG_INFO_SINGLE> ctx("prepareMockData");
  using boost::format;
  using CosmoTool::square;

  createCosmologicalPowerSpectrum(state, cosmo_params);

  bundle.sel_updater.sample(state);
  try {
    bundle.density_mc->generateMockData(state);
  } catch (pybind11::error_already_set const &e) {
    Console::instance().print<LOG_ERROR>("An error was thrown by python:");
    Console::instance().print<LOG_ERROR>(LibLSS::tokenize(e.what(), "\n"));
    error_helper<ErrorBadState>("Python thrown an unrecoverable error.");
  }

  {
    std::shared_ptr<H5::H5File> f;

    if (comm->rank() == 0)
      f = std::make_shared<H5::H5File>("mock_data.h5", H5F_ACC_TRUNC);
    state.mpiSaveState(f, comm, false);
  }
}
