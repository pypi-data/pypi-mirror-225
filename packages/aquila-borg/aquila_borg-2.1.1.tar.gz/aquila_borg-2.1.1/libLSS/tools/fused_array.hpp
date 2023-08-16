/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/fused_array.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_FUSED_ARRAY_HPP
#define __LIBLSS_FUSED_ARRAY_HPP

#include <boost/multi_array.hpp>

#include "libLSS/tools/nary_arrays.hpp"
#include "libLSS/tools/fused_assign.hpp"
#include "libLSS/tools/ref_tools.hpp"

namespace LibLSS {

  namespace FUSE_detail {

    namespace FusedArrayTypes {

      typedef boost::multi_array_types::size_type size_type;
      typedef boost::multi_array_types::index index;

    } // namespace FusedArrayTypes

    template <typename T, std::size_t ND, typename Allocator>
    struct BoostArray {
      enum { NumDims = ND };
      typedef boost::multi_array<T, ND, Allocator> type;
      typedef T element;
    };

    template <typename T, std::size_t ND>
    struct BoostRefArray {
      enum { NumDims = ND };
      typedef boost::const_multi_array_ref<T, ND> type;
      typedef T element;
    };

    template <typename T>
    struct ConstantArray {
      enum { NumDims = 0 };
      typedef T type;
      typedef T element;
    };

    struct FusedArray_base {
      typedef FusedArrayTypes::size_type size_type;
      typedef FusedArrayTypes::index index;
    };

    template <
        typename ArrayTuple, typename Operation, std::size_t N,
        std::size_t order, bool shaped>
    struct FusedArray_view;

    template <typename ArrayTuple, typename Operation, std::size_t N>
    struct FusedArray_view_scalar : FusedArray_base {
      static constexpr bool Shaped = ArrayTuple::Shaped;
      Operation op;
      const ArrayTuple &tuple;
      typedef typename ArrayTuple::element element;
      typedef FusedArrayTypes::size_type size_type;
      typedef boost::array<index, N> subindex;
      subindex idx;

      inline FusedArray_view_scalar(
          Operation _op, const ArrayTuple &_tuple, const subindex &i)
          : op(_op), tuple(_tuple), idx(i) {}

      inline const element &apply() const {
        return details::apply_op(op, tuple, idx);
      };

      inline operator element() const {
        return details::apply_op(op, tuple, idx);
      }
    };

    // *************************** Begin of view with no shape support ****************

    template <
        typename ArrayTuple, typename Operation, std::size_t N,
        std::size_t order>
    struct FusedArray_view<ArrayTuple, Operation, N, order, false>
        : FusedArray_base {
      static constexpr bool Shaped = ArrayTuple::Shaped;
      Operation op;
      ArrayTuple tuple;

      typedef boost::array<index, N> subindex;
      typedef FusedArray_view<ArrayTuple, Operation, N, order - 1, false>
          subview;
      typedef FusedArray_view<ArrayTuple, Operation, N, 0, false> subview0;
      subindex idx;

      inline FusedArray_view(
          Operation _op, const ArrayTuple &_tuple, const subindex &i)
          : op(_op), tuple(_tuple), idx(i) {}

      template <typename T_sub>
      inline typename std::enable_if<
          subindex::static_size == T_sub::static_size, subview0>::type
      operator()(T_sub const &i) const {
        return subview0(op, tuple, i);
      }

      template <typename T_sub>
      inline typename std::enable_if<
          order != N &&
              (N - order + T_sub::static_size == subindex::static_size),
          subview0>::type
      operator()(T_sub const &i) const {
        subindex j;
        for (unsigned int k = 0; k < N - order; k++)
          j[k] = idx[k];
        for (unsigned int k = N - order; k < N; k++)
          j[k] = i[k - (N - order)];

        return subview0(op, tuple, j);
      }

      inline subview operator[](size_type i) const {
        subindex idx0 = idx;
        idx0[N - order] = i;
        return subview(op, tuple, idx0);
      }
    };

    template <typename ArrayTuple, typename Operation, std::size_t N>
    struct FusedArray_view<ArrayTuple, Operation, N, 0, false>
        : FusedArray_view_scalar<ArrayTuple, Operation, N> {
      static constexpr bool Shaped = ArrayTuple::Shaped;
      typedef FusedArray_view_scalar<ArrayTuple, Operation, N> super;
      typedef typename super::subindex subindex;

      inline FusedArray_view(
          Operation _op, const ArrayTuple &_tuple, const subindex &i)
          : FusedArray_view_scalar<ArrayTuple, Operation, N>(_op, _tuple, i) {}
    };

    // a (0,0) is never shaped.
    template <typename ArrayTuple, typename Operation>
    struct FusedArray_view<ArrayTuple, Operation, 0, 0, false>
        : FusedArray_base {
      static constexpr bool Shaped = ArrayTuple::Shaped;
      typedef typename ArrayTuple::element element;
      Operation op;
      const ArrayTuple &tuple;
      const index *indexes;
      const size_type *shapes;
      typedef boost::array<size_type, 0> subindex;
      typedef FusedArray_view<ArrayTuple, Operation, 0, 0, false> subview;

      inline FusedArray_view(
          Operation _op, const ArrayTuple &_tuple, const subindex &i)
          : op(_op), tuple(_tuple) {}

      inline const element &apply() const {
        return details::apply_op(op, tuple, subindex());
      };

      inline operator element() const {
        return details::apply_op(op, tuple, subindex());
      }

      inline subview operator[](size_type i) const {
        // Ignore everything
        return subview(op, tuple, subindex());
      }
    };

    // *************************** End of view with no shape support ****************

    // *************************** Begin of view with shape support ****************

    template <
        typename ArrayTuple, typename Operation, std::size_t N,
        std::size_t order>
    struct FusedArray_view<ArrayTuple, Operation, N, order, true>
        : FusedArray_base {
      typedef typename ArrayTuple::element element;
      Operation op;
      ArrayTuple tuple;

      static constexpr bool Shaped = ArrayTuple::Shaped;
      typedef boost::array<index, N> subindex_root;
      typedef boost::array<index, order> subindex;
      typedef FusedArray_view<ArrayTuple, Operation, N, order - 1, true>
          subview;
      typedef FusedArray_view<ArrayTuple, Operation, N, 0, true> subview0;
      subindex_root idx;
      const index *v_index;
      const size_type *v_size;

      inline FusedArray_view(
          Operation _op, const ArrayTuple &_tuple, const subindex_root &i,
          const index *_index, const size_type *_size)
          : op(_op), tuple(_tuple), idx(i), v_index(_index), v_size(_size) {}

      template <typename T = element>
      inline typename std::enable_if<order == 1, T>::type
      operator[](size_type i) const {
        subindex_root idx0 = idx;
        idx0[N - order] = i;
        return details::apply_op(op, tuple, idx0);
      }

      template <typename T = subview>
      inline typename std::enable_if<order != 1, T>::type
      operator[](size_type i) const {
        subindex_root idx0 = idx;
        idx0[N - order] = i;
        return subview(op, tuple, idx0, v_index + 1, v_size + 1);
      }

      inline subview0 operator()(subindex_root const &i) const {
        return subview0(op, tuple, i, 0, 0);
      }

      template <typename T = subview0>
      inline typename std::enable_if<order != N, T>::type
      operator()(subindex const &i) const {
        subindex_root idx0 = idx;
        for (unsigned int k = 0; k < order; k++)
          idx0[N - order + k] = i[k];
        return subview0(op, tuple, idx0, 0, 0);
      }

      inline const size_type *shape() const { return v_size; }

      inline const index *index_bases() const { return v_index; }
    };

    template <typename ArrayTuple, typename Operation, std::size_t N>
    struct FusedArray_view<ArrayTuple, Operation, N, 0, true>
        : FusedArray_view_scalar<ArrayTuple, Operation, N> {
      typedef FusedArray_view_scalar<ArrayTuple, Operation, N> super;
      static constexpr bool Shaped = ArrayTuple::Shaped;
      typedef typename super::subindex subindex;
      typedef typename super::index index;
      typedef typename super::size_type size_type;

      inline FusedArray_view(
          Operation _op, const ArrayTuple &_tuple, const subindex &i,
          const index *_index, const size_type *_size)
          : FusedArray_view_scalar<ArrayTuple, Operation, N>(_op, _tuple, i) {}
      // Here we discard _index and _size as we have just a zero-dim array.
    };

    // *************************** End of view with shape support ****************

    template <std::size_t N>
    struct NumDimDecrement {
      enum { value = N - 1 };
    };

    template <>
    struct NumDimDecrement<0> {
      enum { value = 0 };
    };

    template <
        typename ArrayTuple, typename Operation,
        bool ShapeTuple = ArrayTuple::Shaped>
    struct FusedArray;

    template <typename ArrayTuple, typename Operation>
    struct FusedArray<ArrayTuple, Operation, true> : FusedArray_base {
      enum { NumDims = ArrayTuple::NumDims };
      enum { dimensionality = ArrayTuple::NumDims };
      typedef typename ArrayTuple::element element;
      static constexpr bool Shaped = true;

      ArrayTuple const a;
      Operation const op;
      typedef boost::array<index, NumDims> subindex;
      typedef FusedArray_view<
          ArrayTuple, Operation, NumDims, NumDimDecrement<NumDims>::value,
          ArrayTuple::Shaped>
          subview;

      inline FusedArray(ArrayTuple p_a, Operation p_op) : a(p_a), op(p_op) {}

      inline subview operator[](FusedArrayTypes::size_type i) const {
        subindex idx;
        if (NumDims >= 1)
          idx[0] = i;
        return subview(op, a, idx, a.index_bases() + 1, a.shape() + 1);
      }

      inline element operator()(const subindex &idx) const {
        return details::apply_op(op, a, idx);
      }

      inline const size_type *shape() const { return a.shape(); }

      inline const index *index_bases() const { return a.index_bases(); }

      inline size_type num_elements() const { return a.num_elements(); }
    };

    // No shape then strip all the shape related functions.
    template <typename ArrayTuple, typename Operation>
    struct FusedArray<ArrayTuple, Operation, false> : FusedArray_base {
      enum { NumDims = ArrayTuple::NumDims };
      enum { dimensionality = ArrayTuple::NumDims };
      typedef typename ArrayTuple::element element;
      static constexpr bool Shaped = false;

      ArrayTuple const a;
      Operation const op;
      typedef boost::array<index, NumDims> subindex;
      typedef FusedArray_view<
          ArrayTuple, Operation, NumDims, NumDimDecrement<NumDims>::value,
          ArrayTuple::Shaped>
          subview;

      inline FusedArray(ArrayTuple p_a, Operation p_op) : a(p_a), op(p_op) {}

      inline subview operator[](FusedArrayTypes::size_type i) const {
        subindex idx;
        if (NumDims >= 1)
          idx[0] = i;
        return subview(op, a, idx);
      }

      inline element operator()(const subindex &idx) const {
        return details::apply_op(op, a, idx);
      }
    };

    // This is a new API using Variadic templates. The interface is incompatible with b_fused
    // thus a new name. The operator has to be put at the front of the list to
    // support an arbitrary number of arrays in the list.
    // This variant can only be used if there is at least one array
    // in the list, thus this specialization.
    // The no-array variant is as usual using the ArrayNullTuple variant.

    // This function is compatible both with temporary objects and stable objects.
    // The universal reference mechanism (Array1&& etc) grabs everything and produce
    // references, even to rvalues. However reference to rvalues is unsafe and likely produce
    // segv in most cases for our specific use. So we strip the rvalue reference and convert
    // it back to a normal copy in that case. That allows slicing, intricated fused calls etc.

    template <typename A>
    using remove_const_ref = typename boost::remove_const<
        typename boost::remove_reference<A>::type>::type;

    template <
        typename Return, typename Operation, typename Array1,
        typename... Arrays>
    inline auto b_va_fused(Operation op, Array1 &&a1, Arrays &&... arrays) {
      typedef typename boost::remove_reference<Array1>::type BareArray1;
      typedef std::tuple<
          typename strip_rvalue_ref<decltype(a1)>::type,
          typename strip_rvalue_ref<decltype(arrays)>::type...>
          btuple;
      typedef ArrayTuple<
          BareArray1::dimensionality, Return, btuple,
          DetectShaped<typename boost::remove_const<BareArray1>::type>::Shaped>
          RealTuple;

      return FusedArray<RealTuple, Operation>(
          RealTuple(btuple(a1, arrays...)), op);
    }

    template <typename Return, std::size_t N, typename Operation>
    inline auto b_va_fused(Operation op) {
      typedef ArrayNullTuple<N, Return, N> RealTuple;
      return FusedArray<RealTuple, Operation>(RealTuple(), op);
    }

    template <
        typename Return, typename Array1, typename Array2, typename Array3,
        typename Array4, typename Operation>
    inline auto b_fused(
        const Array1 &a1, const Array2 &a2, const Array3 &a3, const Array4 &a4,
        Operation op) {
      typedef typename std::tuple<
          const Array1 &, const Array2 &, const Array3 &, const Array4 &>
          tuple;
      typedef ArrayTuple<Array1::dimensionality, Return, tuple, true> RealTuple;

      return FusedArray<RealTuple, Operation>(
          RealTuple(std::forward_as_tuple(a1, a2, a3, a4)), op);
    }

    template <
        typename Return, typename Array1, typename Array2, typename Array3,
        typename Operation>
    inline auto b_fused(
        const Array1 &a1, const Array2 &a2, const Array3 &a3, Operation op) {
      typedef
          typename std::tuple<const Array1 &, const Array2 &, const Array3 &>
              tuple;
      typedef ArrayTuple<Array1::dimensionality, Return, tuple, true> RealTuple;

      return FusedArray<RealTuple, Operation>(
          RealTuple(std::forward_as_tuple(a1, a2, a3)), op);
    }

    template <
        typename Return, typename Array1, typename Array2, typename Operation>
    inline auto b_fused(const Array1 &a1, const Array2 &a2, Operation op) {
      typedef typename std::tuple<const Array1 &, const Array2 &> tuple;
      typedef ArrayTuple<Array1::dimensionality, Return, tuple, true> RealTuple;

      return FusedArray<RealTuple, Operation>(
          RealTuple(std::forward_as_tuple(a1, a2)), op);
    }

    template <typename Return, typename Array1, typename Operation>
    inline auto b_fused(const Array1 &a1, Operation op) {
      typedef typename std::tuple<const Array1 &> tuple;
      typedef ArrayTuple<Array1::dimensionality, Return, tuple, true> RealTuple;
      return FusedArray<RealTuple, Operation>(
          RealTuple(std::forward_as_tuple(a1)), op);
    }

    template <typename Return, std::size_t N, typename Operation>
    inline auto b_fused(Operation op) {
      typedef ArrayNullTuple<N, Return> RealTuple;
      return FusedArray<RealTuple, Operation>(RealTuple(), op);
    }

    /**
       * This builds a virtual array with N-dimensions, whose elements
       * are of type Return. Each access to the element call the provided
       * operator, with the corresponding requested index. 
       * The signature should thus be "op(size_t, ...)->Return" with number of arguments
       * corresponding to the number of dimensions.
       * This array is "infinite", i.e. it does not have any specified bound, which may be
       * required for some assignment operation.
       *
       * @param op a functor that must be Copy-Constructible
       * @return a Copy-Constructible expression
       */
    template <typename Return, std::size_t N, typename Operation>
    inline auto b_fused_idx(Operation op) {
      typedef ArrayNullTuple<N, Return, N> RealTuple;
      return FusedArray<RealTuple, Operation>(RealTuple(), op);
    }

    /**
       * This builds a virtual array with N-dimensions, whose elements
       * are of type Return. Each access to the element call the provided
       * operator, with the corresponding requested index. 
       * The signature should thus be "op(size_t, ...)->Return" with number of arguments
       * corresponding to the number of dimensions.
       * This array is finite with extents indicated by "f_extents".
       *
       * @param op a functor that must be Copy-Constructible.
       * @param f_extents extent of the new virtual array.
       * @return a Copy-Constructible expression
       */
    template <
        typename Return, std::size_t N, typename ExtentType, typename Operation>
    inline auto b_fused_idx(Operation op, const ExtentType &f_extents) {
      typedef ArrayNullTupleExtent<N, Return, N> RealTuple;
      return FusedArray<RealTuple, Operation>(RealTuple(f_extents), op);
    }

    /**
       * Same as the above, but with extents split into two lists for easier management.
       */
    template <
        typename Return, std::size_t N, typename ShapeList, typename IndexList,
        typename Operation>
    inline auto b_fused_idx(
        Operation op, const ShapeList &_shapes, const IndexList &_indexes) {
      typedef ArrayNullTupleExtent<N, Return, N> RealTuple;
      return FusedArray<RealTuple, Operation>(RealTuple(_shapes, _indexes), op);
    }

  } // namespace FUSE_detail

  using FUSE_detail::b_fused;
  using FUSE_detail::b_fused_idx;
  using FUSE_detail::b_va_fused;

} // namespace LibLSS

#endif
