/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/allocator_policy.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_ALLOCATOR_POLICY_HPP
#define __LIBLSS_ALLOCATOR_POLICY_HPP

namespace LibLSS {

    struct DefaultAllocationPolicy {
		static long getIncrement() { return 1024; }
        //static long getIncrement() { return ( 1024 * 1024 ); }
    };

};

#endif
