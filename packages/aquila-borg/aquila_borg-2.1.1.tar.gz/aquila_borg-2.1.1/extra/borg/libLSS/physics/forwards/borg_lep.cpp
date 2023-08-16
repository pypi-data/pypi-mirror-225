/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/borg_lep.cpp
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
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/tools/powerspectrum/measure.hpp"
#include "libLSS/physics/forwards/borg_lep.hpp"
#include "libLSS/tools/fused_array.hpp"

#undef EXPERIMENTAL_ORDERING

using namespace LibLSS;
using namespace LibLSS::BORG_help;
using CosmoTool::square;

static const double unit_r0 = 1.0;               // Units of distances = 1 Mpc/h
static const double H0 = 100.0;                  // h km/s/Mpc
static const double unit_t0 = 1 / H0;            // Units of time
static const double unit_v0 = unit_r0 / unit_t0; // Units of velocity

#include "lep/borg_fwd_lep.cpp"
#include "lep/borg_fwd_lep_adj.cpp"

template <typename CIC>
void BorgLEPModel<CIC>::tabulate_sin() {
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

template <typename CIC>
BorgLEPModel<CIC>::BorgLEPModel(
    MPI_Communication *comm, const BoxModel &box, int ss_factor, int f_factor,
    int lep_nsteps, bool do_rsd, double ai, double z_start)
    : BORGForwardModel(comm, box) {
  this->ss_factor = ss_factor;
  this->f_factor = f_factor;
  this->lep_nsteps = lep_nsteps;
  this->z_start = z_start;
  this->do_redshift = do_rsd;
  this->ai = ai;

  alloc_arrays();
  tabulate_sin();
}

template <typename CIC>
void BorgLEPModel<CIC>::alloc_arrays() {
  using boost::c_storage_order;

  c_N0 = ss_factor * N0;
  c_N1 = ss_factor * N1;
  c_N2 = ss_factor * N2;
  c_N2_HC = c_N2 / 2 + 1;

  f_N0 = f_factor * N0;
  f_N1 = f_factor * N1;
  f_N2 = f_factor * N2;
  f_N2_HC = f_N2 / 2 + 1;

  force_mgr = new DFT_Manager(f_N0, f_N1, f_N2, comm);
  mgr = new DFT_Manager(c_N0, c_N1, c_N2, comm);

  c_startN0 = mgr->startN0;
  c_localN0 = mgr->localN0;
  f_startN0 = force_mgr->startN0;
  f_localN0 = force_mgr->localN0;

  AUX1_p = new CArray(
      mgr->extents_complex(), c_storage_order(), mgr->allocator_complex);
  aux_p =
      new Array(mgr->extents_real(), c_storage_order(), mgr->allocator_real);
  AUX0_p = new CArray(
      mgr->extents_complex(), c_storage_order(), mgr->allocator_complex);
  f_AUX0_p = new CArray(
      force_mgr->extents_complex(), c_storage_order(),
      force_mgr->allocator_complex);

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
    lo_AUX0_p = AUX0_p;
  }

  ///setup array for large scale gravitational potential
  g_lep0 = new Uninit_FFTW_Real_Array(
      force_mgr->extents_real(), force_mgr->allocator_real);
  g_lep1 = new Uninit_FFTW_Real_Array(
      force_mgr->extents_real(), force_mgr->allocator_real);
  g_lep2 = new Uninit_FFTW_Real_Array(
      force_mgr->extents_real(), force_mgr->allocator_real);

  Uninit_FFTW_Real_Array f_tmp_p(
      force_mgr->extents_real(), force_mgr->allocator_real);
  Uninit_FFTW_Real_Array::array_type &f_tmp = f_tmp_p.get_array();

  c_synthesis_plan = mgr->create_c2r_plan(AUX1_p->data(), aux_p->data());
  c_analysis_plan = mgr->create_r2c_plan(aux_p->data(), AUX1_p->data());
  f_synthesis_plan = force_mgr->create_c2r_plan(f_AUX0_p->data(), f_tmp.data());
  f_analysis_plan = force_mgr->create_r2c_plan(f_tmp.data(), f_AUX0_p->data());
}

template <typename CIC>
BorgLEPModel<CIC>::~BorgLEPModel() {
  delete AUX0_p;
  delete AUX1_p;
  delete aux_p;
  delete f_AUX0_p;

  if (c_deltao != 0) {
    delete c_deltao;
    delete c_tmp_real_field;
    delete c_tmp_complex_field;
    delete lo_AUX0_p;
  }

  mgr->destroy_plan(c_synthesis_plan);
  mgr->destroy_plan(c_analysis_plan);

  force_mgr->destroy_plan(f_synthesis_plan);
  force_mgr->destroy_plan(f_analysis_plan);

  delete force_mgr;
  delete mgr;
}

template <typename CIC>
void BorgLEPModel<CIC>::forwardModel(
    CArrayRef &delta_init, ArrayRef &delta_output, bool adjointNext) {
  ConsoleContext<LOG_DEBUG> ctx("BORG-lep MODEL");
  int nstep = lep_nsteps;

#ifdef EXPERIMENTAL_ORDERING
  typedef boost::general_storage_order<3> order_type;
  typedef order_type::size_type size_type;
  size_type ordering[] = {0, 2, 1};
  bool ascending[] = {true, true, true};
  order_type order(ordering, ascending);
  u_pos = new UninitializedArray<TapeArray>(
      extents[nstep][c_localN0 * c_N1 * c_N2][3]);
  u_vel = new UninitializedArray<TapeArray>(
      extents[nstep][c_localN0 * c_N1 * c_N2][3], std::allocator<double>(),
      order);
#else
  u_pos = new UninitializedArray<TapeArray>(
      extents[nstep][c_localN0 * c_N1 * c_N2][3]);
  u_vel = new UninitializedArray<TapeArray>(
      extents[nstep][c_localN0 * c_N1 * c_N2][3]);
#endif
  timing = new TimingArray(extents[6][nstep]);

  lep_fwd_model(
      delta_init, delta_output, u_pos->get_array(), u_vel->get_array(),
      *timing);

  if (!forwardModelHold && !adjointNext) {
    releaseParticles();
  }
}

template <typename CIC>
void BorgLEPModel<CIC>::adjointModel(ArrayRef &gradient_delta) {
  int nstep = lep_nsteps;

  lep_fwd_model_ag(
      gradient_delta, u_pos->get_array(), u_vel->get_array(), gradient_delta,
      *timing);

  releaseParticles();
}

template class LibLSS::BorgLEPModel<>;

#ifdef _OPENMP
#  include "libLSS/physics/openmp_cic.hpp"
template class LibLSS::BorgLEPModel<OpenMPCloudInCell<double>>;
#endif
