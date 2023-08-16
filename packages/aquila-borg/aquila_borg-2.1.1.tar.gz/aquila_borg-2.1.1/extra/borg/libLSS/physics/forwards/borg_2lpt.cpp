/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/borg_2lpt.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/cconfig.h"
#include <CosmoTool/algo.hpp>
#include <Eigen/Core>
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
#include "libLSS/physics/forwards/borg_2lpt.hpp"
#include "libLSS/borg_splash.hpp"
#include "libLSS/physics/forwards/pm/part_decision.hpp"
#include <H5Cpp.h>
#include "libLSS/physics/forwards/particle_balancer/attributes.hpp"
#include "always_mpi.hpp"

using namespace LibLSS;
using namespace LibLSS::BORG_help;

using CosmoTool::square;

typedef Uninit_FFTW_Real_Array::array_type U_ArrayRef;
static const bool TEST_MODEL_RESPONSE = false;
static const bool VERBOSE_LPT = false;
static const bool DUMP_BORG_DENSITY = false;

template <typename CIC>
Borg2LPTModel<CIC>::Borg2LPTModel(
    MPI_Communication *comm, const BoxModel &box, const BoxModel &box_out,
    bool rsd, int p_ss_factor, double p_factor, double ai, double af,
    bool light_cone)
    : ParticleBasedForwardModel(comm, box, box_out), AUX1_p(0), AUX0_p(0),
      aux_p(0), partFactor(p_factor), lctime(light_cone) {
  using boost::c_storage_order;
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  setupDefault();

  BORG::splash_borg();
  this->do_rsd = rsd;
  this->a_init = ai;
  this->af = af;
  this->ss_factor = p_ss_factor;

  c_N0 = ss_factor * N0;
  c_N1 = ss_factor * N1;
  c_N2 = ss_factor * N2;

  c_N2_HC = c_N2 / 2 + 1;

  mgr = new DFT_Manager(c_N0, c_N1, c_N2, comm);

  c_N2real = mgr->N2real;
  c_startN0 = mgr->startN0;
  c_localN0 = mgr->localN0;

  ctx.print("Allocate AUX1_p");
  AUX1_m = new U_F_Array(mgr->extents_complex(), mgr->allocator_complex);
  AUX1_p = &AUX1_m->get_array();
  ctx.print("Allocate aux_p");
  aux_m = new U_R_Array(mgr->extents_real(), mgr->allocator_real);
  aux_p = &aux_m->get_array();
  ctx.print("Allocate AUX0_p");
  AUX0_m = new U_F_Array(mgr->extents_complex(), mgr->allocator_complex);
  AUX0_p = &AUX0_m->get_array();

  if (ss_factor > 1) {
    ctx.print("c_deltao");
    c_deltao_m = new U_F_Array(mgr->extents_complex(), mgr->allocator_complex);
    c_deltao = &c_deltao_m->get_array();
    ctx.print("c_tmp_real_field");
    c_tmp_real_field_m =
        new U_R_Array(mgr->extents_real(), mgr->allocator_real);
    c_tmp_real_field = &c_tmp_real_field_m->get_array();
    ctx.print("c_tmp_complex_field");
    c_tmp_complex_field_m =
        new U_F_Array(mgr->extents_complex(), mgr->allocator_complex);
    c_tmp_complex_field = &c_tmp_complex_field_m->get_array();
  } else {
    c_deltao = 0;
    c_tmp_real_field = &tmp_real_field->get_array();
    c_tmp_complex_field = &tmp_complex_field->get_array();
  }

  ctx.print("Allocating more arrays");
  u_r_psi_00 = new U_R_Array(mgr->extents_real(), mgr->allocator_real);
  u_r_psi_01 = new U_R_Array(mgr->extents_real(), mgr->allocator_real);
  u_r_psi_02 = new U_R_Array(mgr->extents_real(), mgr->allocator_real);
  u_r_psi_11 = new U_R_Array(mgr->extents_real(), mgr->allocator_real);
  u_r_psi_12 = new U_R_Array(mgr->extents_real(), mgr->allocator_real);
  u_r_psi_22 = new U_R_Array(mgr->extents_real(), mgr->allocator_real);

  u_c_psi_00 = new U_F_Array(mgr->extents_complex(), mgr->allocator_complex);
  u_c_psi_01 = new U_F_Array(mgr->extents_complex(), mgr->allocator_complex);
  u_c_psi_02 = new U_F_Array(mgr->extents_complex(), mgr->allocator_complex);
  u_c_psi_11 = new U_F_Array(mgr->extents_complex(), mgr->allocator_complex);
  u_c_psi_12 = new U_F_Array(mgr->extents_complex(), mgr->allocator_complex);
  u_c_psi_22 = new U_F_Array(mgr->extents_complex(), mgr->allocator_complex);

  r_psi_00 = &u_r_psi_00->get_array();
  r_psi_01 = &u_r_psi_01->get_array();
  r_psi_02 = &u_r_psi_02->get_array();
  r_psi_11 = &u_r_psi_11->get_array();
  r_psi_12 = &u_r_psi_12->get_array();
  r_psi_22 = &u_r_psi_22->get_array();

  c_psi_00 = &u_c_psi_00->get_array();
  c_psi_01 = &u_c_psi_01->get_array();
  c_psi_02 = &u_c_psi_02->get_array();
  c_psi_11 = &u_c_psi_11->get_array();
  c_psi_12 = &u_c_psi_12->get_array();
  c_psi_22 = &u_c_psi_22->get_array();

  ctx.print("Planning");
  c_synthesis_plan = mgr->create_c2r_plan(AUX1_p->data(), aux_p->data());
  c_analysis_plan = mgr->create_r2c_plan(aux_p->data(), AUX1_p->data());

  ///initialize light cone timing
  ctx.print("Lc_timing allocation");
  lc_timing = std::make_shared<U_PArray>(extents[c_localN0 * c_N1 * c_N2][5]);
  oldParams.h = 0.0;
}

template <typename CIC>
void Borg2LPTModel<CIC>::updateCosmo() {
  if (oldParams != cosmo_params) {
    oldParams = cosmo_params;

    gen_light_cone_timing(lc_timing->get_array());
  }
}

template <typename CIC>
Borg2LPTModel<CIC>::~Borg2LPTModel() {
  if (AUX1_p) {
    delete AUX1_m;
    delete aux_m;
    delete AUX0_m;

    if (c_deltao != 0) {
      delete c_tmp_real_field_m;
      delete c_tmp_complex_field_m;
      delete c_deltao_m;
    }

    delete u_r_psi_00;
    delete u_r_psi_01;
    delete u_r_psi_02;
    delete u_r_psi_11;
    delete u_r_psi_12;
    delete u_r_psi_22;
    delete u_c_psi_00;
    delete u_c_psi_01;
    delete u_c_psi_02;
    delete u_c_psi_11;
    delete u_c_psi_12;
    delete u_c_psi_22;

    mgr->destroy_plan(c_synthesis_plan);
    mgr->destroy_plan(c_analysis_plan);

    delete mgr;
  }
  releaseParticles();
}

#include "2lpt/borg_fwd_2lpt.cpp"
#include "2lpt/borg_fwd_2lpt_adj.cpp"

template class LibLSS::Borg2LPTModel<>;

#include "libLSS/physics/modified_ngp.hpp"
template class LibLSS::Borg2LPTModel<ModifiedNGP<double, NGPGrid::Quad>>;
template class LibLSS::Borg2LPTModel<ModifiedNGP<double, NGPGrid::Double>>;
template class LibLSS::Borg2LPTModel<ModifiedNGP<double, NGPGrid::CIC>>;

#ifdef _OPENMP
#  include "libLSS/physics/openmp_cic.hpp"
template class LibLSS::Borg2LPTModel<OpenMPCloudInCell<double>>;
#endif

template <typename Grid = ClassicCloudInCell<double>>
static std::shared_ptr<BORGForwardModel> build_borg_2lpt(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params) {
  double ai = params.get<double>("a_initial");
  double af = params.get<double>("a_final");
  bool rsd = params.get<bool>("do_rsd");
  int ss_factor = params.get<double>("supersampling");
  bool light_cone = params.get<bool>("lightcone");
  double p_factor = params.get<double>("part_factor");
  int mul_out = params.get<int>("mul_out", 1);
  BoxModel box_out = box;

  box_out.N0 *= mul_out;
  box_out.N1 *= mul_out;
  box_out.N2 *= mul_out;

  return std::make_shared<Borg2LPTModel<Grid>>(
      comm, box, box_out, rsd, ss_factor, p_factor, ai, af, light_cone);
}

AUTO_REGISTRATOR_IMPL(LIBLSS_REGISTER_NAME(2LPT_CIC));
AUTO_REGISTRATOR_IMPL(LIBLSS_REGISTER_NAME(2LPT_NGP));
AUTO_REGISTRATOR_IMPL(LIBLSS_REGISTER_NAME(2LPT_DOUBLE));

#ifdef _OPENMP
AUTO_REGISTRATOR_IMPL(LIBLSS_REGISTER_NAME(2LPT_CIC_OPENMP));
#endif

namespace {
  _RegisterForwardModel
      MANGLED_LIBLSS_REGISTER_NAME(LPT_CIC)("2LPT_CIC", build_borg_2lpt<>);
  _RegisterForwardModel MANGLED_LIBLSS_REGISTER_NAME(2LPT_NGP)(
      "2LPT_NGP", build_borg_2lpt<ModifiedNGP<double, NGPGrid::NGP>>);
  _RegisterForwardModel MANGLED_LIBLSS_REGISTER_NAME(2LPT_DOUBLE)(
      "2LPT_DOUBLE", build_borg_2lpt<ModifiedNGP<double, NGPGrid::Double>>);
#ifdef _OPENMP
  _RegisterForwardModel MANGLED_LIBLSS_REGISTER_NAME(2LPT_CIC_OPENMP)(
      "2LPT_CIC_OPENMP", build_borg_2lpt<OpenMPCloudInCell<double>>);
#endif
} // namespace
