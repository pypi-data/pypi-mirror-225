/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/align_helper.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_ALIGN_HELPER_HPP
#define __LIBLSS_ALIGN_HELPER_HPP

#include <Eigen/Core>

namespace LibLSS {

    template<typename T>
    struct DetectAlignment { enum { Align = Eigen::Unaligned }; };


};

#endif