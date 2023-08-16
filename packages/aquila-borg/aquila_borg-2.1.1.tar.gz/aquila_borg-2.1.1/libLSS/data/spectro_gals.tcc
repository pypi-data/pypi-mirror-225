/*+
    ARES/HADES/BORG Package -- ./libLSS/data/spectro_gals.tcc
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/tools/hdf5_scalar.hpp"
#include "libLSS/tools/hdf5_type.hpp"

namespace LibLSS {

template<typename SelFunction, class GalaxyType, class AllocationPolicy>
void GalaxySurvey<SelFunction,GalaxyType,AllocationPolicy>::addGalaxy(const GalaxyType& galaxy) {
    if (numGalaxies == galaxies.size()) {
        galaxies.resize(boost::extents[numGalaxies+AllocationPolicy::getIncrement()]);
    }

    galaxies[numGalaxies] = galaxy;

    numGalaxies++;
}

template<typename SelFunction, class GalaxyType, class AllocationPolicy>
void GalaxySurvey<SelFunction,GalaxyType,AllocationPolicy>::resetWeight() {
  for (size_t i = 0; i < numGalaxies; i++) {
    galaxies[i].final_w = galaxies[i].w;
  }
}

template<typename SelFunction, class GalaxyType, class AllocationPolicy>
void GalaxySurvey<SelFunction,GalaxyType,AllocationPolicy>::useLuminosityAsWeight() {
  for (size_t i = 0; i < numGalaxies; i++) {
    // Add a 10^8 scaling to put the values within a reasonable range scales for the MCMC.
    double L = std::pow(10, -0.4*galaxies[i].M_abs)/1e8;
    galaxies[i].final_w = galaxies[i].w * L;
  }
}

template<typename SelFunction, class GalaxyType, class AllocationPolicy>
void GalaxySurvey<SelFunction,GalaxyType,AllocationPolicy>::saveMain(H5_CommonFileGroup& fg)
{
    optimize();
    CosmoTool::hdf5_write_array(fg, "galaxies", galaxies );

    hdf5_save_scalar(fg, "is_reference_survey", is_reference_survey);
}

template<typename SelFunction, class GalaxyType, class AllocationPolicy>
void GalaxySurvey<SelFunction,GalaxyType,AllocationPolicy>::restoreMain(H5_CommonFileGroup& fg)
{
    CosmoTool::hdf5_read_array(fg, "galaxies", galaxies );
    numGalaxies = galaxies.size();
    is_reference_survey = hdf5_load_scalar<bool>(fg, "is_reference_survey");
}


template<typename SelFunction, class GalaxyType, class AllocationPolicy>
void GalaxySurvey<SelFunction,GalaxyType,AllocationPolicy>::updateComovingDistance(const Cosmology& cosmo, const CorrectionFunction& zcorrection)
{
    LibLSS::ConsoleContext<LOG_DEBUG> ctx("Updating comoving positions of galaxies");
#pragma omp parallel for
    for (size_t i = 0; i < numGalaxies; i++) {
        if (galaxies[i].z < 0) {
          galaxies[i].r = 0;
          galaxies[i].M_abs = std::numeric_limits<double>::infinity();
          continue;
        }
        galaxies[i].r = cosmo.com2comph(cosmo.a2com(cosmo.z2a(galaxies[i].z)));
        double dlum = cosmo.d2dlum(galaxies[i].z, galaxies[i].r);
        double zcorr = zcorrection(galaxies[i].z);
//        ctx.print(boost::format("z[%d] = %lg, m_correction = %lg") % i % galaxies[i].z % zcorr);
        galaxies[i].M_abs = galaxies[i].m - 5 * std::log10(dlum) - 25 - zcorr;
    }
}

};
