/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/phoenix_vars.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHOENIX_VARS_HPP
#define __LIBLSS_PHOENIX_VARS_HPP

#include <boost/phoenix/core/argument.hpp>

namespace LibLSS {


  namespace PhoenixDetails {
      using boost::phoenix::expression::argument;

      argument<1>::type const _p1 = {};
      argument<2>::type const _p2 = {};
      argument<3>::type const _p3 = {};
      argument<4>::type const _p4 = {};
  }
  
  using PhoenixDetails::_p1;
  using PhoenixDetails::_p2;
  using PhoenixDetails::_p3;
  using PhoenixDetails::_p4;
}

#endif
