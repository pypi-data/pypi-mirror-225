/*+
    ARES/HADES/BORG Package -- ./extra/python/python/base.cpp
    Copyright (C) 2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <pybind11/stl.h>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/memusage.hpp"

#include "pyborg.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

static int pythonVerboseLevel = 3;

#include "pyborg_doc.hpp"
#include "pyborg_doc/borg_base.hpp"
#include "pyborg_doc/borg_base.Console.hpp"

void LibLSS::Python::shuttingDown() {
  pythonVerboseLevel = -pythonVerboseLevel;
}

void LibLSS::Python::setupConsole() {
  Console::instance().setVerboseLevel(0);
  Console::instance().setSeparateStream([](int level, std::string const &m) {
    if (level < pythonVerboseLevel) {
      py::gil_scoped_acquire acquire;
      py::print(m);
    } else if (pythonVerboseLevel < 0) {
      if (level < -pythonVerboseLevel) {
        std::cout << m << std::endl;
      }
    }
  });
}

void LibLSS::Python::pyBase(py::module m) {

  py::class_<Console>(m, "Console", DOC(borg_base, Console))
      .def(
          "print_warning",
          [](Console *c, std::string const &s) { c->print<LOG_WARNING>(s); })
      .def(
          "print_std",
          [](Console *c, std::string const &s) { c->print<LOG_STD>(s); },
          DOC(borg_base, Console, print_std))
      .def(
          "print_debug",
          [](Console *c, std::string const &s) { c->print<LOG_DEBUG>(s); })
      .def(
          "print_error",
          [](Console *c, std::string const &s) { c->print<LOG_ERROR>(s); })
      .def(
          "setVerboseLevel",
          [](Console *c, int level) { pythonVerboseLevel = level; },
          "level"_a = 2)
      .def("printStackTrace", &Console::print_stack_trace)
      .def(
          "outputToFile", &Console::outputToFile,
          DOC(borg_base, Console, outputToFile));

  m.def(
      "console", []() -> Console * { return &Console::instance(); },
      py::return_value_policy::reference, DOC(borg_base, console));

  py::class_<AllocationDetail>(m, "_memoryDetail")
      .def_readonly("allocated", &AllocationDetail::allocated)
      .def_readonly("freed", &AllocationDetail::freed)
      .def_readonly("peak", &AllocationDetail::peak)
      .def("__repr__", [](AllocationDetail *detail) {
        return boost::str(
            boost::format("<AllocationDetail: allocated=%g kB, freed=%g kB, "
                          "peak=%g kB>") %
            (detail->allocated / 1024.) % (detail->freed / 1024.) %
            (detail->peak / 1024.));
      });

  m.def("memoryReport", &memoryReport);
}
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019
