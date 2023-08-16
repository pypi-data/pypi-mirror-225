#+
#   ARES/HADES/BORG Package -- ./scripts/misc/check_integrator.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import h5py as h5
import numpy as np
import pylab as plt


fig = plt.figure(1)

fig.clf()
ax = fig.add_subplot(111)

f = h5.File("symplectic.h5")
for k in f.keys():
  ax.semilogy(np.abs(f[k]['energy']), label=k)
f.close()

ax.legend()
fig.savefig("symplectic.png")
