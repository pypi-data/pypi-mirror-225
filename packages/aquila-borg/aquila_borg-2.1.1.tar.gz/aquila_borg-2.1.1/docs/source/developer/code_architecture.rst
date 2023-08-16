Code architecture
=================

Slides of the tutorial
----------------------

See `this file <https://www.aquila-consortium.org/wiki/index.php/File:ARES_code.pdf>`__.
Some of these slides are starting to get outdated. Check the doc pages in case of doubt.


Overall presentation
--------------------

The ARES3 framework is divided into a main library (libLSS) and several
core program (ares3, hades3 at the moment).

A step-by-step tutorial on how to create a new core program is described
:ref:`here <new_core_program>`.

Code units
----------

The units of the code are whenever possible in "physical" units (i.e.
velocities often in km/s, density contrasts, ...). The rational being
that theory papers are often expressed, or easily expressable, in those
units while it kind be hard to follow all the required steps to make the
units work in the global numerical schemes of ARES. So the equations are
more easily readable and matchable to equations. As an example, the
Fourier transform of density contrast must have the unit of a volume.
The density fluctuation power spectrum is also a volume.

That can also however introduce some unexpected complexity.

ares3
~~~~~

All the code rely on the ARES3 code framework. At the basis it is a
library (libLSS) and a common code base for different sampling scheemes
(e.g. ARES, ARES-foreground, ATHENA, HADES, BORG). The sampling schemes
being quite sensitive to the implementation details they are not yet
fully parametrizable by the user and only a few degree of freedoms are
allowed through the configuration file. The configuration file comes as
a Windows INI file, though that may evolve later.

libLSS
~~~~~~

The libLSS library provides different elements to build a full sampling
scheme and the description of a posterior. The different components are
organized in a hierarchical tree. C++ templates are quite heavily used
though classical C++ virtual inheritancy is also present to make the
code more digestible without loss of performance. Some tests are present
in libLSS/tests. They are useful to both check that the library behaves
as it should and to serve as an entry point for newbies.

The LibLSS library is itself divided in several big branches:

-  data: holds the framework data model, it holds the description of
   galaxy surveys into its individual components
-  mcmc: Holds the abstract description of elements that can be
   serialized into a MCMC file or the restart file. There is no specific
   implementation here, only definition of what is an array, a random
   number generator, etc.
-  physics: it contains modules for handling more specific physics
   computations likes cosmology or dynamics.
-  samplers: generic branch that holds the different samplers of libLSS
-  tools: a mixed bag of tools that have different use in libLSS

data
^^^^

-  ``spectro_gals.hpp``: Abstract definition of a galaxy survey
   (spectroscopic, but also photo-z possible).
-  ``window3d.hpp``: Algorithm to compute the selection in 3d volume
   from 2d+1d information.
-  ``galaxies.hpp``: Define structure that describe a galaxy in a
   survey.
-  ``projection.hpp``: Nearest grid point projection of galaxies from a
   survey to a 3d grid.
-  ``linear_selection.hpp``: Implements a radial selection function
   defined piecewise, with linear interpolation
-  ``schechter_completeness.hpp``

tools
^^^^^

"tools" is a grab all bag of tools and core infrastructure that allows
writing the rest of the code. In particular it contains the definition
of the ``console`` object. Among the most useful tools
are the following:

-  the :ref:`FFTW manager <fftw_manager>` class, to help with management
   of parallelism, plan creation, etc with FFTW
-  the :ref:`FUSEd array subsystem <fuse_array_mechanism>`, which enables lazy
   evaluation of multi-dimensional arrays.

mpi
^^^

libLSS provides an MPI class interface with reduces to dummy function
calls when no MPI is present. This allows to write the code once for MPI
and avoid any ifdefs spoiling the source code.


"State" Dictionnary information
------------------------------~

libLSS/samplers/core/types_samplers.hpp gives all the default classes
specialization and types used in ARES/HADES/BORG.

-  (ArrayType) ``galaxy_data_%d``: store the binned observed galaxy
   density or luminosity density.
-  (SelArrayType) ``galaxy_sel_window_%d``: 3d selection window
-  (SelArrayType) ``galaxy_synthetic_sel_window_%d``: 3d selection
   window with foreground corrections applied (ARES)
-  (synchronized double) ``galaxy_nmean_%d``: normalization factor of
   the bias function (can be mean density, it can be ignored for some
   bias models like the ManyPower bias model in the generic framework)
-  (ArrayType1d) ``galaxy_bias_%d``: store the bias parameters
-  (ArrayType) ``s_field``: Store the real representation of the
   Gaussian random initial conditions, scaled at :math:`z=0`.
-  (CArrayType) ``s_hat_field``: Store the complex representation of
   ``s_field``
-  (ArrayType1d) ``powerspectrum``: Finite resolution power spectrum in
   physical unit (Mpc/h)^3
-  (ArrayType1d) ``k_modes``: :math:`k (h/\text{Mpc})` modes
   corresponding to the power spectrum stored in ``powerspectrum``. The
   exact meaning is sampler dependent.
-  (ArrayType) ``k_keys``: A 3d array indicating for each element of the
   Fourier representation of a field how it is related to the power
   spectrum. That allows for doing something like
   ``abs(s_field[i][j][k])^2/P[k_keys[i][j][k]]`` to get the prior value
   associated with the mode in ``i, j, k``.
-  (SLong) ``N0``,\ ``N1``,\ ``N2`` base size of the 3d grid, i.e.
   parameter space dimensions
-  (SDouble) ``L0``,\ ``L1``,\ ``L2`` physical size of the 3d grid,
   units of Mpc/h, comoving length.
-  (ObjectStateElement) ``cosmology``, holds a structure giving the
   currently assumed cosmology.
-  (ArrayType) ``foreground_3d_%d``, a 3d grid corresponding to the
   extruded foreground contamination in data. The '%d' runs across all
   possible foreground specified in the configuration file.
-  (SLong) ``MCMC_STEP``, the identifier of the current MCMC element.
-  (RandomStateElement) ``random_generator``, the common, multi-threaded
   and multi-tasked, random number generator.

**BORG specific**

-  (ArrayType) ``BORG_final_density``: Final result of the forward model
   before likelihood comparison to data
-  (ArrayType1d) ``BORG_vobs``: 3 component 1d array that contains the 3
   component of the additional velocity vector required to fit redshift
   density of galaxies.
-  (ObjectStateElement) ``BORG_model`` (
-  (double) ``hmc_Elh``, minus log-likelihood evaluated by HMC
-  (double) ``hmc_Eprior``, minus log-prior evaluated by HMC
-  (bool) ``hmc_force_save_final``, force the saving of the next final
   density
-  (int) ``hmc_bad_sample``, the number of bad HMC samples since last
   saved MCMC
-  (SLong) ``hades_attempt_count``, number of attempted HMC move since
   last saved MCMC
-  (SLong) ``hades_accept_count``, number of accepted HMC move since
   last saved MCMC
-  (ArrayType) ``hades_mass`` diagonal mass matrix for HMC

**ARES specific**

-  (ArrayType) ``messenger_field``: store the messenger field array
-  (SDouble) ``messenger_tau``: store the scalar value giving the
   covariance of the messenger field.
