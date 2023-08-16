/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/tests/test_julia_hmclet.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#define BOOST_TEST_MODULE julia_hmclet
#define BOOST_TEST_NO_MAIN
#define BOOST_TEST_ALTERNATIVE_INIT_API
#include <boost/test/included/unit_test.hpp>
#include <boost/test/data/test_case.hpp>

#include "libLSS/julia/julia.hpp"
#include "libLSS/julia/julia_mcmc.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/mcmc/state_element.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/console.hpp"

#include "libLSS/tests/setup_hades_test_run.hpp"

#include "libLSS/samplers/julia/julia_likelihood.hpp"
#include "libLSS/physics/forwards/borg_lpt.hpp"
#include "libLSS/tools/string_tools.hpp"
#include "libLSS/hmclet/julia_hmclet.hpp"

namespace utf = boost::unit_test;

using namespace LibLSS;
using namespace LibLSS_test;

struct JuliaFixture {
  static MPI_Communication *comm;
  static MarkovState *state;
  static BoxModel box;

  JuliaFixture() {
    LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
    state = new MarkovState();
    setup_hades_test_run(comm, 32, 600., *state);
    setup_box(*state, box);

    ObjectStateElement<BORGForwardModel, true> *model_elt =
        new ObjectStateElement<BORGForwardModel, true>();

    state->newScalar<bool>("bias_sampler_blocked", false);
    state->newScalar<long>("MCMC_STEP", 0);

    double ai = state->getScalar<double>("borg_a_initial");

    model_elt->obj =
        new BorgLptModel<>(comm, box, box, false, 1, 2.0, ai, 1.0, false);
    state->newElement("BORG_model", model_elt);
  }

  ~JuliaFixture() { Console::instance().print<LOG_DEBUG>("Destroying state."); delete state; }
};

MPI_Communication *JuliaFixture::comm = 0;
MarkovState *JuliaFixture::state;
BoxModel JuliaFixture::box;

BOOST_GLOBAL_FIXTURE(JuliaFixture);

BOOST_AUTO_TEST_CASE(julia_hmclet_fail) {
  LikelihoodInfo info;
  LibLSS_test::setup_likelihood_info(
      *JuliaFixture::state, info);
  Console::instance().print<LOG_DEBUG>(boost::format("Comm is %p") % JuliaFixture::comm);
  auto density = std::make_shared<JuliaDensityLikelihood>(
      JuliaFixture::comm, info, TEST_JULIA_LIKELIHOOD_CODE, "TestLikelihood");
  return;
  JuliaHmcletMeta meta(JuliaFixture::comm, density, "TestLikelihood", JuliaHmclet::types::DIAGONAL, 10, 10, 0.5, true);

  density->initializeLikelihood(*JuliaFixture::state);
  meta.init_markov(*JuliaFixture::state);
  meta.sample(*JuliaFixture::state);
}

int main(int argc, char *argv[]) {
  JuliaFixture::comm = setupMPI(argc, argv);
  StaticInit::execute();

  Console::instance().outputToFile(
      "test_julia_hmclet.txt_" +
      to_string(MPI_Communication::instance()->rank()));

  int ret = utf::unit_test_main(&init_unit_test, argc, argv);

  StaticInit::finalize();
  doneMPI();
  return ret;
}
