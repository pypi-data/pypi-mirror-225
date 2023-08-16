/*+
    ARES/HADES/BORG Package -- ./libLSS/data/postools.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_POSTOOLS_HPP
#define __LIBLSS_POSTOOLS_HPP

#include <cmath>

namespace LibLSS {

    template<typename T, typename Array>
    void loadPosition(T x, T y, T z, Array& xyz) {
        xyz[0] = x;
        xyz[1] = y;
        xyz[2] = z;
    }

    template<typename T, typename Array>
    void loadVelocity(T vx, T vy, T vz, Array& vxyz) {
		vxyz[0] = vx;
		vxyz[1] = vy;
		vxyz[2] = vz;
    }

     //template<typename T, typename Array>
    //void ComputeRedshiftSpacePosition(Array& xyz, Array& vxyz) {
    //}

};

#endif
