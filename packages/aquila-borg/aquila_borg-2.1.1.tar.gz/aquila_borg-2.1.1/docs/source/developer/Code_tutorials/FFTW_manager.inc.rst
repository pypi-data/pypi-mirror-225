.. _fftw_manager:

FFTW manager
============

Using FFTW, particularly with MPI, can be generally delicate and
requiring a lot of intermediate steps. A specific class was created to
handle a good fraction of this code pattern that are often used. The
class is named ``LibLSS::FFTW_Manager_3d`` and is defined in ``libLSS/tools/mpi_fftw_helper.hpp``. The class
is limited to the management of 3d transforms. A generalization for
:math:`N` dimensions is also available: ``LibLSS::FFTW_Manager<T,Nd>``.
We will only talk about that last generation here.

.. _initializing_the_manager:

Initializing the manager
------------------------

The constructor is fairly straightforward to use. The constructor has
:math:`N+1` parameters, the first :math:`N` parameters are for
specificying the grid dimensions and the last one the MPI communicator.

.. _allocating_arrays:

Allocating arrays
-----------------

The manager provides a very quick way to allocate arrays that are padded
correctly and incorporates the appropriate limits for MPI. The two
functions are ``allocate_array()`` and ``allocate_complex_array()``. The
first one allocates the array with the real representation and the
second with the complex representation. The returned value are of the
type ``UnitializedArray``. A type usage is the following:

.. code:: c++

   FFTW_Manager<double, 3> mgr(N0, N1, N2, comm);
   {
     auto array = mgr.allocate_array();
     auto& real_array = array.get_array();
     
     real_array[i][j][k] = something;
     // The array is totally destroyed when exiting here.
     // 
   }

The array allocated that way are designed to be temporary.
