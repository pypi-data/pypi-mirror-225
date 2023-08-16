/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_julia_likelihood.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#define BOOST_TEST_MODULE julia_likelihood
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
#include "libLSS/physics/likelihoods/base.hpp"

namespace utf = boost::unit_test;

using namespace LibLSS;
using namespace LibLSS_test;

struct JuliaFixture {
  static MPI_Communication *comm;
  static MarkovState *state;
  static BoxModel box;
  static GridDensityLikelihoodBase<3>::GridSizes N;
  static GridDensityLikelihoodBase<3>::GridLengths L;
  static LikelihoodInfo info;

  JuliaFixture() {
    LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);

    state = new MarkovState();
    setup_hades_test_run(comm, 32, 600., *state);
    setup_box(*state, box);

    BorgModelElement *model_elt =
        new BorgModelElement();

    double ai = state->getScalar<double>("borg_a_initial");

    N[0] = 32;
    N[1] = 32;
    N[2] = 32;

    L[0] = 600.;
    L[1] = 600.;
    L[2] = 600.;

    model_elt->obj =
        std::make_shared<BorgLptModel<>>(comm, box, box, false, 1, 2.0, ai, 1.0, false);
    state->newElement("BORG_model", model_elt);

    setup_likelihood_info(*state, info);
  }

  ~JuliaFixture() { delete state; }
};

MPI_Communication *JuliaFixture::comm = 0;
MarkovState *JuliaFixture::state;
BoxModel JuliaFixture::box;
GridDensityLikelihoodBase<3>::GridSizes JuliaFixture::N;
GridDensityLikelihoodBase<3>::GridLengths JuliaFixture::L;
LikelihoodInfo JuliaFixture::info;

BOOST_GLOBAL_FIXTURE(JuliaFixture);

BOOST_AUTO_TEST_CASE(julia_likelihood_evaluation) {
  auto density = std::make_shared<JuliaDensityLikelihood>(
      JuliaFixture::comm, JuliaFixture::info,
      TEST_JULIA_LIKELIHOOD_CODE, "TestLikelihood");
  HMCDensitySampler hmc(JuliaFixture::comm, density);

  hmc.init_markov(*JuliaFixture::state);

  hmc.generateMockData(*JuliaFixture::state);
  hmc.computeHamiltonian(*JuliaFixture::state);

  auto model =
      JuliaFixture::state
          ->get<BorgModelElement>("BORG_model")
          ->obj;
  auto &s_hat_field =
      *JuliaFixture::state->get<CArrayType>("s_hat_field")->array;

  FFTW_Complex_Array grad_array(
      model->lo_mgr->extents_complex(), boost::c_storage_order(),
      model->lo_mgr->allocator_complex);

  density->gradientLikelihood(s_hat_field, grad_array, false, 1.0);
}

int main(int argc, char *argv[])
{
  JuliaFixture::comm = setupMPI(argc,argv);
  StaticInit::execute();

  Console::instance().outputToFile(
      "test_julia_likelihood.txt_" +
      to_string(MPI_Communication::instance()->rank()));

  int ret = utf::unit_test_main(&init_unit_test, argc, argv);

  StaticInit::finalize();
  doneMPI();
  return ret;
}
