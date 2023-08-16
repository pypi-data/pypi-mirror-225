|a| is the main component of the Bayesian Large Scale Structure inference
pipeline. The present version of the ARES framework is 2.1. Please consult
:ref:`CHANGES overview` for an overview of the different improvements over the
different versions.

|a| is written in C++14 and has been parallelized with OpenMP and MPI. It currently compiles with major compilers (gcc, intel, clang).

Table of contents
-----------------

.. toctree::
   :maxdepth: 1
   :caption: Theory
   
   theory/ARES
   theory/BORG
   theory/ARES&BORG_FFT_normalization
   
.. toctree::
   :maxdepth: 1
   :caption: User documentation
   
   changes
   user/building
   user/inputs
   user/outputs
   user/running
   user/postprocessing
   user/extras
   user/clusters

.. toctree::
   :maxdepth: 1
   :caption: Developer documentation

   developer/development_with_git
   developer/code_architecture
   developer/life_cycles_of_objects
   developer/ares_modules
   developer/code_tutorials
   developer/contributing_to_this_documentation
   developer/copyright_and_authorship

Citing
^^^^^^

.. sectionauthor:: Florent Leclercq (last update: 20 June 2023)

The following section gives the references for the |ares|, |hades|, and |borg| algorithms and codes (including their direct application to real data, but excluding further scientific exploitation).
For the full list of publications from the Aquila consortium, please check the
`Aquila website <https://aquila-consortium.org/publications/>`_.

ARES
''''

References for the |ares| algorithm (linear data model, Wiener filtering with Gibbs sampling/messenger field)
are the following papers:

* J. Jasche, F. S. Kitaura, B. D. Wandelt, T. A. Enßlin, *Bayesian power-spectrum inference for large-scale structure data*,
  `Monthly Notices of the Royal Astronomical Society (2010) 406, 60 <http://dx.doi.org/10.1111/j.1365-2966.2010.16610.x>`_;
  `arXiv:0911.2493 <http://arxiv.org/pdf/0911.2493>`_
  (linear data model, Wiener filtering and power spectrum inference with Gibbs sampling)
* J. Jasche, B. D. Wandelt, *Methods for Bayesian Power Spectrum Inference with Galaxy Surveys*,
  `The Astrophysical Journal (2013) 779, 15 <http://dx.doi.org/10.1088/0004-637X/779/1/15>`_;
  `arXiv:1306.1821 <http://arxiv.org/pdf/1306.1821>`_
  (luminosity-dependent galaxy bias, calibration of noise levels, reversible jump algorithm)
* J. Jasche, G. Lavaux, *Matrix-free large-scale Bayesian inference in cosmology*,
  `Monthly Notices of the Royal Astronomical Society (2015) 447, 1204 <http://dx.doi.org/10.1093/mnras/stu2479>`_;
  `arXiv:1402.1763 <http://arxiv.org/pdf/1402.1763>`_
  (inference with messenger field)
* J. Jasche, G. Lavaux, *Bayesian power spectrum inference with foreground and target contamination treatment*,
  `Astronomy and Astrophysics (2017) 606, A37 <http://dx.doi.org/10.1051/0004-6361/201730909>`_;
  `arXiv:1706.08971 <http://arxiv.org/pdf/1706.08971>`_
  (joint inference of density field and known foregrounds)

HADES
'''''

References for the |hades| algorithm (log-normal data model, Hamiltonian Monte Carlo sampling, photometric redshift inference) are the following papers:

* J. Jasche, F. S. Kitaura, *Fast Hamiltonian sampling for large-scale structure inference*,
  `Monthly Notices of the Royal Astronomical Society (2010) 407, 29 <http://dx.doi.org/10.1111/j.1365-2966.2010.16897.x>`_;
  `arXiv:0911.2496 <http://arxiv.org/pdf/0911.2496>`_
  (HMC method paper)
* J. Jasche, F. S. Kitaura, C. Li, T. A. Enßlin, *Bayesian non-linear large-scale structure inference of the Sloan Digital
  Sky Survey Data Release 7*,
  `Monthly Notices of the Royal Astronomical Society (2010) 409, 355 <http://dx.doi.org/10.1111/j.1365-2966.2010.17313.x>`_;
  `arXiv:0911.2498 <http://arxiv.org/pdf/0911.2498>`_
  (data application with log-normal data model)
* J. Jasche, B. D. Wandelt, *Bayesian inference from photometric redshift surveys*,
  `Monthly Notices of the Royal Astronomical Society (2012) 425, 1042 <http://dx.doi.org/10.1111/j.1365-2966.2012.21423.x>`_;
  `arXiv:1106.2757 <http://arxiv.org/pdf/1106.2757>`_
  (method paper: joint inference of density and photometric redshifts)

BORG
''''

Methodological papers that shall be cited when referring to the |borg| algorithm (inference with a structure formation model and Hamiltonian Monte Carlo) are the following:

* J. Jasche, B. D. Wandelt, *Bayesian physical reconstruction of initial conditions from large-scale structure surveys*,
  `Monthly Notices of the Royal Astronomical Society (2013) 432, 894 <http://dx.doi.org/10.1093/mnras/stt449>`_;
  `arXiv:1203.3639 <http://arxiv.org/pdf/1203.3639>`_
  (original BORG method paper with differentiable LPT data model and HMC)
* J. Jasche, F. Leclercq, B. D. Wandelt, *Past and present cosmic structure in the SDSS DR7 main sample*,
  `Journal of Cosmology and Astroparticle Physics (2015) 01, 036 <http://dx.doi.org/10.1088/1475-7516/2015/01/036>`_;
  `arXiv:1409.6308 <http://arxiv.org/pdf/1409.6308>`_
  (luminosity-dependent galaxy bias, power-law bias model, calibration of noise levels)
* G. Lavaux, J. Jasche, *Unmasking the masked Universe: the 2M++ catalogue through Bayesian eyes*,
  `Monthly Notices of the Royal Astronomical Society (2016) 455, 3169 <http://dx.doi.org/10.1093/mnras/stv2499>`_;
  `arXiv:1509.05040 <http://arxiv.org/pdf/1509.05040>`_
  (data model with redshift-space distortions)
* J. Jasche, G. Lavaux, *Physical Bayesian modelling of the non-linear matter distribution: New insights into the nearby universe*,
  `Astronomy and Astrophysics (2019) 625, A64 <http://dx.doi.org/10.1051/0004-6361/201833710>`_;
  `arXiv:1806.11117 <http://arxiv.org/pdf/1806.11117>`_
  (BORGPM: particle-mesh data model, observer velocity sampling, "heating up" the likelihood)
* G. Lavaux, J. Jasche, F. Leclercq, *Systematic-free inference of the cosmic matter density field from SDSS3-BOSS data*,
  `arXiv:1909.06396 <http://arxiv.org/pdf/1909.06396>`_
  (data model with light-cone effects, quadratic form bias model)

Data application papers of |borg| are the following:

* J. Jasche, F. Leclercq, B. D. Wandelt, *Past and present cosmic structure in the SDSS DR7 main sample*,
  `Journal of Cosmology and Astroparticle Physics (2015) 01, 036 <http://dx.doi.org/10.1088/1475-7516/2015/01/036>`_;
  `arXiv:1409.6308 <http://arxiv.org/pdf/1409.6308>`_
  (application to SDSS DR7 main galaxy sample)
* G. Lavaux, J. Jasche, *Unmasking the masked Universe: the 2M++ catalogue through Bayesian eyes*,
  `Monthly Notices of the Royal Astronomical Society (2016) 455, 3169 <http://dx.doi.org/10.1093/mnras/stv2499>`_;
  `arXiv:1509.05040 <http://arxiv.org/pdf/1509.05040>`_
  (application to 2M++, LPT data model)
* J. Jasche, G. Lavaux, *Physical Bayesian modelling of the non-linear matter distribution: New insights into the nearby universe*,
  `Astronomy and Astrophysics (2019) 625, A64 <http://dx.doi.org/10.1051/0004-6361/201833710>`_;
  `arXiv:1806.11117 <http://arxiv.org/pdf/1806.11117>`_
  (application to 2M++, PM data model)
* G. Lavaux, J. Jasche, F. Leclercq, *Systematic-free inference of the cosmic matter density field from SDSS3-BOSS data*,
  `arXiv:1909.06396 <http://arxiv.org/pdf/1909.06396>`_
  (application to SDSS3 BOSS, LPT data model)

Additional papers extend the |borg| algorithm and shall be cited depending on the context. The list includes (but may not be limited to):

* Foregrounds/Systematic effects:

  * J. Jasche, G. Lavaux, *Bayesian power spectrum inference with foreground and target contamination treatment*,
    `Astronomy and Astrophysics (2017) 606, A37 <http://dx.doi.org/10.1051/0004-6361/201730909>`_;
    `arXiv:1706.08971 <http://arxiv.org/pdf/1706.08971>`_
    (joint inference of density field and known foregrounds)
  * N. Porqueres, D. Kodi Ramanah, J. Jasche, G. Lavaux, *Explicit Bayesian treatment of unknown foreground contaminations
    in galaxy surveys*,
    `Astronomy and Astrophysics (2019) 624, A115 <http://dx.doi.org/10.1051/0004-6361/201834844>`_;
    `arXiv:1812.05113 <http://arxiv.org/pdf/1812.05113>`_
    (robust likelihood for unknown foregrounds effects)

* Cosmic expansion model (Alcock-Paczynski effect):

  * D. Kodi Ramanah, G. Lavaux, J. Jasche, B. Wandelt, *Cosmological inference from Bayesian forward modelling
    of deep galaxy redshift surveys*,
    `Astronomy and Astrophysics (2019) 621, A69 <http://dx.doi.org/10.1051/0004-6361/201834117>`_;
    `arXiv:1808.07496 <http://arxiv.org/pdf/1808.07496>`_
    (Alcock-Paczynski expansion test)

* Lyman-α forest:

  * N. Porqueres, J. Jasche, G. Lavaux, T. Enßlin, *Inferring high-redshift large-scale structure dynamics from the Lyman-α forest*,
    `Astronomy and Astrophysics (2019) 630, A151 <http://dx.doi.org/10.1051/0004-6361/201936245>`_;
    `arXiv:1907.02973 <http://arxiv.org/pdf/1907.02973>`_ (Lyman alpha data model)
  * N. Porqueres, O. Hahn, J. Jasche, G. Lavaux, *A hierarchical field-level inference approach to reconstruction from
    sparse Lyman-α forest data*,
    `Astronomy and Astrophysics (2020) 642, A139 <http://dx.doi.org/10.1051/0004-6361/202038482>`_;
    `arXiv:2005.12928 <http://arxiv.org/pdf/2005.12928>`_

* Weak lensing (cosmic shear):

  * N. Porqueres, A. Heavens, D. Mortlock, G. Lavaux, *Bayesian forward modelling of cosmic shear data*,
    `Monthly Notices of the Royal Astronomical Society (2021) 502, 3035 <http://dx.doi.org/10.1093/mnras/stab204>`_;
    `arXiv:2011.07722 <http://arxiv.org/pdf/2011.07722>`_
    (original BORG-WL paper)
  * N. Porqueres, A. Heavens, D. Mortlock, G. Lavaux, *Lifting weak lensing degeneracies with a field-based likelihood*,
    `Monthly Notices of the Royal Astronomical Society (2022) 509, 3194 <http://dx.doi.org/10.1093/mnras/stab3234>`_;
    `arXiv:2108.04825 <http://arxiv.org/pdf/2108.04825>`_
    (cosmological parameter inference)
  * N. Porqueres, A. Heavens, D. Mortlock, G. Lavaux, T. L. Makinen, *Field-level inference of cosmic shear with intrinsic
    alignments and baryons*,
    `arXiv:2304.04785 <http://arxiv.org/pdf/2304.04785>`_
    (intrinsic alignments and baryons)

* Cosmic velocity field:

  * S. S. Boruah, G. Lavaux, M. J. Hudson, *Bayesian reconstruction of dark matter distribution from peculiar velocities:
    accounting for inhomogeneous Malmquist bias*,
    `Monthly Notices of the Royal Astronomical Society (2022) 517, 4529 <http://dx.doi.org/10.1093/mnras/stac2985>`_;
    `arXiv:2111.15535 <http://arxiv.org/pdf/2111.15535>`_
    (linear model for the velocity field, inhomogeneous Malmquist bias, observational effects)
  * J. Prideaux-Ghee, F. Leclercq, G. Lavaux, A. Heavens, J. Jasche, *Field-Based Physical Inference From Peculiar Velocity Tracers*,
    `Monthly Notices of the Royal Astronomical Society (2023) 518, 4191 <http://dx.doi.org/10.1093/mnras/stac3346>`_;
    `arXiv:2204.00023 <http://arxiv.org/pdf/2204.00023>`_
    (LPT structure formation model in the data model)

* Primordial non-Gaussianity:

  * A. Andrews, J. Jasche, G. Lavaux, F. Schmidt, *Bayesian field-level inference of primordial
    non-Gaussianity using next-generation galaxy surveys*,
    `Monthly Notices of the Royal Astronomical Society (2023) 520, 5746 <http://dx.doi.org/10.1093/mnras/stad432>`_;
    `arXiv:2203.08838 <http://arxiv.org/pdf/2203.08838>`_ (local fNL sampling)

* Photometric redshift inference:

  * E. Tsaprazi, J. Jasche, G. Lavaux, F. Leclercq, *Higher-order statistics of the large-scale structure from photometric redshifts*,
    `arXiv:2301.03581 <http://arxiv.org/pdf/2301.03581>`_
    (photometric redshift sampling with a structure formation model)

* Effective Field Theory (EFT) bias model and likelihood:

  * F. Schmidt, F. Elsner, J. Jasche, N. M. Nguyen, G. Lavaux, *A rigorous EFT-based forward model for large-scale structure*,
    `Journal of Cosmology and Astroparticle Physics (2019) 01, 042 <http://dx.doi.org/10.1088/1475-7516/2019/01/042>`_;
    `arXiv:1808.02002 <http://arxiv.org/pdf/1808.02002>`_ (EFT likelihood)
  * F. Schmidt, G. Cabass, J. Jasche, G. Lavaux, *Unbiased cosmology inference from biased tracers using the EFT likelihood*,
    `Journal of Cosmology and Astroparticle Physics (2020) 11, 008 <http://dx.doi.org/10.1088/1475-7516/2020/11/008>`_;
    `arXiv:2004.06707 <http://arxiv.org/pdf/2004.06707>`_ (biased tracers with EFT bias model and likelihood)

Acknowledgements
----------------


This work has been funded by the following grants and institutions over the
years:

* The DFG cluster of excellence "Origin and Structure of the Universe"
  (http://www.universe-cluster.de).
* Institut Lagrange de Paris (grant ANR-10-LABX-63, http://ilp.upmc.fr) within 
  the context of the Idex SUPER subsidized by the French government through
  the Agence Nationale de la Recherche (ANR-11-IDEX-0004-02).
* BIG4 (ANR-16-CE23-0002) (https://big4.iap.fr)
* The "Programme National de Cosmologie et Galaxies" (PNCG, CNRS/INSU)
* Through the grant code ORIGIN, it has received support from
  the "Domaine d'Interet Majeur (DIM) Astrophysique et Conditions d'Apparitions
  de la Vie (ACAV)" from Ile-de-France region.
* The Starting Grant (ERC-2015-STG 678652) "GrInflaGal" of the European Research Council.



.. Indices and tables
.. ==================
.. 
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

..  Order of headings used throughout the documentation:
    
    ######### part
    ********* chapter
    ========= sections
    --------- subsections
    ~~~~~~~~~ subsubsections
    ^^^^^^^^^
    '''''''''

.. toctree-filt::
   :maxdepth: 1
   :caption: Python reference documentation

   :aquila:pythonref.rst
