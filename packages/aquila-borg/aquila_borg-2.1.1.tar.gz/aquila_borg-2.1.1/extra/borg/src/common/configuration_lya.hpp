/*+
    ARES/HADES/BORG Package -- ./extra/borg/src/common/configuration_lya.hpp
    Copyright (C) 2020 Natalia Porqueres <n.porqueres@imperial.ac.uk>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef _ARES3_CONFIGURATION_HPP
#define _ARES3_CONFIGURATION_HPP

#include <CosmoTool/algo.hpp>
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include <cmath>
#include <string>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>
#include <boost/algorithm/string.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/samplers/core/main_loop.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/mcmc/state_sync.hpp"
#include <boost/algorithm/string.hpp>
#include "libLSS/data/projection.hpp"

#include "common/preparation_types.hpp"
#include "common/preparation_tools.hpp"

namespace LibLSS {
    template<typename PTree>
    inline void loadConfigurationFile(MPI_Communication& comm, MainLoop& loop, PTree& params)
    {
        using boost::format;
        using boost::to_lower_copy;
        using details::property_accessor;
        using CosmoTool::square;
        using std::sqrt;
        long N0, N1, N2;
        double L0, L1, L2;
        double K_MAX, K_MIN;
        Console& cons = Console::instance();
        MarkovState& state = loop.get_state();
        PTree system_params = params.get_child("system");
        PTree cosmo_params = params.get_child("cosmology");
        MPI_SyncBundle *syncBundle;
        ptrdiff_t local_size, local_size1, localn0, startn0, localn1, startn1;

        try {
            cons.setVerboseLevel(property_accessor<int>(system_params, "verbose_level"));
        } catch (const boost::property_tree::ptree_bad_path& e) {
          cons.print<LOG_INFO_SINGLE>("Missing option in configuration " + e.path<typename PTree::path_type>().dump());
        } catch (const ErrorParams&) {
            cons.print<LOG_INFO_SINGLE>("Error ignored on VERBOSE_LEVEL");// No parameter equal keep default value
        }

        // Load reconstruction box parameters
        N0 = adapt<long>(state, system_params, "N0", true);
        N1 = adapt<long>(state, system_params, "N1", true);
        N2 = adapt<long>(state, system_params, "N2", true);
        cons.print<LOG_INFO_SINGLE>(format("Got base resolution at %d x %d x %d") % N0 % N1 % N2);

        state.newSyScalar<long>("N2_HC", N2/2+1);

#ifdef ARES_MPI_FFTW
        local_size = MPI_FCalls::local_size_3d(N0, N1, N2, comm.comm(), &localn0, &startn0);
        // Local size when first two dims are swapped
        local_size1 = MPI_FCalls::local_size_3d(N1, N0, N2, comm.comm(), &localn1, &startn1);
#else
        local_size1 = local_size = N0*N1*(N2/2+1);
        localn0 = N0;
        startn0 = 0;

        startn1 = 0;
        localn1 = N1;
#endif
        state.newSyScalar<long>("startN0", startn0);
        state.newSyScalar<long>("localN0", localn0);
        state.newSyScalar<long>("fourierLocalSize", local_size);

        state.newSyScalar<long>("startN1", startn0);
        state.newSyScalar<long>("localN1", localn0);
        state.newSyScalar<long>("fourierLocalSize1", local_size1);


        L0 = adapt<double>(state, system_params, "L0", true);
        L1 = adapt<double>(state, system_params, "L1", true);
        L2 = adapt<double>(state, system_params, "L2", true);

        adapt<double>(state, system_params, "corner0", true);
        adapt<double>(state, system_params, "corner1", true);
        adapt<double>(state, system_params, "corner2", true);
        
        K_MAX = M_PI*sqrt( square(N0/L0) + square(N1/L1) + square(N2/L2) ) * 1.1;
        K_MIN = 0;

        state.newSyScalar<double>("K_MAX", K_MAX);
        state.newSyScalar<double>("K_MIN", K_MIN);
        adapt<long>(state, system_params, "NUM_MODES", true);

        adapt<double>(state, system_params, "ares_heat", 1.0, false);

		bool LymanAlphaData = adapt<bool>(state, system_params, "lyman_alpha_data", false ,false);
		
		if (!LymanAlphaData) {

		    std::string projtype = to_lower_copy(system_params.template get<std::string>("projection_model", "number_ngp"));
		    ProjectionDataModel projmodel = NGP_PROJECTION;
		    std::string projmodel_name;

		    if (projtype == "number_ngp") {
		      projmodel = NGP_PROJECTION;
		      projmodel_name = "Nearest Grid point number count";
		    } else if (projtype == "luminosity_cic") {
		      projmodel = LUMINOSITY_CIC_PROJECTION;
		      projmodel_name = "Luminosity weighted CIC field";
		    } else {
		      error_helper<ErrorParams>("Unknown specified projection model");
		    }

		    cons.print<LOG_INFO_SINGLE>(format("Data and model will use the folllowing method: '%s'") % projmodel_name);

		    state.newScalar<ProjectionDataModel>("projection_model", projmodel);
		}
		
        ScalarStateElement<CosmologicalParameters> *s_cosmo = new ScalarStateElement<CosmologicalParameters>();
        CosmologicalParameters& cosmo = s_cosmo->value;

        // Load cosmology
        cosmo.omega_r = property_accessor<double>(cosmo_params, "omega_r");
        cosmo.omega_k = property_accessor<double>(cosmo_params, "omega_k");
        cosmo.omega_m = property_accessor<double>(cosmo_params, "omega_m");
        cosmo.omega_b = property_accessor<double>(cosmo_params, "omega_b");
        cosmo.omega_q = property_accessor<double>(cosmo_params, "omega_q");
        cosmo.w = property_accessor<double>(cosmo_params, "w");
        cosmo.n_s = property_accessor<double>(cosmo_params, "n_s");
        cosmo.wprime = property_accessor<double>(cosmo_params, "wprime");
        cosmo.sigma8 = property_accessor<double>(cosmo_params, "sigma8");
        cosmo.h = property_accessor<double>(cosmo_params, "h100");
        cosmo.beta = property_accessor<double>(cosmo_params, "beta");
        cosmo.z0 = property_accessor<double>(cosmo_params, "z0");
        cosmo.a0 = 1;
      
        state.newElement("cosmology", s_cosmo, true);
    }



}

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Natalia Porqueres
// ARES TAG: email(0) = n.porqueres@imperial.ac.uk
// ARES TAG: year(0) = 2020

