/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/fused_cond.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef _LIBLSS_FUSED_CONDITIONAL_HPP
#define _LIBLSS_FUSED_CONDITIONAL_HPP

#include <functional>
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/ref_tools.hpp"

namespace LibLSS {

  namespace FusedCondDetails {

    using size_type = FUSE_detail::FusedArrayTypes::size_type;
    using index = FUSE_detail::FusedArrayTypes::index;

    template<typename T>
    struct ArrayDim {
      typedef typename std::remove_reference<T>::type Array;
      static constexpr size_t D = Array::dimensionality;
    };

    template<typename T>
    using ArrayIndex = boost::array<index, ArrayDim<T>::D>;

    // This functor allows invokes another functor with the indexes wrapped in a boost::array
    template<typename Return, typename Tuple>
    struct MakeSubIndexOp {
      Tuple const t;

      inline MakeSubIndexOp(Tuple const&& _t) : t(_t) {}
      inline MakeSubIndexOp(Tuple const& _t) : t(_t) {}

      template<typename... Indexes>
      inline Return operator()(Indexes... idx) const {
        boost::array<index, sizeof...(Indexes)> i = { idx... };
        if (std::get<0>(t)(i)) {
          return std::get<1>(t)(i);
        } else {
          return std::get<2>(t)(i);
        }
      }
    };

    // This is an auxiliary function to make life easier
    template<typename Return, typename Tuple>
    inline MakeSubIndexOp<Return, Tuple>
    make_subindex_op(const Tuple&& t) {
      return MakeSubIndexOp<Return, Tuple>(std::forward<Tuple const>(t));
    }

    // Again this is an auxiliary struct that includes a fake begin/end calls.
    template<typename _T>
    struct wrap_ptr {
      typedef typename std::remove_reference<_T>::type T;

      T const *s, *e;
      inline wrap_ptr(T const *_start, T const *_end)
        : s(_start), e(_end) { }

      inline T const *begin() const { return s; }
      inline T const *end() const { return e; }
    };


    // This is the main instrumentation to build the lazy branching on a pair of arrays
    template<typename Return, typename CondArray, typename Array1, typename Array2>
    struct CondHelper {
      // If we have rvalue ref we strip the reference to ensure
      // the value is copied in the tuple. If we are provided
      // with a ref just keep it that way to avoid copying the dense
      // array.
      typedef std::tuple<
        typename strip_rvalue_ref<CondArray>::type,
        typename strip_rvalue_ref<Array1>::type,
        typename strip_rvalue_ref<Array2>::type
        > btuple;

      typedef typename std::remove_reference<CondArray>::type PureCond;
      typedef typename std::remove_reference<Array1>::type PureArray1;
      typedef typename std::remove_reference<Array2>::type PureArray2;

      // This create a functor on the 3 array
      static inline auto make_op(CondArray cond, Array1 a1, Array2 a2)
          -> decltype(FusedCondDetails::make_subindex_op<Return, btuple>(
              btuple(std::forward<CondArray>(cond), std::forward<Array1>(a1), std::forward<Array2>(a2))
            )) {
          return FusedCondDetails::make_subindex_op<Return, btuple>(
              btuple(std::forward<CondArray>(cond), std::forward<Array1>(a1), std::forward<Array2>(a2))
            );
      }
      
      // This wraps the shapes
      template<typename A>
      static inline
      auto build_shape(A a)
        -> decltype(wrap_ptr<decltype(a.shape()[0])>(a.shape(), a.shape() + ArrayDim<A>::D)) {
        return wrap_ptr<decltype(a.shape()[0])>(a.shape(), a.shape() + ArrayDim<A>::D);
      }

      // Similar for index_bases
      template<typename A>
      static inline
      auto build_index_base(A a)
        -> decltype(wrap_ptr<decltype(a.index_bases()[0])>(a.index_bases(), a.index_bases() + ArrayDim<A>::D)) {
        return wrap_ptr<decltype(a.index_bases()[0])>(a.index_bases(), a.index_bases() + ArrayDim<A>::D);
      }

      // This is the main builder, creates a new virtual array out of the 3-array
      static inline auto make(CondArray condition, Array1 array1, Array2 array2)
        -> decltype( b_fused_idx<Return, ArrayDim<CondArray>::D>(
          make_op(std::forward<CondArray>(condition), std::forward<Array1>(array1), std::forward<Array2>(array2)),
          build_shape(condition),
          build_index_base(condition))
          ) {
        return b_fused_idx<Return, ArrayDim<CondArray>::D>(
          make_op(std::forward<CondArray>(condition), std::forward<Array1>(array1), std::forward<Array2>(array2)),
          build_shape(condition),
          build_index_base(condition)
        );
      }
    };
  }

  // Finally a helper function that makes life real easy to the caller.
  // Universal references are probed: if they are rvalue ref, then a copy is
  // made, otherwise we just keep the lvalue ref.
  template<typename Return, typename CondArray, typename Array1, typename Array2>
  inline auto b_cond_fused(CondArray&& condition, Array1&& array1, Array2&& array2)
  {
    return FusedCondDetails::CondHelper<
      Return,
      decltype(condition),
      decltype(array1),
      decltype(array2)
    >::make(std::forward<CondArray>(condition),std::forward<Array1>(array1),std::forward<Array2>(array2));
  }

}

#endif
