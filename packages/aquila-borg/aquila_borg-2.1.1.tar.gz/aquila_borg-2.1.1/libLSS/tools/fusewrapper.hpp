/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/fusewrapper.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_FUSEWRAPPER_HPP
#define __LIBLSS_FUSEWRAPPER_HPP
#pragma once

#include <type_traits>
#include <utility>
#include <boost/core/enable_if.hpp>
#include <boost/type_traits/is_scalar.hpp>
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_assign.hpp"
#include "libLSS/tools/phoenix_vars.hpp"
#include <boost/phoenix/operator.hpp>
#include "libLSS/tools/fused_reduce.hpp"
#include "libLSS/tools/fused_cond.hpp"
#include <boost/tti/has_type.hpp>
#include <boost/tti/has_member_function.hpp>
#include <boost/mpl/and.hpp>
#include <boost/mpl/logical.hpp>
#include "libLSS/tools/array_concepts.hpp"
#include <CosmoTool/algo.hpp>
#include "libLSS/tools/uninitialized_type.hpp"

namespace LibLSS {

  namespace FuseWrapper_detail {

    using LibLSS::array_concepts::is_array_like;
    using LibLSS::array_concepts::is_array_storage;
    using LibLSS::array_concepts::is_array_sub;
    using LibLSS::array_concepts::is_array_view;
    using LibLSS::array_concepts::is_callable;

    template <typename Array, bool copy>
    struct Wrapper;

    template <
        typename Array,
        typename U = typename std::remove_reference<Array>::type>
    Wrapper<U, true> fwrap_(Array &&a, std::true_type);
    template <
        typename Array,
        typename U = typename std::remove_reference<Array>::type>
    Wrapper<U, false> fwrap_(Array &&a, std::false_type);

    template <typename T, size_t Nd, typename Allocator>
    auto fwrap(UninitializedAllocation<T, Nd, Allocator> &a) {
      return fwrap_(a.get_array(), std::false_type());
    }

    template <
        typename Array,
        typename = typename std::enable_if<
            is_array_like<typename std::remove_reference<Array>::type>::value,
            void>::type>
    auto fwrap(Array &&a) {
      return fwrap_(
          std::forward<Array>(a), std::is_rvalue_reference<Array &&>());
    }

    template <typename A, bool copy>
    struct CopyType;

    template <typename A>
    struct CopyType<A, true> {
      typedef A type;
      typedef A const_type;
    };

    template <typename A>
    struct CopyType<A, false> {
      typedef A &type;
      typedef A const &const_type;
    };

    template <typename T>
    struct constantFunctor {
      T value;

      constantFunctor(T v) : value(v) {}

      template <typename... Args>
      T const &operator()(Args &&... a) const {
        return value;
      }
    };

    template <typename F>
    struct singleFunctor {
      typedef std::result_of<F()> Result;
      F f;

      singleFunctor() {}
      singleFunctor(F f_) : f(f_) {}

      template <typename... Args>
      Result operator()(Args &&... a) const {
        return f();
      }
    };

    template <typename Array, bool copy>
    struct Wrapper {
      typedef Array array_t;
      typedef typename CopyType<Array, copy>::type WType;
      typedef typename CopyType<Array, copy>::const_type WTypeConst;
      WType a;
      bool parallel;

      explicit Wrapper(Array &a_) : a(a_), parallel(true) {}
      explicit Wrapper(Array &&a_) : a(a_), parallel(true) {}

      template <typename T, size_t Nd, typename Allocator>
      static inline auto
      fautowrap(UninitializedAllocation<T, Nd, Allocator> &a) {
        return Wrapper(a.get_array());
      }

      Array &operator*() { return a; }
      Array const &operator*() const { return a; }
      Array *operator->() { return &a; }
      Array const *operator->() const { return &a; }

      Wrapper no_parallel() const {
         auto b = *this;
         b.parallel = false;
         return b;
      }

      // This auxiliary function creates a perfect
      // forwarding of the required encapsulation of the array.
      // If a copy is needed to ensure the object is long lived
      // enough, then WType is the full Array object.
      // Otherwise, it will be a reference on the original object.
      // Thus a receiving function will get either a lvalue-ref or an rvalue-ref
      // depending on the need.
      WType forward_wrap() { return a; }
      WTypeConst forward_wrap() const { return a; }

      template <typename Array2, bool B2>
      static inline typename Wrapper<Array2, B2>::WType const
      fautowrap(const Wrapper<Array2, B2> &other) {
        return other.a;
      }

      template <typename Array2, typename U = Array2>
      static inline
          typename std::enable_if<is_array_like<Array2>::value, U>::type const &
          fautowrap(Array2 const &other) {
        return other;
      }

      // Intel 17.2 C++ compiler crashes without those
      template <typename ValueType, size_t N>
      struct wrapconst {
        typedef decltype(b_va_fused<ValueType, N>(
            constantFunctor<ValueType>(ValueType(0)))) Result;

        static inline Result wrap(ValueType value) {
          return (b_va_fused<ValueType, N>(constantFunctor<ValueType>(value)));
        }
      };

      template <typename ValueType, size_t N, typename Operator>
      struct wrapfunc {
        typedef decltype(
            b_va_fused<ValueType, N>(singleFunctor<Operator>())) Result;

        static inline Result wrap(Operator op) {
          return (b_va_fused<ValueType, N>(singleFunctor<Operator>(op)));
        }
      };

      template <typename ValueType, typename U = ValueType>
      static inline typename std::enable_if<
          (boost::is_arithmetic<ValueType>::value ||
           array_concepts::is_complex_type<ValueType>::value) &&
              is_array_like<Array>::value,
          wrapconst<U, Array::dimensionality>>::type::Result
      fautowrap(ValueType other) {
        return wrapconst<ValueType, Array::dimensionality>::wrap(other);
      }

      template <typename F, typename U = F>
      static inline typename boost::enable_if<
          is_callable<F>,
          wrapfunc<typename Array::element, Array::dimensionality, U>>::type::
          Result
          fautowrap(F other) {
        return wrapfunc<
            typename Array::element, Array::dimensionality, F>::wrap(other);
      }

      typename Array::element sum() const {
        return LibLSS::reduce_sum<typename Array::element>(a, parallel);
      }

      typename Array::element min() const {
        return LibLSS::reduce_min<typename Array::element>(a, parallel);
      }

      typename Array::element max() const {
        return LibLSS::reduce_max<typename Array::element>(a, parallel);
      }

      template <typename ArrayTo>
      Wrapper<Array, copy> const &copy_to(ArrayTo &to) const {
        LibLSS::copy_array(to, a, to.parallel);
        return *this;
      }

      Wrapper<Array, copy> &operator=(Wrapper<Array, copy> &other) {
        return operator=((Wrapper<Array, copy> const &)other);
      }

      template <typename Wrap2, typename A = Array>
      inline Wrapper<Array, copy> &operator=(Wrap2 const &other) {
        static_assert(
            is_array_storage<A>::value || is_array_view<A>::value ||
                is_array_sub<A>::value,
            "The wrapped array is likely a pure expression. Impossible to "
            "assign.");
        LibLSS::copy_array(a, fautowrap(other), parallel);
        return *this;
      }
    };
  } // namespace FuseWrapper_detail
} // namespace LibLSS

#include "libLSS/tools/fuse/operators.hpp"

namespace LibLSS {

  using FuseWrapper_detail::fwrap;
  using FuseWrapper_detail::is_wrapper;

  template <
      size_t exponent, typename T,
      typename = typename boost::enable_if<
          boost::is_scalar<typename boost::remove_reference<T>::type>>::type>
  auto ipow(T &&t) {
    return CosmoTool::spower<
        exponent, typename boost::remove_reference<T>::type>(t);
  }

  template <size_t N, typename T>
  struct _spower_helper {
    typedef decltype(CosmoTool::spower<N, T>(T(0))) Return;

    inline Return operator()(T a) const { return CosmoTool::spower<N, T>(a); }
  };

  template <size_t exponent, typename Array, bool copy>
  auto ipow(LibLSS::FuseWrapper_detail::Wrapper<Array, copy> wrap) {
    return fwrap(
        b_va_fused<
            typename _spower_helper<exponent, typename Array::element>::Return>(
            _spower_helper<exponent, typename Array::element>(),
            std::forward<typename LibLSS::FuseWrapper_detail::Wrapper<
                Array, copy>::WType>(wrap.a)));
  }

  template <typename T, size_t Nd, typename ExtentType>
  auto ones(ExtentType e) {
    return fwrap(b_fused_idx<T, Nd>([](auto... x) { return T(1); }, e));
  }

  template <typename T, size_t Nd, typename ExtentType>
  auto zero(ExtentType e) {
    return fwrap(b_fused_idx<T, Nd>([](auto... x) { return T(0); }, e));
  }

  template <typename T, size_t Nd, typename ExtentType>
  auto constant(T value, ExtentType e) {
    return fwrap(
        b_fused_idx<T, Nd>([value](auto... x) { return T(value); }, e));
  }

  template <typename Array1, typename Array2, bool copy1, bool copy2>
  auto make_complex(
      LibLSS::FuseWrapper_detail::Wrapper<Array1, copy1> wrap_re,
      LibLSS::FuseWrapper_detail::Wrapper<Array2, copy2> wrap_im) {
    static_assert(
        std::is_same<typename Array1::element, typename Array2::element>::value,
        "The two array have different base type");
    typedef typename Array1::element element;

    return fwrap(b_va_fused<std::complex<element>>(
        [](element const &a, element const &b) {
          return std::complex<element>(a, b);
        },
        std::forward<
            typename LibLSS::FuseWrapper_detail::Wrapper<Array1, copy1>::WType>(
            wrap_re.a),
        std::forward<
            typename LibLSS::FuseWrapper_detail::Wrapper<Array2, copy2>::WType>(
            wrap_im.a)));
  }

  template <
      typename ArrayM, bool copyM, typename Array1, bool copy1, typename Array2,
      bool copy2>
  auto mask(
      LibLSS::FuseWrapper_detail::Wrapper<ArrayM, copyM> wrap_mask,
      LibLSS::FuseWrapper_detail::Wrapper<Array1, copy1> array1,
      LibLSS::FuseWrapper_detail::Wrapper<Array2, copy2> array2) {
    return fwrap(b_cond_fused<typename Array1::element>(
        wrap_mask.forward_wrap(), array1.forward_wrap(),
        array2.forward_wrap()));
  }
} // namespace LibLSS

#endif
