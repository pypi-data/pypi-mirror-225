/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/borg_2lpt.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_BORG_2LPT_HPP
#define __LIBLSS_BORG_2LPT_HPP

#include "libLSS/tools/array_tools.hpp"
#include "libLSS/tools/auto_interpolator.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/mcmc/state_element.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/physics/forwards/borg_helpers.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/physics/classic_cic.hpp"
#include "libLSS/tools/uninitialized_type.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/physics/forwards/particle_balancer/particle_distribute.hpp"
#include <boost/lambda/lambda.hpp>
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/physics/forwards/registry.hpp"

namespace LibLSS {

  template <typename CIC = ClassicCloudInCell<double>>
  class Borg2LPTModel : virtual public ParticleBasedForwardModel {
  protected:
    // Import member variables
    bool do_rsd;
    double a_init;
    double af;
    typedef Uninit_FFTW_Complex_Array U_F_Array;
    typedef Uninit_FFTW_Real_Array U_R_Array;
    typedef Uninit_FFTW_Real_Array::array_type U_ArrayRef;

    typedef boost::multi_array<size_t, 1> IdxArray;
    typedef UninitializedArray<PhaseArray> U_PArray;

    std::shared_ptr<U_PArray> u_pos, u_vel, lc_timing, u_s_pos, u_pos_ag,
        u_vel_ag;
    std::unique_ptr<IdxArray> lagrangian_id;

    CIC cic;
    long c_N0, c_N1, c_N2, c_localN0, c_N2_HC, c_startN0, c_N2real;
    U_R_Array::array_type *aux_p, *c_tmp_real_field;
    U_F_Array::array_type *AUX1_p, *AUX0_p, *c_deltao, *c_tmp_complex_field;
    DFT_Manager *mgr;
    int ss_factor;
    double partFactor;
    bool lctime;
    BalanceInfo realInfo, redshiftInfo;

    U_R_Array *c_tmp_real_field_m, *aux_m;
    U_F_Array *c_tmp_complex_field_m, *AUX1_m, *AUX0_m, *c_deltao_m;

    U_R_Array *u_r_psi_00, *u_r_psi_01, *u_r_psi_02, *u_r_psi_11, *u_r_psi_12,
        *u_r_psi_22;
    U_F_Array *u_c_psi_00, *u_c_psi_01, *u_c_psi_02, *u_c_psi_11, *u_c_psi_12,
        *u_c_psi_22;

    U_R_Array::array_type *r_psi_00, *r_psi_01, *r_psi_02, *r_psi_11, *r_psi_12,
        *r_psi_22;
    U_F_Array::array_type *c_psi_00, *c_psi_01, *c_psi_02, *c_psi_11, *c_psi_12,
        *c_psi_22;

    DFT_Manager::Calls::plan_type c_analysis_plan, c_synthesis_plan;

    // forward model lpt2
    void lpt2_ic(
        CArrayRef &deltao, PhaseArrayRef &pos, PhaseArrayRef &vel,
        PhaseArrayRef &lctim);
    void lpt2_redshift_pos(
        PhaseArrayRef &pos, PhaseArrayRef &vel, PhaseArrayRef &s_pos,
        PhaseArrayRef &lctim);
    void
    lpt2_density_obs(PhaseArrayRef &pos, ArrayRef &deltao, size_t numParts);
    void lpt2_fwd_model(
        CArrayRef &deltao, PhaseArrayRef &pos, PhaseArrayRef &vel,
        PhaseArrayRef &lctim);
    void forwardModel_rsd_field(ArrayRef &deltaf, double *vobs_ext);
    void gen_light_cone_timing(PhaseArrayRef &lctim);

    // adjoint model lpt2
    void lpt2_ic_ag(
        PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, PhaseArrayRef &lctim);
    template <typename... A>
    void lpt2_add_to_derivative(
        U_F_Array::array_type &result, const PhaseArrayRef &pos_ag,
        const PhaseArrayRef &vel_ag, const PhaseArrayRef &lctim,
        const int axis0, std::tuple<A...> const &t);
    void lpt2_redshift_pos_ag(
        PhaseArrayRef &pos, PhaseArrayRef &vel, PhaseArrayRef &pos_ag,
        PhaseArrayRef &vel_ag, PhaseArrayRef &lctim);

    template <typename PositionArray>
    void lpt2_density_obs_ag(
        PositionArray &pos, PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag,
        ArrayRef &B, size_t numParts);
    void lpt2_fwd_model_ag(
        PhaseArrayRef &pos, PhaseArrayRef &vel, PhaseArrayRef &lctime,
        CArrayRef &DPSI);

    CosmologicalParameters oldParams;
    virtual void updateCosmo();

  public:
    typedef PhaseArrayRef &ParticleArray;
    typedef PhaseArrayRef &VelocityArray;

    Borg2LPTModel(
        MPI_Communication *comm, const BoxModel &box, const BoxModel &box_out,
        bool rsd, int ss_factor, double p_factor, double ai, double af,
        bool light_cone);
    virtual ~Borg2LPTModel();

    virtual void forwardModel_v2(ModelInput<3> delta_init);
    virtual void adjointModel_v2(ModelInputAdjoint<3> gradient_delta);
    virtual void getDensityFinal(ModelOutput<3> delta_output);
    virtual void getAdjointModelOutput(ModelOutputAdjoint<3> ag_delta_output);

    virtual void clearAdjointGradient();

    // This computes the adjoint gradient on the particle positions, velocities
    // Not all models may support this. The default implementation triggers an error.
    virtual void
    adjointModelParticles(PhaseArrayRef &grad_pos, PhaseArrayRef &grad_vel);

    virtual IdSubArray getLagrangianIdentifiers() const {
      boost::multi_array_types::index_gen i_gen;
      typedef boost::multi_array_types::index_range range;
      return (*lagrangian_id)[i_gen[range()]];
    }

    virtual PhaseSubArray getParticlePositions() {
      boost::multi_array_types::index_gen i_gen;
      typedef boost::multi_array_types::index_range range;

      return u_pos->get_array()[i_gen[range()][range()]];
    }

    virtual PhaseSubArray getParticleVelocities() {
      boost::multi_array_types::index_gen i_gen;
      typedef boost::multi_array_types::index_range range;

      return u_vel->get_array()[i_gen[range()][range()]];
    }

    virtual size_t getNumberOfParticles() const {
      return redshiftInfo.localNumParticlesAfter;
    }
    virtual unsigned int getSupersamplingRate() const { return ss_factor; }

    template <typename ArrayOut>
    void copyParticlePositions(ArrayOut &a, int _ = -1) const {
      LibLSS::copy_array(a, u_pos->get_array());
    }

    template <typename ArrayOut>
    void copyParticleVelocities(ArrayOut &a, int _ = -1) const {
      LibLSS::copy_array<ArrayOut>(a, u_vel->get_array());
    }

    virtual void releaseParticles() {
      u_pos.reset();
      u_vel.reset();
      realInfo.clear();
      redshiftInfo.clear();
      lagrangian_id.reset();
    }

    virtual void forwardModelRsdField(ArrayRef &deltaf, double *vobs_ext);

    void test_lpt2_velocities(MarkovState &state);
  };

}; // namespace LibLSS

LIBLSS_REGISTER_FORWARD_DECL(2LPT_CIC);
#ifdef _OPENMP
LIBLSS_REGISTER_FORWARD_DECL(2LPT_CIC_OPENMP);
#endif
LIBLSS_REGISTER_FORWARD_DECL(2LPT_NGP);
LIBLSS_REGISTER_FORWARD_DECL(2LPT_DOUBLE);

#endif
