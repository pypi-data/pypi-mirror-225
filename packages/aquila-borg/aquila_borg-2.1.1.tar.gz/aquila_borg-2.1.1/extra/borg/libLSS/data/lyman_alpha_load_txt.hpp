/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/data/lyman_alpha_load_txt.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_LYMAN_ALPHA_LOAD_TXT_HPP
#define __LIBLSS_LYMAN_ALPHA_LOAD_TXT_HPP

#include <string>
#include <fstream>
#include <iostream>
#include <sstream>
#include <boost/format.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/errors.hpp"
#include "boost/multi_array.hpp"
#include <CosmoTool/hdf5_array.hpp>
#include <libLSS/physics/projector.hpp>
#include <H5Cpp.h>

namespace LibLSS {


  struct BinsSpectraStruct {
     size_t id;
     double phi, theta;
     double r;
     double z;
  };
}

CTOOL_STRUCT_TYPE(LibLSS::BinsSpectraStruct, HDF5T_LibLSS_BinsSpectraStruct,
  ((size_t, id))
  ((double, phi))
  ((double, theta))
  ((double, z))
  ((double, r))
);

namespace LibLSS {
  template<typename LymanAlphaSurvey>
  void  loadLymanAlphaFromHDF5(
      const std::string& fname,
      LymanAlphaSurvey& survey, MarkovState& state) {
      
        std::cout << "ENTER load from hades_lya folder" << std::endl;
       	using namespace std;
        using boost::format;
        Console& cons = Console::instance();
        long originalSize = survey.NumberQSO();
        
        long N0 = static_cast<SLong&>(state["N0"]);
        long N1 = static_cast<SLong&>(state["N1"]);
        long N2 = static_cast<SLong&>(state["N2"]);
		
		bool warningDefault = false;
        
        boost::multi_array<BinsSpectraStruct, 1> QSO;

        H5::H5File fg(fname, H5F_ACC_RDONLY) ;

    	CosmoTool::hdf5_read_array(fg, "QSO", QSO);
    
    	boost::multi_array<LOSContainer, 1> proj;
		proj.resize(boost::extents[QSO.shape()[0]]);
        
        typename LymanAlphaSurvey::QSOType qso;
        typename LymanAlphaSurvey::LOSType los;
        
        RandomGen *rgen = state.get<RandomGen>("random_generator");
        
        //int step = N0 / pow(double(QSO.size()),0.5);
        int ix=0, iy=0;
        int l;
    	for(int i=0; i<QSO.size(); i++)
    	{
    	    qso.id = QSO[i].id;
    	    qso.theta = QSO[i].theta;
    	    qso.phi = QSO[i].phi;
    	    qso.z = QSO[i].z; 
    	    
    		survey.addLOS(proj[i]);
		    survey.addQSO(qso);

		    CosmoTool::hdf5_read_array(fg, str(boost::format("flux_%d") % i),survey.getProjection()[i].flux);
			    
		    l =survey.getProjection()[i].flux.size();
		    survey.getProjection()[i].dlos.resize(boost::extents[l]);
		    survey.getProjection()[i].z.resize(boost::extents[l]);
		    survey.getProjection()[i].voxel_id.resize(boost::extents[l][3]);
		    
		    ix = (N0-2 -2) * rgen->get().uniform() + 2;
		    iy = (N1-2 -2) * rgen->get().uniform() + 2;
			    
		    for (int ii=0; ii<l; ii++){
			    survey.getProjection()[i].voxel_id[ii][0] = int(ix);
			    survey.getProjection()[i].voxel_id[ii][1] = int(iy); 
			    survey.getProjection()[i].voxel_id[ii][2] = int(ii+4);
		    }
			    
			    
		    //iy += step;
		    //if (iy>N2){
			//    iy = 0;
			//    ix += step;
		    //}
			    
			
	}
		
        cons.print<LOG_STD>(format("Got %d los") % QSO.size());
       
   }
} 

#endif
