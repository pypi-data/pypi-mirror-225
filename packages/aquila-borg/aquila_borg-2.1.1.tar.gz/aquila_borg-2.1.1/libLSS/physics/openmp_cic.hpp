/*+
    ARES/HADES/BORG Package -- ./libLSS/physics/openmp_cic.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHYSICS_OPENMP_CIC_HPP
#define __LIBLSS_PHYSICS_OPENMP_CIC_HPP

#include <cmath>
#include "libLSS/tools/console.hpp"
#include <boost/multi_array.hpp>
#include <CosmoTool/omptl/omptl>
#include <CosmoTool/omptl/omptl_algorithm>
#include <iostream>
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/physics/generic_cic.hpp"

namespace LibLSS {

  template <typename T>
  struct OpenMPCloudInCell_impl {
    typedef T Type;
    // Number of extra planes required in case of MPI
    static const int MPI_PLANE_LEAKAGE = 1;
    typedef boost::multi_array<int, 1> ListArray;
    typedef boost::multi_array<int, 1> AtomicListArray;

    template <
        typename ParticleArray, typename ProjectionDensityArray,
        typename WeightArray, typename PeriodicFunction>
    static void projection(
        const ParticleArray &particles, ProjectionDensityArray &density, T Lx,
        T Ly, T Lz, size_t N0, size_t N1, size_t N2, const PeriodicFunction &p,
        const WeightArray &weight, size_t Np) {
      using boost::extents;

      ConsoleContext<LOG_DEBUG> ctx("OpenMP CIC projection");

      T inv_dx = N0 / Lx;
      T inv_dy = N1 / Ly;
      T inv_dz = N2 / Lz;

      typedef UninitializedArray<AtomicListArray> U_AtomicListArray;
      typedef UninitializedArray<ListArray> U_ListArray;
      U_AtomicListArray part_mesh_p(extents[long(N0) * long(N1) * long(N2)]);
      U_ListArray part_list_p(extents[Np]);
      U_AtomicListArray::array_type &part_mesh = part_mesh_p.get_array();
      U_ListArray::array_type &part_list = part_list_p.get_array();
      long Nmesh = part_mesh.num_elements();

      {
        ConsoleContext<LOG_DEBUG> ctx0("initialize arrays");
        array::fill(part_mesh, -1);
        array::fill(part_list, -1);
      }

      {
        ConsoleContext<LOG_DEBUG> ctx0("build mesh list");
// First build part -> mesh list
#pragma omp parallel for schedule(static)
        for (size_t i_part = 0; i_part < Np; i_part++) {

          T x = particles[i_part][0] * inv_dx;
          T y = particles[i_part][1] * inv_dy;
          T z = particles[i_part][2] * inv_dz;

          size_t ix = (size_t)std::floor(x);
          size_t iy = (size_t)std::floor(y);
          size_t iz = (size_t)std::floor(z);

          size_t idx = iz + N2 * iy + N2 * N1 * ix;

          int initial_elt =
              __atomic_exchange_n(&part_mesh[idx], i_part, __ATOMIC_RELAXED);
          if (initial_elt != -1) {
            part_list[i_part] = initial_elt;
          }
        }
      }

      {
        ConsoleContext<LOG_DEBUG> ctx0("reverse list");

        // We built the list in the incorrect order, reverse it as fast as we can
#pragma omp parallel for schedule(dynamic, 10000)
        for (size_t mid = 0; mid < Nmesh; mid++) {
          int current_part = part_mesh[mid];

          if (current_part >= 0) {
            int next_part = part_list[current_part];

            part_list[current_part] = -1;
            while (next_part != -1) {
              int p = part_list[next_part];
              part_list[next_part] = current_part;
              current_part = next_part;
              next_part = p;
            }
            part_mesh[mid] = current_part;
          }
        }
      }

      {
        ConsoleContext<LOG_DEBUG> ctx0("projection");

#pragma omp parallel
        {

          for (int looper0 = 0; looper0 < 2; looper0++) {
            for (int looper1 = 0; looper1 < 2; looper1++) {
              for (int looper2 = 0; looper2 < 2; looper2++) {

                int r[3] = {looper0, looper1, looper2};

#pragma omp barrier
#pragma omp for schedule(dynamic, 10000)
                for (long mid = 0; mid < Nmesh; mid++) {
                  int mz = mid % N2;
                  int my = (mid / N2) % N1;
                  int mx = (mid / (N2 * N1));
                  int i_part = part_mesh[mid];

                  T w = 0;

                  while (i_part != -1) {
                    T w0 = 1;
                    T x = particles[i_part][0] * inv_dx;
                    T y = particles[i_part][1] * inv_dy;
                    T z = particles[i_part][2] * inv_dz;
                    T qx = std::floor(x);
                    T qy = std::floor(y);
                    T qz = std::floor(z);
                    T dx = x - qx;
                    T dy = y - qy;
                    T dz = z - qz;
                    w0 = (r[0] == 1) ? dx : (T(1) - dx);
                    w0 *= (r[1] == 1) ? dy : (T(1) - dy);
                    w0 *= (r[2] == 1) ? dz : (T(1) - dz);
                    w += w0 * weight[i_part];
                    i_part = part_list[i_part];
                  }

                  size_t tx = (mx + looper0);
                  size_t ty = (my + looper1);
                  size_t tz = (mz + looper2);
                  p(tx, ty, tz);
                  density[tx][ty][tz] += w;
                }
              }
            }
          }
        }
#pragma omp barrier
      }
    }

    template <
        typename GradientArray, typename ProjectionDensityArray,
        typename WeightArray>
    static inline
        typename std::enable_if<WeightArray::dimensionality == 1>::type
        __do_gradient(
            GradientArray &adj_gradient, const ProjectionDensityArray &density,
            WeightArray const &a_w, size_t i, int axis, size_t ix, size_t iy,
            size_t iz, size_t jx, size_t jy, size_t jz, T x, T y, T z,
            T global_w) {
      T rx, ry, rz;
      T qx, qy, qz;

      switch (axis) {
      case 0:
        rx = 1;
        qx = -1;
        ry = y - iy;
        qy = 1 - ry;
        rz = z - iz;
        qz = 1 - rz;
        break;
      case 1:
        rx = x - ix;
        qx = 1 - rx;
        ry = 1;
        qy = -1;
        rz = z - iz;
        qz = 1 - rz;
        break;
      case 2:
        rx = x - ix;
        qx = 1 - rx;
        ry = y - iy;
        qy = 1 - ry;
        rz = 1;
        qz = -1;
        break;
      }

      double w = density[ix][iy][iz] * qx * qy * qz +
                 density[ix][iy][jz] * qx * qy * rz +
                 density[ix][jy][iz] * qx * ry * qz +
                 density[ix][jy][jz] * qx * ry * rz +
                 density[jx][iy][iz] * rx * qy * qz +
                 density[jx][iy][jz] * rx * qy * rz +
                 density[jx][jy][iz] * rx * ry * qz +
                 density[jx][jy][jz] * rx * ry * rz;

      adj_gradient[i][axis] = a_w[axis] * w * global_w;
    }

    template <typename GradientArray, typename ProjectionDensityArray>
    static inline void __do_gradient(
        GradientArray &adj_gradient, const ProjectionDensityArray &density,
        T a_w, size_t i, int axis, size_t ix, size_t iy, size_t iz, size_t jx,
        size_t jy, size_t jz, T x, T y, T z, T global_w) {
      T rx, ry, rz;
      T qx, qy, qz;

      switch (axis) {
      case 0:
        rx = 1;
        qx = -1;
        ry = y - iy;
        qy = 1 - ry;
        rz = z - iz;
        qz = 1 - rz;
        break;
      case 1:
        rx = x - ix;
        qx = 1 - rx;
        ry = 1;
        qy = -1;
        rz = z - iz;
        qz = 1 - rz;
        break;
      case 2:
        rx = x - ix;
        qx = 1 - rx;
        ry = y - iy;
        qy = 1 - ry;
        rz = 1;
        qz = -1;
        break;
      }

      double w = density[ix][iy][iz] * qx * qy * qz +
                 density[ix][iy][jz] * qx * qy * rz +
                 density[ix][jy][iz] * qx * ry * qz +
                 density[ix][jy][jz] * qx * ry * rz +
                 density[jx][iy][iz] * rx * qy * qz +
                 density[jx][iy][jz] * rx * qy * rz +
                 density[jx][jy][iz] * rx * ry * qz +
                 density[jx][jy][jz] * rx * ry * rz;

      adj_gradient[i][axis] += a_w * w * global_w;
    }

    template <
        typename ParticleArray, typename ProjectionDensityArray,
        typename GradientArray, typename PeriodicFunction, typename WeightArray>
    static void adjoint(
        const ParticleArray &particles, ProjectionDensityArray &density,
        GradientArray &adjoint_gradient, const WeightArray &w, T Lx, T Ly, T Lz,
        size_t N0, size_t N1, size_t N2, const PeriodicFunction &p, T nmean,
        size_t Np) {
      ConsoleContext<LOG_DEBUG> ctx("Classic CIC adjoint-projection");

      T inv_dx = N0 / Lx;
      T inv_dy = N1 / Ly;
      T inv_dz = N2 / Lz;
      T inv_nmean = 1 / nmean;
      size_t minX = density.index_bases()[0], minY = density.index_bases()[1],
             minZ = density.index_bases()[2],
             maxX = density.index_bases()[0] + density.shape()[0],
             maxY = density.index_bases()[1] + density.shape()[1],
             maxZ = density.index_bases()[2] + density.shape()[2];

#pragma omp parallel for schedule(static)
      for (long i = 0; i < Np; i++) {

        T x = particles[i][0] * inv_dx;
        T y = particles[i][1] * inv_dy;
        T z = particles[i][2] * inv_dz;

        size_t ix = (size_t)std::floor(x);
        size_t iy = (size_t)std::floor(y);
        size_t iz = (size_t)std::floor(z);

        size_t jx = (ix + 1);
        size_t jy = (iy + 1);
        size_t jz = (iz + 1);

        p(jx, jy, jz);

        if (ix < minX || ix >= maxX || iy < minY || iy >= maxY || iz < minZ ||
            iz >= maxZ)
          continue;

        __do_gradient(
            adjoint_gradient, density, w[i], i, 0, ix, iy, iz, jx, jy, jz, x, y,
            z, inv_dx * inv_nmean);
        __do_gradient(
            adjoint_gradient, density, w[i], i, 1, ix, iy, iz, jx, jy, jz, x, y,
            z, inv_dy * inv_nmean);
        __do_gradient(
            adjoint_gradient, density, w[i], i, 2, ix, iy, iz, jx, jy, jz, x, y,
            z, inv_dz * inv_nmean);
      }
    }
  };

  template <typename T>
  class OpenMPCloudInCell : public GenericCIC<T, OpenMPCloudInCell_impl<T>> {
  public:
    typedef T Type;
    // Number of extra planes required in case of MPI
    static const int MPI_PLANE_LEAKAGE = 1;
    static const int MPI_NEGATIVE_PLANE_LEAKAGE = 0;
    typedef CIC_Distribution<T> Distribution;
    typedef CIC_Tools::Periodic_MPI Periodic_MPI;
  };

} // namespace LibLSS

#endif
