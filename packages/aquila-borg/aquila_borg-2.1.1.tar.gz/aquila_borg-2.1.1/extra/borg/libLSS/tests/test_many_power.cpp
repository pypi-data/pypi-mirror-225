/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_many_power.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include <boost/multi_array.hpp>
#include <boost/tuple/tuple.hpp>
#define BOOST_TEST_MODULE many_power
#define BOOST_TEST_NO_MAIN
#define BOOST_TEST_ALTERNATIVE_INIT_API
#include <boost/test/included/unit_test.hpp>
#include <boost/test/data/test_case.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/physics/bias/many_power.hpp"
#include "libLSS/physics/forwards/borg_lpt.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"

namespace utf = boost::unit_test;
using namespace LibLSS;
using namespace LibLSS::bias::detail_manypower;

static constexpr bool TEST_ULTRA_VERBOSE = false;

BOOST_AUTO_TEST_CASE(create_many_power) {
  size_t numLevel = Levels<double>::numLevel;
  size_t numParams;
  BOOST_CHECK_EQUAL(numLevel, 0);

  numParams = 0;
  numLevel = Levels<double, 0>::numLevel;
  BOOST_CHECK_EQUAL(numLevel, 1);
  BOOST_CHECK_EQUAL(numParams, 0);
}

BOOST_AUTO_TEST_CASE(build_levels) {
  static constexpr int N = 4;
  typedef Levels<double, 1, 1> Levels_t;
  Levels_t base_level;
  GhostPlanes<double, 2> ghosts;
  boost::multi_array<double, 3> final_density(boost::extents[N][N][N]);

  LibLSS::copy_array(
      final_density,
      b_fused_idx<double, 3>(
          [](size_t i, size_t j, size_t k) -> double { return i + j + k; }));

  auto comm = MPI_Communication::instance();
  std::unique_ptr<MPI_Communication> local_comm(comm->split(comm->rank()));

  base_level.allocate(N, N, N, N, 0, N);
  base_level.setup(ghosts, local_comm.get());
  base_level.buildLevels(ghosts, final_density);

  for (int j = 0; j < 3; j++)
    BOOST_REQUIRE_EQUAL(base_level.this_level_cache.shape()[j], N / 2);

  auto &second_level = base_level.previousLevels;

  for (size_t i = 0; i < N / 2; i++) {
    for (size_t j = 0; j < N / 2; j++) {
      for (size_t k = 0; k < N / 2; k++) {
        double a = 0;
        for (int r0 = 0; r0 < 2; r0++) {
          for (int r1 = 0; r1 < 2; r1++) {
            for (int r2 = 0; r2 < 2; r2++) {
              BOOST_REQUIRE_EQUAL(
                  final_density[2 * i + r0][2 * j + r1][2 * k + r2],
                  (i * 2 + r0) + (j * 2 + r1) + (k * 2 + r2));
              a += (i * 2 + r0) + (j * 2 + r1) + (k * 2 + r2);
            }
          }
        }
        a /= 8;
        BOOST_REQUIRE_EQUAL(base_level.this_level_cache[i][j][k], a);
      }
    }
  }

  base_level.clear_cache();
  std::array<double, Levels_t::numLevel> local_ag;
  boost::multi_array<double, 3> ag_density(boost::extents[N][N][N]);
  for (size_t i = 0; i < N; i++) {
    for (size_t j = 0; j < N; j++) {
      for (size_t k = 0; k < N; k++) {
        local_ag[0] = 0.1 * j;
        local_ag[1] = 0.5 * i;
        base_level.push_ag_density(local_ag, ag_density, i, j, k);
      }
    }
  }
  base_level.ag_buildLevels(ghosts, ag_density);
  for (size_t i = 0; i < N / 2; i++) {
    for (size_t j = 0; j < N; j++) {
      for (size_t k = 0; k < N; k++) {
        double q = 0.5 * (2 * i + 2 * i + 1) / 2;
        for (int r = 0; r < 2; r++) {
          //Console::instance().print<LOG_DEBUG>(to_string(i)+","+to_string(j)+","+to_string(k) + " ->" + to_string(q) + " vs. " + to_string(ag_density[2*i+r][j][k]));
          BOOST_REQUIRE_EQUAL(ag_density[2 * i + r][j][k], 0.1 * j + q);
        }
      }
    }
  }
}

BOOST_AUTO_TEST_CASE(build_levels_mpi) {
  using boost::multi_array_types::extent_range;
  static constexpr int N = 8;
  Levels<double, 1, 1, 1> base_level;
  GhostPlanes<double, 2> ghosts;
  auto comm = MPI_Communication::instance();
  int rank = comm->rank();
  int csize = comm->size();
  size_t pstart = N * rank / csize, pend = N * (rank + 1) / csize;
  boost::multi_array<double, 3> final_density(
      boost::extents[extent_range(pstart, pend)][N][N]);
  boost::multi_array<double, 3> final_density_ref(boost::extents[N][N][N]);
  constexpr size_t resolution = 2;
  ConsoleContext<LOG_DEBUG> ctx("build_levels_mpi");

  ctx.print("pstart = " + to_string(pstart) + " pend = " + to_string(pend));

  auto generator = b_fused_idx<double, 3>(
      [](size_t i, size_t j, size_t k) -> double { return i + j + k; });

  LibLSS::copy_array(final_density_ref, generator);
  LibLSS::copy_array(final_density, generator);

  base_level.allocate(N, N, N, N, pstart, pend - pstart);
  base_level.setup(ghosts, comm);
  ghosts.synchronize(final_density);
  ;

  base_level.buildLevels(ghosts, final_density);

  auto &second_level = base_level.previousLevels;

  for (size_t i = pstart / 2; i < pend / 2; i++) {
    for (size_t j = 0; j < N / 2; j++) {
      for (size_t k = 0; k < N / 2; k++) {
        double a = 0;
        for (int r0 = 0; r0 < 2; r0++) {
          for (int r1 = 0; r1 < 2; r1++) {
            for (int r2 = 0; r2 < 2; r2++) {
              BOOST_REQUIRE_CLOSE(
                  final_density_ref[2 * i + r0][2 * j + r1][2 * k + r2],
                  (i * 2 + r0) + (j * 2 + r1) + (k * 2 + r2), 1e-3);
              a += (i * 2 + r0) + (j * 2 + r1) + (k * 2 + r2);
            }
          }
        }
        a /= 8;
        if (TEST_ULTRA_VERBOSE) {
          ctx.print("Voxel = " + to_string(std::array<size_t, 3>{i, j, k}));
          ctx.print(
              "cache=" + to_string(second_level.this_level_cache[i][j][k]) +
              " ref = " + to_string(a));
        }
        BOOST_CHECK_CLOSE(second_level.this_level_cache[i][j][k], a, 1e-3);
      }
    }
  }

  auto &first_level = base_level;

  ctx.print("pstart,pend =  " + to_string(std::array<size_t, 2>{pstart, pend}));
  for (size_t i = pstart / 4;
       i < pstart / 4 + std::max(size_t(1), pend / 4 - pstart / 4); i++) {
    for (size_t j = 0; j < N / 4; j++) {
      for (size_t k = 0; k < N / 4; k++) {
        double a = 0;
        for (size_t r0 = 0; r0 < 4; r0++) {
          for (size_t r1 = 0; r1 < 4; r1++) {
            for (size_t r2 = 0; r2 < 4; r2++) {
              if (TEST_ULTRA_VERBOSE) {
                ctx.print(
                    "FVoxel = " +
                    to_string(std::array<size_t, 6>{i, j, k, r0, r1, r2}));
              }
              BOOST_REQUIRE_CLOSE(
                  final_density_ref[4 * i + r0][4 * j + r1][4 * k + r2],
                  (4 * i + r0) + (4 * j + r1) + (4 * k + r2), 1e-3);
              a += (i * 4 + r0) + (j * 4 + r1) + (k * 4 + r2);
            }
          }
        }
        a /= 8 * 8;
        if (TEST_ULTRA_VERBOSE) {
          ctx.print("Voxel = " + to_string(std::array<size_t, 3>{i, j, k}));
          ctx.print(
              "cache=" + to_string(first_level.this_level_cache[i][j][k]) +
              " ref = " + to_string(a));
        }
        BOOST_CHECK_CLOSE(first_level.this_level_cache[i][j][k], a, 1e-3);
      }
    }
  }

  base_level.clear_cache();
}

BOOST_AUTO_TEST_CASE(build_manypower) {
  using boost::multi_array_types::extent_range;
  static constexpr int N = 8;
  BoxModel box = {0, 0, 0, 100, 100, 100, N, N, N};
  boost::multi_array<double, 3> final_density_ref(boost::extents[N][N][N]);
  ConsoleContext<LOG_DEBUG> ctx("build_manypower");
  bias::ManyPower<bias::ManyPowerLevels<double, 1, 1>> bias;
  double nmean = 1;

  auto comm = MPI_Communication::instance();
  std::unique_ptr<MPI_Communication> local_comm(comm->split(comm->rank()));

  auto generator = b_fused_idx<double, 3>(
      [](size_t i, size_t j, size_t k) -> double { return i + j + k; });

  ctx.print("Init density");
  LibLSS::copy_array(final_density_ref, generator);

  ctx.print("Init forward");
  auto model = std::make_shared<BorgLptModel<>>(
      local_comm.get(), box, box, false, 1, 2.0, 0.001, 1.0, false);

  ctx.print("Prepare bias");
  bias.prepare(
      *model, final_density_ref, nmean,
      std::array<double, decltype(bias)::Levels::numParams>{1, 1, 0, 1, 0, 0},
      true);

  ctx.print("Get biased density");
  auto const &out_density =
      std::get<0>(bias.compute_density(final_density_ref));

  ctx.print("Check values");
  for (size_t i = 0; i < N; i++) {
    for (size_t j = 0; j < N; j++) {
      for (size_t k = 0; k < N; k++) {
        double W = 0, V = 0;
        for (size_t r0 = 0; r0 < 2; r0++) {
          for (size_t r1 = 0; r1 < 2; r1++) {
            for (size_t r2 = 0; r2 < 2; r2++) {
              W += generator[2 * (i / 2) + r0][2 * (j / 2) + r1]
                            [2 * (k / 2) + r2];
            }
          }
        }
        W /= 8;
        auto x = generator[i][j][k];
        V = 1 + 2 * x + x * x + 2 * x * W + W * W + 2 * W;
        ctx.print("Got V = " + to_string(V) + " W = " + to_string(W));

        BOOST_CHECK_CLOSE(out_density[i][j][k], V, 1e-3);
      }
    }
  }

  ctx.print("Cleaning up");
  bias.cleanup();
}

int main(int argc, char **argv) {
  auto comm = setupMPI(argc, argv);
  StaticInit::execute();

  Console::instance().outputToFile(
      boost::str(boost::format("many_power_test.txt_%d") % comm->rank()));

  int ret = utf::unit_test_main(&init_unit_test, argc, argv);

  StaticInit::finalize();
  doneMPI();
  return ret;
}
