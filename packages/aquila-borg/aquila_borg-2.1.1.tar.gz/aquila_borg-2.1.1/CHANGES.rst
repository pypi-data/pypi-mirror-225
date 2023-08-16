Release notes
=============

This file only lists the most important changes to each version. We try to follow semantic versioning:
- Major release means API incompatibilities
- Minor release means API compatibilities, but significant feature differences
- Bugfix release only fixes bugs

Release 2.1
-----------

- An option to control the verbosity in log file has been added ("system/logfile_verbose_level", v2.1.3)

Forward related
^^^^^^^^^^^^^^^

- Add a way of transforming all bias models into a forward deterministic transition. It means more flexibility at the cost of losing performance/memory by doing
  more computations than required. For example, each subcatalog needs its own bias which could trigger quite a lot of recomputation and/or caching.
- PMv2 optimization when sampling.
- Implement a simple (non-MPI) haar transform.
- Add EnforceMass model element to articifially fix the mass conservation.
- Forward models may support a new behavior for adjointModel_v2. They can accumulate all adjoint vectors that are provided to them through
  adjointModel_v2. The new behavior must be requested by calling BORGForwardModel::accumulateAdjoint. In that case, the user is explicitly
  requested to clear the adjoint gradient when the computation is done by calling BORGForwardModel::clearAdjointGradient.
  That behavior has been ported to pyborg. If the mode is not supported, an exception will be triggered.
- Merged Altair code.
- Bind ClassCosmo to ARES. Python binding is also active and vectorized for get_Tk.

Sampler related
^^^^^^^^^^^^^^^

- Add CG89 "higher order" symplectic integrator.

API related:
^^^^^^^^^^^^

- ManyPower bias model needs a likelihood info entry now to set the width of the prior on parameters. The name is ManyPower_prior_width in [info].
- Code cleanup in velocity field estimator. It also now supports Simplex-In-Cell (no adjoint gradient yet and only non-MPI).
- Models accept a broader range of parameters using BORGForwardModel::setModelParams.

Python related:
^^^^^^^^^^^^^^^

- *NEW tool* hades_python which supports a full deterministic transition written in python/tensorflow/jax. Data loading is still work in progress and
  may need hacking at the moment
- Python extension is supporting LikelihoodInfo and the bias as forward model element.
- Add a 'setup.py' to support compiling the BORG python module directly with pip and packaging as a wheel file.
- Samplers fully supported from Python.

Build related
^^^^^^^^^^^^^

- build.sh only downloads the dependency if the file is not already there
- Error reporting include a full C++ stacktrace on supported platforms (cmake flag is STACKTRACE_USE_BACKTRACE=ON, experimental at the moment
  It can be turned off).
- Added GIT hooks to check on basic text elements (like formatting) before running commits.
  clang-formatter absence may be overridden using ARES_CLANG_OVERRIDE=1

Release 2.0alpha
----------------

- Use a prior that is purely gaussian unit variance (Fourier) in HMC now. The cosmology is completely moved as a BORGForwardModel.
- BORGForwardModel adds the v2 API to executes model: forwardModel_v2, and adjointModel_v2. This relies heavily on the mechanics of ModelIO
- Deterministic models are now self-registering and the available lists can be dynamically queried.
- Add a hook to optionally dump extra bias fields.
- Add QLPT and QLPT_RSD forward model in extra/borg
- Lots of documentation reorganization
- Added the lyman alpha model in extra/borg
- Merged the EFT likelihood effort in extra/borg


Release 1.0
-----------


Initial release
