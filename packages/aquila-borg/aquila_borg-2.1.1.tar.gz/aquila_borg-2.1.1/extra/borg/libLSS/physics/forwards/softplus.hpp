/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/softplus.hpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HADES_FORWARD_SOFTPLUS_HPP
#  define __LIBLSS_HADES_FORWARD_SOFTPLUS_HPP
#  pragma once

#  include "libLSS/physics/forward_model.hpp"
#  include "libLSS/tools/fusewrapper.hpp"
#  include "libLSS/tools/errors.hpp"
#  include "libLSS/physics/forwards/registry.hpp"

namespace LibLSS {

  /**
   * This class handles the convolution of a real field by some Fourier kernel.
   */
  class ForwardSoftPlus : public BORGForwardModel {
  public:
    using BORGForwardModel::CArrayRef;

  protected:
    double hardness;
    double bias_value;

    ModelInput<3> hold_input;
    ModelInputAdjoint<3> hold_ag_input;

  public:
    /**
     * Constructor.
     */
    explicit ForwardSoftPlus(MPI_Communication *comm, const BoxModel &box)
        : BORGForwardModel(comm, box), hardness(1.0), bias_value(1.0) {
      ensureInputEqualOutput();
    }

    virtual PreferredIO getPreferredInput() const { return PREFERRED_REAL; }
    virtual PreferredIO getPreferredOutput() const { return PREFERRED_REAL; }

    virtual void forwardModel_v2(ModelInput<3> delta_init);
    virtual void getDensityFinal(ModelOutput<3> delta_output);

    void setBiasValue(double b); 
    void setHardness(double h);

    virtual void adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta);
    virtual void
    getAdjointModelOutput(ModelOutputAdjoint<3> out_gradient_delta);

    virtual void forwardModelRsdField(ArrayRef &, double *) {}

    virtual void releaseParticles() {}
  }; // namespace LibLSS

} // namespace LibLSS

LIBLSS_REGISTER_FORWARD_DECL(Softplus);

#endif

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
