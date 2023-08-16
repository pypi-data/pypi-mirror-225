#+
#   ARES/HADES/BORG Package -- ./scripts/check_likelihood_trace.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import read_all_h5
import h5py as h5
from pylab import *
from analysis.analysis import *

#This routine calculates the log-likelihood for a given catalog
def psi_lh(delta,Nobs,selection,nmean,bias,rho_g,eps_g):
    print 'calculating log likelihood...'
    #only calculate for values inside observed domain
    foo=np.where(selection>0.)
    delta=delta[foo]
    rho=1.+delta+1e-12
    Nobs=Nobs[foo]
    selection=selection[foo]
        
    lamb = selection*nmean*(rho**bias)*np.exp(-rho_g*(rho**(-eps_g)))
    aux= lamb - Nobs*(np.log(selection*nmean)+bias*np.log(rho)-rho_g*(rho**(-eps_g)))
    print 'done!'    
    return np.sum(aux)

chain_path="/scratch/jasche/panphasia_run_pm/"

ares=analysis(chain_path=chain_path,LSS_framework='BORG')
ncat=ares.get_ncat()
#load data and masks
mask=[]
nobs=[]
for i in range(ncat):
    print 'load data of catalog Nr.:',i,'...'
    mask.append(ares.get_mask_spliced(i,ncpu=32))
    nobs.append(ares.get_data_spliced(i,ncpu=32))
    print 'done!'  

#open sample
hh=[]
xx=[]

for l in range(822,1350,1):
    #set log likelihood to zero
    H=0
    #open file and get data for smaple
    with h5.File(chain_path + 'mcmc_'+str(l)+'.h5', mode="r") as f:

        delta = f['scalars']['BORG_final_density'][:]
        haux=np.zeros(ncat+1)
        for i in range(ncat):
            nmean   = f['scalars']['galaxy_nmean_' +str(i)][:]
            bias    = f['scalars']['galaxy_bias_' +str(i)][:]
            rho_g   = f['scalars']['galaxy_rho_g_' +str(i)][:]
            eps_g   = f['scalars']['galaxy_eps_g_' +str(i)][:] 
            
            print nmean,bias,rho_g,eps_g
            
            haux[i] = psi_lh(delta,nobs[i],mask[i] ,nmean,bias,rho_g,eps_g)      
            haux[ncat]+=haux[i]
            print nmean,bias,rho_g,eps_g,haux[i]
        
        hh.append(haux)
        xx.append(l)
        
        hha=np.array(hh)
        xxa=np.array(xx)
        print l
        
        np.savez('lh_trace_pm',hh=hha,xx=xxa)
        
plt.plot(xxa,hha)
plt.show()
            
