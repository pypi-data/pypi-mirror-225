#ifndef __LIBLSS_FUNCTION_NAME_HPP
#define __LIBLSS_FUNCTION_NAME_HPP

#include "libLSS/cconfig.h"

#ifdef __LIBLSS_PRETTY_FUNCTION_AVAILABLE
#define LIBLSS_FUNCTION __PRETTY_FUNCTION__
#else
#define LIBLSS_FUNCTION __func__
#endif

#endif

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2018
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
