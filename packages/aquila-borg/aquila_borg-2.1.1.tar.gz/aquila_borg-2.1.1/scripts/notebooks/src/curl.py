#+
#   ARES/HADES/BORG Package -- ./scripts/notebooks/src/curl.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import numpy as np

def curl(vect,dx=1,dy=1,dz=1):
    "return the curl of a n-D field"
    [P_dy,P_dz]=np.gradient(vect[0],axis=[1,2])
    [Q_dx,Q_dz]=np.gradient(vect[1],axis=[0,2])
    [R_dx,R_dy]=np.gradient(vect[2],axis=[0,1])
    
    curl=np.array([R_dy-Q_dz,P_dz-R_dx,Q_dx-P_dy])
    
    return curl

def div(vect,dx=1,dy=1,dz=1):
    "return the divergence of a n-D field"
    return np.sum(np.gradient(vect),axis=0)
             
