/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/optimization/array_helper.hpp
    Copyright (C) 2018-2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TOOLS_OPTIMIZATION_ARRAY_HELPER_HPP
#define __LIBLSS_TOOLS_OPTIMIZATION_ARRAY_HELPER_HPP

#include <complex>
#include <boost/tti/has_type.hpp>
#include <boost/multi_array.hpp>
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/tools/uninitialized_type.hpp"

namespace LibLSS {

  namespace Optimization {

    BOOST_TTI_HAS_TYPE(array_t);
    BOOST_TTI_HAS_TYPE(holder_array_t);

    template<typename T> struct is_complex: public std::false_type {};
    template<typename U> struct is_complex<std::complex<U>> : public std::true_type {};

    template <typename Array1, typename Array2, typename U = typename Array1::array_t::element>
    inline typename std::enable_if<!is_complex<U>::value, double>::type dotprod(Array1 const &a1, Array2 const &a2) {
       return (a1*a2).sum();
    }

    template <typename Array1, typename Array2, typename U = typename Array1::array_t::element>
    inline typename std::enable_if<is_complex<U>::value, double>::type dotprod(Array1 const &a1, Array2 const &a2) {
      auto r = [](auto&& a) { return std::real(a); };
      auto i = [](auto&& a) { return std::imag(a); };
      auto r1 = r(a1);
      auto r2 = r(a2);
      auto i1 = i(a1);
      auto i2 = i(a2);

      return (r1*r2 + i1*i2).sum();
    }

    template <typename Array1, typename Array2>
    inline double dotprod(MPI_Communication* comm, Array1 const &a1, Array2 const &a2) {
      double r = dotprod(a1, a2);

      comm->all_reduce_t(MPI_IN_PLACE, &r, 1, MPI_SUM);
      return r;
    }

    template <typename Array>
    struct array_holder {
    public:
      typedef Array array_t;
      typedef UninitializedArray<array_t> u_array_t;
      typedef std::shared_ptr<u_array_t> holder_array_t;
      holder_array_t holder;

      array_holder() : holder() {}
      array_holder(array_holder<Array> &other) : holder(other.holder) {}
      array_holder(array_holder<Array> &&other)
          : holder(std::move(other.holder)) {}
      array_holder(holder_array_t &&h) : holder(std::move(h)) {}
      array_holder(holder_array_t& h) : holder(h) {}

      array_holder<Array> const &operator=(array_holder<Array> &other) {
        holder = other.holder;
        return *this;
      }

      array_holder<Array> const &operator=(array_holder<Array> &&other) {
        holder = std::move(other.holder);
        return *this;
      }

      inline array_t &get() { return holder.get()->get_array(); }
      inline array_t const &get() const { return holder.get()->get_array(); }

      inline operator bool() const {
        return holder.operator bool();
      }

      inline auto operator*() -> decltype(fwrap(get())) {
        return fwrap(get());
      }

      inline auto operator*() const -> decltype(fwrap(get())) {
        return fwrap(get());
      }
    };

    template <typename T, typename = void>
    struct is_holder : std::false_type {};

    template <typename T>
    struct is_holder<
        T, typename std::enable_if<
               has_type_array_t<T>::value &&
               has_type_holder_array_t<T>::value>::type> : std::true_type {};

    template <typename T, size_t N>
    struct BoostArrayAllocator {
    public:
      typedef boost::multi_array_ref<T, N> array_t;
      typedef array_holder<array_t> holder_t;
      typedef typename holder_t::u_array_t new_array_t;
      typedef decltype(fwrap(*(array_t *)0)) wrap_t;

      inline auto wrapper(array_t const &a) const -> decltype(fwrap(a)) {
        return fwrap(a);
      }

      inline auto wrapper(array_t &a) const -> decltype(fwrap(a)) {
        return fwrap(a);
      }

      inline holder_t new_like(holder_t const &a) { return new_like(a.get()); }

      template<typename ArrayLike>
      inline holder_t new_like(ArrayLike const &a) {
        return holder_t(std::unique_ptr<new_array_t>(
            new new_array_t(LibLSS::array::make_extent_from(a)))
        );
      }
    };

  } // namespace Optimization
} // namespace LibLSS

// ARES TAG: num_authors = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2018-2019

#endif
