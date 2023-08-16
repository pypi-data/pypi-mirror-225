.. _imperial_rcs:

Imperial RCS
============

This page contains notes on how to compile and run |a| (and extensions) on `Imperial Research Computing Services <https://www.imperial.ac.uk/admin-services/ict/self-service/research-support/rcs/>`_.

.. _gain_access_to_imperial_rcs:

Gain access to Imperial RCS
---------------------------

See `this page <https://www.imperial.ac.uk/admin-services/ict/self-service/research-support/rcs/support/getting-started/>`__.

.. _copy_configuration_files:

Copy configuration files
------------------------

Copy the pre-prepared configuration files in your home, by cloning :

.. code:: bash

   cd ~/
   git clone git@bitbucket.org:florent-leclercq/imperialrcs_config.git .bashrc_repo

and typing:

.. code:: bash

   cd .bashrc_repo/
   bash create_symlinks.bash
   source ~/.bashrc

Load compiler and dependencies
------------------------------

Load the following modules (in this order, and **only these** to avoid
conflicts):

.. code:: bash

   module purge
   module load gcc/8.2.0 git/2.14.3 cmake/3.14.0 intel-suite/2019.4 mpi anaconda3/personal

You can check that no other module is loaded using:

.. code:: bash

   module list

.. _prepare_conda_environment:

Prepare conda environment
-------------------------

If it's your first time loading anaconda you will need to run (see `this page <https://www.imperial.ac.uk/admin-services/ict/self-service/research-support/rcs/support/applications/conda/>`__):

.. code:: bash

   anaconda-setup

In any case, start from a clean conda environment (with only numpy) to
avoid conflicts between compilers. To do so:

.. code:: bash

   conda create -n pyborg numpy
   conda activate pyborg

.. _clone_ares_and_additional_packages:

Clone ARES and additional packages
----------------------------------

Clone the repository and additional packages using as usual (see :ref:`ARES Building <Building>`):

.. code:: bash

   mkdir ~/codes
   cd ~/codes
   git clone --recursive git@bitbucket.org:bayesian_lss_team/ares.git
   cd ares
   bash get-aquila-modules.sh --clone

If a particular release or development branch is desired, these
additional lines (for example) must be run:

.. code:: bash

   git checkout develop/2.1
   bash get-aquila-modules.sh --branch-set develop/2.1

Note that 'git branch' should not be used. Once this is done, one should
check to see whether the repository has been properly cloned, and the
submodules are all in the correct branch (and fine). To do so, one
should run:

.. code:: bash

   bash get-aquila-modules.sh --status

The output will describe whether the cloned modules are able to link to
the original repository.

If the root is not all well (for example, the error could be in
cosmotool), try:

.. code:: bash

   git submodule update

and check the modules status again

.. _compile_ares:

Compile ARES
------------

Run the ARES build script using:

.. code:: bash

   bash build.sh --with-mpi --c-compiler icc --cxx-compiler icpc --python

(for other possible flags, such as the flag to compile BORG python, type
``bash build.sh -h``). Note: for releases <= 2.0, a fortran compiler was
necessary: add ``--f-compiler ifort`` to the line above. One may have to
predownload dependencies for ares: for this, add the

::

   --download-deps

flag on the first use of build.sh, and add

::

   --use-predownload

on the second (which will then build ares).

Then compile:

.. code:: bash

   cd build
   make

The 'make' command can be sped up by specifying the number of nodes, N,
used to perform this:

.. code:: bash

   cd build
   make -j N

.. _run_ares_example_with_batch_script:

Run ARES example with batch script
----------------------------------

The following batch script (``job_example.bash``) runs the example using
mixed MPI/OpenMP parallelization (2 nodes, 32 processes/node = 16 MPI
processes x 2 threads per core). Check `this
page <https://www.imperial.ac.uk/admin-services/ict/self-service/research-support/rcs/computing/job-sizing-guidance/>`__
for job sizing on Imperial RCS.

.. code:: bash

   #!/bin/bash

   # request bash as shell for job
   #PBS -S /bin/bash

   # queue, parallel environment and number of processors
   #PBS -l select=2:ncpus=32:mem=64gb:mpiprocs=16:ompthreads=2
   #PBS -l walltime=24:00:00

   # joins error and standard outputs
   #PBS -j oe

   # keep error and standard outputs on the execution host
   #PBS -k oe

   # forward environment variables
   #PBS -V

   # define job name
   #PBS -N ARES_EXAMPLE

   # main commands here
   module load gcc/8.2.0 intel-suite/2019.4 mpi
   cd ~/codes/ares/examples/

   mpiexec ~/codes/ares/build/src/ares3 INIT 2mpp_ares.ini

   exit

As per `Imperial
guidance <https://www.imperial.ac.uk/admin-services/ict/self-service/research-support/rcs/computing/high-throughput-computing/configuring-mpi-jobs/>`__,
do not provide any arguments to ``mpiexec`` other than the name of the
program to run.

Submit the job via ``qsub job_example.bash``. The outputs will appear in
``~/codes/ares/examples``.

.. _select_resources_for_more_advanced_runs:

Select resources for more advanced runs
---------------------------------------

The key line in the submission script is

.. code:: bash

   #PBS -lselect=N:ncpus=Y:mem=Z:mpiprocs=P:ompthreads=W

to select N nodes of Y cores each (i.e. NxY cores will be allocated to
your job). On each node there will be P MPI ranks and each will be
configured to run W threads. You must have PxW<=Y (PxW=Y in all
practical situations). Using W=2 usually makes sense since most nodes
have hyperthreading (2 logical cores per physical core).
