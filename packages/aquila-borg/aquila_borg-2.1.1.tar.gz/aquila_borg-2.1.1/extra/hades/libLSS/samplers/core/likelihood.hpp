/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/samplers/core/likelihood.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_CORE_LIKELIHOOD_BASE_HPP
#  define __LIBLSS_CORE_LIKELIHOOD_BASE_HPP

#  include "libLSS/physics/cosmo.hpp"
#  include "libLSS/mcmc/global_state.hpp"
#  include "libLSS/mcmc/state_element.hpp"

namespace LibLSS {

  /**
   * @brief A type to provide name parameter space mapping to the state element in the MarkovChain
   * 
   */
  typedef std::map<std::string, std::shared_ptr<StateElement>> ParameterSpace;

  /**
   * @brief This is the fundamental likelihood class. 
   * 
   * It does not express log likelihood evaluation but provides entry points to initialize, obtain
   * cosmology and manipulate a MarkovState. 
   * 
   */
  class LikelihoodBase {
  public:
    LikelihoodBase() = default;
    virtual ~LikelihoodBase() {}

    virtual void initializeLikelihood(MarkovState &state) = 0;
    virtual void updateMetaParameters(MarkovState &state) = 0;
    virtual void setupDefaultParameters(MarkovState &state, int catalog) = 0;
    virtual void updateCosmology(CosmologicalParameters const &params) = 0;
    virtual void commitAuxiliaryFields(MarkovState &state) = 0;
  };

} // namespace LibLSS

#endif
