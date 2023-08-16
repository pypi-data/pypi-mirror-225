/*+
    ARES/HADES/BORG Package -- ./libLSS/physics/classic_gpot.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHYSICS_CLASSIC_GPOT_HPP
#define __LIBLSS_PHYSICS_CLASSIC_GPOT_HPP

#include <cmath>
#include "libLSS/tools/console.hpp"
#include <boost/multi_array.hpp>

using namespace LibLSS;
typedef boost::multi_array_types::extent_range range;
using boost::extents;
using boost::format;


namespace LibLSS {

    template<typename T>
    struct ClassicGravitationalPotential {
        typedef T Type;
        typedef boost::multi_array<T, 3> DensityArray;
        typedef boost::multi_array<T, 3> GravityArray;
        
        template<typename PotentialArray>
        static void potential(const PotentialArray& dens, PotentialArray& pot, T Om, T L0, T L1, T L2, 
                               int N0, int N1, int N2) {
            ConsoleContext<LOG_DEBUG> ctx("Classic GravitationalPotential estimation");
            
            //transform density to F-space
            MFCalls::execute_r2c(analysis_plan, dens.data(), AUX0.data());
            
            double normphi=3./2.*Om;

            #pragma omp parallel for
            for (int i=0 ; i<startN0+localN0;i++)
                for (int j=0 ; j<N1;j++)
                    for (int k=0; k<N2_HC;k++)
                    {
                        double kk[3];
                        kk[0]=kmode(i,N0,L0);
                        kk[1]=kmode(j,N1,L1);
                        kk[2]=kmode(k,N2,L2);
                    
                        double sin20 = sin(kk[0]/2.)*sin(kk[0]/2.);
			            double sin21 = sin(kk[1]/2.)*sin(kk[1]/2.);
			            double sin22 = sin(kk[2]/2.)*sin(kk[2]/2.);	

			            double Greens = - normphi/4./(sin20+sin21+sin22);
		  
                        AUX0[i][j][k] *= Greens;                        
	                }
	        //fix zero mode by hand
	        if (startN0 == 0 && localN0 > 0) {
            AUX0[0][0][0]=0;
            }
           
            MFCalls::execute_c2r(synthesis_plan, AUX0.data(), pot.data());            
        }
    };
    
    
}

#endif
