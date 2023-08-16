/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/benchmark_generic_likelihood.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/samplers/borg/borg_poisson_likelihood.hpp"
#include "libLSS/samplers/generic/generic_hmc_likelihood.hpp"
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/physics/bias/broken_power_law.hpp"
#include "libLSS/physics/bias/broken_power_law_sigmoid.hpp"
#include "libLSS/physics/likelihoods/voxel_poisson.hpp"
#include "libLSS/physics/likelihoods/negative_binomial.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"
#include "libLSS/tests/setup_hades_test_run.hpp"
#include "libLSS/physics/forwards/borg_lpt.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "generic_mock.hpp"
#include "libLSS/physics/adapt_classic_to_nb.hpp"
#include <boost/timer/timer.hpp>

using namespace LibLSS;

typedef GenericHMCLikelihood<bias::BrokenPowerLaw, VoxelPoissonLikelihood>
    Likelihood_t;
typedef BorgPoissonLikelihood LikelihoodRef_t;
typedef GenericMetaSampler<Likelihood_t, NmeanSelector> MetaNmean_t;
typedef GenericMetaSampler<Likelihood_t, BiasParamSelector<0>> MetaBias0_t;
typedef Likelihood_t::bias_t bias_t;

using namespace boost::timer;

int main(int argc, char **argv) {
  using boost::extents;
  using LibLSS::fwrap;
  MPI_Communication *mpi_world = setupMPI(argc, argv);
  LibLSS::QUIET_CONSOLE_START = true;
  Console::instance().setVerboseLevel<LOG_ERROR>();
  StaticInit::execute();

  {
    const size_t N = 16;
    const double L = 100;
    MarkovState state;
    BoxModel box;

    boost::multi_array<double, 1> bias_params(
        boost::extents[bias_t::numParams]);
    LikelihoodInfo info;

    bias_t::setup_default(bias_params);

    LibLSS_test::setup_hades_test_run(mpi_world, N, L, state, &bias_params);
    LibLSS_test::setup_box(state, box);
    LibLSS_test::setup_likelihood_info(state, info);
    auto likelihood = std::make_shared<Likelihood_t>(info);
    auto likelihood_ref = std::make_shared<LikelihoodRef_t>(info);
    HMCDensitySampler hmc(mpi_world, likelihood);
    HMCDensitySampler hmc_ref(mpi_world, likelihood_ref);
    auto lpt = std::make_shared<BorgLptModel<>>(
        mpi_world, box, box, false, 1, 2.0,
        state.getScalar<double>("borg_a_initial"), 1.0, false);

    BorgModelElement *model_element = new BorgModelElement();
    model_element->obj = lpt;
    state.newElement("BORG_model", model_element);

    // Initialize the likelihood for good.
    hmc.init_markov(state);
    hmc_ref.init_markov(state);
    likelihood->updateMetaParameters(state);
    generate_mock_data<Likelihood_t>(mpi_world, state, N, L);

    {
      cpu_timer timer;
      double r = 0;
      for (size_t i = 0; i < 100; i++)
        r += hmc.computeHamiltonian(state);
      std::cout << "100 likelihood evaluation (new scheme): " << timer.format()
                << std::endl
                << " value " << r << std::endl;
    }
    {
      auto grad_array_p = lpt->lo_mgr->allocate_complex_array();
      auto &grad_array = grad_array_p.get_array();
      likelihood->gradientLikelihood(
          grad_array, *state.get<CArrayType>("s_hat_field")->array, false, 1.0);
    }

    {
      cpu_timer timer;
      double r = 0;
      for (size_t i = 0; i < 100; i++)
        r += hmc_ref.computeHamiltonian(state);
      std::cout << "100 likelihood evaluation (old scheme): " << timer.format()
                << std::endl
                << " value " << r << std::endl;
    }
  }
  StaticInit::finalize();
  LibLSS::doneMPI();

  return 0;
}
