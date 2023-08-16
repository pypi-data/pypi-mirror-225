/*+
    ARES/HADES/BORG Package -- ./extra/python/python/py_mpi.hpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PYTHON_MPI_HPP
#  define __LIBLSS_PYTHON_MPI_HPP

#  include "libLSS/mpi/generic_mpi.hpp"
#  include "pyborg.hpp"

namespace LibLSS {
  namespace Python {
    static inline py::object makePythonMPI(MPI_Communication *comm) {
      if (!MPI_IS_REAL)
        return py::none();
      auto mpi_mod = py::module::import("mpi4py.MPI");
      py::object m4py_comm = mpi_mod.attr("Comm")();
      auto m4py_ptr = (MPI_Comm *)(py::cast<long long>(
          mpi_mod.attr("_addressof")(m4py_comm)));
      *m4py_ptr = comm->comm();
      return m4py_comm;
    }

    static inline std::shared_ptr<MPI_Communication>
    makeMPIFromPython(py::object pycomm) {
      if (!MPI_IS_REAL)
        return std::shared_ptr<MPI_Communication>(
            MPI_Communication::instance(), [](void*) {});
      auto mpi_mod = py::module::import("mpi4py.MPI");
      auto m4py_ptr = (MPI_Comm *)(py::cast<long long>(
          mpi_mod.attr("_addressof")(pycomm)));
      return std::make_shared<MPI_Communication>(*m4py_ptr);
    }
  } // namespace Python
} // namespace LibLSS

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2020
