/*+
    ARES/HADES/BORG Package -- ./libLSS/mpi/generic_mpi.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifdef ARES_MPI_FFTW 
#define OMPI_SKIP_MPICXX
#define _MPICC_H
#include <mpi.h>
#include "real_mpi/mpi_type_translator.hpp"
#include "real_mpi/mpi_communication.hpp"

#ifndef __LIBLSS_MPI_REAL_DEFINED
#define __LIBLSS_MPI_REAL_DEFINED
namespace LibLSS {
  static constexpr bool MPI_IS_REAL = true;
}
#endif

#else
#include "fake_mpi/mpi_type_translator.hpp"
#include "fake_mpi/mpi_communication.hpp"

#ifndef __LIBLSS_MPI_REAL_DEFINED
#define __LIBLSS_MPI_REAL_DEFINED
namespace LibLSS {
  static constexpr bool MPI_IS_REAL = false;
}
#endif
#endif

