from tqdm import tqdm
import math
import os
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
mpl.use('Agg')
import ares_tools as at
import matplotlib.pyplot as plt
import h5py as h5
import numba as nb

startMC=0
suffix="ref"

ss = at.analysis(".")
opts=dict(Nbins=256,range=(0,ss.kmodes.max()))

names=[]
PP=[]
Fmax=0
while True:
    try:
      os.stat("mcmc_%d.h5" % Fmax)
    except:
      break
    names.append(Fmax)
    Fmax += 1
print(Fmax)

def handle_likelihood():

  def bias_func(rho, bias):
    a=ne.evaluate('exp(b0*log(rho) - b1*rho**(-b2))', dict(b0=bias[0],b1=bias[1],b2=bias[2],rho=rho))
    return a 
  
  
  @nb.jit(parallel=True,nopython=True)
  def compute_likelihood(S,nmean,bias,density,data):
    N0,N1,N2 = density.shape
    alpha,r0,eps = bias
    L = 0
    for p in nb.prange(N0*N1*N2):
          k = p % N2
          j = (p//N2) % N1
          i = (p//N2//N1)
          if S[i,j,k] <= 0:
            continue
  
          rho = 1+density[i,j,k]+1e-6
          x = r0*rho**(-eps)
          lrho = math.log(rho)
          rho_g = nmean * rho**alpha * math.exp(-x)
          log_rho_g = math.log(nmean) + lrho*alpha - x 
          lam = S[i,j,k] * rho_g
          log_lam = math.log(S[i,j,k]) + log_rho_g
          L += data[i,j,k]*log_lam - lam
  
    return L
  
  try:
    Likelihood = list(np.load("Like_%s.npy" % suffix))
    loc_names = names[len(Likelihood):]
  except:
    Likelihood = []
    loc_names = list(names)
  print(loc_names)
  if len(loc_names) == 0:
    return
  
  data = []
  selection = []
  for d_no in range(16):
    print("Load data %d" % (d_no,))
    data.append(ss.get_data(d_no))
    selection.append(ss.get_mask(d_no))
  
  for mc_id in tqdm(loc_names):
    with h5.File("mcmc_%d.h5" % mc_id, mode="r") as f:
      density = f['/scalars/BORG_final_density'][...]
      L=[]
      for i,(D,S) in enumerate(zip(data,selection)):
        nmean = f['/scalars/galaxy_nmean_%d' % i][0]
        bias = f['/scalars/galaxy_bias_%d' % i][...]
        L.append( compute_likelihood(S, nmean, bias, density, D) )
      Likelihood.append(L)
  
  np.save("Like.npy", Likelihood)


def handle_power():
  Pref = ss.rebin_power_spectrum(startMC, **opts)
  try:
    data = np.load("power_%s.npz" % suffix,allow_pickle=True)
    print("Found previous run")
    loc_names = names[len(data['P']):]
    print(loc_names)
    PP = list(data['P'])
  except Exception as exc:
    print(exc)
    print("no previous run")
    PP = []
    loc_names = list(names)
  print(loc_names)
  if len(loc_names) == 0:
    return
  
  for i in tqdm(loc_names):
    PP.append(ss.compute_power_shat_spectrum(i, **opts))
  
  bins = 0.5*(Pref[2][1:]+Pref[2][:-1])
  
  np.savez("power_%s.npz" % suffix, bins=bins, P=PP, startMC=startMC, Fmax=Fmax, Pref=Pref)
  

#handle_likelihood()
handle_power()
