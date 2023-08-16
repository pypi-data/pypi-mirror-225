/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/hades_log.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HADES_LOG_FORWARD_MODEL_HPP
#define __LIBLSS_HADES_LOG_FORWARD_MODEL_HPP
#pragma once

#include "libLSS/physics/forward_model.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/tools/errors.hpp"
#include "libLSS/physics/forwards/registry.hpp"

namespace LibLSS {

  class HadesLog : public BORGForwardModel {
  protected:
    double ai, D_init;
    double rho_mean, A_mean;
    ModelInputAdjoint<3> hold_in_gradient;
    CosmologicalParameters old_params;
    bool shifted_mean;

  public:
    explicit HadesLog(
        MPI_Communication *comm, const BoxModel &box,
        double ai_, bool shifted_mean_ = true);

    virtual void forwardModelSimple(CArrayRef &delta_init);

    virtual void forwardModel_v2(ModelInput<3> delta_init);

    virtual void getDensityFinal(ModelOutput<3> delta_output);
    virtual void updateCosmo();

    virtual void forwardModelRsdField(ArrayRef &deltaf, double *vobs_ext);

    virtual void adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta);

    virtual void getAdjointModelOutput(ModelOutputAdjoint<3> ag_delta_output);

    virtual void clearAdjointGradient();

    virtual void releaseParticles();
  };

} // namespace LibLSS

LIBLSS_REGISTER_FORWARD_DECL(HADES_LOG);

#endif
