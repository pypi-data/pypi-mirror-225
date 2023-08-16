.. _new_core_program:

Writing a new ARES core program
===============================

.. _what_is_a_core_program:

What is a core program ?
------------------------

A core program is in charge of initializing the sampling machine,
loading the data in their structures and running the main sampling loop.
There are two default core programs at the moment: ARES3 (in
src/ares3.cpp) and HADES3 (extra/hades/src/hades3.cpp). ARES3 implements
the classical ARES sampling framework, which includes linear modeling,
bias, foreground and powerspectrum sampling. HADES3 implements the
non-linear density inference machine: classical HADES likelihood, BORG
LPT, BORG 2LPT, BORG PM, and different variant of bias functions.

.. _why_write_a_new_one:

Why write a new one ?
---------------------

Because you are thinking of a radically different way of presenting the
data, or because your model is based on different assumptions you may
have to redesign the way data are load and initialized. Also if you are
thinking of a different way of sampling the different parameters (or
more than usual) then you may have to implement a new bundle.

.. _prepare_yourself:

Prepare yourself
----------------

A core program is composed of different elements that can be taken from
different existing parts. We can look at ares3.cpp for an example. The
main part (except the splash screen) is:

.. code:: c++

   #define SAMPLER_DATA_INIT "../ares_init.hpp"
   #define SAMPLER_BUNDLE "../ares_bundle.hpp"
   #define SAMPLER_BUNDLE_INIT "../ares_bundle_init.hpp"
   #define SAMPLER_NAME "ARES3"
   #define SAMPLER_MOCK_GENERATOR "../ares_mock_gen.hpp"
   #include "common/sampler_base.cpp"

As you can see a number of defines are set up before including the
common part, called "common/sampler_base.cpp". These defines are doing
the following:

-  ``SAMPLER_DATA_INIT`` specifies the include file that holds the
   definition for data initializer. This corresponds to two functions:

   -  ::
   
        template void sampler_init_data(MPI_Communication *mpi_world, MarkovState& state, PTree& params),
        
      which is in charge of allocating the adequate arrays for storing
      input data into the ``state`` dictionnary. The actual names of
      these fields are sampler dependent. In ares and hades, they are
      typically called "galaxy_catalog_%d" and "galaxy_data_%d" (with %d
      being replaced by an integer). This function is always called even
      in the case the code is being resumed from a former run.
   -  ::
   
        template void sampler_load_data(MPI_Communication *mpi_world, MarkovState& state, PTree& params, MainLoop& loop),
        
      which is in charge of loading the data into the structures. This
      function is only called during the first initialization of the
      chain.

-  ``SAMPLER_BUNDLE`` defines the sampler bundle which are going to be
   used. Only the structure definition of ``SamplerBundle`` should be
   given here.
-  ``SAMPLER_BUNDLE_INIT`` defines two functions working on initializing
   the bundle:

   -  ::
   
        template void sampler_bundle_init(MPI_Communication *mpi_world, ptree& params, SamplerBundle& bundle, MainLoop& loop),
        
      which does the real detailed initialization, including the
      sampling loop program.
   -  ::
   
        void sampler_setup_ic(SamplerBundle& bundle, MainLoop& loop),
        
      which allows for more details on the initial conditions to be set
      up.

-  ``SAMPLER_NAME`` must a be a static C string giving the name of this
   core program.
-  ``SAMPLER_MOCK_GENERATOR`` specifies a filename where

.. code:: c++
    
    template void prepareMockData(PTree& ptree, MPI_Communication *comm, MarkovState& state, CosmologicalParameters& cosmo_params, SamplerBundle& bundle)
    
is defined. "ares_mock_gen.hpp" is a single gaussian random field
generator with the selection effect applied to data.

.. _creating_a_new_one:

Creating a new one
------------------

.. _create_the_skeleton:

Create the skeleton
~~~~~~~~~~~~~~~~~~~

.. _create_the_sampler_bundle:

Create the sampler bundle
~~~~~~~~~~~~~~~~~~~~~~~~~

.. _initializing_data_structures:

Initializing data structures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _filling_data_structures:

Filling data structures
~~~~~~~~~~~~~~~~~~~~~~~

.. _attach_the_core_program_to_cmake:

Attach the core program to cmake
--------------------------------

Build
-----
