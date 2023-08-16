/*+
    ARES/HADES/BORG Package -- ./libLSS/data/window3d_post.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_DATA_WINDOW_3D_POST_HPP
#define __LIBLSS_DATA_WINDOW_3D_POST_HPP

#include <cassert>
#include <functional>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/openmp.hpp"
#include <CosmoTool/algo.hpp>
#include <boost/array.hpp>
#include <numeric>
#include <cmath>
#include "libLSS/tools/console.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/fusewrapper.hpp"

namespace LibLSS {

    namespace convolveDetails {
      template<typename RealArray>
      void buildKernel(FFTW_Manager_3d<double>& mgr, RealArray& real_data) {
        constexpr double KernelCore[2] = {1, 0.5};
        decltype(mgr.N0) N[3] = {mgr.N0, mgr.N1, mgr.N2};

        for (int i = -1; i <= 1; i++) {
          size_t ri = (i < 0) ? (N[0]+i) : i;
          if (!mgr.on_core(ri))
            continue;
          size_t ai = std::abs(i);
          for (int j = -1; j<= 1; j++) {
            size_t rj = (j < 0) ? (N[1]+j) : j;
            size_t aj = std::abs(j);
            for (int k = -1; k <= 1; k++) {
              size_t rk = (k < 0) ? (N[2]+k) : k;
              size_t ak = std::abs(k);

              real_data[ri][rj][rk] =  KernelCore[ai]*KernelCore[aj]*KernelCore[ak];
            }
          }
        }
      }
    }

    template<typename SelectionArray, typename T>
    void convolve_selection_cic(MPI_Communication *comm, SelectionArray& sel_array, T const* N)
    {

      typedef FFTW_Manager_3d<double> DFT_Manager;
      typedef typename DFT_Manager::plan_type plan_type;
      ConsoleContext<LOG_DEBUG> ctx("convolution of selection function");

      DFT_Manager mgr(N[0], N[1], N[2], comm);

      Uninit_FFTW_Real_Array real_data_p(mgr.extents_real(), mgr.allocator_real);
      Uninit_FFTW_Complex_Array complex_data_p(mgr.extents_complex(), mgr.allocator_complex);
      Uninit_FFTW_Complex_Array kernel_data_p(mgr.extents_complex(), mgr.allocator_complex);
      auto real_data = real_data_p.get_array();
      auto complex_data = complex_data_p.get_array();
      auto kernel_data = kernel_data_p.get_array();
      auto wc = fwrap(complex_data);
      auto wr = fwrap(real_data);
      auto kc = fwrap(kernel_data);

      ctx.print("Create plans");
      plan_type analysis_plan = mgr.create_r2c_plan(real_data.data(), complex_data.data());
      plan_type synthesis_plan = mgr.create_c2r_plan(complex_data.data(), real_data.data());

      ctx.print("Kernel building");
      wr = 0;
      convolveDetails::buildKernel(mgr, real_data);
      mgr.execute_r2c(analysis_plan, real_data.data(), kernel_data.data());

      ctx.print("Convolve");
      LibLSS::copy_array(real_data, sel_array);
      mgr.execute_r2c(analysis_plan, real_data.data(), complex_data.data());


      wc = wc * kc * (1.0/(N[0]*N[1]*N[2]));

      mgr.execute_c2r(synthesis_plan, complex_data.data(), real_data.data());
      
      auto S = fwrap(sel_array) ;
      
      // This is a mask operation, if the condition is true, then S is copied on itself (thus noop).
      // If the condition is false, then the value is cleared with zero. The wrapping of constant
      // is not trivial at the moment. 
      S = mask((S>0)&&(wr>=0), S, fwrap(S.fautowrap(0)));
      
      ctx.print("Cleaning up");
      mgr.destroy_plan(analysis_plan);
      mgr.destroy_plan(synthesis_plan);
    }

}

#endif
