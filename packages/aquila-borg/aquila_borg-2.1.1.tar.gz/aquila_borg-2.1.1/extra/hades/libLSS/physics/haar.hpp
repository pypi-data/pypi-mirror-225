/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/haar.hpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_HADES_FORWARD_HAAR_HPP
#  define __LIBLSS_HADES_FORWARD_HAAR_HPP
#  pragma once

#  include "libLSS/physics/forward_model.hpp"
#  include "libLSS/tools/fusewrapper.hpp"
#  include "libLSS/tools/errors.hpp"
#  include "libLSS/physics/forwards/registry.hpp"

namespace LibLSS {

  /**
   * This class handles the convolution of a real field by some Fourier kernel.
   */
  class ForwardHaar : public BORGForwardModel {
  protected:
    bool do_inverse;
    ModelInput<3> hold_input;
    ModelInputAdjoint<3> hold_ag_input;

  public:
    /**
     * Constructor.
     */
    explicit ForwardHaar(
        MPI_Communication *comm, const BoxModel &box, bool inverse = false)
        : BORGForwardModel(comm, box), do_inverse(inverse) {
      if (comm->size() > 1) {
        error_helper<ErrorParams>(
            "MPI is not supported. Comm size must be equal to one.");
      }
      ensureInputEqualOutput();
    }

    virtual PreferredIO getPreferredInput() const { return PREFERRED_REAL; }
    virtual PreferredIO getPreferredOutput() const { return PREFERRED_REAL; }

    virtual void forwardModel_v2(ModelInput<3> delta_init);
    virtual void getDensityFinal(ModelOutput<3> delta_output);

    virtual void adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta);
    virtual void
    getAdjointModelOutput(ModelOutputAdjoint<3> out_gradient_delta);
  }; // namespace LibLSS

} // namespace LibLSS

LIBLSS_REGISTER_FORWARD_DECL(Haar);

#endif

// ARES TAG: num_authors = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
