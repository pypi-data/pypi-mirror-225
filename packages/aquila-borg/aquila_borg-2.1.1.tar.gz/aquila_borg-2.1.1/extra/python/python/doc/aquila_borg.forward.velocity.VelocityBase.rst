@class
This is the base class for models that compute velocity field from a forward
model output.

This class is abstract and not constructible. The construction of a velocity field
requires that the base formward model has been executed using
`aquila_borg.forward.models.BORGForwardModel.forwardModel_v2`.

@@ -------------------------------------------------------------------------
@funcname:getOutputBox
Return the `aquila_borg.forward.BoxModel` corresponding to the output of this velocity
field model.

@@ -------------------------------------------------------------------------
@funcname:computeAdjointModel
Push the adjoint gradient of the velocity field in the model.

Depending on the specific model used, the produced adjoint gradient is pushed to
the forward model that produced the simulation (e.g.
`aquila_borg.forward.model.BorgLpt`).

Args:
    ag (numpy.array): The adjoint gradient with respect to the output of the
          velocity model. The adjoint gradient must have a shape 3xN0xN1xN2, where N0
          may be MPI-sliced. If the adjoint is not densely packed and double
          precision, it will be implicitly force cast to the adequate requirement
          (i.e. it may need more memory).

@@ -------------------------------------------------------------------------
@funcname:getVelocityField
Compute and returns the velocity field associated to the base forward model.

Returns:
    numpy.array: a 3xN0xN1xN2 velocity field on grid.
