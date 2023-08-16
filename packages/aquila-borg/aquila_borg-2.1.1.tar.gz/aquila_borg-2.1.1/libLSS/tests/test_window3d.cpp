/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_window3d.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <string>
#include "libLSS/mpi/generic_mpi.hpp"
#include <cmath>
#include <healpix_cxx/healpix_map.h>
#include <boost/multi_array.hpp>
#include <boost/array.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/data/window3d.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"
#include <CosmoTool/hdf5_array.hpp>

static const int N0 = 128;

struct BasicSelFunction
{
    Healpix_Map<double> C;

    double getRadialSelection(double r, int i) const {
        return std::exp(-0.5*(r*r/400.));
    }
    
    int getNumRadial() const { return 1; }
    
    double get_sky_completeness(double x, double y, double z) const { 
        return C[C.vec2pix(vec3(x,y,z))];
    }
    
    double get_sky_completeness(double ra, double dec) const { 
        return C[C.ang2pix(pointing(0.5*M_PI-dec, ra))];
    }

};

using namespace LibLSS;

int main(int argc, char **argv)
{
    Console& console = Console::instance();
    MPI_Communication *comm = LibLSS::setupMPI(argc, argv);
    boost::multi_array<double, 3> selFuncData(boost::extents[N0][N0][N0]);
    double L[3] = {200.,200.,200.};
    double xmin[3] = {-100,-100,-100};
    double delta[3] = {200./N0, 200./N0, 200./N0 };
    StaticInit::execute();

    RandomNumberThreaded<GSL_RandomNumber> rng(-1);
    
    console.setVerboseLevel<LOG_INFO>();
    
    LibLSS::smp_set_nested(true);
    
    BasicSelFunction sel;
    
    sel.C.SetNside(1, RING);
    sel.C.fill(0);
    sel.C[0] = 1.0;

    compute_window_value_elem(comm, rng, sel,  selFuncData, L, delta, xmin, 0.001);
    
    H5::H5File f("test_window.h5", H5F_ACC_TRUNC);
    CosmoTool::hdf5_write_array(f, "selData", selFuncData);
    
    return 0;
}
