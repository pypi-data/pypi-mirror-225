/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/borg_qlpt_rsd.hpp
    Copyright (C) 2020 Natalia Porqueres <n.porqueres@imperial.ac.uk>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_BORG_QLPT_RSD_HPP
#  define __LIBLSS_BORG_QLPT_RSD_HPP

#  include "libLSS/mpi/generic_mpi.hpp"
#  include "libLSS/tools/array_tools.hpp"
#  include "libLSS/tools/auto_interpolator.hpp"
#  include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#  include "libLSS/mcmc/state_element.hpp"
#  include "libLSS/mcmc/global_state.hpp"
#  include "libLSS/physics/forwards/borg_helpers.hpp"
#  include "libLSS/physics/forward_model.hpp"
#  include "libLSS/physics/modified_ngp.hpp"
#  include "libLSS/tools/uninitialized_type.hpp"
#  include "libLSS/tools/mpi_fftw_helper.hpp"
#  include "libLSS/physics/forwards/particle_balancer/particle_distribute.hpp"
#  include <boost/lambda/lambda.hpp>
#  include <CosmoTool/hdf5_array.hpp>
#  include "libLSS/physics/forwards/registry.hpp"

namespace LibLSS {

  class BorgQLptRsdModel : virtual public BORGForwardModel {
  protected:
    // Import member variables
    bool do_rsd;
    double a_init;

    typedef boost::multi_array<size_t, 1> IdxArray;
    typedef UninitializedArray<PhaseArray> U_PArray;
    typedef UninitializedArray<DFT_Manager::ArrayReal, DFT_Manager::AllocReal>
        U_ArrayReal;

    std::shared_ptr<U_PArray> u_pos, u_vel, lc_timing, u_s_pos, u_pos_ag,
        u_vel_ag;
    std::unique_ptr<IdxArray> lagrangian_id;
    std::unique_ptr<U_ArrayReal> potential;

    U_CArray_p AUX1_m, AUX0_m, c_tmp_complex_field_m, c_deltao_m;
    U_Array_p c_tmp_real_field_m, aux_m;
    long c_N0, c_N1, c_N2, c_localN0, c_N2_HC, c_startN0, c_N2real;
    DFT_Manager *mgr;
    int ss_factor;
    double af;
    double partFactor;
    bool lctime;
    double lcboost;
    BalanceInfo realInfo, redshiftInfo;
    bool firstTime;
    bool adjointRequired;
    double hbar;
    double D0, D1, Df1, f1;

    ModelInputAdjoint<3> hold_in_gradient;

    CArray *c_tmp_complex_field, *AUX1_p, *AUX0_p;
    CArray *c_deltao;
    Array *c_tmp_real_field;
    Array *aux_p;

    DFT_Manager::Calls::plan_type c_analysis_plan, c_synthesis_plan, plan;

    ///forward model qlpt_rsd
    void test();
    void qlpt_rsd_ic(CArrayRef &deltao, PhaseArrayRef &lctim);
    void qlpt_rsd_redshift_pos(PhaseArrayRef &pos, PhaseArrayRef &lctim);
    void qlpt_rsd_density_obs(ArrayRef &deltao, size_t numParts);
    void qlpt_rsd_fwd_model(CArrayRef &deltao, PhaseArrayRef &lctim);
    void forwardModel_rsd_field(ArrayRef &deltaf, double *vobs_ext);

    ///adjoint model qlpt_rsd
    void qlpt_rsd_fwd_model_ag(PhaseArrayRef &lctime, ArrayRef &in_ag, ArrayRef &out_ag);

    CosmologicalParameters oldParams;
    void preallocate();
    void updateCosmo() override;

  public:
    typedef PhaseArrayRef &ParticleArray;
    typedef PhaseArrayRef &VelocityArray;

    BorgQLptRsdModel(
        MPI_Communication *comm, BoxModel const &box, BoxModel const &box_out,
        double hbar, bool rsd, int ss_factor, double p_factor, double ai,
        double af, bool light_cone, double light_cone_boost = 1.0);
    virtual ~BorgQLptRsdModel();

    //virtual void forwardModelSimple(ModelInput<3> &delta_init);
    //virtual void forwardModel(
    //    ModelInput<3> &delta_init, ModelInput<3> &delta_output, bool adjointNext);
    //virtual void adjointModel(ModelInput<3> &gradient_delta);

    void forwardModel_v2(ModelInput<3> delta_init) override;
    void adjointModel_v2(ModelInputAdjoint<3> gradient_delta) override;
    void getDensityFinal(ModelOutput<3> delta_output) override;
    void getAdjointModelOutput(ModelOutputAdjoint<3> ag_delta_output) override;

    void clearAdjointGradient() override;
    void setAdjointRequired(bool on) override { adjointRequired = on; }

    void releaseParticles() override {}

    void forwardModelRsdField(ArrayRef &deltaf, double *vobs_ext) override;

    void test_qlpt_rsd_velocities(MarkovState &state);
  };

}; // namespace LibLSS

LIBLSS_REGISTER_FORWARD_DECL(QLPT_RSD);

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Natalia Porqueres
// ARES TAG: email(0) = n.porqueres@imperial.ac.uk
// ARES TAG: year(0) = 2020
