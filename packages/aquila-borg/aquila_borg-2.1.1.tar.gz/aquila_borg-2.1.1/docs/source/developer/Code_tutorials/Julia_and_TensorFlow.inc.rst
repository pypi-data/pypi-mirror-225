.. _julia_and_tensorflow:

Julia and TensorFlow
====================

The ``julia`` language can be used within ``HADES``. It is automatically
installed if ``julia`` (at least ``v0.7.0``) is available on the machine
and if the ``hmclet`` is pulled into ``extra/``. Note that ``julia`` is
a relatively new language and develops quickly - it is also 1 indexed!

hmclet
------

At the moment, the ``julia`` core is available as part of ``hmclet`` - a
small HMC which can be used to sample external parameters, such as bias
parameters.

.. _jl_files:

.jl files
---------

The ``julia`` code is contained in ``.jl`` files which must contain
several things to be used by the ``hmclet``. An example of a linear bias
test likelihood can be found in ``extra/hmclet/example/test_like.jl``.

.. _initialisation_file:

Initialisation file
~~~~~~~~~~~~~~~~~~~

The ``.ini`` needs to have a few lines added to describe the ``julia``
file to use, the name of the module defined in the ``julia`` file and
whether to use a ``slice`` sampler or the ``hmclet``. They are added to
the ``.ini`` file as

.. code:: bash

   [julia]
   likelihood_path=test_like.jl
   likelihood_module=julia_test
   bias_sampler_type=hmclet

.. _module_name_and_importing_from_liblss:

Module name and importing from libLSS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each ``julia`` file must contain a module (whose name is entered in the
``.ini`` file)

.. code:: julia

   module julia_test

To be able to import from libLSS (including the state and the print
functions) the ``julia`` module needs to contain the ``using``
statement, including the points.

.. code:: julia

   using ..libLSS

   import ..libLSS.State
   import ..libLSS.GhostPlanes, ..libLSS.get_ghost_plane
   import ..libLSS.print, ..libLSS.LOG_INFO, ..libLSS.LOG_VERBOSE, ..libLSS.LOG_DEBUG

The dots are necessary since the second point is to access the current
module and the first point is to access the higher level directory.

.. _importing_modules:

Importing modules
~~~~~~~~~~~~~~~~~

Any other ``julia`` module can be included in this ``julia`` code by
using

.. code:: julia

   using MyModule

where ``MyModule`` can be self defined or installed before calling in
HADES using

.. code:: julia

   using Pkg
   Pkg.add("MyModule")

in a ``julia`` terminal.

.. _necessary_functions:

Necessary functions
~~~~~~~~~~~~~~~~~~~

A bunch of different functions are necessary in the ``julia`` code to be
used in the ``hmclet``. These are:

.. code:: julia

   function initialize(state)
       print(LOG_INFO, "Likelihood initialization in Julia")
       # This is where hmclet parameters can be initialised in the state
       NCAT = libLSS.get(state, "NCAT", Int64, synchronous=true) # Number of catalogs
       number_of_parameters = 2 # Number of parameters
       for i=1:NCAT
           hmclet_parameters = libLSS.resize_array(state, "galaxy_bias_"*repr(i - 1), number_of_parameters, Float64)
           hmclet_parameters[:] = 1
       end
   end

   function get_required_planes(state::State)
       print(LOG_INFO, "Check required planes")
       # This is where the planes are gathered when they live on different mpi nodes
       return Array{UInt64,1}([])
   end

   function likelihood(state::State, ghosts::GhostPlanes, array::AbstractArray{Float64,3})
      print(LOG_INFO, "Likelihood evaluation in Julia")
      # Here is where the likelihood is calculated and returned. 
      # This can be a call to likelihood_bias() which is also a necessary function
      NCAT = libLSS.get(state, "NCAT", Int64, synchronous=true)
      L = Float64(0.)
      for i=1:NCAT
          hmclet_parameters = libLSS.get_array_1d(state, "galaxy_bias_"*repr(i - 1), Float64)
          L += likelihood_bias(state, ghosts, array, i, hmclet_parameters)
      end
      return L
   end

   function generate_mock_data(state::State, ghosts::GhostPlanes, array::AbstractArray{Float64,3})
       print(LOG_INFO, "Generate mock")
       # Mock data needs to be generated also
       NCAT = libLSS.get(state, "NCAT", Int64, synchronous=true)
       for i=1:NCAT
           data = libLSS.get_array_3d(state, "galaxy_data_"*sc, Float64)
           generated_data = function_to_generate_data() # We can use other functions which are defined within the julia module
           for i=1:size(data)[1],j=1:size(data)[2],k=1:size(data)[3]
               data[i, j, k] = generated_data[i, j, k] + libLSS.gaussian(state) # We can use functions defined in libLSS
           end
       end
   end

   function adjoint_gradient(state::State, array::AbstractArray{Float64,3}, ghosts::GhostPlanes, ag::AbstractArray{Float64,3})
       print(LOG_VERBOSE, "Adjoint gradient in Julia")
       # The gradient of the likelihood with respect to the input array
       NCAT = libLSS.get(state, "NCAT", Int64, synchronous=true)
       ag[:,:,:] .= 0 # Watch out - this . before the = is necessary... extremely necessary!
       for i=1:NCAT
          # Calculate the adjoint gradient here and update ag
          # Make sure not to update any gradients which are not in the selection
          selection = libLSS.get_array_3d(state, "galaxy_sel_window_"*repr(i - 1), Float64)
          mask = selection .> 0
          adjoint_gradient = function_to_calculate_adjoint_gradient()
          ag[mask] += adjoint_gradient[mask]
       end
   end

   function likelihood_bias(state::State, ghosts::GhostPlanes, array, catalog_id, catalog_bias_tilde)
       # The likelihood after biasing the input array
       L = function_to_calculate_likelihood()
       return L
   end

   function get_step_hint(state, catalog_id, bias_id)
       # Guess for the initialisation of the hmclet mass matrix or the slice sample step size
       return 0.1
   end

   function log_prior_bias(state, catalog_id, bias_tilde)
       # Prior for the bias parameters
       return 0.
   end

   function adjoint_bias(state::State, ghosts::GhostPlanes, array, catalog_id, catalog_bias_tilde, adjoint_gradient_bias)
       # Calculate the gradient of the likelihood with respect to the parameters in the hmclet
       adjoint_gradient_bias[:] .= function_to_calculate_gradient_with_respect_to_bias()
   end

.. _tensorflow_in_julia:

TensorFlow in julia
-------------------

One amazing advantage of having ``julia`` built into ``HADES`` is that
we can now use ``TensorFlow``. ``TensorFlow`` is a very powerful tensor
based computational language which has the exact same syntax for running
on GPUs and CPUs. The version of ``TensorFlow.jl`` is not officially
supported, but is relatively well maintained, although it is based on
``v1.4`` whilst the current version is well beyond that. One can use a
newer vesion of ``TensorFlow`` by installing it from source and placing
it in the ``julia`` ``TensorFlow`` directory, however doing this does
not give you access to all the commands available in ``TensorFlow``. For
example, ``TensorFlow.subtract()`` and ``TensorFlow.divide()`` do not
exist. Fortunately, a lot of ``julia`` functions work on ``TensorFlow``
tensors (such as ``-``, ``.-``, ``/`` and ``./``).

There is a ``TensorFlow`` implementation of ``test_like.jl`` (discussed
above) in ``extra/hmclet/example/test_like_TF.jl``.

The essence of ``TensorFlow`` is to build a graph of tensors connected
by computations. Once the graph is built then results are accessed by
passing values through the graph. An example graph could be:

.. code:: julia

   using TensorFlow
   using Distributions # To be used for initialising variable values

    = TensorFlow.placeholder(Float64, shape = [100, 1], name = "a")      # This is a tensor which contains no value and has a shape
                                                                         # of [100, 1]                                                   
   b = TensorFlow.placeholder(Float64, shape = (), name = "b")           # This is a tensor which contains no value or shape

   c = TensorFlow.placeholder(Float64, shape = [1, 10], name = "c")      # This is a tensor which has no value and has a shape of [1, 10]

   variable_scope("RandomVariable"; initializer=Normal(0., 0.1)) do
       global d = TensorFlow.get_variable("d", Int64[10], Float64)       # This is a variable tensor which can be initialised to a value
   end                                                                   # and has a shape of [10]. It must be global so it has maintains
                                                                         # outside of the scope
   e = TensorFlow.constant(1.:10., dtype = Float64, name = "e")          # This is a tensor of constant value with shape [10]

   f = TensorFlow.matmul(a, c, name = "f")                               # Matrix multiplication of a and c with output shape [100, 10]

   #g = TensorFlow.matmul(b, c, name = "g")                              # Matrix multiplication of b and c 
                                                                         # !THIS WILL FAIL SINCE b HAS NO SHAPE! Instead one can use
   g = TensorFlow.identity(b .* c, name = "g")                           # Here we make use of the overload matrix multiplication
                                                                         # function in julia, the tensor will say it has shape [1, 10]
                                                                         # but this might not be true. We use identity() to give the
                                                                         # tensor a name.
                                                                          
   h = TensorFlow.add(f, e, name = "h")                                  # Addition of f and e

   i = TensorFlow.identity(f - e, name = "i")                            # Subtraction of f and e

   j = TensorFlow.identity(f / e, name = "j")                            # Matrix division of f and e

   k = TensorFlow.identity(j ./ i, name = "k")                           # Elementwise division of j by i

We now have lots of tensors defined, but notice that these are tensors
and are not available as valued quantities until they are run. For
example running these tensors gives

.. code:: julia

   a
       > <Tensor a:1 shape=(100, 1) dtype=Float64>
   b
       > <Tensor b:1 shape=() dtype=Float64> # Note this is not the real shape of this tensor
   c
       > <Tensor c:1 shape=(1, 10) dtype=Float64>
   d
       > <Tensor d:1 shape=(10) dtype=Float64>
   e
       > <Tensor e:1 shape=(10) dtype=Float64>
   f
       > <Tensor f:1 shape=(100, 10) dtype=Float64>
   g
       > <Tensor g:1 shape=(1, 10) dtype=Float64> # Note this is not the real shape of this tensor either
   h
       > <Tensor h:1 shape=(100, 10) dtype=Float64>
   i
       > <Tensor i:1 shape=(100, 10) dtype=Float64>
   j
       > <Tensor j:1 shape=(100, 10) dtype=Float64>
   k
       > <Tensor k:1 shape=(100, 10) dtype=Float64>

To actually run any computations a session is needed

.. code:: julia

   sess = Session(allow_growth = true)

The ``allow_growth`` option prevents ``TensorFlow`` for taking up the
entire memory of a GPU.

Any constant value tensors can now be accessed by running the tensor in
the session

.. code:: julia

   run(sess, TensorFlow.get_tensor_by_name("e"))
       > 10-element Array{Float64,1}:
       >   1.0
       >   2.0
       >   3.0
       >   4.0
       >   5.0
       >   6.0
       >   7.0
       >   8.0
       >   9.0
       >   10.0
   run(sess, e)
       > 10-element Array{Float64,1}:
       >   1.0
       >   2.0
       >   3.0
       >   4.0
       >   5.0
       >   6.0
       >   7.0
       >   8.0
       >   9.0
       >   10.0

Notice how we can call the tensor by its name in the graph (which is the
proper way to do things) or by its variable name. If we want to call an
output to a computation we need to supply all necessary input tensors

.. code:: julia

   distribution = Normal()
   onehundredbyone = reshape(rand(distribution, 100), (100, 1))
   onebyten = reshape(rand(distribution, 10), (1, 10))

   run(sess, TensorFlow.get_tensor_by_name("f"), Dict(TensorFlow.get_tensor_by_name("a")=>onehundredbyone, TensorFlow.get_tensor_by_name("c")=>onebyten))
       > 100×10 Array{Float64,2}:
       >   ... ...
   run(sess, f, Dict(a=>onehundredbyone, c=>onebyten))
       > 100×10 Array{Float64,2}:
       >   ... ...
   run(sess, TensorFlow.get_tensor_by_name("k"), Dict(TensorFlow.get_tensor_by_name("a")=>onehundredbyone, TensorFlow.get_tensor_by_name("c")=>onebyten))
       > 100×10 Array{Float64,2}:
       >   ... ...
   run(sess, k, Dict(a=>onehundredbyone, c=>onebyten))
       > 100×10 Array{Float64,2}:
       >   ... ...

Any unknown shape tensor needs to be fed in with the correct shape, but
can in principle be any shape. If there are any uninitialised values in
the graph they need initialising otherwise the code will output an error

.. code:: julia

   run(sess, TensorFlow.get_tensor_by_name("RandomVariable/d"))
       > Tensorflow error: Status: Attempting to use uninitialized value RandomVariable/d

Notice that the variable built within ``variable_scope`` has the scope
name prepended to the tensor name. The initialisation of the tensor can
be done with ``TensorFlow.global_variables_initializer()``:

.. code:: julia

   run(sess, TensorFlow.global_variables_initializer())

Once this has been run then tensor ``d`` will have a value. This value
can only be accessed by running the tensor in the session

.. code:: julia

   run(sess, TensorFlow.get_tensor_by_name("RandomVariable/d"))
       > 1×10 Array{Float64,2}:
       >  0.0432947  -0.208361  0.0554441  …  -0.017653  -0.0239981  -0.0339648
   run(sess, d)
       > 1×10 Array{Float64,2}:
       >  0.0432947  -0.208361  0.0554441  …  -0.017653  -0.0239981  -0.0339648

This is a brief overview of how to use ``TensorFlow``. The ``HADES``
``hmclet`` likelihood code sets up all of the graph in the
initialisation phase

.. code:: julia

   function setup(N0, N1, N2)
       global adgrad, wgrad
       p = [TensorFlow.placeholder(Float64, shape = (), name = "bias"), TensorFlow.placeholder(Float64, shape = (), name = "noise")]
       δ = TensorFlow.placeholder(Float64, shape = Int64[N0, N1, N2], name = "density")
       g = TensorFlow.placeholder(Float64, shape = Int64[N0, N1, N2], name = "galaxy")
       s = TensorFlow.placeholder(Float64, shape = Int64[N0, N1, N2], name = "selection")
       gaussian = TensorFlow.placeholder(Float64, shape = Int64[N0, N1, N2], name = "gaussian_field")
       mask = TensorFlow.placeholder(Bool, shape = Int64[N0, N1, N2], name = "mask")
       mask_ = TensorFlow.reshape(mask, N0 * N1 * N2, name = "flat_mask")
       g_ = TensorFlow.identity(TensorFlow.boolean_mask(TensorFlow.reshape(g, N0 * N1 * N2), mask_), name = "flat_masked_galaxy")
       s_ = TensorFlow.identity(TensorFlow.boolean_mask(TensorFlow.reshape(s, N0 * N1 * N2), mask_), name = "flat_masked_selection")
       output = TensorFlow.add(1., TensorFlow.multiply(p[1], δ), name = "biased_density")
       mock = TensorFlow.multiply(s, output, name = "selected_biased_density")
       mock_ = TensorFlow.identity(TensorFlow.boolean_mask(TensorFlow.reshape(mock, N0 * N1 * N2), mask_), name = "flat_masked_selected_biased_density")
       mock_galaxy = TensorFlow.add(mock, TensorFlow.multiply(TensorFlow.multiply(TensorFlow.sqrt(TensorFlow.exp(p[2])), s), gaussian), name = "mock_galaxy")
       ms = TensorFlow.reduce_sum(TensorFlow.cast(mask, Float64), name = "number_of_voxels")
       loss = TensorFlow.identity(TensorFlow.add(TensorFlow.multiply(0.5, TensorFlow.reduce_sum(TensorFlow.square(g_ - mock_) / TensorFlow.multiply(TensorFlow.exp(p[2]), s_))), TensorFlow.multiply(0.5, TensorFlow.multiply(ms, p[2]))) - TensorFlow.exp(p[1]) - TensorFlow.exp(p[2]), name = "loss")
       adgrad = TensorFlow.gradients(loss, δ)
       wgrad = [TensorFlow.gradients(loss, p[i]) for i in range(1, length = size(p)[1])]
   end

Notice here that in ``TensorFlow``, the gradients are \*super\* easy to
calculate since it amounts to a call to ``TensorFlow.gradients(a, b)``
which is equivalent to da/db (its actually sum(da/db) so sometimes you
have to do a bit more leg work.

Now, whenever the likelihood needs to be calculated whilst running
``HADES`` the syntax is a simple as

.. code:: julia

   function likelihood(state::State, ghosts::GhostPlanes, array::AbstractArray{Float64,3})
       print(LOG_INFO, "Likelihood evaluation in Julia")
       L = Float64(0.)
       for catalog=1:libLSS.get(state, "NCAT", Int64, synchronous=true)
           L += run(sess, TensorFlow.get_tensor_by_name("loss"),
                   Dict(TensorFlow.get_tensor_by_name("bias")=>libLSS.get_array_1d(state, "galaxy_bias_"*repr(catalog - 1), Float64)[1],
                        TensorFlow.get_tensor_by_name("noise")=>libLSS.get_array_1d(state, "galaxy_bias_"*repr(catalog - 1), Float64)[2],
                        TensorFlow.get_tensor_by_name("density")=>array,
                        TensorFlow.get_tensor_by_name("galaxy")=>libLSS.get_array_3d(state, "galaxy_data_"*repr(catalog - 1), Float64),
                        TensorFlow.get_tensor_by_name("selection")=>libLSS.get_array_3d(state, "galaxy_sel_window_"*repr(catalog - 1), Float64),
                        TensorFlow.get_tensor_by_name("mask")=>libLSS.get_array_3d(state, "galaxy_sel_window_"*repr(catalog - 1), Float64).>0.))
       end
       print(LOG_VERBOSE, "Likelihood is " * repr(L))
       return L
   end

If ``TensorFlow`` is installed to use the GPU, then this code will
automatically distribute to the GPU.
