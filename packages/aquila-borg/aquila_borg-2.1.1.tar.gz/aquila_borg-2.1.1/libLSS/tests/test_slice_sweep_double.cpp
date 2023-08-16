/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_slice_sweep_double.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <H5Cpp.h>
#include <stdlib.h>
#include <boost/chrono.hpp>
#include <boost/format.hpp>
#include <boost/multi_array.hpp>
#include "libLSS/tools/static_init.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"
#include "libLSS/samplers/rgen/slice_sweep.hpp"
#include "libLSS/mpi/generic_mpi.hpp"

using boost::multi_array;
using boost::extents;

using namespace LibLSS;

static const int Ntry=100;

double likelihood1(double x)
{
  return std::log(std::exp(-(x-1)*(x-1)/2) + std::exp(-(x-6)*(x-6)/2));
}

int main(int argc, char **argv)
{
      MPI_Communication *comm = LibLSS::setupMPI(argc, argv);
      StaticInit::execute();
          
      Console::instance().setVerboseLevel<LOG_DEBUG>();
                  
      RandomNumberThreaded<GSL_RandomNumber> rgen(-1);


      multi_array<double, 1> a(extents[2*Ntry]);
      double v = 0;

      for (int i = 0; i < Ntry; i++)
      {
        a[i] = v =  LibLSS::slice_sweep_double(comm, rgen, likelihood1, v, 1e-2);
      }
      for (int i = 0; i < Ntry; i++)
      {
        a[Ntry+i] = v =  LibLSS::slice_sweep_double(comm, rgen, likelihood1, v, 1e4);
      }


      {
        H5::H5File f("test_sweep.h5", H5F_ACC_TRUNC);

        CosmoTool::hdf5_write_array(f, "lh1", a);
      }

      return 0;

}
