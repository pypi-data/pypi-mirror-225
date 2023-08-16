/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/particle_balancer/part_swapper.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TOOLS_PART_SWAPPER_HPP
#define __LIBLSS_TOOLS_PART_SWAPPER_HPP

#include <boost/multi_array.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/physics/forwards/particle_balancer/aux_array.hpp"

namespace LibLSS {

  namespace internal_swapper {

    template <size_t id>
    struct storage_impl {
      template <typename A, typename B, typename T>
      void exec(A &a, B &b, size_t idx, T const &d) {
        storage_impl<id - 1>().exec(a.next, a.this_attribute, d);
      }
    };

    template <>
    struct storage_impl<0> {
      template <typename A, typename B, typename T>
      void exec(A &a, B &b, size_t idx, T const &d) {
        b.store(idx, d);
      }
    };

    // Particles comes as a bunch of arrays of the same size but possibly
    // different types. One array is mandatory: the 3d position. However one
    // can consider adding other attributes. For vectorization purpose, it is
    // slightly better to consider them as bunch of arrays instead of an array
    // of a structure. However it creates also a lot of tension in the code.
    // Maybe in the future everything will be transposed, which will induce a
    // significant rewrite of the PM code. Currently we will consider that a
    // simulation  state can be modeled as follow:
    // struct State {
    //    Positions pos;
    //    Velocities vel;
    //    OtherStuff other;
    // }
    // But each of those is an array of the same size.
    // When doing load balancing these arrays must be swapped synchronously.
    // The other reason for keeping this representation is that a lot of the rest
    // of the infrastructure relies on a Nx3 array for positions. Doing
    // transposes online or non vectorized could cost us dearly in terms of
    // performance.

    template <typename... Attr>
    struct AttributeTuple {};

    // If we have at least one attribute then we can proceed with this
    // implementation.
    template <typename First, typename... Attr>
    struct AttributeTuple<First, Attr...> {
      typedef AttributeTuple<First, Attr...> Self;
      typedef AttributeTuple<Attr...> Next;
      typedef AttributeTuple<
          typename First::TemporaryAttribute,
          typename Attr::TemporaryAttribute...>
          TempSelf;
      typedef typename First::refType refType;
      First this_attribute;
      AttributeTuple<Attr...> next;
      static constexpr size_t numAttributes = 1 + sizeof...(Attr);

      AttributeTuple(Self const &other)
          : this_attribute(other.this_attribute), next(other.next) {}

      AttributeTuple(Self &&other)
          : this_attribute(std::move(other.this_attribute)),
            next(std::move(other.next)) {}

      AttributeTuple(First &&attr, Attr &&... others)
          : this_attribute(std::move(attr)), next(std::move(others)...) {}

      inline void swap(size_t idx0, size_t idx1) {
        this_attribute.swap(idx0, idx1);
        next.swap(idx0, idx1);
      }

      // This is a classic recurrence for store<int> function.
      // Do a recursion till id is zero.
      template <size_t id, typename DataType>
      inline void store(size_t idx, DataType const &data) {
        storage_impl<id>().exec(this->next, this->this_attribute, idx, data);
      }

      template <typename Other>
      struct AcceptedVariant {
        static constexpr auto value = std::is_same<Other, Self>::value ||
                                      std::is_same<Other, TempSelf>::value;
      };

      // We need this other type to be either ourself or a Variant
      // corresponding to the temporary attribute. Anything else is
      // rejected.
      template <typename Other>
      inline typename std::enable_if<AcceptedVariant<Other>::value>::type
      recursive_store(size_t idx, Other const &other, size_t where_from) {
        this_attribute.store(idx, other.this_attribute.get(where_from));
        next.recursive_store(idx, other.next, where_from);
      }

      auto tuple_get(size_t idx) -> decltype(std::tuple_cat(
          std::make_tuple(this_attribute.get(idx)), next.tuple_get(idx))) {
        return std::tuple_cat(
            std::make_tuple(this_attribute.get(idx)), next.tuple_get(idx));
      }

      // This is an helper function. It allows to build a call to function f
      // where all attributes are expanded in a single call. More details in the
      // particle swapper.
      static inline TempSelf allocateTemporary(size_t sz) {
        return TempSelf(
            First::allocateTemporary(sz), Attr::allocateTemporary(sz)...);
      }

      // This is an unusual dynamic operator for static tuple.
      // Unfortunately that is far easier to implement this with a dynamic
      // syntax rather than with template syntax as it is going to be intertwinned
      // with calls to MPI functions.
      inline MPI_Datatype mpi_type(size_t const aid) {
        if (aid == 0)
          return this_attribute.mpi_type();
        else
          return next.mpi_type(aid - 1);
      }

      inline void *getArrayData(size_t const aid, size_t const shift) {
        if (aid == 0)
          return this_attribute.getArrayData(shift);
        else
          return next.getArrayData(aid - 1, shift);
      }
    };

    template <>
    struct AttributeTuple<> {
      typedef AttributeTuple<> Self;
      typedef AttributeTuple<> TempSelf;
      static const size_t numAttributes = 0;

      AttributeTuple(Self const &other) {}
      AttributeTuple() {}
      AttributeTuple(Self &&other) {}

      inline void swap(size_t, size_t) {}

      inline void recursive_store(
          size_t idx, AttributeTuple<> const &other, size_t where_from) {}

      std::tuple<> tuple_get(size_t idx) { return std::tuple<>(); }

      static inline TempSelf allocateTemporary(size_t sz) { return TempSelf(); }

      inline MPI_Datatype mpi_type(size_t aid) {
        LibLSS::Console &cons = LibLSS::Console::instance();
        cons.print<LOG_ERROR>("Invalid access in AttributeTuple::mpi_type");
        MPI_Communication::instance()->abort();
        return MPI_INTEGER;
      }

      inline void *getArrayData(size_t aid, size_t shift) {
        LibLSS::Console &cons = LibLSS::Console::instance();
        cons.print<LOG_ERROR>("Invalid access in AttributeTuple::getArrayData");
        MPI_Communication::instance()->abort();
        return (void *)0;
      }
    };

  } // namespace internal_swapper

  /**
   * Build a attribute tuple which will help accessing the different arrays with a same
   * syntaxic interface.
   */
  template <typename... Attrs>
  inline internal_swapper::AttributeTuple<Attrs...>
  make_attribute_helper(Attrs &&... attrs) {
    return internal_swapper::AttributeTuple<Attrs...>(
        std::forward<Attrs>(attrs)...);
  }

  /**
   * This class implements helper methods to exchange particles
   * and their attributes in place in their arrays.
   * It also provides temporary array allocators for auxiliary attributes.
   * This is supposed to be an internal class for the particle
   * MPI distribution routine. However it is fairly generic for other use
   * requiring synchronize reorganisation of different arrays
   * at the same time, without a-prior knowing what are those arrays before
   * the instanciation.
   *
   * @tparam ArrayRef             reference to the fundamental array corresponding to positions (typically a boost::multi_array or boost::multi_array_ref).
   * @tparam AuxiliaryAttributes  Attribute class descriptor like LibLSS::internal_swapper::AttributeTuple.
   *
   * @see LibLSS::make_attribute_helper
   */
  template <typename ArrayRef, typename AuxiliaryAttributes>
  class ParticleSwapper {
  public:
    typedef typename boost::remove_reference<ArrayRef>::type ArrayRef_bare;
    typedef typename ArrayRef_bare::reference refType;
    typedef ParticleSwapper<ArrayRef, AuxiliaryAttributes> Self;

    ArrayRef pos;
    AuxiliaryAttributes attrs;

    /**
     * Constructor.
     * @param _pos the array of positions
     * @param _attrs the attribute tuple obtained through LibLSS::make_attribute_helper
     */
    ParticleSwapper(ArrayRef _pos, AuxiliaryAttributes _attrs)
        : pos(_pos), attrs(_attrs) {}

    /**
     * Execute an in-place swap of positions and attributes for particles
     * at index idx0 and idx1.
     *
     * @param idx0 Index of first particle.
     * @param idx1 Index of second particle.
     */
    inline void do_swap(size_t idx0, size_t idx1) {
      refType in_pos = pos[idx0];
      refType out_pos = pos[idx1];

      std::swap(in_pos[0], out_pos[0]);
      std::swap(in_pos[1], out_pos[1]);
      std::swap(in_pos[2], out_pos[2]);
      attrs.swap(idx0, idx1);
    }

    /**
     * This is an helper function. It allows to build a call to function f
     * where all attributes are expanded in a single call.
     * allocateTemporary calls each attribute allocateTemporary to ask
     * to expand the attribute to do a single call to create the new
     * AuxiliaryAttributes object. To finalize the construction we rely on
     * allocateTemporaryUnwrapper, which enforces the move semantic and call
     * the actual allocateTemporary on each attribute.
     */
    static inline typename AuxiliaryAttributes::TempSelf
    allocateTemporary(size_t sz) {
      return AuxiliaryAttributes::allocateTemporary(sz);
    }

    /**
     * Get access to the raw pointer holding the specified attribute,
     * eventually shifted by an index 'shift'.
     * @param aid   attribute index.
     * @param shift index of the element for which we request the pointer.
     */
    inline void *getArrayData(size_t const aid, size_t const shift) {
      return attrs.getArrayData(aid, shift);
    }

    /**
     * Return the MPI datatype of the attribute "aid"
     * @param aid Attribute index.
     */
    inline MPI_Datatype mpi_type(size_t const aid) {
      return attrs.mpi_type(aid);
    }

    /**
     * Copy the provided position  (a array-like object with a shape [N][3]) at "where_from"
     * to the target position "target_idx" in the holded array.
     * @param target_idx where to the copy the position to.
     * @param posRecv    an array-like object of position
     * @param where_from source position in posRecv.
     */
    template <typename ArrayRecv>
    inline void copy_in_pos(
        size_t target_idx, const ArrayRecv &posRecv, size_t where_from) {
      typename ArrayRecv::const_reference loc_in_pos = posRecv[where_from];
      refType loc_out_pos = pos[target_idx];

      loc_out_pos[0] = loc_in_pos[0];
      loc_out_pos[1] = loc_in_pos[1];
      loc_out_pos[2] = loc_in_pos[2];
    }

    /**
     * Copy the provided attribute provided in "attrRecv" at "where_from"
     * to the target position "target_idx".
     *
     * @tparam id         the identifier of the attribute.
     * @param  target_idx the target position.
     * @param  attrRecv   an array-like object holding the new attribute value.
     * @param  where_from where to copy that attribute from.
     */
    template <size_t id, typename ArrayRecv>
    inline void copy_in_attr(
        size_t target_idx, const ArrayRecv &attrRecv, size_t where_from) {
      typename ArrayRecv::const_reference loc_in_attr = attrRecv[where_from];
      attrs.store<id>(target_idx, loc_in_attr);
    }

    /**
     * Copy all attributes from attrRecv (AttributeTuple class) to the
     * currently holded position/attribute array.
     */
    template <typename OtherAttributes>
    inline void copy_in_all_attrs(
        size_t target_idx, OtherAttributes const &attrRecv, size_t where_from) {
      attrs.recursive_store(target_idx, attrRecv, where_from);
    }
  };

  // Import only the right class template into the LibLSS namespace
  using internal_swapper::AttributeTuple;
  typedef AttributeTuple<> NoAuxiliaryAttributes;

  // That's compatibility layer for previous mechanisms.
  template <bool doVel, typename ArrayRef>
  class ParticleSwapperTaped {};

  template <typename ArrayRef>
  class ParticleSwapperTaped<true, ArrayRef>
      : public ParticleSwapper<
            typename ArrayRef::reference, NoAuxiliaryAttributes> {
  public:
    typedef ParticleSwapper<typename ArrayRef::reference, NoAuxiliaryAttributes>
        super;

    ParticleSwapperTaped(ArrayRef &_pos, ArrayRef &_vel, int istep)
        : super(_pos[istep], _vel[istep]) {}
  };

  template <typename ArrayRef>
  class ParticleSwapperTaped<false, ArrayRef>
      : public ParticleSwapper<
            typename ArrayRef::reference, NoAuxiliaryAttributes> {
  public:
    typedef ParticleSwapper<typename ArrayRef::reference, NoAuxiliaryAttributes>
        super;

    ParticleSwapperTaped(ArrayRef &_pos, ArrayRef &_vel, int istep)
        : super(_pos[istep]) {}
  };

}; // namespace LibLSS

#endif
