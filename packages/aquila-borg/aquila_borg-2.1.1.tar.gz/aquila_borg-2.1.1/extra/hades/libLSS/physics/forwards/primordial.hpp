/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/forwards/primordial.hpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HADES_FORWARD_PRIMORDIAL_HPP
#  define __LIBLSS_HADES_FORWARD_PRIMORDIAL_HPP
#  pragma once

#  include "libLSS/physics/forward_model.hpp"
#  include "libLSS/tools/fusewrapper.hpp"
#  include "libLSS/tools/errors.hpp"
#  include "libLSS/physics/forwards/registry.hpp"

namespace LibLSS {

  /**
   * This class handles the colouring of a white noise field with a cosmological
   * power spectrum. It is best to provide a fourier and use the returned fourier
   * field with the v2 interface. Otherwise extra FFT will be called to
   * to match to v1 interface.
   */
  class ForwardPrimordial : public BORGForwardModel {
  public:
    typedef IArrayType::ArrayType IArrayRef;
    typedef ArrayType1d::ArrayType Array1dRef;
    using BORGForwardModel::ArrayRef;

  protected:
    CosmologicalParameters old_cosmo_params;
    double af, D_init;
    LibLSS::multi_array<int, 3> powerSpectrumKeys;
    LibLSS::multi_array<double, 1> powerSpectrum;
    LibLSS::multi_array<double, 1> keyTranslate;

    ModelInput<3> hold_input;
    ModelInputAdjoint<3> hold_ag_input;
    bool lazyInit;
    bool invalid;
    bool accumulateAg;

  public:
    /**
     * Constructor.
     */
    explicit ForwardPrimordial(
        MPI_Communication *comm, const BoxModel &box, double af_);

    PreferredIO getPreferredInput() const override { return PREFERRED_FOURIER; }
    PreferredIO getPreferredOutput() const override {
      return PREFERRED_FOURIER;
    }

    auto getPowerSpectrumArray();

    void accumulateAdjoint(bool accumulate) override {
      accumulateAg = accumulate;
    }

    void forwardModel_v2(ModelInput<3> delta_init) override;

    void getDensityFinal(ModelOutput<3> delta_output) override;

    void updateCosmo() override;

    void adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta) override;

    void clearAdjointGradient() override;

    void
    getAdjointModelOutput(ModelOutputAdjoint<3> out_gradient_delta) override;

    void forwardModelRsdField(ArrayRef &, double *) override;

    void releaseParticles() override;

    bool densityInvalidated() const override;
  }; // namespace LibLSS

} // namespace LibLSS

LIBLSS_REGISTER_FORWARD_DECL(PRIMORDIAL);

#endif
// ARES TAG: num_authors = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: name(1) = Jens Jasche
// ARES TAG: year(1) = 2020
// ARES TAG: email(1) = jens.jasche@fysik.su.se
