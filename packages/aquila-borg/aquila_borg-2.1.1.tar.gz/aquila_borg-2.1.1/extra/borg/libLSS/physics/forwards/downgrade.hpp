/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/downgrade.hpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HADES_FORWARD_DOWNGRADE_HPP
#  define __LIBLSS_HADES_FORWARD_DOWNGRADE_HPP
#  pragma once

#  include "libLSS/physics/forward_model.hpp"
#  include "libLSS/tools/fusewrapper.hpp"
#  include "libLSS/tools/errors.hpp"
#  include "libLSS/physics/forwards/registry.hpp"
#  include "libLSS/physics/bias/level_combinator.hpp"

namespace LibLSS {

  /**
   * This class handles the convolution of a real field by some Fourier kernel.
   */
  class ForwardDowngrade : public BORGForwardModel {

  protected:
    ModelInput<3> hold_input;

    typedef Combinator::Levels<double, 1, 1> Level_t;

    std::shared_ptr<DFT_Manager::U_ArrayReal> ag_array;

    Level_t level;
    GhostPlanes<double, 2> ghosts;

  public:
    /**
     * Constructor.
     */
    explicit ForwardDowngrade(MPI_Communication *comm, const BoxModel &box);

    PreferredIO getPreferredInput() const override { return PREFERRED_REAL; }
    PreferredIO getPreferredOutput() const override { return PREFERRED_REAL; }

    bool densityInvalidated() const override { return false; }
      
    void forwardModel_v2(ModelInput<3> delta_init) override;
    void getDensityFinal(ModelOutput<3> delta_output) override;

    void adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta) override;
    void
    getAdjointModelOutput(ModelOutputAdjoint<3> out_gradient_delta) override;

    void forwardModelRsdField(ArrayRef &, double *) override {}

    void releaseParticles() override {}
  }; // namespace LibLSS

} // namespace LibLSS

LIBLSS_REGISTER_FORWARD_DECL(Downgrade);

#endif

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
