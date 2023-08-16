FFT normalization in ARES/BORG
==============================

This page is to summarize the convention used for normalizing Fourier
transform, and the rational behind it.

The discrete fourier transform is defined, for a cubic box of mesh size
:math:`N` as\ 

.. math:: x_{\vec{i}} =  \mathcal{F}_{\vec{i},\vec{a}} x_{\vec{a}} = \sum_{\vec{a}} \exp\left(\frac{2\pi}{N} \vec{i}.\vec{a}\right)

In cosmology we are mostly interested in the continuous infinite Fourier
transform\ 

.. math:: \delta(\vec{x}) = \iiint \frac{\text{d}\vec{k}}{(2\pi)^3} \exp(i \vec{x}.\vec{k}) \hat{\delta}(\vec{k})\;.

It can be shown that the continuous transform, under reasonable
conditions, can be approximated and matched normalized to the following
expression in the discrete case:

:math:`\delta(\vec{x}) = \frac{1}{L^3} \sum_{\vec{k}} \exp\left(i\frac{2\pi}{L} \vec{x} .\vec{k} \right) \hat{\delta}\left(\vec{k}\frac{2\pi}{L}\right)`\ This
leads to define the following operator for the discrete Fourier
transform:

:math:`F = \frac{1}{L^3} \mathcal{F}`\ which admit the following
inverse:

:math:`F^{-1} = L^3 \mathcal{F}^{-1} = \left(\frac{L}{N}\right)^3 \mathcal{F}^\dagger`
