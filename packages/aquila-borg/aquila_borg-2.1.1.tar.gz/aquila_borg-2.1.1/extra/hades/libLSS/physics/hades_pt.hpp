/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/hades_pt.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HADES_LINEAR_FORWARD_MODEL_HPP
#define __LIBLSS_HADES_LINEAR_FORWARD_MODEL_HPP

#include "libLSS/physics/forward_model.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/tools/errors.hpp"
#include "libLSS/physics/forwards/registry.hpp"

namespace LibLSS {

  /**
   * This is the example class to implement the linear gravity model (also
   * known as PT model). It only really do two things: a fast fourier transform
   * and a scaling by the linear growth function.
   */
  class HadesLinear : public BORGForwardModel {
  protected:
    double ai, af, D_init;
    PreferredIO currentOutput, lastInput;

  public:
    /**
     * Consruct a new object.
     * @param comm    an MPI communicator
     * @param box     the box describing the input physical grid
     * @param box_out the box describing the output physical grid (at the moment
     *                 box == box_out is required)
     * @param ai       the universe scale factor at which the initial conditions
     *                 are provided.
     */
    explicit HadesLinear(
        MPI_Communication *comm, const BoxModel &box, const BoxModel &box_out,
        double ai_, double af_);

    virtual void forwardModelSimple(CArrayRef &delta_init);

    virtual PreferredIO getPreferredInput() const;
    virtual PreferredIO getPreferredOutput() const;

    virtual void forwardModel_v2(ModelInput<3> delta_init);

    virtual void getDensityFinal(ModelOutput<3> delta_output);

    virtual void updateCosmo();

    virtual void forwardModelRsdField(ArrayRef &deltaf, double *vobs_ext);

    virtual void adjointModel_v2(ModelInputAdjoint<3> ag_delta_input);

    virtual void getAdjointModelOutput(ModelOutputAdjoint<3> ag_delta_output);

    virtual void releaseParticles();
  };

} // namespace LibLSS

LIBLSS_REGISTER_FORWARD_DECL(HADES_PT);

#endif
