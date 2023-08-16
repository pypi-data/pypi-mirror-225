==================================================
BORG: Bayesian Origin Reconstruction from Galaxies
==================================================

Please check the individual source files for the respective contributors.

Version 2.1

Description
-----------

This is the main component of the Bayesian Large Scale Structure inference
pipeline.

A lot of complementary informations are available on the wiki https://www.aquila-consortium.org/.

Cloning all the modules
-----------------------

The ARES software is only the foundation for other modules that adds many more functionalities to the framework.

Notably, the Aquila collaboration has developped the BORG extension that encodes advanced forward model and complex likelihoods
to run inferences on galaxy clustering, lyman-alpha, and more.

To get access to the extra modules please contact Aquila consortium members, who will tell you what are the policy in places.
Once your account on bitbucket is authorized you may use the script `get-aquila-modules.sh`. The procedure is as follow:

* first change to the desired branch (i.e. develop/2.1) with `git checkout the_interesting_branch`
* clone all the adequate modules `get-aquila-modules.sh --clone`
* setup the branches for the modules `get-aquila-modules.sh --branch-set`
* Polish up your environment by installing the git hooks `get-aquila-modules.sh --hooks`

**NOTE** the git hook require the availability `clang-format` to check on the formatting. If it is not present, then it will fail
the execution.

Building
--------

There is a special command line that prepares prepares build system to compile
all tools and libraries. It resides in the root directory of the ares source
tree and is called "build.sh". By default it will build everything in the
"build" subdirectory. To get all the options please run with the option
"--help".

After the tool has bee run, you can move to the build directory and execute
"make", which will build everything.

Please pay attention warnings and error messages. The most important are color marked.
Notably some problems may occur if two versions of the same compiler are used for C and C++.
To adjust that it is sufficient to explicitly specify the compiler path with the options '--c-compiler'
and '--cxx-compiler' of "build.sh".

*Note*: When modules are present in extra/, you may prevent them from building by putting an empty file called `DO_NOT_BUILD` in the
corresponding directory folder of the concerned module. For example, to prevent `borg` from building do `touch extra/borg/DO_NOT_BUILD`
from the present directory and the build system will ignore `borg`.

Compiler compatibilities
------------------------

Tested on GCC 7.0 - 10.2.
Some performance regressions were noted with gcc 8.1.
Countermeasures have been introduced though some corner cases
may still be a bit slower. Clang is unaffected by this regression.

Note that GCC <= 6 fails because it does not support correctly C++14 features.


Documentation
-------------

Please refer to `docs/README.txt`.

The documentation is also available on https://docs.aquila-consortium.org/borg-public/2.1/

Modules
-------

The core package supports to have extensions statically linked to the core.
They have to be put in extra/ and the cmake scripts will automatically link
to it. Check 'extra/demo/' for an example.

Usage policy
------------

Please check the documentation for details on the citation requirements for using this software: https://www.aquila-consortium.org/docs/borg-public/2.1/.

Acknowledgements
----------------

This work has been funded by the following grants and institutions over the
years:

* the DFG cluster of excellence "Origin and Structure of the Universe"
  (http://www.universe-cluster.de).
* Institut Lagrange de Paris (grant ANR-10-LABX-63, http://ilp.upmc.fr) within
  the context of the Idex SUPER subsidized by the French government through
  the Agence Nationale de la Recherche (ANR-11-IDEX-0004-02).
* BIG4 (ANR-16-CE23-0002) (https://big4.iap.fr)
* The "Programme National de Cosmologie et Galaxies" (PNCG, CNRS/INSU)
* Through the grant code ORIGIN, it has received support from
  the "Domaine d'Interet Majeur (DIM) Astrophysique et Conditions d'Apparitions
  de la Vie (ACAV)" from Ile-de-France region.
