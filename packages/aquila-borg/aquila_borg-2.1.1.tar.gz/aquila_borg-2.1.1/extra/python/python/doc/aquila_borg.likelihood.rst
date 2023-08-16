@class
Likelihood and associated structures
------------------------------------

This module includes the basic components to use BORG likelihoods and develop new likelihoods to mesh with the existing framework.

.. currentmodule:: aquila_borg.likelihood

.. autosummary::
    :toctree: _generate

    MarkovState
    Likelihood3d
    ForwardModelLikelihood3d
    BaseLikelihood
    LikelihoodInfo
    GaussianPassthrough
    GaussianLinear
    PoissonPowerLaw



@@ ---------------------------------------------------------------------------
@class:MarkovState
Create a new MCMC dictionnary.


@@ ---------------------------------------------------------------------------
@funcname:newArray1d
Create and allocate a new 1d array in the dictionnary.

The 1d array holds value in double precision.

Arguments:
  name (:obj:`str`):
  N (int):

Keyword arguments:
  in_mcmc (bool): Default to false.

Raises:
  KeyError: if `name` is already present in the MarkovState

@@ ---------------------------------------------------------------------------
@funcname:newArray3d
Create and allocate a new 3d array in the dictionnary.

The 3d array holds value in double precision.

Arguments:
  name (:obj:`str`): Requested `name` of the array
  N0 (int): First dimension
  N1 (int): Second dimension
  N2 (int): Third dimension

Keyword arguments:
  in_mcmc (bool): Default to false.

Raises:
  KeyError: if `name` is already present in the MarkovState

@@ ---------------------------------------------------------------------------
@funcname:newArray3d_slab
Create and allocate a new 3d array, with MPI slabbing, in the dictionnary.

The 3d array holds value in double precision.

Arguments:
  name (:obj:`str`): Requested `name` of the array
  slab (tuple of 6 int): Slab position and size (start0,local_size0,start1,local_size1,start2,local_size2)
  real_size (tuple of 3 int): Real size

Keyword arguments:
  in_mcmc (bool): Default to false.

Raises:
  KeyError: if `name` is already present in the MarkovState

@@ ---------------------------------------------------------------------------
@funcname:newForwardModel
Create a new entry to hold a forward model in the MarkovState.

The forward model is not saved to disk. This entry is used for legacy that requires
to store a forward model in the MarkovState.


Arguments:
  name (str): Name of the entry
  forward (BORGForwardModel): A forward model object

@@ ---------------------------------------------------------------------------
@class:Likelihood3d
Base class to represent 3d likelihoods in BORG.

The likelihoods are 3d as they manipulate 3d meshes. This object is abstract and cannot
be directly inherited in Python. Please use :obj:`.BaseLikelihood` to create new likelihood
in Python.

@@ ---------------------------------------------------------------------------
@class:ForwardModelLikelihood3d

@funcname:getForwardModel

@class:BaseLikelihood

@class:GaussianPassthrough

@class:GaussianLinear

@class:PoissonPowerLaw

@class:PoissonPassthrough

@class:LikelihoodInfo
