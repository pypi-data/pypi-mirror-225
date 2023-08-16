/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/particle_balancer/dyn/vector.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PARTICLE_ABSTRACT_VECTOR_ATTRIBUTE_HPP
#define __LIBLSS_PARTICLE_ABSTRACT_VECTOR_ATTRIBUTE_HPP

#include "libLSS/mpi/generic_mpi.hpp"

#include <type_traits>
#include <utility>
#include <tuple>
#include <boost/multi_array.hpp>
#include "libLSS/physics/forwards/particle_balancer/dyn/attributes.hpp"

namespace LibLSS {

  namespace AbstractParticles {

    template <typename Element>
    class VectorTemporary : public TemporaryAttribute {
    protected:
      std::shared_ptr<Element> arr;

      VectorTemporary() = default;

    public:
      VectorTemporary(size_t sz_, size_t d)
          : arr(std::shared_ptr<Element>(
                new Element[sz_ * d], [sz_](Element *e) {
                  Console::instance().format<LOG_DEBUG>("Freeing sz=%d", sz_);
                  delete[] e;
                })) {
        LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
        ctx.format("allocated temporary vector sz=%d, d=%d", sz_, d);
        this->ptr = arr;
        this->sz = sz_;
      }
    };

    template <typename ArrayRef>
    class VectorAttribute : public Attribute {
    public:
      typedef typename std::remove_reference<ArrayRef>::type ArrayRef_bare;
      typedef typename ArrayRef_bare::reference refType;
      typedef typename ArrayRef_bare::const_reference crefType;
      typedef typename ArrayRef_bare::element Type;

      ArrayRef_bare &vec;

      VectorAttribute(ArrayRef_bare &_vec) : vec(_vec) {}

      std::shared_ptr<TemporaryAttribute>
      allocateTemporary(size_t sz) override {
        return std::make_shared<VectorTemporary<Type>>(sz, vec.shape()[1]);
      }

      size_t multiplicity() override { return vec.shape()[1]; }

      MPI_Datatype mpi_type() override { return translateMPIType<Type>(); }

      void *getArrayData(size_t offset) override {
        return &this->vec[offset][0];
      }

      void swap(
          boost::multi_array_ref<ssize_t, 1> const &permutation,
          size_t num) override {
        LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
        const size_t d = vec.shape()[1];

        for (size_t i = 0; i < num; ++i) {
          if (permutation[i] != i) {
            for (size_t j = 0; j < d; j++) {
              std::swap(vec[i][j], vec[permutation[i]][j]);
            }
          }
        }
      }

      void copy_from_tmp_to(
          std::shared_ptr<TemporaryAttribute> &tmp, size_t offset) override {
        LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
        if (!tmp) {
          error_helper<ErrorBadState>("Invalid array");
        }
        auto origin = (Type *)tmp->getData();
        size_t sz = tmp->size();
        const size_t d = vec.shape()[1];

        for (size_t i = 0; i < sz; i++)
          for (size_t j = 0; j < d; j++) {
            size_t k = i * d + j;
            ctx.format("i=%d, j=%d, k=%d", i, j, k);
            vec[offset + i][j] = origin[k];
          }
      }
    };

    /**
     * This creates a scalar attribute helper automatically from an array.
     */
    template <typename ArrayRef>
    std::shared_ptr<AbstractParticles::Attribute> vector(ArrayRef &a) {
      return std::make_shared<VectorAttribute<ArrayRef>>(a);
    }

  } // namespace AbstractParticles
} // namespace LibLSS

#endif