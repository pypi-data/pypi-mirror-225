/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_generic_likelihood_bias.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/samplers/generic/generic_hmc_likelihood.hpp"
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/physics/bias/broken_power_law.hpp"
#include "libLSS/physics/bias/broken_power_law_sigmoid.hpp"
#include "libLSS/physics/likelihoods/voxel_poisson.hpp"
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

using namespace LibLSS;

// Classical bias routines need to be adapted to work with negative binomial
// But the additional parameter is automatically discovered
typedef GenericHMCLikelihood<
    AdaptBias_NB<bias::BrokenPowerLaw>, AltNegativeBinomialLikelihood>
    Likelihood_t;
//typedef GenericHMCLikelihood<bias::BrokenPowerLaw,VoxelPoissonLikelihood> Likelihood_t;
typedef GenericMetaSampler<Likelihood_t, NmeanSelector> MetaNmean_t;
typedef BiasParamSelector<3> Selector;
typedef GenericMetaSampler<Likelihood_t, Selector> MetaBias0_t;
typedef Likelihood_t::bias_t bias_t;

int main(int argc, char **argv) {
  using boost::extents;
  using LibLSS::fwrap;
  MPI_Communication *mpi_world = setupMPI(argc, argv);
  LibLSS::QUIET_CONSOLE_START = true;
  Console::instance().setVerboseLevel<LOG_ERROR>();
  StaticInit::execute();

  {
    const size_t N = 64;
    const double L = 100;
    MarkovState state;
    BoxModel box;

    boost::multi_array<double, 1> bias_params(
        boost::extents[bias_t::numParams]);

    bias_t::setup_default(bias_params);
    bias_params[3] = 10;

    LibLSS_test::setup_hades_test_run(mpi_world, N, L, state, &bias_params);
    LibLSS_test::setup_box(state, box);
    LikelihoodInfo info;
    auto likelihood = std::make_shared<Likelihood_t>(info);
    auto lpt = std::make_shared<BorgLptModel<>>(
        mpi_world, box, box, false, 1, 2.0,
        state.getScalar<double>("borg_a_initial"), 1.0, false);
    HMCDensitySampler hmc(mpi_world, likelihood);

    BorgModelElement *model_element = new BorgModelElement();
    model_element->obj = lpt;
    state.newElement("BORG_model", model_element);

    // Initialize the likelihood for good.
    hmc.init_markov(state);

    Console::instance().print<LOG_VERBOSE>("Generating mock data");
    generate_mock_data<Likelihood_t>(mpi_world, state, N, L);

    // Now we are going to scale up and down the s_hat_field and print the likelihood
    CArrayType::ArrayType &s_hat_field =
        *state.get<CArrayType>("s_hat_field")->array;
    //boost::multi_array<std::complex<double>, 3> saved_field = s_hat_field;

    double ref_L = 0;
    double nmean = 0; // unused in practice
    for (size_t i = 0; i < 50; i++) {
      double bias = 9 + 2 * (i + 1) / 50.;

      Selector::select(
          bias, nmean, *state.get<ArrayType1d>("galaxy_bias_0")->array);

      double L = -hmc.computeHamiltonian(state);
      if (i == 0)
        ref_L = L;
      std::cout << bias << " " << (L - ref_L) << std::endl;
    }
  }
  StaticInit::finalize();
  LibLSS::doneMPI();

  return 0;
}
