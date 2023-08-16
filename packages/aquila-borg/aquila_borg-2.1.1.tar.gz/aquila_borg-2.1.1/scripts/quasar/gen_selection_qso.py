#+
#   ARES/HADES/BORG Package -- ./scripts/quasar/gen_selection_qso.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import cosmolopy as cpy
import numpy as np
import pyfits as pf

cosmo={'omega_M_0':0.30,'omega_lambda_0':0.70,'omega_k_0':0,'h':0.65,'sigma8':0.80}

f = pf.open("DR12Q.fits")
c = f[1].data

Z = c['Z_PIPE']

d = cpy.distance.comoving_distance(Z, **cosmo) * cosmo['h']

Dmax = 8000
Nb = 100
delta = 0.5*Dmax/Nb

d = d[d>100]

H,b = np.histogram(d, range=(0-delta,Dmax-delta),bins=Nb)

b0 = 0.5*(b[1:] + b[0:b.size-1])
H = H.astype(np.float64) / (b[1:]**3 - b[0:b.size-1]**3)

b0max = Dmax


H /= H.max()

with open("quasar_selection.txt", mode="wt") as f:

  f.write("%d %lg\n" % (H.size, b0max))
  for r in H:
    f.write("%lg\n" % r)

