/*+
    ARES/HADES/BORG Package -- ./libLSS/data/window3d.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_WINDOW_3D_HPP
#define __LIBLSS_WINDOW_3D_HPP

#include <cassert>
#include <functional>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/openmp.hpp"
#include "libLSS/samplers/rgen/gsl_miser.hpp"
#include <CosmoTool/algo.hpp>
#include <boost/array.hpp>
#include <numeric>
#include <cmath>

namespace LibLSS {

    namespace internalWindow {

      template<typename SelFunction3d>
      double selectionValue(double *k, const SelFunction3d& selfunc) {
        double r = std::sqrt(k[0]*k[0]+k[1]*k[1]+k[2]*k[2]);

        return selfunc.get_sky_completeness(k[0]/r, k[1]/r, k[2]/r) * selfunc.getRadialSelection(r, 0);
      }

      template<typename SelFunction3d>
      double selectionValue_just_sky(double *k, const SelFunction3d& selfunc) {
        return selfunc.get_sky_completeness(k[0], k[1], k[2]);
      }

    }

    template<typename RandomNum, typename SelFunction3d, typename SelFuncMask, typename Dimension>
    void compute_window_value_elem(
                    MPI_Communication *comm,
                    RandomNum& rng,
                    const SelFunction3d& selfunc,
                    SelFuncMask& selfuncData,
                    const Dimension& L,
                    const Dimension& d,
                    const Dimension& xmin, bool filter_mask,
                    double precision = 0.01)
    {
        using boost::str;
        using boost::format;

        Console& cons = Console::instance();
        boost::multi_array<int,1> count_elements(boost::extents[LibLSS::smp_get_max_threads()]);
        size_t startN0 = selfuncData.index_bases()[0];
        size_t localN0 = selfuncData.shape()[0], N1 = selfuncData.shape()[1], N2 = selfuncData.shape()[2];
        double d0=d[0];
        double d1=d[1];
        double d2=d[2];
        double xmin0 = xmin[0];
        double xmin1 = xmin[1];
        double xmin2 = xmin[2];
        size_t N0 = L[0]/d0; // This is HACK

        double refVolume = CosmoTool::square(precision/0.01)*CosmoTool::cube(3);  // Ref is 3 Mpc,

        size_t calls = 10 + size_t(1000 * (d0*d1*d2 / refVolume));

        cons.indent();

        Progress<LOG_STD>& p = cons.start_progress<LOG_STD>("3D Window", localN0*N1*N2, 2);

        cons.print<LOG_INFO>(
            format("Use a tolerance of %g on window function integral / calls = %d")
                    % precision % calls);

        std::fill(count_elements.begin(), count_elements.end(), 0);

        long job_start = startN0*N1*N2;
        long job_end =  (startN0+localN0)*N1*N2;

        cons.print<LOG_DEBUG>(
            format("Window computation, MPI job_start=%ld job_end=%ld") % job_start % job_end
        );
        cons.print<LOG_DEBUG>(
            format("Max threads = %d, ID = %d") % LibLSS::smp_get_max_threads() % LibLSS::smp_get_thread_id());
        cons.print<LOG_DEBUG>(
            format("d=[%g,%g,%g], L=[%g,%g,%g]") % d[0] % d[1] % d[2] % L[0] % L[1] % L[2]
        );

        double dV = d0*d1*d2;


        typedef boost::multi_array_types::extent_range range;
        boost::multi_array<bool,3> dummy(boost::extents[range(startN0,startN0+localN0)][N1][N2]);
        boost::multi_array<double,3> all_err(boost::extents[range(startN0,startN0+localN0)][N1][N2]);
        double mask_th = 0.5; //the voxel should have been observed at least to 50 percent

#pragma omp parallel
        {
          GSL_Miser miser(3);

#pragma omp for schedule(dynamic,100)
          for(size_t i=job_start;i<job_end;i++) {
            ///get 3d indices
            size_t ii=(size_t) (i/N1/N2);
            size_t jj=(size_t) (i/N2 - ii *N1);
            size_t kk=(size_t) (i-jj*N2-ii*N2*N1);

            double
              x = double(ii)*d0+xmin0,
              y = double(jj)*d1+xmin1,
              z = double(kk)*d2+xmin2;
            double err;
            boost::array<double, 3> xl{x - 0.5*d0, y-0.5*d1, z-0.5*d2};
            boost::array<double, 3> xu{x + 0.5*d0, y + 0.5*d1, z + 0.5*d2};

            //here we do a pre-run, where we project the sky completeness into 3d
            double auxval;
            if (filter_mask) {
              auxval = miser.integrate(rng,
                    std::bind(&internalWindow::selectionValue_just_sky<SelFunction3d>, std::placeholders::_1, std::cref(selfunc)),
                    xl, xu, calls, err) / (dV);
            } else {
              auxval =  mask_th*2;
            }

            //avoid double calculations for uninteresting mask regions
            if(auxval > mask_th) {
              dummy[ii][jj][kk]=true;

              selfuncData[ii][jj][kk] =
                miser.integrate(rng,
                      std::bind(&internalWindow::selectionValue<SelFunction3d>, std::placeholders::_1, std::cref(selfunc)),
                      xl, xu, calls, err) / (dV);
               all_err[ii][jj][kk] = err;
            } else {
              selfuncData[ii][jj][kk] = 0.;
            }

            assert(LibLSS::smp_get_thread_id() < LibLSS::smp_get_max_threads());
            count_elements[LibLSS::smp_get_thread_id()]++;
            if (LibLSS::smp_get_thread_id() == 0) {
                int done = std::accumulate(count_elements.begin(), count_elements.end(), 0);
                p.update(done);
            }
          }
        }

        cons.unindent();
        p.destroy();
if (false)
        {
          H5::H5File f("window_err.h5", H5F_ACC_TRUNC);
          CosmoTool::hdf5_write_array(f, "errors", all_err);
          CosmoTool::hdf5_write_array(f, "sel", selfuncData);
        }

        ///now delete from mask
        #pragma omp parallel for collapse(3)
        for (size_t n0 = startN0; n0 < startN0+localN0; n0++) {
            for (size_t n1 = 0; n1 < N1; n1++) {
                for (size_t n2 = 0; n2 < N2; n2++) {
                  if(!dummy[n0][n1][n2])
                    selfuncData[n0][n1][n2] = 0.;
                }
              }
        }
    }
};

#endif
