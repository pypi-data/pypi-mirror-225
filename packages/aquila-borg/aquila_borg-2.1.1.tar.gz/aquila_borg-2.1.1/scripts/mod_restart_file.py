#+
#   ARES/HADES/BORG Package -- ./scripts/mod_restart_file.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import h5py
import numpy as np


#set chain
chain_path="."

#set reference file
refdir ='/scratch/jasche/panphasia_run_lc/'
fref=refdir+'restart.h5_0'

#set target file
tardir ='/scratch/jasche/panphasia_run_h/'
ftar=tardir+'restart.h5_0'

#read density files from reference file
print fref
dref = h5py.File(fref, "r")

dref_final_density=dref['/scalars/BORG_final_density']
dref_s_field=dref['/scalars/s_field']
dref_s_hat_field=dref['/scalars/s_hat_field']


dtar = h5py.File(ftar, "r+")
dtar_final_density=dtar['/scalars/BORG_final_density']
dtar_s_field=dtar['/scalars/s_field']
dtar_s_hat_field=dtar['/scalars/s_hat_field']

'''
WARNING: At this point you will irretrievably
modify your restart file!!!!!!
'''


dtar_final_density[...] = dref_final_density[...]
dtar_s_field[...]       = dref_s_field[...]
dtar_s_hat_field[...]   = dref_s_hat_field[...]


dref.close()
dtar.close()
