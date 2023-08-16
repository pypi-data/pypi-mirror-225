#+
#   ARES/HADES/BORG Package -- ./scripts/misc/plot_power.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import read_all_h5
from pylab import *

P=[]
n=[]
b=[]
n1=[]
b1=[]
i=0
while True:
  a = \
   read_all_h5.read_all_h5("mcmc_%d.h5" % i)
  try:
    P.append(a.scalars.powerspectrum)
    n.append(a.scalars.galaxy_nmean_0[0])
    b.append(a.scalars.galaxy_bias_0[0])
    n1.append(a.scalars.galaxy_nmean_1[0])
    b1.append(a.scalars.galaxy_bias_1[0])
  except AttributeError:
    break
  i += 1

k = read_all_h5.read_all_h5("info.h5").scalars.k_modes  
P = np.array(P)

f=figure(1)
clf()
loglog(k[:,None].repeat(P.shape[0],axis=1),P.transpose())

f=figure(2)
clf()
plot(n)

