import itertools
from tqdm import tqdm
import borg
import numpy as np


def build_gravity_model(state, box, cpar):
    print(cpar)
    lpt = borg.forward.models.BorgLpt(box, box, ai=1.0)
    chain = borg.buildDefaultChain(box, cpar, 1.0, lpt)
    return chain, lpt


def build_likelihood(state, info):
    return borg.likelihood.GaussianLinear(info)


if not borg.EMBEDDED and __name__ == "__main__":
    from tqdm import tqdm

    Ng =  8

    cpar = borg.cosmo.CosmologicalParameters()
    state = borg.likelihood.MarkovState()
    info = borg.likelihood.LikelihoodInfo()
    info["GRID_LENGTH"] = np.array([0, 100., 0, 100., 0, 100.])
    info["GRID"] = np.array([Ng, Ng, Ng], dtype=np.uint32)
    box = borg.forward.BoxModel(100., Ng)

    state.newArray3d("galaxy_data_0", Ng, Ng, Ng)

    fwd, lpt = build_gravity_model(state, box, cpar)
    state.newForwardModel("BORG_model", fwd)
    state.newScalar("corner0", 0.0)
    state.newScalar("corner1", 0.0)
    state.newScalar("corner2", 0.0)
    state.newScalar("localNdata0", 0, False, "L")
    state.newScalar("localNdata1", Ng, False, "L")
    state.newScalar("localNdata2", 0, False, "L")
    state.newScalar("localNdata3", Ng, False, "L")
    state.newScalar("localNdata4", 0, False, "L")
    state.newScalar("localNdata5", Ng, False, "L")
    state.newScalar("ares_heat", 1.0)
    state.newScalar("NCAT", 1, False, "L")
    state.newScalar("galaxy_bias_ref_0", False)

    state.newScalar("cosmology", cpar)
    state.newScalar("galaxy_nmean_0", 0.0)
    state.newArray1d("galaxy_bias_0", 2)
    state.newArray3d("galaxy_synthetic_sel_window_0", Ng, Ng, Ng)
    state["galaxy_bias_0"][:] = np.array([1.0, 1.0])
    state["galaxy_synthetic_sel_window_0"][:] = 1

    like = build_likelihood(state, info)

    like.initializeLikelihood(state)
    like.updateMetaParameters(state)

    s_hat = np.fft.rfftn(np.random.randn(Ng, Ng, Ng) / Ng**(1.5))
    like.generateMockData(s_hat, state)

    like.logLikelihood(s_hat)
    analytic_gradient = like.gradientLikelihood(s_hat)

    num_gradient = np.zeros((Ng, Ng, Ng // 2 + 1), dtype=np.complex128)
    s_hat_epsilon = s_hat.copy()

    epsilon = 0.001
    for i, j, k in tqdm(itertools.product(*map(range, [Ng, Ng, Ng // 2 + 1])),
                        total=Ng * Ng * (Ng // 2 + 1)):
        s_hat_epsilon[i, j, k] = s_hat[i, j, k] + epsilon
        L = like.logLikelihood(s_hat_epsilon)
        s_hat_epsilon[i, j, k] = s_hat[i, j, k] - epsilon
        L -= like.logLikelihood(s_hat_epsilon)
        QQ = L / (2.0 * epsilon)

        s_hat_epsilon[i, j, k] = s_hat[i, j, k] + 1j * epsilon
        L = like.logLikelihood(s_hat_epsilon)
        s_hat_epsilon[i, j, k] = s_hat[i, j, k] - 1j * epsilon
        L -= like.logLikelihood(s_hat_epsilon)
        QQ = QQ + L * 1j / (2.0 * epsilon)

        s_hat_epsilon[i, j, k] = s_hat[i, j, k]

        num_gradient[i, j, k] = QQ

    np.savez("gradients.npz", num=num_gradient, ana=analytic_gradient)
