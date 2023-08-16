/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/core/types_samplers.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TYPES_SAMPLERS_HPP
#define __LIBLSS_TYPES_SAMPLERS_HPP

#include "libLSS/mpi/generic_mpi.hpp"
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#ifdef ARES_MPI_FFTW
#  include <CosmoTool/fourier/fft/fftw_calls_mpi.hpp>
#endif
#include "libLSS/tools/fftw_allocator.hpp"
#include "libLSS/tools/uninitialized_type.hpp"
#include "libLSS/mcmc/state_element.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include <boost/multi_array/storage_order.hpp>
#include "libLSS/tools/memusage.hpp"

namespace LibLSS {

  template <typename T, size_t N>
  using multi_array = boost::multi_array<T, N, LibLSS::track_allocator<T>>;

  template <typename T, size_t N>
  using const_multi_array_ref = boost::const_multi_array_ref<T, N>;

  template <typename T, size_t N>
  using multi_array_ref = boost::multi_array_ref<T, N>;

  typedef CosmoTool::FFTW_Calls<double> FCalls;
#ifdef ARES_MPI_FFTW
  typedef CosmoTool::FFTW_MPI_Calls<double> MPI_FCalls;
  typedef MPI_FCalls MFCalls;
#else
  typedef FCalls MFCalls;
#endif
  typedef ScalarStateElement<long> SLong;
  typedef ScalarStateElement<double> SDouble;
  typedef ScalarStateElement<bool> SBool;
  typedef ArrayStateElement<double, 3, FFTW_Allocator<double>, true> ArrayType;
  typedef ArrayStateElement<
      std::complex<double>, 3, FFTW_Allocator<std::complex<double>>, true>
      CArrayType;
  typedef ArrayStateElement<int, 3, LibLSS::track_allocator<int>, true>
      IArrayType;
  typedef ArrayStateElement<double, 1, LibLSS::track_allocator<double>>
      ArrayType1d;
  typedef ArrayStateElement<int, 1, LibLSS::track_allocator<int>> IArrayType1d;
  typedef RandomStateElement<RandomNumber> RandomGen;
  typedef ArrayStateElement<double, 3, FFTW_Allocator<double>, true>
      SelArrayType;

  typedef CArrayType::ArrayType FFTW_Complex_Array;
  typedef ArrayType::ArrayType FFTW_Real_Array;

  typedef CArrayType::RefArrayType FFTW_Complex_Array_ref;
  typedef ArrayType::RefArrayType FFTW_Real_Array_ref;

  typedef UninitializedArray<
      FFTW_Complex_Array, FFTW_Allocator<std::complex<double>>>
      Uninit_FFTW_Complex_Array;
  typedef UninitializedArray<FFTW_Real_Array, FFTW_Allocator<double>>
      Uninit_FFTW_Real_Array;

  namespace init_helpers {
    // This is a noop when no argument is given
    template <size_t i, typename Array>
    void ArrayDimension_adder(Array &A) {}

    // Fill the i-th value of the array recursively.
    template <size_t i, typename Array, typename... Ntype>
    void ArrayDimension_adder(Array &A, size_t iN, Ntype... Ns) {
      A[i] = iN;
      ArrayDimension_adder<i + 1>(A, Ns...);
    }

  } // namespace init_helpers

  template <typename... Ntype>
  inline boost::array<size_t, sizeof...(Ntype)> ArrayDimension(Ntype... Ns) {
    boost::array<size_t, sizeof...(Ntype)> A;
    init_helpers::ArrayDimension_adder<0>(A, Ns...);
    return A;
  }

} // namespace LibLSS

#endif
