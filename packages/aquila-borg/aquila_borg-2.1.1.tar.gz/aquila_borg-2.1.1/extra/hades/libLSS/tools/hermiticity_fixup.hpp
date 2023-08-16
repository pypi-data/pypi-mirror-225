/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/tools/hermiticity_fixup.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2019 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TOOLS_HERMITICITY_FIXUP_HPP
#  define __LIBLSS_TOOLS_HERMITICITY_FIXUP_HPP

#  include <complex>
#  include <boost/format.hpp>
#  include "libLSS/tools/mpi_fftw_helper.hpp"
#  include "libLSS/tools/mpi/ghost_planes.hpp"

namespace LibLSS {

  template <typename T, size_t Nd>
  struct Hermiticity_fixer {
    typedef FFTW_Manager<T, Nd> Mgr;
    typedef std::shared_ptr<Mgr> Mgr_p;
    typedef typename Mgr::U_ArrayFourier::array_type CArrayRef;

    MPI_Communication *comm;
    Mgr_p mgr;

    GhostPlanes<std::complex<T>, Nd - 1> ghosts;

    Hermiticity_fixer(Mgr_p mgr);

    void forward(CArrayRef &a);
    void adjoint(CArrayRef &a);
  };

} // namespace LibLSS

#endif

// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2014-2020
// ARES TAG: name(1) = Jens Jasche
// ARES TAG: email(1) = jens.jasche@fysik.su.se
// ARES TAG: year(1) = 2009-2019
