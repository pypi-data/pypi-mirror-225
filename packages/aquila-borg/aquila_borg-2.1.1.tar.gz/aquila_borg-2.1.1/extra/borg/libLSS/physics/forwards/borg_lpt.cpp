/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/borg_lpt.cpp
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
#include "libLSS/physics/forwards/borg_lpt.hpp"
#include "libLSS/borg_splash.hpp"
#include <H5Cpp.h>
#include "libLSS/physics/forwards/particle_balancer/attributes.hpp"
#include "libLSS/physics/forwards/particle_balancer/particle_distribute.hpp"
#include "always_mpi.hpp"
#include "libLSS/physics/forwards/registry.hpp"

using namespace LibLSS;
using namespace LibLSS::BORG_help;

using CosmoTool::square;

static const bool TEST_MODEL_RESPONSE = false;
static const bool VERBOSE_LPT = false;
static const bool DUMP_BORG_DENSITY = false;

template <typename CIC>
BorgLptModel<CIC>::BorgLptModel(
    MPI_Communication *comm, BoxModel const &box, BoxModel const &box_out,
    bool rsd, int p_ss_factor, double p_factor, double ai, double af,
    bool light_cone, double light_cone_boost)
    : ParticleBasedForwardModel(comm, box, box_out), partFactor(p_factor),
      lctime(light_cone), lcboost(light_cone_boost), firstTime(true) {
  using boost::c_storage_order;
  ConsoleContext<LOG_DEBUG> ctx("BorgLptModel::BorgLptModel");

  setupDefault();
  BORG::splash_borg();
  this->invalidCache = true;
  this->do_rsd = rsd;
  this->a_init = ai;
  this->af = af;
  this->ss_factor = p_ss_factor;

  ctx.format("Part factor = %g", partFactor);

  c_N0 = ss_factor * N0;
  c_N1 = ss_factor * N1;
  c_N2 = ss_factor * N2;

  c_N2_HC = c_N2 / 2 + 1;

  ctx.print(
      format(
          "Building manager for supersampled resolution: N0=%d, N1=%d, N2=%d") %
      c_N0 % c_N1 % c_N2);
  mgr = new DFT_Manager(c_N0, c_N1, c_N2, comm);

  c_N2real = mgr->N2real;
  c_startN0 = mgr->startN0;
  c_localN0 = mgr->localN0;

  ctx.print("Allocating AUX1");
  AUX1_m = mgr->allocate_ptr_complex_array();
  AUX1_p = &AUX1_m->get_array();
  ctx.print("Allocating aux");
  aux_m = mgr->allocate_ptr_array();
  aux_p = &aux_m->get_array();
  ctx.print("Allocating AUX0");
  AUX0_m = mgr->allocate_ptr_complex_array();
  AUX0_p = &AUX0_m->get_array();

  if (ss_factor > 1) {
    ctx.print("Allocating c_deltao");
    c_deltao_m = mgr->allocate_ptr_complex_array();
    c_deltao = &c_deltao_m->get_array();
    ctx.print("Allocating c_tmp_real_field");
    c_tmp_real_field_m = mgr->allocate_ptr_array();
    c_tmp_real_field = &c_tmp_real_field_m->get_array();
    ctx.print(
        format("Number of elements = %d") % c_tmp_real_field->num_elements());
    ctx.print("Allocating c_tmp_complex_field");
    c_tmp_complex_field_m = mgr->allocate_ptr_complex_array();
    c_tmp_complex_field = &c_tmp_complex_field_m->get_array();
  } else {
    c_deltao = 0;
    c_tmp_real_field = &tmp_real_field->get_array();
    c_tmp_complex_field = &tmp_complex_field->get_array();
  }

  c_synthesis_plan = mgr->create_c2r_plan(AUX1_p->data(), aux_p->data());
  c_analysis_plan = mgr->create_r2c_plan(aux_p->data(), AUX1_p->data());

  ///initialize light cone timing
  lc_timing = std::make_shared<U_PArray>(extents[c_localN0 * c_N1 * c_N2][3]);
  oldParams.h = 0.0;
}

template <typename CIC>
void BorgLptModel<CIC>::updateCosmo() {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  if (firstTime || oldParams != cosmo_params) {
    firstTime = false;
    oldParams = cosmo_params;
    ctx.print("Cosmo Parameter changed. Rebuild light cone.");

    invalidCache = true;

    gen_light_cone_timing(lc_timing->get_array());
  }
}

template <typename CIC>
bool BorgLptModel<CIC>::densityInvalidated() const {
  return invalidCache;
}

template <typename CIC>
BorgLptModel<CIC>::~BorgLptModel() {
  ConsoleContext<LOG_DEBUG> ctx("BorgLptModel::~BorgLptModel");
  mgr->destroy_plan(c_synthesis_plan);
  mgr->destroy_plan(c_analysis_plan);
  delete mgr;
  releaseParticles();
}

#include "lpt/borg_fwd_lpt.cpp"
#include "lpt/borg_fwd_lpt_adj.cpp"

template class LibLSS::BorgLptModel<>;

#include "libLSS/physics/modified_ngp.hpp"
template class LibLSS::BorgLptModel<ModifiedNGP<double, NGPGrid::NGP>>;
template class LibLSS::BorgLptModel<ModifiedNGP<double, NGPGrid::Quad>>;
template class LibLSS::BorgLptModel<ModifiedNGP<double, NGPGrid::Double>>;
template class LibLSS::BorgLptModel<ModifiedNGP<double, NGPGrid::CIC>>;

#include "libLSS/physics/modified_ngp_smooth.hpp"
template class LibLSS::BorgLptModel<SmoothModifiedNGP<double, NGPGrid::Quad>>;
template class LibLSS::BorgLptModel<SmoothModifiedNGP<double, NGPGrid::CIC>>;

#ifdef _OPENMP
#  include "libLSS/physics/openmp_cic.hpp"
template class LibLSS::BorgLptModel<OpenMPCloudInCell<double>>;
#endif

template <typename Grid = ClassicCloudInCell<double>>
static std::shared_ptr<BORGForwardModel> build_borg_lpt(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  double ai = params.get<double>("a_initial");
  double af = params.get<double>("a_final");
  bool rsd = params.get<bool>("do_rsd");
  int ss_factor = params.get<double>("supersampling");
  bool light_cone = params.get<bool>("lightcone");
  double p_factor = params.get<double>("part_factor");
  BoxModel box_out = box;
  int mul_out = params.get<int>("mul_out", 1);

  box_out.N0 *= mul_out;
  box_out.N1 *= mul_out;
  box_out.N2 *= mul_out;

  ctx.format(
      "ai=%g, af=%g, rsd=%d, ss_factor=%d, p_factor=%d, light_cone=%d", ai, af,
      rsd, ss_factor, p_factor, light_cone);
  return std::make_shared<BorgLptModel<Grid>>(
      comm, box, box_out, rsd, ss_factor, p_factor, ai, af, light_cone);
}

AUTO_REGISTRATOR_IMPL(LIBLSS_REGISTER_NAME(LPT_CIC));
AUTO_REGISTRATOR_IMPL(LIBLSS_REGISTER_NAME(LPT_DOUBLE));
AUTO_REGISTRATOR_IMPL(LIBLSS_REGISTER_NAME(LPT_NGP));

#ifdef _OPENMP
AUTO_REGISTRATOR_IMPL(LIBLSS_REGISTER_NAME(LPT_CIC_OPENMP));
#endif
namespace {
  _RegisterForwardModel
      MANGLED_LIBLSS_REGISTER_NAME(LPT_CIC)("LPT_CIC", build_borg_lpt<>);
  _RegisterForwardModel MANGLED_LIBLSS_REGISTER_NAME(LPT_NGP)(
      "LPT_NGP", build_borg_lpt<ModifiedNGP<double, NGPGrid::NGP>>);
  _RegisterForwardModel MANGLED_LIBLSS_REGISTER_NAME(LPT_DOUBLE)(
      "LPT_DOUBLE", build_borg_lpt<ModifiedNGP<double, NGPGrid::Double>>);
#ifdef _OPENMP
  _RegisterForwardModel MANGLED_LIBLSS_REGISTER_NAME(LPT_CIC_OPENMP)(
      "LPT_CIC_OPENMP", build_borg_lpt<OpenMPCloudInCell<double>>);
#endif
} // namespace
