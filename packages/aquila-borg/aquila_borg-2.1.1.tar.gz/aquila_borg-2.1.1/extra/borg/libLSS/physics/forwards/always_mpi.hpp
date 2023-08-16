/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/always_mpi.hpp
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
namespace LibLSS {

  static constexpr bool const SKIP_MPI_FOR_SINGLE_NODE = true;

  inline bool ALWAYS_MPI(MPI_Communication *comm) {
    return (!SKIP_MPI_FOR_SINGLE_NODE || comm->size() > 1);
  }

} // namespace LibLSS

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2019-2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
