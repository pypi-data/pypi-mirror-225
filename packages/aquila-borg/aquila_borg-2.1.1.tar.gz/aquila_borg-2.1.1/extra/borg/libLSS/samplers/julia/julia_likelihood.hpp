/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/julia/julia_likelihood.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_SAMPLERS_JULIA_LIKELIHOOD_HPP
#define __LIBLSS_SAMPLERS_JULIA_LIKELIHOOD_HPP

#include <string>
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/tools/mpi/ghost_planes.hpp"
#include "libLSS/tools/string_tools.hpp"
#include "libLSS/tools/defer.hpp"
#include "libLSS/samplers/core/gridLikelihoodBase.hpp"
#include "libLSS/physics/likelihoods/base.hpp"

namespace LibLSS {

  namespace JuliaLikelihood {

    static inline std::string
    likelihood_module_initialize(std::string const &mname) {
      return "Main." + mname + ".initialize";
    }

    static inline std::string
    likelihood_adjoint_gradient(std::string const &mname) {
      return mname + ".adjoint_gradient";
    }

    static inline std::string likelihood_evaluate(std::string const &mname) {
      return mname + ".likelihood";
    }

    static inline std::string
    likelihood_evaluate_bias(std::string const &mname) {
      return mname + ".likelihood_bias";
    }

    static inline std::string
    likelihood_adjoint_bias(std::string const &mname) {
      return mname + ".adjoint_bias";
    }

    static inline std::string mock_data_generate(std::string const &mname) {
      return mname + ".generate_mock_data";
    }

    static inline std::string query_planes(std::string const &mname) {
      return mname + ".get_required_planes";
    }

    static inline std::string ic_generate(std::string const &mname) {
      return mname + ".generate_ic";
    }

    static inline std::string galaxy_bias_name(size_t cat) {
      return "galaxy_bias_" + to_string(cat);
    }

    static inline std::string
    likelihood_set_default_parameters(std::string const &mname) {
      return mname + ".set_default_parameters";
    }
  } // namespace JuliaLikelihood

  class JuliaDensityLikelihood : public GridDensityLikelihoodBase<3> {
  protected:
    typedef GridDensityLikelihoodBase<3> super_t;

    MPI_Communication *comm;
    std::unique_ptr<Mgr::U_ArrayReal> final_density_field;

    ArrayType1d *vobs;
    ArrayType *borg_final_density;

    std::shared_ptr<BORGForwardModel> model;
    std::string module_name;

    GhostPlanes<double, 2> ghosts;
    Defer notify_init;

    double ai, volume;
    std::unique_ptr<Cosmology> cosmology;

    std::vector<std::shared_ptr<ArrayType1d::ArrayType>> bias_params;
    std::vector<std::shared_ptr<ArrayType::ArrayType>> data, sel_field;
    std::vector<double> nmean;
    std::vector<bool> biasRef;
    MarkovState *p_state;

    void common_initialize(MarkovState &state);

    void gradientLikelihood_internal(ModelInput<3> input, ModelOutputAdjoint<3> out_gradient);

  public:
    JuliaDensityLikelihood(
        MPI_Communication *comm, LikelihoodInfo &info,
        const std::string &code_name, const std::string &module_name);
    virtual ~JuliaDensityLikelihood();

    Defer &getPendingInit() { return notify_init; }

    double
    logLikelihood_internal(ModelInput<3> input, bool gradientIsNext = false);

    virtual double
    logLikelihood(ArrayRef const &parameters, bool gradientIsNext = false);
    virtual void gradientLikelihood(
        ArrayRef const &parameters, ArrayRef &gradient_parameters,
        bool accumulate, double scaling);

    virtual double
    logLikelihood(CArrayRef const &parameters, bool gradientIsNext = false);
    virtual void gradientLikelihood(
        CArrayRef const &parameters, CArrayRef &gradient_parameters,
        bool accumulate, double scaling);
    virtual void initializeLikelihood(MarkovState &state);
    virtual void updateMetaParameters(MarkovState &state);
    virtual void setupDefaultParameters(MarkovState &state, int catalog);
    virtual void updateCosmology(CosmologicalParameters const &params);
    virtual void commitAuxiliaryFields(MarkovState &state);
    virtual void
    generateMockData(CArrayRef const &parameters, MarkovState &state);

    void generateInitialConditions(MarkovState &state);
  };

} // namespace LibLSS

#endif
