/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/ref_tools.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef _LIBLSS_TOOLS_REF_TOOLS_HPP
#define _LIBLSS_TOOLS_REF_TOOLS_HPP

namespace LibLSS {

  // This utility struct is used to remove rvalue references and use copy instead.
  // We cannot allow ourselves to store references to temporary objects, only stable
  // objects.
  template<typename T> struct strip_rvalue_ref {
    typedef T type;
  };

  template<typename T> struct strip_rvalue_ref<T&&> {
    typedef T type;
  };

}

#endif
