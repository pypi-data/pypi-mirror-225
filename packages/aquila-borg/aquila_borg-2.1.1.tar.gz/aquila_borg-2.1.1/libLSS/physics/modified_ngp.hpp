/*+
    ARES/HADES/BORG Package -- ./libLSS/physics/modified_ngp.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHYSICS_MODIFIED_NGP_HPP
#define __LIBLSS_PHYSICS_MODIFIED_NGP_HPP

#include <cmath>
#include "libLSS/tools/console.hpp"
#include <boost/multi_array.hpp>
#include "libLSS/physics/generic_cic.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/compiler_tools.hpp"

namespace LibLSS {

  template <typename T, typename SubgridSpec, bool ignore_overflow>
  struct ModifiedNGP_impl {
    typedef T Type;
    // Number of extra planes required in case of MPI
    static const int MPI_PLANE_LEAKAGE = 1;
    static const bool EXTRA_CHECK = true;
    typedef boost::multi_array<T, 3> DensityArray;

    //get virtual grid spacing
    //for testing we choose subres=1. this should reprodice CIC
    //particles will be assumed to be little boxes of size dx*subres
    // subres = 1 corresponds to CIC
    // subres -> 0 approaches NGP
    static constexpr double subres = SubgridSpec::value;

    template <typename A>
    static inline void _safe_set(
        A &&density, size_t const ix, size_t const iy, size_t const iz,
        ssize_t const bounds[3][2], T const &value) {
      if (ix >= bounds[0][0] && ix < bounds[0][1] && iy >= bounds[1][0] &&
          iy < bounds[1][1] && iz >= bounds[2][0] && iz < bounds[2][1]) {
        density[ix][iy][iz] += value;
      }
    }

    // This function implements the particle projection to a grid.
    // Arguments:
    //   - particles (2d array: Nx3)
    //   - density (3d array: N0xN1xN2, or slice thereof)
    //   - Lx, Ly, Lz: physical size
    //   - N0, N1, N2: grid size
    //   - p: a function applying optional periodic boundary enforcement (depends on MPI for ghost plane)
    //   - weight: per-particle weight functor, maybe returning only "1"
    //   - Np: number of particles to project
    template <
        typename ParticleArray, typename ProjectionDensityArray,
        typename WeightArray, typename PeriodicFunction>
    static void projection(
        const ParticleArray &particles, ProjectionDensityArray &density, T Lx,
        T Ly, T Lz, int N0, int N1, int N2, const PeriodicFunction &p,
        const WeightArray &weight, size_t Np) {
      ConsoleContext<LOG_DEBUG> ctx("Modified NGP projection");

      T inv_dx = N0 / Lx;
      T inv_dy = N1 / Ly;
      T inv_dz = N2 / Lz;

      ssize_t minX = density.index_bases()[0];
      ssize_t minY = density.index_bases()[1];
      ssize_t minZ = density.index_bases()[2];
      ssize_t maxX = minX + density.shape()[0];
      ssize_t maxY = minY + density.shape()[1];
      ssize_t maxZ = minZ + density.shape()[2];

      ssize_t const bounds[3][2] = {{minX, maxX}, {minY, maxY}, {minZ, maxZ}};

      ctx.format("minX=%d, maxX=%d, N0=%d", minX, maxX, N0);
      ctx.format("minY=%d, maxY=%d, N1=%d", minY, maxY, N1);
      ctx.format("minZ=%d, maxZ=%d, N2=%d", minZ, maxZ, N2);

      for (long i = 0; i < Np; i++) {

        //divide particle positions by target grid-size
        //Note: all integer numbers are therefore defined at target resolution
        T x = particles[i][0] * inv_dx;
        T y = particles[i][1] * inv_dy;
        T z = particles[i][2] * inv_dz;

        //Note, we want to find the nearest lower left corner of a voxel that fully contains
        //the box-shapep particle.
        //we therefore have to find the nearest voxel for the lower left corner of the particel box

        size_t ix = (size_t)std::floor(
            x +
            0.5 * (1. - subres)); //the offset of half a subresolution factor
        size_t iy = (size_t)std::floor(
            y +
            0.5 *
                (1. -
                 subres)); //ensures the edges of the particle cloud are within
        size_t iz = (size_t)std::floor(
            z + 0.5 * (1. - subres)); //the lower voxel boundaries
        //Note, it can be easily seen that for subres=1 the CIC scheme is recovered.

        //now calculate distances before wrap-around
        //if particle is fully contained in voxel assign the total mass
        T rx = 0.;
        T qx = 1.;

        T ry = 0.;
        T qy = 1.;

        T rz = 0.;
        T qz = 1.;
        // clang-format off
DISABLE_WARN_DIV_BY_ZERO;
        // clang-format on
        //if fraction of particle is contained in the next cell assign a fraction of mass
        double dd = x - ix - 0.5 * (1 - subres);
        if (dd > 0. && subres > 0) {
          rx = dd / subres;
          qx = 1. - rx;
        }

        dd = y - iy - 0.5 * (1 - subres);
        if (dd > 0. && subres > 0) {
          ry = dd / subres;
          qy = 1. - ry;
        }

        dd = z - iz - 0.5 * (1 - subres);
        if (dd > 0. && subres > 0) {
          rz = dd / subres;
          qz = 1. - rz;
        }
        // clang-format off
ENABLE_WARN_DIV_BY_ZERO;
        // clang-format on

        //we need to check for periodicity
        p(ix, iy, iz);

        //if the particle is fully contained within a voxel
        //then we can attribute its entire mass to this bin.
        //otherwise a fraction of mass will be assigned to
        //the next bin.

        //find next cells
        size_t jx = (ix + 1);
        size_t jy = (iy + 1);
        size_t jz = (iz + 1);

        //check for periodicity
        p(jx, jy, jz);

        double w = weight[i];

        if (!ignore_overflow) {
          if (EXTRA_CHECK && jx >= maxX) {
            Console::instance().print<LOG_ERROR>(
                boost::format("Overflow at ix=%d, jx=%d (maxX=%d)") % ix % jx %
                maxX);
          }
          if (EXTRA_CHECK && ix < minX) {
            Console::instance().print<LOG_ERROR>(
                boost::format("Underflow at ix=%d, jx=%d") % ix % jx);
          }
          if (EXTRA_CHECK && ix >= maxX) {
            Console::instance().print<LOG_ERROR>(
                boost::format("Overflow at ix=%d, jx=%d with x=%g") % ix % jx %
                x);
          }
          if (EXTRA_CHECK && jy >= maxY) {
            Console::instance().print<LOG_ERROR>(
                boost::format("Overflow at iy=%d, jy=%d (maxY=%d)") % iy % jy %
                maxY);
          }
          if (EXTRA_CHECK && iy < minY) {
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
    }

    template <typename GradientArray, typename ProjectionDensityArray>
    static inline void __do_gradient(
        GradientArray &adj_gradient, const ProjectionDensityArray &density,
        size_t i, int axis, int ix, int iy, int iz, int jx, int jy, int jz,
        T rx, T ry, T rz, T qx, T qy, T qz, T global_w) {

      switch (axis) {
      case 0:

        //Note the derivative of the Heaviside function is zero
        if (rx > 0. && subres > 0) {
          rx = 1. / subres;
          qx = -1. / subres;
        } else {
          rx = 0;
          qx = 0;
        }

        break;
      case 1:
        //Note the derivative of the Heaviside function is zero
        if (ry > 0. && subres > 0) {
          ry = 1. / subres;
          qy = -1. / subres;
        } else {
          ry = 0;
          qy = 0;
        }
        break;
      case 2:
        //Note the derivative of the Heaviside function is zero
        if (rz > 0. && subres > 0) {
          rz = 1. / subres;
          qz = -1. / subres;
        } else {
          rz = 0;
          qz = 0;
        }
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
    }

    template <
        typename ParticleArray, typename GradientArray,
        typename ProjectionDensityArray, typename PeriodicFunction,
        typename WeightArray>
    static void adjoint(
        const ParticleArray &particles, ProjectionDensityArray &density,
        GradientArray &adjoint_gradient, const WeightArray &weight, T Lx, T Ly,
        T Lz, int N0, int N1, int N2, const PeriodicFunction &p, T nmean,
        size_t Np) {
      ConsoleContext<LOG_DEBUG> ctx("Modified NGP adjoint-projection");

      T inv_dx = N0 / Lx;
      T inv_dy = N1 / Ly;
      T inv_dz = N2 / Lz;
      T inv_nmean = T(1) / nmean;
      ssize_t minX = density.index_bases()[0];
      ssize_t minY = density.index_bases()[1];
      ssize_t minZ = density.index_bases()[2];
      ssize_t maxX = minX + density.shape()[0];
      ssize_t maxY = minY + density.shape()[1];
      ssize_t maxZ = minZ + density.shape()[2];

      ctx.print(
          boost::format(
              "Number of particles = %d (array is %d), minX=%d maxX=%d") %
          Np % particles.shape()[0] % minX % maxX);
      ctx.print(
          boost::format("Adjoint gradient = %d") % adjoint_gradient.shape()[0]);

#pragma omp parallel for schedule(static)
      for (size_t i = 0; i < Np; i++) {

        T x = particles[i][0] * inv_dx;
        T y = particles[i][1] * inv_dy;
        T z = particles[i][2] * inv_dz;

        ssize_t ix = (ssize_t)std::floor(x + 0.5 * (1. - subres));
        ssize_t iy = (ssize_t)std::floor(y + 0.5 * (1. - subres));
        ssize_t iz = (ssize_t)std::floor(z + 0.5 * (1. - subres));

        T rx = 0.;
        T qx = 1.;

        T ry = 0.;
        T qy = 1.;

        T rz = 0.;
        T qz = 1.;

        double dd = x - ix - 0.5 * (1 - subres);
        if (dd > 0. && subres > 0) {
          rx = dd / subres;
          qx = 1. - rx;
        }

        dd = y - iy - 0.5 * (1 - subres);
        if (dd > 0. && subres > 0) {
          ry = dd / subres;
          qy = 1. - ry;
        }

        dd = z - iz - 0.5 * (1 - subres);
        if (dd > 0. && subres > 0) {
          rz = dd / subres;
          qz = 1. - rz;
        }

        p(ix, iy, iz);

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
            adjoint_gradient, density, i, 0, ix, iy, iz, jx, jy, jz, rx, ry, rz,
            qx, qy, qz, inv_nmean * inv_dx);
        __do_gradient(
            adjoint_gradient, density, i, 1, ix, iy, iz, jx, jy, jz, rx, ry, rz,
            qx, qy, qz, inv_nmean * inv_dy);
        __do_gradient(
            adjoint_gradient, density, i, 2, ix, iy, iz, jx, jy, jz, rx, ry, rz,
            qx, qy, qz, inv_nmean * inv_dz);
      }
    }
  };

  namespace NGPGrid {
    struct NGP {
      static constexpr double value = 0.0;
    };
    struct CIC {
      static constexpr double value = 1.0;
    };
    struct Double {
      static constexpr double value = 0.5;
    };
    struct Quad {
      static constexpr double value = 0.25;
    };
  } // namespace NGPGrid

  // This implements the ModifiedNGP kernel. By default it acts like a CIC, for an additional cost.
  // It relies on GenericCIC to implement the missing auxiliary functions from the base function
  // given in ModifiedNGP_impl
  template <
      typename T, typename SubgridSpec = NGPGrid::CIC,
      bool ignore_overflow = false>
  class ModifiedNGP
      : public GenericCIC<
            T, ModifiedNGP_impl<T, SubgridSpec, ignore_overflow>> {
  public:
    typedef ModifiedNGP_impl<T, SubgridSpec, ignore_overflow> Base;
    typedef T Type;

    // Number of extra ghost planes required in case of MPI. Only post planes are
    // supported.
    // In practice only ONE plane is supported at the moment.
    static const int MPI_PLANE_LEAKAGE = 1;
    static const int MPI_NEGATIVE_PLANE_LEAKAGE = 0;

    typedef CIC_Tools::Periodic_MPI Periodic_MPI;

    // This defines the policy of load balancing distribution for MNGP.
    // This class translates the requirements of slabing by FFTW to particle
    // positions. As we are still using the ghost plane mechanism to adjust for
    // edge effects this decision class is required to be able to do correct parallel
    // projection.
    // Its task is quite minimal as most of the complexity is in "get_peer" and
    // load balancing in samplers/borg/pm/particle_distribution.hpp
    struct Distribution {
      typedef long LongElt;
      typedef LibLSS::FFTW_Manager_3d<T> Manager;

      std::shared_ptr<Manager> &force_mgr;
      size_t f_N0;
      size_t f_startN0;
      size_t f_localN0;
      double L0;

      Distribution(
          std::shared_ptr<Manager> &mgr, double L0, double = 0, double = 0)
          : force_mgr(mgr), f_N0(mgr->N0), f_startN0(mgr->startN0),
            f_localN0(mgr->localN0) {
        this->L0 = L0;
        Console::instance().print<LOG_DEBUG>(
            boost::format(
                "Initialize particle distribution decider: N0 = %d, L0 = %g") %
            f_N0 % L0);
      }

      template <typename Position, typename... U>
      inline LongElt operator()(Position &&pos, U &&...) {
        T x = pos[0] * f_N0 / L0;
        LongElt i0 = LongElt(std::floor(x + 0.5 * (1. - Base::subres))) % f_N0;
        LongElt peer = force_mgr->get_peer(i0);
        //Console::instance().print<LOG_DEBUG>(boost::format("Pos %g, peer = %d") % x % peer);
        return peer;
      }
    };
  };
} // namespace LibLSS

#endif
