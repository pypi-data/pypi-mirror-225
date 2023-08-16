/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/nary_arrays.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_NARY_ARRAYS_HPP
#define __LIBLSS_NARY_ARRAYS_HPP

#include <algorithm>
#include <tuple>
#include "libLSS/tools/array_concepts.hpp"

namespace LibLSS {

    struct ArrayTuple_base {
        typedef boost::multi_array_types::size_type size_type;
        typedef boost::multi_array_types::index index;
    };


    template<size_t Ndims, typename ReturnElement, typename TupleT, bool Shaped>
    struct ArrayTuple;

    template<size_t Ndims, typename ReturnElement, typename TupleT>
    struct ArrayTuple<Ndims, ReturnElement,TupleT,false>: ArrayTuple_base {
      enum { NumDims = Ndims };
      enum { arity = std::tuple_size<TupleT>::value };
      static constexpr bool Shaped = false;
      typedef boost::array<index, Ndims> subindex;
      typedef boost::array<size_type, Ndims> subshape;

      typedef TupleT Tuple;
      typedef ReturnElement element;
      const Tuple tuple;

      inline
      ArrayTuple(Tuple const & t) : tuple(t) {}

      inline bool vectorizable() const { return false; }
    };

    template<size_t Ndims, typename ReturnElement, typename TupleT>
    struct ArrayTuple<Ndims, ReturnElement,TupleT,true>: ArrayTuple_base {
      enum { NumDims = Ndims };
      enum { arity = std::tuple_size<TupleT>::value };
      static constexpr bool Shaped = true;

      typedef TupleT Tuple;
      typedef ReturnElement element;
      const Tuple tuple;

      inline
      ArrayTuple(Tuple const & t) : tuple(t) {}

      inline
      const size_type *shape() const { return std::get<0>(tuple).shape(); }

      inline
      const index *index_bases() const { return std::get<0>(tuple).index_bases(); }

      inline
      size_type num_elements() const { return std::get<0>(tuple).num_elements(); }

      inline bool vectorizable() const { return false; }
    };

    template<size_t Ndims, typename ReturnElement, size_t arity_par = 0>
    struct ArrayNullTuple: ArrayTuple_base {
      enum { NumDims = Ndims };
      enum { arity = arity_par };
      typedef ReturnElement element;
      static constexpr bool Shaped = false;

      // Special no-op tuple
      struct Tuple {

        // Type to access i-th position of the given index.
        template<int i>
        struct TupleElement {
            template<typename Index>
            inline auto operator()(const Index& j) const->
                decltype(j[i]) { return j[i]; }
        };

      };
      // Implicit accessor
      const Tuple tuple;

      inline
      ArrayNullTuple() : tuple() {}
    };


    template<size_t Ndims, typename ReturnElement, size_t arity_par = 0>
    struct ArrayNullTupleExtent: ArrayTuple_base {
      enum { NumDims = Ndims };
      enum { arity = arity_par };
      typedef ReturnElement element;
      static constexpr bool Shaped = true;
      typedef boost::array<index, Ndims> subindex;
      typedef boost::array<size_type, Ndims> subshape;

      // Special no-op tuple
      struct Tuple {

        // Type to access i-th position of the given index.
        template<int i>
        struct TupleElement {
            template<typename Index>
            auto operator()(const Index& j) const -> decltype(j[i]) { return j[i]; }
        };
      };
      // Implicit accessor
      const Tuple tuple;
      subindex indexes;
      subshape shapes;

      typedef boost::multi_array_types::extent_range extent_range;
      size_t total_elts;

      // ExtentGen is a boost::extents like type
      template<typename ExtentType>
      ArrayNullTupleExtent(const ExtentType& f_extents)
        : tuple() {
        using std::transform;

        transform(f_extents.ranges_.begin(), f_extents.ranges_.end(),
                       indexes.begin(),
                       boost::mem_fun_ref(&extent_range::start));
        transform(f_extents.ranges_.begin(), f_extents.ranges_.end(),
                       shapes.begin(),
                       boost::mem_fun_ref(&extent_range::size));

        size_t _total = 1;
        std::for_each(shapes.begin(), shapes.end(),
                      [&_total](size_type s) { _total *= s; });
        total_elts = _total;
      }

      template<typename ShapeList, typename IndexList>
      ArrayNullTupleExtent(const ShapeList& _shapes, const IndexList& _indexbase)
        : tuple() {
        using std::transform;

        std::copy(_indexbase.begin(), _indexbase.end(), indexes.begin());
        std::copy(_shapes.begin(), _shapes.end(), shapes.begin());

        size_t _total = 1;
        std::for_each(shapes.begin(), shapes.end(),
                      [&_total](size_type s) { _total *= s; });
        total_elts = _total;
      }


      const size_type *shape() const { return &shapes[0];}
      const index *index_bases() const { return &indexes[0]; }
      size_type num_elements() const { return 0; }
    };


    // Special cases for which the tuple of array is degenerate to the empty set.\
    // The arraytuple is always not shaped then.
    template<size_t Ndims, typename ReturnElement, bool Shaped>
    struct ArrayTuple<Ndims,ReturnElement,std::tuple<>,Shaped>: ArrayTuple_base, ArrayNullTuple<Ndims,ReturnElement> { };

    template<size_t Ndims, typename ReturnElement, bool Shaped>
    struct ArrayTuple<Ndims,ReturnElement,std::tuple<> const,Shaped>: ArrayTuple_base, ArrayNullTuple<Ndims,ReturnElement> { };


    // Detect whether a type support shapes or not
    // By default no.
    template<typename T, typename = void>
    struct DetectShaped {
      static constexpr bool Shaped = false;
    };

    template<typename T>
    struct DetectShaped<T, typename boost::enable_if<array_concepts::has_shape_info<T>>::type> {
      static constexpr bool Shaped = T::Shaped;
    };

    template<typename T>
    struct DetectShaped<T, typename boost::enable_if<array_concepts::is_array_storage<T>>::type> {
      static constexpr bool Shaped = true;
    };

    template<typename T>
    struct DetectShaped<T, typename std::enable_if<array_concepts::is_array_sub<T>::value && !array_concepts::is_array_view<T>::value && !array_concepts::is_array_storage<T>::value>::type> {
      static constexpr bool Shaped = true;
    };

    template<typename T>
    struct DetectShaped<T, typename boost::enable_if<array_concepts::is_array_view<T>>::type> {
      static constexpr bool Shaped = true;
    };

}


// Populate std with some additional getters to support NullTuples
namespace std {
  template<size_t getter, typename NullTuple>
  inline typename NullTuple::template TupleElement<getter>
  get(NullTuple const& t) throw() {
    return typename NullTuple::template TupleElement<getter>();
  }

}


// Terminate the definition of a lazy/virtual array evaluation
namespace LibLSS {

    namespace details {

        template<int order>
        struct array_apply_tuple {
           template<typename Operation, typename ArrayTuple, typename Index, typename... Args>
           static inline typename ArrayTuple::element
           apply(Operation&& op, ArrayTuple& at, Index i, Args&&... args) {
              return array_apply_tuple<order-1>::apply(op, at, i, std::get<order-1>(at.tuple)(i), args...);
           }
        };

        template<>
        struct array_apply_tuple<0> {
           template<typename Operation, typename ArrayTuple, typename Index, typename... Args>
           static inline typename ArrayTuple::element apply(Operation&& op, ArrayTuple& at, Index i, Args&&... args) {
              return op(args...);
           }
        };

        template<typename Operation, typename ArrayTuple, typename Index>
        inline
        typename ArrayTuple::element
        apply_op(Operation&& op, ArrayTuple& t, Index i ) {
            return array_apply_tuple<ArrayTuple::arity>::apply(op, t, i);
        };
    };

}


#endif
