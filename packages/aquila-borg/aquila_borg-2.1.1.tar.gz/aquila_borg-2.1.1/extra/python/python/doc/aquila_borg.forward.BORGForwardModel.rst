@class

Base class for all forward models.

All forward models derive from this class. However python implemented forward
models must use :obj:`.BaseForwardModel`.

:members:


@funcname:__init__

@funcname:getPreferredOutput
Returns the preferred output format (i.e. the one that incurs less transforms)
for that model.

Returns:
    PreferredIO: the preferred format

@funcname:getPreferredInput


@funcname:setCosmoParams
Setup the cosmological parameters that this model requires.

Args:
    cosmo_params (:obj:`aquila_borg.cosmo.CosmologicalParameters`): Cosmological parameters

@funcname:getModelParam
This queries the current state of the parameters 'keyname' in model 'model'.

Args:
  model (str): sub model name keyname (str): key of the parameter to query

Returns:
  object: the value of the parameter

@@ ---------------------------------------------

@funcname:setName
Give a to localize more easily a model instance.

Args:
  name (str): string name of the instance

@funcname:setModelParams
Allow changing model parameters for different model indexed by the dictionnary key,
each item is another dictionnary with key/value pairs.

@@ ---------------------------------------------

@funcname:getOutputBoxModel
Return the box on which is defined the output of the model is defined.

Returns:
  BoxModel: the box model representing the shape and size of the output of that
  forward model.

@@ ---------------------------------------------
@funcname:adjointModel_v2
Pushes the adjoint gradient from a deeper part of the computation.

This function allows to push the adjoint gradient vector for a deeper part of
the computation (like the likelihood) to the forward model. It will not return
the result which has to be query with :func:`~BORGForwardModel.getAdjointModel`.

Args:
    adjoint_gradient (numpy.array): A 3d numpy array either real or complex. If
    complex it must use the RFFT half-complex representation

Returns:
    None

@@ ---------------------------------------------
@funcname:forwardModel_v2
Run the first part of the forward model (v2 API).

Args:
  input_array (numpy.array): A 3d numpy array either real or complex. If
    complex it must use the RFFT half-complex representation

Returns:
  None

@@ ---------------------------------------------
@funcname:setAdjointRequired
Indicate whether the caller require the adjoint gradient to be computed later.

Args:
  flag (bool): if True, tape is recorded to compute adjoint



@@ ---------------------------------------------
@funcname:clearAdjointGradient
Clear accumulated information to compute the adjoint gradient vector.

This is automaticalled by getAdjointModelOutput.

@@ ---------------------------------------------
@funcname:getMPISlice
Returns a tuple of integer indicating the way the slab is distributed among
the node.

Returns:
   tuple of int: (startN0, localN0, N1, N2)

@@ ---------------------------------------------
@funcname:getCommunicator
Build and return an MPI4PY communicator object that is linked to the internal
MPI communicator of that object.

Returns:
   mpi4py.MPI.Comm


@@ ---------------------------------------------
@funcname:accumulateAdjoint
Request the model to accumulate adjoint vectors instead of resetting at each call.

This changes the default behavior of adjointModel_v2. Use with care.

Args:
  do_accumulate (bool): If true, request the change of behavior.
