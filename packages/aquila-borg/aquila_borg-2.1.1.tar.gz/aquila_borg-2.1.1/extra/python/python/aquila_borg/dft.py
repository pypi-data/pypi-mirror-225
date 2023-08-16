import numpy as np
from .borg_native import *


class DFT:
    """This implements an MPI DFT transform which is compatible with the other IO involved
    in BORG.

    Note that r2c and c2r are inverse and forward transform respectively. They are already
    properly normalized with physical units.

    TODO: Specify sub-communicators

    Arguments:
      box (BoxModel): Physical box specifications of the transform

    """
    def __init__(self, box):
        # We do an abuse of the API here
        self._box = box
        self._model = forward.models.HadesLinear(box, ai=1.0, af=1.0)
        cpar = cosmo.CosmologicalParameters()
        self._model.setCosmoParams(cpar)
        _, localN0, N1, N2 = self._model.getMPISlice()
        self.Nfft = localN0, N1, N2 // 2 + 1
        self.Nreal = localN0, N1, N2

    def r2c(self, real_array):
        """Execute a real to complex transform

        Arguments:
          real_array (numpy.ndarray): Input real array

        Returns:
          numpy.ndarray: A complex array
        """
        assert real_array.dtype == np.float64
        self._model.forwardModel_v2(real_array)

        out = np.empty(self.Nfft, dtype=np.complex128)
        self._model.getDensityFinal(out)
        return out

    def c2r(self, complex_array):
        """Execute a complex to real transform

        Arguments:
          real_array (numpy.ndarray): Input complex array

        Returns:
          numpy.ndarray: A real array
        """
        assert real_array.dtype == np.complex128
        self._model.forwardModel_v2(complex_array)

        out = np.empty(self.Nreal, dtype=np.float64)
        self._model.getDensityFinal(out)
        return out
