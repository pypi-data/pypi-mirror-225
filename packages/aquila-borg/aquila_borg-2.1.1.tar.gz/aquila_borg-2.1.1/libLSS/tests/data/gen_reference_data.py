#+
#   ARES/HADES/BORG Package -- ./libLSS/tests/data/gen_reference_data.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import h5py as h5
import numpy as np

with h5.File("reference_data.h5", mode="w") as f:
  for N in [32]:
    numbers = np.random.normal(size=(N,N,N))
    f[f'/f_size_{N}'] = numbers
    f[f'/c_size_{N}'] = np.fft.rfftn(numbers)
