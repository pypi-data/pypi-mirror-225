import h5py as h5
import cosmotool as ct
import numpy as np
import ares_tools as at


#result = at.read_chain_avg_dev(".",["final_density", "v_field"],step=20*4,prefix="output",do_dev=True,start=20000)
if False:
  mean_p,dev_p = at.read_chain_complex_avg_dev(".",lambda ff: (1+ff['final_density'][...])*ff['v_field'][...],step=10,prefix="output",do_dev=True,start=200, pattern="%s_%04d.h5")
  mean_d,dev_d= at.read_chain_complex_avg_dev(".",lambda ff: ff['final_density'][...],step=10,prefix="output",do_dev=True,start=200,pattern="%s_%04d.h5")
  np.savez("means.npz", mean_p=mean_p, dev_p=dev_p, mean_d=mean_d,dev_d=dev_d)
else:
  x=np.load("means.npz")
  mean_d = x['mean_d']
  mean_p = x['mean_p']

with h5.File("output_2200.h5", mode="r") as ff:
  one_d = ff['final_density'][...]
  one_p = ff['v_field'][...]#(ff['final_density'][...]+1)*ff['v_field'][...]

Nside=256
L=4000
N=256
Dmin=10
Dmax=128

#ix=np.arange(N)*L/N - 0.5*L
ix=np.arange(N)*L/N

# These are the box corners
corner_x=-2200
corner_y=-2000
corner_z=-300

shifter=-np.array([corner_x,corner_y,corner_z])*N/L - 0.5*N
shifter2=np.array([corner_x,corner_y,corner_z])
mm=ct.spherical_projection(Nside, mean_d, Dmin, Dmax,shifter=shifter,integrator_id=1,booster=100)
one_mm=ct.spherical_projection(Nside, one_d, Dmin, Dmax,shifter=shifter,integrator_id=1,booster=100)

x = ix[:,None,None].repeat(N,axis=1).repeat(N,axis=2) + shifter2[0]
y = ix[None,:,None].repeat(N,axis=0).repeat(N,axis=2) + shifter2[1]
z = ix[None,None,:].repeat(N,axis=0).repeat(N,axis=1) + shifter2[2]
r = np.sqrt(x**2+y**2+z**2)

cond = r>0
pr = np.where(cond, (mean_p[0,...] * x + mean_p[1,...] * y + mean_p[2,...]*z)/r,0)
one_pr = np.where(cond,(one_p[0,...] * x + one_p[1,...] * y + one_p[2,...]*z)/r,0)

one = np.ones(pr.shape)

mpr=ct.spherical_projection(Nside, pr, Dmin, Dmax,shifter=shifter,integrator_id=1,booster=100)
one_mpr=ct.spherical_projection(Nside, one_pr, Dmin, Dmax,shifter=shifter,integrator_id=1,booster=100)
mdist=ct.spherical_projection(Nside, one, Dmin, Dmax,shifter=shifter,integrator_id=1,booster=100)

np.savez("sky.npz", d=mm,pr=mpr,r=r,dist=mdist,one_d=one_mm,one_pr=one_mpr)


