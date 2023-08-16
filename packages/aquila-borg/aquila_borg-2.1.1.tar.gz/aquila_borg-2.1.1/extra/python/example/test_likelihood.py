import numpy as np
import borg

cons = borg.console()

myprint = lambda x: cons.print_std(x) if type(x) == str else cons.print_std(
    repr(x))

sigma_noise = 0.1


class MyLikelihood(borg.likelihood.BaseLikelihood):
    def __init__(self, fwd, N, L):
        myprint(f" Init {N}, {L}")
        super().__init__(fwd, N, L)
        self.comm = fwd.getCommunicator()

    def initializeLikelihood(self, state):
        myprint("Init likelihood")
        self.data = state['galaxy_data_0']
        state.newArray3d("my_density_field", self.data.shape[0],
                         self.data.shape[1], self.data.shape[2], True)

    def updateMetaParameters(self, state):
        cpar = state['cosmology']
        myprint(f"Cosmology is {cpar}")
        self.getForwardModel().setCosmoParams(cpar)

    def generateMockData(self, s_hat, state):

        fwd = self.getForwardModel()
        output = np.zeros(fwd.getOutputBoxModel().N)
        fwd.forwardModel_v2(s_hat)
        fwd.getDensityFinal(output)

        state['galaxy_data_0'][:] = output + np.random.normal(
            size=output.shape) * sigma_noise
        state['my_density_field'][:] = output
        like = ((state['galaxy_data_0'][:] - output)**2).sum() / sigma_noise**2
        myprint(
            f"Initial log_likelihood: {like}, var(s_hat) = {np.var(s_hat)}")

    def logLikelihoodComplex(self, s_hat, gradientIsNext):
        fwd = self.getForwardModel()

        output = np.zeros(fwd.getBoxModel().N)
        fwd.forwardModel_v2(s_hat)
        fwd.getDensityFinal(output)
        L = 0.5 * ((output - self.data)**2).sum() / sigma_noise**2
        myprint(f"var(s_hat): {np.var(s_hat)}, Call to logLike: {L}")
        return self.comm.allreduce(L)

    def gradientLikelihoodComplex(self, x_hat):
        fwd = self.getForwardModel()
        output = np.zeros(fwd.getOutputBoxModel().N)
        fwd.forwardModel_v2(x_hat)
        fwd.getDensityFinal(output)
        mygradient = (output - self.data) / sigma_noise**2
        fwd.adjointModel_v2(mygradient)
        mygrad_hat = np.zeros(s_hat.shape, dtype=np.complex128)
        fwd.getAdjointModel(mygrad_hat)
        return mygrad_hat


model = None


@borg.registerGravityBuilder
def build_gravity_model(state, box):
    global model
    chain = borg.forward.ChainForwardModel(box)
    chain.addModel(borg.forward.models.HermiticEnforcer(box))
    chain.addModel(borg.forward.models.Primordial(box, 1.0))
    chain.addModel(borg.forward.models.EisensteinHu(box))
    model = chain
    return chain


@borg.registerLikelihoodBuilder
def build_likelihood(state, info):
    boxm = model.getBoxModel()
    like = MyLikelihood(model, boxm.N, boxm.L)
    #like.initializeLikelihood(state)
    return like


@borg.registerSamplerBuilder
def build_samplers(state, info):
    return []
