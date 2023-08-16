HDF5 catalog format
===================

Passing in the :ref:`ini file<configuration_file>` the following
option in the catalog sections:

-  ``dataformat=HDF5``
-  ``datakey=KEY``

one can load from an HDF5 file the needed data for a catalog. The data
are taken from the entry "KEY" in the HDF5. This allows to store several
catalogs at the same time in the same file.

HDF5 catalog format
-------------------

The catalog must have the following columns:

-  id (``unsigned long int`` compatible)
-  phi (longitude in radians, ``double`` compatible)
-  theta (latitude in radians, ``double`` compatible)
-  zo (observed redshift, dimensionless, ``double`` compatible)
-  m (apparent magnitude, ``double`` compatible)
-  M_abs (absolute magnitude, optional, ``double`` compatible)
-  z (redshift, optional, ``double`` compatible)
-  w (weight, ``double`` compatible, should be 1)

HDF5 halo catalog format
------------------------

-  id (``unsigned long int`` compatible)
-  Mgal (mass, ``double`` compatible)
-  radius (``double`` compatible)
-  spin (``double`` compatible)
-  posx (x position Mpc, ``double`` compatible)
-  posy (y position Mpc, ``double`` compatible)
-  posz (z position Mpc, ``double`` compatible)
-  vx (velocity x, km/s, ``double`` compatible)
-  vy (velocity x, km/s, ``double`` compatible)
-  vz (velocity x, km/s, ``double`` compatible)
-  w (weight, ``double`` compatible, should be 1)

An example converter can be found hereafter:

.. code:: python

   import numpy as np
   import h5py as h5

   # Load text data file
   data0 = np.loadtxt("./halo.txt", dtype=[("id",int),("Mgal", float),("radius",float),("spin",float),("posx",float),("posy",float),("posz",float),("vx",float),("vy",float),("vz",float)])
   # Build a new one with a weight column
   data = np.empty(data0.size, dtype=[("id",int),("Mgal", float),("radius",float),("spin",float),("posx",float),("posy",float),("posz",float),("vx",float),("vy",float),("vz",float),("w",float)])

   for n in data0.dtype.names:
     data[n] = data0[n]

   # Set the weight to one
   data['w'] = 1

   # Write the hdf5
   print("Writing catalog")
   with h5.File("halo.h5", mode="w") as f:
     f['data'] = data
