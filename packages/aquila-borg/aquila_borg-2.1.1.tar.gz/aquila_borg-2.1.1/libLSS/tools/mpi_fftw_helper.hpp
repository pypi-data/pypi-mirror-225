/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/mpi_fftw_helper.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_FFTW_HELPER_HPP
#define __LIBLSS_FFTW_HELPER_HPP

#include <boost/type_traits/remove_reference.hpp>
#include <boost/type_traits/is_same.hpp>
#include <boost/multi_array.hpp>
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/uninitialized_type.hpp"

#define DEBUG_MPI_DEGRADE

#ifdef DEBUG_MPI_DEGRADE
#define CHECK_NYQ(q) Console::instance().c_assert(nyqCheck[q], "Plane not imported")
#endif

namespace LibLSS {

    template<typename T, int Nd = 3> class FFTW_Manager;
    template<typename T> using FFTW_Manager_3d = FFTW_Manager<T,3>;

    namespace internal {
        template<typename T> struct padding_multiplier {};

        template<> struct padding_multiplier<double> {
            enum { multiplier = 2 };
        };

        template<> struct padding_multiplier<float> {
            enum { multiplier = 2 };
        };

        template<> struct padding_multiplier<std::complex<double> > {
            enum { multiplier = 1 };
        };

        template<> struct padding_multiplier<std::complex<float> > {
            enum { multiplier = 1 };
        };

        template<typename T>
        void safe_delete(T *& p) {
          if (p != 0) {
            delete p;
            p = 0;
          }
        }

        template<typename T, bool upgrading>
        struct AssignOperator {
          void clear(std::complex<T>& a) const {  }
          // Natural degrade
          void operator()(std::complex<T>& a, const std::complex<T>& b, bool nyq, bool nyq2) const {
            if (upgrading) {
                a = b;
            } else {
              T f = 1;
              if (nyq) f *= 0.5;
              if (nyq2) f *= 0.5;
              a += f*b;
            }
          }
        };

        template<typename T>
        struct AccumOperator {
          void clear(std::complex<T>& a) const { }
          // Natural degrade
          void operator()(std::complex<T>& a, const std::complex<T>& b, bool nyq, bool nyq2) const {
              T f = 0.5;
              if (nyq) f *= 0.5;
              if (nyq2) f *= 0.5;
              a += f*b;
            }
        };

        template<typename T, bool upgrading> struct Nyquist_adjust;

        #include "mpi_fftw/copy_utils.hpp"
        #include "mpi_fftw/nyquist_upgrade.hpp"
        #include "mpi_fftw/nyquist_downgrade.hpp"

    };


    template<typename ArrayType>
    inline bool copy_padded_data(
        const ArrayType& a,
        typename ArrayType::element *padded_a, bool only_mpi = false)
    {
        typedef typename ArrayType::element ElementType;
        using internal::padding_multiplier;
        long N0 = a.shape()[0], N1 = a.shape()[1], N2 = a.shape()[2];
        long s_j = padding_multiplier<ElementType>::multiplier * (N2/2 + 1);
#ifdef ARES_MPI_FFTW
        long s_i = N1 * s_j;
        long s = a.index_bases()[0];

        for (long i = 0; i < N0; i++)
          for (long j = 0; j < N1; j++)
            for (long k = 0 ; k < N2; k++)
              padded_a[i * s_i + j * s_j + k] = a[i+s][j][k];
        return true;
#else
        if (!only_mpi)
            memcpy(padded_a, a.data(), sizeof(typename ArrayType::element) * a.num_elements());
        return false;
#endif
    }

    template<typename ArrayType>
    inline bool copy_unpadded_data(
        const typename ArrayType::element *padded_a,
        ArrayType& a, bool only_mpi = false)
    {
#ifdef ARES_MPI_FFTW
        long N0 = a.shape()[0], N1 = a.shape()[1], N2 = a.shape()[2];
        long s_j = 2 * (N2/2 + 1);
        long s_i = N1 * s_j;
        long s = a.index_bases()[0];

        for (long i = 0; i < N0; i++)
          for (long j = 0; j < N1; j++)
            for (long k = 0 ; k < N2; k++)
              a[i+s][j][k] = padded_a[i * s_i + j * s_j + k];
        return true;
#else
        if (!only_mpi)
            memcpy(a.data(), padded_a, sizeof(typename ArrayType::element) * a.num_elements());
        return false;
#endif
    }

    template<std::size_t NumDims>
    boost::general_storage_order<NumDims> get_fftw_order() {
      typedef boost::general_storage_order<NumDims> order;
#ifdef ARES_MPI_FFTW
      typedef typename order::size_type size_type;

      boost::array<size_type, NumDims> ordering;
      boost::array<bool, NumDims> ascending;

      if (NumDims >= 2) {
        for (size_type i = 2; i != NumDims; i++) {
          ordering[i] = NumDims - 1 - i;
          ascending[i] = true;
        }

        ordering[0] = 1;
        ordering[1] = 0;
        ascending[0] = ascending[1] = true;

      } else if (NumDims == 1) {
        ordering[0] = 0;
        ascending[0] = true;
      }
      return order(ordering.begin(), ascending.begin());
#else
      return order(boost::c_storage_order());
#endif
    }

#include "libLSS/tools/mpi_fftw/impl_3d.hpp"

}

#ifdef DEBUG_MPI_DEGRADE
#undef CHECK_NYQ
#endif
#endif
