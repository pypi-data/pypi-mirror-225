#pragma once

namespace LibLSS {

  namespace FuseWrapper_detail {
    template <typename T>
    struct is_wrapper : std::false_type {};

    template <typename Array, bool copy>
    struct is_wrapper<Wrapper<Array, copy>> : std::true_type {};

    // Here we builds recursively lazy binary expressions using boost::phoenix capabilities.
    //
    template <typename T, typename U>
    using DisableIf = typename std::enable_if<!T::value, U>::type;

    template <typename T, typename U>
    using EnableIf = typename std::enable_if<T::value, U>::type;

    template <typename A, typename = int>
    struct _DetectElement;

    template <typename A>
    struct _DetectElement<
        A, typename std::enable_if<
               !is_array_like<A>::value && !is_wrapper<A>::value, int>::type> {
      typedef typename std::remove_reference<A>::type element;
    };

    template <typename A>
    struct _DetectElement<A, EnableIf<is_array_like<A>, int>> {
      typedef typename std::remove_reference<A>::type::element element;
    };

    template <typename Array, bool copy>
    struct _DetectElement<Wrapper<Array, copy>> {
      typedef typename Array::element element;
    };

    template <typename A>
    using DetectElement = typename _DetectElement<
        typename std::remove_reference<A>::type>::element;

#define FWRAPPER_BUILD_UNARY_OPERATOR(op)                                      \
  template <typename Array, bool copy>                                         \
  inline auto operator op(Wrapper<Array, copy> const &self) {                  \
    return fwrap(                                                              \
        b_va_fused<typename Array::element>(op _p1, self.forward_wrap()));     \
  }

    FWRAPPER_BUILD_UNARY_OPERATOR(-)
    FWRAPPER_BUILD_UNARY_OPERATOR(!)

#undef FWRAPPER_BUILD_UNARY_OPERATOR

#define FWRAPPER_BUILD_BINARY_OPERATOR(op)                                     \
  template <typename Array, bool copy, typename ToWrap2>                       \
  inline auto operator op(                                                     \
      Wrapper<Array, copy> const &self, ToWrap2 const &other) {                \
    typedef typename Array::element A_t;                                       \
    typedef DetectElement<ToWrap2> O_t;                                        \
    typedef decltype(::std::declval<A_t>() op ::std::declval<O_t>()) AO_t;     \
    return fwrap(b_va_fused<AO_t>(                                             \
        _p1 op _p2, self.forward_wrap(),                                       \
        Wrapper<Array, copy>::fautowrap(other)));                              \
  }                                                                            \
                                                                               \
  template <                                                                   \
      typename Array, bool copy, typename NotWrap2,                            \
      typename T = DisableIf<is_wrapper<NotWrap2>, void>>                      \
  inline auto operator op(                                                     \
      NotWrap2 const &other, Wrapper<Array, copy> const &self) {               \
    typedef typename Array::element A_t;                                       \
    typedef DetectElement<NotWrap2> O_t;                                       \
    typedef decltype(::std::declval<A_t>() op ::std::declval<O_t>()) AO_t;     \
    return fwrap(b_va_fused<AO_t>(                                             \
        _p2 op _p1, self.forward_wrap(),                                       \
        Wrapper<Array, copy>::fautowrap(other)));                              \
  }

    FWRAPPER_BUILD_BINARY_OPERATOR(+);
    FWRAPPER_BUILD_BINARY_OPERATOR(-);
    FWRAPPER_BUILD_BINARY_OPERATOR(/);
    FWRAPPER_BUILD_BINARY_OPERATOR(*);
    FWRAPPER_BUILD_BINARY_OPERATOR(^);

#undef FWRAPPER_BUILD_BINARY_OPERATOR

#define FWRAPPER_BUILD_COMPARATOR(op)                                          \
  template <typename Array, bool copy, typename Wrap2>                         \
  inline auto operator op(                                                     \
      Wrapper<Array, copy> const &self, Wrap2 const &other)                    \
      ->decltype(fwrap(b_va_fused<bool>(                                       \
          _p1 op _p2, self.forward_wrap(),                                     \
          Wrapper<Array, copy>::fautowrap(other)))) {                          \
    return fwrap(b_va_fused<bool>(                                             \
        _p1 op _p2, self.forward_wrap(),                                       \
        Wrapper<Array, copy>::fautowrap(other)));                              \
  }                                                                            \
  template <typename Array, bool copy, typename NotWrap2>                      \
  inline auto operator op(                                                     \
      NotWrap2 const &other, Wrapper<Array, copy> const &self)                 \
      ->DisableIf<                                                             \
          is_wrapper<NotWrap2>,                                                \
          decltype(fwrap(b_va_fused<bool>(                                     \
              _p2 op _p1, self.forward_wrap(),                                 \
              Wrapper<Array, copy>::fautowrap(other))))> {                     \
    return fwrap(b_va_fused<bool>(                                             \
        _p2 op _p1, self.forward_wrap(),                                       \
        Wrapper<Array, copy>::fautowrap(other)));                              \
  }

    FWRAPPER_BUILD_COMPARATOR(==)
    FWRAPPER_BUILD_COMPARATOR(!=)
    FWRAPPER_BUILD_COMPARATOR(>)
    FWRAPPER_BUILD_COMPARATOR(<)
    FWRAPPER_BUILD_COMPARATOR(<=)
    FWRAPPER_BUILD_COMPARATOR(>=)
    FWRAPPER_BUILD_COMPARATOR(&&)
    FWRAPPER_BUILD_COMPARATOR(||)

#undef FWRAPPER_BUILD_COMPARATOR

    //    template<typename Array >
    //    Wrapper<Array const,false> fwrap(Array const& a) {
    //        return Wrapper<Array const,false>(a);
    //    }
    //

    template <typename Array, typename U>
    Wrapper<U, true> fwrap_(Array &&a, std::true_type) {
      // lvalue refs, copy mandatorily
      return Wrapper<U, true>(a);
    }

    template <typename Array, typename U>
    Wrapper<U, false> fwrap_(Array &&a, std::false_type) {
      // rvalue refs, do not copy
      return Wrapper<U, false>(a);
    }

  } // namespace FuseWrapper_detail
} // namespace LibLSS

#define FUSE_MATH_UNARY_OPERATOR(mathfunc)                                     \
  namespace LibLSS {                                                           \
    namespace FuseWrapper_detail {                                             \
      template <typename T>                                                    \
      struct mathfunc##_functor {                                              \
        auto operator()(T const &val) const -> decltype(std::mathfunc(val)) {  \
          return std::mathfunc(val);                                           \
        }                                                                      \
      };                                                                       \
      template <typename T>                                                    \
      using result_##mathfunc =                                                \
          typename std::result_of<mathfunc##_functor<T>(T)>::type;             \
    }                                                                          \
  }                                                                            \
                                                                               \
  namespace std {                                                              \
    template <typename Array, bool copy>                                       \
    auto mathfunc(LibLSS::FuseWrapper_detail::Wrapper<Array, copy> wrap) {     \
      typedef LibLSS::FuseWrapper_detail::result_##mathfunc<                   \
          typename Array::element>                                             \
          Return;                                                              \
      typedef LibLSS::FuseWrapper_detail::mathfunc##_functor<                  \
          typename Array::element>                                             \
          Functor;                                                             \
      return LibLSS::FuseWrapper_detail::fwrap(                                \
          LibLSS::b_va_fused<Return>(Functor(), wrap.forward_wrap()));         \
    }                                                                          \
  }

//// std::cout << "Functor=" #mathfunc << " type = " << typeid(Return).name() << std::endl;\
//
//

#define FUSE_MATH_RESULT(mathfunc) result_##mathfunc

#define FUSE_MATH_BINARY_OPERATOR(mathfunc)                                    \
  namespace LibLSS {                                                           \
    namespace FuseWrapper_detail {                                             \
      template <typename T, typename T2>                                       \
      struct mathfunc##_functor {                                              \
        T2 val2;                                                               \
                                                                               \
        mathfunc##_functor(T2 val2_) : val2(val2_) {}                          \
        auto operator()(T const &val) const                                    \
            -> decltype(std::mathfunc(val, val2)) {                            \
          return std::mathfunc(val, val2);                                     \
        }                                                                      \
      };                                                                       \
      template <typename T, typename T2>                                       \
      using FUSE_MATH_RESULT(mathfunc) =                                       \
          typename std::result_of<mathfunc##_functor<T, T2>(T)>::type;         \
    }                                                                          \
  }                                                                            \
                                                                               \
  namespace std {                                                              \
    template <                                                                 \
        typename Array, bool copy, typename Other,                             \
        typename =                                                             \
            typename std::enable_if<std::is_scalar<Other>::value, void>::type> \
    auto mathfunc(                                                             \
        LibLSS::FuseWrapper_detail::Wrapper<Array, copy> wrap, Other other) {  \
      return LibLSS::FuseWrapper_detail::fwrap(                                \
          LibLSS::b_va_fused<                                                  \
              LibLSS::FuseWrapper_detail::FUSE_MATH_RESULT(mathfunc) <         \
                  typename Array::element,                                     \
              Other>>                                                          \
          (LibLSS::FuseWrapper_detail::mathfunc##_functor<                     \
               typename Array::element, Other>(other),                         \
           wrap.forward_wrap()));                                              \
    }                                                                          \
  }

FUSE_MATH_UNARY_OPERATOR(real);
FUSE_MATH_UNARY_OPERATOR(imag);
FUSE_MATH_UNARY_OPERATOR(norm);
FUSE_MATH_UNARY_OPERATOR(conj);
FUSE_MATH_UNARY_OPERATOR(exp);
FUSE_MATH_UNARY_OPERATOR(sinh);
FUSE_MATH_UNARY_OPERATOR(cosh);
FUSE_MATH_UNARY_OPERATOR(tanh);
FUSE_MATH_UNARY_OPERATOR(sin);
FUSE_MATH_UNARY_OPERATOR(cos);
FUSE_MATH_UNARY_OPERATOR(tan);
FUSE_MATH_UNARY_OPERATOR(atan);
FUSE_MATH_UNARY_OPERATOR(acos);
FUSE_MATH_UNARY_OPERATOR(asin);
FUSE_MATH_UNARY_OPERATOR(sqrt);
FUSE_MATH_UNARY_OPERATOR(log);
FUSE_MATH_UNARY_OPERATOR(log10);
FUSE_MATH_UNARY_OPERATOR(floor);
FUSE_MATH_UNARY_OPERATOR(ceil);
FUSE_MATH_UNARY_OPERATOR(abs);
FUSE_MATH_UNARY_OPERATOR(erf);
FUSE_MATH_UNARY_OPERATOR(erfc);
FUSE_MATH_BINARY_OPERATOR(pow);
FUSE_MATH_BINARY_OPERATOR(modf);
FUSE_MATH_BINARY_OPERATOR(fmod);
