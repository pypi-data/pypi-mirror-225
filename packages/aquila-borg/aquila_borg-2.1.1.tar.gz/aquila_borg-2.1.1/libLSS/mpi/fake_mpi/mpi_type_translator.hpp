/*+
    ARES/HADES/BORG Package -- ./libLSS/mpi/fake_mpi/mpi_type_translator.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

#ifndef FAKE_MPI_TYPE_TRANSLATOR_HPP_INCLUDED
#define FAKE_MPI_TYPE_TRANSLATOR_HPP_INCLUDED

#include <complex>

namespace LibLSS
{
  typedef int MPI_Datatype;
  static const int MPI_INT = 0;
  static const int MPI_LONG = 1;
  static const int MPI_DOUBLE = 2;
  static const int MPI_LONG_DOUBLE = 3;
  static const int MPI_INTEGER = 0;
  static const int MPI_UNSIGNED = 0;
  static const int MPI_UNSIGNED_LONG = 1;

  template<typename T>
  MPI_Datatype translateMPIType();

#define MPI_FORCE_TYPE(T) \
  template<> \
  inline MPI_Datatype translateMPIType<T>() \
  { \
    return sizeof(T); \
  }

#define MPI_FORCE_COMPOUND_TYPE(T) \
  template<> \
  inline MPI_Datatype translateMPIType<T>() \
  { \
    return sizeof(T); \
  }

  MPI_FORCE_TYPE(int);
  MPI_FORCE_TYPE(double);
  MPI_FORCE_TYPE(long double);
#ifdef __GNU__
  MPI_FORCE_TYPE(__float128);
#endif
  MPI_FORCE_TYPE(float);
  MPI_FORCE_TYPE(long);
  MPI_FORCE_TYPE(long long);
  MPI_FORCE_TYPE(unsigned long);
  MPI_FORCE_TYPE(unsigned long long);
  MPI_FORCE_TYPE(bool);
  MPI_FORCE_TYPE(std::complex<float>);
  MPI_FORCE_TYPE(std::complex<double>);


#undef MPI_FORCE_TYPE

  template<typename BaseType, size_t Dim>
  struct mpiVectorType {
    typedef mpiVectorType<BaseType, Dim> Self;

    inline MPI_Datatype type() const { return sizeof(BaseType)*Dim; }

    static Self& instance() {
      static Self variable;
      return variable;
    }
    mpiVectorType() {}
  };
};

#endif // MPI_TYPE_TRANSLATOR_HPP_INCLUDED
