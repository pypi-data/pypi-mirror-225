/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_supersampling.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <H5Cpp.h>
#include <CosmoTool/hdf5_array.hpp>
#include <boost/bind/bind.hpp>
#include <complex>
#include <boost/lambda/lambda.hpp>
#include <boost/multi_array.hpp>
#include "libLSS/samplers/rgen/gsl_random_number.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"

using namespace LibLSS;
using namespace std;
using boost::bind;
using boost::c_storage_order;
using boost::ref;
using CosmoTool::hdf5_write_array;
using boost::lambda::constant;
using boost::placeholders::_1;

typedef FFTW_Manager_3d<double> Manager;
typedef Manager::ArrayFourier F_Array;
typedef Manager::ArrayReal R_Array;

namespace {
#if defined(ARES_MPI_FFTW)
    RegisterStaticInit reg0(fftw_mpi_init, fftw_mpi_cleanup, 9, "MPI/FFTW");
#endif
    // WISDOM must come at the end. Otherwise it is reset
    RegisterStaticInit reg1(CosmoTool::init_fftw_wisdom, CosmoTool::save_fftw_wisdom, 12, "FFTW/WISDOM");
/*#if defined(_OPENMP) // Do not use MPI and Threaded FFTW at the same time for the moment.
    RegisterStaticInit reg2(fftw_init_threads, fftw_cleanup_threads, 11, "FFTW/THREADS");
#endif*/
}


template<typename RGen>
double rand_init(RGen *rgen, double fac)
{
  return rgen->gaussian_ratio() * fac;
}

static
double filler()
{
  static long counter = 0;
  
  return 1;
}

int main(int argc, char **argv)
{
  using boost::format;
  using boost::str;
  namespace Larray = LibLSS::array;
    MPI_Communication *world = setupMPI(argc, argv);

    StaticInit::execute();    
    Console::instance().outputToFile(str(format("log_test_supersampling.txt.%d") % world->rank()));
    Console::instance().setVerboseLevel<LOG_DEBUG>();

    Manager mgr(16,16,16, world);
    Manager mgr2(32,32,32, world);
    
    {
      F_Array f_array(mgr.extents_complex(), c_storage_order(), mgr.allocator_complex);
      F_Array f2_array(mgr2.extents_complex(), c_storage_order(), mgr2.allocator_complex);
      F_Array f3_array(mgr2.extents_complex(), c_storage_order(), mgr2.allocator_complex);
      F_Array f4_array(mgr.extents_complex(), c_storage_order(), mgr.allocator_complex);
      R_Array r0_array(mgr.extents_real(), c_storage_order(), mgr.allocator_real);
      R_Array r_array(mgr.extents_real(), c_storage_order(), mgr.allocator_real);
      R_Array r2_array(mgr2.extents_real(), c_storage_order(), mgr2.allocator_real);
      R_Array r3_array(mgr2.extents_real(), c_storage_order(), mgr2.allocator_real);
      R_Array r4_array(mgr.extents_real(), c_storage_order(), mgr.allocator_real);
      R_Array r5_array(mgr.extents_real(), c_storage_order(), mgr.allocator_real);

      R_Array r_hi_array(mgr2.extents_real(), c_storage_order(), mgr2.allocator_real);
      R_Array tmp_hi(mgr2.extents_real(), c_storage_order(), mgr2.allocator_real);
      R_Array r_lo_array(mgr.extents_real(), c_storage_order(), mgr.allocator_real);

      F_Array f_hi_array(mgr2.extents_complex(), c_storage_order(), mgr2.allocator_complex);
      F_Array f_hi2_array(mgr2.extents_complex(), c_storage_order(), mgr2.allocator_complex);
      F_Array tmp_f_lo(mgr.extents_complex(), c_storage_order(), mgr.allocator_complex);
      F_Array f_lo_array(mgr.extents_complex(), c_storage_order(), mgr.allocator_complex);

      
      Manager::plan_type plan_r2c = mgr.create_r2c_plan(r_array.data(), f_array.data());
      Manager::plan_type plan_c2r_lo = mgr.create_c2r_plan(f_array.data(), r_array.data());

      Manager::plan_type plan_r2c_hi = mgr2.create_r2c_plan(r_hi_array.data(), f_hi_array.data());
      Manager::plan_type plan_c2r = mgr2.create_c2r_plan(f3_array.data(), r2_array.data());

      typedef RandomNumberMPI<GSL_RandomNumber> RGen;
      
      {
        RGen rgen(world, -1);
        double fac = 1.0/(mgr.N0*mgr.N1*mgr.N2);
        boost::function0<double> ff = bind(rand_init<RGen>, &rgen, fac);

        rgen.seed(2012145);
          
        Console::instance().print<LOG_DEBUG>(format("ff = %lg") % ff());
          
        copy_array(r_array,         b_fused<double, 3>(bind(rand_init<RGen>, &rgen, fac))); 
        r0_array = r_array;
        
        mgr.execute_r2c(plan_r2c, r_array.data(), f_array.data());

        mgr2.upgrade_complex(mgr, f_array, f2_array);
        mgr.degrade_complex(mgr2, f2_array, f4_array);
        
        Larray::copyArray3d(f3_array, f2_array);
        mgr2.execute_c2r(plan_c2r, f3_array.data(), r2_array.data());
        Larray::scaleArray3d(r2_array, 1./16./16./16.);
  ///      mgr.degrade_real(mgr2, r2_array, r_array);

        Larray::fill(r3_array, 1);
  ////      mgr.degrade_real(mgr2, r3_array, r4_array);
  ////     r3_array[2][2][2] = 0;
  ////      mgr.degrade_real(mgr2, r3_array, r5_array);

        copy_array(r_hi_array, b_fused<double, 3>( ff ) );          
        Larray::copyArray3d(tmp_hi, r_hi_array);
        mgr2.execute_r2c(plan_r2c_hi, tmp_hi.data(), f_hi_array.data());
        
        Larray::scaleArray3d(f_hi_array, 1./(mgr.N0*mgr.N1*mgr.N2));
        
        mgr.degrade_complex(mgr2, f_hi_array, f_lo_array);
        mgr2.upgrade_complex(mgr, f_lo_array, f_hi2_array);

        Larray::copyArray3d(tmp_f_lo, f_lo_array);
        
        mgr.execute_c2r(plan_c2r_lo, tmp_f_lo.data(), r_lo_array.data());

        {
          string s = boost::str(boost::format("test_upgrade.h5_%d") % world->rank());
          H5::H5File f(s, H5F_ACC_TRUNC);
          hdf5_write_array(f, "ref", f_array);
          hdf5_write_array(f, "upgrade", f2_array);
          hdf5_write_array(f, "degrade_complex", f4_array);
          hdf5_write_array(f, "ref0", r0_array);
          hdf5_write_array(f, "upgrade_real", r2_array);
          hdf5_write_array(f, "updowngrade", r_array);
          hdf5_write_array(f, "down_a", r4_array);
          hdf5_write_array(f, "down_b", r5_array);
          
          hdf5_write_array(f, "hi__r_hi", r_hi_array);
          hdf5_write_array(f, "hi__f_hi", f_hi_array);
          hdf5_write_array(f, "hi__f_hi2", f_hi2_array);
          hdf5_write_array(f, "hi__f_lo", f_lo_array);
          hdf5_write_array(f, "hi__r_lo", r_lo_array);
        }
      }
    }
        
    world->barrier();
    StaticInit::finalize();
    doneMPI();
    return 0;
}
