/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/julia_gradient_test.cpp
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
#include "libLSS/physics/chain_forward_model.hpp"
#include "libLSS/physics/hermitic.hpp"
#include <CosmoTool/cosmopower.hpp>
#include <CosmoTool/algo.hpp>
#include <boost/format.hpp>
#include "libLSS/julia/julia.hpp"
#include "libLSS/samplers/julia/julia_likelihood.hpp"
#include "libLSS/physics/forwards/borg_lpt.hpp"
#include "libLSS/physics/likelihoods/base.hpp"
#include "libLSS/tests/setup_hades_test_run.hpp"
#include  "libLSS/physics/forwards/primordial.hpp"
#include "libLSS/physics/forwards/transfer_ehu.hpp"

using namespace LibLSS;
using boost::format;
using CosmoTool::square;
using std::string;

typedef boost::multi_array_types::extent_range range;

typedef RandomNumberThreaded<GSL_RandomNumber> RGenType;

static const int STEP_GRADIENT = 1;//8
static const bool TEST_BORG_REDSHIFT = false;

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

int main(int argc, char **argv) {
  MPI_Communication *comm = setupMPI(argc, argv);
  StaticInit::execute();
  Console &cons = Console::instance();
  cons.setVerboseLevel<LOG_DEBUG>();
  std::string code_name, module_name;

  cons.outputToFile(
      boost::str(format("gradient_test_rank_%d.txt") % comm->rank()));
  if (argc != 3) {
    cons.print<LOG_ERROR>("Invalid number of arguments");

    StaticInit::finalize();
    doneMPI();
    return 1;
  }
  code_name = argv[1];
  module_name = argv[2];

  {
    MarkovState state;
    RGenType randgen(-1);
    BoxModel box;
    LikelihoodInfo info;

    randgen.seed(2348098);

    state.newElement(
        "random_generator", new RandomStateElement<RandomNumber>(&randgen));

    LibLSS_test::setup_hades_test_run(comm, 16, 600., state);
    LibLSS_test::setup_box(state, box);
    LibLSS_test::setup_likelihood_info(state, info);

    CosmologicalParameters &cparams =
        state.getScalar<CosmologicalParameters>("cosmology");

    DummyPowerSpectrum dummy_p(comm);
    auto likelihood = std::make_shared<JuliaDensityLikelihood>(
        comm, info, code_name, module_name);
    auto model = std::make_shared<BorgLptModel<>>(
        comm, box, box, false /* norsd*/, 1 /* ss factor */, 2.0, 0.001, 1.0,
        false);
    auto chain = std::make_shared<ChainForwardModel>(comm, box);
    auto fixer = std::make_shared<ForwardHermiticOperation>(comm, box);

    chain->addModel(fixer);
    chain->addModel(std::make_shared<ForwardPrimordial>(comm, box, 0.001));
    chain->addModel(std::make_shared<ForwardEisensteinHu>(comm, box));
    chain->addModel(model);

    HMCDensitySampler hmc(comm, likelihood);

    {
      ArrayType1d::ArrayType vobs(boost::extents[3]);
      vobs[0] = 1000.;
      vobs[1] = -300;
      vobs[2] = 200.;
      model->setObserver(vobs);
    }
    state.newElement("BORG_model", new BorgModelElement(chain));

    dummy_p.init_markov(state);

    hmc.init_markov(state);

    hmc.generateMockData(state);
    cons.setVerboseLevel<LOG_INFO>();
    hmc.checkGradient(state, STEP_GRADIENT);
    hmc.checkGradientReal(state, STEP_GRADIENT);

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
