/*+
    ARES/HADES/BORG Package -- ./libLSS/data/survey_load_bin.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_GALAXY_LOAD_BIN_HPP
#define __LIBLSS_GALAXY_LOAD_BIN_HPP

#include <string>
#include <fstream>
#include <iostream>
#include <sstream>
#include <boost/format.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/errors.hpp"
#include <CosmoTool/hdf5_array.hpp>
#include <H5Cpp.h>

namespace LibLSS {


  struct BinGalaxyStruct {
     size_t id;
     double phi, theta;
     double zo;
     double m;
     double M_abs;
     double z;
     double w;
  };

  struct BinHaloStruct {
    size_t id;
    double Mgal, radius, spin, posx, posy, posz, vx, vy, vz;
    double w;
  };

}

CTOOL_STRUCT_TYPE(LibLSS::BinGalaxyStruct, HDF5T_LibLSS_BinGalaxyStruct,
  ((size_t, id))
  ((double, phi))
  ((double, theta))
  ((double, zo))
  ((double, m))
  ((double, M_abs))
  ((double, z))
  ((double, w))
);

CTOOL_STRUCT_TYPE(LibLSS::BinHaloStruct, HDF5T_LibLSS_BinHaloStruct,
  ((size_t, id))
  ((double, Mgal))
  ((double, radius))
  ((double, spin))
  ((double, posx))
  ((double, posy))
  ((double, posz))
  ((double, vx))
  ((double, vy))
  ((double, vz))
  ((double, w))
);

namespace LibLSS {
  template<typename GalaxySurvey>
  void  loadCatalogFromHDF5(
      const std::string& fname,
      const std::string& key,
      GalaxySurvey& sim) {
        using namespace std;
        using boost::format;
        Console& cons = Console::instance();
        long originalSize = sim.surveySize();

        cons.print<LOG_STD>(format("Reading HDF5 catalog file '%s' / key '%s'") % fname % key);
        bool warningDefault = false;

        boost::multi_array<BinGalaxyStruct, 1> halos;

        H5::H5File f(fname, H5F_ACC_RDONLY) ;
        CosmoTool::hdf5_read_array(f, key, halos);
        auto& gals = sim.allocateGalaxies(halos.shape()[0]);
        for (size_t i = 0; i < halos.num_elements(); i++) {
          gals[i].id = halos[i].id;
          gals[i].phi = halos[i].phi;
          gals[i].theta = halos[i].theta;
          gals[i].final_w = gals[i].w = halos[i].w;
          gals[i].m = halos[i].m;
          gals[i].M_abs = halos[i].M_abs;
          gals[i].z = halos[i].z;
          gals[i].zo = halos[i].zo;
        }
        cons.print<LOG_STD>(format("Got %d halos") % gals.num_elements());
   }

  template<typename GalaxySurvey>
  void  loadHaloSimulationFromHDF5(
      const std::string& fname,
      const std::string& key,
      GalaxySurvey& sim) {
        using namespace std;
        using boost::format;
        Console& cons = Console::instance();
        long originalSize = sim.surveySize();

        cons.format<LOG_STD>("Reading HDF5 catalog file '%s' / key '%s'", fname , key);
        bool warningDefault = false;

        boost::multi_array<BinHaloStruct, 1> halos;

        H5::H5File f(fname, H5F_ACC_RDONLY) ;
	cons.print<LOG_STD>("Reading data file");
        CosmoTool::hdf5_read_array(f, key, halos);
	cons.print<LOG_STD>("Transfering to internal structure");
        auto& gals = sim.allocateGalaxies(halos.num_elements());
        for (size_t i = 0; i < halos.num_elements(); i++) {
          gals[i].id = halos[i].id;
          gals[i].final_w = gals[i].w = halos[i].w;
          gals[i].posx = halos[i].posx;
          gals[i].posy = halos[i].posy;
          gals[i].posz = halos[i].posz;
          gals[i].vx = halos[i].vx;
          gals[i].vy = halos[i].vy;
          gals[i].vz = halos[i].vz;
          gals[i].spin = halos[i].spin;
          gals[i].radius = halos[i].radius;
          gals[i].Mgal = halos[i].Mgal;
          vec2ang(std::array<double,3>{halos[i].posx,halos[i].posy,halos[i].posz}, gals[i].phi, gals[i].theta, gals[i].r);
        }
        cons.print<LOG_STD>(format("Got %d halos") % gals.num_elements());
   }
} 

#endif
