#cython: language_level=3
import numpy as np
cimport numpy as np

np.import_array()
np.import_ufunc()

cdef extern from "sys/types.h":
   ctypedef np.int64_t int64_t

cdef extern from "numpy/npy_common.h":
   ctypedef npy_intp

cdef extern from "special_math.hpp" namespace "CosmoTool":
   T log_modified_bessel_first_kind[T](T v, T z) nogil except +

cdef extern from "numpy_adaptors.hpp" namespace "CosmoTool":
   void parallel_ufunc_dd_d[T,IT](char **args, IT* dimensions, IT* steps, void *func)


cdef np.PyUFuncGenericFunction loop_func[1]
cdef char input_output_types[3]
cdef void *elementwise_funcs[1]

loop_func[0] = <np.PyUFuncGenericFunction>parallel_ufunc_dd_d[double,npy_intp]

input_output_types[0] = np.NPY_DOUBLE
input_output_types[1] = np.NPY_DOUBLE
input_output_types[2] = np.NPY_DOUBLE

elementwise_funcs[0] = <void*>log_modified_bessel_first_kind[double]

log_modified_I = np.PyUFunc_FromFuncAndData(
    loop_func,
    elementwise_funcs,
    input_output_types,
    1, # number of supported input types
    2, # number of input args
    1, # number of output args
    0, # `identity` element, never mind this
    "log_modified_bessel_first_kind", # function name
    "log_modified_bessel_first_kind(v: Float, z: Float) -> Float", # docstring
    0 # unused
    )

