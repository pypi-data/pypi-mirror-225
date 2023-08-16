/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/particle_balancer/dyn/scalar.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PARTICLE_ABSTRACT_SCALAR_ATTRIBUTE_HPP
#define __LIBLSS_PARTICLE_ABSTRACT_SCALAR_ATTRIBUTE_HPP

#include "libLSS/mpi/generic_mpi.hpp"

#include <type_traits>
#include <utility>
#include <tuple>
#include <boost/multi_array.hpp>
#include "libLSS/physics/forwards/particle_balancer/dyn/attributes.hpp"

namespace LibLSS {

  namespace AbstractParticles {

    template <typename Element>
    class ScalarTemporary : public TemporaryAttribute {
    protected:
      std::shared_ptr<Element> arr;

      ScalarTemporary() = default;

    public:
      ScalarTemporary(size_t sz_)
          : arr(std::shared_ptr<Element>(
                new Element[sz_], [](Element *e) { delete[] e; })) {
        this->ptr = arr;
        this->sz = sz_;
      }
    };

    template <typename ArrayRef>
    class ScalarAttribute : public Attribute {
    public:
      typedef typename std::remove_reference<ArrayRef>::type ArrayRef_bare;
      typedef typename ArrayRef_bare::reference refType;
      typedef typename ArrayRef_bare::const_reference crefType;
      typedef typename ArrayRef_bare::element Type;

      ArrayRef_bare &vec;

      ScalarAttribute(ArrayRef_bare &_vec) : vec(_vec) {}
      ~ScalarAttribute() override {}

      std::shared_ptr<TemporaryAttribute>
      allocateTemporary(size_t sz) override {
        Console::instance().format<LOG_DEBUG>("allocateTemporary(sz=%d)", sz);
        return std::make_shared<ScalarTemporary<Type>>(sz);
      }

      size_t multiplicity() override { return 1; }

      MPI_Datatype mpi_type() override { return translateMPIType<Type>(); }

      void *getArrayData(size_t offset) override { return &vec[offset]; }

      void swap(
          boost::multi_array_ref<ssize_t, 1> const &permutation,
          size_t num) override {
        for (size_t i = 0; i < num; ++i) {
          if (permutation[i] != i)
            std::swap(vec[i], vec[permutation[i]]);
        }
      }

      void copy_from_tmp_to(
          std::shared_ptr<TemporaryAttribute> &tmp, size_t offset) override {
        if (!tmp) {
          error_helper<ErrorBadState>("Invalid array");
        }
        auto origin = (Type *)tmp->getData();
        size_t sz = tmp->size();
        for (size_t i = 0; i < sz; i++)
          vec[offset + i] = origin[i];
      }
    };

    /**
     * This creates a scalar attribute helper automatically from an array.
     */
    template <typename ArrayRef>
    std::shared_ptr<AbstractParticles::Attribute> scalar(ArrayRef &a) {
      return std::make_shared<ScalarAttribute<ArrayRef>>(a);
    }
  } // namespace AbstractParticles
} // namespace LibLSS

#endif