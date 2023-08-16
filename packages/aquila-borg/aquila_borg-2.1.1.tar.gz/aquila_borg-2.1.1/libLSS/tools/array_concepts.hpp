/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/array_concepts.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TOOLS_ARRAYCONCEPTS_HPP
#define __LIBLSS_TOOLS_ARRAYCONCEPTS_HPP

#include <type_traits>
#include <utility>
#include <boost/core/enable_if.hpp>
#include <boost/tti/has_static_member_data.hpp>
#include <boost/tti/has_type.hpp>
#include <boost/mpl/and.hpp>
#include <boost/multi_array/base.hpp>
#include <boost/mpl/not.hpp>

namespace LibLSS {

  namespace array_concepts {

    BOOST_TTI_HAS_TYPE(element);

    template <typename T, typename = int>
    struct has_shape_info : std::false_type {};

    template <typename T>
    struct has_shape_info<T, decltype((void)T::Shaped, int(0))>
        : std::true_type {};

    template <class F, class... Args>
    struct is_callable {
      template <class U>
      static auto test(U *p)
          -> decltype((*p)(std::declval<Args>()...), void(), std::true_type());
      template <class U>
      static auto test(...) -> decltype(std::false_type());

      static constexpr bool value = decltype(test<F>(0))::value;
    };

    // https://stackoverflow.com/questions/1966362/sfinae-to-check-for-inherited-member-functions/8752988
#define MEMBER_FUNC_CHECKER(name, fn, args)                                    \
  template <class C, typename ret, typename = void>                            \
  struct name : std::false_type {};                                            \
  template <class C, typename ret>                                             \
  struct name<                                                                 \
      C, ret,                                                                  \
      typename std::enable_if<std::is_convertible<                             \
          decltype(std::declval<C>().fn args), ret>::value>::type>             \
      : std::true_type {};

    MEMBER_FUNC_CHECKER(has_member_function_data, data, ())
    MEMBER_FUNC_CHECKER(has_member_function_origin, origin, ())
    MEMBER_FUNC_CHECKER(has_member_function_reindex, reindex, (0))

    template <typename T>
    using is_array_like = has_type_element<T>;

    template <class C, typename = void>
    struct check_element_type {
      typedef void element;
    };

    template <class C>
    struct check_element_type<
        C, typename std::enable_if<has_type_element<C>::value>::type> {
      typedef typename C::element element;
    };

    template <typename T>
    struct is_complex_type : std::false_type {};

    template <typename T>
    struct is_complex_type<std::complex<T>> : std::true_type {};

    template <typename T>
    using is_array_storage = boost::mpl::and_<
        has_type_element<T>,
        has_member_function_data<T, typename check_element_type<T>::element *>>;

    template <typename T>
    using is_array_sub = boost::mpl::and_<
        has_type_element<T>, has_member_function_origin<
                                 T, typename check_element_type<T>::element *>>;

    template <typename T>
    using is_array_view = boost::mpl::and_<
        has_type_element<T>,
        boost::mpl::not_<has_member_function_data<
            T, typename check_element_type<T>::element *>>,
        has_member_function_reindex<T, void>>;

  } // namespace array_concepts

} // namespace LibLSS

#endif
