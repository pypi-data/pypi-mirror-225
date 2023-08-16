Running ARES: basic run on 2M++
===============================

Introduction
------------

First of course please :ref:`build ARES<building>`. We will call $BUILD,
the directory where you built the entire code. By default it is located
in the source directory in the subdirectory build. But if you have
specified a different directory with the argument "--build-dir", then
$BUILD represent that last directory name. We will also call $SOURCE the
top source directory of ARES. In that case ``$SOURCE/README.rst`` would
point to the README file at the top source directory.

After a successful build you should find a binary program in
$BUILD/src/ares3. This is the main ARES3 program. If you type
``$BUILD/src/ares3``, then you should get the following output:

.. code:: text

   setupMPI with threads
   Initializing console.
   [0/1] [DEBUG  ] INIT: MPI/FFTW
   [STD    ]                                                
   [STD    ]        o                                       
   [STD    ]     ,-.|____________________                   
   [STD    ]  O==+-|(>-------- --  -     .>                 
   [STD    ]     `- |"""""""d88b"""""""""                   
   [STD    ]      | o     d8P 88b                           
   [STD    ]      |  \    98=, =88                          
   [STD    ]      |   \   8b _, 88b                         
   [STD    ]      `._ `.   8`..'888                         
   [STD    ]       |    \--'\   `-8___        __________________________________
   [STD    ]       \`-.              \                        ARES3             
   [STD    ]         `. \ -       - / <          (c) Jens Jasche 2012 - 2017    
   [STD    ]           \ `---   ___/|_-\             Guilhem Lavaux 2014 - 2017 
   [STD    ]            |._      _. |_-|      __________________________________
   [STD    ]            \  _     _  /.-\                    
   [STD    ]             | -! . !- ||   |                   
   [STD    ]             \ "| ^ |" /\   |                   
   [STD    ]             =oO)<>(Oo=  \  /                   
   [STD    ]              d8888888b   < \                   
   [STD    ]             d888888888b  \_/                   
   [STD    ]             d888888888b                        
   [STD    ] 
   [STD    ] Please acknowledge XXXX
   [0/1] [DEBUG  ] INIT: FFTW/WISDOM
   [0/1] [INFO   ] Starting ARES3. rank=0, size=1
   [0/1] [INFO   ] ARES3 base version c9e74ec93121f9d99a3b2fecb859206b4a8b74a3
   [0/1] [ERROR  ] ARES3 requires exactly two parameters: INIT or RESUME as first parameter and the configuration file as second parameter.

We will now go step by step for this output:

-  First we encounter ``setupMPI with threads``, it means the code asks
   for the MPI system to support multithreading for hybrid
   parallelization. The console is then initialized as it needs MPI to
   properly chose which file should receive the output.
-  After that the console logs get a prefix ``[R/N]``, with R and N
   integers. R is the MPI rank of the task emitting the information, and
   N is total number of MPI tasks. Then there is another ``[ XXXX ]``,
   where XXXX indicates the console log level. The amount of output you
   get is dependent on some flags in the configuration file. But by
   default you get everything, till the ini file is read. Note that
   "STD" level is only printed on the task of rank 0.
-  Then ``[0/1] [DEBUG ] INIT: MPI/FFTW`` indicates that the code asks
   for the MPI variant of FFTW to be initialized. It means the code is
   indeed compiled with FFTW with MPI support.
-  The ascii art logo is then shown.
-  ``[0/1] [DEBUG ] INIT: FFTW/WISDOM`` indicates the wisdom is
   attempted to be recovered for faster FFTW plan constructions.
-  ``[0/1] [INFO ] Starting ARES3. rank=0, size=1`` Reminds you that we
   are indeed starting an MPI run.
-  ``ARES3 base version XXXX`` gives the git version of the ARES base
   git repository used to construct the binary. In case of issue it is
   nice to report this number to check if any patch has been applied
   compared to other repository and make debugging life easier.
-  Finally you get an error::

    ARES3 requires exactly two parameters: INIT or RESUME as first parameter and the configuration file as second parameter,

   which tells you that you need to pass down two arguments: the first
   one is either "INIT" or "RESUME" (though more flags are available but
   they are documented later on) and the second is the parameter file.

First run
---------

Now we can proceed with setting up an actual run. You can use the files available in ``$SOURCE/examples/``. There are (as of 27.10.2020) 
ini files for running the executables on the given datasets (in this case the 2MPP dataset). Create a directory (e.g.
test_ares/, which we call $TEST_DIR) and now proceeds as follow:

.. code:: bash

    cd $TEST_DIR 
    $BUILD/src/ares3 INIT $SOURCE/examples/2mpp_ares3.ini

Note if you are using SLURM, you should execute with ``srun``. With the above options ares3 will start as a single MPI task, and allocate 
as many parallel threads as the computer can support. The top of the output is the following (after the splash and the other outputs
aforementioned):

.. code:: text

    [0/1] [DEBUG  ] Parsing ini file
    [0/1] [DEBUG  ] Retrieving system tree
    [0/1] [DEBUG  ] Retrieving run tree
    [0/1] [DEBUG  ] Creating array which is UNALIGNED
    [0/1] [DEBUG  ] Creating array which is UNALIGNED
    [INFO S ] Got base resolution at 64 x 64 x 64
    [INFO S ] Data and model will use the folllowing method: 'Nearest Grid point number count'
    [0/1] [INFO   ] Initializing 4 threaded random number generators
    [0/1] [INFO   ] Entering initForegrounds
    [0/1] [INFO   ] Done
    [INFO S ] Entering loadGalaxySurveyCatalog(0)
    [STD    ] | Reading galaxy survey file '2MPP.txt'
    [0/1] [WARNING] | I used a default weight of 1
    [0/1] [WARNING] | I used a default weight of 1
    [STD    ] | Receive 67224 galaxies in total
    [INFO S ] | Set the bias to [1]
    [INFO S ] | No initial mean density value set, use nmean=1
    [INFO S ] | Load sky completeness map 'completeness_11_5.fits.gz'

Again, we will explain some of these lines

-  ``Got base resolution at 64 x 64 x 64`` indicates ARES understands
   you want to use a base grid of 64x64x64. In the case of HADES however
   multiple of this grid may be used.
-  ``Data and model will use the folllowing method: 'Nearest Grid point number count'``
   indicates that galaxies are going to binned.
-  ``[0/1] [INFO ] Initializing 4 threaded random number generators``,
   we clearly see here that the code is setting up itself to use 4
   threads. In particular the random number generator is getting seeded
   appropriately to generate different sequences on each of the thread.
-  ``[STD ] | Reading galaxy survey file '2MPP.txt'`` indicates the data
   are being read from the indicated file.
-  ``[0/1] [WARNING] | I used a default weight of 1``, in the case of
   this file there is a missing last column which can indicate the
   weight. By default it gets set to one.

The code then continues proceeding. All the detailed outputs are sent to
logares.txt_rank_0 . The last digit indices the MPI rank task , as each
task will output in its own file to avoid synchronization problems. Also
it reduces the clutter in the final file.

Restarting
----------

If for some reason you have to interrupt the run, then it is not a
problem to resuming it at the same place. ARES by default saves a
restart file each time a MCMC file is emitted. This can be reduced by
changing the flag "savePeriodicity" to an integer number indicating the
periodicity (i.e. 5 to emit a restart file every 5 mcmc files).

Then you can resume the run using: ``$BUILD/src/ares3 RESUME 2mpp.ini``.
ARES will initialize itself, then reset its internal state using the
values contained in the restart file. Note that there is one restart
file per MPI task (thus the suffix ``_0`` if you are running with only
the multithreaded mode).

Checking the output
-------------------

After some (maybe very long) time, you can check the output files that
have been created by ARES. By default the ini file is set to run for
10,000 samples, so waiting for the end of the run will take possibly
several hours on a classic workstation. The end of the run will conclude
like:

.. code:: text

    [STD    ] Reached end of the loop. Writing restart file.
    [0/1] [INFO   ] Cleaning up parallel random number generators
    [0/1] [INFO   ] Cleaning up Messenger-Signal
    [0/1] [INFO   ] Cleaning up Powerspectrum sampler (b)
    [0/1] [INFO   ] Cleaning up Powerspectrum sampler (a)

Looking at the powerspectrum
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now we are going to set the ``PYTHONPATH`` to ``$SOURCE/scripts``. I.e.,
if you are using bash you can run the following piece:

.. code:: bash

    PYTHONPATH=$SOURCE/scripts:$PYTHONPATH
    export PYTHONPATH

Then we can start analyzing the powerspectrum of the elements of the
chain. You can copy paste the following code in a python file (let's
call it show_powerspectrum.py) and run it with your python3 interpreter
(depending on your installation it can be python3, python3.5, python3.6
or later):

.. code:: python

   import matplotlib
   matplotlib.use('Agg')
   import matplotlib.pyplot as plt
   import ares_tools as at

   chain = at.read_chain_h5(".", ['scalars.powerspectrum'])

   meta = at.read_all_h5("restart.h5_0", lazy=True)

   fig = plt.figure(1)
   ax = fig.add_subplot(111)
   ax.loglog(meta.scalars.k_modes, chain['scalars.powerspectrum'].transpose(),color='k',alpha=0.05)
   ax.set_xlim(1e-2,1)
   ax.set_ylim(1e2,1e6)
   ax.set_xlabel('$k$ ($h$ Mpc$^{-1}$)')
   ax.set_ylabel('$P(k)$ (($h^{-1}$ Mpc)$^3$)')

   fig.savefig("powerspectrum.png")

We will see what each of the most important lines are doing:

-  line 1-2: we import matplotlib and enforce that we only need the Agg
   backend (to avoid needing a real display connection).
-  line 4: we import the ares_tools analysis scripts
-  line 6: we ask to read the entire chain contained in the current path
   (``"."``). Also we request to obtain the field
   ``scalars.powerspectrum`` from each file. The result is stored in a
   named column array ``chain``. We could have asked to only partially
   read the chain using the keyword ``start``, ``end`` or ``step``. Some
   help is available using the command ``help(at.read_chain_h5)``.
-  line 8: we ask to read the entirety of ``restart.h5_0``, however it
   is done lazily (``lazy=True``), meaning the data is not read in
   central memory but only referenced to data in the file. The fields of
   the file are available as recursive objects in ``meta``. For example,
   ``scalars.k_modes`` here is available as the array stored as
   ``meta.scalars.k_modes``. While we are at looking this array, it
   corresponds to the left side of the bins of powerspectra contained in
   ``scalars.powerspectrum``.
-  line 12: we plot all the spectra using k_modes on the x-axis and the
   content of ``chain['scalars.powerspectrum']`` on the y-axis. The
   array is transposed so that we get bins in *k* on the first axis of
   the array, and each sample on the second one. This allows to use only
   one call to ``ax.loglog``.
-  line 18: we save the result in the given image file.

After this script is run, you will get a plot containing all the sampled
powerspectra in the chain. It is saved in *powerspectrum.png*

| Running this script will result typically in the following plot (here
  for 10,000 samples):

.. raw:: html

   <center>

.. figure:: /user/running/ARES_Tutorials_files/Powerspectrum_tutorial1_ares.png
   :alt: Powerspectrum_tutorial1_ares.png
   :width: 400px

   running/ARES_Tutorials_files/Powerspectrum_tutorial1_ares.png

.. raw:: html

   </center>

Looking at the density field
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now we can also compute the aposteriori mean and standard deviation per
voxel of the matter density field. The following script does exactly
this:

.. code:: python

   import matplotlib
   matplotlib.use('Agg')
   import matplotlib.pyplot as plt
   import numpy as np
   import ares_tools as at

   density = at.read_chain_avg_dev(".", ['scalars.s_field'], slicer=lambda x: x[32,:,:], do_dev=True, step=1)

   meta = at.read_all_h5("restart.h5_0", lazy=True)

   L = meta.scalars.L0[0]
   N = meta.scalars.N0[0]

   ix = np.arange(N)*L/(N-1) - 0.5*L

   fig = plt.figure(1, figsize=(16,5))
   ax = fig.add_subplot(121)
   im = ax.pcolormesh(ix[:,None].repeat(N,axis=1), ix[None,:].repeat(N,axis=0), density['scalars.s_field'][0],vmin=-1,vmax=2)
   ax.set_aspect('equal')
   ax.set_xlim(-L/2,L/2)
   ax.set_ylim(-L/2,L/2)
   ax.set_title('Mean density')
   ax.set_xlabel('$h^{-1}$ Mpc')
   ax.set_ylabel('$h^{-1}$ Mpc')
   fig.colorbar(im)

   ax = fig.add_subplot(122)
   im = ax.pcolormesh(ix[:,None].repeat(N,axis=1), ix[None,:].repeat(N,axis=0), density['scalars.s_field'][1],vmin=0,vmax=1.8)
   ax.set_aspect('equal')
   ax.set_xlim(-L/2,L/2)
   ax.set_ylim(-L/2,L/2)
   ax.set_xlabel('$h^{-1}$ Mpc')
   ax.set_ylabel('$h^{-1}$ Mpc')
   ax.set_title('Standard deviation')
   fig.colorbar(im)

   fig.savefig("density.png")

In this script we introduce ``read_chain_avg_dev`` (line 7) which allows
to compute mean and standard deviation without loading the chain in
memory. Additionally the *slicer* argument allows to only partially load
the field. The *step* argument allows for thinning the chain by the
indicator factor. In the above case we do not thin the chain. Also we
request the field *scalars.s_field* (which contains the density field)
and take only the plane *x=32*. The returned object is a named-columned
object. Also, *density['scalars.s_field']* is a [2,M0,...] array, with
M0,... being the dimensions returned by the slicer function. The first
slice is the mean field (as can be seen on line 18) and the second is
the standard deviation (line 28).

Once the script is run we get the following pictures:

.. raw:: html

   <center>
   
.. figure:: /user/running/ARES_Tutorials_files/Density_tutorial1_ares.png
   :alt: Density_tutorial1_ares.png
   
   Density_tutorial1_ares.png

.. raw:: html

   </center>

We can see that there are large scale features in the mean field (like
ringing here). Though even in perfect conditions this feature could
occur, this could also indicate a defect in the selection
characterization process.
