#
# Example to run a forward model with PyBORG
#
import borg
import numpy as np


# Setup resolution of the initial mesh
Ng=64
# Box size in Mpc/h
L=100.

# setup the box
bb = borg.forward.BoxModel()
bb.L = L,L,L
bb.N = Ng,Ng,Ng

# Initialize some default cosmology
cosmo = borg.cosmo.CosmologicalParameters()

# Fiducial scale factor to express initial conditions
a0=0.1

chain = borg.forward.ChainForwardModel(bb)
# Add primordial fluctuations
chain.addModel(borg.forward.models.Primordial(bb, a0))
# Add E&Hu transfer function
chain.addModel(borg.forward.models.EisensteinHu(bb))
# Run an LPT model from a=0.0 to af. The ai=a0 is the scale factor at which the IC are expressed
lpt = borg.forward.models.BorgLpt(bb, bb, ai=a0, af=1.0)
chain.addModel(lpt)

# Set the cosmology
chain.setCosmoParams(cosmo)


# Generate white noise: it has to be scaled by 1/N**(3./2) to be one in Fourier
ic = np.random.randn(Ng, Ng, Ng)/np.sqrt(Ng**3)
delta_m = np.zeros((Ng,Ng,Ng))

# RUN!
chain.forwardModel_v2(ic)
chain.getDensityFinal(delta_m)

# Obtain the particles
pp = np.zeros((lpt.getNumberOfParticles(),3))
lpt.getParticlePositions(pp)

print(pp)
