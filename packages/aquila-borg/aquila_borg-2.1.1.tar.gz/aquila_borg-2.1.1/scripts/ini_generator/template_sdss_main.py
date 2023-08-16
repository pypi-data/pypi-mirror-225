#+
#   ARES/HADES/BORG Package -- ./scripts/ini_generator/template_sdss_main.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
CONFIG=dict(
  absmag_min=-23.,absmag_max = -17.,
  num_subcat=6,catalog='sdss_ares_cat.txt',
  mask='SDSSDR7MASK_4096.fits', ref_subcat=0,
  cutter='magnitude'
  )

radial_selection = 'schechter'
schechter_mstar = -20.44
schechter_alpha = -1.05
schechter_sampling_rate = 2000
schechter_dmax = 1000
bias = 1
nmean = 1
galaxy_bright_apparent_magnitude_cut = 13.5
galaxy_faint_apparent_magnitude_cut = 17.6
