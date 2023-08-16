#+
#   ARES/HADES/BORG Package -- ./scripts/misc/plot_void.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
from pylab import *
from read_all_h5 import explore_chain

def box2sphere(x,y,z):
 #calculate radii
 r=np.sqrt(x**2+y**2+z**2)
 
 print np.shape(r),np.shape(x)
 
 dec=np.zeros(np.shape(r))
 '''
 foo= np.where(r>0)
 dec[foo]=np.arcsin(z[foo]/r[foo])
 '''
 ra=np.arctan2(y,x)
 
 print np.shape(r),np.shape(ra)
 
 return ra,dec,r


chain_path="."

N = 256 
L = 677.7
Nb = 128 
f = np.sqrt(3)*0.5

ix = np.arange(N)*L/N - 0.5*L

ra,dec,r=box2sphere(ix[:,None,None],ix[None,:,None],ix[None,None,:])

r = np.sqrt(ix[:,None,None]**2 + ix[None,:,None]**2 + ix[None,None,:]**2)

print np.shape(r)

H, b = np.histogram(r, range=(0,f*L), bins=Nb)

Hw_mean=np.zeros(np.shape(H))

cnt=0

mu  = np.zeros(np.shape(H))
var = np.zeros(np.shape(H))

nn=1
for i,a in explore_chain(chain_path, 400,4100, 10):
  d = a['BORG_final_density'][:]

  Hw, b = np.histogram(r, weights=d, range=(0,f*L), bins=Nb)
  Hw /= H
  
  mu    = (nn-1.)/float(nn)*mu +1./float(nn)*Hw
  if(nn>1): 
          aux = (mu-Hw)**2
          var = (nn-1.)/nn*var+1./(nn-1)*aux
  
  nn+=1
  
plot(b[1:], mu, label='average', color='red')

fill_between(b[1:], mu, mu+np.sqrt(var), interpolate=True, color='gray', alpha='0.5')
fill_between(b[1:], mu-np.sqrt(var), mu, interpolate=True, color='gray', alpha='0.5')
fill_between(b[1:], mu, mu+2*np.sqrt(var), interpolate=True, color='darkgray', alpha='0.5')
fill_between(b[1:], mu-2*np.sqrt(var), mu, interpolate=True, color='darkgray', alpha='0.5')


plt.xlabel(r'$r \left[\mathrm{Mpc/h} \right]$')
plt.ylabel(r'$\langle \delta \rangle$')

    
axhline(0.0,lw=1.5, color='black')

#legend()
ylim(-1,1)
gcf().savefig("void.png")
