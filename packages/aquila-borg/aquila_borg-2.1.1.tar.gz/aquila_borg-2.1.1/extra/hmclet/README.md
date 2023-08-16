# README #

This is HMCLET: a small extra HMC framework for ARES to allow sampling a bunch of model parameters together. It provides a self calibration step to estimate
the masses for the HMC. 

### What is this repository for? ###

* Quick summary
* Version

### How do I get set up? ###

To include HMCLET please do a git clone of this repository in the `extra/` subfolder of ARES. For example:

    cd $ARES/extra
    git clone git@bitbucket.org:bayesian_lss_team/hmclet.git hmclet

Finally you can go to your build directory run `cmake .` to refresh the detected modules and run "make" again to finish the building
with HMClet included.

You can run `libLSS/tests/test_hmclet` to check that no error is triggered and verify the content of "test_sample.h5". It must contain a chain with 2 parameters
for which the first one oscillates around 1 with a variance of 10, and the other oscillates around 4 with a variance of 2.

### Contribution guidelines ###

You can submit pull requests to the BLSS team admin.

### Who do I talk to? ###

Guilhem Lavaux or Jens Jasche.
Check [our website](https://aquila-consortium.org/people.html) and the [wiki](https://aquila-consortium.org/wiki/).
