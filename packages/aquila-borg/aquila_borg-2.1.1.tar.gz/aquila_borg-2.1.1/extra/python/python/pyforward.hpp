/*+
    ARES/HADES/BORG Package -- ./extra/python/python/pyforward.hpp
    Copyright (C) 2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PYTHON_FORWARD_HPP
#  define __LIBLSS_PYTHON_FORWARD_HPP
#  pragma once

#  include <memory>
#  include <exception>
#  include <boost/format.hpp>
#  include "libLSS/physics/forward_model.hpp"

namespace LibLSS {
  template <typename T>
  static inline void
  check_array_real(T &in, std::shared_ptr<BORGForwardModel::DFT_Manager> &mgr) {
    if (in.shape(0) != mgr->localN0 || in.shape(1) != mgr->N1 ||
        in.shape(2) != mgr->N2)
      throw std::range_error(boost::str(
          boost::format("Input array has invalid dimensions, expecting "
                        "%dx%dx%d") %
          mgr->localN0 % mgr->N1 % mgr->N2));
  }

  template <typename T>
  static inline void check_array_complex(
      T &in, std::shared_ptr<BORGForwardModel::DFT_Manager> &mgr) {
    if (in.shape(0) != mgr->localN0 || in.shape(1) != mgr->N1 ||
        in.shape(2) != mgr->N2_HC)
      throw std::range_error(boost::str(
          boost::format("Input array has invalid dimensions, expecting "
                        "%dx%dx%d") %
          mgr->localN0 % mgr->N1 % mgr->N2_HC));
  }

} // namespace LibLSS

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019
