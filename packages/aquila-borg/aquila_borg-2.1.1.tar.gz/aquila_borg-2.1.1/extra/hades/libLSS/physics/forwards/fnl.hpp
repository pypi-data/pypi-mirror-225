/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/forwards/fnl.hpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HADES_FORWARD_FNL_HPP
#  define __LIBLSS_HADES_FORWARD_FNL_HPP
#  pragma once

#  include "libLSS/physics/forward_model.hpp"
#  include "libLSS/tools/fusewrapper.hpp"
#  include "libLSS/tools/errors.hpp"
#  include "libLSS/physics/forwards/registry.hpp"

namespace LibLSS {

  /**
   * This class handles the addition of an fNL into primordial potential.
   */
  class ForwardFNL : public BORGForwardModel {
  public:
    typedef IArrayType::ArrayType IArrayRef;
    typedef ArrayType1d::ArrayType Array1dRef;
    using BORGForwardModel::ArrayRef;

  protected:
    ModelInput<3> hold_input;
    ModelInputAdjoint<3> hold_ag_input;
    bool lazyInit;

  public:
    /**
     * Constructor.
     */
    explicit ForwardFNL(MPI_Communication *comm, const BoxModel &box);

    virtual PreferredIO getPreferredInput() const { return PREFERRED_REAL; }
    virtual PreferredIO getPreferredOutput() const { return PREFERRED_REAL; }

    virtual void forwardModel_v2(ModelInput<3> delta_init);
    virtual void getDensityFinal(ModelOutput<3> delta_output);
    virtual void adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta);
    virtual void
    getAdjointModelOutput(ModelOutputAdjoint<3> out_gradient_delta);
    virtual void forwardModelRsdField(ArrayRef &, double *);
    virtual void clearAdjointGradient();
    virtual void releaseParticles();
  }; // namespace LibLSS

} // namespace LibLSS

LIBLSS_REGISTER_FORWARD_DECL(PRIMORDIAL_FNL);

#endif
// ARES TAG: num_authors = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: name(1) = Jens Jasche
// ARES TAG: year(1) = 2020
// ARES TAG: email(1) = jens.jasche@fysik.su.se
