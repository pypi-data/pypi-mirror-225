Code tutorials
##############

.. include:: Code_tutorials/Types.inc.rst

.. include:: Code_tutorials/FFTW_manager.inc.rst

.. _reading_in_meta_parameters_and_arrays:

Reading in meta-parameters and arrays
=====================================

If one wishes to access the the content of ARES MCMC files in C++,
functions are available in CosmoTool and LibLSS. For example:

.. code:: c++

   #include <iostream>
   #include <boost/multi_array.hpp> //produce arrays
   #include "CosmoTool/hdf5_array.hpp" //read h5 atributes as said arrays
   #include "libLSS/tools/hdf5_scalar.hpp" //read h5 attributes as scalars
   #include <H5Cpp.h> //access h5 files

   using namespace std;
   using namespace LibLSS;

   int main()
   {
       typedef  boost::multi_array<double, 3> array3_type;
       
       //access mcmc and restart files 
       H5::H5File meta("restart.h5_0", H5F_ACC_RDONLY);
       H5::H5File f("mcmc_0.h5", H5F_ACC_RDONLY);
       
       //read the number of pixels of the cube as integrer values (x,y,z)
       int N0 = LibLSS::hdf5_load_scalar<int>(meta, "scalars/N0");
       int N1 = LibLSS::hdf5_load_scalar<int>(meta, "scalars/N1");
       int N2 = LibLSS::hdf5_load_scalar<int>(meta, "scalars/N2");
       
       array3_type density(boost::extents[N0][N1][N2]);
       
       //read the density field as a 3d array
       CosmoTool::hdf5_read_array(f, "scalars/s_field", density);
   }

.. _obtaining_timing_statistics:

Obtaining timing statistics
===========================

By default the statistics are not gathered. It is possible (and advised
during development and testing) to activate them through a build.sh
option ``--perf``. In that case, each "ConsoleContext" block is timed
separately. In the C++ code, a console context behaves like this:

.. code:: c++

   /* blabla */
   {
     LibLSS::ConsoleContext<LOG_DEBUG> ctx("costly computation");

     /* Computations */
     ctx.print("Something I want to say");
   } /* Exiting context */
   /* something else */

Another variant that automatically notes down the function name and the
filename is

.. code:: c++

   /* blabla */
   {
      LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
     /* Computations */
     ctx.print("Something I want to say");
   } /* Exiting context */
   /* something else */

A timer is started at the moment the ConsoleContext object is created.
The timer is destroyed at the "Exiting context" stage. The result is
marked in a separate hash table. Be aware that in production mode you
should turn off the performance measurements as they take time for
functions that are called very often. You can decide on a log level
different than LOG_DEBUG (it can be LOG_VERBOSE, LOG_INFO, ...), it is
the default level for any print call used with the context.

The string given to console context is used as an identifier, so please
use something sensible. At the moment the code gathering performances is
not aware of how things are recursively called. So you will only get one
line per context. Once you have run an executable based on libLSS it
will produce a file called "timing_stats.txt" in the current working
directory. It is formatted like this:

.. code:: text

   Cumulative timing spent in different context
   --------------------------------------------
   Context,   Total time (seconds)

                             BORG LPT MODEL        2       0.053816
                      BORG LPT MODEL SIMPLE        2       0.048709
                         BORG forward model        2       0.047993
                     Classic CIC projection        2       0.003018
   (...)

It consists in three columns, separated by a tab. The first column is
the name of the context. The second column is the number of times this
context has been called. The last and third column is the cumulative
time taken by this context, in seconds. At the moment the output is not
sorted but it may be in future. You want the total time to be as small
as possible. This time may be large for two reasons: you call the
context an insane amount of time, or you call it a few times but each
one is very costly. The optimization to achieve is then up to you.


.. include:: Code_tutorials/CPP_Multiarray.inc.rst


MPI tools
=========

Automatic particle exchange between MPI tasks
---------------------------------------------

It is often useful for code doing N-body simulations to exchange the
ownership of particles and all their attributes. The BORG submodule has
a generic framework to handle these cases. It is composed of the
following parts:

-  a ``BalanceInfo`` structure (in
   ``libLSS/physics/forwards/particle_balancer/particle_distribute.hpp``)
   which holds temporary information required to do the balancing, and
   eventually undo it for adjoint gradients. It has an empty constructor
   and a special function ``allocate`` which must take an MPI
   communicator and the amount of particles that are to be considered
   (including extra buffering).
-  generic distribute / undistribute functions called respectively
   ``particle_redistribute`` and ``particle_undistribute``.
-  a generic attribute management system to remove buffer copies.

We can start from an example taken from ``test_part_swapper.cpp``:

.. code:: c++

   BalanceInfo info;
   NaiveSelector selector;
   boost::multi_vector<double, 2> in_positions;
   size_t numRealPositions, Nparticles;

   /* Fill in_positions... */

   info.allocate(comm, Nparticles);

   info.localNumParticlesBefore = numRealPositions;
   particle_redistribute(info, in_positions, selector);
   /* info.localNumParticlesAfter is filled */

In the code above all the initializations are skipped. The load balancer
is initialized with ``allocate``. Then the actual number of particles
that is really used in the input buffer is indicated by filling
``localNumParticlesBefore``. Then ``particle_redistribute`` is invoked.
The particles may be completely reshuffled in that operation. The real
number of viable particles is indicated in ``localNumParticlesAfter``.
Finally, but importantly, the balancing decision is taken by
``selector``, which at the moment must be a functor and bases its
decision on the position alone. In future it is possible to use an
attribute instead.

Now it is possible to pass an arbitrary number of attributes, living in
separate array-like objects. The example is similar as previously:

.. code:: c++

   BalanceInfo info;
   NaiveSelector selector;
   boost::multi_vector<double, 2> in_positions;
   boost::multi_vector<double, 2> velocities;
   size_t numRealPositions, Nparticles;

   /* Fill in_positions... */

   info.allocate(comm, Nparticles);

   info.localNumParticlesBefore = numRealPositions;
   particle_redistribute(info, in_positions, selector,
         make_attribute_helper(Particles::vector(velocities))
   );
   /* info.localNumParticlesAfter is filled */

The code will allocate automatically a little amount of temporary memory
to accommodate for I/O operations. Two kind of attribute are supported
by default, though it is extendable by creating new adequate classes:

-  scalar: a simple 1d array of single elements (float, double, whatever
   is supported by the automatic MPI translation layer and does not rely
   on dynamic allocations).
-  vector: a simple 2d array of the shape Nx3 of whatever elements
   supported by the automatic MPI translation layer.

.. _ghost_planes:

Ghost planes
------------

The BORG module has a special capabilities to handle ghost planes, i.e.
(N-1)d-planes of a Nd cube that are split for MPI work. This happens
typically when using FFTW for which only a slab of planes are available
locally and the code needs some other information from the other planes
to do local computation. An example of this case is the computation of
gradient: one needs one extra plane at each edge of the slab to be able
to compute the gradient. The ghost plane mechanism tries to automate the
boring part of gathering information and eventually redistributing the
adjoint gradient of that same operation. The header is
``libLSS/tools/mpi/ghost_planes.hpp`` and is exporting one templated
structure:

.. code:: c++

   template<typename T, size_t Nd>
   struct GhostPlanes: GhostPlaneTypes<T, Nd> {
     template<typename PlaneList,typename PlaneSet, typename DimList>
     void setup(
         MPI_Communication* comm_,
         PlaneList&& planes, PlaneSet&& owned_planes,
         DimList&& dims,
         size_t maxPlaneId_);

      void clear_ghosts();

      template<typename T0, size_t N>
      void synchronize(boost::multi_array_ref<T0,N> const& planes);

      template<typename T0, size_t N>
      void synchronize_ag(boost::multi_array_ref<T0,N>& ag_planes);

      ArrayType& ag_getPlane(size_t i);
      ArrayType& getPlane(size_t i);
   };

Many comments are written in the code. Note that ``Nd`` above designate
the number of dimension for a **plane**. So if you manipulate 3d-boxes,
you want to indicate ``Nd=2``. The typical work flow of using
ghostplanes is the following:

-  GhostPlanes object creation
-  call setup method to indicate what are the provided data and
   requirements
-  do stuff
-  call synchronize before needing the ghost planes
-  use the ghost planes with getPlane()
-  Repeat synchronize if needed

There is an adjoint gradient variant of the synchronization step which
does sum reduction of the adjoint gradient arrays corresponding to the
ghost planes.

An example C++ code is

.. code:: c++

   std::vector<size_t> here_planes{/* list of the planes that are on the current MPI node */};
   std::vector<size_t> required_planes{/* list of the  planes that you need to do computation on this node */};
   ghosts.setup(comm, required_planes, here_planes, std::array<int,2>{128,128} /* That's the dimension of the plane, here 2d */, 64 /* That's the total number of planes over all nodes */);

   /* A is a slab with range in [startN0,startN0+localN0]. This function will synchronize the data over all nodes. */
   ghosts.synchronize(A);
     
   /* ghosts.getPlane(plane_id) will return a 2d array containing the data of the ghost plane 'plane_id'. Note that the data of A are not accessible through that function. */


The ``synchronize`` and ``synchronize_ag`` accepts an optional argument
to indicate what kind of synchronization the user wants. At the moment
two synchronization are supported GHOST_COPY and GHOST_ACCUMULATE.
GHOST_COPY is the classic mode, which indicates the missing planes has
to be copied from a remote task to the local memory. It specified that
the adjoint gradient will accumulate information from the different
tasks. Note that the array ``A`` is a slab. It means that if you do not use
the FFTW helper mechanism you should allocate it using the following
pattern for 3d arrays

.. code:: c++

   // Some alias for convenience
   using boost::extents;
   typedef boost::multi_array_types::extent_range e_range;

   /* To use a classical multi_array allocation, may be slow */
   boost::multi_array<double, 2> A(extents[e_range(startN0, localN0)][N1][N2]);

   /* To allocate using the uninitialized array mechanism */
   U_Array A_p(extents[e_range(startN0, localN0)][N1][N2]);
   auto& A = A_p.get_array();
   // Note that A_p is destroyed at the end of the current context if you
   // use that.

   /* To allocate using the uninitialized array mechanism, and shared_ptr */
   std::shared_ptr<U_Array> A_p = std::make_shared<U_Array>(extents[e_range(startN0, localN0)][N1][N2]);
   auto& A = A_p->get_array();

   // If A_p is transferred somewhere else, then it will not be deallocated.

For 2d arrays, just remove one dimension in all the above code.

The use of the adjoint gradient part is very similar

.. code:: c++

   ghosts.clear_ghosts();

   /* declare gradient, fill up with the local information on the slab */
   /* if there is information to deposit on 'plane' use the special array as follow*/
   ghosts.ag_getPlane(plane)[j][k] = some_value;

   /* finish the computation with synchronize_ag, the gradient will compute  */
   ghosts.synchronize_ag(gradient);

   /* now the gradient holds the complete gradient that must resides on the local slab and the computation may continue */

You can check ``extra/borg/libLSS/samplers/julia/julia_likelihood.cpp``
for a more detailed usage for the Julia binding. This tool is also used
by the ManyPower bias model though in a much more complicated fashion
(``extra/borg/libLSS/physics/bias/many_power.hpp``).

.. include:: Code_tutorials/Julia_and_TensorFlow.inc.rst

.. include:: Code_tutorials/New_core_program.inc.rst
.. 
.. include:: Code_tutorials/Adding_a_new_likelihood_in_C++.inc.rst



Adding a new likelihood/bias combination in BORG
================================================

*To be written...*

Useful resources
================

-  `Google code of conduct in C++ <https://google.github.io/styleguide/cppguide.html>`__
