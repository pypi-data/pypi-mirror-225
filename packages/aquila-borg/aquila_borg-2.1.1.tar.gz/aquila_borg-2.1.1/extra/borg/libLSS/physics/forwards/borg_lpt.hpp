/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/borg_lpt.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_BORG_LPT_HPP
#define __LIBLSS_BORG_LPT_HPP

#include "libLSS/tools/array_tools.hpp"
#include "libLSS/tools/auto_interpolator.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/mcmc/state_element.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/physics/forwards/borg_helpers.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/physics/classic_cic.hpp"
#include "libLSS/physics/modified_ngp.hpp"
#include "libLSS/tools/uninitialized_type.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/physics/forwards/particle_balancer/particle_distribute.hpp"
#include <boost/lambda/lambda.hpp>
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/physics/forwards/registry.hpp"

namespace LibLSS {

  template <typename CIC = ClassicCloudInCell<double>>
  class BorgLptModel : virtual public ParticleBasedForwardModel {
  protected:
    // Import member variables
    bool do_rsd;
    bool invalidCache;
    double a_init;

    typedef boost::multi_array<size_t, 1> IdxArray;
    typedef UninitializedArray<PhaseArray> U_PArray;

    std::shared_ptr<U_PArray> u_pos, u_vel, lc_timing, u_s_pos, u_pos_ag,
        u_vel_ag;
    std::unique_ptr<IdxArray> lagrangian_id;
    U_CArray_p AUX1_m, AUX0_m, c_tmp_complex_field_m, c_deltao_m;
    U_Array_p c_tmp_real_field_m, aux_m;
    CIC cic;
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

    CArray *c_tmp_complex_field, *AUX1_p, *AUX0_p;
    CArray *c_deltao;
    Array *c_tmp_real_field;
    Array *aux_p;

    DFT_Manager::Calls::plan_type c_analysis_plan, c_synthesis_plan;

    ///forward model lpt
    void lpt_ic(
        CArrayRef &deltao, PhaseArrayRef &pos, PhaseArrayRef &vel,
        PhaseArrayRef &lctim);
    void lpt_redshift_pos(
        PhaseArrayRef &pos, PhaseArrayRef &vel, PhaseArrayRef &s_pos,
        PhaseArrayRef &lctim);
    void lpt_density_obs(PhaseArrayRef &pos, ArrayRef &deltao, size_t numParts);
    void lpt_fwd_model(
        CArrayRef &deltao, PhaseArrayRef &pos, PhaseArrayRef &vel,
        PhaseArrayRef &lctim);
    void forwardModel_rsd_field(ArrayRef &deltaf, double *vobs_ext);
    void gen_light_cone_timing(PhaseArrayRef &lctim);

    ///adjoint model lpt
    void lpt_ic_ag(
        PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, PhaseArrayRef &lctim);
    void lpt_redshift_pos_ag(
        PhaseArrayRef &pos, PhaseArrayRef &vel, PhaseArrayRef &pos_ag,
        PhaseArrayRef &vel_ag, PhaseArrayRef &lctim);

    template <typename PositionArray>
    void lpt_density_obs_ag(
        PositionArray &pos, PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag,
        ArrayRef const &B, size_t numParts);
    void lpt_fwd_model_ag(
        PhaseArrayRef &pos, PhaseArrayRef &vel, PhaseArrayRef &lctime,
        CArrayRef &out_ag);

    CosmologicalParameters oldParams;

    void preallocate();
    void updateCosmo() override;

  public:
    typedef PhaseArrayRef &ParticleArray;
    typedef PhaseArrayRef &VelocityArray;

    BorgLptModel(
        MPI_Communication *comm, BoxModel const &box, BoxModel const &box_out,
        bool rsd, int ss_factor, double p_factor, double ai, double af,
        bool light_cone, double light_cone_boost = 1.0);
    virtual ~BorgLptModel();

    bool densityInvalidated() const override;

    void forwardModel_v2(ModelInput<3> delta_init) override;
    void adjointModel_v2(ModelInputAdjoint<3> gradient_delta) override;
    void getDensityFinal(ModelOutput<3> delta_output) override;
    void getAdjointModelOutput(ModelOutputAdjoint<3> ag_delta_output) override;

    void clearAdjointGradient() override;

    void setAdjointRequired(bool on) override { adjointRequired = on; }

    size_t getNumberOfParticles() const override {
      return redshiftInfo.localNumParticlesAfter;
    }
    unsigned int getSupersamplingRate() const override { return ss_factor; }

    PhaseArrayRef const &lightConeTiming() const {
      return lc_timing->get_array();
    }

    PhaseSubArray getParticlePositions() override {
      boost::multi_array_types::index_gen i_gen;
      typedef boost::multi_array_types::index_range range;
      if (!u_pos)
        error_helper<ErrorBadState>("Particle array already freed.");

      return u_pos->get_array()[i_gen[range(
          0, redshiftInfo.localNumParticlesAfter)][range()]];
    }

    PhaseSubArray getParticleVelocities() override {
      boost::multi_array_types::index_gen i_gen;
      typedef boost::multi_array_types::index_range range;
      if (!u_vel)
        error_helper<ErrorBadState>("Particle array already freed.");

      return u_vel->get_array()[i_gen[range(
          0, redshiftInfo.localNumParticlesAfter)][range()]];
    }

    template <typename ArrayOut>
    void copyParticlePositions(ArrayOut &a, int _ = -1) const {
      LibLSS::copy_array(a, u_pos->get_array());
    }

    template <typename ArrayOut>
    void copyParticleVelocities(ArrayOut &a, int _ = -1) const {
      LibLSS::copy_array<ArrayOut>(a, u_vel->get_array());
    }

    void releaseParticles() override {
      if (u_pos) {
        u_pos.reset();
        u_vel.reset();
      }
      if (u_s_pos) {
        u_s_pos.reset();
      }
      realInfo.clear();
      redshiftInfo.clear();
      lagrangian_id.reset();
    }

    IdSubArray getLagrangianIdentifiers() const override {
      boost::multi_array_types::index_gen i_gen;
      typedef boost::multi_array_types::index_range range;

      return (
          *lagrangian_id)[i_gen[range(0, redshiftInfo.localNumParticlesAfter)]];
    }

    void adjointModelParticles(
        PhaseArrayRef &grad_pos, PhaseArrayRef &grad_vel) override;

    void forwardModelRsdField(ArrayRef &deltaf, double *vobs_ext) override;

    void test_lpt_velocities(MarkovState &state);
  };

}; // namespace LibLSS
LIBLSS_REGISTER_FORWARD_DECL(LPT_CIC);
#ifdef _OPENMP
LIBLSS_REGISTER_FORWARD_DECL(LPT_CIC_OPENMP);
#endif
LIBLSS_REGISTER_FORWARD_DECL(LPT_NGP);
LIBLSS_REGISTER_FORWARD_DECL(LPT_DOUBLE);

#endif
