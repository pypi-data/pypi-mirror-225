#+
#   ARES/HADES/BORG Package -- ./scripts/test_analysis.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
from analysis.analysis import *
import pylab as plt
import numpy as np
import healpy as hp

#chain_path="/scratch/jasche/panphasia_run_pm/"
chain_path="/scratch/jasche/2mpp_highres_pm/"

ares=analysis(chain_path=chain_path,LSS_framework='BORG')


mu_i,var_i,mu_f,var_i=ares.mean_var_density(first_sample=299,last_sample=300,sample_steps=2)


plt.imshow(np.log(2+mu_f[:,:,64]))
plt.show()
'''
image=ares.get_spherical_slice(mu,nside=256,rslice=50)
hp.mollview(image)
plt.show()

'''

'''
k,mu,var=ares.mean_var_spec(first_sample=0,last_sample=100000,sample_steps=1)

#set loglog scale
plt.xscale('log')
plt.yscale('log')

plt.errorbar(k, mu, yerr=np.sqrt(var), fmt='-')
#plt.plot(k,mu,color='red')

plt.show()
'''
