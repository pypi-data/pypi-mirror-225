#+
#   ARES/HADES/BORG Package -- ./extra/python/python/aquila_borg/__init__.py
#   Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
"""
PyBORG root module
==================

PyBORG is a complete binding of the borg machine to python. The borg
module can be imported either from a normal python interpret or from
the embedded python in hades_python.

Be aware that you cannot import directly any of the native modules. To import
all borg facilities, it is required *and* sufficient to just execute ``import aquila_borg``.
It will provide all the modules such as `aquila_borg.cosmo` or `aquila_borg.samplers`.


*Note:* The `borg` module may be installed as an alias to `aquila_borg`. However the package name
is the same as the one used by BorgBackup. Thus there may be clashes between these two softwares.
It is advised to use `aquila_borg` to avoid conflicts.

"""
import sys
import io
import contextlib
import logging

try:
    import mpi4py

    MPI4PY_AVAILABLE = True
except:
    MPI4PY_AVAILABLE = False

from .borg_native import *

from . import dft
from . import utils

class _RewriteIO(io.IOBase):
    def __init__(self, original):
        self.original = original
        self.newline = False
        if MPI4PY_AVAILABLE:
            self.comm = mpi4py.MPI.COMM_WORLD
            self.prefix = f"[{self.comm.rank} / {self.comm.size}] "
        else:
            self.prefix = "[0/0]"

    def write(self, b):
        if b[0] == "\n":
            return self.original.write(b)
        return self.original.write(self.prefix + b)

    def writelines(self, lines):
        return self.original.writelines(lines)

class BorgMessageStream(io.IOBase):
    def __init__(self, console, level='std'):
        super().__init__()
        self.console = console
        if level == 'std':
            self.printer = console.print_std
        elif level == 'warn':
            self.printer = console.print_warning
        elif level == 'error':
            self.printer = console.print_error
        else:
            raise ValueError()

    def write(self, b):
        for line in b.split(sep="\n"):
           self.printer(line)

    def writelines(self, lines):
        for line in lines:
            if line[-1] == '\n':
                line = line[:-1]
            self.printer(line)

def capture_warnings(logger="py.warnings",level='warn'):
    logging.captureWarnings(True)
    l = logging.getLogger(logger)
    h = logging.StreamHandler(BorgMessageStream(console(), level=level))
    l.addHandler(h)
    return h

@contextlib.contextmanager
def borgConsole(original=sys.stdout):
    """Setup a clean redirection of BORG output, notably in presence of MPI4PY.

    Keyword Arguments:
        original (file-like): Where to send the console to (default: :class:`sys.stdout`)

    """
    yield contextlib.redirect_stdout(_RewriteIO(original))


def buildDefaultChain(box, cosmo_pars, a_init, model):
    """Build a default BORG chain from a model. This remove the hastle of setting up
    a primordial fluctuation generator, and the cosmological parameters.

    Args:
        box (borg.forward.BoxModel): the specification of the box for the simulation
        cosmo_pars (borg.cosmo.CosmologicalParameters): the cosmology chosen
        a_init (float): the starting scale factor for `model`
        model (borg.forward.BORGForwardModel): the model to be chained with

    Returns:
        borg.forward.BORGForwardModel: a newly built chain for cosmology
    """
    chain = forward.ChainForwardModel(box)
    chain.addModel(forward.models.HermiticEnforcer(box))
    chain.addModel(forward.models.Primordial(box, a_init))
    chain.addModel(forward.models.EisensteinHu(box))
    chain.addModel(model)
    chain.setCosmoParams(cosmo_pars)
    return chain


if EMBEDDED:
    capture_warnings()

__all__ = ["borgConsole", "buildDefaultChain", "dft", "utils"] + borg_native.__all__

# ARES TAG: authors_num = 1
# ARES TAG: name(0) = Guilhem Lavaux
# ARES TAG: year(0) = 2020
# ARES TAG: email(0) = guilhem.lavaux@iap.fr
