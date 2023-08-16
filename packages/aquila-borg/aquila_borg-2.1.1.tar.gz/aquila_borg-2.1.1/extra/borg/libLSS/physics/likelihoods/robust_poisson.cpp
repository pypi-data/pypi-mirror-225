/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/likelihoods/robust_poisson.cpp
    Copyright (C) 2018 Natalia Porqueres <natalia_porqueres@hotmail.com>
    Copyright (C) 2018 Doogesh Kodi Ramanah <ramanah@iap.fr>
    Copyright (C) 2018-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/physics/likelihoods/robust_poisson.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/tools/fusewrapper.hpp"

using namespace LibLSS;

void RobustPoissonLikelihood::setup(LikelihoodInfo const &info) {
  ConsoleContext<LOG_DEBUG> ctx("RobustPoissonLikelihood::setup");

  auto promised_color_map =
      Likelihood::getPromisedArray<long, 3>(info, Likelihood::COLOR_MAP);

  color_map = promised_color_map.get();

  auto const &grid =
      Likelihood::query<Likelihood::GridSize>(info, Likelihood::DATA_GRID);
  auto const &mpi_grid =
      Likelihood::query<Likelihood::GridSize>(info, Likelihood::MPI_GRID);

  startN0 = mpi_grid[0];
  endN0 = mpi_grid[1];

  N0 = grid[0];
  N1 = grid[1];
  N2 = grid[2];

  ctx.format("Full grid is %dx%dx%d", N0, N1, N2);

  using boost::extents;
  typedef boost::multi_array_types::extent_range range;
  auto a_extent = extents[range(startN0, endN0)][N1][N2];
  out_gradient_p =
      std::unique_ptr<U_GradientArray>(new U_GradientArray(a_extent));

  Nkeys = 0;
  N_colors = 0;

  promised_color_map.defer.ready([&]() {
    auto &cmap = *color_map;
    N_colors = fwrap(cmap).max() + 1;
    comm->all_reduce_t(MPI_IN_PLACE, &N_colors, 1, MPI_MAX);
    ctx.print(boost::format("Found Ncol=%d") % N_colors);
    ctx.format("colors: startN0=%d, endN0=%d", startN0, endN0);

    color_flat = std::make_shared<LibLSS::U_Array<FlatArray, 1>>(
        boost::extents[(endN0 - startN0) * N1 * N2]);

    /* Build a mapping between patch id and 3d-index */
    fwrap(*color_flat) = b_fused_idx<FlatArray, 1>([&](size_t idx) {
      uint16_t ib = idx / (N1 * N2);
      uint16_t i = ib + startN0;
      uint16_t j = (idx - ib * N1 * N2) / N2;
      uint16_t k = (idx - ib * N1 * N2 - j * N2);
      Console::instance().c_assert(
          idx == (k + j * N2 + ib * N1 * N2), "Inconsistency");
      Console::instance().c_assert(i < endN0, "Bad i");
      Console::instance().c_assert(j < N1, "Bad j");
      Console::instance().c_assert(k < N2, "Bad k");
      return std::make_tuple(Index3d{i, j, k}, cmap[i][j][k]);
    });

    auto &cflat = color_flat->get_array();
    size_t const Nelt = cflat.num_elements();
    /* Sort the mapping by patch id, only those present on the present node are considered */
    std::sort(
        &cflat[0], &cflat[Nelt - 1] + 1,
        [](FlatArray const &a, FlatArray const &b) {
          return std::get<1>(a) < std::get<1>(b);
        });

    key_shift =
        std::make_shared<U_Array<size_t, 1>>(boost::extents[N_colors + 1]);
    auto &ckey = key_shift->get_array();

    size_t location = 1;
    size_t key = std::get<1>(cflat[0]);
    /* Do a compressed representation, build an array indicating the start of each patch in the flattened
     * mapping.
     */
    ckey[0] = 0;
    for (size_t i = 1; i < Nelt; i++) {
      int32_t this_key = std::get<1>(cflat[i]);
      if (this_key != key) {
        Console::instance().c_assert(location <= N_colors, "Too many colors");
        ckey[location++] = i;
        key = this_key;
      }
    }
    Nkeys = location;
    // Add a last element for simplicity
    ckey[location] = Nelt;
    Console::instance().format<LOG_VERBOSE>(
        "Patches on this node: ckey[0] = %d, ckey[%d] = %d", ckey[0], Nkeys,
        ckey[Nkeys]);

    // Now we need to decide on MPI jobs
    // Build the set of the local colors
    std::set<int32_t> color_set;
    for (size_t i = 0; i < Nkeys; i++) {
      color_set.insert(std::get<1>(cflat[ckey[i]]));
    }

    ghost_colors.setup(comm, color_set);
  });
}

// ARES TAG: authors_num = 3
// ARES TAG: name(0) = Natalia Porqueres
// ARES TAG: name(1) = Doogesh Kodi Ramanah
// ARES TAG: name(2) = Guilhem Lavaux
// ARES TAG: name(3) = Jens Jasche
// ARES TAG: email(0) = natalia_porqueres@hotmail.com
// ARES TAG: email(1) = ramanah@iap.fr
// ARES TAG: email(2) = guilhem.lavaux@iap.fr
// ARES TAG: email(3) = jens.jasche@fysik.su.se
// ARES TAG: year(0) = 2018
// ARES TAG: year(1) = 2018
// ARES TAG: year(2) = 2018-2020
// ARES TAG: year(3) = 2018
