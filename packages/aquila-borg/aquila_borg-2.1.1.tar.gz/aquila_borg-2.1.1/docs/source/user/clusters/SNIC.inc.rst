.. _snic:

SNIC
====

These instructions are for building on Tetralith - variations for other
systems may occur

Building at SNIC
----------------

Overview
~~~~~~~~

#. Ask for time
#. Load modules
#. Git clone the repo and get submodules
#. Use build.sh to build
#. Compile the code
#. Cancel remaining time

Detailed Instructions
~~~~~~~~~~~~~~~~~~~~~

1) ::

    interactive -N1 --exclusive -t 2:00:00

2) ::

    module load git
    module load buildenv-gcc/2018a-eb
    module load CMake/3.15.2

3) See instructions above

4) ::

    bash build.sh --with-mpi --cmake /software/sse/manual/CMake/3.15.2/bin/cmake --c-compiler /software/sse/manual/gcc/8.3.0/nsc1/bin/gcc --cxx-compiler /software/sse/manual/gcc/8.3.0/nsc1/bin/g++ --debug

Note that these links are NOT the ones from the buildenv (as loaded
before). These are "hidden" in the systems and not accessible from the
"module avail". If trying to compile with the buildenv versions the
compilation will fail (due to old versions of the compilers)

5) ::

    cd build
    make -j

6) Find the jobID: ``squeue -u YOUR_USERNAME``

Find the jobID from the response
::

    scancel JOBID

Running on Tetralith
--------------------

Use the following template:

.. code:: text

    #!/bin/bash
    ####################################
    #     ARIS slurm script template   #
    #                                  #
    # Submit script: sbatch filename   #
    #                                  #
    ####################################
    #SBATCH -J NAME_OF_JOB
    #SBATCH -t HH:MM:SS
    #SBATCH -n NUMBER_OF_NODES          
    #SBATCH -c NUMBER_OF_CORES PER NODE (Max is 32)  
    #SBATCH --output=log.%j.out # Stdout (%j expands to jobId) (KEEP AS IS)
    #SBATCH --error=error.%j.err # Stderr (%j expands to jobId) (KEEP AS IS)
    #SBATCH --account=PROJECT-ID
    export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK   ## you have to explicitly set this
    mpprun ./PATH/TO/HADES3 INIT_OR_RESUME /PATH/TO/CONFIG/FILE.INI\ 
