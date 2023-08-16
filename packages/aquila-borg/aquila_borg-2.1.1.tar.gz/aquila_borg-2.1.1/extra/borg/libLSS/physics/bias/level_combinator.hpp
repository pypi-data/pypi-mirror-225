/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/bias/level_combinator.hpp
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2019-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_LEVEL_COMBINATOR_HPP
#  define __LIBLSS_LEVEL_COMBINATOR_HPP

#  include <cmath>
#  include <functional>
#  include <array>
#  include "libLSS/tools/fused_array.hpp"
#  include <tuple>
#  include "libLSS/tools/phoenix_vars.hpp"
#  include <boost/phoenix/operator.hpp>
#  include <boost/phoenix/stl/cmath.hpp>
#  include "libLSS/tools/tuple_helper.hpp"
#  include "libLSS/physics/bias/base.hpp"
#  include "libLSS/tools/mpi/ghost_planes.hpp"
#  include "libLSS/tools/array_tools.hpp"
#  include <boost/config.hpp>
#  include "libLSS/tools/string_tools.hpp"

namespace LibLSS {

  namespace Combinator {
    static constexpr bool ULTRA_VERBOSE = false;

    namespace ph = std::placeholders;

    // This a pow that works as a constant expression for all compilers.
    template <typename T>
    static inline constexpr T const_pow(T x, size_t p) {
      return p == 0 ? 1 : (x * const_pow(x, p - 1));
    }

    template <typename T, size_t... N>
    struct Levels;

    template <typename T>
    struct Levels<T> {
      static constexpr const int numParams = 1;
      static constexpr const int Nmax = 1;
      static constexpr const int numLevel = 0;
      typedef boost::multi_array_ref<T, 3> ArrayRef;

      template <size_t maxLevel, typename SomeArray>
      inline void get_density(
          std::array<double, maxLevel> &delta_out,
          SomeArray const &density_levels, size_t i, size_t j, size_t k) {}

      template <size_t level, typename SomeArray>
      inline double
      get_density_level(SomeArray const &, size_t i, size_t j, size_t k) {
        return 0.0;
      }

      template <size_t level, typename SomeArray>
      inline void
      push_ag_density_level(double, SomeArray &, size_t i, size_t j, size_t k) {
      }

      void allocate(
          size_t, size_t, size_t, size_t, size_t, size_t,
          std::tuple<ssize_t, ssize_t> * = 0) {}
      void clear_cache() {}

      template <size_t maxLevel>
      inline void push_ag_density(
          std::array<double, maxLevel> &ag_delta, ArrayRef &ag_density,
          size_t i, size_t j, size_t k) {}

      constexpr static inline size_t getPower(size_t) { return 0; }

      void get_requirement(std::vector<size_t> &) {}

      void ag_buildLevels(GhostPlanes<T, 2> &ghosts, ArrayRef &ag_density) {}
      void buildLevels(
          GhostPlanes<T, 2> &ghosts,
          boost::multi_array_ref<T, 3> const &final_density) {}
    };

    template <typename T, size_t thisN, size_t... N>
    struct Levels<T, thisN, N...> {
      typedef Levels<T, N...> PreviousLevels;
      typedef typename PreviousLevels::ArrayRef ArrayRef;
      PreviousLevels previousLevels;
      static constexpr const int Npower = thisN;
      static constexpr const int Nmax = thisN + PreviousLevels::Nmax;
      static constexpr const int numParams = Nmax * (Nmax + 1) / 2;
      static constexpr const int numLevel = PreviousLevels::numLevel + 1;

      size_t N0, N1, N2, N2real, startN0, localN0;

      std::vector<size_t> required_ghosts;
      boost::multi_array<T, 3> this_level_cache, ag_this_level_cache;

      constexpr static inline size_t getPower(size_t level) {
        return (level == numLevel) ? Npower : PreviousLevels::getPower(level);
      }

      void allocate(
          size_t N0_, size_t N1_, size_t N2_, size_t N2real_, size_t startN0_,
          size_t localN0_, std::tuple<ssize_t, ssize_t> *cache_bound = 0) {
        ConsoleContext<LOG_DEBUG> ctx(
            "allocate multi-level<" + to_string(numLevel) + ">");
        N0 = N0_;
        N1 = N1_;
        N2 = N2_;
        N2real = N2real_;
        startN0 = startN0_;
        localN0 = localN0_;

        constexpr size_t resolution = const_pow(2, numLevel - 1);
        if (numLevel > 1) {
          ssize_t start_cache, end_cache;

          if (cache_bound == 0) {
            start_cache = (startN0 >= resolution)
                              ? (startN0 - resolution + 1) / resolution
                              : 0;
            end_cache = (startN0 + localN0 + resolution - 1) / resolution;
          } else {
            std::tie(start_cache, end_cache) = *cache_bound;
          }
          if (ULTRA_VERBOSE) {
            ctx.print(
                "numLevel=" + to_string(numLevel) +
                " resolution=" + to_string(resolution));
            ctx.print(
                "start_cache=" + to_string(start_cache) +
                " end_cache=" + to_string(end_cache));
          }
          auto cache_ext =
              boost::extents[boost::multi_array_types::extent_range(
                  start_cache, end_cache)][N1 / resolution][N2 / resolution];
          this_level_cache.resize(cache_ext);
          ag_this_level_cache.resize(cache_ext);
        }
        previousLevels.allocate(
            N0, N1, N2, N2real, startN0, localN0,
            cache_bound == 0 ? 0 : (cache_bound + 1));
        if (numLevel > 1) {
          required_ghosts.clear();
          required_ghosts.reserve(resolution);
          size_t start_cache = this_level_cache.index_bases()[0];
          size_t end_cache = start_cache + this_level_cache.shape()[0];
          for (size_t i = start_cache; i < end_cache; i++)
            for (size_t q = 0; q < resolution; q++) {
              size_t plane = i * resolution + q;
              // We have boundary effect here.
              if (((plane < startN0) || (plane >= (startN0 + localN0))) &&
                  plane < N0)
                required_ghosts.push_back(plane);
            }
          if (ULTRA_VERBOSE)
            ctx.print(
                "Required ghost planes (N0=" + to_string(N0) +
                "): " + to_string(required_ghosts));
        }
      }

      void ag_buildLevels(GhostPlanes<T, 2> &ghosts, ArrayRef &ag_density) {
        ConsoleContext<LOG_DEBUG> ctx(
            "adjoint gradient multi-level<" + std::to_string(numLevel) + ">");

        // The top level has no need for that.
        if (numLevel == 1) {
          return;
        }

        size_t r = const_pow(2, numLevel - 1);
        double inv_r3 = 1.0 / (r * r * r);
        size_t finalN0 = startN0 + localN0;

        // We have to update ag_density with all the cached values of the
        // sub levels
        previousLevels.ag_buildLevels(ghosts, ag_density);

        size_t level_start = ag_this_level_cache.index_bases()[0];
        size_t level_end = level_start + ag_this_level_cache.shape()[0];
        ctx.print("Add contribution from the cache");
        for (size_t i = level_start; i < level_end; i++) {
          for (size_t j = 0; j < N1 / r; j++) {
            for (size_t k = 0; k < N2 / r; k++) {
              typename ArrayRef::element ag =
                  ag_this_level_cache[i][j][k] * inv_r3;
              Console::instance().c_assert(!std::isnan(ag), "AG is Nan  (0)");
              for (size_t a = 0; a < r; a++) {
                size_t n = r * i + a;
                if (n < startN0 || n >= finalN0)
                  continue;
                auto out_ag = ag_density[n];
                for (size_t b = 0; b < r; b++)
                  for (size_t c = 0; c < r; c++)
                    out_ag[r * j + b][r * k + c] += ag;
              }
            }
          }
        }

        // Now we need to update the ag ghost planes to propagate
        // the ag caches.
        ctx.print("Propagate to the ghost planes");
        for (auto other_plane : required_ghosts) {
          auto this_plane = ag_this_level_cache[other_plane / r];
          auto &g_plane = ghosts.ag_getPlane(other_plane);

          for (size_t j = 0; j < N1 / r; j++) {
            for (size_t k = 0; k < N2 / r; k++) {
              typename ArrayRef::element ag = this_plane[j][k] * inv_r3;
              // The first loop is implicit from the top-level one.
              // Explicit looping would be more complicated and involves extra
              // lookup.
              Console::instance().c_assert(!std::isnan(ag), "AG is Nan");
              for (size_t b = 0; b < r; b++)
                for (size_t c = 0; c < r; c++)
                  g_plane[r * j + b][r * k + c] += ag;
            }
          }
        }
      }

      void
      buildLevels(GhostPlanes<T, 2> &ghosts, ArrayRef const &final_density) {
        ConsoleContext<LOG_DEBUG> ctx(
            "precompute multi-level<" + std::to_string(numLevel) + ">");

        if (numLevel == 1)
          return; // Do nothing

        // First build the lower level (high resolution)
        previousLevels.buildLevels(ghosts, final_density);

        // This is redundnat. It is possible to use the information on previous Levels
        // to build this one.
        size_t level_start = this_level_cache.index_bases()[0];
        size_t level_final = level_start + this_level_cache.shape()[0];
        size_t r = const_pow(2, numLevel - 1);
        double inv_r3 = 1.0 / (r * r * r);
        array::fill(this_level_cache, 0);
        if (ULTRA_VERBOSE)
          ctx.print("Building cache, r = " + to_string(r));
// We do not collapse more than 3 because of the injection operation.
// FIXME: this code assumes that all the ranges have some divisible properties
//        We accept this for the moment but future might need a more General
//        scheme.
#  pragma omp parallel for collapse(3)
        for (size_t i = level_start; i < level_final; i++) {
          for (size_t j = 0; j < N1 / r; j++) {
            for (size_t k = 0; k < N2 / r; k++) {
              typename ArrayRef::element V = 0;
              for (size_t a = 0; a < r; a++) {
                size_t n = r * i + a;
                if (n < startN0 || n >= (startN0 + localN0))
                  continue;
                auto D = final_density[n];
                for (size_t b = 0; b < r; b++)
                  for (size_t c = 0; c < r; c++) {
                    V += D[r * j + b][k * r + c];
                    if (std::isnan(V)) {
                      ctx.format(
                          "Nan(%g) detected at %d,%d,%d", V, n, r * j + b,
                          k * r + c);
                      MPI_Communication::instance()->abort();
                    }
                  }
              }
              if (ULTRA_VERBOSE)
                ctx.print(
                    "Setting i,j,k=" +
                    to_string(std::array<size_t, 3>{i, j, k}) + " with " +
                    to_string(V));
              this_level_cache[i][j][k] = V * inv_r3;
            }
          }
        }

        if (ULTRA_VERBOSE)
          ctx.print(
              "Use ghosts plane \"" + LibLSS::to_string(required_ghosts) +
              "\"");
        for (auto other_plane : required_ghosts) {
          auto this_plane = this_level_cache[other_plane / r];
          auto &g_plane = ghosts.getPlane(other_plane);
#  pragma omp parallel for collapse(2)
          for (size_t j = 0; j < N1 / r; j++) {
            for (size_t k = 0; k < N2 / r; k++) {
              typename ArrayRef::element V = 0;
              for (size_t a = 0; a < r; a++)
                for (size_t b = 0; b < r; b++) {
                  V += g_plane[j * r + a][k * r + b];
                  if (std::isnan(V)) {
                    ctx.format(
                        "Nan detected at %d,%d,%d", other_plane, j * r + a,
                        k * r + b);
                    MPI_Communication::instance()->abort();
                  }
                }
              if (ULTRA_VERBOSE)
                ctx.print(
                    "Adding to i,j,k=" +
                    to_string(std::array<size_t, 3>{other_plane / r, j, k}) +
                    " with " + to_string(V));
              this_plane[j][k] += V * inv_r3;
            }
          }
        }
      }

      void clear_cache() {
        previousLevels.clear_cache();
        array::fill(ag_this_level_cache, 0);
      }

      void get_requirement(std::vector<size_t> &all_required_ghosts) {
        all_required_ghosts.insert(
            all_required_ghosts.end(), required_ghosts.begin(),
            required_ghosts.end());
        previousLevels.get_requirement(all_required_ghosts);
      }

      void setup(GhostPlanes<T, 2> &ghosts, MPI_Communication *comm) {
        std::vector<size_t> local_planes, all_required_planes;
        for (size_t j = startN0; j < startN0 + localN0; j++)
          local_planes.push_back(j);

        get_requirement(all_required_planes);

        ghosts.setup(
            comm, all_required_planes, local_planes,
            std::array<size_t, 2>{N1, N2real}, N0);
      }

      template <size_t maxLevel>
      inline void push_ag_density(
          std::array<double, maxLevel> &ag_delta, ArrayRef &ag_density,
          size_t i, size_t j, size_t k) {
        previousLevels.push_ag_density(ag_delta, ag_density, i, j, k);

        if (numLevel == 1) {
          // Only the top level updates the ag directly.
          ag_density[i][j][k] += ag_delta[0];
        } else {
          auto reduction = const_pow(2, numLevel - 1);
          size_t i_l = i / reduction;
          size_t j_l = j / reduction;
          size_t k_l = k / reduction;

          // All other levels go through the cache to update the ag later.
          ag_this_level_cache[i_l][j_l][k_l] += ag_delta[numLevel - 1];
        }
      }

      template <size_t level>
      inline void push_ag_density_level(
          double ag_delta, ArrayRef &ag_density, size_t i, size_t j, size_t k) {
        if (level == numLevel - 1) {
          if (level == 0)
            ag_density[i][j][k] += ag_delta;
          else
            ag_this_level_cache[i][j][k] += ag_delta;
        } else
          previousLevels.template push_ag_density_level<level>(
              ag_delta, ag_density, i, j, k);
      }

      template <size_t level>
      inline double get_density_level(
          ArrayRef const &final_density, size_t i, size_t j, size_t k) {
        if (level == numLevel - 1) {
          if (level == 0)
            return final_density[i][j][k];
          else
            return this_level_cache[i][j][k];
        } else {
          return previousLevels.template get_density_level<level>(
              final_density, i, j, k);
        }
      }

      template <size_t maxLevel>
      inline void get_density(
          std::array<double, maxLevel> &delta_out,
          ArrayRef const &final_density, size_t i, size_t j, size_t k) {
        previousLevels.get_density(delta_out, final_density, i, j, k);

        if (numLevel == 1) {
          delta_out[0] = final_density[i][j][k];
        } else {
          auto reduction = const_pow(2, numLevel - 1);
          size_t i_l = i / reduction;
          size_t j_l = j / reduction;
          size_t k_l = k / reduction;

          delta_out[numLevel - 1] = this_level_cache[i_l][j_l][k_l];
        }
      }

      inline size_t minPlaneRequest() {
        size_t reduction = const_pow(2, numLevel - 1);

        return reduction * (startN0 / reduction);
      }

      inline size_t maxPlaneRequest() {
        size_t reduction = const_pow(2, numLevel - 1);

        return reduction * ((startN0 + localN0) / reduction);
      }
    };
  } // namespace Combinator
} // namespace LibLSS

#endif
// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2019-2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: name(1) = Jens Jasche
// ARES TAG: year(1) = 2019-2020
// ARES TAG: email(1) = jens.jasche@fysik.su.se
