/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/powerspectrum/measure.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_POWERSPECTRUM_MEASURE_HPP
#define __LIBLSS_POWERSPECTRUM_MEASURE_HPP

#include <CosmoTool/algo.hpp>
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"

namespace LibLSS {

    namespace PowerSpectrum {

        template<typename CArray>
        void computePower(ArrayType1d::ArrayType& power, const CArray& density, const IArrayType& a_keys, 
                          const IArrayType& a_adjust, const IArrayType1d& a_nmode, double volume, bool clear = true) {
            using CosmoTool::square;
            const IArrayType::ArrayType& keys = *a_keys.array;
            const IArrayType::ArrayType& adjust = *a_adjust.array;
            const IArrayType1d::ArrayType& nmode = *a_nmode.array;
            int begin0 = density.index_bases()[0];
            int begin1 = density.index_bases()[1];
            int begin2 = density.index_bases()[2];
            int end0 = density.index_bases()[0] + density.shape()[0];
            int end1 = density.index_bases()[1] + density.shape()[1];
            int end2 = density.index_bases()[2] + density.shape()[2];

            if (clear)
              std::fill(power.begin(), power.end(), 0);
            for (int i = begin0; i < end0; i++) {
                for (int j = begin1; j < end1; j++) {
                    for (int k = begin2; k < end2; k++) {
                        double P = square(density[i][j][k].real()) + square(density[i][j][k].imag());
                    
                        power[ keys[i][j][k] ] += P * adjust[i][j][k];
                    
                    }
                }
            }
            
            for (int i = 0; i < power.num_elements(); i++)
               if (nmode[i] != 0)
                 power[i] /= (volume * nmode[i]);
        }

        template<typename F, typename CArray>
        void savePower(F& f, const std::string& n, const CArray& density, const IArrayType& a_keys, 
                          const IArrayType& a_adjust, const IArrayType1d& a_nmode, double volume) {
            ArrayType1d::ArrayType P(boost::extents[a_nmode.array->num_elements()]);
            
            computePower(P, density, a_keys, a_adjust, a_nmode, volume);
            CosmoTool::hdf5_write_array(f, n, P);
        }
    }

};

#endif
