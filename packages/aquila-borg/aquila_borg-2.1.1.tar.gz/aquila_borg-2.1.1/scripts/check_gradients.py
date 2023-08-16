#+
#   ARES/HADES/BORG Package -- ./scripts/check_gradients.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import matplotlib
matplotlib.use('Agg')
from ares_tools import read_all_h5
import pylab as plt
from sys import argv

file='dump.h5'

if (len(argv) > 1):
    file = argv[1]

print('Reading from %s.' % file)
g=read_all_h5(file)

#ss=16
#step=10

ss=4#8*8
step=5

prior = g.scalars.gradient_array_prior[::ss,:,:].flatten()
prior_ref = g.scalars.gradient_array_prior[::ss,:,:].flatten()

dpr_adj_re= prior.real
dpr_ref_re= prior_ref.real
dpr_adj_im= prior.imag
dpr_ref_im= prior_ref.imag

lh = g.scalars.gradient_array_lh[::ss,:,:].flatten()
lh_ref = g.scalars.gradient_array_lh_ref[::ss,:,:].flatten()

dlh_adj_re= lh.real
dlh_ref_re= 1*lh_ref.real
dlh_adj_im= lh.imag
dlh_ref_im= 1*lh_ref.imag

fig = plt.figure(figsize=(12, 6))
fig.subplots_adjust(left=0.08, right=0.98, bottom=0.1, top=0.95, wspace=0.25, hspace=0.16)

ax1=plt.subplot(2,2,1)             # left subplot in top row
plt.axhline(0.0, color='black', linestyle=':')
plt.plot(dpr_adj_re[::step],'ro',markersize=5.)
plt.plot(dpr_ref_re[::step],color='blue')
ax1.yaxis.get_major_formatter().set_powerlimits((-2, 2))
ax1.xaxis.set_ticklabels('')
plt.ylabel('dPSI_prior_real')

ax2=plt.subplot(2,2,2)             # right subplot in top row
plt.axhline(0.0, color='black', linestyle=':')
gg,=plt.plot(dpr_adj_im[::step],'ro',markersize=5.)
rr,=plt.plot(dpr_ref_im[::step],color='blue')
ax2.legend((gg,rr),('gradient','finite diff'))
ax2.yaxis.get_major_formatter().set_powerlimits((-2, 2))
ax2.xaxis.set_ticklabels('')
plt.ylabel('dPSI_prior_imag')

ax3=plt.subplot(2,2,3)             # left subplot in bottom row
plt.axhline(0.0, color='black', linestyle=':')
plt.plot(dlh_adj_re[::step],'ro',markersize=5.)
plt.plot(dlh_ref_re[::step],color='blue')
ax3.yaxis.get_major_formatter().set_powerlimits((-2, 2))
plt.xlabel('voxel ID')
plt.ylabel('dPSI_likelihood_real')

ax4=plt.subplot(2,2,4)             # right subplot in bottom row
plt.axhline(0.0, color='black', linestyle=':')
plt.plot(dlh_adj_im[::step],'ro',markersize=5.)
plt.plot(dlh_ref_im[::step],color='blue')
ax4.yaxis.get_major_formatter().set_powerlimits((-2, 2))
plt.xlabel('voxel ID')
plt.ylabel('dPSI_likelihood_imag')

plt.savefig('check_gradient.png')

#plt.scatter(dpr_adj_re,dpr_ref_re)
#plt.show()
