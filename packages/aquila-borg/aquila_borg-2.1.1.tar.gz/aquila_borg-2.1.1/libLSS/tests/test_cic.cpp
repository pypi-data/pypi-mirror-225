/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_cic.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <cmath>
#include <CosmoTool/algo.hpp>
#include <boost/multi_array.hpp>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/uninitialized_type.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/physics/classic_cic.hpp"
#include "libLSS/physics/openmp_cic.hpp"
#include "libLSS/physics/cosmo.hpp"
#include <H5Cpp.h>
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/tools/hdf5_error.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"
#include <boost/chrono.hpp>

#undef RANDOM_ACCESS
//#define RANDOM_ACCESS

using namespace LibLSS;
using CosmoTool::cube;

typedef ClassicCloudInCell<double> CIC;
#ifdef _OPENMP
typedef OpenMPCloudInCell<double> CIC_MP;
#endif

int main(int argc, char **argv) {
  MPI_Communication *world = setupMPI(argc, argv);
  StaticInit::execute();
  CosmologicalParameters cosmo;
  cosmo.omega_m = 0.30;
  cosmo.omega_b = 0.045;
  cosmo.omega_q = 0.70;
  cosmo.w = -1;
  cosmo.n_s = 0.97;
  cosmo.sigma8 = 0.8;
  cosmo.h = 0.68;
  cosmo.a0 = 1.0;

  Console::instance().setVerboseLevel<LOG_DEBUG>();

  double L = 1.0;
  int N = 64;
  int Np_g = 128;
  int Np = cube(Np_g);
  typedef UninitializedArray<boost::multi_array<double, 3>> U_Density;
  typedef UninitializedArray<boost::multi_array<double, 2>> U_Particles;
  U_Density density_p(boost::extents[N][N][N]);
  U_Density density_mp_p(boost::extents[N][N][N]);
  U_Particles particles_p(boost::extents[Np][3]);
  U_Density::array_type &density = density_p.get_array();
  U_Density::array_type &density_mp = density_mp_p.get_array();
  U_Particles::array_type &particles = particles_p.get_array();
  CIC cic;
#ifdef _OPENMP
  CIC_MP cic_mp;
#endif

#ifdef RANDOM_ACCESS
  RandomNumberThreaded<GSL_RandomNumber> rgen(-1);

#  pragma omp parallel for schedule(static)
  for (long i = 0; i < Np; i++) {
    particles[i][0] = L * rgen.uniform();
    particles[i][1] = L * rgen.uniform();
    particles[i][2] = L * rgen.uniform();
  }
#else

#  pragma omp parallel for schedule(static)
  for (long i = 0; i < Np; i++) {
    int iz = (i % Np_g);
    int iy = ((i / Np_g) % Np_g);
    int ix = ((i / Np_g / Np_g));
    particles[i][0] = L / Np_g * ix;
    particles[i][1] = L / Np_g * iy;
    particles[i][2] = L / Np_g * iz;
  }

#endif

  Console::instance().print<LOG_INFO>("Clearing and projecting");
  array::fill(density, 0);
  array::fill(density_mp, 0);

  using namespace boost::chrono;
  system_clock::time_point start_classic, end_classic, start_mp, end_mp;

  start_classic = system_clock::now();
  cic.projection(particles, density, L, L, L, N, N, N);
  end_classic = system_clock::now();

  start_mp = system_clock::now();
#ifdef _OPENMP
  cic_mp.projection(particles, density_mp, L, L, L, N, N, N);
#endif
  end_mp = system_clock::now();

  duration<double> elapsed_classic = end_classic - start_classic;
  duration<double> elapsed_mp = end_mp - start_mp;

  std::cout << "OpenMP: " << elapsed_mp << "  Classic: " << elapsed_classic
            << std::endl;

  try {
    H5::H5File f("cic.h5", H5F_ACC_TRUNC);
    CosmoTool::hdf5_write_array(f, "density", density);
    CosmoTool::hdf5_write_array(f, "density_mp", density_mp);
  } catch (const H5::FileIException &) {
    Console::instance().print<LOG_ERROR>(
        "Failed to load ref_pm.h5 in the current directory. Check in the "
        "source directory libLSS/tests/");
    return 1;
  }

  return 0;
}
