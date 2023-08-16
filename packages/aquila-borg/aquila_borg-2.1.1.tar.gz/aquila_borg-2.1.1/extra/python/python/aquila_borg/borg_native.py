#+
#   ARES/HADES/BORG Package -- ./extra/python/python/aquila_borg/borg_native.py
#   Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
try:
    from borg_embed import *
    EMBEDDED = True
except ModuleNotFoundError as e:
    # If we do not detect the embedded module we add some
    # symbols to account for the missing decorator functions
    # That way the python code are working both embedded or
    # in standalone python.
    from ._borg import *

    def _warning_function(f):
        print("warning! not embedded borg")
        return f

    registerLikelihoodBuilder = _warning_function
    registerGravityBuilder = _warning_function
    registerSamplerBuilder = _warning_function
    EMBEDDED = False
    del _warning_function

__all__ = [
    "cosmo", "forward", "bias", "likelihood", "samplers", "Console", "console",
    "memoryReport", "registerLikelihoodBuilder", "registerGravityBuilder",
    "registerSamplerBuilder", "EMBEDDED"
]


# ARES TAG: authors_num = 1
# ARES TAG: name(0) = Guilhem Lavaux
# ARES TAG: year(0) = 2020
# ARES TAG: email(0) = guilhem.lavaux@iap.fr
