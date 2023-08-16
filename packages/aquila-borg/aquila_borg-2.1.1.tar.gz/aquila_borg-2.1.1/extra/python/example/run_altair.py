#
# Example to run a Altair forward model with PyBORG
#
import borg
import numpy as np


# Setup resolution of the initial mesh
Ng = 64
# Box size in Mpc/h
L = 8000.0

# setup the box
bb = borg.forward.BoxModel()
bb.L = L, L, L
bb.N = Ng, Ng, Ng
bb.xmin = -L/2,-L/2,-L/2

print(bb)

# Initialize some default cosmology
cosmo = borg.cosmo.CosmologicalParameters()

# Fiducial scale factor to express initial conditions
a0 = 0.1

chain = borg.forward.ChainForwardModel(bb)
# Add primordial fluctuations
chain.addModel(borg.forward.models.Primordial(bb, a0))
# Add E&Hu transfer function
chain.addModel(borg.forward.models.EisensteinHu(bb))
# Run an LPT model from a=0.0 to af. The ai=a0 is the scale factor at which the IC are expressed
lpt = borg.forward.models.BorgLpt(bb, bb, ai=a0, af=1.0)
chain.addModel(lpt)

Lz=10000
altair = borg.forward.models.newModel(
    "ALTAIR_AP",
    bb,
    dict(
        corner0_z=-Lz/2,
        corner1_z=-Lz/2,
        corner2_z=-Lz/2,
        L0_z=Lz,
        L1_z=Lz,
        L2_z=Lz,
        N0_z=64,
        N1_z=64,
        N2_z=64,
        is_contrast=True
    ),
)
chain.addModel(altair)

# Set the cosmology
chain.setCosmoParams(cosmo)


# Generate white noise: it has to be scaled by 1/N**(3./2) to be one in Fourier
ic = np.random.randn(Ng, Ng, Ng) / np.sqrt(Ng ** 3)
delta_m = np.zeros(lpt.getOutputBoxModel().N)
delta_m_ap = np.zeros(chain.getOutputBoxModel().N)

# RUN!
chain.forwardModel_v2(ic)
lpt.getDensityFinal(delta_m)
chain.getDensityFinal(delta_m_ap)

# Obtain the particles
pp = np.zeros((lpt.getNumberOfParticles(), 3))
lpt.getParticlePositions(pp)

print(pp)
