#+
#   ARES/HADES/BORG Package -- ./extra/hades/libLSS/tests/data/gen_gradient_data.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import h5py as h5
import numpy as np

N=32

numbers = np.random.normal(size=(N,N,N))
with h5.File("gradient_numbers.h5", mode="w") as f:
  f['/random'] = numbers
  f['/random_fft'] = np.fft.rfftn(numbers)
