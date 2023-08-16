/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/samplers/core/simpleLikelihood.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __HADES_SIMPLE_LIKELIHOOD_HPP
#  define __HADES_SIMPLE_LIKELIHOOD_HPP

#  include "libLSS/physics/likelihoods/base.hpp"
#  include "libLSS/samplers/core/types_samplers.hpp"
#  include "libLSS/samplers/core/likelihood.hpp"

namespace LibLSS {

  /**
   * @brief Likelihood that has a simple structure, parallelization wise. 
   * 
   * It assumes that all nodes are going to obtain the same copy of the parameters
   * and produce something collectively that may depend on other parameters that
   * are local to the MPI nodes. For single task node, the difference to the GridDensityLikelihoodBase
   * is only the shape of the parameter space. However for parallel jobs it can be
   * become very different.
   * 
   * We note that the proposed_params arguments are unnamed, thus the behaviour will heavily
   * depend on the semantic of those parameters. Some synchronization of the behaviour may
   * be required with the user of such a likelihood. 
   */
  class SimpleLikelihood : virtual public LikelihoodBase {
  public:
    SimpleLikelihood(LikelihoodInfo const &info);
    virtual ~SimpleLikelihood();

    /**
     * @brief Compute the log likelihood assuming the proposed parameters.
     * 
     * @param global_params     a global parameter state that is not changing with the current transition kernel
     * @param proposed_params   the set of parameters that are provided to get a new evaluation of the likelihood
     * @return double    the result
     */
    virtual double logLikelihoodSimple(
        ParameterSpace const &global_params,
        LibLSS::const_multi_array_ref<double, 1> const &proposed_params) = 0;

    /**
     * @brief Compute the gradient of the log-likelihood w.r.t to the proposed_params
     * 
     * @param global_params      a global parameter state that is not changing with the current transition kernel
     * @param proposed_params    the set of parameters that are provided to get a new evaluation of the likelihood
     * @param gradient           the gradient w.r.t proposed_params
     */
    virtual void gradientLikelihoodSimple(
        ParameterSpace const &global_params,
        LibLSS::const_multi_array_ref<double, 1> const &proposed_params,
        LibLSS::multi_array_ref<double, 1> &gradient) = 0;

    /**
     * @brief Returns the number of dimensions required by this likelihood.
     * 
     * Note: as SimpleLikelihood is global. That number must be the same on all
     * MPI nodes.
     * 
     * @return unsigned int 
     */
    virtual unsigned int numDimensions() const = 0;
  };

} // namespace LibLSS

#endif
