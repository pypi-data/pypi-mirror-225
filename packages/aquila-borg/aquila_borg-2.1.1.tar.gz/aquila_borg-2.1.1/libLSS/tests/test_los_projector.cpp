/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_los_projector.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include "libLSS/physics/projector.hpp"

using namespace LibLSS;

int main()
{
	// number of pixels
	double N[3] = {10,10,10};
	// size pixels
	double dl[3]={2,2,2};
	//lower left corner
	double min[3]={-1,-1,-1};
	//observer position
	double origin[3]={0,0,0};
	// shooting direction (normalized)
	double pointing[3]={1./sqrt(2.),1./sqrt(2.),0};
	//double pointing[3]={1./2.,sqrt(3.)/2.,0};
	//double pointing[3]={1.,0.,0.};
	//double pointing[3]={1./sqrt(3.),1./sqrt(3.),1./sqrt(3.)};
		
	LOSContainer data;
	ray_tracer(origin, pointing, min, dl, N, data);
	
	std::cout << "L:" << N[0]*dl[0] << "," << N[1]*dl[1] << "," << N[2]*dl[2] << std::endl;
	std::cout << "corner:" << min[0] << "," << min[1] << "," << min[2] << std::endl;
	std::cout << "origin:" << origin[0] << "," << origin[1] << "," << origin[2] << std::endl;
	std::cout << "direction:" << pointing[0] << "," << pointing[1] << "," << pointing[2] << std::endl;
	std::cout << "voxel_id, los:" << std::endl;
	for(int i=0; i<10; i++) 
	{
		std::cout << data.voxel_id[i][0] << data.voxel_id[i][1] << data.voxel_id[i][2] << " , " << data.dlos[i] << std::endl;
	}
	
	return 0;
}
