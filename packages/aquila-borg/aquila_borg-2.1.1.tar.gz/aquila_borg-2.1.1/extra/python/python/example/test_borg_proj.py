from matplotlib import pyplot as plt
import io
import numpy as np
import sys
import mpi4py
import contextlib
import mpi4py.MPI
import _borg

cons=_borg.console()

M = 128
pfact=1.02

class RewriteIO(io.IOBase):
    def __init__(self, original):
        self.original = original
        self.newline = False
        self.comm = mpi4py.MPI.COMM_WORLD
        self.prefix = f'[{self.comm.rank} / {self.comm.size}] '

    def write(self, b):
        if b[0] == '\n':
            return self.original.write(b)
        return self.original.write(self.prefix + b)

    def writelines(self,lines):
        return self.original.writelines(lines)


def make_P(box, delta):
  ik = np.fft.fftfreq(box.N[0], d=box.L[0]/box.N[0] ) *2*np.pi
  kx,ky,kz = np.meshgrid(ik,ik,ik[:(box.N[0]//2 + 1)])
  kn = np.sqrt(kx**2 + ky**2 + kz**2)

  delta_hat = np.fft.rfftn(delta) * box.volume / box.Ntot
  P, bins = np.histogram(kn, weights = np.abs(delta_hat)**2, range=(0,1),bins=50)
  Pw, _ = np.histogram(kn, range=(0,1),bins=50)
  P = P / Pw / box.volume
  return bins, P
  

with contextlib.redirect_stdout(RewriteIO(sys.stdout)):
  
  cons.setVerboseLevel(5)
  
  cosmo_par = _borg.cosmo.CosmologicalParameters()
  cosmo_par.default()
  print(repr(cosmo_par))
  
  cosmo = _borg.cosmo.Cosmology(cosmo_par)
  cpower = _borg.cosmo.CosmoPower(cosmo_par)
  
  box = _borg.forward.BoxModel()
  box.L = (600,600,600)
  box.N = (M,M,M)
  print(box)
  
  # Generate random numbers variance 1 in fourier space
  indelta = np.random.randn(*box.N)
  indelta /= np.sqrt(indelta.size)
  delta_hat = np.fft.rfftn(indelta)

  comm = mpi4py.MPI.COMM_WORLD
  delta_hat = delta_hat[comm.rank*box.N[0]//comm.size : (comm.rank+1)*box.N[0]//comm.size, :, :]
  
  # Generate k grid
  ik = np.fft.fftfreq(box.N[0], d=box.L[0]/box.N[0] ) *2*np.pi
  kx,ky,kz = np.meshgrid(ik,ik,ik[:(box.N[0]//2 + 1)])
  kn = np.sqrt(kx**2 + ky**2 + kz**2)
  kn = kn[comm.rank*box.N[0]//comm.size : (comm.rank+1)*box.N[0]//comm.size, :, :]
  
  # Scale and multiply by power spectrum
  scale = cosmo.d_plus(0.1)/cosmo.d_plus(1.0)
  delta_hat *= scale* np.sqrt(box.L[0]**3 * cpower.power(kn))

  outN = (comm.rank+1)*box.N[0]//comm.size - (comm.rank)*box.N[0]//comm.size, box.N[1], box.N[2]
  
  #
  # Apply LPT
  final_delta_lpt = np.zeros(outN)
  model = _borg.forward.models.BorgLpt(box,ai=0.1, particle_factor=pfact)
  model.holdParticles()
  model.setCosmoParams(cosmo_par)
  model.forwardModel(delta_hat / box.L[0]**3, final_delta_lpt)
  del model

  final_delta_lpt_ngp_quad = np.zeros(outN)
  model = _borg.forward.models.BorgLptNGP_Quad(box,ai=0.1, particle_factor=pfact)
  model.holdParticles()
  model.setCosmoParams(cosmo_par)
  model.forwardModel(delta_hat / box.L[0]**3, final_delta_lpt_ngp_quad)
  del model

  final_delta_lpt_smooth_ngp_quad = np.zeros(outN)
  model = _borg.forward.models.BorgLptSmoothNGP_Quad(box,ai=0.1, particle_factor=pfact)
  model.holdParticles()
  model.setCosmoParams(cosmo_par)
  model.forwardModel(delta_hat / box.L[0]**3, final_delta_lpt_smooth_ngp_quad)
  del model


  P_cic = make_P(box, final_delta_lpt)
  P_ngp_quad = make_P(box, final_delta_lpt_ngp_quad)
  P_smooth_ngp_quad = make_P(box, final_delta_lpt_smooth_ngp_quad)

  kk = (P_cic[0][1:]+P_cic[0][:-1])/2
  fig=plt.figure()
  ax = fig.add_subplot(111)
  ax.loglog(kk,P_ngp_quad[1],label='MNGP QUAD')
  ax.loglog(kk,P_smooth_ngp_quad[1],label='Smooth QUAD')
  ax.loglog(kk,P_cic[1],label='CIC')
  ax.loglog(kk,cpower.power(kk),label='linear')
  ax.legend()
  ax.set_xlabel('$k (h/Mpc)$')
  ax.set_ylabel("$P(k)$")
  ax.set_ylim(1,1e5)

  fig.savefig(f"P_{box.N[0]}.pdf")

