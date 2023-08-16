/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/deprecated/borg_pm.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <CosmoTool/algo.hpp>
#include <Eigen/Core>
#include <boost/array.hpp>
#include <boost/format.hpp>
#include <boost/bind.hpp>
#include <boost/mpl/for_each.hpp>
#include <boost/mpl/range_c.hpp>
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/tools/powerspectrum/measure.hpp"
#include "libLSS/physics/forwards/deprecated/borg_pm.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/borg_splash.hpp"
#include "libLSS/physics/forwards/particle_balancer/attributes.hpp"
#include "libLSS/physics/forwards/particle_balancer/particle_distribute.hpp"

#undef EXPERIMENTAL_ORDERING

using namespace LibLSS;
using namespace LibLSS::BORG_help;
using CosmoTool::square;

static const bool SKIP_MPI_FOR_SINGLE_NODE = true;
static const bool FORCE_REDISTRIBUTE = false;

static inline bool ALWAYS_MPI(MPI_Communication *comm) {
  return (!SKIP_MPI_FOR_SINGLE_NODE || comm->size() > 1);
}

#include "pm/borg_fwd_pm.cpp"
#include "pm/borg_fwd_pm_adj.cpp"

template <typename FIC, typename CIC>
void BorgPMModel<FIC, CIC>::tabulate_sin() {
  sin2K[0].resize(boost::extents[f_N0]);
  sin2K[1].resize(boost::extents[f_N1]);
  sin2K[2].resize(boost::extents[f_N2]);

  for (int i = 0; i < f_N0; i++) {
    sin2K[0][i] = square(sin(M_PI * i / double(f_N0)) * 2 * f_N0 / L0);
  }

  for (int i = 0; i < f_N1; i++) {
    sin2K[1][i] = square(sin(M_PI * i / double(f_N1)) * 2 * f_N1 / L1);
  }

  for (int i = 0; i < f_N2; i++) {
    sin2K[2][i] = square(sin(M_PI * i / double(f_N2)) * 2 * f_N2 / L2);
  }
}

template <typename FIC, typename CIC>
BorgPMModel<FIC, CIC>::BorgPMModel(
    MPI_Communication *comm, const BoxModel &box, int ss_factor, int f_factor,
    int pm_nsteps, double p_factor, bool do_rsd, double ai, double af,
    double z_start)
    : ParticleBasedForwardModel(comm, box) {
  this->ss_factor = ss_factor;
  this->f_factor = f_factor;
  this->pm_nsteps = pm_nsteps;
  this->z_start = z_start;
  this->do_redshift = do_rsd;
  this->ai = ai;
  this->af = af;
  this->part_factor = p_factor;

  u_pos = 0;
  u_vel = 0;

  if (pm_nsteps < 2) {
    error_helper<ErrorParams>(
        "BORG_PM is not defined for less than 2 PM steps.");
  }

  BORG::splash_borg();

  alloc_arrays();
  tabulate_sin();
}

template <typename FIC, typename CIC>
void BorgPMModel<FIC, CIC>::alloc_arrays() {
  using boost::c_storage_order;

  c_N0 = ss_factor * N0;
  c_N1 = ss_factor * N1;
  c_N2 = ss_factor * N2;
  c_N2_HC = c_N2 / 2 + 1;

  f_N0 = f_factor * N0;
  f_N1 = f_factor * N1;
  f_N2 = f_factor * N2;
  f_N2_HC = f_N2 / 2 + 1;

  force_mgr = std::make_unique<DFT_Manager>(f_N0, f_N1, f_N2, comm);
  mgr = std::make_unique<DFT_Manager>(c_N0, c_N1, c_N2, comm);

  // When RSD is activated we need another final step.
  int real_nsteps = pm_nsteps + (do_redshift ? 1 : 0);

  numTransferStep.resize(boost::extents[real_nsteps][comm->size()]);
  numReceiveStep.resize(boost::extents[real_nsteps][comm->size()]);
  offsetReceiveStep.resize(boost::extents[real_nsteps][1 + comm->size()]);
  offsetSendStep.resize(boost::extents[real_nsteps][1 + comm->size()]);
  local_usedParticles.resize(boost::extents[real_nsteps]);

  c_startN0 = mgr->startN0;
  c_localN0 = mgr->localN0;
  f_startN0 = force_mgr->startN0;
  f_localN0 = force_mgr->localN0;
  f_startN1 = force_mgr->startN1;
  f_localN1 = force_mgr->localN1;

  AUX1_p = new CArray(
      mgr->extents_complex(), c_storage_order(), mgr->allocator_complex);
  aux_p =
      new Array(mgr->extents_real(), c_storage_order(), mgr->allocator_real);
  AUX0_p = new CArray(
      mgr->extents_complex(), c_storage_order(), mgr->allocator_complex);
#ifdef ARES_MPI_FFTW
  f_AUX0_p = new CArray(
      force_mgr->extents_complex_transposed(), c_storage_order(),
      force_mgr->allocator_complex);
#else
  f_AUX0_p = new CArray(
      force_mgr->extents_complex(), c_storage_order(),
      force_mgr->allocator_complex);
#endif

  if (ss_factor > 1) {
    c_deltao = new CArray(
        mgr->extents_complex(), c_storage_order(), mgr->allocator_complex);
    c_tmp_real_field =
        new Array(mgr->extents_real(), c_storage_order(), mgr->allocator_real);
    c_tmp_complex_field = new CArray(
        mgr->extents_complex(), c_storage_order(), mgr->allocator_complex);
    lo_AUX0_p = new CArray(
        lo_mgr->extents_complex(), c_storage_order(),
        lo_mgr->allocator_complex);
  } else {
    c_deltao = 0;
    c_tmp_real_field = tmp_real_field;
    c_tmp_complex_field = tmp_complex_field;
    lo_AUX0_p = new CArray(
        lo_mgr->extents_complex(), c_storage_order(),
        lo_mgr->allocator_complex); //AUX0_p;
  }

  Uninit_FFTW_Real_Array f_tmp_p(
      force_mgr->extents_real(), force_mgr->allocator_real);
  Uninit_FFTW_Real_Array::array_type &f_tmp = f_tmp_p.get_array();

  c_synthesis_plan = mgr->create_c2r_plan(AUX1_p->data(), aux_p->data());
  c_analysis_plan = mgr->create_r2c_plan(aux_p->data(), AUX1_p->data());
  f_synthesis_plan =
      force_mgr->create_c2r_plan(f_AUX0_p->data(), f_tmp.data(), true);
  f_analysis_plan =
      force_mgr->create_r2c_plan(f_tmp.data(), f_AUX0_p->data(), true);
}

template <typename FIC, typename CIC>
BorgPMModel<FIC, CIC>::~BorgPMModel() {
  delete AUX0_p;
  delete AUX1_p;
  delete aux_p;
  delete f_AUX0_p;
  delete lo_AUX0_p;

  if (c_deltao != 0) {
    delete c_deltao;
    delete c_tmp_real_field;
    delete c_tmp_complex_field;
  }

  mgr->destroy_plan(c_synthesis_plan);
  mgr->destroy_plan(c_analysis_plan);

  force_mgr->destroy_plan(f_synthesis_plan);
  force_mgr->destroy_plan(f_analysis_plan);
}

template <typename FIC, typename CIC>
void BorgPMModel<FIC, CIC>::forwardModelSimple(CArrayRef &delta_init) {
  ConsoleContext<LOG_DEBUG> ctx("BORG-PM MODEL (particles)");
  int nstep = pm_nsteps;
  int real_nstep = nstep + (do_redshift ? 1 : 0);
  size_t part_number =
      size_t(part_factor * size_t(c_localN0) * size_t(c_N1) * size_t(c_N2));

  if (u_pos != 0)
    delete u_pos;
  if (u_vel != 0)
    delete u_vel;

#ifdef EXPERIMENTAL_ORDERING
  typedef boost::general_storage_order<3> order_type;
  typedef order_type::size_type size_type;
  size_type ordering[] = {0, 2, 1};
  bool ascending[] = {true, true, true};
  order_type order(ordering, ascending);
  u_pos =
      new UninitializedArray<TapeArray>(extents[real_nstep][part_number][3]);
  u_vel = new UninitializedArray<TapeArray>(
      extents[nstep][part_number][3], std::allocator<double>(), order);
#else
  u_pos =
      new UninitializedArray<TapeArray>(extents[real_nstep][part_number][3]);
  u_vel = new UninitializedArray<TapeArray>(extents[nstep][part_number][3]);
#endif
  lagrangian_id = std::unique_ptr<IdxArray>(new IdxArray(extents[part_number]));
  u_idx =
      new UninitializedArray<IdxTapeArray>(extents[real_nstep][part_number]);
  timing = new TimingArray(extents[4][nstep]);

  pm_fwd_model(
      delta_init, u_pos->get_array(), u_vel->get_array(), u_idx->get_array(),
      *timing);
}

template <typename FIC, typename CIC>
void BorgPMModel<FIC, CIC>::forwardModel(
    CArrayRef &delta_init, ArrayRef &delta_output, bool adjointNext) {
  ConsoleContext<LOG_DEBUG> ctx("BORG-PM MODEL");
  int nstep = pm_nsteps;
  int real_nstep = nstep + (do_redshift ? 1 : 0);
  int last_step = nstep - 1;
  TapeArrayRef::index_gen i_gen;
  typedef TapeArrayRef::index_range i_range;
  // Make some alias first

  forwardModelSimple(delta_init);

  auto &pos = u_pos->get_array();
  auto &vel = u_vel->get_array();
  auto &part_idx = u_idx->get_array();

  //build density field
  if (do_redshift) {
    // the RSD is collectively as complex as a full time step.
    // particles are moved then they have to be redistributed to nodes
    // and the density built on each node.
    // of course this has to be undone in the adjoint gradient
    ctx.print("doing redshift space distortions.");
    int s_step = last_step + 1;
    TapeArrayRef::reference s_pos = pos[s_step];
    size_t loc_used = local_usedParticles[last_step];

    // Move particles to their redshift position in the s_pos buffer (actually last entry of pos tape array)
    ctx.print("Produce redshift coordinates");
    pm_redshift_pos(pos[last_step], vel[last_step], s_pos, loc_used);
    // Reinit indexes to 0, 1, ..., loc_used-1
    ctx.print("init indexes");
    initIndexes(part_idx[s_step], loc_used);
    // Domain decomposition, use the FIC distribution criterion
    ctx.print("redistribute");
    pm_distribute_particles<false, FIC>(
        lo_mgr, s_step, pos, vel, part_idx, loc_used);
    // pos[s_step] is now guaranteed to live only in the acceptable domain for delta_output
    ctx.print("project");
    pm_density_obs(
        s_pos[i_gen[i_range(0, local_usedParticles[s_step])][i_range()]],
        delta_output);
  } else {
    auto slice_inds =
        i_gen[i_range(0, local_usedParticles[last_step])][i_range()];
    pm_density_obs(pos[last_step][slice_inds], delta_output);
  }

  if (!forwardModelHold && !adjointNext) {
    releaseParticles();
  }
  forwardModelHold = false;
}

template <typename FIC, typename CIC>
void BorgPMModel<FIC, CIC>::adjointModelParticles(
    PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, ArrayRef &gradient_delta) {
  int nstep = pm_nsteps;

  pm_fwd_model_ag(pos_ag, vel_ag, u_idx->get_array(), gradient_delta, *timing);

  releaseParticles();
}

template <typename FIC, typename CIC>
void BorgPMModel<FIC, CIC>::adjointModel(ArrayRef &gradient_delta) {
  ConsoleContext<LOG_DEBUG> ctx("BORG-PM ADJOINT MODEL main");
  int nstep = pm_nsteps;
  size_t partNumber = size_t(part_factor * c_localN0 * c_N1 * c_N2);
  U_PhaseArray pos_ag_p(extents[partNumber][3]);
  U_PhaseArray vel_ag_p(extents[partNumber][3]);

  PhaseArrayRef &pos_ag = pos_ag_p.get_array();
  PhaseArrayRef &vel_ag = vel_ag_p.get_array();

  PhaseArrayRef::index_gen i_gen;
  TapeArrayRef &pos = u_pos->get_array();
  TapeArrayRef &vel = u_vel->get_array();

  int last_step = nstep - 1;
  size_t lastParts = local_usedParticles[last_step];

  if (do_redshift) {
    ctx.print("doing redshift space distortions.");
    int rsd_step = last_step + 1;
    size_t rsdParts = local_usedParticles[rsd_step];

    //        U_PhaseArray s_pos_u(extents[lastParts][3]);
    //        PhaseArrayRef& s_pos = s_pos_u.get_array();
    //
    //        pm_redshift_pos(pos[last_step], vel[last_step], s_pos);
    ///work backwards from final to initial conditions
    //1.) undo CIC
    pm_density_obs_ag(pos[rsd_step], pos_ag, vel_ag, gradient_delta, rsdParts);
    pm_distribute_particles_ag<false>(
        nstep, pos_ag, vel_ag, pos, vel, u_idx->get_array());
    //2.) undo redshift distortions
    pm_redshift_pos_ag(
        pos[last_step], vel[last_step], pos_ag, vel_ag, lastParts);
  } else {
    pm_density_obs_ag(
        pos[last_step], pos_ag, vel_ag, gradient_delta, lastParts);
  }

  pm_fwd_model_ag(pos_ag, vel_ag, u_idx->get_array(), gradient_delta, *timing);

  releaseParticles();
}

template class LibLSS::BorgPMModel<>;

#include "libLSS/physics/modified_ngp.hpp"
template class LibLSS::BorgPMModel<
    ModifiedNGP<double, NGPGrid::Double>, ClassicCloudInCell<double>>;
template class LibLSS::BorgPMModel<
    ModifiedNGP<double, NGPGrid::Quad>, ClassicCloudInCell<double>>;

#ifdef _OPENMP
#  include "libLSS/physics/openmp_cic.hpp"
template class BorgPMModel<OpenMPCloudInCell<double>>;
#endif
