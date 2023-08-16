/*+
    ARES/HADES/BORG Package -- ./libLSS/mpi/real_mpi/mpi_type_translator.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

#ifndef LIBLSS_MPI_TYPE_TRANSLATOR_HPP_INCLUDED
#define LIBLSS_MPI_TYPE_TRANSLATOR_HPP_INCLUDED

#include <complex>
#include <iostream>
#include <cstdlib>
#include <tuple>

namespace LibLSS
{
  template<typename T>
  MPI_Datatype translateMPIType();

#define MPI_FORCE_TYPE(T, val) \
  template<> \
  inline MPI_Datatype translateMPIType<T>() \
  { \
    return val; \
  }

#define MPI_FORCE_COMPOUND_TYPE(T) \
  template<> \
  inline MPI_Datatype translateMPIType<T>() \
  { \
     return MPI_CompoundType<T>::instance().datatype; \
  }

  MPI_FORCE_TYPE(int, MPI_INT);
  MPI_FORCE_TYPE(double, MPI_DOUBLE);
  MPI_FORCE_TYPE(float, MPI_FLOAT);
  MPI_FORCE_TYPE(long, MPI_LONG);
  MPI_FORCE_TYPE(bool, MPI_INT);
  MPI_FORCE_TYPE(unsigned long, MPI_UNSIGNED_LONG);
  MPI_FORCE_TYPE(unsigned long long, MPI_LONG_LONG_INT);
  MPI_FORCE_TYPE(unsigned int, MPI_UNSIGNED);

  struct MPI_GenericCompoundType {
    MPI_Datatype datatype;
    ~MPI_GenericCompoundType() {
  // FIXME: See how to properly free the type before MPI_Finalize
  //    MPI_Type_free(&datatype);
    }
  };

  template<typename T>
  struct MPI_CompoundType {};

  template<typename T> struct MPI_CompoundType<std::complex<T> >: MPI_GenericCompoundType {
      static MPI_CompoundType<std::complex<T> >& instance() {
          static MPI_CompoundType<std::complex<T> > variable;
          return variable;
      }

      MPI_CompoundType<std::complex<T> >() {
          (std::cerr << "Creating complex type " << std::endl).flush();
          int ret = MPI_Type_contiguous(2, translateMPIType<T>(), &datatype);

          if (ret != MPI_SUCCESS) {
            (std::cerr << "Error while creating types for complexes. Code was " << ret << std::endl).flush();
            ::abort();
          }
          MPI_Type_commit(&datatype);
      }
  };

  MPI_FORCE_COMPOUND_TYPE(std::complex<float>);
  MPI_FORCE_COMPOUND_TYPE(std::complex<double>);

  #undef MPI_FORCE_TYPE

  namespace internal_compound_helper {
    template <size_t Idx, typename Tuple>
    struct _offset_helper {
      static void fill_displacement(MPI_Aint *displ) {
        _offset_helper<Idx - 1, Tuple>::fill_displacement(displ);
        displ[Idx] = (ptrdiff_t)&std::get<Idx>(*(Tuple *)0);
      }
    };

    template <typename Tuple>
    struct _offset_helper<0, Tuple> {
      static void fill_displacement(MPI_Aint *displ) {
        displ[0] = (ptrdiff_t)&std::get<0>(*(Tuple *)0);
      }
    };
  } // namespace internal_compound_helper

  template <typename... Args>
  struct MPI_CompoundType<std::tuple<Args...>> : MPI_GenericCompoundType {

    typedef std::tuple<Args...> Tuple;

    static MPI_CompoundType<std::tuple<Args...>> &instance() {
      static MPI_CompoundType<std::tuple<Args...>> variable;
      return variable;
    }

    MPI_CompoundType<std::tuple<Args...>>() {
      using namespace internal_compound_helper;
      constexpr size_t N = sizeof...(Args);
      MPI_Datatype types[N] = {translateMPIType<Args>()...};
      int len[N];
      MPI_Aint displacement[N];

      std::fill(len, len + N, 1);
      _offset_helper<N - 1, Tuple>::fill_displacement(displacement);

#if !defined(MPI_VERSION) || (MPI_VERSION < 3)
      int ret = MPI_Type_struct(N, len, displacement, types, &datatype);
#else
      int ret = MPI_Type_create_struct(N, len, displacement, types, &datatype);
#endif

      if (ret != MPI_SUCCESS) {
        (std::cerr
         << "Error while creating types for tuple compound type. Code was "
         << ret << std::endl)
            .flush();
        ::abort();
      }
      MPI_Type_commit(&datatype);
    }
  };

   
  template<typename BaseType, size_t Dim>
  struct mpiVectorType {
    typedef mpiVectorType<BaseType, Dim> Self;
    MPI_Datatype datatype;

    inline MPI_Datatype type() const { return datatype; }

    static Self& instance() {
      static Self variable;
      return variable;
    }

    mpiVectorType() {
      int ret = MPI_Type_contiguous(Dim, translateMPIType<BaseType>(), &datatype);

      if (ret != MPI_SUCCESS) {
        ::abort();
      }
      MPI_Type_commit(&datatype);
    }
  };

};

#endif // MPI_TYPE_TRANSLATOR_HPP_INCLUDED
