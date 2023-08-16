#+
#   ARES/HADES/BORG Package -- ./scripts/misc/convert_2m++.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import numpy as np
from scipy import constants as sconst

LIGHT_SPEED = sconst.c/1000. #In km/s

catalog = np.load("2m++.npy")

with open("2MPP.txt", mode="w") as f:
    
    cond = (catalog['flag_vcmb']==1)*(catalog['flag_zoa']==0)*(catalog['best_velcmb'] > 100)
    for i,c in enumerate(catalog[cond]):
        M = c['K2MRS'] - 5*np.log10(c['best_velcmb']/100*1e5)
        zo = c['velcmb']/LIGHT_SPEED
        z = zo
        
        f.write(
            "%d %lg %lg %lg %lg %lg %lg\n" %
                (i, np.radians(c['ra']), np.radians(c['dec']), zo, c['K2MRS'], M, z)
            )
            
