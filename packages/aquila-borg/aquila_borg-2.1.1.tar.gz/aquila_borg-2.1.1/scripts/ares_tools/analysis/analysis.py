#+
#   ARES/HADES/BORG Package -- ./scripts/ares_tools/analysis/analysis.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
from ..read_all_h5 import explore_chain, rebuild_spliced_h5
import errno
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


def detect_ncpus(path):
  ncpu = 0
  try:
    while True:
      with open("%s_%d" % (path,ncpu), mode= "rb") as f:
        ncpu += 1
  except IOError as e:
    if e.errno != errno.ENOENT:
      raise e

  return ncpu



#ARES/HADES/BORG analysis class
class analysis:


    def __init__(self, chain_path='.', LSS_framework='ARES', start=0, step=1):
        self.chain_path         = chain_path
        self.LSS_framework      = LSS_framework

        self.description = "This Class is part of the ARES/HADES/BORG analysis framework"
        self.author = "Copyright (C) 2009-2017 Jens Jasche \n Copyright (C) 2014-2017 Guilhem Lavaux"

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

        self.ncpus = detect_ncpus(os.path.join(self.chain_path, "restart.h5"))

        self.mcmc_list=[]
        Fmax=start
        while True:
            try:
              os.stat("mcmc_%d.h5" % Fmax)
            except:
              break
            self.mcmc_list.append(Fmax)
            Fmax += step
        

        with h5.File(os.path.join(self.chain_path, "restart.h5_0"), mode="r") as f:
            #print markov.keys()
            #print info.keys()
            #print f['scalars'].keys()

            self.L0 = f['scalars']['L0'][0]
            self.L1 = f['scalars']['L1'][0]
            self.L2 = f['scalars']['L2'][0]
            self.N0 = int(f['scalars']['N0'][:])
            self.N1 = int(f['scalars']['N1'][:])
            self.N2 = int(f['scalars']['N2'][:])
            self.xmin0 = int(f['scalars']['corner0'][:])
            self.xmin1 = int(f['scalars']['corner1'][:])
            self.xmin2 = int(f['scalars']['corner2'][:])
            self.ncat = int(f['scalars']['NCAT'][:])

            if(LSS_framework!='BORG'):
                self.kmodes = f['/scalars/k_modes'][:]
                self.nmodes = len(self.kmodes)


        #get brefs
            #self.k_keys = rebuild_spliced_h5(os.path.join(self.chain_path, "restart.h5"), ["scalars.k_keys"], self.ncpus)["scalars.k_keys"]

            bref=[]
            if LSS_framework != 'VIRBIUS' and LSS_framework != 'LYA':
              for i in range(self.ncat):
                  bref.append(f['scalars']['galaxy_bias_ref_'+str(i)][:])
              self.bias_ref=np.array(bref)

    def _internal_power(self, P, Nbins, range, unit=False):
        if not hasattr(self, '_k'):
          ik0 = np.fft.fftfreq(self.N0, d=self.L0/self.N0)*2*np.pi
          ik1 = np.fft.fftfreq(self.N1, d=self.L1/self.N1)*2*np.pi
          ik2 = np.fft.fftfreq(self.N2, d=self.L2/self.N2)*2*np.pi
          k = self._k = np.sqrt(ik0[:,None,None]**2+ik1[None,:,None]**2+ik2[None,None,:(self.N2//2+1)]**2)
          self._Pw, _ = np.histogram(k, bins=Nbins, range=range)
          Pw = self._Pw
        else:
          k = self._k 
          Pw = self._Pw

        P, b = np.histogram(k, weights=P, bins=Nbins, range=range)
        if not unit:
          P /= self.L0*self.L1*self.L2
        cond = Pw > 0
        P[cond] /= Pw[cond]
        return P, Pw, b 

    def rebin_power_spectrum(self, chain_id, Nbins=100, range=(0,1), unit=False):
        with h5.File(os.path.join(self.chain_path, "mcmc_%d.h5" % (chain_id,)), mode="r") as f:
          P = f['/scalars/powerspectrum'][...] * (self.L0 * self.L1 * self.L2)

        return self._internal_power(P[self.k_keys], Nbins, range, unit=unit)


    def compute_power_spectrum_mock(self, Nbins=100, unit=False, range=(0,1)):
        with h5.File(os.path.join(self.chain_path, "mock_data.h5"), mode="r") as f:
          shat = f['/scalars/s_hat_field'][...]
        return self._internal_power(ne.evaluate('real(s)**2+imag(s)**2', dict(s=shat)), Nbins, range, unit=unit)

    def compute_power_spectrum_galaxydata(self, Nbins=100, range=(0,1)):
        with h5.File(os.path.join(self.chain_path, "mock_data.h5"), mode="r") as f:
          # FFT galaxy data  
          dV = self.L0*self.L1*self.L2/(self.N0*self.N1*self.N2)
          fd = np.fft.rfftn(f['/scalars/galaxy_data_0'][...])*dV
          # remove zero mode
          fd[0][0][0] = 0. + 0.j
        return self._internal_power(ne.evaluate('real(s)**2+imag(s)**2', dict(s=fd)), Nbins, range)

    def compute_power_shat_spectrum(self, chain_id, Nbins=100, unit=False, range=(0,1)):

        dV = self.L0*self.L1*self.L2/(self.N0*self.N1*self.N2)

        with h5.File(os.path.join(self.chain_path, "mcmc_%d.h5" % (chain_id,)), mode="r") as f:
          if '/scalars/s_hat_field' in f:
            shat = f['/scalars/s_hat_field'][...]
          else:
            shat = np.fft.rfftn(f['/scalars/s_field'][...])*dV

        return self._internal_power(ne.evaluate('real(s)**2+imag(s)**2', dict(s=shat)), Nbins, range, unit=unit)

    def compute_power_shat_cross_spectrum(self, chain_id1, chain_id2,
                                          Nbins=100, unit=False, range=(0,1)):

        dV = self.L0*self.L1*self.L2/(self.N0*self.N1*self.N2)

        with h5.File(os.path.join(self.chain_path, "mcmc_%d.h5" % (chain_id1,)), mode="r") as f:
          if '/scalars/s_hat_field' in f:
            shat1 = f['/scalars/s_hat_field'][...]
          else:
            shat1 = np.fft.rfftn(f['/scalars/s_field'][...])*dV

        with h5.File(os.path.join(self.chain_path, "mcmc_%d.h5" % (chain_id2,)), mode="r") as f:
          if '/scalars/s_hat_field' in f:
            shat2 = f['/scalars/s_hat_field'][...]
          else:
            shat2 = np.fft.rfftn(f['/scalars/s_field'][...])*dV

        return self._internal_power(ne.evaluate('real(s1)*real(s2)+imag(s1)*imag(s2)', dict(s1=shat1,s2=shat2)), Nbins, range, unit=unit)
    
        #return self._internal_power(ne.evaluate('real(s)**2+imag(s)**2', dict(s=shat)), Nbins, range, unit=unit)

    # maybe 'unit' argument is not sensible here...
    def compute_power_spectrum_finaldensity(self, chain_id, Nbins=100, unit=False, range=(0,1)):

        dV = self.L0*self.L1*self.L2/(self.N0*self.N1*self.N2)

        with h5.File(os.path.join(self.chain_path, "mcmc_%d.h5" % (chain_id,)), mode="r") as f:
            fd = np.fft.rfftn(f['/scalars/BORG_final_density'][...]) * dV

        return self._internal_power(ne.evaluate('real(s)**2+imag(s)**2', dict(s=fd)), Nbins, range, unit=unit)

    # compute power spectrum of real-space field from given path and field name
    def compute_power_shat_spectrum_file(self, path, fieldname='phases', Nbins=100, unit=False, range=(0,1)):

        dV = self.L0*self.L1*self.L2/(self.N0*self.N1*self.N2)

        with h5.File(path, mode="r") as f:
          if fieldname in f:
              # do FFT
              shat = np.fft.rfftn(f[fieldname][...])*dV
              # remove zero mode
              shat[0][0][0] = 0. + 0.j
          else:
              print("No field '%s' found in file." % fieldname)

        return self._internal_power(ne.evaluate('real(s)**2+imag(s)**2', dict(s=shat)), Nbins, range, unit=unit)

    def check_biasref(self):
        return self.bias_ref

    def get_ncat(self):
        return self.ncat

    def get_mask(self,msknr):
        selkey = "scalars.galaxy_sel_window_%s"%msknr
        return \
             rebuild_spliced_h5(
                 os.path.join(
                    self.chain_path,"restart.h5"
                 ),
                 [selkey],
                 self.ncpus
             )[selkey] 

    def get_data(self,datnr):
        datkey = "scalars.galaxy_data_%s"%datnr
        return \
             rebuild_spliced_h5(
                 os.path.join(
                    self.chain_path,"restart.h5"
                 ),
                 [datkey],
                 self.ncpus
             )[datkey]

    def scan_datacube(self,data):
        fig = figure()
        ax = fig.add_subplot(111)
        plt.jet()
        tracker = IndexTracker(ax, data)
        fig.canvas.mpl_connect('key_press_event', tracker.onscroll)
        show()


    def get_2d_marginal(self,attribute_a='s_field',attribute_b='s_field',id_a=None,id_b=None, first_sample=0,last_sample=1000):
        print( '-'*60)
        print( 'Estimate 2d marginals for parameters ', attribute_a, ' and ', attribute_b , ' for ' , self.LSS_framework, ' run!')
        print( '-'*60)

        if(id_a==None or id_b==None):
            print( "Error: no index chosen")
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
        print( '-'*60)
        print( 'Estimate 2d marginals for parameters ', attribute_a, ' and ', attribute_b , ' for ' , self.LSS_framework, ' run!')
        print( '-'*60)

        if(id_a==None or id_b==None):
            print("Error: no index chosen")
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
        print( '-'*60)
        print( 'Record trace for parameters ', attribute , ' for ' , self.LSS_framework, ' run!')
        print( '-'*60)

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
        print( '-'*60)
        print( 'Estimate correlation length for parameters ', attribute , ' for ' , self.LSS_framework, ' run!')
        print( '-'*60)

        if(element_id==None):
            print( "Error: no list of indices provided")
            return -1

        if(nlength>last_sample-first_sample):
            print("Warning: Chain setting not long enough set nlength to last_sample")
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

            print( np.shape(d))

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


    def build_power_spectrum_chain(Nbins=256):
      opts=dict(Nbins=Nbins,range=(0,self.kmodes.max()))
      #FIXME: Do not use the first element
      Pref = self.rebin_power_spectrum(self.mcmc_list[0], **opts)
      try:
        data = np.load("power_%s.npz" % suffix)
        loc_names = names[len(data['P']):]
        PP = list(data['P'])
      except:
        PP = []
        loc_names = list(names)
      print(loc_names)
      if len(loc_names) == 0:
        return
      
      for i in pb.ProgressBar()(loc_names):
        PP.append(ss.compute_power_shat_spectrum(i, **opts))
      
      bins = 0.5*(Pref[2][1:]+Pref[2][:-1])
      
      np.savez("power_%s.npz" % suffix, bins=bins, P=PP, startMC=startMC, Fmax=Fmax, Pref=Pref)


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
            print( "Rendering Sphere...")

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

                    qx = 1-rx;
                    qy = 1-ry;
                    qz = 1-rz;
                    val = VolumeData3D[ix,iy,iz] * qx * qy * qz +VolumeData3D[ix,iy,jz] * qx * qy * rz +VolumeData3D[ix,jy,iz] * qx * ry * qz +VolumeData3D[ix,jy,jz] * qx * ry * rz +VolumeData3D[jx,iy,iz] * rx * qy * qz +VolumeData3D[jx,iy,jz] * rx * qy * rz +VolumeData3D[jx,jy,iz] * rx * ry * qz +VolumeData3D[jx,jy,jz] * rx * ry * rz;
                    image[ipix]=val

                print( '\r'+str(100 * ipix / (len(image) - 1)).zfill(3) + "%")


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
