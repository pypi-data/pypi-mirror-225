/*+
    ARES/HADES/BORG Package -- ./libLSS/data/integer_window3d.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_MAJORITY_VOTE_WINDOW_3D_HPP
#define __LIBLSS_MAJORITY_VOTE_WINDOW_3D_HPP

#include <cassert>
#include <functional>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/openmp.hpp"
#include <CosmoTool/algo.hpp>
#include <boost/array.hpp>
#include <numeric>
#include <cmath>

namespace LibLSS {

  namespace internalIntegerWindow {

    template <typename SelFunction3d>
    unsigned int selectionValue(
        std::array<double, 3> const &x, SelFunction3d const &selfunc) {
      double r = std::sqrt(x[0] * x[0] + x[1] * x[1] + x[2] * x[2]);

      // *WARNING:* We use a sum here
      return selfunc.get_sky_completeness(x[0] / r, x[1] / r, x[2] / r) +
             selfunc.getRadialSelection(r, 0);
    }
  } // namespace internalIntegerWindow

  template <
      typename RandomNum, typename IntegerWindow, typename SelFunction3d,
      typename Dimension, typename IDimension>
  void computeMajorityVoteWindow3d(
      MPI_Communication *comm, RandomNum &rng, SelFunction3d const &selFuncData,
      IntegerWindow &selfunc, const Dimension &L, const Dimension &d,
      const Dimension &xmin, const IDimension &N, size_t numCalls = 6000) {
    LIBLSS_AUTO_CONTEXT2(LOG_INFO, ctx, "computeMajorityVoteWindow3d");
    using boost::format;
    using boost::str;

    boost::multi_array<int, 1> count_elements(
        boost::extents[LibLSS::smp_get_max_threads()]);
    size_t startN0 = selfunc.index_bases()[0];
    size_t localN0 = selfunc.shape()[0], N1 = N[1], N2 = N[2];
    double d0 = d[0];
    double d1 = d[1];
    double d2 = d[2];
    double xmin0 = xmin[0];
    double xmin1 = xmin[1];
    double xmin2 = xmin[2];
    size_t N0 = N[0];

    size_t calls = 10;

    auto &p = Console::instance().start_progress<LOG_STD>(
        "3D Integer Window", localN0 * N1 * N2, 2);

    ctx.format("Use %d calls integral / calls", numCalls);

    std::fill(count_elements.begin(), count_elements.end(), 0);

    long job_start = startN0 * N1 * N2;
    long job_end = (startN0 + localN0) * N1 * N2;

    ctx.format2<LOG_DEBUG>(
        "Window computation, MPI job_start=%ld job_end=%ld", job_start,
        job_end);
    ctx.format2<LOG_DEBUG>(
        "d=[%g,%g,%g], L=[%g,%g,%g]", d[0], d[1], d[2], L[0], L[1], L[2]);

    double dV = d0 * d1 * d2;

    typedef boost::multi_array_types::extent_range range;
    boost::multi_array<bool, 3> dummy(
        boost::extents[range(startN0, startN0 + localN0)][N1][N2]);
    boost::multi_array<double, 3> all_err(
        boost::extents[range(startN0, startN0 + localN0)][N1][N2]);

#pragma omp parallel
    {
      std::map<unsigned int, unsigned int> hitCount;
#pragma omp for schedule(dynamic, 100)
      for (size_t i = job_start; i < job_end; i++) {
        ///get 3d indices
        size_t ii = (size_t)(i / N1 / N2);
        size_t jj = (size_t)(i / N2 - ii * N1);
        size_t kk = (size_t)(i - jj * N2 - ii * N2 * N1);

        double x = double(ii) * d0 + xmin0, y = double(jj) * d1 + xmin1,
               z = double(kk) * d2 + xmin2;
        double err;
        std::array<double, 3> xl{x - 0.5 * d0, y - 0.5 * d1, z - 0.5 * d2}; // half voxel shift is for NGP in projection
        std::array<double, 3> xu{x + 0.5 * d0, y + 0.5 * d1, z + 0.5 * d2};

        hitCount.clear();
        for (size_t c = 0; c < numCalls; c++) {
          std::array<double, 3> x;
          for (unsigned int j = 0; j < 3; j++)
            x[j] = xl[j] + (xu[j] - xl[j]) * rng.uniform();

          hitCount[internalIntegerWindow::selectionValue(x, selFuncData)]++;
        }

        // Find majority vote
        selfunc[ii][jj][kk] = std::max_element(
                                  hitCount.begin(), hitCount.end(),
                                  [](auto const &x, auto const &y) {
                                    return x.second < y.second;
                                  })
                                  ->first;

        assert(LibLSS::smp_get_thread_id() < LibLSS::smp_get_max_threads());
        count_elements[LibLSS::smp_get_thread_id()]++;
        if (LibLSS::smp_get_thread_id() == 0) {
          int done =
              std::accumulate(count_elements.begin(), count_elements.end(), 0);
          p.update(done);
        }
      }
    }
    p.destroy();
  }
}; // namespace LibLSS

#endif
