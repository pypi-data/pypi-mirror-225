#+
#   ARES/HADES/BORG Package -- ./libLSS/tests/plot_grav.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import h5py as h5
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

H100=100.e3
h=0.68
L=100.
N=128
G=6.67e-11
omega_m=0.30
Mpc_in_m=3.08567758e22
udistance=1.*Mpc_in_m

dmean = 1.0/(float(N)**3)

with h5.File("gravity.h5") as f:
  g = f['gravity'][...]
  p = f['position'][...]
  pot = f['potential'][...]
  ud = f['unit_density'][0] 
  up = f['unit_potential'][0]

ud *= Mpc_in_m**3

g = g[:(g.shape[0]/2),:]
p = p[:(p.shape[0]/2),:]
pot = pot[:(pot.shape[0]/2)]

ref = np.array([L/2,0,L/2])

plt.clf()
#plt.plot(-g[:,0])
plt.plot(p[:,1],-g[:,1])

yy = p[:,1]

aa = 6.67e-11 * ud * (L/N)**3 * yy/yy**3

plt.plot(yy, aa)

plt.gca().set_yscale('log')
plt.gca().set_xscale('log')

#plt.plot(g[:,2])

plt.gcf().savefig("grav.png")


xx=np.arange(N/2)*L/N 
mass = 3*(H100*h/Mpc_in_m)**2/(8*np.pi*G) * omega_m * (Mpc_in_m)**3

real_pot = 6.67e-11 * mass / (udistance*xx)

plt.clf()
plt.plot(xx,pot*up)
plt.plot(xx,real_pot)
plt.gca().set_yscale('log')
plt.gca().set_xscale('log')
plt.gcf().savefig("pot.png")
