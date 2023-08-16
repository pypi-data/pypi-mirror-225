/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/transfer.hpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HADES_FORWARD_TRANSFER_HPP
#  define __LIBLSS_HADES_FORWARD_TRANSFER_HPP
#  pragma once

#  include "libLSS/physics/forward_model.hpp"
#  include "libLSS/tools/fusewrapper.hpp"
#  include "libLSS/tools/errors.hpp"
#  include "libLSS/physics/forwards/registry.hpp"

namespace LibLSS {

  /**
   * This class handles the convolution of a real field by some Fourier kernel.
   */
  class ForwardTransfer : public BORGForwardModel {
  public:
    using BORGForwardModel::CArrayRef;

  protected:
    std::shared_ptr<DFT_Manager::U_ArrayFourier> Tk;

    ModelInput<3> hold_input;
    ModelInputAdjoint<3> hold_ag_input;

  public:
    /**
     * Constructor.
     */
    explicit ForwardTransfer(
        MPI_Communication *comm, const BoxModel &box)
        : BORGForwardModel(comm, box) {
      ensureInputEqualOutput();
    }

    PreferredIO getPreferredInput() const override { return PREFERRED_FOURIER; }
    PreferredIO getPreferredOutput() const override { return PREFERRED_FOURIER; }

    bool densityInvalidated() const override { return false; }
      
    void forwardModel_v2(ModelInput<3> delta_init) override;
    void getDensityFinal(ModelOutput<3> delta_output) override;

    /**
     * Set the transfer function, it is copied inside the
     * object such that the initial array can be discarded.
     *
     * @param Tk 3d transfer function
     */
    void setTransfer(std::shared_ptr<DFT_Manager::U_ArrayFourier> Tk_);

    void setupInverseCIC(double smoother);
    void setupSharpKcut(double cut, bool reversed = false);

    void adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta) override;
    void
    getAdjointModelOutput(ModelOutputAdjoint<3> out_gradient_delta) override;

    void forwardModelRsdField(ArrayRef &, double *) override {}

    void releaseParticles() override {}
  }; // namespace LibLSS

} // namespace LibLSS

LIBLSS_REGISTER_FORWARD_DECL(Transfer);

#endif

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
