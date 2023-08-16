/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_robust_poisson.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include <boost/multi_array.hpp>
#include <boost/tuple/tuple.hpp>
#define BOOST_TEST_MODULE robust_poisson
#define BOOST_TEST_NO_MAIN
#define BOOST_TEST_ALTERNATIVE_INIT_API
#include <boost/test/included/unit_test.hpp>
#include <boost/test/data/test_case.hpp>

#include "libLSS/tools/static_init.hpp"
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_reduce.hpp"
#include "libLSS/physics/likelihoods/base.hpp"
#include "libLSS/physics/likelihoods/robust_poisson.hpp"

using boost::extents;
using LibLSS::b_fused;
using LibLSS::b_fused_idx;
typedef LibLSS::RobustPoissonLikelihood Likelihood;

namespace utf = boost::unit_test;

boost::multi_array<double, 3> data(extents[4][8][8]);
boost::multi_array<double, 3> lambda(extents[4][8][8]);

static constexpr double CONST_LAMBDA = 2;
static constexpr double CONST_DATA = 1;
auto const_lambda = [](int i, int j, int k) -> double { return CONST_LAMBDA; };
auto vmodel = b_fused_idx<double, 3>(const_lambda);
auto mask = b_fused_idx<bool, 3>([](int, int, int) -> bool { return true; });
auto data_gen =
    b_fused_idx<double, 3>([](int, int, int) -> double { return CONST_DATA; });
using LibLSS::LikelihoodInfo;
using LibLSS::MPI_Communication;
LikelihoodInfo info;

BOOST_AUTO_TEST_CASE(likelihood_init) {
  namespace L = LibLSS::Likelihood;

  LibLSS::copy_array(lambda, vmodel);
  LibLSS::copy_array(data, data_gen);

  info[L::MPI] = MPI_Communication::instance();

  std::shared_ptr<boost::multi_array_ref<long, 3>> cmap;

  info[L::COLOR_MAP] = cmap =
      std::make_shared<boost::multi_array<long, 3>>(boost::extents[4][8][8]);

  LibLSS::copy_array(
      *cmap, b_fused_idx<long, 3>([](int, int, int) -> long { return 1; }));

  try {
    L::getMPI(info);
  } catch (const boost::bad_any_cast &a) {
    using LibLSS::Console;
    using LibLSS::LOG_DEBUG;
    Console::instance().print<LOG_DEBUG>(
        "Type is " + std::string(info[L::MPI].type().name()));
    BOOST_FAIL("Cannot recover MPI from LikelihoodInfo, " << a.what());
  }

  L::GridSize gs(boost::extents[3]), mpi_gs(boost::extents[6]);

  gs[0] = 4;
  gs[1] = 8;
  gs[2] = 8;
  mpi_gs[0] = 0;
  mpi_gs[1] = 4;
  mpi_gs[2] = 0;
  mpi_gs[3] = 8;
  mpi_gs[4] = 0;
  mpi_gs[5] = 8;

  info[L::GRID] = gs;
  info[L::MPI_GRID] = mpi_gs;
}

BOOST_AUTO_TEST_CASE(likelihood1, *utf::depends_on("likelihood_init")) {
  LibLSS::ConsoleContext<LibLSS::LOG_DEBUG> ctx("likelihood1");
  Likelihood l(info);
  ctx.print("going to log_proba");
  double L = l.log_probability(data, std::make_tuple(lambda), mask);
  double sum_lambda = 4 * 8 * 8 * CONST_LAMBDA,
         sum_log_lambda = 4 * 8 * 8 * CONST_DATA * log(CONST_LAMBDA),
         sum_N_obs = 4 * 8 * 8 * CONST_DATA;
  double ref_L = -((sum_N_obs + 1) * log(sum_lambda) - sum_log_lambda);
  BOOST_CHECK_CLOSE(L, ref_L, 1e-6);
}

BOOST_AUTO_TEST_CASE(likelihood2, *utf::depends_on("likelihood_init")) {
  Likelihood l(info);
  double L = l.log_probability(data, std::make_tuple(std::cref(vmodel)), mask);
  double sum_lambda = 4 * 8 * 8 * CONST_LAMBDA,
         sum_log_lambda = 4 * 8 * 8 * CONST_DATA * log(CONST_LAMBDA),
         sum_N_obs = 4 * 8 * 8 * CONST_DATA;
  double ref_L = -((sum_N_obs + 1) * log(sum_lambda) - sum_log_lambda);

  BOOST_CHECK_CLOSE(L, ref_L, 1e-6);
}

BOOST_AUTO_TEST_CASE(likelihood_diff, *utf::depends_on("likelihood_init")) {
  Likelihood l(info);
  double d_lambda = -1 + CONST_DATA / CONST_LAMBDA;
  double sum_lambda = 4 * 8 * 8 * CONST_LAMBDA,
         sum_log_lambda = 4 * 8 * 8 * CONST_DATA * log(CONST_LAMBDA),
         sum_N_obs = 4 * 8 * 8 * CONST_DATA;
  double ref_gradient =
      ((sum_N_obs + 1) / sum_lambda - (CONST_DATA / CONST_LAMBDA)) * d_lambda;
  auto dlog =
      l.diff_log_probability(data, std::make_tuple(std::cref(vmodel)), mask);

  for (int i = 0; i < 4; i++)
    for (int j = 0; j < 8; j++) {
      for (int k = 0; k < 8; k++) {
        double value = std::get<0>(dlog)[i][j][k];
        BOOST_CHECK_CLOSE(value, ref_gradient, 1e-6);
      }
    }
}

using namespace LibLSS;
int main(int argc, char *argv[]) {
  setupMPI(argc, argv);
  StaticInit::execute();

  Console::instance().outputToFile(
      "test_robust_likelihood.txt_" +
      to_string(MPI_Communication::instance()->rank()));

  int ret = utf::unit_test_main(&init_unit_test, argc, argv);

  StaticInit::finalize();
  doneMPI();
  return ret;
}
