/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/tests/generic_gradient_test.cpp
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
#include "libLSS/physics/likelihoods/base.hpp"
#include "libLSS/physics/hades_pt.hpp"
#include "libLSS/physics/chain_forward_model.hpp"
#include "libLSS/physics/hermitic.hpp"

using namespace LibLSS;
using boost::format;
using CosmoTool::square;
using std::string;

typedef boost::multi_array_types::extent_range range;

typedef RandomNumberMPI<GSL_RandomNumber> RGenType;

static const int STEP_GRADIENT = 1 * 1; //2*2;//8*8;
static const bool TEST_BORG_REDSHIFT = false;

#ifndef BORG_SUPERSAMPLING
#  define BORG_SUPERSAMPLING 1
#endif

#ifndef BORG_FORCESAMPLING
#  define BORG_FORCESAMPLING 1
#endif

#ifndef MODEL_TO_TEST
#  define MODEL_TO_TEST(model, box)                                            \
    auto model = new HadesLinear(comm, box, 0.001)
#endif

namespace {
#if defined(ARES_MPI_FFTW)
  RegisterStaticInit reg0(fftw_mpi_init, fftw_mpi_cleanup, 9, "MPI/FFTW");
#endif
  RegisterStaticInit reg1(
      CosmoTool::init_fftw_wisdom, CosmoTool::save_fftw_wisdom, 10,
      "FFTW/WISDOM");
}; // namespace

class DummyPowerSpectrum : public PowerSpectrumSampler_Base {
public:
  DummyPowerSpectrum(MPI_Communication *comm)
      : PowerSpectrumSampler_Base(comm) {}

  virtual void initialize(MarkovState &state) { initialize_base(state); }
  virtual void restore(MarkovState &state) { restore_base(state); }

  virtual void sample(MarkovState &state) {}
};

void createCosmologicalPowerSpectrum(
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
  for (long i = 0; i < k.num_elements(); i++) {
    Pk[i] = cpower.power(k[i] * h) * h * h * h * adjust;
  }
}

int main(int argc, char **argv) {
  MPI_Communication *comm = setupMPI(argc, argv);
  StaticInit::execute();
  Console &cons = Console::instance();
  cons.setVerboseLevel<LOG_DEBUG>();

  cons.outputToFile(
      boost::str(format("gradient_test_rank_%d.txt") % comm->rank()));
  {
    MarkovState state;
    SelArrayType *sel_data, *sel_data2;
    SLong *N0, *N1, *N2, *N2_HC, *Ncat, *fourierLocalSize, *NUM_MODES, *localN0,
        *startN0;
    SDouble *L0, *L1, *L2, *K_MIN, *K_MAX, *corner0, *corner1, *corner2,
        *borg_a_initial;
    ArrayType1d *bias0;
    ArrayType *data0, *growth;
    RGenType randgen(comm, -1);
    int M;
    BoxModel box, box2;

    randgen.seed(2348098);

    state.newElement(
        "random_generator", new RandomStateElement<RandomNumber>(&randgen));

    state.newElement("N0", N0 = new SLong());
    state.newElement("N1", N1 = new SLong());
    state.newElement("N2", N2 = new SLong());
    state.newElement("N2_HC", N2_HC = new SLong());
    state.newElement("NUM_MODES", NUM_MODES = new SLong());
    state.newElement("K_MIN", K_MIN = new SDouble());
    state.newElement("K_MAX", K_MAX = new SDouble());

    state.newElement("L0", L0 = new SDouble());
    state.newElement("L1", L1 = new SDouble());
    state.newElement("L2", L2 = new SDouble());

    state.newElement("NCAT", Ncat = new SLong());
    state.newElement("startN0", startN0 = new SLong());
    state.newElement("localN0", localN0 = new SLong());
    state.newElement("fourierLocalSize", fourierLocalSize = new SLong());

    state.newElement("corner0", corner0 = new SDouble());
    state.newElement("corner1", corner1 = new SDouble());
    state.newElement("corner2", corner2 = new SDouble());

    state.newElement("borg_a_initial", borg_a_initial = new SDouble());

    state.newScalar<double>("ares_heat", 1.0);
    state.newScalar<int>("borg_pm_nsteps", 1);
    state.newScalar<double>("borg_pm_start_z", 69.);
    state.newScalar<bool>("borg_do_rsd", TEST_BORG_REDSHIFT);
    state.newScalar<int>("borg_supersampling", BORG_SUPERSAMPLING);
    state.newScalar<int>("borg_forcesampling", BORG_FORCESAMPLING);

    M = box.N0 = N0->value = 16;
    box.N1 = N1->value = M;
    box.N2 = N2->value = M;

    state.newScalar<long>("Ndata0", M / DOWNGRADE_DATA);
    state.newScalar<long>("Ndata1", M / DOWNGRADE_DATA);
    state.newScalar<long>("Ndata2", M / DOWNGRADE_DATA);
    ptrdiff_t localn0, startn0, data_localn0, data_startn0;

#ifdef ARES_MPI_FFTW
    {

      fourierLocalSize->value =
          MPI_FCalls::local_size_3d(M, M, M, comm->comm(), &localn0, &startn0);
      startN0->value = startn0;
      localN0->value = localn0;

      MPI_FCalls::local_size_3d(
          M / DOWNGRADE_DATA, M / DOWNGRADE_DATA, M / DOWNGRADE_DATA,
          comm->comm(), &data_localn0, &data_startn0);
    }
#else
    fourierLocalSize->value = M * M * (M / 2 + 1);
    startn0 = startN0->value = 0;
    localn0 = localN0->value = M;
    data_localn0 = M / DOWNGRADE_DATA;
    data_startn0 = 0;
#endif

    state.newScalar<long>("localNdata0", data_startn0);
    state.newScalar<long>("localNdata1", data_startn0 + data_localn0);
    state.newScalar<long>("localNdata2", 0);
    state.newScalar<long>("localNdata3", (M / DOWNGRADE_DATA));
    state.newScalar<long>("localNdata4", 0);
    state.newScalar<long>("localNdata5", (M / DOWNGRADE_DATA));

    cons.print<LOG_INFO>(
        format("startN0 = %d, localN0 = %d") % startN0->value % localN0->value);

    Ncat->value = 1;

    box.xmin0 = corner0->value = -1500;
    box.xmin1 = corner1->value = -1500;
    box.xmin2 = corner2->value = -1500;
    N2_HC->value = M / 2 + 1;
    NUM_MODES->value = 300;
    box.L0 = L0->value = 3000.0;
    box.L1 = L1->value = 3000.0;
    box.L2 = L2->value = 3000.0;
    K_MIN->value = 0.;
    K_MAX->value =
        M_PI *
        sqrt(
            square(N0->value / L0->value) + square(N1->value / L1->value) +
            square(N2->value / L2->value)) *
        1.1;

    box2 = box;
    box2.N0 *= 2;
    box2.N1 *= 2;
    box2.N2 *= 2;

    borg_a_initial->value = 0.001;

    state.newElement(
        "growth_factor",
        growth = new ArrayType(
            boost::extents[range(startn0, startn0 + localn0)][M][M]));
    growth->eigen().fill(1);
    growth->setRealDims(ArrayDimension(M, M, M));
    if (DOWNGRADE_DATA == 1) {
      auto ext = boost::extents[range(startn0, startn0 + localn0)][M][M];
      auto adim = ArrayDimension(M, M, M);
      state.newElement("galaxy_data_0", data0 = new ArrayType(ext));
      data0->setRealDims(adim);
      state.newElement("galaxy_sel_window_0", sel_data = new SelArrayType(ext));
      sel_data->setRealDims(adim);
      state.newElement(
          "galaxy_synthetic_sel_window_0", sel_data2 = new SelArrayType(ext));
      sel_data2->setRealDims(adim);
    } else {
      size_t startdown = data_startn0;
      size_t enddown = data_startn0 + data_localn0;
      auto ext = boost::extents[range(startdown, enddown)][M / DOWNGRADE_DATA]
                               [M / DOWNGRADE_DATA];
      auto adim = ArrayDimension(
          M / DOWNGRADE_DATA, M / DOWNGRADE_DATA, M / DOWNGRADE_DATA);

      state.newElement("galaxy_data_0", data0 = new ArrayType(ext));
      data0->setRealDims(adim);
      state.newElement("galaxy_sel_window_0", sel_data = new SelArrayType(ext));
      sel_data->setRealDims(adim);
      state.newElement(
          "galaxy_synthetic_sel_window_0", sel_data2 = new SelArrayType(ext));
      sel_data2->setRealDims(adim);
    }
    state.newElement(
        "galaxy_bias_0", bias0 = new ArrayType1d(boost::extents[0]));
    state.newScalar("galaxy_nmean_0", 20.0);
    state.newScalar("galaxy_bias_ref_0", false);
    state.newScalar("ares_heat", 1.0);

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
    // Initialize (data,s)->t sampler

    LikelihoodInfo info;

    {
      namespace L = LibLSS::Likelihood;

      info[L::MPI] = MPI_Communication::instance();
      info["ManyPower_prior_width"] = 3.5;

      L::GridSize gs(boost::extents[3]), mpi_gs(boost::extents[6]),
          gsd(boost::extents[3]);
      L::GridLengths gl(boost::extents[6]);

      state.getScalarArray<long, 3>("Ndata", gsd);

      gs[0] = N0->value;
      gs[1] = N1->value;
      gs[2] = N2->value;
      mpi_gs[0] = startn0;
      mpi_gs[1] = startn0 + localn0;
      mpi_gs[2] = 0;
      mpi_gs[3] = N1->value;
      mpi_gs[4] = 0;
      mpi_gs[5] = N2->value;
      gl[0] = corner0->value;
      gl[1] = corner0->value + L0->value;
      gl[2] = corner1->value;
      gl[3] = corner1->value + L1->value;
      gl[4] = corner2->value;
      gl[5] = corner2->value + L2->value;

      info[L::GRID] = gs;
      info[L::GRID_LENGTH] = gl;
      info[L::MPI_GRID] = mpi_gs;
      info[L::DATA_GRID] = gsd;
      info["EFT_Lambda"] = 0.07;

      std::shared_ptr<boost::multi_array_ref<long, 3>> cmap =
          std::make_shared<boost::multi_array<long, 3>>(boost::extents[range(
              startn0, startn0 + localn0)][N1->value][N2->value]);

      array::fill(*cmap, 0);

      for (int i = startn0; i < startn0 + localn0; i++) {
        for (int j = 0; j < N1->value; j++) {
          for (int k = 0; k < N2->value; k++) {
            long idx = (i + j * N0->value + k * N0->value * N1->value) % 8;

            (*cmap)[i][j][k] = idx;
          }
        }
      }
      auto p_cmap = make_promise_pointer(cmap);
      info[L::COLOR_MAP] = p_cmap;

      p_cmap.defer.submit_ready();
    }

#ifdef DATA_SETUP
    DATA_SETUP(state);
#endif

    DummyPowerSpectrum dummy_p(comm);
    HMCDensitySampler::Likelihood_t likelihood = makeLikelihood(info);
    HMCDensitySampler hmc(comm, likelihood);

    dummy_p.init_markov(state);

    auto model = makeModel(comm, state, box, box2);
    auto chain = std::make_shared<ChainForwardModel>(comm, box);
    auto fixer = std::make_shared<ForwardHermiticOperation>(comm, box);

    BorgModelElement *model_element = new BorgModelElement();

    chain->addModel(fixer);
    chain->addModel(model);

    {
      ArrayType1d::ArrayType vobs(boost::extents[3]);
      vobs[0] = 1000.;
      vobs[1] = -300;
      vobs[2] = 200.;
      model->setObserver(vobs);
    }
    model_element->obj = std::shared_ptr<BORGForwardModel>(chain);
    state.newElement("BORG_model", model_element);

    createCosmologicalPowerSpectrum(state, cparams);

    hmc.init_markov(state);

    likelihood->setupDefaultParameters(state, 0);

    // Build some mock field

    sel_data->eigen().fill(1);
    sel_data2->eigen().fill(1);

#if 0
    //Build spherical mask
    for (int n0 = 0; n0 < M; n0++) {
        for (int n1 = 0; n1 < M; n1++) {
            for (int n2 = 0; n2 < M; n2++) {

            double r= sqrt((n0-M/2)*(n0-M/2) + (n1-M/2)*(n1-M/2) +(n2-M/2)*(n2-M/2));

            if(r>M/4) (*sel_data->array)[n0][n1][n2] = 0.;

            }
            }
            }
#endif
#if 0
    for (int n0 = startn0; n0 < startn0 + localn0; n0++) {
      double in0 = (n0 - M / 2) * 1.0 / M;
      for (int n1 = 0; n1 < M; n1++) {
        double in1 = (n1 - M / 2) * 1.0 / M;
        for (int n2 = 0; n2 < M; n2++) {
          double in2 = (n2 - M / 2) * 1.0 / M;
          double S =
              exp(-0.5 * (in0 * in0 + in1 * in1 + in2 * in2) / (0.2 * 0.2));
          double r = sqrt(
              (n0 - M / 2) * (n0 - M / 2) + (n1 - M / 2) * (n1 - M / 2) +
              (n2 - M / 2) * (n2 - M / 2));

          (*sel_data->array)[n0][n1][n2] = S;
          if (r > M / 4)
            (*sel_data->array)[n0][n1][n2] = 0.;
          (*sel_data2->array)[n0][n1][n2] = (*sel_data->array)[n0][n1][n2];
        }
      }
    }
#endif
    // Build some s field

    long N2real;

#ifdef ARES_MPI_FFTW
    N2real = 2 * N2_HC->value;
#else
    N2real = N2->value;
#endif

    hmc.generateMockData(state);
    cons.setVerboseLevel<LOG_INFO>();
    hmc.checkGradient(state, STEP_GRADIENT);
    //hmc.checkGradientReal(state, STEP_GRADIENT);

    {
      std::shared_ptr<H5::H5File> f;

      if (comm->rank() == 0)
        f = std::make_shared<H5::H5File>("dump.h5", H5F_ACC_TRUNC);

      state.mpiSaveState(f, comm, false);
    }
  }
  StaticInit::finalize();
  doneMPI();

  return 0;
}
