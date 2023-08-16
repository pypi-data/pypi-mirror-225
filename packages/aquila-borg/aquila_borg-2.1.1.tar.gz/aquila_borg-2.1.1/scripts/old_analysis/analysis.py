#+
#   ARES/HADES/BORG Package -- ./scripts/old_analysis/analysis.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
from read_all_h5 import explore_chain
from read_all_h5 import rebuild_spliced_h5
import h5py as h5
import numpy as np
import healpy as hp
import numexpr as ne
import os
import math
from pylab import *
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show

#import numba
'''
@numba.jit
def _special_spectrum_builder(P, PP, tmp, alpha, N_i, Pk_i):

    for i in range(Pk_i.size):
        for j in range(PP.size):
            v = PP[j]**(-alpha)*exp(- N_i[i]*Pk_i[i] / (2 * PP[j]))
            tmp[j] = v
            total += v

        for j in range(PP.size):
            P[j] += tmp[j] / total
 ''' 
 
 
 #ARES/HADES/BORG image scanning class
class IndexTracker:
    def __init__(self, ax, X):
        self.ax = ax
        self.ax.set_title('use up/down keys to navigate images')

        self.X = X
        rows,cols,self.slices = X.shape
        self.ind  = self.slices/2

        cmax=X.max()
        cmin=X.min()
        
        self.im = self.ax.imshow(self.X[:,self.ind,:],vmax=cmax,vmin=cmin)
        self.update()

    def onscroll(self, event):
        #print ("%s " % (event.key))
        if event.key=='up':
            self.ind = np.clip(self.ind+1, 0, self.slices-1)
        else:
            self.ind = np.clip(self.ind-1, 0, self.slices-1)


        self.update()

    def update(self):
        self.im.set_data(self.X[:,self.ind,:])
        self.ax.set_ylabel('slice %s'%self.ind)
        self.im.axes.figure.canvas.draw()

           
#ARES/HADES/BORG analysis class
class analysis:

    def __init__(self, chain_path='.', LSS_framework='ARES'):
        self.chain_path 	= chain_path
        self.LSS_framework 	= LSS_framework
      
        self.description = "This Class is part of the ARES/HADES/BORG analysis framework"
        self.author = "Copyright (C) 2009-2016 Jens Jasche \n Copyright (C) 2014-2016 Guilhem Lavaux"
        
        #get chain setup
        
        self.L0=0
        self.L1=0
        self.L2=0
        self.N0=0
        self.N1=0
        self.N2=0
	self.x0=0
        self.x1=0
        self.x2=0
        
        with h5.File(os.path.join(self.chain_path, "restart.h5_0"), mode="r") as f:
	    info=f.require_group('/info')
	    markov=f.require_group('/markov')		
	    #print markov.keys()
	    #print info.keys()
	    print f['info']['scalars'].keys()
	    #print f['markov']['scalars'].keys()	
	
            self.L0 = f['info']['scalars']['L0'][:]
            self.L1 = f['info']['scalars']['L1'][:]
            self.L2 = f['info']['scalars']['L2'][:]
            self.N0 = int(f['info']['scalars']['N0'][:])
            self.N1 = int(f['info']['scalars']['N1'][:])
            self.N2 = int(f['info']['scalars']['N2'][:])
	    self.xmin0 = int(f['info']['scalars']['corner0'][:])
            self.xmin1 = int(f['info']['scalars']['corner1'][:])
            self.xmin2 = int(f['info']['scalars']['corner2'][:])
            self.ncat = int(f['info']['scalars']['NCAT'][:]) 
	

            if(LSS_framework!='BORG'):
                self.kmodes = f['/info/scalars/k_modes'][:]  
                self.nmodes = len(self.kmodes)
        
        #get brefs
            bref=[]	
	    for i in range(self.ncat):
		bref.append(f['info']['scalars']['galaxy_bias_ref_'+str(i)][:])
            self.bias_ref=np.array(bref)
		

    def check_biasref(self):
        return self.bias_ref

    def get_ncat(self):
        return self.ncat	

    def get_mask_spliced(self,msknr,ncpu=0):
        if ncpu>0:
            mskkey = "info.scalars.galaxy_sel_window_" + str(msknr)
            a=rebuild_spliced_h5(os.path.join(self.chain_path, "restart.h5"),[mskkey],32)
            return np.array(a[mskkey][:,:,:,0])
        else:
            print 'Error: need number of processes to read files !'    
            
    def get_mask(self,msknr):
    
	with h5.File(os.path.join(self.chain_path, "restart.h5_0"), mode="r") as f:
		mskkey = "galaxy_sel_window_" + str(msknr)
		mask = f['info']['scalars'][mskkey][:]		    
	return np.array(mask[:,:,:,0])

    def get_data(self,datnr):

	with h5.File(os.path.join(self.chain_path, "restart.h5_0"), mode="r") as f:
		datkey = "galaxy_data_" + str(datnr)
		data = f['info']['scalars'][datkey][:]		    
	return np.array(data)

    def get_data_spliced(self,msknr,ncpu=0):
        if ncpu>0:
            mskkey = "info.scalars.galaxy_data_" + str(msknr)
            a=rebuild_spliced_h5(os.path.join(self.chain_path, "restart.h5"),[mskkey],32)
            return np.array(a[mskkey][:])
        else:
            print 'Error: need number of processes to read files !'    

    def scan_datacube(self,data):
	fig = figure()
	ax = fig.add_subplot(111)
	plt.jet()
	tracker = IndexTracker(ax, data)
	fig.canvas.mpl_connect('key_press_event', tracker.onscroll)
	show()
        
                
    def get_2d_marginal(self,attribute_a='s_field',attribute_b='s_field',id_a=None,id_b=None, first_sample=0,last_sample=1000):
        print '-'*60
        print 'Estimate 2d marginals for parameters ', attribute_a, ' and ', attribute_b , ' for ' , self.LSS_framework, ' run!'
        print '-'*60
        
        if(id_a==None or id_b==None):
            print "Error: no index chosen"
            return -1
            
        #2) collect chain
        samples_a = []
        samples_b = []
        for i,a in explore_chain(self.chain_path, first_sample,last_sample, 1):
                d   = a[attribute_a][:]
                e   = a[attribute_b][:]
                
                samples_a.append(d[id_a])
                samples_b.append(e[id_b])
        
        H, xedges, yedges = np.histogram2d(samples_a, samples_b)
        
        return xedges,yedges, H
        
    def get_cross_corcoeff(self,attribute_a='s_field',attribute_b='s_field',id_a=None,id_b=None, first_sample=0,last_sample=1000):
        print '-'*60
        print 'Estimate 2d marginals for parameters ', attribute_a, ' and ', attribute_b , ' for ' , self.LSS_framework, ' run!'
        print '-'*60
        
        if(id_a==None or id_b==None):
            print "Error: no index chosen"
            return -1
            
        #2) collect chain
        samples_a = []
        samples_b = []
        
        nelements_a = len(id_a[0])
        nelements_b = len(id_b[0])
        
        mu_a    = np.zeros(nelements_a)
        var_a   = np.zeros(nelements_a)
        
        mu_b    = np.zeros(nelements_b)
        var_b   = np.zeros(nelements_b)
        nn=1
        for i,a in explore_chain(self.chain_path, first_sample,last_sample, 1):
                d   = a[attribute_a][:]
                e   = a[attribute_b][:]
                
                aux_a   = d[id_a]
                aux_b   = e[id_b]
                
                mu_a  = (nn-1.)/float(nn)*mu_a +1./float(nn)*aux_a                
                if(nn>1): 
                    aux     = (mu_a-aux_a)**2
                    var_a     = (nn-1.)/nn*var_a+1./(nn-1)*aux
                
                mu_b  = (nn-1.)/float(nn)*mu_b +1./float(nn)*aux_b                
                if(nn>1): 
                    aux     = (mu_b-aux_b)**2
                    var_b     = (nn-1.)/nn*var_b+1./(nn-1)*aux
                
                samples_a.append(aux_a)
                samples_b.append(aux_b)
                nn+=1
        
        pc= np.zeros((nelements_a,nelements_b))
        cnt=0
        for n in range(nn-1):
                x=samples_a[n]
                y=samples_b[n]
                pc += np.multiply.outer(x-mu_a, y-mu_b)
                cnt+=1
        
        return pc/float(cnt) #/np.sqrt(var_a*var_b)    
        
    
    def get_trace(self,attribute='s_field',element_id=None, first_sample=0,last_sample=1000):
        print '-'*60
        print 'Record trace for parameters ', attribute , ' for ' , self.LSS_framework, ' run!'
        print '-'*60
    
        '''
        if(element_id==None):
            print "Error: no list of indices provided"
            return -1
        '''
        
        #1) collect chain
        samples = []
          
        nn=1
        for i,a in explore_chain(self.chain_path, first_sample,last_sample, 1):
                d   = a[attribute][:]
                if (element_id!=None):
                    samples.append(d[element_id])
                else:
                    samples.append(d)          
                nn+=1
                
        return samples
    
    
    def get_corrlength(self,attribute='s_field',element_id=None,nlength=100, first_sample=0,last_sample=1000):
        print '-'*60
        print 'Estimate correlation length for parameters ', attribute , ' for ' , self.LSS_framework, ' run!'
        print '-'*60
    
        if(element_id==None):
            print "Error: no list of indices provided"
            return -1
            
        if(nlength>last_sample-first_sample):
            print "Warning: Chain setting not long enough set nlength to last_sample"
            nlength = last_sample-first_sample -1

        nelements = len(element_id[0])
    
        #1) calculate mean and variance
        mu  = np.zeros(nelements)
        var = np.zeros(nelements)
        
        #2) collect chain
        samples = []

        nn=1
        for i,a in explore_chain(self.chain_path, first_sample,last_sample, 1):
                d   = a[attribute][:]

		print np.shape(d)
          
                mu  = (nn-1.)/float(nn)*mu +1./float(nn)*d[element_id]                
                if(nn>1): 
                    aux     = (mu-d[element_id])**2
                    var     = (nn-1.)/nn*var+1./(nn-1)*aux
                
                samples.append(d[element_id])
                
                nn+=1
        

        cl      = np.zeros((nlength,nelements))
        cl_count= np.zeros(nlength)
   
        for i in range(nlength):
            for j in range(len(samples)-i):
	            cl[i]+= (samples[j]-mu)*(samples[j+i]-mu)/var
	            cl_count[i] +=1.;

        for i in range(nlength):
            cl[i]/=cl_count[i]
       
        return np.array(range(nlength)), cl

    def print_job(self,msg):
        print('-'*60)
        print(msg)
        print('-'*60)



    def spectrum_pdf(self, first_sample=0, last_sample=-1, sample_steps=10, gridsize=1000, Pmin=None, Pmax=None):
        
        P = np.zeros((gridsize, Npk), dtype=np.float64)
        
        if Pmin is None or Pmax is None:
            P0m,P0M = np.inf,0
            for i,a in explore_chain(self.chain_path, first_sample,last_sample, sample_steps):
                P0m = a['/scalars/powerspectrum'].min()
                P0M = a['/scalars/powerspectrum'].max()
                Pb_m,Pb_M = min(P0m, Pb_m),max(P0M,Pb_M)
            if Pmin is None:
                Pmin = Pb_m
            if Pmax is None:
                Pmax = Pb_M
            
        PP = Pmin*np.exp(np.arange(gridsize)*np.log(Pmax/Pmin))
        N=0
        prior=0
        N_ib = 0.5*(self.Nk+prior)[None,:]
        for i,a in explore_chain(self.chain_path, first_sample,last_sample, sample_steps):
            Pk_i = a['/scalars/powerspectrum'][:]
            N_i = self.Nk
            
            _special_spectrum_builder(P, PP, tmp_PP, N_ib, N_i, Pk_i)
            
            N += 1

        P /= N
        
        return P

    def get_spherical_slice(self,vdata,nside=32, observer=np.array([0,0,0]),rslice = 150.):

	def RenderSphere(VolumeData3D,image,rslice,observer,Larr,Narr):
    	    print "Rendering Sphere..."

	    NSIDE=hp.npix2nside(len(image))
    
    	    idx=Larr[0]/Narr[0]
    	    idy=Larr[1]/Narr[1]
    	    idz=Larr[2]/Narr[2]
    
    	    for ipix in range(len(image)):
       		#get direction of pixel and calculate unit vectors
		dx,dy,dz=hp.pix2vec(NSIDE, ipix)
	    	d = math.sqrt(dx * dx + dy * dy + dz * dz)
	    	dx = dx / d; dy = dy / d; dz = dz / d # ray unit vector
	    
	    	rayX = observer[0]+rslice*dx; rayY = observer[1]+rslice*dy; rayZ = observer[2]+rslice*dz
	    	rayX /= idx; rayY /= idy; rayZ /= idz 
	    	#find voxel inside box
	    	ix = int(round(rayX))
	    	iy = int(round(rayY))
	    	iz = int(round(rayZ))
	    
	    	image[ipix]=np.nan 
	    	if ix > -1 and ix < Narr[0] \
            		or iy > -1 and iy < Narr[1] \
            		or iz > -1 and iz < Narr[2]:
	    
	            	jx = (ix+1) % Narr[0];
	            	jy = (iy+1) % Narr[1];
	            	jz = (iz+1) % Narr[2];
	            	rx = (rayX - ix);
	            	ry = (rayY - iy);
	            	rz = (rayZ - iz);
	    
	            	qx = 1.-rx;
	            	qy = 1.-ry;
	            	qz = 1.-rz;
	            	val = VolumeData3D[ix,iy,iz] * qx * qy * qz +VolumeData3D[ix,iy,jz] * qx * qy * rz +VolumeData3D[ix,jy,iz] * qx * ry * qz +VolumeData3D[ix,jy,jz] * qx * ry * rz +VolumeData3D[jx,iy,iz] * rx * qy * qz +VolumeData3D[jx,iy,jz] * rx * qy * rz +VolumeData3D[jx,jy,iz] * rx * ry * qz +VolumeData3D[jx,jy,jz] * rx * ry * rz;
	            	image[ipix]=val

		print '\r'+str(100 * ipix / (len(image) - 1)).zfill(3) + "%"

	
        obs = np.array([observer[0]-self.xmin0,observer[1]-self.xmin1,observer[2]-self.xmin2])

	Larr=np.array([self.L0,self.L1,self.L2])
	Narr=np.array([self.N0,self.N1,self.N2]) 
	image = np.zeros(hp.nside2npix(nside))
        RenderSphere(vdata,image,rslice,obs,Larr,Narr)
	return image

    def mean_var_density(self, first_sample=0,last_sample=-1,sample_steps=10):
        self.print_job('Estimate mean and variance of density fields for %s run!' % self.LSS_framework)
    
        
        if(self.LSS_framework=='ARES'):
            mu_i    = np.zeros((self.N0,self.N1,self.N2))
            
            var_i     = np.zeros((self.N0,self.N1,self.N2))
            
            nn=1
            for i,a in explore_chain(self.chain_path, first_sample,last_sample, sample_steps):
                d = a['s_field'][:]
                mu_i    = (nn-1.)/float(nn)*mu_i +1./float(nn)*d
                
                if(nn>1): 
                    aux = (mu_i-d)**2
                    var_i   = (nn-1.)/nn*var_i+1./(nn-1)*aux
                    
                nn+=1
            
            return mu_i, var_i
            
        elif(self.LSS_framework=='HADES'):
            mu_i    = np.zeros((self.N0,self.N1,self.N2))
            
            var_i     = np.zeros((self.N0,self.N1,self.N2))
            
            nn=1
            for i,a in explore_chain(self.chain_path, first_sample,last_sample, sample_steps):
                d = a['s_field'][:]
                mu_i    = (nn-1.)/float(nn)*mu_i +1./float(nn)*d
                
                if(nn>1): 
                    aux = (mu_i-d)**2
                    var_i   = (nn-1.)/nn*var_i+1./(nn-1)*aux
                    
                nn+=1
            
            return mu_i, var_i
            
        else:
            mu_i    = np.zeros((self.N0,self.N1,self.N2))
            mu_f    = np.zeros((self.N0,self.N1,self.N2))
            
            var_i     = np.zeros((self.N0,self.N1,self.N2))
            var_f     = np.zeros((self.N0,self.N1,self.N2))
            
            nn=1
            for i,a in explore_chain(self.chain_path, first_sample,last_sample, sample_steps):
                d = a['s_field'][:]
                mu_i    = (nn-1.)/float(nn)*mu_i +1./float(nn)*d
                
                if(nn>1): 
                    aux = (mu_i-d)**2
                    var_i   = (nn-1.)/nn*var_i+1./(nn-1)*aux
                
                d = a['BORG_final_density'][:]
                mu_f    = (nn-1.)/float(nn)*mu_f +1./float(nn)*d
                
                if(nn>1):
                    aux = (mu_f-d)**2
                    var_f   = (nn-1.)/nn*var_f+1./(nn-1)*aux
                
                nn+=1
                
                
            return mu_i, var_i, mu_f, var_f

    def mean_var_spec(self, first_sample=0,last_sample=-1,sample_steps=10):
        self.print_job('Estimate mean and variance of density fields for %s run!' % self.LSS_framework)
         
        if(self.LSS_framework=='ARES'):
            mu    = np.zeros(self.nmodes)
            var   = np.zeros(self.nmodes)
            
            nn=1
            for i,a in explore_chain(self.chain_path, first_sample,last_sample, sample_steps):
                d = a['/scalars/powerspectrum'][:]
                mu    = (nn-1.)/float(nn)*mu +1./float(nn)*d
                
                if(nn>1): 
                    aux = (mu-d)**2
                    var   = (nn-1.)/nn*var+1./(nn-1)*aux
                    
                nn+=1
            
            return self.kmodes,mu, var
            
        elif(self.LSS_framework=='HADES'):
            mu    = np.zeros(self.nmodes)
            var   = np.zeros(self.nmodes)
            
            nn=1
            for i,a in explore_chain(self.chain_path, first_sample,last_sample, sample_steps):
                d = a['/scalars/powerspectrum'][:]
                mu    = (nn-1.)/float(nn)*mu +1./float(nn)*d
                
                if(nn>1): 
                    aux = (mu-d)**2
                    var   = (nn-1.)/nn*var+1./(nn-1)*aux
                    
                nn+=1
            
            return self.kmodes,mu, var
            
        else:
            mu    = np.zeros(self.nmodes)
            var   = np.zeros(self.nmodes)
            
            nn=1
            for i,a in explore_chain(self.chain_path, first_sample,last_sample, sample_steps):
                d = a['/scalars/powerspectrum'][:]
                mu    = (nn-1.)/float(nn)*mu +1./float(nn)*d
                
                if(nn>1): 
                    aux = (mu-d)**2
                    var   = (nn-1.)/nn*var+1./(nn-1)*aux
                    
                nn+=1
            
            return self.kmodes,mu, var
