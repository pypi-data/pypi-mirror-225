/*+
    ARES/HADES/BORG Package -- ./extra/python/python/bind.cpp
    Copyright (C) 2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/mpi/generic_mpi.hpp"
#include <memory>
#include <exception>
#include <boost/format.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "pyborg.hpp"
#include "pyfuse.hpp"

namespace py = pybind11;
namespace lss = LibLSS;

bool LibLSS::Python::mpi4py_available = false;

void LibLSS::Python::bindBORG(py::module m) {
  py::module cosmo = m.def_submodule("cosmo", "Submodule for cosmology");
  py::module forward =
      m.def_submodule("forward", "Base declaration for forward models");
  py::module forward_impl =
      forward.def_submodule("models", "Implementation of forward models");
  py::module bias = m.def_submodule("bias", "Bias models");
  py::module velocity =
      forward.def_submodule("velocity", "Velocity forward models");
  py::module likelihood = m.def_submodule("likelihood", "Likelihoods");
  py::module samplers = m.def_submodule("samplers", "Submodule for samplers algorithm and specifics");

  py::class_<pythonHolder, std::shared_ptr<pythonHolder>>(m, "_pythonPointerHolder");

  lss::Python::pyBase(m);
  lss::Python::pyCosmo(cosmo);
  lss::Python::pyForwardBase(forward);
  lss::Python::pyForwardBorg(forward_impl);
  lss::Python::pyForwardAll(forward_impl);
  lss::Python::pyBias(bias);
  lss::Python::pyVelocity(velocity);
  lss::Python::pyLikelihood(likelihood);
  lss::Python::pySamplers(samplers);
}
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019
