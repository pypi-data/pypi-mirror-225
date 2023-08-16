.. _introduction_to_borg:

Introduction to BORG
====================

The BORG3 (Bayesian Origin Reconstruction from Galaxies) model is a
submodule of the ARES3 framework. It shares the same infrastructure ,
I/O system and general mechanism. BORG3 relies also on HADES3 package
which implements an efficient Hamiltonian Markov Chain sampler of the
density field at fixed power spectrum and fixed selection effects.

More specifically, BORG3 implements the forward and adjoint gradient
model for different dynamical model: Lagrangian perturbation theory,
Second order Lagrangian perturbation theory, Linearly Evolving Potential
and full Particle Mesh. On top of that redshift space distortions are
supported by adding a translation to intermediate particle
representations.

On top of that BORG3 provides different likelihood model to relate the
matter density field to the galaxy density field: Gaussian white noise,
Poisson noise (with non-linear truncated power-law bias model), Negative
binomial likelihood.

Finally BORG3 fully supports MPI with scaling at least up to 1024 cores.
