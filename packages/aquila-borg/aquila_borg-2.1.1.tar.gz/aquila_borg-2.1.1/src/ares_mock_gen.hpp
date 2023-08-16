/*+
    ARES/HADES/BORG Package -- ./src/ares_mock_gen.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __ARES_MOCK_GEN_HPP
#define __ARES_MOCK_GEN_HPP

namespace LibLSS {

    template<typename PTree>
    void prepareMockData(PTree& ptree, MPI_Communication *comm, MarkovState& state,
                        CosmologicalParameters& cosmo_params,
                        SamplerBundle& bundle
                        ) {
        ConsoleContext<LOG_INFO_SINGLE> ctx("prepareMockData");
        using boost::format;
     
        createCosmologicalPowerSpectrum(state, cosmo_params);

        bundle.sel_updater.sample(state);
        bundle.sampler_s.setMockGeneration(true);
        bundle.sampler_catalog_projector.setMockGeneration(true);
        
        // Generate the tau
        bundle.sampler_catalog_projector.sample(state);
        bundle.sampler_s.sample(state);
        // Generate the data
        bundle.sampler_catalog_projector.sample(state);
        
        bundle.sampler_s.setMockGeneration(false);
        bundle.sampler_t.setMockGeneration(false);
        bundle.sampler_catalog_projector.setMockGeneration(false);

        {
            std::shared_ptr<H5::H5File> f;

            if (comm->rank() == 0)
              f = std::make_shared<H5::H5File>("mock_data.h5", H5F_ACC_TRUNC);
            state.mpiSaveState(f, comm, false);
        }
            
        state.get<ArrayType>("s_field")->eigen().fill(0);
        state.get<ArrayType>("x_field")->eigen().fill(0);
    }
}

#endif
