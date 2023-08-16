#+
#   ARES/HADES/BORG Package -- ./scripts/dump_initial_field.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import pylab as plt
import h5py
import numpy as np
from read_all_h5 import explore_chain


chain_path="."

f = h5py.File('restart.h5_0', "r+")
print list(f['/scalars'])

xmin0 = f['/scalars/corner0'][:]
xmin1 = f['/scalars/corner1'][:]
xmin2 = f['/scalars/corner2'][:]

L0 = f['/scalars/L0'][:]
L1 = f['/scalars/L1'][:]
L2 = f['/scalars/L2'][:]

cosmology=f['/scalars/cosmology'][:]

xmin=np.array([xmin0,xmin1,xmin2])
L=np.array([L0,L1,L2])

outdir ='/scratch/jasche/'

for i,a in explore_chain(chain_path, 5000,8900, 10):
  d = a['s_field'][:]
  fname = outdir+'borg_ic_2m++_'+ str(i)
  print "Saving file : ", fname+'.npz'
  np.savez(fname, 
         ICfield = d, 
         BoxLength = L, 
         posmin = xmin, 
         omega_r = cosmology[0][0],
         omega_k = cosmology[0][1],
         omega_m = cosmology[0][2],
         omega_b = cosmology[0][3],
         omega_q = cosmology[0][4],
         w = cosmology[0][5],
         n_s = cosmology[0][6],
         wprime = cosmology[0][7],
         sigma8 = cosmology[0][8],
         h100 = cosmology[0][10],
         beta = cosmology[0][11])
   
data = np.load(fname+'.npz')

print data.keys()

plt.imshow(data['ICfield'][:,:,128])
plt.show()


