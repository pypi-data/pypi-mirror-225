/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/generic_borg_vobs_test.cpp
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
#include "libLSS/tests/setup_hades_test_run.hpp"
#include "libLSS/samplers/generic/generic_hmc_likelihood.hpp"
#include "libLSS/physics/likelihoods/base.hpp"

using namespace LibLSS;
using boost::format;
using CosmoTool::square;
using std::string;

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

  cons.outputToFile(boost::str(format("borg_vobs_test_%d.txt") % comm->rank()));
  {
    MarkovState state;
    BoxModel box;
    LikelihoodInfo info;

    LibLSS_test::setup_hades_test_run(comm, 32, 600, state);
    LibLSS_test::setup_box(state, box);
    LibLSS_test::setup_likelihood_info(state, info);

    L::gridSide(info);
    auto likelihood = std::make_shared<ThisLikelihood>(info);
    auto model = makeModel(state, box, info);
    HMCDensitySampler hmc(comm, likelihood);

    GenericVobsSampler<ThisLikelihood> meta(comm, likelihood);
    BorgModelElement *model_element = new BorgModelElement();
    ArrayType1d *vobs = 0;
    DummyPowerSpectrum dummy_p(comm);

    model_element->obj = model;
    state.newElement("BORG_model", model_element);

    dummy_p.init_markov(state);
    hmc.init_markov(state);
    meta.init_markov(state);

    //set current observer velocity state
    vobs = state.get<ArrayType1d>("BORG_vobs");

    //set vobs
    (*vobs->array)[0] = 1000.;
    (*vobs->array)[1] = 1000.;
    (*vobs->array)[2] = 1000.;

    hmc.generateMockData(state);

    //now test meta sampler

    for (int nn = 0; nn < 100; nn++)
      meta.sample(state);
  }

  StaticInit::finalize();
  doneMPI();

  return 0;
}
