/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_gradient_supersampling.cpp
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
#include "libLSS/tools/sigcatcher.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include <CosmoTool/algo.hpp>

using namespace LibLSS;
using CosmoTool::square;
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

typedef UninitializedArray<R_Array, Manager::AllocReal> UR_Array;
typedef UninitializedArray<F_Array, Manager::AllocComplex> UF_Array;

static const double epsilon = 1e-9;

namespace {
#if defined(ARES_MPI_FFTW)
    RegisterStaticInit reg0(fftw_mpi_init, fftw_mpi_cleanup, 9, "MPI/FFTW");
#endif
    // WISDOM must come at the end. Otherwise it is reset
    RegisterStaticInit reg1(CosmoTool::init_fftw_wisdom, CosmoTool::save_fftw_wisdom, 12, "FFTW/WISDOM");
}


template<typename RGen>
double rand_init(RGen& rgen, double fac)
{
  return rgen.gaussian_ratio();// * fac;
}

static
double filler()
{
  static long counter = 0;
  
  return 1;
}

template<typename Array>
typename Array::element chi2_sum(Manager& mgr, const Array& a)
{
  typename Array::element chi2 = 0;
  
  for (long i = mgr.startN0; i < mgr.startN0+mgr.localN0; i++)
    for (long j = 0; j < a.shape()[1]; j++)
      for (long k = 0; k < a.shape()[2]; k++)
        chi2 += CosmoTool::square(a[i][j][k]);

  return chi2;
}


template<typename A,typename B>
double forward_chi2(MPI_Communication *comm, Manager& mgr, Manager& mgr2, Manager::plan_type& plan, const A& a, const B& mu)
{      
  using boost::lambda::_1;
  using boost::lambda::_2;
  UF_Array tmp_hi(mgr2.extents_complex(), mgr2.allocator_complex);
  UR_Array r_hi_array(mgr2.extents_real(), mgr2.allocator_real);

  LibLSS::array::fill(tmp_hi.get_array(), 0);
  mgr2.upgrade_complex(mgr, a, tmp_hi.get_array());
  copy_array(tmp_hi.get_array(), b_fused<std::complex<double> >(tmp_hi.get_array(),mu,_1+_2));
  mgr2.execute_c2r(plan, tmp_hi.get_array().data(), r_hi_array.get_array().data());

  double chi2 = chi2_sum(mgr2, r_hi_array.get_array());

  comm->all_reduce_t(MPI_IN_PLACE, &chi2, 1, MPI_SUM);
  
  return chi2;
}

template<typename A, typename B>
void gradient_chi2(Manager& mgr, Manager& mgr2, Manager::plan_type& plan, const A& a, B& mu, A& c, B& d)
{      
  using boost::lambda::_1;
  using boost::lambda::_2;
  UF_Array mu_lo(mgr.extents_complex(), mgr.allocator_complex);
  UF_Array sum_hi(mgr2.extents_complex(), mgr2.allocator_complex);
  long N = mgr2.N0 * mgr2.N1 * mgr2.N2;

  LibLSS::array::fill(sum_hi.get_array(), 0);

  mgr2.upgrade_complex(mgr, a, sum_hi.get_array());
  copy_array(sum_hi.get_array(), b_fused<std::complex<double> >(sum_hi.get_array(), mu, _1+_2));
  mgr.degrade_complex(mgr2, sum_hi.get_array(), c);

  LibLSS::array::copyArray3d(d, sum_hi.get_array());
  
  LibLSS::array::scaleArray3d(c, 4*N);
  
  if (mgr.on_core(0)) {
    c[0][0][0] /= 2;
    c[0][mgr.N1/2][0] /= 2;
    c[0][0][mgr.N2/2] /= 2;
    c[0][mgr.N1/2][mgr.N2/2] /= 2;
  }

  if (mgr.on_core(mgr.N0/2)) {
    c[mgr.N0/2][0][0] /= 2;
    c[mgr.N0/2][mgr.N1/2][0] /= 2;
    c[mgr.N0/2][0][mgr.N2/2] /= 2;
    c[mgr.N0/2][mgr.N1/2][mgr.N2/2] /= 2;
  }
}

int main(int argc, char **argv)
{
    using boost::format;
    using boost::str;
    MPI_Communication *world = setupMPI(argc, argv);

    typedef RandomNumberMPI<GSL_RandomNumber> RGen;

    StaticInit::execute();    
    Console& cons = Console::instance();
    cons.outputToFile(str(format("log_test_supersampling.txt.%d") % world->rank()));
    cons.setVerboseLevel<LOG_DEBUG>();

    Manager mgr(16,16,16, world);
    Manager mgr2(32,32,32, world);
    
    {
      RGen rgen(world, -1);

      rgen.seed(97249);

      F_Array f_lo_array(mgr.extents_complex(), c_storage_order(), mgr.allocator_complex);
      F_Array tmp_f_array(mgr.extents_complex(), c_storage_order(), mgr.allocator_complex);
      F_Array gradient_ref(mgr.extents_complex(), c_storage_order(), mgr.allocator_complex);
      F_Array gradient(mgr.extents_complex(), c_storage_order(), mgr.allocator_complex);
      R_Array r_array(mgr.extents_real(), c_storage_order(), mgr.allocator_real);
      R_Array tmp_array(mgr.extents_real(), c_storage_order(), mgr.allocator_real);
      R_Array r_hi_array(mgr2.extents_real(), c_storage_order(), mgr2.allocator_real);
      F_Array f_hi_array(mgr2.extents_complex(), c_storage_order(), mgr2.allocator_complex);
      F_Array tmp_gradient(mgr2.extents_complex(), c_storage_order(), mgr2.allocator_complex);
      F_Array mu(mgr2.extents_complex(), c_storage_order(), mgr2.allocator_complex);
      Manager::plan_type plan_r2c = mgr.create_r2c_plan(r_array.data(), f_lo_array.data());
      Manager::plan_type plan_r2c_hi = mgr2.create_r2c_plan(r_hi_array.data(), f_hi_array.data());
      Manager::plan_type plan_c2r_hi = mgr2.create_c2r_plan(f_hi_array.data(), r_hi_array.data());

      double fac = 1/double(r_array.num_elements());

      copy_array(r_hi_array, b_fused<double, 3>( bind(rand_init<RGen>, boost::ref(rgen), 1) ) );
      mgr2.execute_r2c(plan_r2c_hi, r_hi_array.data(), mu.data());
      LibLSS::array::scaleArray3d(mu, 1.0/r_hi_array.num_elements());

      // Generate random numbers
      copy_array(r_array, b_fused<double, 3>( bind(rand_init<RGen>, boost::ref(rgen), fac) ) );          
      // Save them
      LibLSS::array::copyArray3d(tmp_array, r_array);
      mgr.execute_r2c(plan_r2c, tmp_array.data(), f_lo_array.data());
      LibLSS::array::scaleArray3d(f_lo_array, 1.0/r_array.num_elements());

      LibLSS::array::fill(gradient_ref, 0);

      double chi2 = forward_chi2(world, mgr, mgr2, plan_c2r_hi, f_lo_array, mu);
      for (long i = 0; i < mgr.N0; i++) {
        for (long j = 0; j < mgr.N1; j++) {
          for (long k = 0; k < mgr.N2_HC; k++) {
            std::complex<double> delta(0,0);

            cons.print<LOG_DEBUG>(format("doing %d,%d,%d") % i % j % k);
            LibLSS::array::copyArray3d(tmp_f_array, f_lo_array);
            if (mgr.on_core(i))
              tmp_f_array[i][j][k] = f_lo_array[i][j][k] + std::complex<double>(epsilon,0);
            if (k==mgr.N2/2 || k == 0) {
              long plane = (mgr.N0-i)%mgr.N0;
              F_Array::element value = 0;
              
              if (mgr.on_core(plane)) {
                if (world->size() > 1 && !mgr.on_core(i)) 
                  world->recv(&value, 1, translateMPIType<F_Array::element>(), mgr.get_peer(i), i);
                else
                  value = tmp_f_array[i][j][k];
        
                tmp_f_array[plane][(mgr.N1-j)%mgr.N1][k] = std::conj(value);
              } else if (mgr.on_core(i)) {
                world->send(&tmp_f_array[i][j][k], 1, translateMPIType<F_Array::element>(), mgr.get_peer(plane), i);
              }
            }
           
            delta.real((forward_chi2(world, mgr, mgr2, plan_c2r_hi, tmp_f_array, mu) - chi2)/epsilon);

            if (mgr.on_core(i))
              tmp_f_array[i][j][k] = f_lo_array[i][j][k] + std::complex<double>(0,epsilon);
            if (k==mgr.N2/2 || k == 0) {
              long plane = (mgr.N0-i)%mgr.N0;
              F_Array::element value = 0;

              if (mgr.on_core(i) && plane == i && (mgr.N1-j)%mgr.N1 == j) {
                tmp_f_array[i][j][k].imag(0);
              }
              if (mgr.on_core(plane)) {
                  if (world->size() > 1 && !mgr.on_core(i)) 
                    world->recv(&value, 1, translateMPIType<F_Array::element>(), mgr.get_peer(i), i);
                  else
                    value = tmp_f_array[i][j][k];
                  tmp_f_array[plane][(mgr.N1-j)%mgr.N1][k] = std::conj(value);
              } else if (mgr.on_core(i)) {
                  world->send(&tmp_f_array[i][j][k], 1, translateMPIType<F_Array::element>(), mgr.get_peer(plane), i);
              }
            }

            delta.imag((forward_chi2(world, mgr, mgr2, plan_c2r_hi, tmp_f_array, mu) - chi2)/epsilon);
            if (mgr.on_core(i))
                gradient_ref[i][j][k] = delta;
          }
        }
      }
      world->barrier();

      LibLSS::array::fill(gradient, 0);
      gradient_chi2(mgr, mgr2, plan_c2r_hi, f_lo_array, mu, gradient, tmp_gradient);

      // Now we have our modes
      {
        string s = boost::str(boost::format("test_grad_degrade.h5_%d") % world->rank());
        H5::H5File f(s, H5F_ACC_TRUNC);
        hdf5_write_array(f, "gradient_ref", gradient_ref);
        hdf5_write_array(f, "gradient", gradient);
        hdf5_write_array(f, "gradient_hi", tmp_gradient);
        hdf5_write_array(f, "mu", mu);
        hdf5_write_array(f, "lo", f_lo_array);
        
        mgr2.upgrade_complex(mgr, f_lo_array, f_hi_array);
        hdf5_write_array(f, "hi", f_hi_array);

      }
    }
    
    world->barrier();
    StaticInit::finalize();
    return 0;
}
