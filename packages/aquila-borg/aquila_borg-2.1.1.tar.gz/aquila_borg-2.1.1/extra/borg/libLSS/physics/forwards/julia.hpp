/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/julia.hpp
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHYSICS_JULIA_HPP
#define __LIBLSS_PHYSICS_JULIA_HPP

#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/julia/julia.hpp"

namespace LibLSS {

  namespace Julia {
    Object make_simulation_box(const BoxModel &box);
  }

  class JuliaForward : public BORGForwardModel {
  protected:
    std::string module_name;
    Julia::Object forward_object;

  public:
    JuliaForward(
        MPI_Communication *comm, const BoxModel &box,
        const std::string &code_name, const std::string &module_name);
    virtual ~JuliaForward();

    virtual void forwardModel_v2(ModelInput<3> delta_init);
    virtual void getDensityFinal(ModelOutput<3> delta_out);
    virtual void adjointModel_v2(ModelInputAdjoint<3> gradient_delta);
    virtual void getAdjointModelOutput(ModelOutputAdjoint<3> gradient_delta);
    virtual void releaseParticles();
    virtual void updateCosmo();
  };
} // namespace LibLSS

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019-2020

