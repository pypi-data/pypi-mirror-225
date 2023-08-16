/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/ares/ares_bias.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_ARES_BIAS_HPP
#define __LIBLSS_ARES_BIAS_HPP

#include "libLSS/tools/console.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include <boost/format.hpp>

namespace LibLSS {
  namespace ARES {
    inline double& extract_bias(MarkovState& state, int c)
    {
      using boost::format;
      return (*state.get<ArrayType1d>(format("galaxy_bias_%d") % c)->array)[0];
    }
    
    template<typename InitializerArray>
    void ensure_bias_size(MarkovState& state, unsigned int c, const InitializerArray& init_a)
    {
      using boost::format;
      auto& a = (*state.get<ArrayType1d>(format("galaxy_bias_%d") % c)->array);
      size_t old_sz = a.size();
      if (old_sz < init_a.size()) {
        a.resize(boost::extents[init_a.size()]);
        for (size_t i = old_sz; i < init_a.size(); i++)
	  a[i] = init_a[i];	
      }
    }

  }
}

#endif
