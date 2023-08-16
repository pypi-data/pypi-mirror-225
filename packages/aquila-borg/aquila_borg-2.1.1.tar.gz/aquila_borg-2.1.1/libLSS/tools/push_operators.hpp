/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/push_operators.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PUSH_OPERATORS
#define __LIBLSS_PUSH_OPERATORS

namespace LibLSS {

    template<bool accum> 
    struct push_to {
        template<typename T>
        static void apply(T& ref, const T& value);
        
        template<typename T>
        void operator()(T& ref, const T& value) {
            apply(ref, value);
        }        
    };

    template<>
    struct push_to<true> {
        template<typename T>
        static void apply(T& ref, const T& value) {
            ref += value;
        }
    };

    template<>
    struct push_to<false> {
        template<typename T>
        static void apply(T& ref, const T& value) {
            ref = value;
        }
    };

}

#endif
