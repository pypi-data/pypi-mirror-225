/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/forwards/upgrade.hpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_HADES_FORWARD_UPGRAADE_HPP
#  define __LIBLSS_HADES_FORWARD_UPGRADE_HPP

#  include "libLSS/physics/forward_model.hpp"
#  include "libLSS/tools/fusewrapper.hpp"
#  include "libLSS/tools/errors.hpp"
#  include "libLSS/physics/forwards/registry.hpp"
#  include "libLSS/tools/mpi/ghost_planes.hpp"

namespace LibLSS {

  /**
   * @brief Upgrade forward model element
   * 
   * It pads the fourier representation of the input field with zeros, treating Nyquist plane correctly.
   */
  class ForwardUpgrade : public BORGForwardModel {
  protected:
    ModelInput<3> hold_input;
    ModelInputAdjoint<3> hold_adjoint;

    GhostPlanes<std::complex<double>, 2> ghosts;

  public:
    ForwardUpgrade(
        MPI_Communication *comm, BoxModel const &box, unsigned int multiply);

    PreferredIO getPreferredInput() const override { return PREFERRED_FOURIER; }
    PreferredIO getPreferredOutput() const override {
      return PREFERRED_FOURIER;
    }

    bool densityInvalidated() const override { return false; }
      
    void forwardModel_v2(ModelInput<3> delta_init) override;
    void getDensityFinal(ModelOutput<3> delta_output) override;

    void adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta) override;

    void
    getAdjointModelOutput(ModelOutputAdjoint<3> out_gradient_delta) override;
  };
} // namespace LibLSS

LIBLSS_REGISTER_FORWARD_DECL(Upgrade);

// ARES TAG: num_authors = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: name(1) = Jens Jasche
// ARES TAG: year(1) = 2020
// ARES TAG: email(1) = jens.jasche@fysik.su.se

#endif