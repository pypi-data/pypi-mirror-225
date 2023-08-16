.. _outputs:

Outputs
#######

hmc_perfomance.txt
==================

This text file is appended with a new line every time the HMC is used.
Each column has the following meaning:

-  epsilon used in the integrator
-  number of timesteps
-  variation of energy between first and last step (:math:`\Delta H = H_{final} - H_{initial}`). Please note
   that you actually want this one to be negative or order 1 as the acceptance is determined by the probability
   :math:`exp(-\Delta H)`.
-  wall seconds taken to do the entire HMC run
-  scheme used to integrate
-  value of the final hamiltonian

.. _log_files:

log files
=========

The log files are formatted by libLSS/tools/console.hpp. If you have not
explicitly disabled the debug level, then all the messages emitted by
the code are saved in those files. Otherwise, it is limited to verbose
level. Each line starts with square brackets, with the level of the
message indicated "[LEVEL]". Each new indentation corresponds to a new
subcontext. If timing information were requested at compile time, each
termination of context gives also the time taken in the context itself,
including everything called inside this same context.

.. _restart_files:

restart files
=============

This file gives you access to the relevant infromation required to
restart an MCMC run, such as the initial configuration. The ares
framework creates one restart file per MPI task. Each file is suffixed
by "_X" where X is the MPI task id. Most of the variables are just the
same from one file to the other. The exception are the arrays explicitly
sliced by the MPI parallelization which are only present by slab.

The file contains the following groups:

-  galaxy_catalog_0
-  galaxy_kecorrection_0
-  random_generator
-  scalars

The python script "scripts/merge_mpi_restart.py" can merge all these
restart files into a single restart.h5 file. Be aware that it may
consume quite a lot of memory. However it is a required step to allow
the user to change the number of MPI task for an exisiting ARES run. The
MPI run may be resumed with the option "SPECIAL_RESUME" instead of
"RESUME" and it will read restart.h5 to recreate the set of
"restart.h5_XX" files with the new number of MPI tasks.

.. _mcmc_files:

MCMC files
==========

Depending on length of run, a series of mcmc files will be produced with
file names 'mcmc_chainNumber.h5'. All attributes of the file are
contained within the group 'scalars', for example the following for the
basic run in "examples":

-  catalog_foreground_coefficient_0
-  galaxy_bias_0
-  galaxy_nmean_0
-  powerspectrum
-  s_field
-  spectrum_c_eval_counter

For reference, these groups and attributes can be easily searched
through a few lines of python:

.. code:: python

   import h5py as h5

   # access mcmc file
   hf = h5.File("mcmc_0.h5")
   # list groups within file 
   list(hf.keys())
   # list attributes within 'scalars' group
   list(hf['scalars'].keys())

A tutorial to read and plot basic ARES outputs with python is available :ref:`here <tutorial_ares_basic_outputs>`.

If one wishes to access the MCMC files in C++, functions are available
in CosmoTool and LibLSS: see :ref:`this code tutorial <reading_in_meta_parameters_and_arrays>`.
