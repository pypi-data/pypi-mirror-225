import itertools
from tqdm import tqdm
import borg
import numpy as np

cons = borg.console()

myprint = lambda x: cons.print_std(x) if type(x) == str else cons.print_std(
    repr(x))


def build_gravity_model(box, cpar):
    lpt = borg.forward.models.BorgLpt(box, box, ai=1.0)
    chain = borg.buildDefaultChain(box, cpar, 1.0, lpt)
    vfield = borg.forward.velocity.CICModel(box, lpt)
    return chain, lpt, vfield


if not borg.EMBEDDED and __name__ == "__main__":
    from tqdm import tqdm

    Ng = 8

    # Create the auxiliary objects
    cpar = borg.cosmo.CosmologicalParameters()
    box = borg.forward.BoxModel(100., Ng)

    fwd, lpt, vfield = build_gravity_model(box, cpar)

    s_hat = np.fft.rfftn(np.random.randn(Ng, Ng, Ng) / Ng**(1.5))

    def vfield_like(s_hat):
        fwd.forwardModel_v2(s_hat)
        rho = np.zeros((Ng, Ng, Ng))
        fwd.getDensityFinal(rho)
        vgrid = vfield.getVelocityField()
        return (vgrid**2).sum()

    def vfield_ag(s_hat):
        fwd.forwardModel_v2(s_hat)
        rho = np.zeros((Ng, Ng, Ng))
        fwd.getDensityFinal(rho)
        # The derivative of square is 2 * vector
        vgrid = 2 * vfield.getVelocityField()

        fwd.clearAdjointGradient()
        vfield.computeAdjointModel(vgrid)
        myprint("Calling adjoint")
        # We have to trigger the adjoint computation in any case
        fwd.adjointModel_v2(None)
        myprint("Done with adjoint")
        analytic_gradient = np.zeros((Ng, Ng, Ng // 2 + 1),
                                     dtype=np.complex128)
        fwd.getAdjointModel(analytic_gradient)
        return analytic_gradient

    myprint("Running adjoint")

    num_gradient = np.zeros((Ng, Ng, Ng // 2 + 1), dtype=np.complex128)
    s_hat_epsilon = s_hat.copy()
    cons.setVerboseLevel(5)
    analytic_gradient = vfield_ag(s_hat)
    cons.setVerboseLevel(1)

    epsilon = 0.001
    for i, j, k in tqdm(itertools.product(*map(range, [Ng, Ng, Ng // 2 + 1])),
                        total=Ng * Ng * (Ng // 2 + 1)):
        s_hat_epsilon[i, j, k] = s_hat[i, j, k] + epsilon
        L = vfield_like(s_hat_epsilon)
        s_hat_epsilon[i, j, k] = s_hat[i, j, k] - epsilon
        L -= vfield_like(s_hat_epsilon)
        QQ = L / (2.0 * epsilon)

        s_hat_epsilon[i, j, k] = s_hat[i, j, k] + 1j * epsilon
        L = vfield_like(s_hat_epsilon)
        s_hat_epsilon[i, j, k] = s_hat[i, j, k] - 1j * epsilon
        L -= vfield_like(s_hat_epsilon)
        QQ = QQ + L * 1j / (2.0 * epsilon)

        s_hat_epsilon[i, j, k] = s_hat[i, j, k]

        num_gradient[i, j, k] = QQ

    np.savez("gradients.npz", num=num_gradient, ana=analytic_gradient)
