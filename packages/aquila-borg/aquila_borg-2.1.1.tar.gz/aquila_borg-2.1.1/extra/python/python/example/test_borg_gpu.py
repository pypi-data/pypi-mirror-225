import matplotlib.pyplot as plt
import numpy as np
import borg
import jax
import jax.numpy as jnp

myprint = lambda s: borg.console().print_std(s if type(s) == str else repr(s))


def get_psi(k2, k, x, L, delta_hat, inv_dVol):
    phi_hat = jnp.where(k2 == 0.0, 0.0j, delta_hat * 1j * k / (k2+1e-19))
    phi_hat[0,0,0]=0j
    p = x + jnp.fft.irfftn(phi_hat) * inv_dVol
    return jnp.where(p >= 0, p % L, L - (-p) % L)


def mymodf(x):
    ix = jnp.floor(x)
    return x - ix, ix


def do_cic(x, y, z, Nx, Ny, Nz, Lx, Ly, Lz):

    Ntot = Nx * Ny * Nz
    x = x * Nx / Lx
    y = y * Ny / Ly
    z = z * Nz / Lz
    qx, ix = mymodf(x)
    qy, iy = mymodf(y)
    qz, iz = mymodf(z)
    ix = ix.astype(int)
    iy = iy.astype(int)
    iz = iz.astype(int)
    rx = 1.0 - qx
    ry = 1.0 - qy
    rz = 1.0 - qz
    jx = (ix + 1) % Nx
    jy = (iy + 1) % Ny
    jz = (iz + 1) % Nz

    rho = jnp.zeros((Ntot, ))

    for a in [False, True]:
        for b in [False, True]:
            for c in [False, True]:
                ax = jx if a else ix
                ay = jy if b else iy
                az = jz if c else iz
                ux = qx if a else rx
                uy = qy if b else ry
                uz = qz if c else rz

                idx = az + Nz * ay + Nz * Ny * ax
                rho += jnp.bincount(idx, weights=ux * uy * uz, length=Ntot)

    return rho.reshape((Nx, Ny, Nz)) / (x.shape[0] / Ntot) - 1.0


def build_density(delta_hat, ikx, iky, ikz, x, y, z, N0: int, N1: int, N2: int,
                  L0: float, L1: float, L2: float, inv_dVol: float):
    k2 = ikx**2 + iky**2 + ikz**2
    return do_cic(
        get_psi(k2, ikx, x, L0, delta_hat, inv_dVol).flatten(),
        get_psi(k2, iky, y, L1, delta_hat, inv_dVol).flatten(),
        get_psi(k2, ikz, z, L2, delta_hat, inv_dVol).flatten(), N0, N1, N2, L0,
        L1, L2)


build_density = jax.jit(build_density, (7, 8, 9))


class JaxLpt(borg.forward.BaseForwardModel):
    def __init__(self, box):
        super().__init__(box, box)
        N0, N1, N2 = box.N
        L0, L1, L2 = box.L
        self.ikx = 2 * np.pi * jnp.fft.fftfreq(N0, d=L0 / N0)[:, jnp.newaxis,
                                                              jnp.newaxis]
        self.iky = 2 * np.pi * jnp.fft.fftfreq(N1, d=L1 / N1)[jnp.newaxis, :,
                                                              jnp.newaxis]
        self.ikz = 2 * np.pi * jnp.fft.fftfreq(
            N2, d=L2 / N2)[jnp.newaxis, jnp.newaxis, :(N2 // 2 + 1)]
        self.x = jnp.arange(N0)[:, jnp.newaxis, jnp.newaxis] * L0 / N0
        self.y = jnp.arange(N1)[jnp.newaxis, :, jnp.newaxis] * L1 / N1
        self.z = jnp.arange(N2)[jnp.newaxis, jnp.newaxis, :] * L2 / N2
        self.inv_dVol = box.Ntot / box.volume
        self.L = tuple(box.L)
        self.N = tuple(box.N)

    def getPreferredInput(self):
        return borg.forward.PREFERRED_FOURIER

    def getPreferredOutput(self):
        return borg.forward.PREFERRED_REAL

    def forwardModel_v2_impl(self, input_array):
        import jax.numpy as jnp
        myprint("In fwdmodel!")
        delta_hat = jnp.array(input_array)
        self.save_array, self.grad = jax.vjp(
            lambda d: build_density(d, self.ikx, self.iky, self.ikz, self.x,
                                    self.y, self.z, self.N[0], self.N[1], self.
                                    N[2], self.L[0], self.L[1], self.L[
                                        2], self.inv_dVol), delta_hat)

    def getDensityFinal_impl(self, output_array):
        output_array[:] = self.save_array

    def adjointModel_v2_impl(self, input_ag):
        ag_delta = jnp.array(input_ag)
        self.output_ag, = self.grad(ag_delta)

    def getAdjointModel_impl(self, output_ag):
        output_ag[:] = self.output_ag

    def setModelParams(self, myparams):
        print(f"setModelParams in python: pars={myparams}")


cons = borg.console()

cons.setVerboseLevel(5)

cosmo_par = borg.cosmo.CosmologicalParameters()
cosmo_par.default()
print(repr(cosmo_par))

cosmo = borg.cosmo.Cosmology(cosmo_par)

box = borg.forward.BoxModel()
box.L = (100, 100, 100)
box.N = (64,64,64)#, 32, 32)
print(box)

rho = np.zeros(box.N)
rho_gpu = np.zeros(box.N)
icplus = np.zeros((box.N[0], box.N[1], box.N[2] // 2 + 1), dtype=np.complex128)

ic = np.fft.rfftn(np.random.randn(*box.N)) / box.N[0]**(1.5)

box2 = borg.forward.BoxModel()
box2.L = box.L
box2.N = tuple(map(lambda x: 2 * x, box.N))

h = borg.forward.models.HermiticEnforcer(box)
primordial = borg.forward.models.Primordial(box, 1.0)
ehu = borg.forward.models.EisensteinHu(box)

chain = borg.forward.ChainForwardModel(box)
chain.addModel(h)
chain.addModel(primordial)
chain.addModel(ehu)
chain.setCosmoParams(cosmo_par)

#lpt_gpu = borg.forward.models.newModel("LPT_GPU", box, {});
lpt = borg.forward.models.newModel(
    "LPT_CIC", box,
    dict(a_initial=1.0,
         a_final=1.0,
         do_rsd=False,
         supersampling=1,
         lightcone=False,
         part_factor=1.1,
         mul_out=1))
lpt_omp = borg.forward.models.newModel(
    "LPT_CIC_OPENMP", box,
    dict(a_initial=1.0,
         a_final=1.0,
         do_rsd=False,
         supersampling=1,
         lightcone=False,
         part_factor=1.1,
         mul_out=1))

rho = np.zeros(box.N)
rho_gpu = np.zeros(box.N)
rho_omp = np.zeros(box.N)
icplus = np.zeros(box.N)

#chain.addModel(lpt_gpu)
chain.forwardModel_v2(ic)
chain.getDensityFinal(icplus)

lpt_gpu = JaxLpt(box)

#
lpt.setCosmoParams(cosmo_par)
#lpt_omp.setCosmoParams(cosmo_par)
#ehu.getDensityFinal(icplus)
lpt.forwardModel_v2(icplus)
lpt.getDensityFinal(rho)
lpt_gpu.forwardModel_v2(icplus)
lpt_gpu.getDensityFinal(rho_gpu)
#lpt_omp.forwardModel_v2(icplus)
#lpt_omp.getDensityFinal(rho_omp)
#
#
ag = np.random.uniform(size=box.N)/10.
lpt_gpu.adjointModel_v2(ag)
ag_gpu = np.zeros(box.N)
lpt_gpu.getAdjointModel(ag_gpu)

lpt.adjointModel_v2(ag)
ag_cpu = np.zeros(box.N)
lpt.getAdjointModel(ag_cpu)
