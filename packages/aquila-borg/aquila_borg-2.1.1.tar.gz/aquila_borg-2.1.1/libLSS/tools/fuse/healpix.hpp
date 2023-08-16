/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/fuse/healpix.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_TOOLS_FUSE_HEALPIX_HPP
#  define __LIBLSS_TOOLS_FUSE_HEALPIX_HPP

#  include <healpix_cxx/healpix_map.h>

namespace LibLSS {

  namespace FuseWrapper_detail {
    template <typename T>
    auto fwrap(Healpix_Map<T> &a) {
      boost::const_multi_array_ref<T, 1> b(&a.Map()[0], boost::extents[a.Npix()]);
      return fwrap_(b, std::true_type());
    }
  } // namespace FuseWrapper_detail
  using FuseWrapper_detail::fwrap;
} // namespace LibLSS

#endif
