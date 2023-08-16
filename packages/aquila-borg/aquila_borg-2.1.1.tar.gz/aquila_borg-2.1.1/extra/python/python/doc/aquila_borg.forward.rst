@class
BORG forward model
------------------
This module includes the basic components to manipulate forward models.

.. currentmodule:: aquila_borg.forward

.. autosummary::
   :toctree: _generate

   PreferredIO
   BoxModel
   BORGForwardModel
   ParticleBasedForwardModel
   BaseForwardModel
   ChainForwardModel


@class:PreferredIO
Enumeration to specify the preferred Input/Output of a forward model


@@ ---------------------------------------------------------------------------
@class:ParticleBasedForwardModel
Special abstract class to provide an API to access to particles used in the forward computation of
certain models.


@funcname:getNumberOfParticles
Return the number of particles present on the current MPI task

@funcname:getParticlePositions
Return the positions of the particles in the provided numpy array

Arguments:
  positions (np.array): Pre-allocated numpy array `Nx3`. `N` must be at least the number returned by `ref`:getNumberOfParticles

@funcname:getParticleVelocities
Return the velocities of the particles in the provided numpy array

Arguments:
  velocities (np.array): Pre-allocated numpy array `Nx3`. `N` must be at least the number returned by `ref`:getNumberOfParticles

@funcname:setStepNotifier
Setup a callback when a new step is being computed for particles.

TODO: The C++ side has access to particles, which has not yet been done for the Python callback

Arguments:
   callback (object): A callable object. The object will be called with two arguments: the
     time and the number of particles on the current task.
