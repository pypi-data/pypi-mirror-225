Text catalog format
===================

It is determined by the function ``loadGalaxySurveyFromText`` in
``libLSS/data/survey_load_txt.hpp`` (ARES git tree)

**[Galaxy Survey]**

For galaxy survey, the standard catalog format includes 7-8 columns. The meaning of each column, from left to right, is listed below.

-  galaxy id
-  phi: longitude, :math:`2\pi >= \phi >= 0` [rad].
-  theta: latitude, :math:`\pi/2 >= \theta >= -\pi/2` [rad].
-  zo: total observed redshift, to be used with photo-z.
-  m: apparent magnitude.
-  M_abs: absolute magnitude, not really used as it is derived from
   other quantities.
-  z: redshift, used to position the galaxies, cosmology is used to
   transform this to comoving distance at the moment.
-  w: weight, used as a multiplier when creating the grid of galaxy
   distribution.

**[Dark Matter Simulation]**

For Dark Matter simulation, the standard catalog format includes 10
columns. The meaning of each column, from left to right, is listed
below.

-  halo id
-  halo mass: given in unit of solar mass
-  halo radius
-  halo spin
-  x, y, z: comoving coordinates
-  vz, vy, vz: velocities
