import matplotlib.pyplot as plt
import h5py as h5
import subprocess as sp


models={'lpt':'LPT','old_pm':'PMv1','pm':'PMv2','tcola':'tCOLA'}
#models={'lpt':'LPT','pm':'PMv2'}
output={}
output_v={}
Pref=None
km=None

for m,name in models.items():
  sp.run(f"./libLSS/tests/test_forward_{m}", check=True)
  with h5.File("dump.h5", mode="r") as ff:
      output[m] = ff['power'][:]
      output_v[m] = ff['power_v'][:]
      Pref = ff['scalars/powerspectrum'][:]
      km = ff['scalars/k_modes'][:]

#km = 0.5*(km[1:]+km[:-1])

fig2 = plt.figure(figsize=(5,5))
fig  = plt.figure(figsize=(5,6))
ax0 = plt.axes([0.1 ,0.2,0.9 ,0.7], rasterized=False)
ax1 = plt.axes([0.1 ,0.05,0.9 ,0.15], rasterized=False)
ax2_0 = fig2.add_subplot(111)
ax0.set_xlim(1e-3,2.2)
ax0.set_ylim(1e2,1e5)
ax1.set_xlim(1e-3,2.2)
ax0.set_xticks([])
ax1.set_xlabel('k ($h$ Mpc$^{-1}$)')
ax1.set_ylabel('$P(k) / P_{ref}(k)$')
ax0.set_ylabel('$P(k)$ ($h^{-3}$ Mpc$^{3}$)')
ax2_0.set_ylabel('$P(k)$ (km$^2$ s$^{-2}$ $h^{-3}$ Mpc$^{3}$)')
ax2_0.set_xlabel('k ($h$ Mpc$^{-1}$)')
ax2_0.set_ylim(1, 1e7)


for m,name in models.items():
  ax0.loglog(km,output[m],label=name)
  ax1.semilogx(km, output[m]/Pref,label=name)
  ax2_0.loglog(km, output_v[m], label=name)

ax0.loglog(km,Pref)
ax0.legend()
ax1.set_ylim(0.,1.5)
ax1.axhline(1.0,lw=1.0,color='k')
ax2_0.legend()
fig.savefig("models.pdf",bbox_inches='tight')
fig2.savefig("v_models.pdf",bbox_inches='tight')
