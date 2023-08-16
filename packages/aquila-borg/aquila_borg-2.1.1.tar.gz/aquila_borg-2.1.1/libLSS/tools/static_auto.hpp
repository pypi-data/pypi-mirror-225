/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/static_auto.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_STATIC_AUTO_HPP
#define __LIBLSS_STATIC_AUTO_HPP

#define AUTO_CLASS_NAME(N) RegistratorHelper_##N

#define AUTO_REGISTRATOR_DECL(N) \
namespace LibLSS { \
  namespace StaticInitDummy { \
      struct AUTO_CLASS_NAME(N) { \
         AUTO_CLASS_NAME(N)(); \
      }; \
      \
      static AUTO_CLASS_NAME(N) helper_## N; \
  } \
}

#define AUTO_REGISTRATOR_IMPL(N) LibLSS::StaticInitDummy::AUTO_CLASS_NAME(N)::AUTO_CLASS_NAME(N)() {}


#endif