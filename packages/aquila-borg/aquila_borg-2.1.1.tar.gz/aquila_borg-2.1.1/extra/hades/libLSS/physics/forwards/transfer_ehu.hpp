/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/forwards/transfer_ehu.hpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HADES_FORWARD_TRANSFER_EHU_HPP
#  define __LIBLSS_HADES_FORWARD_TRANSFER_EHU_HPP
#  pragma once

#  include "libLSS/physics/forward_model.hpp"
#  include "libLSS/tools/fusewrapper.hpp"
#  include "libLSS/tools/errors.hpp"
#  include "libLSS/physics/forwards/registry.hpp"

namespace LibLSS {

  /**
   * @brief Forward model element that applies a Eisensten&Hu transfer function
   * 
   * It assumes that the input is a properly linearly-scaled gravitational potential.
   */
  class ForwardEisensteinHu : public BORGForwardModel {
  public:
    typedef IArrayType::ArrayType IArrayRef;
    typedef ArrayType1d::ArrayType Array1dRef;
    using BORGForwardModel::ArrayRef;

  protected:
    CosmologicalParameters old_cosmo_params;
    LibLSS::multi_array<int, 3> powerSpectrumKeys;
    LibLSS::multi_array<double, 1> powerSpectrum;
    LibLSS::multi_array<double, 1> keyTranslate;

    ModelInput<3> hold_input;
    ModelInputAdjoint<3> hold_ag_input;
    bool lazyInit;

    double sign_k2;

    bool invalid;
    bool accum;

  public:
    /**
     * Constructor.
     */
    explicit ForwardEisensteinHu(MPI_Communication *comm, const BoxModel &box);

    PreferredIO getPreferredInput() const override { return PREFERRED_FOURIER; }
    PreferredIO getPreferredOutput() const override {
      return PREFERRED_FOURIER;
    }

    auto getPowerSpectrumArray();

    void setReverseSign(bool reverse) { sign_k2 = reverse ? -1 : 1; }

    void forwardModel_v2(ModelInput<3> delta_init) override;

    void getDensityFinal(ModelOutput<3> delta_output) override;

    void updateCosmo() override;

    void adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta) override;

    void accumulateAdjoint(bool do_accumulate) override {
      accum = do_accumulate;
    }

    void clearAdjointGradient() override;

    void
    getAdjointModelOutput(ModelOutputAdjoint<3> out_gradient_delta) override;

    void forwardModelRsdField(ArrayRef &, double *) override;

    void releaseParticles() override;

    bool densityInvalidated() const override;
  }; // namespace LibLSS

} // namespace LibLSS

LIBLSS_REGISTER_FORWARD_DECL(TRANSFER_EHU);

#endif
// ARES TAG: num_authors = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: name(1) = Jens Jasche
// ARES TAG: year(1) = 2020
// ARES TAG: email(1) = jens.jasche@fysik.su.se
