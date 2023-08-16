/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_generic_likelihood_base.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/samplers/generic/generic_hmc_likelihood.hpp"
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/physics/hades_log.hpp"
#include "libLSS/physics/bias/broken_power_law.hpp"
#include "libLSS/physics/likelihoods/voxel_poisson.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"
#include "setup_hades_test_run.hpp"

using namespace LibLSS;

typedef GenericHMCLikelihood<bias::PowerLaw, VoxelPoissonLikelihood>
    Likelihood_t;
//typedef GenericMetaSampler<Likelihood_t, NmeanSelector> MetaNmean_t;
typedef GenericMetaSampler<Likelihood_t, BiasParamSelector<0>> MetaNmean_t;
typedef GenericMetaSampler<Likelihood_t, BiasParamSelector<1>> MetaBias0_t;

int main(int argc, char **argv) {
  using boost::extents;
  using LibLSS::fwrap;
  MPI_Communication *mpi_world = setupMPI(argc, argv);
//  LibLSS::QUIET_CONSOLE_START = true;
  StaticInit::execute();

  Console::instance().setVerboseLevel<LOG_DEBUG>();

  {
    size_t N = 32;

    //Likelihood_t likelihood(mpi_world);

    MarkovState state;
    LikelihoodInfo info;
    BoxModel box;
    //    LikelihoodBroken_t likelihood_broken(mpi_world);

    LibLSS_test::setup_hades_test_run(mpi_world, N, 100., state);
    LibLSS_test::setup_likelihood_info(state, info);
    LibLSS_test::setup_box(state, box);

    auto likelihood = std::make_shared<Likelihood_t>(info);
    MetaNmean_t nmean_sampler(mpi_world, likelihood);
    MetaBias0_t bias_sampler(mpi_world, likelihood);
    RandomNumberThreaded<GSL_RandomNumber> rgen(-1);

    rgen.seed(1);

    double nmean = 0.9;
    size_t N_post = 1000;
    MetaNmean_t::BiasParamArray bias_params(extents[2]);
    MetaNmean_t::SelectionArray sel_field(extents[N][N][N]);
    MetaNmean_t::DensityArray matter_density(extents[N][N][N]);
    MetaNmean_t::DataArray data(extents[N][N][N]);
    MetaNmean_t::CatalogData cdata{nmean, bias_params, sel_field,
                                   matter_density, data};
    MetaBias0_t::CatalogData cdata2{nmean, bias_params, sel_field,
                                    matter_density, data};

    bias_params[0] = 0.9;
    bias_params[1] = 3.3;
    fwrap(sel_field) = 1;
    // Make three sinus
    auto rhom = fwrap(matter_density);

    state.newElement("BORG_model",
      new BorgModelElement(
        std::make_shared<HadesLog>(mpi_world, box, 0.001)
      )
    );

    likelihood->initializeLikelihood(state);

    rhom = LibLSS::b_fused_idx<double, 3>(
        [N](size_t i, size_t j, size_t k) -> double {
          double x = double(i) / N;
          double z = double(j) / N;
          double y = double(k) / N;

          return sin(M_PI * x) * sin(M_PI * y) * sin(M_PI * z);
        });

    // Make nmean=3, data
    fwrap(data) = rgen.poisson(nmean * std::pow(1 + 1e-6+ rhom, bias_params[1]));

    //std::cout << matter_density[16][13][10] << std::endl;
    //std::cout << data[16][13][10] << std::endl;

    std::ofstream f("bias_posterior.txt");
    for (size_t i = 0; i < N_post; i++) {
      double x = (6.0 * (i + 1)) / N_post;
      f << x << " " << nmean_sampler.bound_posterior(1.0, x, cdata) << " "
                << bias_sampler.bound_posterior(1.0, x, cdata2) << std::endl;
    }
  }
  StaticInit::finalize();

  return 0;
}
