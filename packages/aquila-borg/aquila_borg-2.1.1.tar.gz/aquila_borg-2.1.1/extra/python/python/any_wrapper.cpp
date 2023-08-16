/*+
    ARES/HADES/BORG Package -- ./extra/python/python/any_wrapper.cpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/console.hpp"

#include <memory>
#include <exception>
#include <boost/format.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/eval.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include "pyborg.hpp"
#include "pyfuse.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"

using namespace LibLSS;
namespace py = pybind11;

using namespace LibLSS;

template <typename A, size_t... I>
auto extents_from_numpy(A const &a, std::integer_sequence<size_t, I...>) {
  return array::extent((size_t)a.shape(I)...);
}

struct basic_any_converter {
  virtual py::object load(boost::any &) const = 0;
  virtual boost::any store(py::object) const = 0;
};

template <typename T>
struct any_scalar_converter : basic_any_converter {
  static basic_any_converter *instance() {
    static any_scalar_converter<T> obj;
    return &obj;
  }
  py::object load(boost::any &e) const override {
    T value = boost::any_cast<T>(e);
    return py::cast(value);
  }
  boost::any store(py::object obj) const override {
    return boost::any(obj.cast<T>());
  }
};

template <typename T>
struct any_array_converter : basic_any_converter {
  static basic_any_converter *instance() {
    static any_array_converter<T> obj;
    return &obj;
  }
  py::object load(boost::any &e) const override {
    T array = boost::any_cast<T>(e);
    typedef typename T::element element;

    std::array<ssize_t, T::dimensionality> shapes, strides;
    std::copy(array.shape(), array.shape() + shapes.size(), shapes.begin());
    for (int i = 0; i < strides.size(); i++)
      strides[i] = array.strides()[i] * sizeof(element);
    return py::array_t<element>(shapes, strides, array.data());
  }
  boost::any store(py::object obj) const override {
    py::array_t<typename T::element> a = obj;
    auto a_u = a.template unchecked<T::dimensionality>();

    T tmp(extents_from_numpy(
        a_u, std::make_integer_sequence<size_t, T::dimensionality>()));
    Python::PyToFuseArray<typename T::element, T::dimensionality, false>
        mapped_array(a_u);

    fwrap(tmp) = mapped_array;
    return boost::any(tmp);
  }
};

struct any_to_python_impl {
private:
  typedef std::map<std::type_index, basic_any_converter *> Map;
  typedef std::map<std::tuple<int, char>, basic_any_converter *> InvMap;
  Map any_converter;
  InvMap inv_converter;

  any_to_python_impl() {
    any_converter[typeid(bool)] = any_scalar_converter<bool>::instance();
    any_converter[typeid(size_t)] = any_scalar_converter<size_t>::instance();
    any_converter[typeid(double)] = any_scalar_converter<double>::instance();
    any_converter[typeid(boost::multi_array<size_t, 1>)] =
        any_array_converter<boost::multi_array<size_t, 1>>::instance();
    any_converter[typeid(LibLSS::multi_array<double, 1>)] =
        any_array_converter<LibLSS::multi_array<double, 1>>::instance();
    any_converter[typeid(boost::multi_array<double, 1>)] =
        any_array_converter<boost::multi_array<double, 1>>::instance();
    any_converter[typeid(boost::multi_array<size_t, 2>)] =
        any_array_converter<boost::multi_array<size_t, 2>>::instance();
    any_converter[typeid(boost::multi_array<double, 2>)] =
        any_array_converter<boost::multi_array<double, 2>>::instance();
    any_converter[typeid(boost::multi_array<size_t, 3>)] =
        any_array_converter<boost::multi_array<size_t, 3>>::instance();
    any_converter[typeid(boost::multi_array<double, 3>)] =
        any_array_converter<boost::multi_array<double, 3>>::instance();
    inv_converter[std::make_tuple(0, 'u')] =
        any_scalar_converter<size_t>::instance();
    inv_converter[std::make_tuple(0, 'f')] =
        any_scalar_converter<double>::instance();
    inv_converter[std::make_tuple(1, 'u')] =
        any_array_converter<boost::multi_array<size_t, 1>>::instance();
    inv_converter[std::make_tuple(1, 'f')] =
        any_array_converter<boost::multi_array<double, 1>>::instance();
    inv_converter[std::make_tuple(2, 'u')] =
        any_array_converter<boost::multi_array<size_t, 2>>::instance();
    inv_converter[std::make_tuple(2, 'f')] =
        any_array_converter<boost::multi_array<double, 2>>::instance();
    inv_converter[std::make_tuple(3, 'u')] =
        any_array_converter<boost::multi_array<size_t, 3>>::instance();
    inv_converter[std::make_tuple(3, 'f')] =
        any_array_converter<boost::multi_array<double, 3>>::instance();
  }

public:
  static any_to_python_impl *instance() {
    static any_to_python_impl cvt;
    return &cvt;
  }

  py::object a2p(boost::any &a) {
    if (a.empty())
      return py::none();
    Map::iterator iter = any_converter.find(a.type());

    if (iter == any_converter.end())
      throw std::runtime_error("Unknown stored type.");
    return iter->second->load(a);
  }

  boost::any p2a(py::object o) {
    basic_any_converter *cvt = 0;

    // Handle array objects
    if (py::isinstance<py::array>(o)) {
      py::array a = o;
      auto iter =
          inv_converter.find(std::make_tuple(a.ndim(), a.dtype().kind()));
      if (iter == inv_converter.end())
        throw std::runtime_error("Unknown type to store.");
      cvt = iter->second;
    } else if (py::isinstance<py::bool_>(o)) {
      cvt = any_scalar_converter<bool>::instance();
    } else if (py::isinstance<py::float_>(o)) {
      cvt = any_scalar_converter<double>::instance();
    } else if (py::isinstance<py::int_>(o)) {
      cvt = any_scalar_converter<size_t>::instance();
    } else {
      throw std::runtime_error("Unknown type to store.");
    }

    return cvt->store(o);
  }
};

py::object LibLSS::Python::any_to_python(boost::any &a) {
  return any_to_python_impl::instance()->a2p(a);
}

boost::any LibLSS::Python::python_to_any(py::object o) {
  return any_to_python_impl::instance()->p2a(o);
}

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
