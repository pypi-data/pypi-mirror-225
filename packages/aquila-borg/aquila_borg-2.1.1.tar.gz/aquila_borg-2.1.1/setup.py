import stat
import os
import sys
import shutil
from distutils.command.install_data import install_data
import pathlib
from setuptools import find_packages, setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.install_lib import install_lib
from setuptools.command.install_scripts import install_scripts
import struct

BITS = struct.calcsize("P") * 8
PACKAGE_NAME = "aquila_borg"

class CMakeExtension(Extension):
    """
    An extension to run the cmake build

    This simply overrides the base extension class so that setuptools
    doesn't try to build your sources for you
    """

    def __init__(self, name, sources=[]):

        super().__init__(name = name, sources = sources)

        self.SOURCE_DIR = str(pathlib.Path().absolute())

class InstallCMakeLibsData(install_data):
    """
    Just a wrapper to get the install data into the egg-info

    Listing the installed files in the egg-info guarantees that
    all of the package files will be uninstalled when the user
    uninstalls your package through pip
    """

    def run(self):
        """
        Outfiles are the libraries that were built using cmake
        """

        # There seems to be no other way to do this; I tried listing the
        # libraries during the execution of the InstallCMakeLibs.run() but
        # setuptools never tracked them, seems like setuptools wants to
        # track the libraries through package data more than anything...
        # help would be appriciated

        self.outfiles = self.distribution.data_files

class InstallCMakeLibs(install_lib):
    """
    Get the libraries from the parent distribution, use those as the outfiles

    Skip building anything; everything is already built, forward libraries to
    the installation step
    """

    def run(self):
        """
        Copy libraries from the bin directory and place them as appropriate
        """

        self.announce("Moving library files", level=3)
#        print(self.build_temp)
#
#        self.distribution.bin_dir = CosmoTool_extension.bin_dir
#
#        # We have already built the libraries in the previous build_ext step
#
#        self.skip_build = True
#
#        # Depending on the files that are generated from your cmake
#        # build chain, you may need to change the below code, such that
#        # your files are moved to the appropriate location when the installation
#        # is run
#
#        libs = [os.path.join(bin_dir, _lib) for _lib in
#                os.listdir(bin_dir) if
#                os.path.isfile(os.path.join(bin_dir, _lib)) and
#                os.path.splitext(_lib)[1] in [".dll", ".so"]
#                and not (_lib.startswith("python") or _lib.startswith(PACKAGE_NAME))]
#
#        for lib in libs:
#
#            shutil.move(lib, os.path.join(self.build_dir,
#                                          os.path.basename(lib)))
#
#        # Mark the libs for installation, adding them to
#        # distribution.data_files seems to ensure that setuptools' record
#        # writer appends them to installed-files.txt in the package's egg-info
#        #
#        # Also tried adding the libraries to the distribution.libraries list,
#        # but that never seemed to add them to the installed-files.txt in the
#        # egg-info, and the online recommendation seems to be adding libraries
#        # into eager_resources in the call to setup(), which I think puts them
#        # in data_files anyways.
#        #
#        # What is the best way?
#
#        # These are the additional installation files that should be
#        # included in the package, but are resultant of the cmake build
#        # step; depending on the files that are generated from your cmake
#        # build chain, you may need to modify the below code
#
#        self.distribution.data_files = [os.path.join(self.install_dir,
#                                                     os.path.basename(lib))
#                                        for lib in libs]
#        print(self.distribution.data_files)
#
#        # Must be forced to run after adding the libs to data_files

        self.distribution.run_command("install_data")

        super().run()

class BuildCMakeExt(build_ext):
    """
    Builds using cmake instead of the python setuptools implicit build
    """

    def run(self):
        """
        Perform build_cmake before doing the 'normal' stuff
        """

        for extension in self.extensions:

            if extension.name == 'borg':
                self.package = 'borg'

                self.build_cmake(extension)

        #super().run()

    def build_cmake(self, extension: Extension):
        """
        The steps required to build the extension
        """

        self.announce("Preparing the build environment", level=3)

        package_dir = os.path.abspath(os.path.join(self.build_lib, 'borg'))


        extension.build_dir = pathlib.Path(self.build_temp)
        install_dir = os.path.abspath(self.build_lib)
        #extension.bin_dir = str(pathlib.Path(os.path.join(extension.build_dir, 'private_install')).absolute())
        SOURCE_DIR = extension.SOURCE_DIR
        build_dir = extension.build_dir

        extension_path = pathlib.Path(self.get_ext_fullpath(extension.name))

        os.makedirs(build_dir, exist_ok=True)
        os.makedirs(extension_path.parent.absolute(), exist_ok=True)

        # Now that the necessary directories are created, build

        self.announce("Configuring cmake project", level=3)

        self.spawn(['cmake', '-H'+SOURCE_DIR, '-B'+self.build_temp,
                    '-DENABLE_OPENMP=ON','-DINTERNAL_BOOST=ON','-DINTERNAL_EIGEN=ON',
                    '-DINTERNAL_HDF5=ON','-DINTERNAL_GSL=ON',
                    '-DBUILD_PYTHON_EXTENSION=ON', '-DBUILD_TESTING=OFF',
                    '-DBUILD_PYTHON_EMBEDDER=OFF', '-DINSTALL_PYTHON_LOCAL=OFF',
                    '-DINSTALL_COMPATIBILITY_PYBORG=OFF',
                    '-DCONTEXT_TIMER=ON', '-DBUILD_JULIA=OFF', '-DUSE_NATIVE_ARCH=OFF',
                    f"-DPYTHON_SITE_PACKAGES={install_dir}",
                    f"-DPYTHON_EXECUTABLE={sys.executable}"])


        self.announce("Building binaries", level=3)

        self.spawn(["cmake", "--build", self.build_temp, "--target", "install",
                      "--config", "Release"])

        # Build finished, now copy the files into the copy directory
        # The copy directory is the parent directory of the extension (.pyd)

pyborg_extension = CMakeExtension(name="borg")

version_py = os.path.join(os.path.dirname(__file__), 'VERSION.txt')
with open(version_py, "r") as gh:
  version = gh.read().strip()

setup(name='aquila_borg',
      version=version,
      packages=["aquila_borg"],
      package_dir={'aquila_borg': 'extra/python/python/aquila_borg'},
      install_requires=['numpy','deprecated'],
      setup_requires=['numpy'],
      ext_modules=[pyborg_extension],
      description='ARES/BORG engine packaged in a Python module',
      long_description=open("./README.rst", 'r').read(),
      long_description_content_type="text/x-rst",
      keywords="cosmology, inference, simulation, statistics",
      classifiers=["Intended Audience :: Developers",
                   "Natural Language :: English",
                   "License :: OSI Approved :: "
                   "GNU Lesser General Public License v3 (LGPLv3)",
                   "License :: OSI Approved :: "
                   "CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)",
                   "Programming Language :: C",
                   "Programming Language :: C++",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: Implementation :: CPython"],
      license_files=('License_CeCILL_V2.1.txt','License_GPL-3.0.txt'),
      include_package_data=True,
      cmdclass={
          'build_ext': BuildCMakeExt,
          'install_data': InstallCMakeLibsData,
          'install_lib': InstallCMakeLibs,
          },
      python_requires='>=3.6'
)
