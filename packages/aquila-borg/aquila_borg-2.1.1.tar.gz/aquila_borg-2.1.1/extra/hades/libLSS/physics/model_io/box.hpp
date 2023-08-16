/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/model_io/box.hpp
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_PHYSICS_MODELIO_BOX_HPP
#  define __LIBLSS_PHYSICS_MODELIO_BOX_HPP

#  include <memory>
#  include "libLSS/physics/cosmo.hpp"
#  include "libLSS/mpi/generic_mpi.hpp"
#  include "libLSS/tools/mpi_fftw_helper.hpp"
#  include "libLSS/tools/errors.hpp"
#  include "libLSS/samplers/core/types_samplers.hpp"
#  include <boost/variant.hpp>

namespace LibLSS {

  template <size_t Nd>
  struct NBoxModel {};

  template <>
  struct NBoxModel<2> {
    double xmin0, xmin1;
    double L0, L1;
    long N0, N1;

    void fill(std::array<ssize_t, 2> &N) const {
      N[0] = N0;
      N[1] = N1;
    }

    double volume() const { return L0 * L1; }
    long numElements() const { return N0 * N1; }

    bool operator==(NBoxModel<2> const &other) const {
      return xmin0 == other.xmin0 && xmin1 == other.xmin1 && L0 == other.L0 &&
             L1 == other.L1 && N0 == other.N0 && N1 == other.N1;
    }
    bool operator!=(NBoxModel<2> const &other) const {
      return !operator==(other);
    }
  };

  template <>
  struct NBoxModel<3> {
    double xmin0, xmin1, xmin2;
    double L0, L1, L2;
    long N0, N1, N2;

    void fill(std::array<ssize_t, 3> &N) const {
      N[0] = N0;
      N[1] = N1;
      N[2] = N2;
    }

    double volume() const { return L0 * L1 * L2; }
    long numElements() const { return N0 * N1 * N2; }

    bool operator==(NBoxModel<3> const &other) const {
      return xmin0 == other.xmin0 && xmin1 == other.xmin1 &&
             xmin2 == other.xmin2 && L0 == other.L0 && L1 == other.L1 &&
             L2 == other.L2 && N0 == other.N0 && N1 == other.N1 &&
             N2 == other.N2;
    }

    bool operator!=(NBoxModel<3> const &other) const {
      return !operator==(other);
    }
  };

  typedef NBoxModel<3> BoxModel;

} // namespace LibLSS
#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019-2020
