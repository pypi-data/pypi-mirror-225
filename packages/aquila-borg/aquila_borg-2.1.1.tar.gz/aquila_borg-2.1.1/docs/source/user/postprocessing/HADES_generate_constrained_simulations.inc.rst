Tutorial: generating constrained simulations from HADES
=======================================================

Get the source
--------------

First you have to clone the bitbucket repository

.. code:: text

   git@bitbucket.org:bayesian_lss_team/borg_constrained_sims.git

Ensure that you have the package H5PY and numexpr installed.

How to run
----------

If you run "python3 gen_ic.py -h" it will print the following help:

.. code:: text

   usage: gen_ic.py [-h] --music MUSIC [--simulator SIMULATOR] [--sample SAMPLE]
                    [--mcmc MCMC] [--output OUTPUT] [--augment AUGMENT]

   optional arguments:
     -h, --help            show this help message and exit
     --music MUSIC         Path to music executable
     --simulator SIMULATOR
                           Which simulator to target (Gadget,RAMSES,WHITE)
     --sample SAMPLE       Which sample to consider
     --mcmc MCMC           Path of the MCMC chain
     --output OUTPUT       Output directory
     --augment AUGMENT     Factor by which to augment small scales

All arguments are optional except "music" if it is not available in your
PATH.

The meaning of each argument is the following:

-  music: Full path to MUSIC executable
-  simulator: Type of simulator that you wish to use. It can either be

   -  WHITE, if you only want the 'white' noise (i.e. the Gaussian
      random number, with variance 1, which are used to generate ICs)
   -  Gadget, for a gadget simulation with initial conditions as Type 1
   -  RAMSES, for a ramses simulation (Grafic file format)

-  sample: Give the integer id of the sample in the MCMC to be used to
   generate ICs.
-  output: the output directory for the ICs
-  augment: whether to increase resolution by augmenting randomly the
   small scales (with unconstrained gaussian random numbers of variance
   1). This parameter must be understood as a power of two multiplier to
   the base resolution. For example, 'augment 2' on a run at 256 will
   yield a simulation at 512. 'augment 4' will yield a simulation at
   1024.

Generating initial conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*TO BE IMPROVED*

The main script can be found
`here <https://bitbucket.org/bayesian_lss_team/borg_constrained_sims/src/master/>`__,
which generates ICs for one or a small number of steps in the MCMC
chain. You will need all the restart_* files, along with the mcmc_*
files of the step you want to analyse. You also need the Music
executable. Using ``src.bcs``, the default is to generate ICs over the
entire simulation volume, with resolution increased by a factor of
``fac_res`` (i.e. white noise generated up to this scale). If you set
``select_inner_region=True`` then ICs are generated over only the
central half of the simulation volume, which effectively doubles your
resolution. An alternative is to use src.bcs_zoom, which instead zooms
in on the central sphere with radius and resolution as specified in that
script. In this case ``fac_res`` is irrelevant. Besides the properties
of the ellipse, the relevant parameter is the number in levelmax which
is the resolution with which you want to zoom in (e.g. if you start with
a :math:`256^3` grid ``[levelmin=8]``, specifying ``levelmax=11`` will
mean the zoom region starts at :math:`2048^3` resolution). For either
script you can choose to generate ICs for either the Ramses or Gadget
simulators.

Result
------

Gadget
~~~~~~

You will find a "gadget_param.txt" in the output directory and a file
called ic.gad in the subdirectory "ic". The log of the generation is in
"white_noise/"

Ramses
~~~~~~

Clumpfinding on the fly
^^^^^^^^^^^^^^^^^^^^^^^

There is a merger tree patch in Ramses which does halo-finding and
calculates merger trees as the simulation runs. The code is in
``patch/mergertree`` in the ramses folder where there is also some
documentation. The halos are calculated and linked at each of the
specified outputs of the simulation, so for the merger trees to be
reliable these outputs must be fairly frequent. The most conservative
choice is to have an output every coarse time step. The mergertree patch
is activated by specifying clumpfind=.true. in the run_params block, and
adding a clumpfind_params block to specify the parameters of the
clumpfinding. The extra files that this generates at each output are
halo_* (properties of the halos), clump_* (properties of the clumps,
essentially subhalos; this should include all the halos as well),
mergertree_* (information on the connected halos across the timesteps)
and progenitor_data_* (which links the halos from one step to the
next). If you wish to store the merger tree information more frequently
than the full particles (restart) information, you can hack the code in
``amr/output_amr`` to only output the ``part_*``, ``amr_*`` and
``grav_*`` files on some of the outputs (specified for example by the
scale factor ``aexp``). You can also hack the code in
``patch/mergertree/merger_tree.py`` to remove for example the
``clump_*`` files (if you only want to keep main halos), and/or remove
the ``progenitor_data_*`` files before the preceding snapshot when they
are no longer necessary. Finally, you may wish to concatenate the
remaining files (e.g. ``mergertree_*`` and ``halo_*``) over all the
processors.

Example namelist
^^^^^^^^^^^^^^^^^

.. code:: text

   &RUN_PARAMS
   cosmo=.true.
   pic=.true.
   poisson=.true.
   hydro=.false.
   nrestart=0
   nremap=20
   nsubcycle=1,1,1,1,20*2
   ncontrol=1
   clumpfind=.true.
   verbose=.false.
   debug=.false.
   /

   &INIT_PARAMS
   aexp_ini=0.0142857
   filetype='grafic'
   initfile(1)='/cosma7/data/dp016/dc-desm1/Ramses_8600/ic/ramses_ic/level_008'
   initfile(2)='/cosma7/data/dp016/dc-desm1/Ramses_8600/ic/ramses_ic/level_009'
   initfile(3)='/cosma7/data/dp016/dc-desm1/Ramses_8600/ic/ramses_ic/level_010'
   initfile(4)='/cosma7/data/dp016/dc-desm1/Ramses_8600/ic/ramses_ic/level_011'
   /

   &AMR_PARAMS
   ngridmax=3500000
   npartmax=8000000
   levelmin=8
   levelmax=19              
   nexpand=0,0,20*1         
   /

   &REFINE_PARAMS
   m_refine=30*8.            
   mass_cut_refine=2.32831e-10           
   ivar_refine=0  
   interpol_var=0
   interpol_type=2
   /

   &CLUMPFIND_PARAMS
   !max_past_snapshots=3
   relevance_threshold=3   ! define what is noise, what real clump
   density_threshold=80    ! rho_c: min density for cell to be in clump
   saddle_threshold=200    ! rho_c: max density to be distinct structure
   mass_threshold=100      ! keep only clumps with at least this many particles
   ivar_clump=0            ! find clumps of mass density
   clinfo=.true.           ! print more data
   unbind=.true.           ! do particle unbinding
   nmassbins=100           ! 100 mass bins for clump potentials
   logbins=.true.          ! use log bins to compute clump grav. potential
   saddle_pot=.true.       ! use strict unbinding definition
   iter_properties=.true.  ! iterate unbinding
   conv_limit=0.01         ! limit when iterated clump properties converge
   make_mergertree=.true.
   nmost_bound=200
   make_mock_galaxies=.false.
   /

   &OUTPUT_PARAMS
   aout=1.
   foutput=1
   /

White
~~~~~

This is a dummy output for which the output is only the whitened initial
conditions.
