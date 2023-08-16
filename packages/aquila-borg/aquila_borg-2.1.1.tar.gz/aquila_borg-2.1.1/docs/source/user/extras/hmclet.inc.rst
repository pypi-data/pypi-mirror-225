hmclet
======

Guilhem has developped a much smaller variant of the Hamiltonian Markov
Chain algorithm to jointly sample a limited set of parameters (like <
100).

This is **HMCLET**: a small extra HMC framework for |a| to allow sampling a bunch of model parameters
together. It provides a self calibration step to estimate the masses for
the HMC.

Setup
-----

The code is available in "hmclet" module . To use it, clone this
repository into extra/hmclet in ARES source tree. You can for example
do:

.. code:: bash

   cd $ARES_SOURCE/extra
   git clone https://bitbucket.org/bayesian_lss_team/hmclet.git hmclet

Once it is checked out you can move to the build directory and run
``cmake .``, then ``make`` and you will have the new module compiled.

You can run ``libLSS/tests/test_hmclet`` to check that no error is
triggered and verify the content of "test_sample.h5". It must contain a
chain with 2 parameters for which the first one oscillates around 1 with
a variance of 10, and the other oscillates around 4 with a variance of
2.

Use
---

The Little HMC (HMClet, like Applet) framework consists in two classes
in the namespace ``LibLSS::HMCLet``:

-  JointPosterior, which is the one acting like a parent to your class
   describing the log-posterior,
-  SimpleSampler, which is using an instance of JointPosterior to
   generate samples using the HMC algorithm.

There is a demonstration (and test case) available in
libLSS/tests/test_hmclet.cpp, please have a look at it.

To use SingleSampler you have to make a new class derivative of
JointPosterior and implement three functions:

-  ``getNumberOfParameters()`` which returns an integer corresponding to
   the number of parameters supported by your posterior
-  ``evaluate(parameters)`` which returns the opposite of the
   log-posterior (i.e. like chi2/2)
-  ``adjointGradient(parameters, adjoint_gradient)`` which fills the
   adjoint gradient vector corresponding to the given parameters.

An example is as follow:

.. code:: cpp

   class MyPosterior: virtual public JointPosterior {
   public:
      /* Bla bla for constructor and destructor */
      virtual size_t getNumberOfParameters() const  {
       return 1;
     }

     virtual double evaluate(VectorType const& params) {
       return 0.5 * square(params[0]-1)/10.;
     }

     virtual void adjointGradient(VectorType const& params, VectorType& params_gradient) {
       params_gradient[0] = (params[0]-1)/10.;
     }
   };

The above posterior will represent a Gaussian distribution centered on
one, with a variance of 10. It depends on a single parameter.

The sampling would occur like this:

.. code:: cpp

   auto posterior = std::make_shared<MyPosterior>();
   SimpleSampler sampler(posterior);

   /* Calibrate the mass matrix.
    *   comm: MPI communication
    *   rgen: Random number generator
    *   steps: number of steps to attempt for calibration
    *   init_params: initial parameters to start calibration
    *   init_step: typical step size to start with
    */
   sampler.calibrate(comm, rgen, steps, init_params, init_step);

   /* Generate a sample with HMC
    *   comm: MPI communication
    *   rgen: Random number generator
    *   params: current parameter state
    */
   sampler.newSample(comm, rgen, init_params);

Contributors
------------

-  Guilhem Lavaux
-  Jens Jasche

You can submit pull requests to the BLSS team admin.
