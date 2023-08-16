import numpy as np
import _borg

cosmo_par = _borg.cosmo.CosmologicalParameters()
cosmo_par.default()
print(repr(cosmo_par))

cosmo = _borg.cosmo.Cosmology(cosmo_par)
cpower = _borg.cosmo.CosmoPower(cosmo_par)

box = _borg.forward.BoxModel()
box.L = (100,100,100)
box.N = (128,128,128) 
print(box)

# Generate random numbers variance 1 in fourier space
indelta = np.random.randn(*box.N)
indelta /= np.sqrt(indelta.size)
delta_hat = np.fft.rfftn(indelta)

# Generate k grid
ik = np.fft.fftfreq(box.N[0], d=box.L[0]/box.N[0] ) *2*np.pi
kx,ky,kz = np.meshgrid(ik,ik,ik[:(box.N[0]//2 + 1)])
kn = np.sqrt(kx**2 + ky**2 + kz**2)

# Scale and multiply by power spectrum
scale = cosmo.d_plus(0.1)/cosmo.d_plus(1.0)
delta_hat *= scale* np.sqrt(box.L[0]**3 * cpower.power(kn))

#
# Apply LPT
final_delta_lpt = np.zeros(box.N)
model = _borg.forward.models.BorgLpt(box,ai=0.1, particle_factor=2)
model.setCosmoParams(cosmo_par)
model.forwardModel(delta_hat / box.L[0]**3, final_delta_lpt)


biased_density = np.zeros_like(final_delta_lpt)
biased_density_2 = np.zeros_like(final_delta_lpt)
_borg.bias.PowerLawBias().compute(model, 1.0, [1.0,2.0], final_delta_lpt, biased_density)
_borg.bias.BrokenPowerLawBias().compute(model, 1.0, [1.0,2.0,0.1,0.1], final_delta_lpt, biased_density_2)
