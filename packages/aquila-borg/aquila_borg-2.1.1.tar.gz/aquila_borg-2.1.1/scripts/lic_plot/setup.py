#+
#   ARES/HADES/BORG Package -- ./scripts/lic_plot/setup.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy 

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [
	Extension("lic_internal", ["lic_internal.pyx"],
			include_dirs=[numpy.get_include()])
	],
)

