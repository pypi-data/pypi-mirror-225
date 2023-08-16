/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/samplers/core/splitLikelihood.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_HADES_SPLIT_LIKELIHOOD_HPP
#  define __LIBLSS_HADES_SPLIT_LIKELIHOOD_HPP

#  include "libLSS/samplers/core/likelihood.hpp"
#  include "libLSS/samplers/core/gridLikelihoodBase.hpp"
#  include "libLSS/samplers/core/simpleLikelihood.hpp"
#  include <boost/variant.hpp>
#  include <list>
#  include <memory>
#  include <tuple>

namespace LibLSS {

  /**
   * @brief 
   * 
   */
  class SplitAndReshapeLikelihood : public LikelihoodBase {
  protected:
    typedef boost::variant<
        std::shared_ptr<GridDensityLikelihoodBase<3>>,
        std::shared_ptr<SimpleLikelihood>>
        LikelihoodVariant;

    MPI_Communication *comm;
    std::list<std::tuple<std::string, LikelihoodVariant>> parameterLikelihood;

  public:
    SplitAndReshapeLikelihood(MPI_Communication *comm_);
    ~SplitAndReshapeLikelihood();

    void initializeLikelihood(MarkovState &state) override;
    void updateMetaParameters(MarkovState &state) override;
    void setupDefaultParameters(MarkovState &state, int catalog) override;
    void updateCosmology(CosmologicalParameters const &params) override;
    void commitAuxiliaryFields(MarkovState &state) override;

    /**
     * @brief Add that this parameter must be evaluated with a specific log-likelihood object
     * The parameter needs to exist later in the MarkovState. 
     * 
     * Depending on the likelihood variant, the behaviour will be different:
     *    - GridDensityLikelihoodBase<3> is for likelihoods
     *      that are grid based and thus split over MPI nodes with FFTW slabbing.
     *    - SimpleLikelihoodBase is for likelihoods that have their parameters identical
     *      and replicated on all MPI nodes
     * 
     * @param parameter 
     * @param likelihood
     */
    void addNamedParameter(std::string parameter, LikelihoodVariant likelihood);

    /**
     * @brief Get the total number Of parameters that are resident on the
     * current MPI node. 
     * 
     * The sampler/optimizer will need allocate only this
     * portion.
     * 
     * @return unsigned int
     */
    unsigned int getTotalNumberOfParameters();

    /**
     * @brief Compute the log likelihood using the provided array. 
     * 
     * WARNING!! The parameters provided here depends heavily on the inner structure
     * of the split likelihood parameter space. Some parameters need be replicated over MPI nodes and 
     * some others not.
     * 
     * @param params 
     * @return double 
     */
    double logLikelihood(LibLSS::const_multi_array_ref<double, 1> &params);

    /**
     * @brief Compute the gradient of the log likelihood using the provided array to evaluate it. 
     * 
     * WARNING!! The parameters provided here depends heavily on the inner structure
     * of the split likelihood parameter space. Some parameters need be replicated over MPI nodes and 
     * some others not.
     * 
     * @param params 
     * @return double 
     */
    double gradientLikelihood(
        LibLSS::const_multi_array_ref<double, 1> &params,
        LibLSS::multi_array_ref<double, 1> &gradient_params);
  };

} // namespace LibLSS

#endif