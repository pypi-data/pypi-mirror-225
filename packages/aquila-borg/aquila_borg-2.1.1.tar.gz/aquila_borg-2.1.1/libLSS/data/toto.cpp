/*+
    ARES/HADES/BORG Package -- ./libLSS/data/toto.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <boost/preprocessor/cat.hpp>
#include <boost/preprocessor/seq/for_each.hpp>
#include <boost/preprocessor/stringize.hpp>

#define SEQ (z)(x)(y)(z)

#define MACRO(r, data, elem) BOOST_PP_CAT(BOOST_PP_STRINGIZE(elem), data)

BOOST_PP_SEQ_FOR_EACH(MACRO, _, SEQ) // expands to w_ x_ y_ z_
