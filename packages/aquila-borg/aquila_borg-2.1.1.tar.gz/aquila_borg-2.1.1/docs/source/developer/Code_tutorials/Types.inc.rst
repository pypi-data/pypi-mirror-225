.. _ares_types:

Types used in the ARES code
===========================

A lot of the useful type 'aliases' are actually defined in ``libLSS/samplers/core/types_samplers.hpp``. We can
discuss a few of those types here.

LibLSS::multi_array
-------------------

.. code:: c++

   template<typename T, size_t N>
   using multi_array = boost::multi_array<T, N, LibLSS::track_allocator<T>>;

This is a type alias for boost::multi_array which uses the default
allocator provided by LibLSS to track allocation. It is advised to use
it so that it is possible to investigate memory consumption
automatically in future. It is perfectly legal not to use it, however
you will those features in your report.

LibLSS::ArrayType
-----------------

This is a type to hold, and store in MCMC file, 3d array targeted to be
used in FFT transforms. The definition is

.. code:: c++

   typedef ArrayStateElement<double, 3, FFTW_Allocator<double>, true > ArrayType;

It happens that ArrayType is misnamed as it is only a shell for the
type. In future, we can expect it to be renamed to something else like
ArrayTypeElement (or something else). We can see that it is a double
array, with 3 dimensions. It requires an FFTW_Allocator and it is a
spliced array to be reconstructed for mcmc files (last 'true').

Allocating the element automatically requires the array to be allocated
at the same time. An example for that is as follow:

.. code:: c++

   s_field =new ArrayType(extents[range(startN0,startN0+localN0)][N1][N2], allocator_real);
   s_field->setRealDims(ArrayDimension(N0, N1, N2));

To access to the underlying `multi_array` one needs to access to the member variable `array`. In the case of the above `s_field`, it would be:

.. code:: c++

   auto& my_array = *s_field->array;
   // Now we can access the array
   std::cout << my_array[startN0][0][0] << std::endl;

.. warning::

   Do not store a pointer to the above `my_array`. The array member variable
   is a shared pointer which can be safely stored with the following type
   `std::shared_ptr<LibLSS::ArrayType::ArrayType>`.


LibLSS::CArrayType
------------------

This is a type to hold, and store in MCMC file, 3d complex array
targeted to be used in FFT transforms. The definition is

.. code:: c++

   typedef ArrayStateElement<std::complex<double>, 3, FFTW_Allocator<std::complex<double> >, true > CArrayType;

It happens that ArrayType is misnamed as it is only a shell for the
type. In future, we can expect it to be renamed to something else like
CArrayTypeElement (or something else). We can see that it is a double
array, with 3 dimensions. It requires an FFTW_Allocator and it is a
spliced array to be reconstructed for mcmc files (last 'true').

Allocating the element automatically requires the array to be allocated
at the same time. An example for that is as follow:

.. code:: c++

   s_hat_field = new CArrayType(base_mgr->extents_complex(), allocator_complex);
   s_hat_field->setRealDims(ArrayDimension(N0, N1, N2_HC));

LibLSS::Uninit_FFTW_Complex_Array
---------------------------------

The types above are for arrays designated to be saved in MCMC file. To
allocator \*temporary\* arrays that still needs to be run through FFTW,
the adequate type is:

.. code:: c++

   typedef UninitializedArray<FFTW_Complex_Array, FFTW_Allocator<std::complex<double> > > Uninit_FFTW_Complex_Array;

This is a helper type because

.. code:: c++

   boost::multi_array

wants to do **slow** preinitialization of the large array that we use.
To circumvent the uninitialization the trick is to create a

.. code:: c++

   boost::multi_array_ref

on a memory allocated by an helper class. UninitializedArray is built
for that however it comes at the cost of adding one step before using
the array:

.. code:: c++

   Uninit_FFTW_Complex_Array gradient_psi_p(extents[range(startN0,startN0+localN0)][N1][N2_HC],
                                              allocator_complex);
   Uninit_FFTW_Complex_Array::array_type& gradient_psi = gradient_psi_p.get_array();

Here 'gradient_psi_p' is the holder of the array (i.e. if it gets
destroyed, the array itself is destroyed). But if you want to use the
array you need to first get it with 'get_array'.
