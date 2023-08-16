/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/hermitic.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHYSICS_HERMITIC_HPP
#  define __LIBLSS_PHYSICS_HERMITIC_HPP

#  include "libLSS/tools/errors.hpp"
#  include "libLSS/physics/forward_model.hpp"
#  include "libLSS/physics/forwards/registry.hpp"
#  include "libLSS/tools/fusewrapper.hpp"
#  include "libLSS/tools/hermiticity_fixup.hpp"

namespace LibLSS {

  class ForwardHermiticOperation : public BORGForwardModel {
  protected:
    Hermiticity_fixer<double, 3> fixer;
    ModelInput<3> hold_input;
    ModelInputAdjoint<3> hold_ag_input;

  public:
    explicit ForwardHermiticOperation(
        MPI_Communication *comm, const BoxModel &box)
        : BORGForwardModel(comm, box), fixer(lo_mgr) {}

    virtual PreferredIO getPreferredInput() const { return PREFERRED_FOURIER; }
    virtual PreferredIO getPreferredOutput() const { return PREFERRED_FOURIER; }

    virtual void forwardModel_v2(ModelInput<3> input) {
      input.setRequestedIO(PREFERRED_FOURIER);
      hold_input = std::move(input);
    }

    virtual void getDensityFinal(ModelOutput<3> output) {
      LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
      output.setRequestedIO(PREFERRED_FOURIER);
      fwrap(output.getFourierOutput()) = fwrap(hold_input.getFourierConst());
      fixer.forward(output.getFourierOutput());
    }

    virtual void clearAdjointGradient() {
      hold_input.clear();
      hold_ag_input.clear();
    }

    virtual void adjointModel_v2(ModelInputAdjoint<3> ag_input) {
      ag_input.setRequestedIO(PREFERRED_FOURIER);
      hold_ag_input = std::move(ag_input);
    }

    virtual void getAdjointModelOutput(ModelOutputAdjoint<3> ag_output) {
      LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
      ag_output.setRequestedIO(PREFERRED_FOURIER);
      fwrap(ag_output.getFourierOutput()) = hold_ag_input.getFourierConst();
      fixer.adjoint(ag_output.getFourierOutput());
    }
  };

} // namespace LibLSS

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2014-2020
