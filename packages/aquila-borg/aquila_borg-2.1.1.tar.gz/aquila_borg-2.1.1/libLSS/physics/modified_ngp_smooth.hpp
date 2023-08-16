/*+
    ARES/HADES/BORG Package -- ./libLSS/physics/modified_ngp_smooth.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHYSICS_SMOOTH_MODIFIED_NGP_HPP
#define __LIBLSS_PHYSICS_SMOOTH_MODIFIED_NGP_HPP

#include <cmath>
#include <CosmoTool/algo.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/physics/generic_cic.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"

namespace LibLSS {

    template<typename T, typename SubgridSpec>
    struct SmoothModifiedNGP_impl {
        typedef T Type;
        // Number of extra planes required in case of MPI
        static const int MPI_PLANE_LEAKAGE = 1;
        static const bool EXTRA_CHECK = true;

        //get virtual grid spacing
        //for testing we choose subres=1. this should reprodice CIC
        //particles will be assumed to be little boxes of size dx*subres
        // subres = 1 corresponds to CIC
        // subres -> 0 approaches NGP
        static constexpr double subres=SubgridSpec::value;

        static constexpr double C0 = (1. - subres)/6.;

        static inline T kernel(T delta) {
            double const a = subres > 0 ? delta/subres : 0;
            if (a < 0.5 && a > -0.5) {
               return 0.5 + (a  - CosmoTool::cube(2*a) * C0);
            } else if (a > 0.5) {
                return 1 - 8 * C0 * CosmoTool::cube((0.5 - delta)/(1-subres));
            } else {
                return 8 * C0 * CosmoTool::cube((0.5 + delta)/(1-subres));
            }
        }

        static inline T adjoint(T delta) {
            double const a = subres > 0 ? delta/subres : 0;
            if (a < 0.5 && a > -0.5) {
               return (1 - (6*C0)*CosmoTool::square(2*a))/subres;
            } else if (a > 0.5) {
                return (24 * C0/(1-subres)) * CosmoTool::square((0.5 - delta)/(1-subres));
            } else {
                return (24 * C0/(1-subres)) * CosmoTool::square((0.5 + delta)/(1-subres));
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
        template<typename ParticleArray, typename ProjectionDensityArray, typename WeightArray,
                 typename PeriodicFunction >
        static void projection(const ParticleArray& particles, ProjectionDensityArray& density,
                               T Lx, T Ly, T Lz,
                               int N0, int N1, int N2, const PeriodicFunction& p, const WeightArray& weight, size_t Np) {
            ConsoleContext<LOG_DEBUG> ctx("Modified NGP projection");

            T inv_dx = N0/Lx;
            T inv_dy = N1/Ly;
            T inv_dz = N2/Lz;

            int minX = density.index_bases()[0];
            int minY = density.index_bases()[1];
            int minZ = density.index_bases()[2];
            int maxX = density.index_bases()[0] + density.shape()[0];
            int maxY = density.index_bases()[1] + density.shape()[1];
            int maxZ = density.index_bases()[2] + density.shape()[2];

            ctx.print(boost::format("minX=%d, maxX=%d, N0=%d") % minX % maxX % N0);

            for (long i = 0; i < Np; i++) {

                //divide particle positions by target grid-size
                //Note: all integer numbers are therefore defined at target resolution
                T x = particles[i][0]*inv_dx;
                T y = particles[i][1]*inv_dy;
                T z = particles[i][2]*inv_dz;

                //Note, we want to find the nearest lower left corner of a voxel that fully contains
                //the box-shapep particle.
                //we therefore have to find the nearest voxel for the lower left corner of the particel box

                size_t ix = (size_t)std::floor(x); //the offset of half a subresolution factor
                size_t iy = (size_t)std::floor(y); //ensures the edges of the particle cloud are within
                size_t iz = (size_t)std::floor(z); //the lower voxel boundaries

                T rx, qx;
                T ry, qy;
                T rz, qz;

                // dx > 0 by construction. delta is taken with respect to the center
                // dx = ix+0.5 - x
                qx = kernel((double(ix)-x) + 0.5);
                rx = 1-qx;
                qy = kernel((double(iy)-y) + 0.5);
                ry = 1-qy;
                qz = kernel((double(iz)-z) + 0.5);
                rz = 1-qz;

                //we need to check for periodicity
                p(ix, iy, iz);

                //if the particle is fully contained within a voxel
                //then we can attribute its entire mass to this bin.
                //otherwise a fraction of mass will be assigned to
                //the next bin.

                //find next cells
                size_t jx = (ix+1);
                size_t jy = (iy+1);
                size_t jz = (iz+1);

                //check for periodicity
                p(jx, jy, jz);

                double w = weight[i];

                if (EXTRA_CHECK && jx >= maxX) {
                    Console::instance().print<LOG_ERROR>(boost::format("Overflow at ix=%d, jx=%d (maxX=%d)") % ix % jx % maxX);
                }
                if (EXTRA_CHECK && ix < minX) {
                    Console::instance().print<LOG_ERROR>(boost::format("Underflow at ix=%d, jx=%d") % ix % jx);
                }
                if (EXTRA_CHECK && ix >= maxX) {
                    Console::instance().print<LOG_ERROR>(boost::format("Overflow at ix=%d, jx=%d with x=%g") % ix % jx % x);
                }
                if (EXTRA_CHECK && jy >= maxY) {
                    Console::instance().print<LOG_ERROR>(boost::format("Overflow at iy=%d, jy=%d (maxY=%d)") % iy % jy % maxY);
                }
                if (EXTRA_CHECK && iy < minY) {
                    Console::instance().print<LOG_ERROR>(boost::format("Underflow at iy=%d, jy=%d") % iy % jy);
                }

                density[ix][iy][iz] += (  qx)*(  qy)*(  qz)*w;
                density[ix][iy][jz] += (  qx)*(  qy)*(  rz)*w;
                density[ix][jy][iz] += (  qx)*(  ry)*(  qz)*w;
                density[ix][jy][jz] += (  qx)*(  ry)*(  rz)*w;
                density[jx][iy][iz] += (  rx)*(  qy)*(  qz)*w;
                density[jx][iy][jz] += (  rx)*(  qy)*(  rz)*w;
                density[jx][jy][iz] += (  rx)*(  ry)*(  qz)*w;
                density[jx][jy][jz] += (  rx)*(  ry)*(  rz)*w;
            }

        }


        template<typename GradientArray, typename ProjectionDensityArray>
        static inline void __do_gradient(GradientArray& adj_gradient,
                                  const ProjectionDensityArray& density,
                                  size_t i,
                                  int axis,
                                  int ix, int iy, int iz,
                                  int jx, int jy, int jz,
                                  T dx, T dy, T dz,
                                  T rx, T ry, T rz, T qx, T qy, T qz, T global_w)
        {

            switch (axis) {
                case 0:
                    qx = -adjoint(dx);
                    rx= -qx;
                    break;
                case 1:
                    qy = -adjoint(dy);
                    ry= -qy;
                    break;
                case 2:
                    qz = -adjoint(dz);
                    rz= -qz;
                    break;
            }

            double w =
                density[ix][iy][iz] * qx * qy * qz +
                density[ix][iy][jz] * qx * qy * rz +
                density[ix][jy][iz] * qx * ry * qz +
                density[ix][jy][jz] * qx * ry * rz +
                density[jx][iy][iz] * rx * qy * qz +
                density[jx][iy][jz] * rx * qy * rz +
                density[jx][jy][iz] * rx * ry * qz +
                density[jx][jy][jz] * rx * ry * rz;

            adj_gradient[i][axis] += w*global_w;
        }

        template<typename ParticleArray, typename GradientArray, typename ProjectionDensityArray, typename PeriodicFunction, typename WeightArray>
        static void adjoint(const ParticleArray& particles, ProjectionDensityArray& density,
                            GradientArray& adjoint_gradient, const WeightArray& weight,
                            T Lx, T Ly, T Lz,
                            int N0, int N1, int N2,
                            const PeriodicFunction& p,
                            T nmean, size_t Np) {
            ConsoleContext<LOG_DEBUG> ctx("Modified NGP adjoint-projection");

            T inv_dx = N0/Lx;
            T inv_dy = N1/Ly;
            T inv_dz = N2/Lz;
            T inv_nmean = T(1)/nmean;
            int minX = density.index_bases()[0];
            int minY = density.index_bases()[1];
            int minZ = density.index_bases()[2];
            int maxX = minX + density.shape()[0];
            int maxY = minY + density.shape()[1];
            int maxZ = minZ + density.shape()[2];

            ctx.print(boost::format("Number of particles = %d (array is %d), minX=%d maxX=%d") % Np %particles.shape()[0] % minX % maxX);
            ctx.print(boost::format("Adjoint gradient = %d") % adjoint_gradient.shape()[0]);

#pragma omp parallel for schedule(static)
            for (size_t i = 0; i < Np; i++) {

                T x = particles[i][0]*inv_dx;
                T y = particles[i][1]*inv_dy;
                T z = particles[i][2]*inv_dz;

                size_t ix = (size_t)std::floor(x);
                size_t iy = (size_t)std::floor(y);
                size_t iz = (size_t)std::floor(z);

                T rx, qx;
                T ry, qy;
                T rz, qz;
		T dx = (double(ix)-x)+0.5;
		T dy = (double(iy)-y)+0.5;
		T dz = (double(iz)-z)+0.5;

                qx = kernel(dx);
                rx = 1-qx;
                qy = kernel(dy);
                ry = 1-qy;
                qz = kernel(dz);
                rz = 1-qz;

                p(ix, iy, iz);

                size_t jx = (ix+1);
                size_t jy = (iy+1);
                size_t jz = (iz+1);

                p(jx, jy, jz);

                if (EXTRA_CHECK && jx >= maxX) {
                    Console::instance().print<LOG_ERROR>(boost::format("Overflow at ix=%d, jx=%d (maxX adj = %d)") % ix % jx % maxX);
                }
                if (EXTRA_CHECK &&ix < minX) {
                    Console::instance().print<LOG_ERROR>(boost::format("Underflow at ix=%d, jx=%d (adj)") % ix % jx);
                }
                if (EXTRA_CHECK &&jy >= maxY) {
                    Console::instance().print<LOG_ERROR>(boost::format("Overflow at iy=%d, jy=%d (maxY=%d) adj") % iy % jy % maxY);
                }
                if (EXTRA_CHECK && iy < minY) {
                    Console::instance().print<LOG_ERROR>(boost::format("Underflow at iy=%d, jy=%d adj") % iy % jy);
                }
                if (EXTRA_CHECK && jz >= maxZ) {
                    Console::instance().print<LOG_ERROR>(boost::format("Overflow at iz=%d, jz=%d (maxZ=%d) adj") % iz % jz % maxZ);
                }
                if (EXTRA_CHECK && iz < minZ) {
                    Console::instance().print<LOG_ERROR>(boost::format("Underflow at iz=%d, jz=%d adj") % iz % jz);
                }

                __do_gradient(adjoint_gradient, density, i, 0, ix, iy, iz, jx, jy, jz, dx, dy, dz, rx, ry, rz, qx, qy, qz, inv_nmean*inv_dx);
                __do_gradient(adjoint_gradient, density, i, 1, ix, iy, iz, jx, jy, jz, dx, dy, dz, rx, ry, rz, qx, qy, qz, inv_nmean*inv_dy);
                __do_gradient(adjoint_gradient, density, i, 2, ix, iy, iz, jx, jy, jz, dx, dy, dz, rx, ry, rz, qx, qy, qz, inv_nmean*inv_dz);
            }

        }

    };


    namespace SmoothNGPGrid {
      struct CIC { static constexpr double value = 1; };
      struct Double { static constexpr double value = 0.5; };
      struct Quad { static constexpr double value = 0.3; };
    }


    // This implements the ModifiedNGP kernel. By default it acts like a CIC, for an additional cost.
    // It relies on GenericCIC to implement the missing auxiliary functions from the base function
    // given in ModifiedNGP_impl
    template<typename T,typename SubgridSpec = SmoothNGPGrid::CIC>
    class SmoothModifiedNGP: public GenericCIC<T, SmoothModifiedNGP_impl<T,SubgridSpec> > {
    public:
        typedef SmoothModifiedNGP_impl<T,SubgridSpec> Base;
        typedef T Type;

        // Number of extra ghost planes required in case of MPI. Only post planes are
        // supported.
        // In practice only ONE plane is supported at the moment.
        static const int MPI_PLANE_LEAKAGE = 1;
        static const int MPI_NEGATIVE_PLANE_LEAKAGE = 1;

        struct Periodic_MPI
        {
          bool start;
          size_t N0, N1, N2;

          Periodic_MPI(size_t _N0, size_t _N1, size_t _N2, MPI_Communication *comm)
            : N0(_N0), N1(_N1), N2(_N2) {
            start = comm->rank() == 0;
          }

          void operator()(size_t& i, size_t& j, size_t& k) const {
            if (start)
              if (i >= N0) i %= N0;
            if (j >= N1) j %= N1;
            if (k >= N2) k %= N2;
          }
        };

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

	    std::shared_ptr<Manager>& force_mgr;
            size_t f_N0;
            size_t f_startN0;
            size_t f_localN0;
            double L0;

            Distribution(std::shared_ptr<Manager>& mgr, double L0, double = 0, double = 0)
                : force_mgr(mgr), f_N0(mgr->N0), f_startN0(mgr->startN0), 
                  f_localN0(mgr->localN0) {
                  this->L0 = L0;
                  Console::instance().print<LOG_DEBUG>(boost::format("Initialize particle distribution decisioner: N0 = %d, L0 = %g") % f_N0 % L0);
            }

            template<typename Position, typename... U>
            inline LongElt operator()(Position&& pos, U&&...) {
                T x = pos[0]*f_N0/L0;
                LongElt i0 = LongElt(std::floor(x))  % f_N0;
                LongElt peer = force_mgr->get_peer(i0);
                //Console::instance().print<LOG_DEBUG>(boost::format("Pos %g, peer = %d") % x % peer);
                return peer;
            }
        };

    };
}

#endif
