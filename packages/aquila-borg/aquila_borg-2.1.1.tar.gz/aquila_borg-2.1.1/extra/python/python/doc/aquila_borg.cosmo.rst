@class
Cosmology computations
----------------------
This module includes the basic components to describe and to do
cosmological computations.

.. currentmodule:: aquila_borg.cosmo

.. autosummary::
   :toctree: _generate

   CosmologicalParameters
   Cosmology
   CosmoPower
   ClassCosmo


@@ ---------------------------------------------------------------------------
@class:CosmologicalParameters
Class that holds the values of all cosmological parameters relevant to the BORG framework.

The constructor setup a sane default LCDM cosmology.

@funcname:default
Reset parameters to default cosmology

@funcname:omega_r
:math:`\Omega_r` cosmological parameter (i.e. redshift 0 normalized radiation density)


@funcname:omega_k
:math:`\Omega_k` cosmological parameter (i.e. redshift 0 normalized curvature)

@funcname:omega_m
:math:`\Omega_m` cosmological parameter (i.e. redshift 0 matter density)

@funcname:omega_b
:math:`\Omega_b` cosmological parameter (i.e. redshift 0 baryon density)

@funcname:omega_q
:math:`\Omega_q` cosmological parameter (i.e. redshift 0 quintescence/dark energy density). Requires extra parameter :math:`w` and :math:`w'`.

@funcname:w
:math:`w` cosmological parameter (i.e. redshift 0 equation of state of quintescence/dark energy).

@funcname:wprime
:math:`w'` cosmological parameter (i.e. redshift 0 time derivative at $a=0$ of the equation of state of quintescence/dark energy).

@funcname:n_s
:math:`n_s` cosmological parameter (i.e. redshift 0, power law index of primordial fluctuations).

@funcname:fnl
:math:`f_\mathrm{NL}`, quadratic type non-gaussianity

@funcname:h
Hubble constant normalized to :math:`100 \mathrm{km s Mpc}^{-1}`.

@funcname:sum_mnu
:math:`\sum m_\nu`, sum of mass of neutrinos in eV

@@ ---------------------------------------------------------------------------
@class:Cosmology
Class to compute different quantities for an homogeneous universe and given cosmological parameters

Arguments:
  cosmo_params (CosmologicalParameters): Cosmological parameters to use
      to construct the `Cosmology` object

@@ ---------------------------------------------------------------------------
@class:CosmoPower
Construct a new CosmoPower object from the given cosmological parameters.

Arguments:
  cosmo_params (CosmologicalParameters): Cosmological parameters to use
      to construct the `Cosmology` object

@@ ---------------------------------------------------------------------------
@class:ClassCosmo
Builds a new object ClassCosmo. It relies on the embedded CLASS (https://class-code.net)
to compute the primordial gravitational potential and/or density fluctuations.

Arguments:
  params (CosmologicalParameters): The cosmological parameters to use to precompute the
       transfer function

@funcname:get_Tk

Arguments:
   k (numpy,float,array): Mode where to compute the transfer function at (in h/Mpc)

Returns:
   numpy array of the transfer function at each k

Throws:
   RuntimeError if beyond range of validity

@funcname:getCosmology

Returns:
  dict of string/double pairs, corresponding to each cosmological parameters.
