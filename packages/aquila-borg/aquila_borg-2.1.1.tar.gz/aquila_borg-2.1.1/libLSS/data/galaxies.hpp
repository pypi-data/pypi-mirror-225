/*+
    ARES/HADES/BORG Package -- ./libLSS/data/galaxies.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_GALAXIES_HPP
#define __LIBLSS_GALAXIES_HPP


#include <CosmoTool/hdf5_array.hpp>

namespace LibLSS {

    struct BaseGalaxyDescriptor {
        unsigned long long id;
        double phi, theta;
        double zo;
        double m;
        double M_abs;
        double Mgal;
        double z;
        double r;
        double w;
        double final_w;

        double radius;
        double spin;
        double posx, posy ,posz;

        double vx, vy, vz;
    };

    struct PhotoGalaxyDescriptor {
        BaseGalaxyDescriptor base;
        double sigma_z0;
        int gridid;
    };


    enum GalaxySelectionType {
      GALAXY_SELECTION_FILE,
      GALAXY_SELECTION_SCHECHTER,
      GALAXY_SELECTION_PIECEWISE,
      HALO_SELECTION_NONE,
      HALO_SELECTION_MASS,
      HALO_SELECTION_RADIUS,
      HALO_SELECTION_SPIN,
      HALO_SELECTION_MIXED
    };
};

  CTOOL_ENUM_TYPE(LibLSS::GalaxySelectionType, HDF5T_GalaxySelectionType,
    (LibLSS::GALAXY_SELECTION_FILE)
    (LibLSS::GALAXY_SELECTION_SCHECHTER)
    (LibLSS::GALAXY_SELECTION_PIECEWISE)
    (LibLSS::HALO_SELECTION_NONE)
    (LibLSS::HALO_SELECTION_MASS)
    (LibLSS::HALO_SELECTION_RADIUS)
    (LibLSS::HALO_SELECTION_SPIN)
    (LibLSS::HALO_SELECTION_MIXED)
  );

  /* HDF5 complex type */
  CTOOL_STRUCT_TYPE(LibLSS::BaseGalaxyDescriptor, HDF5T_BaseGalaxyDescriptor,
    ((unsigned long long, id))
    ((double, phi))
    ((double, theta))
    ((double, posx))
    ((double, posy))
    ((double, posz))
	((double, radius))
    ((double, spin))
    ((double, zo))
    ((double, m))
    ((double, M_abs))
    ((double, Mgal))
    ((double, z))
    ((double, vx))
    ((double, vy))
    ((double, vz))
    ((double, r))
    ((double, w))
    ((double, final_w))
  );

  CTOOL_STRUCT_TYPE(LibLSS::PhotoGalaxyDescriptor, HDF5T_PhotoGalaxyDescriptor,
    ((LibLSS::BaseGalaxyDescriptor, base))
    ((double, sigma_z0))
    ((int, gridid))
  );


#endif
