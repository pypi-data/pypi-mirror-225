/*+
    ARES/HADES/BORG Package -- ./libLSS/mpi/real_mpi/mpi_communication.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#define OMPI_SKIP_MPICXX
#define _MPICC_H
#include <mpi.h>
#include "mpi_type_translator.hpp"
#include "mpi_communication.hpp"

LibLSS::MPI_Communication *LibLSS::MPI_Communication::singleton = 0;
