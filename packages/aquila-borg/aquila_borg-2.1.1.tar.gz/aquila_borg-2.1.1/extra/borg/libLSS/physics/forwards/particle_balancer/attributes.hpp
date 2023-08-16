/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/particle_balancer/attributes.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PARTICLE_ATTRIBUTES_HPP
#define __LIBLSS_PARTICLE_ATTRIBUTES_HPP

#include "libLSS/mpi/generic_mpi.hpp"

#include <type_traits>
#include <utility>
#include <tuple>
#include <boost/multi_array.hpp>
#include "libLSS/physics/forwards/particle_balancer/aux_array.hpp"

namespace LibLSS {

  /* We implement classical attributes manager.
   * At the moment we support a simple scalar, and a vector of 3 components.
   * More is possible for a modest implementation cost.
   */

  namespace Particles {

    /**
     * This handles the addition arbitrary scalar attributes attached to a particle.
     * If "tempScalar" is true, then the attribute is a temporary and some cleaning will be done
     * at the exit.
     */
    template <typename ArrayRef, bool tempScalar = false>
    struct ScalarAttribute {
      typedef typename std::remove_reference<ArrayRef>::type ArrayRef_bare;
      typedef typename ArrayRef_bare::reference refType;
      typedef typename ArrayRef_bare::const_reference crefType;
      typedef typename ArrayRef_bare::element Type;
      typedef aux_array::TemporaryArrayStore<Type, 1> TemporaryArray;
      typedef typename TemporaryArray::Array TemporaryArrayType;
      typedef ScalarAttribute<TemporaryArrayType, true> TemporaryAttribute;
      static constexpr bool temporaryHolder = tempScalar;

      // This is a very thin unique pointer owner implementation.
      // This allows to support temporary arrays that self clean
      // when leaving the context, while allowing external arrays
      // to be provided.
      TemporaryArray temp_array_holder;
      ArrayRef_bare &vec;

      ScalarAttribute(ArrayRef_bare &_vec) : temp_array_holder(), vec(_vec) {}

      ScalarAttribute(ScalarAttribute<ArrayRef, false> const &a)
          : temp_array_holder(), vec(a.vec) {
        static_assert(
            tempScalar == false,
            "It is not possible to copy a non-temp ScalarAttribute to a temp "
            "ScalarAttribute. Fix your code.");
      }

      ScalarAttribute(ScalarAttribute<ArrayRef, true> &&a)
          : temp_array_holder(std::move(a.temp_array_holder)),
            vec(temp_array_holder.array) {}

      ScalarAttribute(TemporaryArray &&temp)
          : temp_array_holder(std::move(temp)), vec(temp_array_holder.array) {}

      // Attribute swapper.
      inline void swap(size_t idx0, size_t idx1) {
        std::swap(vec[idx0], vec[idx1]);
      }

      // Store a value in the attribute array. This
      // is completely expanded by the compiler.
      template <typename Value>
      inline void store(size_t idx, Value const &value) {
        vec[idx] = value;
      }

      inline Type const &get(size_t idx) const { return vec[idx]; }

      // Recover the mpi type of the content of this attribute.
      inline MPI_Datatype mpi_type() {
        // Use the mpiVector helper. This array is a set of 3-elements packed
        // in a array. Create an MPI type for that to help us doing I/O
        return translateMPIType<typename ArrayRef_bare::element>();
      }

      // Get the pointer to the memory holding the data.
      inline Type *getArrayData(size_t shift) { return &vec[shift]; }

      // Allocate a new independent, temporary, scalar attribute.
      // It will self clean at the destruction of the returned object.
      static inline TemporaryAttribute allocateTemporary(size_t sz) {
        return TemporaryAttribute(TemporaryArray(boost::extents[sz]));
      }
    };

    /**
     * This creates a scalar attribute helper automatically from an array.
     */
    template <typename ArrayRef>
    ScalarAttribute<ArrayRef> scalar(ArrayRef &a) {
      return ScalarAttribute<ArrayRef>(a);
    }

    /**
     * This handles the addition arbitrary 3d vector attribute attached to a particle.
     */
    template <typename ArrayRef, bool tempVector = false>
    struct VectorAttribute {

      typedef typename std::remove_reference<ArrayRef>::type ArrayRef_bare;
      typedef typename ArrayRef_bare::reference refType;
      typedef typename ArrayRef_bare::const_reference crefType;
      typedef typename ArrayRef_bare::element Type;
      typedef aux_array::TemporaryArrayStore<Type, 2> TemporaryArray;
      typedef typename TemporaryArray::Array TemporaryArrayType;
      typedef VectorAttribute<TemporaryArrayType, true> TemporaryAttribute;
      static constexpr bool temporaryHolder = tempVector;

      TemporaryArray temp_array_holder;
      ArrayRef_bare &vec;

      VectorAttribute(ArrayRef_bare &_vec) : temp_array_holder(), vec(_vec) {}

      VectorAttribute(VectorAttribute<ArrayRef, false> const &a)
          : temp_array_holder(), vec(a.vec) {
        static_assert(
            tempVector == false,
            "It is not possible to copy a non-temp VectorAttribute to a temp "
            "VectorAttribute. Fix your code.");
      }

      VectorAttribute(VectorAttribute<ArrayRef, true> &&a)
          : temp_array_holder(std::move(a.temp_array_holder)),
            vec(temp_array_holder.array) {}

      // Only activate this constructor if the passed array is compatible with
      // temporaryarray.
      VectorAttribute(TemporaryArray &&temp)
          : temp_array_holder(std::move(temp)), vec(temp_array_holder.array) {}

      inline void swap(size_t idx0, size_t idx1) {
        refType vec0 = vec[idx0];
        refType vec1 = vec[idx1];

        std::swap(vec0[0], vec1[0]);
        std::swap(vec0[1], vec1[1]);
        std::swap(vec0[2], vec1[2]);
      }

      template <typename Value>
      inline void store(size_t idx, Value const &value) {
        vec[idx][0] = value[0];
        vec[idx][1] = value[1];
        vec[idx][2] = value[2];
      }

      inline auto get(size_t idx) const -> decltype(vec[idx]) {
        return vec[idx];
      }

      inline MPI_Datatype mpi_type() {
        // Use the mpiVector helper. This array is a set of 3-elements packed
        // in a array. Create an MPI type for that to help us doing I/O
        return mpiVectorType<typename ArrayRef_bare::element, 3>::instance()
            .type();
      }

      inline Type *getArrayData(size_t shift) { return &vec[shift][0]; }

      inline static VectorAttribute<TemporaryArrayType, true>
      allocateTemporary(size_t sz) {
        return VectorAttribute<TemporaryArrayType, true>(
            TemporaryArray(boost::extents[sz][3]));
      }
    };

    template <typename ArrayRef>
    VectorAttribute<ArrayRef> vector(ArrayRef &a) {
      return VectorAttribute<ArrayRef>(a);
    }

  } // namespace Particles

} // namespace LibLSS

#endif
