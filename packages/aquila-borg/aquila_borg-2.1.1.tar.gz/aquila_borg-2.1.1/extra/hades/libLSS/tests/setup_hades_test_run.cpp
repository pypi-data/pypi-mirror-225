/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/tests/setup_hades_test_run.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/tools/static_init.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/physics/forward_model.hpp"
#include <CosmoTool/cosmopower.hpp>
#include <CosmoTool/algo.hpp>
#include <boost/format.hpp>
#include "libLSS/tools/fusewrapper.hpp"
#include "setup_hades_test_run.hpp"
#include "libLSS/physics/likelihoods/base.hpp"

using namespace LibLSS;
using boost::format;
using CosmoTool::square;
using std::string;

typedef boost::multi_array_types::extent_range range;

typedef RandomNumberThreaded<GSL_RandomNumber> RGenType;

namespace {
#if defined(ARES_MPI_FFTW)
  RegisterStaticInit reg0(fftw_mpi_init, fftw_mpi_cleanup, 9, "MPI/FFTW");
#endif
  RegisterStaticInit reg1(
      CosmoTool::init_fftw_wisdom, CosmoTool::save_fftw_wisdom, 10,
      "FFTW/WISDOM");

  class DummyPowerSpectrum : public PowerSpectrumSampler_Base {
  public:
    DummyPowerSpectrum(MPI_Communication *comm)
        : PowerSpectrumSampler_Base(comm) {}

    virtual void initialize(MarkovState &state) { initialize_base(state); }
    virtual void restore(MarkovState &state) { restore_base(state); }

    virtual void sample(MarkovState &state) {}
  };

  constexpr size_t TEST_NUM_MODES = 200;

}; // namespace

static void createCosmologicalPowerSpectrum(
    MarkovState &state, CosmologicalParameters &cosmo_params,
    double adjust = 1) {
  double h;
  CosmoTool::CosmoPower cpower;

  h = cpower.h = cosmo_params.h;
  cpower.OMEGA_B = cosmo_params.omega_b;
  cpower.OMEGA_C = cosmo_params.omega_m - cosmo_params.omega_b;
  cpower.SIGMA8 = cosmo_params.sigma8;
  cpower.setFunction(CosmoTool::CosmoPower::HU_WIGGLES);
  cpower.updateCosmology();
  cpower.normalize();

  ArrayType1d::ArrayType &k = *state.get<ArrayType1d>("k_modes")->array;
  ArrayType1d::ArrayType &Pk = *state.get<ArrayType1d>("powerspectrum")->array;
  for (size_t i = 0; i < k.num_elements(); i++) {
    Pk[i] = cpower.power(k[i] * h) * h * h * h * adjust;
  }
}

void LibLSS_test::setup_box(MarkovState &state, BoxModel &box) {
  box.xmin0 = state.getScalar<double>("corner0");
  box.xmin1 = state.getScalar<double>("corner1");
  box.xmin2 = state.getScalar<double>("corner2");
  box.L0 = state.getScalar<double>("L0");
  box.L1 = state.getScalar<double>("L1");
  box.L2 = state.getScalar<double>("L2");
  box.N0 = state.getScalar<long>("N0");
  box.N1 = state.getScalar<long>("N1");
  box.N2 = state.getScalar<long>("N2");
}

void LibLSS_test::setup_likelihood_info(
    MarkovState &state, LikelihoodInfo &info, MPI_Communication *comm) {
  namespace L = LibLSS::Likelihood;

  info[L::MPI] = comm;
  info["ManyPower_prior_width"] = 3.5;

  L::GridSize gs(boost::extents[3]), gsd(boost::extents[3]),
      mpi_gs(boost::extents[6]);
  L::GridLengths gl(boost::extents[6]);

  state.getScalarArray<long, 3>("N", gs);
  mpi_gs[0] = state.getScalar<long>("startN0");
  mpi_gs[1] = mpi_gs[0] + state.getScalar<long>("localN0");
  mpi_gs[2] = 0;
  mpi_gs[3] = gs[1];
  mpi_gs[4] = 0;
  mpi_gs[5] = gs[2];
  gl[0] = state.getScalar<double>("corner0");
  gl[2] = state.getScalar<double>("corner1");
  gl[4] = state.getScalar<double>("corner2");
  gl[1] = gl[0] + state.getScalar<double>("L0");
  gl[3] = gl[2] + state.getScalar<double>("L1");
  gl[5] = gl[4] + state.getScalar<double>("L2");

  info[L::GRID] = gs;
  info[L::GRID_LENGTH] = gl;
  info[L::MPI_GRID] = mpi_gs;
  info["EFT_Lambda"] = 0.15;   // Some default, 0.15 h/Mpc
  if (state.exists("Ndata0")) {
    state.getScalarArray<long, 3>("Ndata", gsd);
    info[L::DATA_GRID] = gsd;
  }

  std::shared_ptr<boost::multi_array_ref<long, 3>> cmap =
      std::make_shared<boost::multi_array<long, 3>>(
          boost::extents[range(mpi_gs[0], mpi_gs[1])][mpi_gs[3]][mpi_gs[5]]);
  array::fill(*cmap, 0);

  for (int i = mpi_gs[0]; i < mpi_gs[1]; i++) {
    for (int j = 0; j < mpi_gs[3]; j++) {
      for (int k = 0; k < mpi_gs[5]; k++) {
        long idx = (i + j * gs[0] + k * gs[0] * gs[1]) % 8;

        (*cmap)[i][j][k] = idx;
      }
    }
  }
  auto promise_cmap = make_promise_pointer(cmap);
  info[L::COLOR_MAP] = promise_cmap;

  promise_cmap.defer.submit_ready();
}

void LibLSS_test::setup_hades_test_run(
    MPI_Communication *comm, size_t Nbase, double L, MarkovState &state,
    boost::multi_array_ref<double, 1> *bias_params) {
  Console &cons = Console::instance();

  SelArrayType *sel_data, *s_sel_data;
  ArrayType1d *bias0;
  ArrayType *data0, *growth;
  RGenType *randgen = new RGenType(-1);

  randgen->seed(23482098);

  cons.print<LOG_INFO>("Setting up a mock run configuration");

  state.newElement(
      "random_generator", new RandomStateElement<RandomNumber>(randgen, true));

  state.newScalar<long>("N0", Nbase);
  state.newScalar<long>("N1", Nbase);
  state.newScalar<long>("N2", Nbase);
  state.newScalar<long>("N2_HC", Nbase / 2 + 1);
  state.newScalar<long>("NUM_MODES", TEST_NUM_MODES);
  state.newScalar<double>("K_MIN", 0);
  state.newScalar<double>("K_MAX", 2 * M_PI / L * Nbase * 1.1 * std::sqrt(3.0));

  state.newScalar<double>("L0", L);
  state.newScalar<double>("L1", L);
  state.newScalar<double>("L2", L);

  state.newScalar<long>("NCAT", 1);

  state.newScalar<double>("ares_heat", 1.0);

  state.newScalar<double>("corner0", -L / 2);
  state.newScalar<double>("corner1", -L / 2);
  state.newScalar<double>("corner2", -L / 2);

  state.newScalar<double>("borg_a_initial", 0.001);

  state.newScalar<int>("borg_pm_nsteps", 30);
  state.newScalar<double>("borg_pm_start_z", 69.);

  FFTW_Manager_3d<double> mgr(Nbase, Nbase, Nbase, comm);

  state.newScalar<long>("startN0", mgr.startN0);
  state.newScalar<long>("localN0", mgr.localN0);
  state.newScalar<long>("fourierLocalSize", mgr.allocator_real.minAllocSize);

  auto local_extent =
      boost::extents[range(mgr.startN0, mgr.startN0 + mgr.localN0)][Nbase]
                    [Nbase];
  auto full_extent = ArrayDimension(Nbase, Nbase, Nbase);

  state.newElement("growth_factor", growth = new ArrayType(local_extent));
  growth->eigen().fill(1);
  growth->setRealDims(full_extent);
  state.newElement("galaxy_data_0", data0 = new ArrayType(local_extent));
  data0->setRealDims(full_extent);
  state.newElement(
      "galaxy_sel_window_0", sel_data = new SelArrayType(local_extent));
  state.newElement(
      "galaxy_synthetic_sel_window_0",
      s_sel_data = new SelArrayType(local_extent));
  sel_data->setRealDims(full_extent);
  s_sel_data->setRealDims(full_extent);

  size_t Nb = (bias_params == 0) ? 1 : bias_params->shape()[0];
  state.newElement(
      "galaxy_bias_0", bias0 = new ArrayType1d(boost::extents[Nb]));

  if (bias_params == 0)
    (*bias0->array)[0] = 2;
  else
    fwrap(*bias0->array) = *bias_params;
  state.newScalar<double>("galaxy_nmean_0", 20);
  state.newScalar<bool>("galaxy_bias_ref_0", true);

  DummyPowerSpectrum dummy_p(comm);

  dummy_p.init_markov(state);

  ScalarStateElement<CosmologicalParameters> *s_cosmo =
      new ScalarStateElement<CosmologicalParameters>();
  state.newElement("cosmology", s_cosmo);

  CosmologicalParameters &cparams = s_cosmo->value;
  cparams.omega_r = 0.; /* negligible radiation density */
  cparams.omega_k = 0.; /* curvature - flat prior for everything! */
  cparams.omega_m = 0.3175;
  cparams.omega_b = 0.049;
  cparams.omega_q = 0.6825;
  cparams.w = -1.;
  cparams.n_s = 0.9624;
  cparams.wprime = 0.;
  cparams.sigma8 = 0.8344;
  cparams.h = 0.6711;
  cparams.beta = 1.5;
  cparams.z0 = 0.;
  cparams.a0 = 1.; /* scale factor at epoch of observation usually 1*/

  createCosmologicalPowerSpectrum(state, cparams);

  // Build some mock field

  sel_data->eigen().fill(1);
  s_sel_data->eigen().fill(1);
}
