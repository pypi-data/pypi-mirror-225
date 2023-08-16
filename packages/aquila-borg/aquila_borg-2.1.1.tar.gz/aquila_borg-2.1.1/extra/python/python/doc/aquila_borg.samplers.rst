@class
Samplers and sampler algorithms
-------------------------------
This module includes the basic components to generate new samplers in a block sampling
strategy.

.. currentmodule:: aquila_borg.samplers

.. autosummary::
    :toctree: _generate

    MarkovSampler
    PyBaseSampler
    slice_sampler
    GenericBiasSampler
    BiasModelParamsSampler
    HMCDensitySampler
    ModelParamsSampler
    Sigma8Sampler
    AltairMetaSampler

@@ ------------------------------------------------
@funcname:slice_sampler
Basic slice_sampler implementation.

This implements a slice sampler without rescaling of the stepper.

Args:
    state (MarkovState):  A markov state with an initialized random number generation
    callback (callable):  A callable object, typically a lambda function or a function with one argument
    previous_value (float): Previous value of the slice sampler chain
    step (float):         Step to progress through the posterior

Returns:
    float: new position

@@ ------------------------------------------------
@class:PyBaseSampler
PyBaseSampler class to implement MarkovSampler object from python.

The constructor must call super().__init__() to ensure the native part of the object
is well initialized.

Note that three functions must be implemented:
  * initialize(state: MarkovState)
  * restore(state: MarkovState)
  * sample(state: MarkovState)

The first two are hidden from the MarkovSampler interface as being protected in
the native interface.

@@ ------------------------------------------------
@class:GenericBiasSampler
This is a sampler that will run a slice sampler for each bias parameter of catalog.
It basically adapts the standard behavior of hades3 for the python environment.

Arguments:
    model (Likelihood3d): A likelihood model to sample the bias parameter from.


@@ ------------------------------------------------
@class:BiasModelParamsSampler
A sampler that sample bias parameters using the borg forward model strategy.

It relies on block sampling and slice sampler approach to be able to do it on anything,
though it is expected to be slow in the end.

The sampler will update the bias parameters using the mechanism of :meth:`aquila_borg.forward.BORGForwardModel.setModelParams`.
It is provided with an update on the key "biasParameters" which is a 1d array of the size as provided
to the constructor.

The array is initialized by introspection by querying :meth:`aquila_borg.forward.BORGForwardModel.getModelParam` on the model
with the nickname "bias" and the parameter "biasParameters". On restart, those parameters will be reset
correctly.

:Example:

For example the following python model would be interrogated by this sampler:

.. code-block:: python

   class Model(aquila_borg.forward.BORGForwardModel):
     # skip common section
     def setModelParams(self, params):
       if 'biasParameters' in params:
         print(" I am getting some parameters: "  + repr(params))

     def getModelParam(self, modelname, keyname):
       if modelname == 'bias' and keyname == 'biasParameters':
         print(" Let's return some numpy array with parameters" )
         return np.array([0.0,1.0])  #This array must match the number of parameters

Arguments:
   likelihood (Likelihood3d): the likelihood to evaluate the quality of the parameter
   model (BORGForwardModel): the forward model element to pass the bias parameter upon
   prefix (str): Prefix for the bias parameter array
   limiter (callable): Function to be called before trying to sample the bias parameters
   unlimited (callable): Function to be called after a new sample of the bias parameters

@@ ------------------------------------------------
@class:HMCDensitySampler
Build a new HMC based density sampler.

Arguments:
   likelihood (Likelihood3d): A 3d likelihood object. This is the present restriction of the HMC.

Keyword arguments:
   prefix (str): add a prefix to HMC variables. This is useful in case several HMC are running at the same
       time to solve the problem.
   k_max (float): Only sample the modes up to the provided k_max. The others are frozen.

@@ ------------------------------------------------
@class:Sigma8Sampler
Build a new sigma8 sampler.

It supports three arguments in the `info` object:
  * `sigma8_min`: min bound of the prior
  * `sigma8_max`: max bound of the prior
  * `sigma8_step`: typical step to execute the slice sampler

Arguments:
   likelihood (Likelihood3d): A 3d likelihood object.
   info (LikelihoodInfo): A LikelihoodInfo dictionnary object.

@@ ------------------------------------------------
@class:ModelParamsSampler
Build a new model params sampler.

Arguments:
   prefix (str):
   params (list of str):
   likelihood (Likelihood3d):
   model (BORGForwardModel):
   init (dict):


@@ ------------------------------------------------
@class:AltairMetaSampler
Build a new sampler for altair

Arguments:
  likelihood (ForwardModelLikelihood3d): A likelihood based on a forward model (required to update it)
