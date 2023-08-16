/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/deprecated/borg_pm.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_BORG_PM_HPP
#define __LIBLSS_BORG_PM_HPP

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
#include "libLSS/tools/array_tools.hpp"

namespace LibLSS {

  class BorgPMTypes {
  public:
    typedef boost::multi_array<double, 2> TimingArray;
    typedef boost::multi_array<double, 3> TapeArray;
    typedef boost::multi_array<long, 2> IdxTapeArray;
    typedef boost::multi_array_ref<double, 3> TapeArrayRef;
    typedef boost::multi_array_ref<long, 2> IdxTapeArrayRef;
    typedef boost::multi_array<double, 1> SinArray;
    typedef boost::multi_array<long, 2> TapeTransferArray;
    typedef boost::multi_array<size_t, 1> IdxArray;

    constexpr static const double unit_r0 = 1.0; // Units of distances = 1 Mpc/h
    constexpr static const double H0 = 100.0;    // h km/s/Mpc
    constexpr static const double unit_t0 = 1 / H0; // Units of time
    constexpr static const double unit_v0 =
        unit_r0 / unit_t0; // Units of velocity
  };

  template <
      typename FinalInCell = ClassicCloudInCell<double>,
      typename CIC = ClassicCloudInCell<double>>
  class BorgPMModel : virtual public ParticleBasedForwardModel,
                      public BorgPMTypes {
  protected:
    typedef typename LibLSS::array::EigenMap<ArrayRef> EMap;
    typedef UninitializedArray<PhaseArray> U_PhaseArray;
    typedef UninitializedArray<TapeArray> U_TapeArray;
    typedef UninitializedArray<IdxTapeArray> U_IdxTapeArray;

    TimingArray *timing;
    U_TapeArray *u_pos, *u_vel;
    U_IdxTapeArray *u_idx;
    std::unique_ptr<IdxArray> lagrangian_id;

    TapeTransferArray numTransferStep, numReceiveStep, offsetSendStep,
        offsetReceiveStep;
    boost::multi_array<size_t, 1> local_usedParticles;
    SinArray sin2K[3];

    U_CArray_p AUX1_m, AUX0_m, c_tmp_complex_field_m;

    CArray *AUX1_p, *AUX0_p, *lo_AUX0_p, *f_AUX0_p;
    CArray *c_deltao;
    long c_N0, c_N1, c_N2, c_localN0, c_N2_HC, c_startN0, c_N2real;
    long f_N0, f_N1, f_N2, f_localN0, f_N2_HC, f_startN0;
    long f_startN1, f_localN1;
    Array *aux_p;
    std::unique_ptr<DFT_Manager> mgr, force_mgr;
    int ss_factor, f_factor, pm_nsteps;
    double part_factor;
    bool do_redshift;
    double z_start;
    double ai, af;

    CArray *c_tmp_complex_field;
    Array *c_tmp_real_field;

    DFT_Manager::Calls::plan_type c_analysis_plan, c_synthesis_plan;
    DFT_Manager::Calls::plan_type f_analysis_plan, f_synthesis_plan;

    void pm_fwd_model(
        CArrayRef &deltao, TapeArrayRef &pos, TapeArrayRef &vel,
        IdxTapeArrayRef &part_idx, TimingArray &timing);
    void pm_fwd_model_ag(
        PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, IdxTapeArrayRef &part_idx,
        ArrayRef &DPSI, TimingArray &timing);
    void pm_gen_timesteps(double ai, double af, TimingArray &timing, int nstep);

  protected:
    // =====================================================
    // IC generation
    void pm_ic(
        CArrayRef &deltao, TapeArrayRef &pos, TapeArrayRef &vel,
        IdxTapeArrayRef &part_idx, TimingArray &timing);
    void
    pm_ic_ag(PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, TimingArray &timing);

    // =====================================================
    // Redshift space folding and its AG
    template <typename PositionArray, typename RedshiftPosition>
    void pm_redshift_pos(
        const PositionArray &pos, const PositionArray &vel,
        RedshiftPosition &s_pos, size_t numParticles);
    template <typename PositionArray, typename PosAgArray>
    void pm_redshift_pos_ag(
        const PositionArray &pos, const PositionArray &vel, PosAgArray &pos_ag,
        PosAgArray &vel_ag, size_t partNum);

    // =====================================================
    // Density project and its AG

    template <typename PositionArray>
    void pm_density_obs(const PositionArray &pos, ArrayRef &deltao);
    template <typename PositionArray, typename OutputArray>
    void pm_density_obs_ag(
        const PositionArray &pos, OutputArray &pos_ag, OutputArray &vel_ag,
        ArrayRef &B, size_t partNum);

    // =====================================================
    // Special Force AG

    template <typename PositionArray>
    void pm_force_0_ag(
        const PositionArray &pos, const PositionArray &vel,
        PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, PhaseArrayRef &F_ag,
        double dtr, double dtv, size_t agNum);
    template <typename PositionArray>
    void pm_force_1_ag(
        const PositionArray &pos, const PositionArray &vel,
        PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, PhaseArrayRef &F_ag,
        double dtr, double dtv, size_t agNum);

    // =====================================================
    // Update position and its AG

    void pm_pos_update(
        TapeArrayRef &pos, TapeArrayRef &vel, IdxTapeArrayRef &part_idx,
        double dtr, int istep);
    template <typename ForceArray>
    void pm_pos_update_ag(
        PhaseArrayRef &pos_ag, const ForceArray &F_ag, double dtr,
        size_t agNum);

    // =====================================================
    // This is the main stepping routine and its AG.
    void pm_stepping(
        int nstep, TimingArray &timing, TapeArrayRef &pos, TapeArrayRef &vel,
        IdxTapeArrayRef &part_idx);

    void pm_stepping_ag(
        int nstep, TimingArray &timing, TapeArrayRef &pos, TapeArrayRef &vel,
        PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag,
        IdxTapeArrayRef &part_idx);

    // =====================================================
    // These routines are in charge of force over MPI.
    template <int axis, bool accum, int sign, typename PotentialArray>
    void codelet_force(
        int i, FFTW_Real_Array_ref &g, PotentialArray &pot_plus,
        PotentialArray &pot_minus);

    template <int axis, bool accum, int sign>
    void compute_force(FFTW_Real_Array_ref &g, FFTW_Real_Array_ref &pot);

    // =====================================================
    // This the velocity update step and its AG
    template <typename TapePos, typename TapeVel, typename Grav>
    void codelet_vel_update(
        int axis, int istep, double dtv, int i_g_plus, TapePos &pos,
        TapeVel &vel, Grav &g_plus, Grav &g);

    void pm_vel_update(
        TapeArrayRef &pos, TapeArrayRef &vel, IdxTapeArrayRef &part_idx,
        double dtv, int istep);
    void pm_vel_update_ag(
        PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, double dtr, size_t agNum);

    // =====================================================
    // Gravitational potential computation
    template <typename PositionArray>
    void pm_grav_density(
        bool clear, const PositionArray &pos, size_t partNum,
        FFTW_Real_Array_ref &pot);

    void pm_gravpot(FFTW_Real_Array_ref &pot);
    template <typename PositionArray>
    void pm_gravpot_ag(const PositionArray &pos, FFTW_Real_Array &pot);

    // =====================================================
    // These are pure I/O routines to exchange data over MPI.
    template <bool doVel, typename Projector = CIC>
    void pm_distribute_particles(
        std::unique_ptr<DFT_Manager> &dmgr, int istep, TapeArrayRef &pos,
        TapeArrayRef &vel, IdxTapeArrayRef &part_idx, size_t inParts);

    template <bool doVel>
    void pm_distribute_particles_ag(
        int istep, PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag,
        TapeArrayRef &pos, TapeArrayRef &vel, IdxTapeArrayRef &part_idx);

    template <bool accum, typename PlaneArray>
    void pm_exchange_planes(
        PlaneArray &density, std::unique_ptr<DFT_Manager> &d_mgr,
        int extra_planes = CIC::MPI_PLANE_LEAKAGE);

    template <typename OutPlaneArray, typename InPlaneArray>
    void pm_exchange_planes_ag(
        OutPlaneArray &loc_density, InPlaneArray &global_density,
        std::unique_ptr<DFT_Manager> &d_mgr);
    // =====================================================

    void alloc_arrays();
    void tabulate_sin();

  public:
    typedef TapeArray::reference ParticleArray;
    typedef TapeArray::reference VelocityArray;

    BorgPMModel(
        MPI_Communication *comm, const BoxModel &box, int ss_factor,
        int f_factor, int nsteps, double part_factor, bool do_rsd, double ai,
        double af, double z_start);
    virtual ~BorgPMModel();

    virtual void forwardModelSimple(CArrayRef &delta_init);
    virtual void forwardModel(
        CArrayRef &delta_init, ArrayRef &delta_output, bool adjointNext);
    virtual void adjointModel(ArrayRef &gradient_delta);
    virtual void adjointModelParticles(
        PhaseArrayRef &grad_pos, PhaseArrayRef &grad_vel,
        ArrayRef &gradient_delta);

    virtual size_t getNumberOfParticles() const {
      return local_usedParticles[pm_nsteps - 1];
    }
    virtual unsigned int getSupersamplingRate() const { return ss_factor; }

    virtual IdSubArray getLagrangianIdentifiers() const {
      boost::multi_array_types::index_gen i_gen;
      typedef boost::multi_array_types::index_range range;
      int last_step = pm_nsteps - 1;
      auto idx_parts = i_gen[range(0, local_usedParticles[last_step])];

      return (*lagrangian_id)[idx_parts];
    }

    virtual PhaseSubArray getParticlePositions() {
      boost::multi_array_types::index_gen i_gen;
      typedef boost::multi_array_types::index_range range;

      int last_step = pm_nsteps - 1;
      auto idx_parts =
          i_gen[last_step][range(0, local_usedParticles[last_step])][range()];

      return u_pos->get_array()[idx_parts];
    }

    virtual PhaseSubArray getParticleVelocities() {
      boost::multi_array_types::index_gen i_gen;
      typedef boost::multi_array_types::index_range range;

      int last_step = pm_nsteps - 1;
      auto idx_parts =
          i_gen[last_step][range(0, local_usedParticles[last_step])][range()];

      return u_vel->get_array()[idx_parts];
    }

    virtual double getVelocityMultiplier() { return unit_v0 / af; }

    template <typename ArrayOut>
    void copyParticlePositions(ArrayOut &a, int pmstep = -1) const {
      typedef TapeArray::index_range i_range;
      typename TapeArray::index_gen i_gen;
      // We do not care about rsd.
      int last_step = (pmstep < 0) ? pm_nsteps - 1 : pmstep;
      auto idx_parts =
          i_gen[last_step][i_range(0, local_usedParticles[last_step])]
               [i_range()];

      LibLSS::copy_array(a, u_pos->get_array()[idx_parts]);
    }

    template <typename ArrayOut>
    void copyParticleVelocities(ArrayOut &a, int pmstep = -1) const {
      typedef TapeArray::index_range i_range;
      typename TapeArray::index_gen i_gen;
      // We do not care about rsd.
      int last_step = pmstep < 0 ? (pm_nsteps - 1) : pmstep;
      auto idx_parts =
          i_gen[last_step][i_range(0, local_usedParticles[last_step])]
               [i_range()];

      double facRSD = unit_v0 / af;

      LibLSS::copy_array(
          a, b_fused<double>(
                 u_vel->get_array()[idx_parts], boost::lambda::_1 * facRSD));
    }

    virtual void releaseParticles() {
      if (u_pos != 0) {
        delete u_idx;
        delete timing;
        delete u_pos;
        delete u_vel;
        lagrangian_id.reset();
        u_pos = 0;
        u_vel = 0;
      }
      lagrangian_id.reset();
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
