/*+
    ARES/HADES/BORG Package -- ./libLSS/physics/generic_cic.hpp
    Copyright (C) 2009-2019 Jens Jasche <jens.jasche@fysik.su.se>
    Copyright (C) 2014-2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2019 Florent Leclercq <florent.leclercq@polytechnique.org>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_GENERIC_CIC_HPP
#define __LIBLSS_GENERIC_CIC_HPP

#include <boost/config.hpp>

namespace LibLSS {

    namespace CIC_Tools {

        struct NonPeriodic {
            NonPeriodic(int, int, int ) {}

            template<typename I>
            void operator()(I& i, I& j, I& k) const {}
        };

        struct Periodic {
            int N0, N1, N2;

            Periodic(int fN0, int fN1, int fN2) :
                N0(fN0), N1(fN1), N2(fN2) {}

            template<typename I>
            void operator()(I& i, I& j, I& k) const {
                if (i>=N0) i %= N0;
                if (j>=N1) j %= N1;
                if (k>=N2) k %= N2;
            }
        };

        struct Periodic_MPI {
            size_t N0, N1, N2;

            Periodic_MPI(size_t fN0, size_t fN1, size_t fN2, MPI_Communication *comm) :
                N0(fN0), N1(fN1), N2(fN2) {}

            template<typename I>
            void operator()(I& i, I& j, I& k) const {
                if (j>=N1) j %= N1;
                if (k>=N2) k %= N2;
            }
        };

        struct DefaultWeight  {
            BOOST_STATIC_CONSTANT(size_t, dimensionality = 1);
            double operator[](long) const { return 1; }
        };
        
        struct DefaultWeightDim2  {
            BOOST_STATIC_CONSTANT(size_t, dimensionality = 2);
            auto operator[](long) const { return DefaultWeight(); }
        };
    }


    template<typename T,typename ImplType>
    class GenericCIC {
    public:
        typedef ImplType impl;

        template<typename ParticleArray, typename ProjectionDensityArray, typename WeightArray,
                 typename PeriodicFunction>
        static void projection(const ParticleArray& particles, ProjectionDensityArray& density,
                               T Lx, T Ly, T Lz,
                               int N0, int N1, int N2,
                               const PeriodicFunction& p, const WeightArray& weight, size_t Np) {
            impl::projection(particles, density, Lx, Ly, Lz, N0, N1, N2, p, weight, Np);
        }


        template<typename ParticleArray, typename ProjectionDensityArray, typename WeightArray,
                 typename PeriodicFunction>
        static void projection(const ParticleArray& particles, ProjectionDensityArray& density,
                               T Lx, T Ly, T Lz,
                               int N0, int N1, int N2,
                               const PeriodicFunction& p, const WeightArray& weight) {
          impl::projection(particles, density, Lx, Ly, Lz, N0, N1, N2, p, weight, particles.shape()[0]);
        }

        template<typename ParticleArray, typename ProjectionDensityArray, typename PeriodicFunction>
        static void projection(const ParticleArray& particles, ProjectionDensityArray& density,
                               T Lx, T Ly, T Lz,
                               int N0, int N1, int N2,
                               const PeriodicFunction& p) {
          impl::projection(particles, density, Lx, Ly, Lz, N0, N1, N2, p,
                       CIC_Tools::DefaultWeight(), particles.shape()[0]);
        }

        template<typename ParticleArray, typename ProjectionDensityArray>
        static void projection(const ParticleArray& particles, ProjectionDensityArray& density,
                               T Lx, T Ly, T Lz,
                               int N0, int N1, int N2) {
          impl::projection(particles, density, Lx, Ly, Lz, N0, N1, N2, CIC_Tools::Periodic(N0, N1, N2),
                           CIC_Tools::DefaultWeight(), particles.shape()[0]);
        }
        
        template<typename ParticleBasedScalar, typename ParticleArray, typename ProjectionDensityArray,
                  typename WeightArray, typename PeriodicFunction>
        static void interpolation_scalar(ParticleBasedScalar &A, const ParticleArray &particles, const ProjectionDensityArray &field, T Lx,
        T Ly, T Lz, int N0, int N1, int N2, const PeriodicFunction &p,
        const WeightArray &weight, size_t Np) {
            impl::interpolation_scalar(A, particles, field, Lx, Ly, Lz, N0, N1, N2, p, weight, Np);
        }
        
        template<typename ParticleBasedScalar, typename ParticleArray, typename ProjectionDensityArray,
                  typename WeightArray, typename PeriodicFunction>
        static void interpolation_scalar(ParticleBasedScalar &A, const ParticleArray &particles, const ProjectionDensityArray &field, T Lx,
        T Ly, T Lz, int N0, int N1, int N2, const PeriodicFunction &p,
        const WeightArray &weight) {
            impl::interpolation_scalar(A, particles, field, Lx, Ly, Lz, N0, N1, N2, p, weight, particles.shape()[0]);
        }
        
        template<typename ParticleBasedScalar, typename ParticleArray, typename ProjectionDensityArray,
                  typename WeightArray, typename PeriodicFunction>
        static void interpolation_scalar(ParticleBasedScalar &A, const ParticleArray &particles, const ProjectionDensityArray &field, T Lx,
        T Ly, T Lz, int N0, int N1, int N2, const PeriodicFunction &p) {
            impl::interpolation_scalar(A, particles, field, Lx, Ly, Lz, N0, N1, N2, p, CIC_Tools::DefaultWeight(), particles.shape()[0]);
        }
        
        template<typename ParticleBasedScalar, typename ParticleArray, typename ProjectionDensityArray,
                  typename WeightArray, typename PeriodicFunction>
        static void interpolation_scalar(ParticleBasedScalar &A, const ParticleArray &particles, const ProjectionDensityArray &field, T Lx,
        T Ly, T Lz, int N0, int N1, int N2) {
            impl::interpolation_scalar(A, particles, field, Lx, Ly, Lz, N0, N1, N2, CIC_Tools::Periodic(N0, N1, N2), CIC_Tools::DefaultWeight(), particles.shape()[0]);
        }
        
        template<typename ParticleBasedArray, typename ParticleArray, typename ProjectionDensityArray,
                 typename WeightArray, typename PeriodicFunction>
        static void interpolation(ParticleBasedArray &A, const ParticleArray &particles, const ProjectionDensityArray &field, T Lx,
        T Ly, T Lz, int N0, int N1, int N2, const PeriodicFunction &p,
        const WeightArray &weight, size_t Np) {
            impl::interpolation(A, particles, field, Lx, Ly, Lz, N0, N1, N2, p, weight, Np);
        }

        template<typename ParticleBasedArray, typename ParticleArray, typename ProjectionDensityArray,
                 typename WeightArray, typename PeriodicFunction>
        static void interpolation(ParticleBasedArray &A, const ParticleArray &particles, const ProjectionDensityArray &field, T Lx,
        T Ly, T Lz, int N0, int N1, int N2, const PeriodicFunction &p,
        const WeightArray &weight) {
            impl::interpolation(A, particles, field, Lx, Ly, Lz, N0, N1, N2, p, weight, particles.shape()[0]);
        }
        
        template<typename ParticleBasedArray, typename ParticleArray, typename ProjectionDensityArray,
                 typename WeightArray, typename PeriodicFunction>
        static void interpolation(ParticleBasedArray &A, const ParticleArray &particles, const ProjectionDensityArray &field, T Lx,
        T Ly, T Lz, int N0, int N1, int N2, const PeriodicFunction &p) {
            impl::interpolation(A, particles, field, Lx, Ly, Lz, N0, N1, N2, p, CIC_Tools::DefaultWeightDim2(), particles.shape()[0]);
        }
        
        template<typename ParticleBasedArray, typename ParticleArray, typename ProjectionDensityArray,
                 typename WeightArray, typename PeriodicFunction>
        static void interpolation(ParticleBasedArray &A, const ParticleArray &particles, const ProjectionDensityArray &field, T Lx,
        T Ly, T Lz, int N0, int N1, int N2) {
            impl::interpolation(A, particles, field, Lx, Ly, Lz, N0, N1, N2, CIC_Tools::Periodic(N0, N1, N2), CIC_Tools::DefaultWeightDim2(), particles.shape()[0]);
        }
        
        template<typename ParticleArray, typename GradientArray, typename ProjectionDensityArray, typename PeriodicFunction>
        static void adjoint(const ParticleArray& particles, ProjectionDensityArray& density,
                            GradientArray& adjoint_gradient,
                            T Lx, T Ly, T Lz,
                            int N0, int N1, int N2,
                            const PeriodicFunction& p,
                            T nmean, size_t Np) {
            impl::adjoint(particles, density, adjoint_gradient,CIC_Tools::DefaultWeight(), Lx, Ly, Lz, N0, N1, N2, p, nmean, Np);
        }

        template<typename ParticleArray, typename GradientArray, typename ProjectionDensityArray, typename PeriodicFunction>
        static void adjoint(const ParticleArray& particles, ProjectionDensityArray& density,
                            GradientArray& adjoint_gradient,
                            T Lx, T Ly, T Lz,
                            int N0, int N1, int N2,
                            const PeriodicFunction& p,
                            T nmean) {
            impl::adjoint(particles, density, adjoint_gradient,CIC_Tools::DefaultWeight(), Lx, Ly, Lz, N0, N1, N2, p, nmean, particles.shape()[0]);
        }

        template<typename ParticleArray, typename GradientArray, typename ProjectionDensityArray>
        static void adjoint(const ParticleArray& particles, ProjectionDensityArray& density,
                            GradientArray& adjoint_gradient,
                            T Lx, T Ly, T Lz,
                            int N0, int N1, int N2,
                            T nmean) {
          impl::adjoint(particles, density, adjoint_gradient,CIC_Tools::DefaultWeight(), Lx, Ly, Lz, N0, N1, N2, CIC_Tools::Periodic(N0, N1, N2), nmean, particles.shape()[0]);
        }
        
        template<typename ParticleBasedScalar, typename ParticleArray, typename ProjectionDensityArray,
        typename WeightArray, typename PeriodicFunction>
        static void adjoint_interpolation_scalar(
            int axis, ParticleBasedScalar &A, const ParticleArray &particles, const ProjectionDensityArray &field, T Lx, T Ly, T Lz, int N0, int N1, int N2, const PeriodicFunction &p, const WeightArray &weight, size_t Np) {
            impl::adjoint_interpolation_scalar(axis, A, particles, field, Lx, Ly, Lz, N0, N1, N2, p, weight, Np);
        }
        
        template<typename ParticleBasedArray, typename ParticleArray, typename ProjectionDensityArray,
                 typename WeightArray, typename PeriodicFunction>
        static void adjoint_interpolation(
            int axis, ParticleBasedArray &A, const ParticleArray &particles, const ProjectionDensityArray &field, T Lx,
            T Ly, T Lz, int N0, int N1, int N2, const PeriodicFunction &p,
            const WeightArray &weight, size_t Np) {
            impl::adjoint_interpolation(axis, A, particles, field, Lx, Ly, Lz, N0, N1, N2, p, weight, Np);
        }
        

    };

}

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
