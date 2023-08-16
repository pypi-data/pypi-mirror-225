@class
Velocity field computations
---------------------------
This module includes the components to compute velocity field from result
of forward models.

.. currentmodule:: aquila_borg.forward.velocity

.. autosummary::
    :toctree: _generate

    VelocityBase
    ParticleBasedModel
    CICModel
    SICModel

@funcname:getVelocityField
Compute and returns the velocity field from the forward model.


@class:ParticleBasedModel
ParticleBasedModel is the base class for the computation of velocity field
from forward model that are particle based (such as `aquila_borg.forward.models.BorgLpt`
or `aquila_borg.forward.models.BorgPm`).

@class:CICModel
This class implements the Cloud-In-Cell (CIC) model for velocity field computation.

The momentum field is computed by projecting each particle velocities onto a
grid using a CIC kernel. Then the mass field is computed in the same way uses
as divisor of the momentum field.

@class:SICModel
This class implements Simplex-In-Cell (SIC) model for the velocity field computation.

@funcname:__init__
Construct a new SIC forward model element. It relies on the output of the
provided BORG forward model element, which must be particle based.
