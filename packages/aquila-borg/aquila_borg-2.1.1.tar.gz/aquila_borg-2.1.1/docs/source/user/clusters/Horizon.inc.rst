.. _horizon:

Horizon
=======

Compiling and using ARES/BORG on Horizon
----------------------------------------

Modules
~~~~~~~

.. code:: bash

   module purge
   module load gcc/7.4.0
   module load openmpi/3.0.3-ifort-18.0 
   module load fftw/3.3.8-gnu
   module load hdf5/1.10.5-gcc5
   module load cmake
   module load boost/1.68.0-gcc6
   module load gsl/2.5
   module load julia/1.1.0

Building
~~~~~~~~

.. code:: bash

   bash build.sh --use-predownload --use-system-hdf5 --use-system-gsl  --build-dir /data34/lavaux/BUILD_ARES --c-compiler gcc --cxx-compiler g++  

Running
~~~~~~~

Jupyter on Horizon
------------------

Jupyter is not yet installed by default on the horizon cluster. But it
offers a nice remote interface for people:

-  with slow and/or unreliable connections,
-  who wants to manage a notebook that can be annotated directly inline
   with Markdown, and then later converted to html or uploaded to the
   wiki with the figures included,
-  Use ipyparallel more efficiently

They are not for:

-  people who does not like notebooks for one reason or the other

Installation
~~~~~~~~~~~~

We use python 3.5, here. Load the following modules;

.. code:: bash

   module load intel/16.0-python-3.5.2 gcc/5.3.0

Then we are going to install jupyter locally:

.. code:: bash

   pip3.5 install --user jupyter-client==5.0.1 jupyter-contrib-core==0.3.1 jupyter-contrib-nbextensions==0.2.8 jupyter-core==4.3.0 jupyter-highlight-selected-word==0.0.11 jupyter-latex-envs==1.3.8.4 jupyter-nbextensions-configurator==0.2.5

At the moment (22 June 2017), I am using the above versions but later may well
work without problems.

Automatic port forwarding and launch of Jupyter instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Jupyter can be cumbersome to start reliably, automatically and in a
consistent fashion. Guilhem Lavaux has written two scripts (`here <https://www.aquila-consortium.org/wiki/index.php/File:Jupyter_horizon.zip>`__) that
can help in that regard. The first script (``jupyter.sh``) has to be
left in the home directory on Horizon, it helps at starting a new
jupyter job and reporting where it is located and how to contact it. The
two scripts are here: . The second script has to be kept on the local
station (i.e. the laptop of the user or its workstation). It triggers
the opening of ssh tunnels, start jobs and forward ports. The second
script (``.horizon-env.sh``) should be loaded from ``.bashrc`` with a
command like source ``${HOME}/.horizon-env.sh``. After such steps are
taken several things are possible. First to start a jupyter on horizon
you may run juphorizon. It will give the following output:

.. code:: text

   ~ $ juphoriz 
   Forwarding 10000 to b20:8888

Now you use your web-browser and connect to
`localhost:10000 <https://localhost:10000>`__. You also know that your jupyter is on
beyond20 (port 8888).

To stop the session do the following:

.. code:: text

   ~ $ stopjup 
   Do you confirm that you want to stop the session ? [y/N] 
   y
   Jupyter stopped

If you run it a second time you will get:

.. code:: text

   [guilhem@gondor] ~ $ stopjup 
   Do you confirm that you want to stop the session ? [y/N] 
   y
   No port forwarding indication. Must be down.

which means that the port forwarding information has been cleared out
and the script does not know exactly how to proceed. So it does nothing.
If you still have a job queued on the system it is your responsability
to close it off to avoid using an horizon node for nothing.

Two other commands are available:

-  ``shuthorizon``, it triggers the shutdown of the tunnel to horizon.
   Be careful as no checkings are done at the moment. So if you have
   port forwarding they will be cancelled and you will have to set them
   up manually again.
-  ``hssh``, this opens a new ssh multi-plex connection to horizon. It
   will not ask for your password as it uses the multiplexer available
   in ssh. Note that it is not possible to start an X11 forwarding using
   this.

IPyParallel
-----------

Now we need to install ipyparallel:

.. code:: bash

   pip3.5 install --user ipyparallel
   $HOME/.local/bin/ipcluster nbextension enable

Use `this pbs template <https://www.aquila-consortium.org/wiki/index.php/File:Pbs.engine.template.txt>`__.

You have to put several files in your $HOME/.ipython/profile_default:

-  `IPCluster configuration <https://www.aquila-consortium.org/wiki/index.php/File:IPython_ipcluster_config_py.txt>`__
   as *ipcluster_config.py*. This file indicates how to interact with
   the computer cluster administration. Notable it includes a link to
   aforementioned template for PBS. I have removed all the extra
   untouched configuration options. However in the original file
   installed by ipyparallel you will find all the other possible knobs.
-  `IPCluster
   configuration <https://www.aquila-consortium.org/wiki/index.php/File:IPython_ipcontroller_config_py.txt>`__ as
   *ipcontroller_config.py*. This file is used to start up the
   controller aspect which talks to all engines. It is fairly minor as I
   have kept the controller on the login node to talk to engines on
   compute nodes.
-  `IPCluster configuration <https://www.aquila-consortium.org/wiki/index.php/File:IPython_ipengine_config_py.txt>`__ as
   *ipengine_config.py*. This file is used to start up the engines on
   compute nodes. The notable option is to indicate to listen to any
   incoming traffic.

The documentation to ipyparallel is available from readthedocs
`here <http://ipyparallel.readthedocs.io/en/6.0.2/>`__.

Once you have put all the files in place you can start a new PBS-backed
kernel:

.. code:: text

   $ ipcluster start -n 16

With the above files, that will start one job of 16 cores. If you have
chosen 32, then it would have been 2 MPI-task of 16 cores each one, etc.

To start using with ipyparallel open a new python kernel (either from
ipython, or more conveniently from jupyter notebook):

.. code:: text

   import ipyparallel as ipp
   c = ipp.Client()

Doing this will connect your kernel with a running ipyparallel batch
instance. ``c`` will hold a dispatcher object from which you can
instruct engines what to do.

IPyParallel comes with magic commands for IPython
`3 <http://ipyparallel.readthedocs.io/en/6.0.2/magics.html>`__. They are
great to dispatch all your commands, however you must be aware that the
contexts is different from your main ipython kernel. Any objects has to
be first transmitted to the remote engine first. Check that page
carefully to learn how to do that.

MPIRUN allocation
-----------------

These are tips provided by Stephane Rouberol for specifying finely the
core/socket association of a given MPI/OpenMP computation.

.. code:: text

   # default is bind to *socket*
   mpirun -np 40 --report-bindings /bin/true  2>&1 | sed -e 's/.*rank \([[:digit:]]*\) /rank \1 /' -e 's/bound.*://' | sort -n -k2 | sed -e 's/ \([[:digit:]]\) /  \1 /'

   rank  0 [B/B/B/B/B/B/B/B/B/B][./././././././././.][./././././././././.][./././././././././.]
   rank  1 [./././././././././.][B/B/B/B/B/B/B/B/B/B][./././././././././.][./././././././././.]
   (...)

.. code:: text

   # we can bind to core
   mpirun -np 40 --bind-to core --report-bindings /bin/true 2>&1 | sed -e 's/.*rank \([[:digit:]]*\) /rank \1 /' -e 's/bound.*://' | sort -n -k2 | sed -e 's/ \([[:digit:]]\) /  \1

   rank  0 [B/././././././././.][./././././././././.][./././././././././.][./././././././././.]
   rank  1 [./././././././././.][B/././././././././.][./././././././././.][./././././././././.]
   (...)

.. code:: text

   # we can bind to core + add optimization for nearest-neighbour comms (put neighbouring ranks on the same socket)
   mpirun -np 40  --bind-to core -map-by slot:PE=1 --report-bindings /bin/true 2>&1 | sed -e 's/.*rank \([[:digit:]]*\) /rank \1 /' -e 's/bound.*://' | sort -n -k2 | sed -e 's/ \([[:digit:]]\) /  \1

   rank  0 [B/././././././././.][./././././././././.][./././././././././.][./././././././././.]
   rank  1 [./B/./././././././.][./././././././././.][./././././././././.][./././././././././.]

.. code:: text

   # -----------------------------------------------------------
   # case 2: 1 node, nb of ranks < number of cores (hybrid code)
   # -----------------------------------------------------------

   beyond08: ~ > mpirun -np 12 -map-by slot:PE=2   --report-bindings /bin/true  2>&1 | sort -n -k 4
   [beyond08.iap.fr:34077] MCW rank 0 bound to socket 0[core 0[hwt 0]], socket 0[core 1[hwt 0]]: [B/B/./././././././.][./././././././././.][./././././././././.][./././././././././.]
   [beyond08.iap.fr:34077] MCW rank 1 bound to socket 0[core 2[hwt 0]], socket 0[core 3[hwt 0]]: [././B/B/./././././.][./././././././././.][./././././././././.][./././././././././.]
   [beyond08.iap.fr:34077] MCW rank 2 bound to socket 0[core 4[hwt 0]], socket 0[core 5[hwt 0]]: [././././B/B/./././.][./././././././././.][./././././././././.][./././././././././.]

.. code:: text

   beyond08: ~ > mpirun -np 12 -map-by socket:PE=2   --report-bindings /bin/true  2>&1 | sort -n -k 4
   [beyond08.iap.fr:34093] MCW rank 0 bound to socket 0[core 0[hwt 0]], socket 0[core 1[hwt 0]]: [B/B/./././././././.][./././././././././.][./././././././././.][./././././././././.]
   [beyond08.iap.fr:34093] MCW rank 1 bound to socket 1[core 10[hwt 0]], socket 1[core 11[hwt 0]]: [./././././././././.][B/B/./././././././.][./././././././././.][./././././././././.]
   [beyond08.iap.fr:34093] MCW rank 2 bound to socket 2[core 20[hwt 0]], socket 2[core 21[hwt 0]]: [./././././././././.][./././././././././.][B/B/./././././././.][./././././././././.]

.. code:: text

   beyond08: ~ > mpirun -np 12 -map-by socket:PE=2 --rank-by core --report-bindings /bin/true  2>&1 | sort -n -k 4
   [beyond08.iap.fr:34108] MCW rank 0 bound to socket 0[core 0[hwt 0]], socket 0[core 1[hwt 0]]: [B/B/./././././././.][./././././././././.][./././././././././.][./././././././././.]
   [beyond08.iap.fr:34108] MCW rank 1 bound to socket 0[core 2[hwt 0]], socket 0[core 3[hwt 0]]: [././B/B/./././././.][./././././././././.][./././././././././.][./././././././././.]
   [beyond08.iap.fr:34108] MCW rank 2 bound to socket 0[core 4[hwt 0]], socket 0[core 5[hwt 0]]: [././././B/B/./././.][./././././././././.][./././././././././.][./././././././././.]
   [beyond08.iap.fr:34108] MCW rank 3 bound to socket 1[core 10[hwt 0]], socket 1[core 11[hwt 0]]: [./././././././././.][B/B/./././././././.][./././././././././.][./././././././././.]

Fighting the shared node curse
------------------------------

Horizon compute nodes are each made of a mother motherboard with 4 cpus
setup on it. The physical access to the resources is transparently
visible from any of the CPU. Unfortunately each memory bank is attached
physically to a preferred CPU. For a typical node with 512 GB of RAM,
each CPU gets 128 GB. If one of the CPU needs access to physical RAM
space hosted by another CPU, then the latency is significantly higher.
The Linux kernel wants to minimize this kind of problem so it will try
hard to relocated the processes so that memory access is not
delocalised, kicking out at the same time any computations already in
progress on that cpu. This results in computations residing on some CPU
to affect computations on another CPU.

The situation can be even worse if two computations are sharing the same
CPU (which holds each N cores, 8 < N < 14). In that case the
computations are fighting for CPU and memory resources. For pure
computation that is generally less of a problem, but this case is not so
frequent on computer designed to handle the analysis of large N-body
simulations.

To summarise, without checking and allocating that your computations are
sitting wholly on a CPU socket you may have catastrophic performance
degradation (I have experienced a few times at least a factor 10).

There are ways of avoiding this problem:

-  check the number of cores available on the compute nodes and try your
   best to allocate a single CPU socket. For example, beyond40cores
   queue is composed of nodes of 10 cores x 4 cpus. You should then ask
   to PBS "-l nodes=1:beyond40cores:ppn=10", which will give you 10
   cores, i.e. a whole CPU socket.
-  think that if you need 256 GB, then you should use the 2 cpu sockets
   in practice. So allocate 2 N cores (as in the previous cases, we
   would need 20 cores, even if in the end only one CPU is doing
   computation).
-  Use numactl to get informed and enforce the resources allocation. For
   example, typing "numactl -H" on beyond08 gives the following:

.. code:: text

   available: 4 nodes (0-3)
   node 0 cpus: 0 1 2 3 4 5 6 7 8 9
   node 0 size: 131039 MB
   node 0 free: 605 MB
   node 1 cpus: 10 11 12 13 14 15 16 17 18 19
   node 1 size: 131072 MB
   node 1 free: 99 MB
   node 2 cpus: 20 21 22 23 24 25 26 27 28 29
   node 2 size: 131072 MB
   node 2 free: 103 MB
   node 3 cpus: 30 31 32 33 34 35 36 37 38 39
   node 3 size: 131072 MB
   node 3 free: 108 MB
   node distances:
   node   0   1   2   3 
     0:  10  21  30  21 
     1:  21  10  21  30 
     2:  30  21  10  21 
     3:  21  30  21  10 

It states that the compute node is composed of 4 "nodes" (=CPU socket
here). The logical CPU affected to each physical CPU is given by "node X
cpus". The first line indicate that the Linux kernel logical cpu "0 1 2
... 9" are affected to the physical CPU 0. At the same time the node 0
has "node 0 size" RAM physically attached. The amount of free RAM on
this node is shown by "node 0 free". Finally there is a node distance
matrix. It tells the user how far are each node from each other in terms
of communication speed. It can be seen that there may be up to a factor
3 penalty for communication between node 0 and node 2.

Scratch space
-------------
