/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/fftw_allocator.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/tools/fftw_allocator.hpp"

using LibLSS::FFTW_Allocator;

/*#define TYPE_IMPL(T) template<> FFTW_Allocator<T>::size_type FFTW_Allocator<T>::minAllocSize = 0

TYPE_IMPL(float);
TYPE_IMPL(double);
*/