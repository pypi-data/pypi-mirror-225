/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/borg_lep.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_BORG_LEP_HPP
#define __LIBLSS_BORG_LEP_HPP

#include "libLSS/tools/array_tools.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/mcmc/state_element.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/physics/forwards/borg_helpers.hpp"
#include "libLSS/tools/uninitialized_type.hpp"
#include "libLSS/tools/push_operators.hpp"
#include "libLSS/physics/classic_cic.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/physics/forward_model.hpp"

namespace LibLSS {

  template <typename CIC = ClassicCloudInCell<double>>
  class BorgLEPModel : public BORGForwardModel {
  protected:
    typedef boost::multi_array<double, 2> TimingArray;
    typedef boost::multi_array<double, 3> TapeArray;
    typedef boost::multi_array_ref<double, 3> TapeArrayRef;
    typedef boost::multi_array<double, 1> SinArray;

    typedef typename LibLSS::array::EigenMap<ArrayRef> EMap;
    typedef UninitializedArray<PhaseArray> U_PhaseArray;
    typedef UninitializedArray<TapeArray> U_TapeArray;

    TimingArray *timing;
    U_TapeArray *u_pos, *u_vel;
    SinArray sin2K[3];

    CArray *AUX1_p, *AUX0_p, *lo_AUX0_p, *f_AUX0_p;
    CArray *c_deltao;
    long c_N0, c_N1, c_N2, c_localN0, c_N2_HC, c_startN0, c_N2real;
    long f_N0, f_N1, f_N2, f_localN0, f_N2_HC, f_startN0;
    Array *aux_p;
    DFT_Manager *mgr, *force_mgr;
    int ss_factor, f_factor, lep_nsteps;
    bool do_redshift;
    double z_start;
    double ai;

    CArrayRef *c_tmp_complex_field;
    ArrayRef *c_tmp_real_field;

    Uninit_FFTW_Real_Array *g_lep0;
    Uninit_FFTW_Real_Array *g_lep1;
    Uninit_FFTW_Real_Array *g_lep2;

    DFT_Manager::Calls::plan_type c_analysis_plan, c_synthesis_plan;
    DFT_Manager::Calls::plan_type f_analysis_plan, f_synthesis_plan;

    ///forward model lep
    void lep_ic(
        CArrayRef &deltao, TapeArrayRef &pos, TapeArrayRef &vel,
        TimingArray &timing);
    template <typename PositionArray, typename RedshiftPosition>
    void lep_redshift_pos(
        const PositionArray &pos, const PositionArray &vel,
        RedshiftPosition &s_pos);

    template <typename PositionArray>
    void lep_density_obs(const PositionArray &pos, ArrayRef &deltao);
    void lep_fwd_model(
        CArrayRef &deltao, ArrayRef &deltaf, TapeArrayRef &pos,
        TapeArrayRef &vel, TimingArray &timing);
    template <typename PositionArray>
    void lep_gravpot(const PositionArray &pos, FFTW_Real_Array_ref &pot);
    void lep_vel_update(
        TapeArrayRef &pos, TapeArrayRef &vel, double dtv, double dDv,
        int istep);
    void lep_pos_update(
        TapeArrayRef &pos, TapeArrayRef &vel, double dtr, double dDr,
        int istep);
    void lep_stepping(
        TapeArrayRef &pos, TapeArrayRef &vel, int nstep, TimingArray &timing);
    void
    lep_gen_timesteps(double ai, double af, TimingArray &timing, int nstep);

    //adjoint model lep
    void lep_ic_ag(
        PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, TimingArray &timing);

    template <typename PositionArray, typename PosAgArray>
    void lep_redshift_pos_ag(
        const PositionArray &pos, const PositionArray &vel, PosAgArray &pos_ag,
        PosAgArray &vel_ag);

    template <typename PositionArray, typename OutputArray>
    void lep_density_obs_ag(
        const PositionArray &pos, OutputArray &pos_ag, OutputArray &vel_ag,
        ArrayRef &B);

    template <typename PositionArray>
    void lep_gravpot_ag(const PositionArray &pos, FFTW_Real_Array &pot);
    template <typename PositionArray>
    void lep_force_0_ag(
        const PositionArray &pos, const PositionArray &vel,
        PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, PhaseArrayRef &F_ag,
        double dtr, double dtv);
    template <typename PositionArray>
    void lep_force_1_ag(
        const PositionArray &pos, const PositionArray &vel,
        PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, PhaseArrayRef &F_ag,
        double dtr, double dtv);
    template <typename ForceArray>
    void lep_pos_update_ag(
        PhaseArrayRef &pos_ag, const ForceArray &F_ag, double dtr);
    void
    lep_vel_update_ag(PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, double dtr);
    void lep_stepping_ag(
        TapeArrayRef &pos, TapeArrayRef &vel, PhaseArrayRef &pos_ag,
        PhaseArrayRef &vel_ag, int nstep, TimingArray &timing);
    void lep_fwd_model_ag(
        ArrayRef &B, TapeArrayRef &pos, TapeArrayRef &vel, ArrayRef &DPSI,
        TimingArray &timing);

    template <int axis, bool accum, int sign>
    void compute_force(FFTW_Real_Array_ref &g, FFTW_Real_Array_ref &pot);

    template <int axis, bool accum, int sign>
    void compute_lep_force(FFTW_Real_Array_ref &g, FFTW_Real_Array_ref &pot);

    void alloc_arrays();
    void tabulate_sin();

  public:
    BorgLEPModel(
        MPI_Communication *comm, const BoxModel &box, int ss_factor,
        int f_factor, int nsteps, bool do_rsd, double ai, double z_start);
    virtual ~BorgLEPModel();

    virtual void forwardModel(
        CArrayRef &delta_init, ArrayRef &delta_output, bool adjointNext);
    virtual void adjointModel(ArrayRef &gradient_delta);
    TapeArray::reference getParticlePositions() {
      return u_pos->get_array()[lep_nsteps - 1];
    }
    TapeArray::reference getParticleVelocities() {
      return u_vel->get_array()[lep_nsteps - 1];
    }
    virtual void releaseParticles() {
      if (u_pos != 0) {
        delete u_pos;
        delete u_vel;
        delete timing;
      }
    }

    virtual void forwardModelRsdField(ArrayRef &deltaf, double *vobs_ext);

    virtual void clearAdjointGradient() {}
    virtual void pushAdjointModelParticles(
        PhaseArrayRef &grad_pos, PhaseArrayRef &grad_vel) {
      error_helper<ErrorNotImplemented>(
          "adjointModelParticles is not implemented in this model.");
    }

    virtual void retrieveAdjointGradient(CArrayRef &agDeltaInit) {}
  };

}; // namespace LibLSS

#endif
