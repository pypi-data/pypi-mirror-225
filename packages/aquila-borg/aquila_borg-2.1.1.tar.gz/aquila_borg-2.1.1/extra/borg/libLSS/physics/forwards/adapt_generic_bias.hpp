/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/adapt_generic_bias.hpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_HADES_FORWARD_BIAS_GENERIC_HPP
#  define __LIBLSS_HADES_FORWARD_BIAS_GENERIC_HPP

#  include "libLSS/physics/forward_model.hpp"
#  include "libLSS/tools/fusewrapper.hpp"
#  include "libLSS/tools/errors.hpp"
#  include "libLSS/physics/forwards/registry.hpp"
#  include "libLSS/physics/likelihoods/base.hpp"
#  include "libLSS/tools/static_init.hpp"
#  include "libLSS/tools/static_auto.hpp"

namespace LibLSS {

  /**
   * This class handles the convolution of a real field by some Fourier kernel.
   */
  template <typename T>
  class ForwardGenericBias : public BORGForwardModel {
  public:
    using BORGForwardModel::CArrayRef;
    typedef T bias_t;

  protected:
    ModelInput<3> hold_input;
    ModelInputAdjoint<3> hold_ag_input;

    bool bias_cleaned;
    std::shared_ptr<bias_t> bias;
    bool invalidDensity;
    bool biasSet;

    LibLSS::multi_array<double, 1> currentBiasParams;

    std::shared_ptr<BORGForwardModel> dummyModel;

    void commonSetup();

    void rebuildBias(std::shared_ptr<LikelihoodInfo> info = std::shared_ptr<LikelihoodInfo>());

  public:
    /**
     * Constructor.
     */
    explicit ForwardGenericBias(
        MPI_Communication *comm, const BoxModel &box, const BoxModel &box2)
        : BORGForwardModel(comm, box, box2), bias_cleaned(true),
          invalidDensity(true), biasSet(false) {
      commonSetup();
    }

    /**
     * Constructor.
     */
    explicit ForwardGenericBias(MPI_Communication *comm, const BoxModel &box)
        : BORGForwardModel(comm, box), bias_cleaned(true),
          invalidDensity(true), biasSet(false) {
      commonSetup();
    }

    virtual ~ForwardGenericBias();

    // Difficult to guess directly at the moment. However the classical default for bias
    // is to handle data in REAL representation.

    PreferredIO getPreferredInput() const override { return PREFERRED_REAL; }
    PreferredIO getPreferredOutput() const override { return PREFERRED_REAL; }

    void forwardModel_v2(ModelInput<3> delta_init) override;
    void getDensityFinal(ModelOutput<3> delta_output) override;

    void adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta) override;
    void
    getAdjointModelOutput(ModelOutputAdjoint<3> out_gradient_delta) override;

    void releaseParticles() override {}

    void setModelParams(ModelDictionnary const &params) override;
    boost::any getModelParam(std::string const& n, std::string const& param) override;

    bool densityInvalidated() const override { return invalidDensity; }
  }; // namespace LibLSS

} // namespace LibLSS

AUTO_REGISTRATOR_DECL(ForwardGenericBias);

#endif

// ARES TAG: num_authors = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
