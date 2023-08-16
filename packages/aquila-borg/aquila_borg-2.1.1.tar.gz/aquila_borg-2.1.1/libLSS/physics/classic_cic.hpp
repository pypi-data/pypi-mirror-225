/*+
    ARES/HADES/BORG Package -- ./libLSS/physics/classic_cic.hpp
    Copyright (C) 2009-2019 Jens Jasche <jens.jasche@fysik.su.se>
    Copyright (C) 2014-2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2019 Florent Leclercq <florent.leclercq@polytechnique.org>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHYSICS_CLASSIC_CIC_HPP
#  define __LIBLSS_PHYSICS_CLASSIC_CIC_HPP

#  include <cmath>
#  include "libLSS/tools/console.hpp"
#  include <boost/multi_array.hpp>
#  include "libLSS/physics/generic_cic.hpp"
#  include "libLSS/tools/mpi_fftw_helper.hpp"
#  include <memory>

namespace LibLSS {

  template <typename T, bool ignore_overflow>
  struct ClassicCloudInCell_impl {
    typedef T Type;
    // Number of extra planes required in case of MPI
    static const int MPI_PLANE_LEAKAGE = 1;
    static const bool EXTRA_CHECK = true;
    typedef boost::multi_array<T, 3> DensityArray;
    typedef boost::multi_array_ref<T, 1> ParticleBasedScalar;
    typedef boost::multi_array_ref<T, 2> ParticleBasedArray;

    template <typename A>
    static inline void _safe_set(
        A &&density, size_t const ix, size_t const iy, size_t const iz,
        size_t const bounds[3][2], T const &value) {
      if (ix >= bounds[0][0] && ix < bounds[0][1] && iy >= bounds[1][0] &&
          iy < bounds[1][1] && iz >= bounds[2][0] && iz < bounds[2][1]) {
        density[ix][iy][iz] += value;
      } else {
      }
    } //_safe_set

    template <
        typename ParticleArray, typename ProjectionDensityArray,
        typename WeightArray, typename PeriodicFunction>
    static typename std::enable_if<WeightArray::dimensionality == 1>::type
    projection(
        const ParticleArray &particles, ProjectionDensityArray &density, T Lx,
        T Ly, T Lz, int N0, int N1, int N2, const PeriodicFunction &p,
        const WeightArray &weight, size_t Np) {
      ConsoleContext<LOG_DEBUG> ctx("Classic CIC projection");

      T inv_dx = N0 / Lx;
      T inv_dy = N1 / Ly;
      T inv_dz = N2 / Lz;
      size_t minX = density.index_bases()[0];
      size_t minY = density.index_bases()[1];
      size_t minZ = density.index_bases()[2];
      size_t maxX = density.index_bases()[0] + density.shape()[0];
      size_t maxY = density.index_bases()[1] + density.shape()[1];
      size_t maxZ = density.index_bases()[2] + density.shape()[2];

      ctx.print(boost::format("minX=%d, maxX=%d, N0=%d") % minX % maxX % N0);

      size_t const bounds[3][2] = {{minX, maxX}, {minY, maxY}, {minZ, maxZ}};
      for (long i = 0; i < Np; i++) {

        T x = particles[i][0] * inv_dx;
        T y = particles[i][1] * inv_dy;
        T z = particles[i][2] * inv_dz;

        size_t ix = (size_t)std::floor(x);
        size_t iy = (size_t)std::floor(y);
        size_t iz = (size_t)std::floor(z);

        size_t jx = ix + 1;
        size_t jy = (iy + 1);
        size_t jz = (iz + 1);

        p(jx, jy, jz);

        T rx = (x - ix);
        T ry = (y - iy);
        T rz = (z - iz);

        T qx = 1 - rx;
        T qy = 1 - ry;
        T qz = 1 - rz;

        double w = weight[i];

        if (!ignore_overflow) {
          if (jx >= maxX) {
            Console::instance().print<LOG_ERROR>(
                boost::format(
                    "Overflow at ix=%d, jx=%d (maxX=%d), x=%g, rx=%g, qx=%g") %
                ix % jx % maxX % x % rx % qx);
          }
          if (ix < minX) {
            Console::instance().print<LOG_ERROR>(
                boost::format("Underflow at ix=%d, jx=%d") % ix % jx);
          }
          if (jy >= maxY) {
            Console::instance().print<LOG_ERROR>(
                boost::format("Overflow at iy=%d, jy=%d (maxY=%d)") % iy % jy %
                maxY);
          }
          if (iy < minY) {
            Console::instance().print<LOG_ERROR>(
                boost::format("Underflow at iy=%d, jy=%d") % iy % jy);
          }
          density[ix][iy][iz] += (qx) * (qy) * (qz)*w;
          density[ix][iy][jz] += (qx) * (qy) * (rz)*w;
          density[ix][jy][iz] += (qx) * (ry) * (qz)*w;
          density[ix][jy][jz] += (qx) * (ry) * (rz)*w;
          density[jx][iy][iz] += (rx) * (qy) * (qz)*w;
          density[jx][iy][jz] += (rx) * (qy) * (rz)*w;
          density[jx][jy][iz] += (rx) * (ry) * (qz)*w;
          density[jx][jy][jz] += (rx) * (ry) * (rz)*w;

        } else {

          _safe_set(density, ix, iy, iz, bounds, qx * qy * qz * w);
          _safe_set(density, ix, iy, jz, bounds, qx * qy * rz * w);
          _safe_set(density, ix, jy, iz, bounds, qx * ry * qz * w);
          _safe_set(density, ix, jy, jz, bounds, qx * ry * rz * w);

          _safe_set(density, jx, iy, iz, bounds, rx * qy * qz * w);
          _safe_set(density, jx, iy, jz, bounds, rx * qy * rz * w);
          _safe_set(density, jx, jy, iz, bounds, rx * ry * qz * w);
          _safe_set(density, jx, jy, jz, bounds, rx * ry * rz * w);
        }
      }
    } //projection

    template <
        typename ParticleArray, typename ProjectionDensityArray,
        typename WeightArray, typename PeriodicFunction>
    static typename std::enable_if<WeightArray::dimensionality != 1>::type
    projection(
        const ParticleArray &particles, ProjectionDensityArray &density, T Lx,
        T Ly, T Lz, int N0, int N1, int N2, const PeriodicFunction &p,
        const WeightArray &weight, size_t Np) {
      ConsoleContext<LOG_DEBUG> ctx("Classic CIC projection");

      T inv_dx = N0 / Lx;
      T inv_dy = N1 / Ly;
      T inv_dz = N2 / Lz;
      size_t minX = density.index_bases()[1];
      size_t minY = density.index_bases()[2];
      size_t minZ = density.index_bases()[3];
      size_t maxX = density.index_bases()[1] + density.shape()[1];
      size_t maxY = density.index_bases()[2] + density.shape()[2];
      size_t maxZ = density.index_bases()[3] + density.shape()[3];

      ctx.print(boost::format("minX=%d, maxX=%d, N0=%d") % minX % maxX % N0);

      unsigned int dims = weight.shape()[1];
      size_t const bounds[3][2] = {{minX, maxX}, {minY, maxY}, {minZ, maxZ}};
      for (size_t i = 0; i < Np; i++) {

        T x = particles[i][0] * inv_dx;
        T y = particles[i][1] * inv_dy;
        T z = particles[i][2] * inv_dz;

        size_t ix = (size_t)std::floor(x);
        size_t iy = (size_t)std::floor(y);
        size_t iz = (size_t)std::floor(z);

        size_t jx = ix + 1;
        size_t jy = (iy + 1);
        size_t jz = (iz + 1);

        p(jx, jy, jz);

        T rx = (x - ix);
        T ry = (y - iy);
        T rz = (z - iz);

        T qx = 1 - rx;
        T qy = 1 - ry;
        T qz = 1 - rz;

        if (!ignore_overflow) {
          if (jx >= maxX) {
            Console::instance().print<LOG_ERROR>(
                boost::format("Overflow at ix=%d, jx=%d (maxX=%d)") % ix % jx %
                maxX);
          }
          if (ix < minX) {
            Console::instance().print<LOG_ERROR>(
                boost::format("Underflow at ix=%d, jx=%d") % ix % jx);
          }
          if (jy >= maxY) {
            Console::instance().print<LOG_ERROR>(
                boost::format("Overflow at iy=%d, jy=%d (maxY=%d)") % iy % jy %
                maxY);
          }
          if (iy < minY) {
            Console::instance().print<LOG_ERROR>(
                boost::format("Underflow at iy=%d, jy=%d") % iy % jy);
          }

          for (unsigned int k = 0; k < dims; k++) {
            T w = weight[i][k];

            density[k][ix][iy][iz] += (qx) * (qy) * (qz)*w;
            density[k][ix][iy][jz] += (qx) * (qy) * (rz)*w;
            density[k][ix][jy][iz] += (qx) * (ry) * (qz)*w;
            density[k][ix][jy][jz] += (qx) * (ry) * (rz)*w;
            density[k][jx][iy][iz] += (rx) * (qy) * (qz)*w;
            density[k][jx][iy][jz] += (rx) * (qy) * (rz)*w;
            density[k][jx][jy][iz] += (rx) * (ry) * (qz)*w;
            density[k][jx][jy][jz] += (rx) * (ry) * (rz)*w;
          }
        } else {

          for (int k = 0; k < dims; k++) {
            T w = weight[i][k];

            _safe_set(density[k], ix, iy, iz, bounds, qx * qy * qz * w);
            _safe_set(density[k], ix, iy, jz, bounds, qx * qy * rz * w);
            _safe_set(density[k], ix, jy, iz, bounds, qx * ry * qz * w);
            _safe_set(density[k], ix, jy, jz, bounds, qx * ry * rz * w);

            _safe_set(density[k], jx, iy, iz, bounds, rx * qy * qz * w);
            _safe_set(density[k], jx, iy, jz, bounds, rx * qy * rz * w);
            _safe_set(density[k], jx, jy, iz, bounds, rx * ry * qz * w);
            _safe_set(density[k], jx, jy, jz, bounds, rx * ry * rz * w);
          }
        }
      }
    } //projection

    template <
        typename ParticleBasedScalar, typename ProjectionDensityArray,
        typename WeightArray>
    static inline
        typename std::enable_if<WeightArray::dimensionality == 1>::type
        __do_interpolation(
            ParticleBasedScalar &A, const ProjectionDensityArray &field,
            const WeightArray &weight, size_t i, T qx, T qy, T qz, T rx, T ry,
            T rz, size_t ix, size_t iy, size_t iz, size_t jx, size_t jy,
            size_t jz) {
      T f1 = 1. * qx * qy * qz;
      T f2 = 1. * rx * qy * qz;
      T f3 = 1. * qx * ry * qz;
      T f4 = 1. * qx * qy * rz;
      T f5 = 1. * rx * ry * qz;
      T f6 = 1. * rx * qy * rz;
      T f7 = 1. * qx * ry * rz;
      T f8 = 1. * rx * ry * rz;
      double w = weight[i];

      A[i] = (field[ix][iy][iz] * f1 + field[jx][iy][iz] * f2 +
              field[ix][jy][iz] * f3 + field[ix][iy][jz] * f4 +
              field[jx][jy][iz] * f5 + field[jx][iy][jz] * f6 +
              field[ix][jy][jz] * f7 + field[jx][jy][jz] * f8) /
             w;
    } //__do_interpolation

    template <
        typename ParticleBasedScalar, typename ParticleArray,
        typename ProjectionDensityArray, typename WeightArray,
        typename PeriodicFunction>
    static typename std::enable_if<WeightArray::dimensionality == 1>::type
    interpolation_scalar(
        ParticleBasedScalar &A, const ParticleArray &particles,
        const ProjectionDensityArray &field, T Lx, T Ly, T Lz, int N0, int N1,
        int N2, const PeriodicFunction &p, const WeightArray &weight,
        size_t Np) {
      ConsoleContext<LOG_DEBUG> ctx("Classic CIC interpolation");

      T inv_dx = N0 / Lx;
      T inv_dy = N1 / Ly;
      T inv_dz = N2 / Lz;
      size_t minX = field.index_bases()[0];
      size_t minY = field.index_bases()[1];
      size_t minZ = field.index_bases()[2];
      size_t maxX = field.index_bases()[0] + field.shape()[0];
      size_t maxY = field.index_bases()[1] + field.shape()[1];
      size_t maxZ = field.index_bases()[2] + field.shape()[2];

      ctx.print(boost::format("minX=%d, maxX=%d, N0=%d") % minX % maxX % N0);

      size_t const bounds[3][2] = {{minX, maxX}, {minY, maxY}, {minZ, maxZ}};
#  pragma omp parallel for schedule(static)
      for (long i = 0; i < Np; i++) {

        T x = particles[i][0] * inv_dx;
        T y = particles[i][1] * inv_dy;
        T z = particles[i][2] * inv_dz;

        size_t ix = (size_t)std::floor(x);
        size_t iy = (size_t)std::floor(y);
        size_t iz = (size_t)std::floor(z);

        size_t jx = ix + 1;
        size_t jy = (iy + 1);
        size_t jz = (iz + 1);

        p(jx, jy, jz);

        T rx = (x - ix);
        T ry = (y - iy);
        T rz = (z - iz);

        T qx = 1 - rx;
        T qy = 1 - ry;
        T qz = 1 - rz;

        if (jx >= maxX) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Overflow at ix=%d, jx=%d (maxX=%d)") % ix % jx %
              maxX);
          MPI_Communication::instance()->abort();
        }
        if (ix < minX) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Underflow at ix=%d, jx=%d") % ix % jx);
          MPI_Communication::instance()->abort();
        }
        if (jy >= maxY) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Overflow at iy=%d, jy=%d (maxY=%d)") % iy % jy %
              maxY);
          MPI_Communication::instance()->abort();
        }
        if (iy < minY) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Underflow at iy=%d, jy=%d") % iy % jy);
          MPI_Communication::instance()->abort();
        }

        __do_interpolation(
            A, field, weight, i, qx, qy, qz, rx, ry, rz, ix, iy, iz, jx, jy,
            jz);
      }
    } //interpolation

    template <
        typename ParticleBasedArray, typename ProjectionDensityArray,
        typename WeightArray>
    static inline
        typename std::enable_if<WeightArray::dimensionality != 1>::type
        __do_interpolation_vec(
            ParticleBasedArray &A, const ProjectionDensityArray &field,
            const WeightArray &weight, size_t i, T qx, T qy, T qz, T rx, T ry,
            T rz, size_t ix, size_t iy, size_t iz, size_t jx, size_t jy,
            size_t jz) {
      T f1 = 1. * qx * qy * qz;
      T f2 = 1. * rx * qy * qz;
      T f3 = 1. * qx * ry * qz;
      T f4 = 1. * qx * qy * rz;
      T f5 = 1. * rx * ry * qz;
      T f6 = 1. * rx * qy * rz;
      T f7 = 1. * qx * ry * rz;
      T f8 = 1. * rx * ry * rz;
      unsigned int dims = A.shape()[1];

      for (unsigned int k = 0; k < dims; k++) {
        T w = weight[i][k];

        A[i][k] = (field[k][ix][iy][iz] * f1 + field[k][jx][iy][iz] * f2 +
                   field[k][ix][jy][iz] * f3 + field[k][ix][iy][jz] * f4 +
                   field[k][jx][jy][iz] * f5 + field[k][jx][iy][jz] * f6 +
                   field[k][ix][jy][jz] * f7 + field[k][jx][jy][jz] * f8) /
                  w;
      }
    } //__do_interpolation_vec

    template <
        typename ParticleBasedArray, typename ParticleArray,
        typename ProjectionDensityArray, typename WeightArray,
        typename PeriodicFunction>
    static typename std::enable_if<WeightArray::dimensionality != 1>::type
    interpolation(
        ParticleBasedArray &A, const ParticleArray &particles,
        const ProjectionDensityArray &field, T Lx, T Ly, T Lz, int N0, int N1,
        int N2, const PeriodicFunction &p, const WeightArray &weight,
        size_t Np) {
      ConsoleContext<LOG_DEBUG> ctx("Classic CIC interpolation");

      T inv_dx = N0 / Lx;
      T inv_dy = N1 / Ly;
      T inv_dz = N2 / Lz;
      size_t minX = field.index_bases()[1];
      size_t minY = field.index_bases()[2];
      size_t minZ = field.index_bases()[3];
      size_t maxX = field.index_bases()[1] + field.shape()[1];
      size_t maxY = field.index_bases()[2] + field.shape()[2];
      size_t maxZ = field.index_bases()[3] + field.shape()[3];

      ctx.print(boost::format("minX=%d, maxX=%d, N0=%d") % minX % maxX % N0);

      size_t const bounds[3][2] = {{minX, maxX}, {minY, maxY}, {minZ, maxZ}};
#  pragma omp parallel for schedule(static)
      for (size_t i = 0; i < Np; i++) {

        T x = particles[i][0] * inv_dx;
        T y = particles[i][1] * inv_dy;
        T z = particles[i][2] * inv_dz;

        size_t ix = (size_t)std::floor(x);
        size_t iy = (size_t)std::floor(y);
        size_t iz = (size_t)std::floor(z);

        size_t jx = ix + 1;
        size_t jy = (iy + 1);
        size_t jz = (iz + 1);

        p(jx, jy, jz);

        T rx = (x - ix);
        T ry = (y - iy);
        T rz = (z - iz);

        T qx = 1 - rx;
        T qy = 1 - ry;
        T qz = 1 - rz;

        if (jx >= maxX) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Overflow at ix=%d, jx=%d (maxX=%d)") % ix % jx %
              maxX);
          MPI_Communication::instance()->abort();
        }
        if (ix < minX) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Underflow at ix=%d, jx=%d") % ix % jx);
          MPI_Communication::instance()->abort();
        }
        if (jy >= maxY) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Overflow at iy=%d, jy=%d (maxY=%d)") % iy % jy %
              maxY);
          MPI_Communication::instance()->abort();
        }
        if (iy < minY) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Underflow at iy=%d, jy=%d") % iy % jy);
          MPI_Communication::instance()->abort();
        }

        __do_interpolation_vec(
            A, field, weight, i, qx, qy, qz, rx, ry, rz, ix, iy, iz, jx, jy,
            jz);
      }
    } //interpolation

    template <
        typename GradientArray, typename ProjectionDensityArray,
        typename WeightArray>
    static inline
        typename std::enable_if<WeightArray::dimensionality == 1>::type
        __do_gradient(
            GradientArray &adj_gradient, const ProjectionDensityArray &density,
            const WeightArray &weight, size_t i, int axis, int ix, int iy,
            int iz, int jx, int jy, int jz, T x, T y, T z, T global_w) {
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

      adj_gradient[i][axis] += w * global_w;
    } //__do_gradient

    template <
        typename ParticleArray, typename GradientArray,
        typename ProjectionDensityArray, typename PeriodicFunction,
        typename WeightArray>
    static typename std::enable_if<WeightArray::dimensionality == 1>::type
    adjoint(
        const ParticleArray &particles, ProjectionDensityArray &density,
        GradientArray &adjoint_gradient, const WeightArray &weight, T Lx, T Ly,
        T Lz, int N0, int N1, int N2, const PeriodicFunction &p, T nmean,
        size_t Np) {
      ConsoleContext<LOG_DEBUG> ctx("Classic CIC adjoint-projection");

      T inv_dx = N0 / Lx;
      T inv_dy = N1 / Ly;
      T inv_dz = N2 / Lz;
      T inv_nmean = T(1) / nmean;
      size_t minX = density.index_bases()[0];
      size_t minY = density.index_bases()[1];
      size_t minZ = density.index_bases()[2];
      size_t maxX = minX + density.shape()[0];
      size_t maxY = minY + density.shape()[1];
      size_t maxZ = minZ + density.shape()[2];

      ctx.print(
          boost::format(
              "Number of particles = %d (array is %d), minX=%d maxX=%d") %
          Np % particles.shape()[0] % minX % maxX);
      ctx.print(
          boost::format("Adjoint gradient = %d") % adjoint_gradient.shape()[0]);

#  pragma omp parallel for schedule(static)
      for (size_t i = 0; i < Np; i++) {

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

        if (ignore_overflow) {
          error_helper<ErrorBadState>("Overflow cannot be ignored in adjoint.");
        }

        if (EXTRA_CHECK && jx >= maxX) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Overflow at ix=%d, jx=%d (maxX adj = %d)") % ix %
              jx % maxX);
        }
        if (EXTRA_CHECK && ix < minX) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Underflow at ix=%d, jx=%d (adj)") % ix % jx);
        }
        if (EXTRA_CHECK && jy >= maxY) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Overflow at iy=%d, jy=%d (maxY=%d) adj") % iy %
              jy % maxY);
        }
        if (EXTRA_CHECK && iy < minY) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Underflow at iy=%d, jy=%d adj") % iy % jy);
        }
        if (EXTRA_CHECK && jz >= maxZ) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Overflow at iz=%d, jz=%d (maxZ=%d) adj") % iz %
              jz % maxZ);
        }
        if (EXTRA_CHECK && iz < minZ) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Underflow at iz=%d, jz=%d adj") % iz % jz);
        }

        __do_gradient(
            adjoint_gradient, density, weight[i], i, 0, ix, iy, iz, jx, jy, jz,
            x, y, z, inv_nmean * inv_dx);
        __do_gradient(
            adjoint_gradient, density, weight[i], i, 1, ix, iy, iz, jx, jy, jz,
            x, y, z, inv_nmean * inv_dy);
        __do_gradient(
            adjoint_gradient, density, weight[i], i, 2, ix, iy, iz, jx, jy, jz,
            x, y, z, inv_nmean * inv_dz);
      }
    } //adjoint

    template <typename GradientArray, typename ProjectionDensityArray>
    static inline void __do_gradient(
        GradientArray &adj_gradient, const ProjectionDensityArray &density,
        double weight, size_t i, int axis, int ix, int iy, int iz, int jx,
        int jy, int jz, T x, T y, T z, T global_w) {
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

      adj_gradient[i][axis] = w * global_w * weight;
    } //__do_gradient

    template <
        typename GradientArray, typename ProjectionDensityArray,
        typename WeightElement>
    static inline void __do_gradient_vec(
        GradientArray &adj_gradient, const ProjectionDensityArray &density,
        WeightElement const &weight, size_t i, int axis, int ix, int iy, int iz,
        int jx, int jy, int jz, T x, T y, T z, T global_w) {
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

      unsigned int dims = weight.shape()[1];

      adj_gradient[i][axis] = 0.;
      for (unsigned int k = 0; k < dims; k++) {
        double w = density[k][ix][iy][iz] * qx * qy * qz +
                   density[k][ix][iy][jz] * qx * qy * rz +
                   density[k][ix][jy][iz] * qx * ry * qz +
                   density[k][ix][jy][jz] * qx * ry * rz +
                   density[k][jx][iy][iz] * rx * qy * qz +
                   density[k][jx][iy][jz] * rx * qy * rz +
                   density[k][jx][jy][iz] * rx * ry * qz +
                   density[k][jx][jy][jz] * rx * ry * rz;

        adj_gradient[i][axis] += w * global_w * weight[k];
      }
    } //__do_gradient_vec

    template <
        typename ParticleArray, typename GradientArray,
        typename ProjectionDensityArray, typename PeriodicFunction,
        typename WeightArray>
    static typename std::enable_if<WeightArray::dimensionality != 1>::type
    adjoint(
        const ParticleArray &particles, ProjectionDensityArray &density,
        GradientArray &adjoint_gradient, const WeightArray &weight, T Lx, T Ly,
        T Lz, int N0, int N1, int N2, const PeriodicFunction &p, T nmean,
        size_t Np) {
      ConsoleContext<LOG_DEBUG> ctx("Classic CIC adjoint-projection");

      T inv_dx = N0 / Lx;
      T inv_dy = N1 / Ly;
      T inv_dz = N2 / Lz;
      T inv_nmean = T(1) / nmean;
      size_t minX = density.index_bases()[0];
      size_t minY = density.index_bases()[1];
      size_t minZ = density.index_bases()[2];
      size_t maxX = minX + density.shape()[0];
      size_t maxY = minY + density.shape()[1];
      size_t maxZ = minZ + density.shape()[2];

      ctx.print(
          boost::format(
              "Number of particles = %d (array is %d), minX=%d maxX=%d") %
          Np % particles.shape()[0] % minX % maxX);
      ctx.print(
          boost::format("Adjoint gradient = %d") % adjoint_gradient.shape()[0]);

#  pragma omp parallel for schedule(static)
      for (size_t i = 0; i < Np; i++) {

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

        if (ignore_overflow) {
          error_helper<ErrorBadState>("Overflow cannot be ignored in adjoint.");
        }

        if (EXTRA_CHECK && jx >= maxX) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Overflow at ix=%d, jx=%d (maxX adj = %d)") % ix %
              jx % maxX);
        }
        if (EXTRA_CHECK && ix < minX) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Underflow at ix=%d, jx=%d (adj)") % ix % jx);
        }
        if (EXTRA_CHECK && jy >= maxY) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Overflow at iy=%d, jy=%d (maxY=%d) adj") % iy %
              jy % maxY);
        }
        if (EXTRA_CHECK && iy < minY) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Underflow at iy=%d, jy=%d adj") % iy % jy);
        }
        if (EXTRA_CHECK && jz >= maxZ) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Overflow at iz=%d, jz=%d (maxZ=%d) adj") % iz %
              jz % maxZ);
        }
        if (EXTRA_CHECK && iz < minZ) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Underflow at iz=%d, jz=%d adj") % iz % jz);
        }

        __do_gradient_vec(
            adjoint_gradient, density, weight[i], i, 0, ix, iy, iz, jx, jy, jz,
            x, y, z, inv_nmean * inv_dx);
        __do_gradient_vec(
            adjoint_gradient, density, weight[i], i, 1, ix, iy, iz, jx, jy, jz,
            x, y, z, inv_nmean * inv_dy);
        __do_gradient_vec(
            adjoint_gradient, density, weight[i], i, 2, ix, iy, iz, jx, jy, jz,
            x, y, z, inv_nmean * inv_dz);
      }
    } //adjoint

    template <
        typename ParticleBasedScalar, typename ParticleArray,
        typename ProjectionDensityArray, typename WeightArray,
        typename PeriodicFunction>
    static typename std::enable_if<WeightArray::dimensionality == 1>::type
    adjoint_interpolation_scalar(
        int axis, ParticleBasedScalar &A, const ParticleArray &particles,
        const ProjectionDensityArray &field, T Lx, T Ly, T Lz, int N0, int N1,
        int N2, const PeriodicFunction &p, const WeightArray &weight,
        size_t Np) {
      ConsoleContext<LOG_DEBUG> ctx("Classic CIC adjoint-interpolation");

      T inv_dx = N0 / Lx;
      T inv_dy = N1 / Ly;
      T inv_dz = N2 / Lz;
      size_t minX = field.index_bases()[0];
      size_t minY = field.index_bases()[1];
      size_t minZ = field.index_bases()[2];
      size_t maxX = field.index_bases()[0] + field.shape()[0];
      size_t maxY = field.index_bases()[1] + field.shape()[1];
      size_t maxZ = field.index_bases()[2] + field.shape()[2];

      ctx.print(boost::format("minX=%d, maxX=%d, N0=%d") % minX % maxX % N0);

      size_t const bounds[3][2] = {{minX, maxX}, {minY, maxY}, {minZ, maxZ}};
#  pragma omp parallel for schedule(static)
      for (long i = 0; i < Np; i++) {

        T x = particles[i][0] * inv_dx;
        T y = particles[i][1] * inv_dy;
        T z = particles[i][2] * inv_dz;

        size_t ix = (size_t)std::floor(x);
        size_t iy = (size_t)std::floor(y);
        size_t iz = (size_t)std::floor(z);

        size_t jx = ix + 1;
        size_t jy = (iy + 1);
        size_t jz = (iz + 1);

        p(jx, jy, jz);

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

        if (jx >= maxX) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Overflow at ix=%d, jx=%d (maxX=%d)") % ix % jx %
              maxX);
          MPI_Communication::instance()->abort();
        }
        if (ix < minX) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Underflow at ix=%d, jx=%d") % ix % jx);
          MPI_Communication::instance()->abort();
        }
        if (jy >= maxY) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Overflow at iy=%d, jy=%d (maxY=%d)") % iy % jy %
              maxY);
          MPI_Communication::instance()->abort();
        }
        if (iy < minY) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Underflow at iy=%d, jy=%d") % iy % jy);
          MPI_Communication::instance()->abort();
        }

        __do_interpolation(
            A, field, weight, i, qx, qy, qz, rx, ry, rz, ix, iy, iz, jx, jy,
            jz);
      }
    } //adjoint_interpolation_scalar

    template <
        typename ParticleBasedArray, typename ParticleArray,
        typename ProjectionDensityArray, typename WeightArray,
        typename PeriodicFunction>
    static typename std::enable_if<WeightArray::dimensionality != 1>::type
    adjoint_interpolation(
        int axis, ParticleBasedArray &A, const ParticleArray &particles,
        const ProjectionDensityArray &field, T Lx, T Ly, T Lz, int N0, int N1,
        int N2, const PeriodicFunction &p, const WeightArray &weight,
        size_t Np) {
      ConsoleContext<LOG_DEBUG> ctx("Classic CIC adjoint-interpolation");

      T inv_dx = N0 / Lx;
      T inv_dy = N1 / Ly;
      T inv_dz = N2 / Lz;
      size_t minX = field.index_bases()[0];
      size_t minY = field.index_bases()[1];
      size_t minZ = field.index_bases()[2];
      size_t maxX = field.index_bases()[0] + field.shape()[0];
      size_t maxY = field.index_bases()[1] + field.shape()[1];
      size_t maxZ = field.index_bases()[2] + field.shape()[2];

      ctx.print(boost::format("minX=%d, maxX=%d, N0=%d") % minX % maxX % N0);

      size_t const bounds[3][2] = {{minX, maxX}, {minY, maxY}, {minZ, maxZ}};
#  pragma omp parallel for schedule(static)
      for (size_t i = 0; i < Np; i++) {

        T x = particles[i][0] * inv_dx;
        T y = particles[i][1] * inv_dy;
        T z = particles[i][2] * inv_dz;

        size_t ix = (size_t)std::floor(x);
        size_t iy = (size_t)std::floor(y);
        size_t iz = (size_t)std::floor(z);

        size_t jx = ix + 1;
        size_t jy = (iy + 1);
        size_t jz = (iz + 1);

        p(jx, jy, jz);

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

        if (jx >= maxX) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Overflow at ix=%d, jx=%d (maxX=%d)") % ix % jx %
              maxX);
          MPI_Communication::instance()->abort();
        }
        if (ix < minX) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Underflow at ix=%d, jx=%d") % ix % jx);
          MPI_Communication::instance()->abort();
        }
        if (jy >= maxY) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Overflow at iy=%d, jy=%d (maxY=%d)") % iy % jy %
              maxY);
          MPI_Communication::instance()->abort();
        }
        if (iy < minY) {
          Console::instance().print<LOG_ERROR>(
              boost::format("Underflow at iy=%d, jy=%d") % iy % jy);
          MPI_Communication::instance()->abort();
        }

        __do_interpolation_vec(
            A, field, weight, i, qx, qy, qz, rx, ry, rz, ix, iy, iz, jx, jy,
            jz);
      }
    } //adjoint_interpolation
  };

  template <typename T>
  struct CIC_Distribution {
    typedef long LongElt;

    std::shared_ptr<FFTW_Manager_3d<T>> &force_mgr;
    size_t f_N0;
    size_t f_startN0;
    size_t f_localN0;
    double L0, inv_dx;

    CIC_Distribution(
        std::shared_ptr<FFTW_Manager_3d<T>> &mgr, double L0, double = 0,
        double = 0)
        : force_mgr(mgr), f_N0(mgr->N0), f_startN0(mgr->startN0),
          f_localN0(mgr->localN0) {
      this->L0 = L0;
      this->inv_dx = f_N0 / L0;
    }

    template <typename Position, typename... U>
    LongElt operator()(Position &&pos, U &&...) {
      double q = pos[0] * inv_dx;
      double floor_q = std::floor(q);
      LongElt i0 = LongElt(floor_q);
      if (i0 < 0 || i0 >= f_N0)
        error_helper<ErrorBadState>(
            "Do not know how to distribute that position: " +
            std::to_string(pos[0]));
      return force_mgr->get_peer(i0);
    }
  };

  template <typename T, bool ignore_overflow = false>
  class ClassicCloudInCell
      : public GenericCIC<T, ClassicCloudInCell_impl<T, ignore_overflow>> {
  public:
    typedef T Type;
    typedef ClassicCloudInCell_impl<T, ignore_overflow> Base;
    // Number of extra planes required in case of MPI
    static const int MPI_PLANE_LEAKAGE = 1;
    static const int MPI_NEGATIVE_PLANE_LEAKAGE = 0;

    typedef CIC_Tools::Periodic_MPI Periodic_MPI;
    typedef CIC_Distribution<T> Distribution;
  };
} // namespace LibLSS

#endif

// ARES TAG: authors_num = 3
// ARES TAG: name(0) = Jens Jasche
// ARES TAG: year(0) = 2009-2019
// ARES TAG: email(0) = jens.jasche@fysik.su.se
// ARES TAG: name(1) = Guilhem Lavaux
// ARES TAG: year(1) = 2014-2019
// ARES TAG: email(1) = guilhem.lavaux@iap.fr
// ARES TAG: name(2) = Florent Leclercq
// ARES TAG: year(2) = 2019
// ARES TAG: email(2) = florent.leclercq@polytechnique.org
