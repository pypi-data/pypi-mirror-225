/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/generic/generic_hmc_likelihood.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_GENERIC_HMC_LIKELIHOOD_HPP
#  define __LIBLSS_GENERIC_HMC_LIKELIHOOD_HPP

#  include <CosmoTool/hdf5_array.hpp>
#  include <CosmoTool/algo.hpp>
#  include <functional>
#  include <list>
#  include <memory>
#  include "libLSS/physics/cosmo.hpp"
#  include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#  include "libLSS/physics/forward_model.hpp"
#  include "libLSS/tools/fused_array.hpp"
#  include <boost/tuple/tuple.hpp>
#  include "libLSS/tools/phoenix_vars.hpp"
#  include <boost/signals2.hpp>
#  include <boost/phoenix/operator.hpp>
#  include <boost/fusion/algorithm/iteration/for_each.hpp>
#  include <boost/fusion/include/for_each.hpp>
#  include <boost/fusion/adapted/boost_tuple.hpp>
#  include <boost/fusion/include/boost_tuple.hpp>
#  include "libLSS/physics/bias/power_law.hpp"
#  include "libLSS/tools/auto_interpolator.hpp"

#  include "libLSS/data/spectro_gals.hpp"
#  include "libLSS/data/linear_selection.hpp"
#  include "libLSS/mcmc/state_element.hpp"
#  include "libLSS/data/galaxies.hpp"
#  include "libLSS/physics/likelihoods/base.hpp"
#  include "libLSS/samplers/core/gridLikelihoodBase.hpp"

namespace LibLSS {

  namespace GenericDetails {
    void compute_forward(
        std::shared_ptr<FFTW_Manager<double, 3>> &mgr,
        std::shared_ptr<BORGForwardModel> &model,
        const CosmologicalParameters &cosmoparams, double ai,
        boost::multi_array_ref<double, 1> const &vobs, ModelInput<3> ic,
        ModelOutput<3> out_density, bool adjoint_next);

    static GridDensityLikelihoodBase<3>::GridLengths
    getGridLengths(LikelihoodInfo const &info) {
      GridDensityLikelihoodBase<3>::GridLengths out;
      auto grid_length = Likelihood::query<Likelihood::GridLengths>(
          info, Likelihood::GRID_LENGTH);

      out[0] = grid_length[0];
      out[1] = grid_length[1];
      out[2] = grid_length[2];
      return out;
    }

    static GridDensityLikelihoodBase<3>::GridSizes
    getGridSize(LikelihoodInfo const &info) {
      GridDensityLikelihoodBase<3>::GridSizes out;
      auto mpi_grid =
          Likelihood::query<Likelihood::GridSize>(info, Likelihood::MPI_GRID);

      out[0] = mpi_grid[0];
      out[1] = mpi_grid[1];
      out[2] = mpi_grid[2];
      return out;
    }
  } // namespace GenericDetails

  class AbstractGenericHMCLikelihood : public ForwardModelBasedLikelihood {
  public:

    using ForwardModelBasedLikelihood::ForwardModelBasedLikelihood;

    /**
     * @brief Return the number of bias parameters for this likelihood/bias model.
     */
    virtual int getNumberOfBiasParameters() const = 0;

    /**
     * @brief indicate whether the bias model cares about nmean or if it is part of the bias parameters.
     */
    virtual bool nmeanIsBias() const = 0;

    /**
     * @brief Evaluate the log-likelihood for the specific bias parameters.
     *
     * This call does not invoke the forward model and rely on a previous evaluation to provide the density field
     * to the bias model.
     */
    virtual double logLikelihoodBias(
        int catalog, double nmean,
        boost::multi_array_ref<double, 1> &biases) = 0;
  };

  template <class AbstractBiasType, class VoxelLikelihoodType>
  class GenericHMCLikelihood : public AbstractGenericHMCLikelihood {
  public:
    typedef AbstractBiasType bias_t;
    typedef VoxelLikelihoodType likelihood_t;

  protected:
    typedef boost::multi_array_types::extent_range range;
    typedef AbstractGenericHMCLikelihood super_t;

    double ares_heat;
    double ai, volume;
    double xmin0, xmin1, xmin2;
    ArrayType1d *vobs;
    ArrayType *borg_final_density;

    size_t localNdata[6];

    std::shared_ptr<BORGForwardModel> model;
    std::shared_ptr<bias_t> bias;
    std::shared_ptr<likelihood_t> likelihood;
    LikelihoodInfo info;
    std::shared_ptr<Mgr> mgr;
    std::unique_ptr<Cosmology> cosmology;
    std::unique_ptr<Mgr::U_ArrayReal> final_density_field;

    std::vector<std::shared_ptr<ArrayType1d::ArrayType>> bias_params;
    std::vector<std::shared_ptr<ArrayType::ArrayType>> data, sel_field;
    std::vector<double> nmean;
    std::vector<bool> biasRef;

    void commonInitialize(MarkovState &state);
    auto s_range() const { return mgr->strict_range(); }
    auto s_extents() const { return model->out_mgr->extents_real_strict(); }

  public:
    boost::signals2::signal<void(
        std::shared_ptr<likelihood_t> &, std::shared_ptr<bias_t> &)>
        ready;

    GenericHMCLikelihood(LikelihoodInfo &base_info);

    virtual ~GenericHMCLikelihood() {}

    /**
     * @brief Retrieve the forward model on which this likelihood is based on.
     *
     * @return A shared_ptr on BORGForwardModel.
     */
    std::shared_ptr<BORGForwardModel> getForwardModel() override {
      return model;
    }

    // Thin-wrap for samplers that do not want to see the specificities of the bias
    // model.

    /**
     * @brief Return the number of bias parameters for this likelihood/bias model.
     */
    int getNumberOfBiasParameters() const override { return bias_t::numParams; }

    /**
     * @brief indicate whether the bias model cares about nmean or if it is part of the bias parameters.
     */
    bool nmeanIsBias() const override { return bias_t::NmeanIsBias; }

    /**
     * @brief Evaluate the log-likelihood for the specific bias parameters.
     *
     * This call does not invoke the forward model and rely on a previous evaluation to provide the density field
     * to the bias model.
     */
    double logLikelihoodBias(
        int catalog, double nmean,
        boost::multi_array_ref<double, 1> &biases) override;

    double
    logLikelihood(ArrayRef const &parameters, bool gradientIsNext = false) override;
    void gradientLikelihood(
        ArrayRef const &parameters, ArrayRef &gradient_parameters,
        bool accumulate, double scaling) override;

    double
    logLikelihood(CArrayRef const &parameters, bool gradientIsNext = false) override;
    void gradientLikelihood(
        CArrayRef const &parameters, CArrayRef &gradient_parameters,
        bool accumulate, double scaling) override;

    void gradientLikelihood_internal(
        ModelInput<3> parameters, ModelOutputAdjoint<3> gradient_parameters);

    void initializeLikelihood(MarkovState &state) override;
    void updateMetaParameters(MarkovState &state) override;
    void setupDefaultParameters(MarkovState &state, int catalog) override;
    void updateCosmology(CosmologicalParameters const &params) override;
    void commitAuxiliaryFields(MarkovState &state) override;
    void
    generateMockData(CArrayRef const &parameters, MarkovState &state) override;
  };

  template <typename Likelihood>
  class LikelihoodConnector {
  protected:
    typedef typename Likelihood::likelihood_t likelihood_t;
    typedef typename Likelihood::bias_t bias_t;

    std::shared_ptr<likelihood_t> likelihood;
    std::shared_ptr<bias_t> bias;

    void likelihoodReady(
        std::shared_ptr<likelihood_t> &global_likelihood,
        std::shared_ptr<bias_t> &global_bias) {
      likelihood = global_likelihood;
      bias = global_bias;
    }

  public:
    LikelihoodConnector(std::shared_ptr<Likelihood> &base) {
      // We want to avoid multiple construction of the likelihood and bias object.
      // When base is ready, it will inform us asynchronously.
      base->ready.connect(std::bind(
          &LikelihoodConnector<Likelihood>::likelihoodReady, this,
          std::placeholders::_1, std::placeholders::_2));
    }
  };

  template <typename Likelihood, typename MetaSelector, bool Active = true>
  class GenericMetaSampler;

  template <typename Likelihood, typename MetaSelector>
  class GenericMetaSampler<Likelihood, MetaSelector, true>
      : public MarkovSampler, public LikelihoodConnector<Likelihood> {
  public:
    typedef typename Likelihood::bias_t bias_t;
    typedef typename Likelihood::likelihood_t likelihood_t;

    typedef ArrayType1d::ArrayType BiasParamArray;
    typedef ArrayType::ArrayType SelectionArray;
    typedef ArrayType::ArrayType DensityArray;
    typedef ArrayType::ArrayType DataArray;

    struct CatalogData {
      double &nmean;
      BiasParamArray &bias_params;
      SelectionArray &sel_field;
      DensityArray &matter_density;
      DataArray &data;
    };

    double bound_posterior(double H, double x, CatalogData &catalog);

  protected:
    int Ncat;
    MPI_Communication *comm;
    std::shared_ptr<BORGForwardModel> model;

  public:
    GenericMetaSampler(
        MPI_Communication *comm_, std::shared_ptr<Likelihood> &base)
        : LikelihoodConnector<Likelihood>(base), MarkovSampler(), comm(comm_) {}
    virtual ~GenericMetaSampler() {}

    void initialize(MarkovState &state) override;
    void restore(MarkovState &state) override;
    void sample(MarkovState &state) override;
  };

  template <typename Likelihood, typename MetaSelector>
  class GenericMetaSampler<Likelihood, MetaSelector, false>
      : public MarkovSampler {
  public:
    typedef typename Likelihood::bias_t bias_t;
    typedef typename Likelihood::likelihood_t likelihood_t;

    typedef ArrayType1d::ArrayType BiasParamArray;
    typedef ArrayType::ArrayType SelectionArray;
    typedef ArrayType::ArrayType DensityArray;
    typedef ArrayType::ArrayType DataArray;

    struct CatalogData {
      double &nmean;
      BiasParamArray &bias_params;
      SelectionArray &sel_field;
      DensityArray &matter_density;
      DataArray &data;
    };

    GenericMetaSampler(
        MPI_Communication *comm_, std::shared_ptr<Likelihood> &base)
        : MarkovSampler() {
      Console::instance().print<LOG_INFO_SINGLE>(
          "This bias model discards the use of Nmean");
    }
    virtual ~GenericMetaSampler() {}

    void initialize(MarkovState &state) override {}
    void restore(MarkovState &state) override{}
    void sample(MarkovState &state) override {}
  };

  // This selection nmean for sampling.
  struct NmeanSelector {
    static constexpr double step_advisor = 0.1;

    static inline std::string name() { return "nmean"; }

    template <typename Array>
    static inline void select(double x, double &nmean, Array &biases) {
      nmean = x;
    }

    template <typename Array>
    static inline double get_value(double &nmean, Array &biases) {
      return nmean;
    }
  };

  // This selection p-th parameter for sampling.
  template <size_t p>
  struct BiasParamSelector {

    static constexpr double step_advisor = 0.1;

    static inline std::string name() {
      return boost::str(boost::format("bias %d") % p);
    }

    template <typename Array>
    static inline void select(double x, double &nmean, Array &biases) {
      biases[p] = x;
    }

    template <typename Array>
    static inline auto get_value(double &nmean, Array &biases)
        -> decltype(biases[p]) {
      return biases[p];
    }
  };

  template <typename Likelihood>
  class GenericVobsSampler : public MarkovSampler,
                             public LikelihoodConnector<Likelihood> {
  public:
    typedef typename Likelihood::bias_t bias_t;
    typedef typename Likelihood::likelihood_t likelihood_t;

    typedef ArrayType1d::ArrayType BiasParamArray;
    typedef ArrayType1d::ArrayType VobsArray;
    typedef ArrayType::ArrayType SelectionArray;
    typedef ArrayType::ArrayType DensityArray;
    typedef ArrayType::ArrayType DataArray;

    typedef FFTW_Manager_3d<double> DFT_Manager;

    double bound_posterior(double x, int component, MarkovState &state);

  protected:
    int Ncat;
    MPI_Communication *comm;
    std::shared_ptr<BORGForwardModel> model;
    std::shared_ptr<DFT_Manager> mgr;
    std::shared_ptr<VobsArray> vobs;
    std::unique_ptr<DensityArray> vobs_matter_field;

  public:
    GenericVobsSampler(
        MPI_Communication *comm_, std::shared_ptr<Likelihood> &base)
        : LikelihoodConnector<Likelihood>(base), MarkovSampler(), comm(comm_) {}
    virtual ~GenericVobsSampler();

    void initialize(MarkovState &state) override;
    void restore(MarkovState &state) override;
    void sample(MarkovState &state) override;
  };

  template <typename Likelihood>
  class GenericForegroundSampler : public MarkovSampler,
                                   public LikelihoodConnector<Likelihood> {
  public:
    typedef typename Likelihood::bias_t bias_t;
    typedef typename Likelihood::likelihood_t likelihood_t;

    typedef ArrayType1d::ArrayType BiasParamArray;
    typedef ArrayType::ArrayType SelectionArray;
    typedef ArrayType::ArrayType DataArray;
    typedef ArrayType::ArrayType DensityArray;

    typedef FFTW_Manager_3d<double> DFT_Manager;

    typedef UninitializedArray<DFT_Manager::ArrayReal, DFT_Manager::AllocReal>
        U_ArrayReal;
    typedef U_ArrayReal::array_type ArrayReal;

    typedef decltype(
        ((bias_t *)0)->compute_density(*(DensityArray *)0)) BiasTuple;
    typedef decltype(
        ((bias_t *)0)
            ->selection_adaptor.apply(
                *(DensityArray *)0, *(BiasTuple *)0)) SelectedDensityTuple;
    typedef decltype(
        last_of_tuple<1>(*(SelectedDensityTuple *)0)) TupleResidual;

    double bound_posterior(
        double fgval, double fgvalmin, double fgvalmax, DensityArray &gdata,
        DensityArray &fg_field, ArrayReal &pre_selection_field,
        DensityArray &original_selection, TupleResidual &r_tuple);

    void local_initialize(MarkovState &state);

  protected:
    MPI_Communication *comm;
    std::shared_ptr<BORGForwardModel> model;
    std::shared_ptr<DFT_Manager> mgr;

    std::vector<int> fgmap_list;
    std::vector<double> step_norm, fgvalmax, fgvalmin;
    int catalog;

    size_t N0, N1, N2;

    void foregroundLoaded(MarkovState &state, int fgid);

  public:
    GenericForegroundSampler(
        MPI_Communication *comm_, std::shared_ptr<Likelihood> &base,
        int catalog_)
        : LikelihoodConnector<Likelihood>(base), MarkovSampler(), comm(comm_),
          catalog(catalog_) {}
    virtual ~GenericForegroundSampler();

    void addMap(int fgmap);

    void initialize(MarkovState &state) override;
    void restore(MarkovState &state) override;
    void sample(MarkovState &state) override;
  };

} // namespace LibLSS

#endif
