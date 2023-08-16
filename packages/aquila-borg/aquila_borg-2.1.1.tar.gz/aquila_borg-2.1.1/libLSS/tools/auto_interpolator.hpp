/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/auto_interpolator.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TOOLS_AUTO_INTERP_HPP
#define __LIBLSS_TOOLS_AUTO_INTERP_HPP

#include <boost/multi_array.hpp>
#include <cmath>
#include "libLSS/tools/errors.hpp"

namespace LibLSS {

  namespace internal_auto_interp {

    template <typename T>
    class auto_interpolator {
    public:
      typedef T bare_t;
      typedef boost::multi_array<T, 1> array_type;

    private:
      array_type *array_vals;
      size_t N;
      T start, end, step, overflow, underflow;
      bool throwOnOverflow;

    public:
      explicit auto_interpolator(
          const T &_start, const T &_end, const T &_step, const T &_under,
          const T &_over, array_type *value)
          : array_vals(value), start(_start), end(_end), step(_step),
            underflow(_under), overflow(_over), N(value->size()),
            throwOnOverflow(false) {}

      auto_interpolator(auto_interpolator<T> &&other)
          : array_vals(other.array_vals), start(other.start), end(other.end),
            step(other.step), underflow(other.underflow),
            overflow(other.overflow), N(other.N), throwOnOverflow(false) {
        other.array_vals = 0;
      }

      explicit auto_interpolator()
          : array_vals(0), start(0), end(0), step(0), underflow(0), overflow(0),
            N(0), throwOnOverflow(false) {}

      auto_interpolator(auto_interpolator<T> const &other) {
        array_vals = 0;
        operator=(other);
      }

      auto_interpolator<T> &operator=(auto_interpolator<T> const &other) {
        if (array_vals)
          delete array_vals;
        array_vals = new array_type(boost::extents[other.N]);
        start = other.start;
        end = other.end;
        step = other.step;
        underflow = other.underflow;
        overflow = other.overflow;
        N = other.N;
        throwOnOverflow = other.throwOnOverflow;
        for (size_t i = 0; i < N; i++)
          (*array_vals)[i] = (*other.array_vals)[i];
        return *this;
      }

      ~auto_interpolator() {
        if (array_vals)
          delete array_vals;
      }

      auto_interpolator<T> &setThrowOnOverflow() {
        throwOnOverflow = true;
        return *this;
      }

      T operator()(const T &a) const {
        T normed_pos = (a - start) / step;
        T f_pos = std::floor(normed_pos);
        ssize_t i_pos = ssize_t(f_pos);
        T r = normed_pos - f_pos;

        if (i_pos < 0)
          return underflow;
        if (i_pos == (N - 1) && std::abs(r) < 1e-5) {
          return (*array_vals)[N - 1];
        }
        if (i_pos >= (N - 1)) {
          if (throwOnOverflow)
            throw ErrorParams("overflow in interpolation");
          return overflow;
        }
        return (1 - r) * (*array_vals)[i_pos] + r * (*array_vals)[i_pos + 1];
      }
    };

    template <typename T, typename Functor>
    auto_interpolator<T> build_auto_interpolator(
        const Functor &f, const T &start, const T &end, const T &step,
        const T &underflow, const T &overflow) {
      typedef auto_interpolator<T> a_interp;
      typedef typename a_interp::array_type array_type;
      size_t N = size_t(round((end - start) / step));
      array_type *vals = new array_type(boost::extents[N]);

#pragma omp parallel
      for (size_t i = 0; i < N; i++) {
        T x = start + i * step;
        (*vals)[i] = f(x);
      }

      return a_interp(start, end, step, underflow, overflow, vals);
    }

  } // namespace internal_auto_interp

  using internal_auto_interp::auto_interpolator;
  using internal_auto_interp::build_auto_interpolator;

} // namespace LibLSS

#endif
