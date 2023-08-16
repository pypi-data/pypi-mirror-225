/*+
    ARES/HADES/BORG Package -- ./extra/python/python/_borg.cpp
    Copyright (C) 2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/mpi/generic_mpi.hpp"
#include <memory>
#include <dlfcn.h>
#include <cstring>
#include <cstdlib>
#include <exception>
#include <boost/format.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#if defined(ARES_MPI_FFTW)
#  include <CosmoTool/fourier/fft/fftw_calls_mpi.hpp>
#endif
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/cpu/feature_check.hpp"
#include "pyborg.hpp"

namespace py = pybind11;
namespace lss = LibLSS;

namespace {

#if defined(ARES_MPI_FFTW)
  lss::RegisterStaticInit reg0(fftw_mpi_init, fftw_mpi_cleanup, 9, "MPI/FFTW");
#endif
  // WISDOM must come at the end. Otherwise it is reset
  lss::RegisterStaticInit reg1(
      CosmoTool::init_fftw_wisdom, CosmoTool::save_fftw_wisdom, 12,
      "FFTW/WISDOM");
#if !defined(ARES_MPI_FFTW) &&                                                 \
    defined(                                                                   \
        _OPENMP) // Do not use MPI and Threaded FFTW at the same time for the moment.
  lss::RegisterStaticInit
      reg2(fftw_init_threads, fftw_cleanup_threads, 11, "FFTW/THREADS");
#endif
} // namespace

static void finalize() {
  LibLSS::Python::shuttingDown();
  lss::StaticInit::finalize();
}

template <typename Signature>
static std::function<Signature> cast(void *f) {
  return reinterpret_cast<Signature *>(f);
}

static void build_argc_argv(int &argc, char **&argv) {
  auto sys = py::module::import("sys");
  py::list py_argv = sys.attr("argv");
  argc = 0;
  argv = (char **)::malloc(sizeof(char *) * (py_argv.size()+1));
  for (auto &o : py_argv) {
    std::string s = py::cast<std::string>(o);
    argv[argc++] = ::strdup(s.c_str());
  }
  argv[argc] = 0;
  // Remove all arguments from the argv list.
  py_argv.attr("clear")();
}

void free_argc_argv(int &argc, char **&argv) {
  auto sys = py::module::import("sys");
  py::list py_argv = sys.attr("argv");
  for (int i = 0; i < argc; i++) {
    py_argv.append(argv[i]);
    free(argv[i]);
  }
  free(argv);
}

PYBIND11_MODULE(_borg, m) {
  m.doc() = "ARES/BORG python binding module"; // optional module docstring

  lss::Python::setupConsole();
  bool foundMPI4PY = true;

  // Try to access mpi4py
#if defined(ARES_MPI_FFTW)
  try {
    py::module mpi4py = py::module::import("mpi4py.MPI");

    m.attr("_mpi_addressof") = mpi4py.attr("_addressof");
    if (LibLSS::MPI_IS_REAL) {
      lss::setupMPI((MPI_Comm)(py::cast<long long>(
          mpi4py.attr("_handleof")(mpi4py.attr("COMM_WORLD")))));
      lss::Python::mpi4py_available = true;
    }
  } catch (py::error_already_set &) {
    // Ignore mpi4py errors.
    // Print a warning though
    foundMPI4PY = false;
    lss::Python::mpi4py_available = false;
    int argc;
    char **argv;
    // This hack is for IntelMPI. Shame on you.
    build_argc_argv(argc, argv);
    lss::setupMPI(argc, argv);
    free_argc_argv(argc, argv);
  }
#endif
  lss::StaticInit::execute();
#if defined(ARES_MPI_FFTW)
  if (foundMPI4PY)
    lss::Console::instance().print<lss::LOG_INFO>("Found MPI4PY.");
  else
    lss::Console::instance().print<lss::LOG_INFO>(
        "Not Found MPI4PY. Starting without MPI.");
#endif

  {
    std::string cpu_features;
    auto &cons = lss::Console::instance();
    bool result = lss::check_compatibility(cpu_features);
    cons.format<lss::LOG_INFO>("CPU features: %s", cpu_features);
    if (!result) {
      cons.print<lss::LOG_ERROR>(
          "Binary is incompatible with your CPU. Stop here.");
      lss::MPI_Communication::instance()->abort();
      return;
    }
  }

  lss::Python::bindBORG(m);

  // Register LSS cleanup
  Py_AtExit(finalize);
  /*  auto atexit = py::module::import("atexit");
  atexit.attr("register")(
      py::cpp_function([]() { lss::StaticInit::finalize(); }));*/
}
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019
