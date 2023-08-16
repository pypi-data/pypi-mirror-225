/*+
    ARES/HADES/BORG Package -- ./extra/hades/src/hades_mock_gen.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __HADES_MOCK_GEN_HPP
#define __HADES_MOCK_GEN_HPP

#include <CosmoTool/algo.hpp>
#include <cmath>

namespace LibLSS {

  template <typename PTree>
  void prepareMockData(
      PTree &ptree, MPI_Communication *comm, MarkovState &state,
      CosmologicalParameters &cosmo_params, SamplerBundle &bundle) {
    ConsoleContext<LOG_INFO_SINGLE> ctx("prepareMockData");
    using boost::format;
    using CosmoTool::square;

    double Rsmooth = ptree.template get<double>("system.hades_smoothing", 1.0);
//    createCosmologicalPowerSpectrum(state, cosmo_params);

    bundle.sel_updater.sample(state);
    bundle.density_mc->generateMockData(state);

    {
      std::shared_ptr<H5::H5File> f;

      if (comm->rank() == 0) {
        f = std::make_shared<H5::H5File>("mock_data.h5", H5F_ACC_TRUNC);
      }
      state.mpiSaveState(f, comm, false);
    }

    //        bundle.hmc->generateRandomField(state);
    //        state.get<CArrayType>("s_hat_field")->eigen() *= 0.02;
    //        state.get<ArrayType>("s_field")->eigen() *= 0.02;
  }
} // namespace LibLSS

#endif
