/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/borg_qlpt.cpp
    Copyright (C) 2020 Natalia Porqueres <n.porqueres@imperial.ac.uk>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/cconfig.h"
#include "libLSS/mpi/generic_mpi.hpp"
#include <CosmoTool/algo.hpp>
#include <Eigen/Core>
#include <boost/format.hpp>
#include <boost/bind.hpp>
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#ifdef ARES_MPI_FFTW
#  include <CosmoTool/fourier/fft/fftw_calls_mpi.hpp>
#endif
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/tools/powerspectrum/measure.hpp"
#include "libLSS/physics/forwards/borg_qlpt.hpp"
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
static const bool VERBOSE_QLPT = false;
static const bool DUMP_BORG_DENSITY = false;

BorgQLptModel::BorgQLptModel(
    MPI_Communication *comm, BoxModel const &box, BoxModel const &box_out,
    double hbar, bool rsd, int p_ss_factor, double p_factor, double ai,
    double af, bool light_cone, double light_cone_boost)
    : BORGForwardModel(comm, box, box_out), partFactor(p_factor),
      lctime(light_cone), lcboost(light_cone_boost), firstTime(true) {
  using boost::c_storage_order;
  ConsoleContext<LOG_DEBUG> ctx("BorgQLptModel::BorgQLptModel");

  setupDefault();
  BORG::splash_borg();
  this->do_rsd = rsd;
  this->a_init = ai;
  this->af = af;
  this->ss_factor = p_ss_factor;

  this->hbar = hbar * L0 / 2000. * 256. / N0; //0.07*L0/2000.*256./N0;

  /*    if (comm->size() > 1) {
      error_helper<ErrorParams>("MPI is not fully supported for QLPT forward model. Please use PM in degenerate configuration (nsteps=2, zstart=0)");
    }
*/

  c_N0 = N0;
  c_N1 = N1;
  c_N2 = N2;

  c_N2_HC = c_N2 / 2 + 1;

  ctx.print(
      format(
          "Building manager for supersampled resolution: N0=%d, N1=%d, N2=%d") %
      c_N0 % c_N1 % c_N2);
  mgr = new DFT_Manager(c_N0, c_N1, c_N2, comm);

  N2real = mgr->N2real;
  startN0 = mgr->startN0;
  localN0 = mgr->localN0;

  c_localN0 = mgr->localN0;
  c_startN0 = mgr->startN0;

  potential = lo_mgr->allocate_ptr_array();

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

  synthesis_plan = mgr->create_c2r_plan(AUX1_p->data(), aux_p->data());
  analysis_plan = mgr->create_r2c_plan(aux_p->data(), AUX1_p->data());

  ///initialize light cone timing
  lc_timing = std::make_shared<U_PArray>(extents[localN0 * N1 * N2][3]);
  oldParams.h = 0.0;
}

void BorgQLptModel::updateCosmo() {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  if (firstTime || oldParams != cosmo_params) {
    firstTime = false;
    oldParams = cosmo_params;
    ctx.print("Cosmo Parameter changed. Rebuild light cone.");

    Cosmology cosmo(cosmo_params);
    D0 = cosmo.d_plus(a_init);
    D1 = cosmo.d_plus(af) / D0;
    Df1 = cosmo.d_plus(af) / D0;
    f1 = cosmo.g_plus(af);
  }
}

BorgQLptModel::~BorgQLptModel() {
  ConsoleContext<LOG_DEBUG> ctx("BorgQLptModel::~BorgQLptModel");
  delete mgr;
  releaseParticles();
}

#include "qlpt/borg_fwd_qlpt.cpp"
#include "qlpt/borg_fwd_qlpt_adj.cpp"

static std::shared_ptr<BORGForwardModel> build_borg_qlpt(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  double ai = params.get<double>("a_initial");
  double af = params.get<double>("a_final");
  bool rsd = params.get<bool>("do_rsd");
  int ss_factor = params.get<double>("supersampling");
  bool light_cone = params.get<bool>("lightcone");
  double p_factor = params.get<double>("part_factor");
  double hbar = params.get<double>("hbar");
  BoxModel box_out = box;
  int mul_out = params.get<int>("mul_out", 1);

  box_out.N0 *= mul_out;
  box_out.N1 *= mul_out;
  box_out.N2 *= mul_out;

  ctx.format(
      "ai=%g, af=%g, rsd=%d, ss_factor=%d, p_factor=%d, light_cone=%d", ai, af,
      hbar, rsd, ss_factor, p_factor, light_cone);
  return std::make_shared<BorgQLptModel>(
      comm, box, box_out, hbar, rsd, ss_factor, p_factor, ai, af, light_cone);
}

AUTO_REGISTRATOR_IMPL(LIBLSS_REGISTER_NAME(QLPT_NGP));

namespace {
  _RegisterForwardModel
      MANGLED_LIBLSS_REGISTER_NAME(QLPT_NGP)("QLPT", build_borg_qlpt);

} // namespace

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Natalia Porqueres
// ARES TAG: email(0) = n.porqueres@imperial.ac.uk
// ARES TAG: year(0) = 2020
