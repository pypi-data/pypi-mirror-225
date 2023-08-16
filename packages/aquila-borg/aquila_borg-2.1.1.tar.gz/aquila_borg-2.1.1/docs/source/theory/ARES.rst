.. _introduction_to_bayesian_large_scale_structure_inference:

Introduction to ARES
====================

The Algorithm for REconstruction and Sampling (ARES) is a full Bayesian
large scale structure inference method targeted at precision recovery of
cosmological power-spectra from three dimensional galaxy redshift
surveys. Specifically it performs joint inferences of three dimensional
density fields, cosmological power spectra as well as luminosity
dependent galaxy biases and corresponding noise levels for different
galaxy populations in the survey.

In order to provide full Bayesian uncertainty quantification the
algorithm explores the joint posterior distribution of all these
quantities via an efficient implementation of high dimensional Markov
Chain Monte Carlo methods in a block sampling scheme. In particular the
sampling consists in generating from a Wiener posterior distribution
random realizations of three dimensional density fields constrained by
data in the form of galaxy number counts. Following each generation, we
produce conditioned random realizations of the power-spectrum, galaxy
biases and noise levels through several sampling steps. Iterating these
sampling steps correctly yields random realizations from the joint
posterior distribution. In this fashion the ARES algorithm accounts for
all joint and correlated uncertainties between all inferred quantities
and allows for accurate inferences from galaxy surveys with non-trivial
survey geometries. Classes of galaxies with different biases are treated
as separate sub samples, allowing even for combined analyses of more
than one galaxy survey.

For further information please consult our publications that are listed
`here <https://www.aquila-consortium.org/publications/>`__.

.. _implementation_the_ares3_code:

Implementation: the ARES3 code
------------------------------

The ARES3 package comes with a basic flavour within the binary program
"ares3". "ares3" is an implementation of the algorithm outlined in the
paper "Matrix free Large scale Bayesian inference" (Jasche & Lavaux
2014)

The ARES3 serves as a basis for number of extensions and modules. The
minimal extension is the foreground sampler mechanism, that allows to
fit some model of foreground contamination in large scale structure
data. The second main module is the *HADES* sampler, which
incorporates the HMC base definition and implementation alongside some
likelihood models. The third module is the :ref:`BORG <introduction_to_borg>` sampler. It
is a much more advanced likelihood analysis which incorporates
non-linear dynnamics of the Large scale structures.

.. _ares_model:

ARES model
----------

The model implemented in ARES is the most simple 'linear' model. The
density field is supposed to be a pure Gaussian random field, which
linearly biased, selected and with a Gaussian error model. For a single
catalog, the forward model corresponds to:

:math:`N^\mathrm{g}_p = \bar{N} R_p (1 + b \delta_p) + n_p` with
:math:`\langle n_p n_{p'} \rangle = R_p \bar{N} \delta^K_{p, p'}`

:math:`\delta^K` is the Kronecker symbol, :math:`R_p` is the linear
response of the survey, i.e. the 3d completeness, :math:`b` the linear
bias and :math:`\bar{N}` the mean number of galaxies per grid element.
Effectively :math:`\bar{N}` will absorb the details of the normalization
of :math:`R_p`.
