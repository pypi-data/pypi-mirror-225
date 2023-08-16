/*+
    ARES/HADES/BORG Package -- ./extra/python/python/pyborg.hpp
    Copyright (C) 2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_PYTHON_BASE_HPP
#  define __LIBLSS_PYTHON_BASE_HPP

#  include <pybind11/pybind11.h>
#  include <boost/any.hpp>

namespace LibLSS {
  namespace Python {
    namespace py = pybind11;

    void setupConsole();
    void bindBORG(py::module m);
    void pyBase(py::module m);
    void pyCosmo(py::module m);
    void pyLikelihood(py::module m);
    void pyForwardBase(py::module m);
    void pyForwardBorg(py::module m);
    void pyForwardAll(py::module m);
    void pyBias(py::module m);
    void pyVelocity(py::module m);
    void pySamplers(py::module m);

    void shuttingDown();

    py::object any_to_python(boost::any &a);
    boost::any python_to_any(py::object o);

    extern bool mpi4py_available;
  } // namespace Python
} // namespace LibLSS

#endif

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019
