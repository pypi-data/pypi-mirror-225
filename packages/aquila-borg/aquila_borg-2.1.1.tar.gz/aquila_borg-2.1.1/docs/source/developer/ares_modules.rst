ARES modules
============

ARES is typically the root project of many other sub-project or sub-modules. This is notably the case of the following modules:

- **hades**: this module declares and implements some of the fundamental API for manipulating general likelihood and deterministic forward models in the ARES/BORG framework. Notably important posterior samplers like the Hamiltonian Markov Chain algorithm are implemented there.
- **borg**: this module deals more with the physical aspect and the statistics of large scale structures. As an highlight it holds the code for implementing first and second order lagrangian perturbation theory, and the particle mesh (with tCOLA) model.
- **python**: this modules implements the python bindings, both as an external module for other python VM, or with an embedded python VM to interpret likelihoods and configuration written in python.
- **hmclet**:
