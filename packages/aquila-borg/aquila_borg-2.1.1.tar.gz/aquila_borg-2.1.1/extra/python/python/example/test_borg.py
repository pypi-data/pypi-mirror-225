import io
import numpy as np
import sys
import mpi4py
import contextlib
import borg

cons=borg.console()

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


with contextlib.redirect_stdout(RewriteIO(sys.stdout)):
  
  cons.setVerboseLevel(5)
  
  cosmo_par = borg.cosmo.CosmologicalParameters()
  cosmo_par.default()
  print(repr(cosmo_par))
  
  cosmo = borg.cosmo.Cosmology(cosmo_par)
  cpower = borg.cosmo.CosmoPower(cosmo_par)
  
  box = borg.forward.BoxModel()
  box.L = (100,100,100)
  box.N = (128,128,128)
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
  # Apply 2LPT
  final_delta_2lpt = np.zeros(outN)
  model = borg.forward.models.Borg2Lpt(box,ai=0.1, particle_factor=2)
  model.setCosmoParams(cosmo_par)
  model.forwardModel(delta_hat / box.L[0]**3, final_delta_2lpt)
  del model
  
  #
  # Apply LPT
  final_delta_lpt = np.zeros(outN)
  model = borg.forward.models.BorgLpt(box,ai=0.1, particle_factor=2)
  model.holdParticles()
  model.setCosmoParams(cosmo_par)
  model.forwardModel(delta_hat / box.L[0]**3, final_delta_lpt)
  
  print(f"Num particles = {model.getNumberOfParticles()}")
  Npart = model.getNumberOfParticles()
  print(f"Grid = {Npart**(1./3)}")
  x=np.empty((Npart,3),dtype=np.float64)
  v=np.empty((Npart,3),dtype=np.float64)
  model.getParticlePositions(x)
  model.getParticleVelocities(v)
  
  del model
  
  #
  # Apply PM
  final_delta_pm = np.zeros(outN)
  model = borg.forward.models.BorgPM(box,ai=0.1, nsteps=5, particle_factor=2, supersampling=2)
  model.setAdjointRequired(False)
  model.setCosmoParams(cosmo_par)
  model.forwardModel(delta_hat / box.L[0]**3, final_delta_pm)
  del model

  #
  # Apply PM
  final_delta_pm2 = np.zeros(outN)
  model = borg.forward.models.BorgPM(box,ai=0.1, nsteps=5, particle_factor=2, supersampling=2, force_factor=2)
  model.setAdjointRequired(False)
  model.setCosmoParams(cosmo_par)
  model.forwardModel(delta_hat / box.L[0]**3, final_delta_pm2)
  del model
  
  #
  # Apply PM-RSD
  final_delta_pm_rsd = np.zeros(outN)
  model = borg.forward.models.BorgPM(box,ai=0.1, nsteps=5, particle_factor=2,rsd=True)
  model.setAdjointRequired(False)
  model.setCosmoParams(cosmo_par)
  model.forwardModel(delta_hat / box.L[0]**3, final_delta_pm_rsd)
  del model
  
  np.savez("results.npz", lpt=final_delta_lpt, tlpt=final_delta_2lpt, pm=final_delta_pm, pm2=final_delta_pm2, pm_rsd=final_delta_pm_rsd)
