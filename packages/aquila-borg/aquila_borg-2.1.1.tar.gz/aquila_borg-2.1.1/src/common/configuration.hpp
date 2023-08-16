/*+
    ARES/HADES/BORG Package -- ./src/common/configuration.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

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

#include "preparation_types.hpp"
#include "preparation_tools.hpp"

namespace LibLSS {

  /**
   * @brief This function loads the configuration stored in the property tree params and fills up
   * the MarkovState dictionnary of the MainLoop
   *
   * @tparam PTree the property tree type, it will be deduced from parameter
   * @param comm an MPI communicator
   * @param loop the main loop to configure
   * @param params the property tree filled up from a configuration file
   */
  template <typename PTree>
  inline void loadConfigurationFile(
      MPI_Communication &comm, MainLoop &loop, PTree &params) {
    using boost::format;
    using boost::to_lower_copy;
    using CosmoTool::square;
    using details::property_accessor;
    using std::sqrt;
    long N0, N1, N2, Ndata0, Ndata1, Ndata2;
    double L0, L1, L2;
    double K_MAX, K_MIN;
    Console &cons = Console::instance();
    MarkovState &state = loop.get_state();
    PTree system_params = params.get_child("system");
    PTree cosmo_params = params.get_child("cosmology");
    MPI_SyncBundle *syncBundle;
    ptrdiff_t local_size, local_size1, localn0, startn0, localn1, startn1;

    try {
      cons.setVerboseLevel(
          property_accessor<int>(system_params, "verbose_level"));
    } catch (const boost::property_tree::ptree_bad_path &e) {
      cons.print<LOG_INFO_SINGLE>(
          "Missing option in configuration " +
          e.path<typename PTree::path_type>().dump());
    } catch (const ErrorParams &) {
      cons.print<LOG_INFO_SINGLE>(
          "Error ignored on VERBOSE_LEVEL"); // No parameter equal keep default value
    }

    if (auto o = system_params.template get_optional<int>("logfile_verbose_level")) {
      cons.format<LOG_INFO_SINGLE>("Setting up logfile level to %d", *o);
      cons.setLogfileVerboseLevel(*o);
    }

    // Load reconstruction box parameters
    N0 = adapt<long>(state, system_params, "N0");
    N1 = adapt<long>(state, system_params, "N1");
    N2 = adapt<long>(state, system_params, "N2");
    Ndata0 = adapt<long>(state, system_params, "Ndata0", N0);
    Ndata1 = adapt<long>(state, system_params, "Ndata1", N1);
    Ndata2 = adapt<long>(state, system_params, "Ndata2", N2);
    cons.print<LOG_INFO_SINGLE>(
        format("Got base resolution at %d x %d x %d") % N0 % N1 % N2);

    state.newScalar<long>("N2_HC", N2 / 2 + 1);

    size_t localNdata[6];

#ifdef ARES_MPI_FFTW
    local_size =
        MPI_FCalls::local_size_3d(N0, N1, N2, comm.comm(), &localn0, &startn0);
    // Local size when first two dims are swapped
    local_size1 =
        MPI_FCalls::local_size_3d(N1, N0, N2, comm.comm(), &localn1, &startn1);
    state.newScalar<long>("N2real", 2 * (N2 / 2 + 1));

    {
      ptrdiff_t data_localn0, data_startn0;
      MPI_FCalls::local_size_3d(
          Ndata0, Ndata1, Ndata2, comm.comm(), &data_localn0, &data_startn0);

      localNdata[0] = data_startn0;
      localNdata[1] = data_startn0 + data_localn0;
      localNdata[2] = 0;
      localNdata[3] = Ndata1;
      localNdata[4] = 0;
      localNdata[5] = Ndata2;
    }
#else
    state.newScalar<long>("N2real", N2);
    local_size1 = local_size = N0 * N1 * (N2 / 2 + 1);
    localn0 = N0;
    startn0 = 0;

    startn1 = 0;
    localn1 = N1;
    state.newScalar<long>("N2real", N2);
    localNdata[0] = 0;
    localNdata[1] = Ndata0;
    localNdata[2] = 0;
    localNdata[3] = Ndata1;
    localNdata[4] = 0;
    localNdata[5] = Ndata2;
#endif
    for (int i = 0; i < 6; i++)
      state.newScalar<long>(boost::format("localNdata%d") % i, localNdata[i])
          ->setDoNotRestore(true);
    state.newScalar<long>("startN0", startn0);
    state.newScalar<long>("localN0", localn0);
    state.newScalar<long>("fourierLocalSize", local_size);

    state.newScalar<long>("startN1", startn0);
    state.newScalar<long>("localN1", localn0);
    state.newScalar<long>("fourierLocalSize1", local_size1);

    L0 = adapt<double>(state, system_params, "L0");
    L1 = adapt<double>(state, system_params, "L1");
    L2 = adapt<double>(state, system_params, "L2");

    adapt<double>(state, system_params, "corner0");
    adapt<double>(state, system_params, "corner1");
    adapt<double>(state, system_params, "corner2");

    K_MAX =
        M_PI * sqrt(square(N0 / L0) + square(N1 / L1) + square(N2 / L2)) * 1.1;
    K_MIN = 0;

    state.newScalar<double>("K_MAX", K_MAX);
    state.newScalar<double>("K_MIN", K_MIN);
    adapt<long>(state, system_params, "NUM_MODES");

    adapt<double>(state, system_params, "ares_heat", 1.0);

    ScalarStateElement<CosmologicalParameters> *s_cosmo =
        new ScalarStateElement<CosmologicalParameters>();
    CosmologicalParameters &cosmo = s_cosmo->value;

    // Load cosmology
    cosmo.omega_r = property_accessor<double>(cosmo_params, "omega_r");
    cosmo.omega_k = property_accessor<double>(cosmo_params, "omega_k");
    cosmo.omega_m = property_accessor<double>(cosmo_params, "omega_m");
    cosmo.omega_b = property_accessor<double>(cosmo_params, "omega_b");
    cosmo.omega_q = property_accessor<double>(cosmo_params, "omega_q");
    cosmo.w = property_accessor<double>(cosmo_params, "w");
    cosmo.n_s = property_accessor<double>(cosmo_params, "n_s");
    cosmo.fnl = property_accessor<double>(cosmo_params, "fnl");
    cosmo.wprime = property_accessor<double>(cosmo_params, "wprime");
    cosmo.sigma8 = property_accessor<double>(cosmo_params, "sigma8");
    cosmo.h = property_accessor<double>(cosmo_params, "h100");
    cosmo.beta = property_accessor<double>(cosmo_params, "beta");
    cosmo.z0 = property_accessor<double>(cosmo_params, "z0");
    cosmo.a0 = 1;

    state.newElement("cosmology", s_cosmo, true); //true);
  }

} // namespace LibLSS

#endif
