/*+
    ARES/HADES/BORG Package -- ./libLSS/mpi/real_mpi/mpi_mutex.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include <mpi.h>
#include "mpi_type_translator.hpp"
#include "mpi_communication.hpp"

using namespace CMB;
using namespace std;

MPICC_Mutex::MPICC_Mutex(MPI_Comm c, int mutex_tag)
{
  int err;
  int size, rank;
  int lockSize;
  host_rank = 0;
  this->mutex_tag = mutex_tag;

  this->comm = c;

  MPI_Comm_size(c, &size);
  MPI_Comm_rank(c, &rank);  

  if (rank == host_rank)
    {
      lockSize = size * sizeof(int);      
      if ((err = MPI_Alloc_mem(lockSize, MPI_INFO_NULL, &lockArray)) != MPI_SUCCESS)
          throw MPI_Exception(err);

      for (int i = 0; i < size; i++)
        lockArray[i] = 0;
    }
  else
    {
      lockArray = 0;
      lockSize = 0;
    }

  if ((err = MPI_Win_create(lockArray, lockSize, sizeof(int), MPI_INFO_NULL, comm, &win)) != MPI_SUCCESS)
    {
      if (lockArray != 0)
        MPI_Free_mem(lockArray);
      throw MPI_Exception(err);
    }
}

MPICC_Mutex::~MPICC_Mutex()
{
  MPI_Win_free(&win);

  if (lockArray != 0)
    MPI_Free_mem(lockArray);
}

void MPICC_Mutex::acquire()
{
  int err;
  int size, rank;
  int *all_locks;

  MPI_Comm_size(comm, &size);
  MPI_Comm_rank(comm, &rank);  

  all_locks = new int[size];

  try
    {
      bool already_locked = false;
      (std::cout << "[" << rank << "] Try to obtain lock" << std::endl).flush();
      do {
        all_locks[rank] = 1;
        err = MPI_Win_lock(MPI_LOCK_EXCLUSIVE, host_rank, 0, win);
        assert(err==MPI_SUCCESS);

        err = MPI_Put(all_locks+rank, 1, MPI_INT,
                      host_rank,
                      rank, 1, MPI_INT, win);
        assert(err == MPI_SUCCESS);
        if (rank > 0)
          {
            err = MPI_Get(all_locks, rank, MPI_INT,
                        host_rank,
                        0, rank, MPI_INT, win);
            assert(err == MPI_SUCCESS);
          }

        if (rank < size-1)
          {
            err = MPI_Get(all_locks+rank+1, size-rank-1, MPI_INT,
                          host_rank,
                          rank+1, size-rank-1, MPI_INT, win);
            assert(err == MPI_SUCCESS);
          }

      if ((err = MPI_Win_unlock(host_rank, win)) != MPI_SUCCESS)
        throw MPI_Exception(err);
  
      assert(all_locks[rank] == 1);

      already_locked = false;
      int whose_lock = -1;
      for (int i = 0; i < size; i++)
        if (i != rank && all_locks[i] != 0)
          {
            already_locked = true;
            whose_lock = i;
            break;
          }

      if (false&&already_locked) {
        // Failure release it.
        err = MPI_Win_lock(MPI_LOCK_EXCLUSIVE, host_rank, 0, win);
        all_locks[rank] = 0;
        err = MPI_Put(all_locks+rank, 1, MPI_INT,
                      host_rank,
                      rank, 1, MPI_INT, win);
        assert(err == MPI_SUCCESS);
        err = MPI_Win_unlock(host_rank, win);
      }

      if (already_locked)
        {
          MPI_Status status;
          int v = 0;
          (std::cout << "[" << rank << "] Blocking" << std::endl).flush();
          MPI_Recv(&v, 1, MPI_BYTE, MPI_ANY_SOURCE, mutex_tag, comm, &status);
          already_locked = false;
        }
     } while (already_locked);
     (std::cout << "[" << rank << "] Obtained lock" << std::endl).flush();
    }
  catch (MPI_Exception& e)
    {
      delete[] all_locks;
      throw e;
    }

  delete[] all_locks;
}

void MPICC_Mutex::release()
{
  int err;
  int rank, size;
  int *all_locks;

  MPI_Comm_size(comm, &size);
  MPI_Comm_rank(comm, &rank);  

  all_locks = new int[size];
  all_locks[rank] = 0;

  if ((err = MPI_Win_lock(MPI_LOCK_EXCLUSIVE, host_rank, 0, win)) != MPI_SUCCESS)
    throw MPI_Exception(err);

  err = MPI_Put(all_locks+rank, 1, MPI_INT,
                host_rank,
                rank, 1, MPI_INT, win);
  assert(err == MPI_SUCCESS);
  if (rank > 0)
    {
      err = MPI_Get(all_locks, rank, MPI_INT,
                    host_rank,
                    0, rank, MPI_INT, win);
      assert(err == MPI_SUCCESS);
    }

  if (rank < size-1)
    {
      err = MPI_Get(all_locks+rank+1, size-rank-1, MPI_INT,
                    host_rank,
                    rank+1, size-rank-1, MPI_INT, win);
      assert(err == MPI_SUCCESS);
    }

  if ((err = MPI_Win_unlock(host_rank, win)) != MPI_SUCCESS)
    throw MPI_Exception(err);

  assert(all_locks[rank] == 0);

  for (int i = 0; i < size; i++)
    {
      int p = (rank+i) % size;
      if (p!= rank && all_locks[p] != 0)
      {
        MPI_Status status;
        int v = 0;
        (std::cout << "[" << rank << "] Releasing  " << p << std::endl).flush();
        MPI_Send(&v, 1, MPI_BYTE, p, mutex_tag, comm);
        break;
      }
    }
  delete[] all_locks;

}

