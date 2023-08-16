/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/particle_balancer/dyn/attributes.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PARTICLE_ABSTRACT_ATTRIBUTES_HPP
#define __LIBLSS_PARTICLE_ABSTRACT_ATTRIBUTES_HPP

#include "libLSS/mpi/generic_mpi.hpp"

#include <type_traits>
#include <utility>
#include <tuple>
#include <boost/multi_array.hpp>

namespace LibLSS {

  namespace AbstractParticles {

    /**
     * @brief Abstract management of temporary memory for attribute
     *
     */
    class TemporaryAttribute {
    protected:
      std::shared_ptr<void> ptr;
      size_t sz;

      TemporaryAttribute() = default;

    public:
      void *getData() { return ptr.get(); }
      size_t size() const { return sz; }
    };

    /**
     * @brief Management of attribute
     *
     */
    class Attribute {
    public:
      virtual ~Attribute();
      virtual std::shared_ptr<TemporaryAttribute>
      allocateTemporary(size_t sz) = 0;
      virtual MPI_Datatype mpi_type() = 0;
      virtual size_t multiplicity() = 0;
      virtual void *getArrayData(size_t offset) = 0;

      virtual void swap(
          boost::multi_array_ref<ssize_t, 1> const &permutation,
          size_t num) = 0;

      virtual void copy_from_tmp_to(
          std::shared_ptr<TemporaryAttribute> &tmp, size_t offset) = 0;
    };

  } // namespace AbstractParticles
} // namespace LibLSS

#endif
