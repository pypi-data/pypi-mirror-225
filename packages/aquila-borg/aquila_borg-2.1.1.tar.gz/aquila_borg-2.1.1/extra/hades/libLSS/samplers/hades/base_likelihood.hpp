/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/samplers/hades/base_likelihood.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HADES_BASE_LIKELIHOOD_HPP
#define __LIBLSS_HADES_BASE_LIKELIHOOD_HPP

#include "libLSS/cconfig.h"
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/tools/fftw_allocator.hpp"
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/core/gridLikelihoodBase.hpp"
#include "libLSS/samplers/core/likelihood.hpp"
#include "libLSS/samplers/core/simpleLikelihood.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/physics/likelihoods/base.hpp"

namespace LibLSS {

  /**
   * This is a base class for simple bias models. It inherits both from forward model based likelihood
   * and simple likelihood as two kind of gradients will be produced. The ForwardModelBasedLikelihood produces
   * gradients w.r.t the density field, whereas the SimpleLikelihood produces gradients w.r.t to the bias parameters.
   */
  class HadesBaseDensityLikelihood : public ForwardModelBasedLikelihood,
                                     public SimpleLikelihood {
  public:
    //typedef GridDensityLikelihoodBase<3> super_t;
    typedef ForwardModelBasedLikelihood super_t;

  protected:
    GridLengths corners;
    ArrayType1d *vobs;
    ArrayType *borg_final_density;

    std::shared_ptr<BORGForwardModel> model;

    std::unique_ptr<Cosmology> cosmology;
    std::shared_ptr<Mgr::U_ArrayReal> final_density_field;
    double ai;
    double volume;

    boost::multi_array<double, 1> nmean;
    std::vector<std::shared_ptr<ArrayType::ArrayType>> data, sel_field;

    typedef ArrayType1d::ArrayType BiasArray;
    std::vector<std::unique_ptr<BiasArray>> bias;
    std::vector<bool> biasRef;
    size_t numBiasParams;

    void gradientLikelihood_internal(
        ModelInput<3> parameters, ModelOutputAdjoint<3> gradient_parameters);

  public:
    HadesBaseDensityLikelihood(LikelihoodInfo &info, size_t numBiasParams);
    virtual ~HadesBaseDensityLikelihood();

    void
    generateMockData(CArrayRef const &parameters, MarkovState &state) override;

    std::shared_ptr<BORGForwardModel> getForwardModel() override {
      return model;
    }

    void initializeLikelihood(MarkovState &state) override;
    void updateMetaParameters(MarkovState &state) override;
    void updateCosmology(CosmologicalParameters const &params) override;
    void updateBiasParameters(int catalog, BiasArray const &params);
    void updateNmean(int catalog, double nmean);
    void commitAuxiliaryFields(MarkovState &state) override;

    /**
     * This is for computing a log likelihood with a provided dark matter density field
     */
    virtual double logLikelihoodSpecific(ArrayRef const &density) = 0;

    /**
     * This is for computing a gradient log likelihood with a provided dark matter density field.
     * The output gradient must be stored in "grad_density".
     */
    virtual void gradientLikelihoodSpecific(
        ArrayRef const &density, ArrayRef &grad_density) = 0;

    virtual void
    generateMockSpecific(ArrayRef const &density, MarkovState &state) = 0;

    /*
     * This computes the opposite of the log likelihood. If gradientIsnext is
     * true the model has to prepare itself for a gradientLikelihood call.
     * Otherwise it can free temporary memory used to compute the forward model.
     * This variant takes the image in real space representation. The input is
     * preserved as indicated by the const.
     */
    double logLikelihood(
        ArrayRef const &parameters, bool gradientIsNext = false) override;

    /*
     * This is the gradient of the opposite of the log likelihood. It
     * returns the gradient in real space representation.
     * You must have called logLikelihood with gradientIsNext=true first.
     * If accumulate is set to true, the gradient will be summed with existing values.
     * 'scaling' indicates by how much the gradient must be scaled before accumulation.
     */
    void gradientLikelihood(
        ArrayRef const &parameters, ArrayRef &gradient_parameters,
        bool accumulate, double scaling) override;

    /*
     * This is the opposite of log likelihood, Fourier representation. The same
     * rules applies as for the real space variant. The modes must be
     * in unit of Volume as per the continuous Fourier transform.
     */
    double logLikelihood(
        CArrayRef const &parameters, bool gradientIsNext = false) override;

    /*
     * This is the gradient of the logarithm of the opposite of the log
     * likelihood (Fourier representation variant).
     * The same rules applies as for the real space variant.
     */
    void gradientLikelihood(
        CArrayRef const &parameters, CArrayRef &gradient_parameters,
        bool accumulate, double scaling) override;

    double logLikelihoodSimple(
        ParameterSpace const &global,
        LibLSS::const_multi_array_ref<double, 1> const &params) override;

    void gradientLikelihoodSimple(
        ParameterSpace const &global,
        LibLSS::const_multi_array_ref<double, 1> const &params,
        LibLSS::multi_array_ref<double, 1> &gradient) override;

    unsigned int numDimensions() const override;
  };

  class HadesMetaSampler : public MarkovSampler {
  protected:
    typedef std::shared_ptr<HadesBaseDensityLikelihood> likelihood_t;
    int Ncat;
    MPI_Communication *comm;
    likelihood_t likelihood;

  public:
    HadesMetaSampler(MPI_Communication *comm_, likelihood_t likelihood_)
        : comm(comm_), likelihood(likelihood_) {}
    virtual ~HadesMetaSampler() {}

    void initialize(MarkovState &state) override;
    void restore(MarkovState &state) override;
    void sample(MarkovState &state) override;
  };

}; // namespace LibLSS

#endif
