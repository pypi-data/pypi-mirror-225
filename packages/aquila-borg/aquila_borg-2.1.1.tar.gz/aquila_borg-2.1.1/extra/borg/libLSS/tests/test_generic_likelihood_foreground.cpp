/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_generic_likelihood_foreground.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#define BOOST_TEST_MODULE generic_likelihood_foreground
#define BOOST_TEST_NO_MAIN
#define BOOST_TEST_ALTERNATIVE_INIT_API

#include <boost/test/included/unit_test.hpp>
#include <boost/test/data/test_case.hpp>

#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/samplers/generic/generic_hmc_likelihood.hpp"
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/physics/bias/broken_power_law.hpp"
#include "libLSS/physics/likelihoods/robust_poisson.hpp"
#include "libLSS/physics/likelihoods/negative_binomial.hpp"
#include "libLSS/physics/likelihoods/negative_binomial_alt.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"
#include "libLSS/tests/setup_hades_test_run.hpp"
#include "libLSS/physics/forwards/borg_lpt.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "generic_mock.hpp"
#include "libLSS/physics/adapt_classic_to_nb.hpp"
#include "libLSS/tools/string_tools.hpp"
#include "src/common/foreground.hpp"

using namespace LibLSS;

namespace utf = boost::unit_test;

// Classical bias routines need to be adapted to work with negative binomial
// But the additional parameter is automatically discovered
typedef GenericHMCLikelihood<bias::PowerLaw, RobustPoissonLikelihood>
    Likelihood_t;
//typedef GenericHMCLikelihood<bias::BrokenPowerLaw,VoxelPoissonLikelihood> Likelihood_t;
typedef Likelihood_t::bias_t bias_t;

int main(int argc, char **argv) {
  using boost::extents;
  using LibLSS::fwrap;
  setupMPI(argc, argv);
  LibLSS::QUIET_CONSOLE_START = true;
  Console::instance().outputToFile(
      "test_likelihood.txt_" +
      to_string(MPI_Communication::instance()->rank()));
  Console::instance().setVerboseLevel<LOG_ERROR>();

  StaticInit::execute();

  int ret = utf::unit_test_main(&init_unit_test, argc, argv);

  StaticInit::finalize();
  LibLSS::doneMPI();
  return ret;
}

BOOST_AUTO_TEST_CASE(foreground) {
  const size_t N = 64;
  const double L = 100;
  MarkovState state;
  BoxModel box;
  auto mpi_world = MPI_Communication::instance();

  boost::multi_array<double, 1> bias_params(boost::extents[bias_t::numParams]);

  bias_t::setup_default(bias_params);
  bias_params[0] = 10;

  LibLSS_test::setup_hades_test_run(mpi_world, N, L, state, &bias_params);
  LibLSS_test::setup_box(state, box);
  LikelihoodInfo info;
  std::shared_ptr<boost::multi_array_ref<long, 3>> colormap3d =
      std::make_shared<boost::multi_array<long, 3>>(boost::extents[N][N][N]);

  LibLSS_prepare::details::ForegroundAdaptor fg_adapt;
  std::array<double, 3> delta{L / N, L / N, L / N};
  std::array<double, 3> corner{0.5 * L, 0.5 * L, 0.5 * L};
  LibLSS_prepare::RGenType randgen(mpi_world, -1);
  fg_adapt.loadSky("cmap.fits");
  compute_window_value_elem(
      mpi_world, randgen, fg_adapt, *colormap3d, {L, L, L}, delta, corner,
      false, 0.1);

  info[Likelihood::COLOR_MAP] = colormap3d;
  info[Likelihood::MPI] = mpi_world;

  auto likelihood = std::make_shared<Likelihood_t>(info);
  auto lpt = std::make_shared<BorgLptModel<>>(
      mpi_world, box, box, false, 1, 2.0, state.getScalar<double>("borg_a_initial"),
      1.0, false);
  HMCDensitySampler hmc(mpi_world, likelihood);

  state.newElement("BORG_model", new BorgModelElement(lpt));

  // Initialize the likelihood for good.
  hmc.init_markov(state);

  Console::instance().print<LOG_VERBOSE>("Generating mock data");
  generate_mock_data<Likelihood_t>(mpi_world, state, N, L);

  // Now we are going to scale up and down the s_hat_field and print the likelihood
  CArrayType::ArrayType &s_hat_field =
      *state.get<CArrayType>("s_hat_field")->array;
  //boost::multi_array<std::complex<double>, 3> saved_field = s_hat_field;

  boost::multi_array<double, 3> FG(boost::extents[N][N][N]);
  fg_adapt.loadSky("DUST.fits");
  compute_window_value_elem(
      mpi_world, randgen, fg_adapt, FG, {L, L, L}, delta, corner, false, 0.1);

  double ref_L = 0;
  double nmean = 0; // unused in practice
  double min_FG = fwrap(FG).min();
  double max_FG = fwrap(FG).max();
  double min_alpha, max_alpha;

  if (max_FG > 0) {
    max_alpha = 1 / max_FG;
    min_alpha = -1 / max_FG; //1/min_FG;
  } else {
    min_alpha = 1 / max_FG;
    max_alpha = -1 / max_FG; //1/min_FG;
  }
  auto f_FG = fwrap(FG);

  for (size_t i = 0; i < 50; i++) {
    double alpha = min_alpha + (i + 1) / 50. * (max_alpha - min_alpha);

    auto sel_window =
        fwrap(*state.get<SelArrayType>("galaxy_sel_window_0")->array);
    auto synth_sel_window =
        fwrap(*state.get<SelArrayType>("galaxy_synthetic_sel_window_0")->array);

    synth_sel_window = (1 - alpha * f_FG) * sel_window;

    double L = -hmc.computeHamiltonian(state);
    if (i == 0)
      ref_L = L;
    std::cout << alpha << " " << (L - ref_L) << std::endl;
  }
}
