/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/samplers/rgen/density_sampler.hpp
    Copyright (C) 2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_SAMPLERS_DENSITY_SAMPLER_HPP
#define __LIBLSS_SAMPLERS_DENSITY_SAMPLER_HPP

namespace LibLSS {

  class GenericDensitySampler: public MarkovSampler {
  public:
      virtual void generateMockData(MarkovState& state) = 0;
  };

}

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019
