@class

Standard BORG forward models
----------------------------

This module includes direct access to a number of fundamental forward models.

.. currentmodule:: aquila_borg.forward.models

.. autosummary::
    :toctree: _generate

    HermiticEnforcer
    Primordial
    EisensteinHu
    Downgrade
    Transfer
    HadesLinear
    HadesLog
    BorgLpt
    BorgLptOpenMP
    BorgLptNGP_Double
    BorgLptNGP_Quad
    BorgLptSmoothNGP_Quad
    Borg2Lpt
    BorgPM
    newModel
    listModels


@funcname:newModel
Builds a new forward model object from its named.

This is a very generic tool to build any forward model built in the borg library.
Being generic means there are some limitations. It relies on the arguments
available to the INI configuration file to build those models.

Args:

  name (str):  name of the model
  box (aquila_borg.forward.BoxModel):   Input box for the model
  arguments (dict):  A key-value pair dictionary. Its context matches the INI file specification

Returns:

  aquila_borg.forward.BORGForwardModel:  a constructed forward model element

@funcname:listModels
List the available forward models using their internal name.

Returns:

  list of str: a list of name


@@ ----------------------------------------------------------
@class:BorgPM
Construct a new BorgPM object.

Arguments:
  box (aquila_borg.forward.BoxModel): Box specification of the initial conditions.
  box_out (aquila_borg.forward.BoxModel): Output box specification for the final conditions.

Keyword arguments:
  supersampling (int): Indicate by how much to supersample the initial conditions with particles.
  force_factor (int): Indicate the relative resolution for the computation of the gravitational field.
  particle_factor (float): Sets the over-allocation of the particle array on the current task for MPI load balancing
  rsd (bool): Add redshift space distortion by displacing particles using their velocities.
  ai (float): Scale factor of the initial conditions provided by the previous step.
  af (float): Requested scale factor for the output
  z_start (float): Redshift at which to switch between LPT and the full particle mesh integration.
  tCOLA (bool): Indicate whether to use tCOLA for the integration.

@@ ----------------------------------------------------------
@class:BorgLpt
This class binds the borg LPT forward model (CIC mass assignment).

Arguments:
  box (BoxModel): Input box comoving size

Keyword arguments:
  box_out (BoxModel): Output box (default is equal to input).
  rsd (bool): inject redshift space distortions, default false.
  supersampling (int): supersampling factor, i.e. by multiplicative factor, for each side, between particle array and input array [default 1].
  particle_factor (float): allocation ratio of the particle arrays (must be > 1) [default 1.1]
  ai (float): scale factor used for the input density field (default 0.1)
  af (float): scale factor requested for the output (default 1.0)
  lightcone (bool): if true, add lightcone effect at order 0, (default false)
  lightcone_boost (float): make the structures goes quicker, useful for art drawing of lightcones (default 1.0)

@@ ----------------------------------------------------------
@class:BorgLptOpenMP
This class binds the borg LPT forward model (CIC/OpenMP mass assignment).

@@ ----------------------------------------------------------
@class:BorgLptNGP_Double
This class binds the borg LPT forward model (NGP double mass assignment).

@@ ----------------------------------------------------------
@class:BorgLptNGP_Quad
This class binds the borg LPT forward model (NGP quad mass assignment).

@@ ----------------------------------------------------------
@class:BorgLptSmoothNGP_Quad
This class binds the borg LPT forward model (Smooth NGP quad mass assignment).

@@ ----------------------------------------------------------
@class:Borg2Lpt

Arguments:
  box (BoxModel): BORG 3d box descriptor of the input
  box_out (BoxMOdel):  BORG 3d box descriptor of the output

Keyword arguments:
  rsd (bool): Apply redshift distortion at particle level Default to False
  supersampling (float): Number of times to supersample the initial condition
    before generating Lagrangian particles. (default 1)
  particle_factor (float): *For MPI purpose*, memory overallocation per task of the particle arrays (default 1.1)
  ai (float): Input scale factor (default 0.1)
  af (float): Output scale factor (default 1.0)
  lightcone (bool): Whether to generate particle on lightcone at zero order (default False)

@@ ----------------------------------------------------------
@class:Transfer

Forward model to apply a transfer function (not necessarily isotropic) to the input field

@funcname:setupSharpKcut

@funcname:setupInverseCIC

@funcname:setTransfer

@@ ----------------------------------------------------------
@class:HermiticEnforcer

Enforce the hermiticity of the input complex field. If real space data is provided
the adjoint gradient is not guaranteed to be adequate, as it supposes that there are more
degree of freedom in the complex plane.

Arguments:
  box (BoxModel): BORG 3d box descriptor


@@ ----------------------------------------------------------
@class:HadesLog

Applies an exponential transform to the real space field. By default it enforces to conserve the mean.

Arguments:
  box (BoxModel): BORG 3d box descriptor
  ai (float): Input scale factor

@@ ----------------------------------------------------------
@class:HadesLinear

Do nothing but Eulerian linear perturbation scaling

Arguments:
  box (BoxModel): BORG 3d box descriptor
  ai (float): Input scale factor
  af (float): Output scale factor
