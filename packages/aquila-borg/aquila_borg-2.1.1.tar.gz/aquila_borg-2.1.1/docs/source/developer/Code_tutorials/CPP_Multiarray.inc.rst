.. _multi_dimensional_array_management:

Multi-dimensional array management
==================================

Allocating arrays
-----------------

There are several ways of allocating multidimensional arrays dependent
on the effect that wants to be achieved.

.. _for_use_with_fftwmpi:

For use with FFTW/MPI
~~~~~~~~~~~~~~~~~~~~~

It is **strongly** recommended to use the class ``FFTW_Manager<T,N>``
(see documentation :ref:`here <fftw_manager>`, most of BORG is used assuming
that you have T=double, N=3; for 3D) to allocate arrays as the MPI and
FFTW needs some specific padding and over-allocation of memory which are
difficult to get right at first. Assuming ``mgr`` is such an object then
you can allocate an array like this:

.. code:: c++

      auto array_p = mgr.allocate_array();
      auto& a = array_p.get_array();
      
      // a is now a boost::multi_array_ref
      for (int i = a0; i < a1; i++)
        for (int j = b0; j < b1; j++)
          for (int k = c0; k < c1; k++)
            std::cout << "a has some value " << a[i][j][k] << std::endl;

With the above statement, keep in mind that the array will be destroyed
at the **exit of the context**. It is possible to have more permanent
arrays with the following statement:

.. code:: c++

      auto array_p = mgr.allocate_ptr_array();
      auto& a = array_p->get_array();
      
      // array_p is a shared_ptr that can be saved elsewhere
      // a is now a boost::multi_array_ref

.. _uninitialized_array:

Uninitialized array
~~~~~~~~~~~~~~~~~~~

Generally it is advised to allocate the array with the type
``LibLSS::U_Array<T,N>``. It creates an array that is a much faster to
initialize and statistics on memory allocation is gathered.

The typical usage is the following:

.. code:: c++

      using namespace LibLSS;
      
      U_Array<double, 2> x_p(boost::extents[N][M]);
      auto&x = x_p.get_array();

The line with ``U_Array`` will allocate the array (at the same time
gathering the statistics), the second line provides with you a
``boost::multi_array_ref`` object that can directly access all elements
as usual (see previous section).

.. _dumping_an_array_of_scalars:

Dumping an array of scalars
---------------------------

A significant amount of abstraction has been coded in to dump arrays
into HDF5 file the most painless possible. Typically to dump an array
you would have the following code.

.. code:: c++

   #include <H5Cpp.h>
   #include <CosmoTool/hdf5_array.hpp>
   #include <boost/multi_array.hpp>

   void myfunction() {
      boost::multi_array<double, 2> a(boost::extents[10][4]);

      // Do some initialization of a

      {
        // Open and truncate myfile.h5 (i.e. removes everything in it)
        H5::H5File f("myfile.h5", H5F_ACC_TRUNC);
        // Save 'a' into the dataset "myarray" in the file f.
        CosmoTool::hdf5_write_array(f, "myarray", a);
      }
   }

But you need to have your array either be a multi_array or mapped to it
through multi_array_ref. Usual types (float, double, int, ...) are
supported, as well as complex types of. There is also a mechanism to
allow for the

.. _fuse_array_mechanism:

FUSE array mechanism
--------------------

The FUSE subsystem is made available through the includes
libLSS/tools/fused_array.hpp, libLSS/tools/fuse_wrapper.hpp. They define
wrappers and operators to make the writing of expressions on array
relatively trivial, parallelized and possibly vectorized if the arrays
permit. To illustrate this there are two examples in the library of
testcases: test_fused_array.cpp and test_fuse_wrapper.cpp.

We will start from a most basic example:

.. code:: c++

     boost::multi_array<double, 1> a(boost::extents[N]);
     auto w_a = LibLSS::fwrap(a);

     w_a = 1;

These few lines create a one dimensional array of length N. Then this
array is wrapped in the seamless FUSE expression system. It is quite
advised to use auto here as the types can be complex and difficult to
guess for newcomers. Finally, the last line fills the array with value
1. This is a trivial example but we can do better:

.. code:: c++

     w_a = std::pow(std::cos(w_a*2*M_PI), 2);

This transforms the content of a by evaluating :math:`cos(2\pi x)^2` for
each element :math:`x` of the array wrapped in w_a. This is done without
copy using the lazy expression mechanism. It is possiible to save the
expression for later:

.. code:: c++

     auto b = std::pow(std::cos(w_a*2*M_PI), 2);

Note that nothing is evaluated. This only occurs at the assignment
phase. This wrap behaves also mostly like a virtual array:

.. code:: c++

    (*b)[i]

accesses computes the i-th value of the expression and nothing else.

Some other helpers in the libLSS supports natively the fuse mechanism.
That is the case for ``RandomNumber::poisson`` for example:

.. code:: c++

     auto c = fwrap(...);
     c = rgen.poisson(b);

This piece of code would compute a poisson realization for a mean value
given by the element of the ``b`` expression (which must be a wrapped
array or one expression of it) and stores this into ``c``.

The ``sum`` reduce (parallel reduction) operation is supported by the
wrapper:

.. code:: c++

     double s = c.sum();

Some arrays could be entirely virtual, i.e. derived from C++
expressions. This needs to invoke a lower layer of the FUSE mechanism.
Creating a pure virtual array looks like that:

.. code:: c++

     auto d = LibLSS::fwrap(LibLSS::b_fused_idx<double, 2>(
        [](size_t i, size_t j)->double {
          return sqrt(i*i + j*j);
        }
     ));

This operation creates a virtual array and wraps it immediately. The
virtual array is a double bidimensional array (the two template
parameters), and infinite. Its element are computed using the provided
lambda function, which obligatorily takes 2 parameters. It is possible
to make finite virtual arrays by adding an extent parameter:

.. code:: c++

     auto d = LibLSS::fwrap(LibLSS::b_fused_idx<double, 2>(
        [](size_t i, size_t j)->double {
          return sqrt(i*i + j*j);
        },
        boost::extents[N][N]
     ));

Only in that case it is possible to query the dimension of the array.

Finally **FUSED mechanism does not yet support automatic dimensional
broadcast!**
