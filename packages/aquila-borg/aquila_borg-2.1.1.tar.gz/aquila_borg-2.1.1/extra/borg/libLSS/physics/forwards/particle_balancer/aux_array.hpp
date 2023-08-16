/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/particle_balancer/aux_array.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_AUX_ARRAY_HPP
#define __LIBLSS_AUX_ARRAY_HPP

#include <array>
#include <boost/multi_array.hpp>
#include <boost/container/static_vector.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/log_traits.hpp"
#include "libLSS/tools/memusage.hpp"

namespace LibLSS {

  namespace aux_array {
    template <typename Extent>
    size_t product_get(Extent ext) {
      size_t N = 1;
      for (auto s : ext) {
        N *= s.size();
      }
      return N;
    }

    template <size_t N>
    std::array<size_t, N> zero_gen() {
      std::array<size_t, N> a;
      a.fill(0);
      return a;
    }

    template <typename T, size_t nd>
    struct TemporaryArrayStore {
      typedef LibLSS::Console Console;
      typedef boost::multi_array_ref<T, nd> Array;
      size_t array_size;
      T *array_data;
      Array array;

      TemporaryArrayStore()
        : array_size(0), array(0, zero_gen<nd>()){
        array_data = 0;
      }

      TemporaryArrayStore(typename boost::multi_array_types::extent_gen::gen_type<nd>::type extents)
        : array_size(product_get(extents.ranges_)),
	  array_data(new T[product_get(extents.ranges_)]),
          array(array_data, extents)
      {
	report_allocation(array_size*sizeof(T), array_data);
      }

      template <typename Extent>
      TemporaryArrayStore(Extent extents)
        : array_size(product_get(extents)),
	  array_data(new T[product_get(extents)]),
          array(array_data, extents)
      {
	report_allocation(array_size*sizeof(T), array_data);
      }

      TemporaryArrayStore(TemporaryArrayStore&& other)
        : array_size(other.array_size),
          array_data(other.array_data),
          array(array_data, boost::container::static_vector<size_t, nd>(other.array.shape(), other.array.shape()+nd))
        {
          other.array_data = 0;
        }

      ~TemporaryArrayStore() {
        if (array_data != 0) {
          delete[] array_data;
	  report_free(array_size*sizeof(T), array_data);
        }
      }
    };
  } // namespace aux_array

} // namespace LibLSS

#endif
