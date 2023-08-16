.. _occigen:

Occigen
=======

Occigen is a CINES managed supercomputer in France. You need a time
allocation on this to use it. Check https://www.edari.fr

Module setup
------------

Compile with Intel
~~~~~~~~~~~~~~~~~~

.. code:: bash

   module purge
   module load gcc/8.3.0
   module load intel/19.4 
   # WARNING: openmpi 2.0.4 has a bug with Multithread, cause hangs
   module load openmpi-intel-mt/2.0.2 
   module load intelpython3/2019.3
   export OMPI_CC=$(which icc)
   export OMPI_CXX=$(which icpc)

Then run:

.. code:: bash

   bash build.sh --use-predownload --no-debug-log --perf --native  --c-compiler icc --cxx-compiler icpc --f-compiler ifort --with-mpi  --build-dir $SCRATCHDIR/ares-build-icc --cmake $HOME/.local/bin/cmake

Compile with gcc
~~~~~~~~~~~~~~~~

.. code:: bash

   module purge
   module load gcc/8.3.0
   # WARNING: openmpi 2.0.4 has a bug with Multithread, cause hangs
   module load openmpi/gnu-mt/2.0.2
   module load intelpython3/2019.3
   export OMPI_CC=$(which gcc)
   export OMPI_CXX=$(which g++)

Prerequisite
~~~~~~~~~~~~

Download cmake >= 3.10.

.. code:: bash

   wget https://github.com/Kitware/CMake/releases/download/v3.15.5/cmake-3.15.5.tar.gz

Be sure the above modules are loaded and then compile:

.. code:: bash

   cd cmake-3.15.5
   ./configure  --prefix=$HOME/.local
   nice make
   make install

On your laptop run:

.. code:: bash

   bash build.sh --download-deps
   scp -r downloads occigen:${ARES_ROOT_ON_OCCIGEN}

Build
-----

.. _with_intel:

With intel
~~~~~~~~~~

.. code:: bash

   bash build.sh --use-predownload --no-debug-log --perf --native  --c-compiler icc --cxx-compiler icpc --f-compiler ifort --with-mpi  --build-dir $SCRATCHDIR/ares-build-icc --cmake $HOME/.local/bin/cmake

.. _with_gcc:

With gcc
~~~~~~~~

.. code:: bash

   bash build.sh --use-predownload --no-debug-log --perf --native  --c-compiler gcc --cxx-compiler g++ --f-compiler gfortran --with-mpi  --build-dir $SCRATCHDIR/ares-build-gcc --cmake $HOME/.local/bin/cmake
