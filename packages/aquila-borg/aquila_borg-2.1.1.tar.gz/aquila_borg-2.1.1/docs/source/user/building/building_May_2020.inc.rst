Installing BORG for the Aquila meeting (May 2020)
=================================================

This note provides a step by step instruction for downloading and
installing the BORG software package. This step-by-step instruction has
been done using a MacBook Air running OS X El Capitan. I encourage
readers to modify this description as may be required to install BORG on
a different OS. Please indicate all necessary modifications and which OS
was used.

Some prerequisites
------------------

The total installation will take approximately **7-8 GByte** of disk
space. Software prerequisites:

cmake≥ 3.10 automake libtool pkg-config gcc ≥ 7 , or intel compiler (≥
2018), or Clang (≥ 7) wget (to download dependencies; the flag
--use-predownload can be used to bypass this dependency if you already
have downloaded the required files in the ``downloads`` directory)

Clone the repository from BitBucket
-----------------------------------

To clone the ARES repository execute the following git command in a
console:
``{r, engine='bash', count_lines} git clone --recursive git@bitbucket.org:bayesian_lss_team/ares.git``

After the clone is successful, you shall change directory to ``ares``,
and execute:

.. code:: bash

    bash get-aquila-modules.sh --clone

Ensure that correct branches are setup for the submodules using:

.. code:: bash

    bash get-aquila-modules.sh --branch-set

If you want to check the status of the currently checked out ARES and
its modules, please run:

.. code:: bash

    bash get-aquila-modules.sh --status

You should see the following output:

.. code:: text

    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    This script can be run only by Aquila members.
    if your bitbucket login is not accredited the next operations will fail.
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    Checking GIT status...

    Root tree    (branch master) : good. All clear.
    Module ares_fg  (branch master) : good. All clear.
    Module borg (branch master) : good. All clear.
    Module dm_sheet (branch master) : good. All clear.
    Module hades    (branch master) : good. All clear.
    Module hmclet   (branch master) : good. All clear.
    Module python   (branch master) : good. All clear.

Building BORG
-------------

To save time and bandwidth it is advised to pre-download the
dependencies that will be used as part of the building procedure. You
can do that with

.. code:: bash

    bash build.sh --download-deps

That will download a number of tar.gz which are put in the
``downloads/`` folder.

Then you can configure the build itself:

.. code:: bash

    bash build.sh --cmake CMAKE_BINARY --c-compiler YOUR_PREFERRED_C_COMPILER --cxx-compiler YOUR_PREFERRED_CXX_COMPILER --use-predownload

Add ``--with-mpi`` to add MPI support. E.g. (This probably needs to be
adjusted for your computer.):

.. code:: bash

    bash build.sh --cmake /usr/local/Cellar/cmake/3.17.1/bin/cmake --c-compiler /usr/local/bin/gcc-10 --cxx-compiler /usr/local/bin/g++-10 --use-predownload

Once the configure is successful you should see a final output similar
to this:

.. code:: text

    ------------------------------------------------------------------

    Configuration done.
    Move to /Volumes/EXTERN/software/borg_fresh/ares/build and type 'make' now.
    Please check the configuration of your MPI C compiler. You may need
    to set an environment variable to use the proper compiler.

    Some example (for SH/BASH shells):
    - OpenMPI:
        OMPI_CC=/usr/local/bin/gcc-9
        OMPI_CXX=/usr/local/bin/g++-9
        export OMPI_CC OMPI_CXX

    ------------------------------------------------------------------

It tells you to move to the default build directory using ``cd build``,
after what you can type ``make``. To speed up the compilation you can
use more computing power by adding a ``-j`` option. For example

.. code:: bash

    make -j4

will start 4 compilations at once (thus keep 4 cores busy all the time
typically). Note, that the compilation can take some time.

Running a test example
----------------------

The ARES repository comes with some standard examples for LSS analysis.
Here we will use a simple standard unit example for BORG. From your ARES
base directory change to the examples folder:

.. code:: bash

    cd examples

We will copy a few files to a temporary directory for executing the run. We
will assume here that ``$SOME_DIRECTORY`` is a directory that you have created
for the purpose of this tutorial. Please replace any occurence of it by the
path of your choice in the scripts below. We will also assume that ``$ARES``
represents the source directory path of the ares tree.

.. code:: bash

   mkdir $SOME_DIRECTORY
   cp 2mpp-chain.ini $SOME_DIRECTORY
   cp completeness_12_5.fits.gz completeness_11_5.fits.gz 2MPP.txt $SOME_DIRECTORY
   cd $SOME_DIRECTORY

In the above, we have copied the ini file describing the run, then the data
file (survey mask) and 2M++ data file for BORG.  To start a BORG run just
execute the following code in the console:

.. code:: bash

    $ARES/build/src/hades3 INIT 2mpp-chain.ini.txt

BORG will now execute a simple MCMC. You can interupt calculation at any
time. To resume the run you can just type:

.. code:: bash

    $ARES/build/src/hades3 RESUME borg_unit_example.ini

You need at least on the order of 1000 samples to pass the initial
warm-up phase of the sampler. As the execution of the code will consume
about 2GB of your storage, we suggest to execute BORG in a directory
with sufficient free hard disk storage.

You can also follow the Aquila tutorial
---------------------------------------

You can find a tutorial on running and analysing a BORG run in the scripts
directory of the ARES base directory:
``$ARES/docs/users/building/Aquila_tutorial_0.ipynb``. It is a jupyter
notebook, so please have a `jupyter <https://jupyter.org>`_ running. We
provide access to the content of this notebook directly through this `link to the notebook <building/Aquila_tutorial_0.ipynb>`_.
It illustrates how to read and
plot some of the data produced by BORG.

Switching to another branch
---------------------------

Follow these steps to switch your ares clone to another branch (starting
from the ``ares/`` directory):

.. code:: bash

    git checkout user/fancy_branch
    git pull
    # (the above step should only be necessary if you are not on a fresh clone and have not pulled recently)
    bash get-aquila-modules.sh --branch-set
    bash get-aquila-modules.sh --status
    # ( verify that it responds with "all clear" on all repos)
    bash get-aquila-modules.sh --pull
    # ready to build: (make clean optional)
    cd build ; make clean ; make
