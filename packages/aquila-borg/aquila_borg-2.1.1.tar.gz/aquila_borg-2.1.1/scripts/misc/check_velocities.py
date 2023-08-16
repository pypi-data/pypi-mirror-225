#+
#   ARES/HADES/BORG Package -- ./scripts/misc/check_velocities.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
from read_all_h5 import *
import pylab as plt

g=read_all_h5('dump_velocities.h5')


V = g.scalars.L0[0]*g.scalars.L1[0]*g.scalars.L2[0]

q = g.scalars.k_pos_test
H=100.
D=1.
a=1.
f=g.scalars.cosmology['omega_m']**(5./9)
vref = 2* q/((q**2).sum()) / V * g.scalars.A_k_test * f * H * a**2 * D
vborg = g.scalars.lpt_vel[:,::].max(axis=0)

print "vref = %r" % vref
print "vborg = %r" % vborg

print "ratio = %r" % (vborg/vref)
