/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/openmp.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_OPENMP_HPP
#define __LIBLSS_OPENMP_HPP

#ifdef _OPENMP
#include <omp.h>
#endif

namespace LibLSS {

    inline int smp_get_max_threads() {
#ifdef _OPENMP
        return omp_get_max_threads();
#else
        return 1;
#endif
    }
    
    inline int smp_get_thread_id() {
#ifdef _OPENMP
        return omp_get_thread_num();
#else
        return 0;
#endif
    }

    inline int smp_get_num_threads() {
#ifdef _OPENMP
        return omp_get_num_threads();
#else
        return 1;
#endif

    }
    
    inline void smp_set_nested(bool n) {
#ifdef _OPENMP
        omp_set_nested(n ? 1 : 0);
#endif
    }

    
};

#endif
