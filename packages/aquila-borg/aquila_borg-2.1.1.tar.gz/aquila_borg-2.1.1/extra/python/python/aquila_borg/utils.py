import numpy as np
from .borg_native import *


def newRealOutput(fwd_model):
    startN0,localN0,N1,N2 = fwd_model.getMPISlice()
    return np.empty((localN0, N1, N2))