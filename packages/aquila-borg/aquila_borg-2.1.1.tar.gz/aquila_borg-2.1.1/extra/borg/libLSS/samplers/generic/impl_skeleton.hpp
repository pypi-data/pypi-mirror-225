/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/generic/impl_skeleton.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/cconfig.h"
#include "generic_hmc_likelihood.hpp"

#include "generic_hmc_likelihood_impl.cpp"
#include "libLSS/physics/bias/noop.hpp"

#include "generic_meta_impl.cpp"
#include "generic_vobs_impl.cpp"
#include "generic_foreground_impl.cpp"

#include <boost/preprocessor/repetition/repeat.hpp>
#include <boost/preprocessor/tuple/elem.hpp>

#define LIKE_DECL(T)                                                           \
  LibLSS::GenericHMCLikelihood<                                                \
      BOOST_PP_TUPLE_ELEM(2, 0, T), BOOST_PP_TUPLE_ELEM(2, 1, T)>

#define META_DECL(z, n, T)                                                     \
  template class LibLSS::GenericMetaSampler<                                   \
      LIKE_DECL(T), LibLSS::BiasParamSelector<n>>;

#define FORCE_INSTANCE(BIAS, LIKELIHOOD, NUM_PARAMS)                           \
  template class LIKE_DECL((BIAS, LIKELIHOOD));                                \
  template class LibLSS::GenericMetaSampler<                                   \
      LIKE_DECL((BIAS, LIKELIHOOD)), LibLSS::NmeanSelector>;                   \
  template class LibLSS::GenericVobsSampler<LIKE_DECL((BIAS, LIKELIHOOD))>;    \
  template class LibLSS::GenericForegroundSampler<LIKE_DECL(                   \
      (BIAS, LIKELIHOOD))>;                                                    \
  BOOST_PP_REPEAT(NUM_PARAMS, META_DECL, (BIAS, LIKELIHOOD))
