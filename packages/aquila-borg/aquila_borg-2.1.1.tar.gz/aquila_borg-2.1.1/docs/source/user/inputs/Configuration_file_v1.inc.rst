.. _configuration_file:

ARES_Configuration_file_v1
==========================

The configuration file for ARES uses the INI file syntax. It is
separated into sections among which three are main sections.

Main sections
-------------

Section [system]
~~~~~~~~~~~~~~~~

-  console_output: Holds the prefix filename for all log output files.
-  VERBOSE_LEVEL: Set the verbosity level for the console. Files get all
   outputs.
-  N0: Number of grid elements along the X axis.
-  N1: Same for Y axis.
-  N2: Same for Z axis.
-  L0: Comoving length of the X axis
-  L1: Same for Y axis
-  L2: Same for Z axis
-  corner0: Center of the voxel at the corner of the box in -X
   direction, this should be the smallest X value.
-  corner1: Same for Y
-  corner2: Same for Z
-  NUM_MODES: number of bins to represent the power spectrm
-  N_MC: Maximum number of markov chain samples to produce in a single
   run (**Note:** Used only for *v1*)
-  borg_supersampling: Supersampling level of the grid for intermediate
   calculations. The number of particles is
   N0*N1*N2*borg_supersampling**3
-  hades_likelihood: Likelihood to use in HADES run. Can be either one
   of those values:

   -  BORG_POISSON: Use poisson likelihood
   -  BORG_POISSON_POWER:
   -  BORG_VOODOO:
   -  BORG_VOODOO_MAGIC:
   -  BORG_LINEAR: ARES likelihood model. Noise is Gaussian with
      Variance equal to :math:`S \bar{N}`. Use power law bias.
   -  BORG_SH:
   -  BORG_NB: Negative binomial. Broken power law bias.
   -  Generic framework:

      -  GAUSSIAN_BROKEN_POWERLAW_BIAS
      -  GAUSSIAN_MO_WHITE_BIAS: Gaussian noise model, variance is
         fitted. Double power law bias
      -  GAUSSIAN_POWERLAW_BIAS
      -  GAUSSIAN_2ND_ORDER_BIAS
      -  GENERIC_POISSON_BROKEN_POWERLAW_BIAS
      -  GENERIC_GAUSSIAN_LINEAR_BIAS
      -  GENERIC_GAUSSIAN_MANY_POWER_1^1
      -  GENERIC_GAUSSIAN_MANY_POWER_1^2
      -  GENERIC_GAUSSIAN_MANY_POWER_1^4
      -  GENERIC_POISSON_MANY_POWER_1^1
      -  GENERIC_POISSON_MANY_POWER_1^2
      -  GENERIC_POISSON_MANY_POWER_1^4

-  hades_forward_model: Forward model to use

   -  LPT: Lagrangian perturbation theory, ModifiedNGP/Quad final
      projection
   -  2LPT: Second order Lagrangian perturbation theory,
      ModifiedNGP/Quad final projection
   -  PM: Particle mesh, ModifiedNGP/Quad final projection
   -  LPT_CIC: Same as LPT, but use CIC for final projection
   -  2LPT_CIC: Same as LPT, but use CIC for final projection
   -  PM_CIC: Same as LPT, but use CIC for final projection
   -  HADES_LOG: Use Exponential transform (HADES model) for the forward
      model. Preserved mean density is enforced.

-  borg_do_rsd: Do redshift space distortion if set to "true".

-  projection_model: Specifies which projection to use for data. No
   constraints are enforced on the likelihood, but of course they should be matched 
   to the value adopted here. The value is inspected in ``src/common/projection.hpp``. 
   There are two available at the moment: ``number_ngp`` and ``luminosity_cic``. 
   The ``number_ngp`` is just Nearest-Grid-Point number counting. 
   The ``luminosity_cic`` uses the value in ``Mgal`` to weight the object 
   before doing CIC projection.

    -  number_ngp: it just counts the number of galaxies/objects within a voxel

    -  luminosity_cic: it weights galaxies by their luminosity and do a CIC projection.

-  test_mode: Runs ARES/BORG/HADES in test mode. Data is not used, mock
   data is generated on the fly.
-  seed_cpower: Set to true to seed the power spectrum with the correct
   one according to the cosmology section. Otherwise it is set to a
   small fraction of it.
-  hades_max_epsilon: Stepsize for the HMC. It is unitless. Good
   starting point is around 0.01.
-  hades_max_timesteps: Maximum number of timesteps for a single HMC
   sample.
-  hades_mixing: Number of samples to compute before writing to disk.
-  savePeriodicity: This reduces the number of times the restart files
   are dumped to the hard drives. This is useful for reducing I/Os, as
   restart files are heavy. You can set this to a number that is a
   multiple of the number of mcmc steps. For example, 20 tells ares to
   dump restart files every 20 mcmc steps.
-  mask_precision: Precision to which you want to compute the mask. By
   default it is "0.01", which is not related to the actual precision
   (unfortunately not yet). It allows scaling the internal number of
   evaluation of the selection function. So 0.001 will call it 100 times
   more. The advice is not to decrease below 0.01.
-  furious_seeding: if set to true the core sampler will reseed itself
   from a system entropy source at each step of the MCMC. That means the
   MCMC becomes unpredictable and the seed number is discarded.
-  simulation: if set to true switches to N-body simulation analysis.
   Additional cuts are possible depending on masses, spins, etc, of
   halos.

Likelihoods that use the generic bias framework (currently
GAUSSIAN_MO_WHITE_BIAS) supports also the following tags:

-  bias_XX_sampler_generic_blocked: if sets to true, it will not
   sampling the XX parameter of the bias. XX varies depending on the
   likelihood.
-  block_sigma8_sampler: true by default, to sample sigma8 in the
   initial conditions, sets this to false

Section [run]
~~~~~~~~~~~~~

-  NCAT: Number of catalogs. This affects the number of "catalog"
   sections.

-  SIMULATION: Specify if the input is from simulation. Default is
   false.

Section [cosmology]
~~~~~~~~~~~~~~~~~~~

-  omega_r: Radiation density
-  omega_k: Curvature
-  omega_m: Total matter density
-  omega_b: Baryonic matter density
-  omega_q: Quintescence density
-  w: Quintescence equation of state
-  wprime: Derivative of the equation of state
-  n_s: Slope of the power spectrum of scalar fluctuations
-  sigma8: Normalisation of powerspectrum at 8 Mpc/h
-  h100: Hubble constant in unit of 100 km/s/Mpc

Section [julia]
~~~~~~~~~~~~~~~

-  likelihood_path: Path to the julia file describing the likelihood
   (i.e. the main entry point for BORG in the likelihood)
-  likelihood_module: Name of the julia module holding the likelihood
-  bias_sampler_type: slice or hmclet, which sampling strategy to use to
   sample the "bias" parameters
-  ic_in_julia: true or false, whether the initial condition of the
   Markov Chain is set in julia
-  hmclet_diagonalMass: whether to use a diagonal or a dense mass matrix
   estimed on the fly
-  hmclet_burnin: number of steps allowed in "BURN IN" mode. This
   depends on the complexity of the likelihood. A few hundred seems
   reasonable.
-  hmclet_burnin_memory: size of the memory in "BURN IN" mode. Something
   like 50 is advocated to be sure it is fairly local but not too noisy.
-  hmclet_maxEpsilon: maximum epsilon for the HMC integrator (take order
   0.01)
-  hmclet_maxNtime: maximum number of timesteps for the HMC integrator
   (take a few decade like 20-50)

Catalog sections
----------------

Basic fields
~~~~~~~~~~~~

-  datafile: Text filename holding the data
-  maskdata: Healpix FITS file with the mask
-  radial_selection: Type of selection function, can be either
   "schechter", "file" or "piecewise".
-  refbias: true if this catalog is a reference for bias. Bias will not
   be sampled for it
-  bias: Default bias value, also used for mock generation
-  nmean: Initial mean galaxy density value, also used for mock
   generation

Halo selection
~~~~~~~~~~~~~~

-  halo_selection: Specifying how to select the halos from the halo catalog. Can be ``mass, radius, spin or mixed``. The ``mixed`` represents the combined cuts and can be applied by specifying, eg "halo_selection = mass radius"  
-  halo_low_mass_cut: this is log10 of mass in the same unit as the
   masses of the input text file
-  halo_high_mass_cut: same as for halo_low_mass_cut, this is log10 of
   mass
-  halo_small_radius_cut
-  halo_large_radius_cut
-  halo_small_spin_cut
-  halo_high_spin_cut

Schechter selection function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  schechter_mstar: Mstar for Schechter function
-  schechter_alpha: Power law slope of Schechter function
-  schechter_sampling_rate: How many distance points to precompute from
   Schechter (i.e. 1000)
-  schechter_dmax: Maximum distance to precompute Schecter selection
   functino
-  galaxy_bright_apparent_magnitude_cut: Apparent magnitude where data
   and selection must be truncated, bright end.
-  galaxy_faint_apparent_magnitude_cut: Same for faint end.
-  galaxy_bright_absolute_magnitude_cut: Absolute magnitude cut in data
   and selection function, bright end, useful to select different galaxy
   populations
-  galaxy_faint_absolute_magnitude_cut: Similar but faint end
-  zmin: Minimum redshift for galaxy sample, galaxies will be truncated
-  zmax: Maximum redshift for galaxy sample, galaxies will be truncated

'File' selection function
~~~~~~~~~~~~~~~~~~~~~~~~~

-  radial_file: Text file to load the selection from

The file has the following format. Each line starting with a '#' is a
comment line, and discarded. The first line is a set of three numbers:
'rmin dr N'. Each line that follows must be a number between 0 and 1
giving the selection function at a distance r = rmin + dr \* i, where
'i' is the line number (zero based). Finally 'N' is the number of points
in the text file.

Two possibilities are offered for adjusting the catalog and the
selection together:

-  either you chose not to do anything, and take the whole sample and
   provided selection. Then you need to specify:

   -  file_dmin: Minimal distance for selection function and data
   -  file_dmax: same but maximal distance
   -  no_cut_catalog: set to false, if you do not set this you will get
      an error message.

-  or you want ares to preprocess the catalog and then you need:

   -  zmin
   -  zmax
   -  galaxy_faint_apparent_magnitude_cut: Same for faint end.
   -  galaxy_bright_absolute_magnitude_cut: Absolute magnitude cut in
      data and selection function, bright end, useful to select
      different galaxy populations
   -  galaxy_faint_absolute_magnitude_cut: Similar but faint end
   -  no_cut_catalog: (not necessary, as it defaults to true)
