/*+
    ARES/HADES/BORG Package -- ./extra/python/python/pyfuse.hpp
    Copyright (C) 2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PYTHON_FUSE_ARRAY_HPP
#  define __LIBLSS_PYTHON_FUSE_ARRAY_HPP

#  include "libLSS/tools/fused_array.hpp"
#  include "pyborg.hpp"
#  include <pybind11/pybind11.h>
#  include <pybind11/numpy.h>
#  include "libLSS/tools/string_tools.hpp"

namespace LibLSS {
  namespace Python {

    template <typename T, typename py_T, size_t order, size_t Nd, bool mut>
    class PyToFuseView {
    public:
      enum { dimensionality = order };
      typedef T element;
      typedef ArrayTuple_base::size_type size_type;
      typedef ArrayTuple_base::index index;
      typedef PyToFuseView<
          T, py_T, FUSE_detail::NumDimDecrement<order>::value, Nd, mut>
          subview;
      py_T &array;
      std::array<index, Nd> idx;
      ssize_t const *bases;
      size_t const *shapes;

      PyToFuseView(
          py_T &a, std::array<index, Nd> idx_, ssize_t const *bases_,
          size_t const *shapes_)
          : array(a), idx(idx_), bases(bases_), shapes(shapes_) {}

      inline const size_type *shape() const { return shapes; }

      inline const index *index_bases() const { return bases; }

      inline subview operator[](index i) {
        std::array<index, Nd> idx_new = idx;
        idx_new[Nd - order] = i;
        return subview(array, idx_new, bases + 1, shapes + 1);
      }
    };

    template <typename T, typename py_T, size_t Nd>
    class PyToFuseView<T, py_T, 1, Nd, false> {
    public:
      enum { dimensionality = 1 };
      typedef T element;
      typedef ArrayTuple_base::size_type size_type;
      typedef ArrayTuple_base::index index;
      typedef element subview;
      py_T const &array;
      std::array<index, Nd> idx;
      ssize_t const *bases;
      size_t const *shapes;

      PyToFuseView(
          py_T const &a, std::array<index, Nd> idx_, ssize_t const *bases_,
          size_t const *shapes_)
          : array(a), idx(idx_), bases(bases_), shapes(shapes_) {}

      inline const size_type *shape() const { return shapes; }

      inline const index *index_bases() const { return bases; }

      template <size_t... Is>
      static inline auto const &_unroll_call(
          py_T const &a, std::array<ssize_t, Nd> const &idx,
          std::index_sequence<Is...>) {
        return a(idx[Is]...);
      }

      inline element const &operator[](ssize_t i) const {
        std::array<index, Nd> idx_new = idx;
        idx_new[Nd - 1] = i;
        return _unroll_call(array, idx_new, std::make_index_sequence<Nd>());
      }
    };

    template <typename T, typename py_T, size_t Nd>
    class PyToFuseView<T, py_T, 1, Nd, true> {
    public:
      typedef T element;
      typedef ArrayTuple_base::size_type size_type;
      typedef ArrayTuple_base::index index;
      typedef PyToFuseView<
          T, py_T, FUSE_detail::NumDimDecrement<Nd>::value, Nd, true>
          subview;
      py_T &array;
      std::array<index, Nd> idx;
      ssize_t const *bases;
      size_t const *shapes;

      PyToFuseView(
          py_T &a, std::array<index, Nd> idx_, ssize_t const *bases_,
          size_t const *shapes_)
          : array(a), idx(idx_), bases(bases_), shapes(shapes_) {}

      inline const size_type *shape() const { return shapes; }

      inline const index *index_bases() const { return bases; }

      template <typename T3, size_t... Is>
      static inline auto &_unroll_call(
          T3 &a, std::array<ssize_t, Nd> const &idx,
          std::index_sequence<Is...>) {
        return a(idx[Is]...);
      }

      inline element const &operator[](ssize_t i) const {
        std::array<index, Nd> idx_new = idx;
        idx_new[Nd - 1] = i;
        return _unroll_call<py_T const>(
            array, idx_new, std::make_index_sequence<Nd>());
      }

      inline element &operator[](ssize_t i) {
        std::array<index, Nd> idx_new = idx;
        idx_new[Nd - 1] = i;
        return _unroll_call<py_T>(
            array, idx_new, std::make_index_sequence<Nd>());
      }
    };

    template <typename T, size_t Nd, bool mut>
    struct pyArrayType;

    template <typename T, size_t Nd>
    struct pyArrayType<T, Nd, false> {
      typedef decltype(
          std::declval<py::array_t<T> &>().template unchecked<Nd>()) const type;

      static inline type unchecked(py::array_t<T> &a) {
        return a.template unchecked<Nd>();
      }

      static inline T const *data(type const &a) {
        assert(false);
        return 0;
      } //a.data(0); }
    };

    template <typename T, size_t Nd>
    struct pyArrayType<T, Nd, true> {
      typedef decltype(std::declval<py::array_t<T> &>()
                           .template mutable_unchecked<Nd>()) type;

      static inline type unchecked(py::array_t<T> &a) {
        return a.template mutable_unchecked<Nd>();
      }

      // This one is to fool fusewrapper.
      static inline T *data(type &a) {
        assert(false);
        return 0;
      } //a.mutable_data(0); }
    };

    template <typename T, size_t Nd, bool mut>
    class PyToFuseArrayBase {
    public:
      static constexpr bool Shaped = true;
      typedef T element;
      typedef ArrayTuple_base::size_type size_type;
      typedef ArrayTuple_base::index index;
      typedef typename pyArrayType<T, Nd, mut>::type py_unchecked_t;
      typedef PyToFuseView<
          T, py_unchecked_t, FUSE_detail::NumDimDecrement<Nd>::value, Nd, mut>
          subview;

      py_unchecked_t array;

      std::array<index, Nd> static_index_base;
      std::array<size_type, Nd> static_shape;

      PyToFuseArrayBase(py_unchecked_t a) : array(a) {
        if (a.ndim() != Nd) {
          throw std::runtime_error("Invalid array number of dimensions");
        }
        std::fill(static_index_base.begin(), static_index_base.end(), 0);
        for (unsigned int i = 0; i < Nd; i++)
          static_shape[i] = a.shape(i);
        Console::instance().print<LOG_DEBUG>(
            "Shape of PyFuse is " + LibLSS::to_string(static_shape));
      }

      inline const size_type *shape() const { return static_shape.data(); }

      inline size_type num_elements() const { return array.size(); }

      inline size_type size() const { return shape()[0]; }

      inline const index *index_bases() const {
        return static_index_base.data();
      }

      inline auto data() { return pyArrayType<T, Nd, mut>::data(array); }
    };

    template <typename T, bool mut>
    struct maybe_add_const;

    template <typename T>
    struct maybe_add_const<T, false> {
      typedef T const type;
    };

    template <typename T>
    struct maybe_add_const<T, true> {
      typedef T type;
    };

    template <typename T, size_t Nd, bool mut>
    class PyToFuseArray : public PyToFuseArrayBase<T, Nd, mut> {
    public:
      enum { dimensionality = Nd };
      typedef PyToFuseArrayBase<T, Nd, mut> super_t;
      typedef PyToFuseArrayBase<T, Nd, false> ro_super_t;
      typedef typename super_t::element element;
      typedef typename super_t::subview subview;
      typedef typename ro_super_t::subview ro_subview;
      typedef typename super_t::size_type size_type;
      typedef typename super_t::index index;
      typedef typename maybe_add_const<T, mut>::type ret_element;
      using super_t::super_t;

      template <bool enabled = mut>
      inline typename std::enable_if<enabled, subview>::type
      operator[](index i) {
        std::array<index, Nd> idx;
        idx[0] = i;
        return subview(
            this->array, idx, this->index_bases() + 1, this->shape() + 1);
      }

      template <bool enabled = mut>
      inline typename std::enable_if<!enabled, ro_subview>::type
      operator[](index i) const {
        std::array<index, Nd> idx;
        idx[0] = i;
        return ro_subview(
            this->array, idx, this->index_bases() + 1, this->shape() + 1);
      }

      template <typename T2, size_t... Is>
      static inline auto &_unroll_call(
          T2 &a, boost::array<index, Nd> const &idx,
          std::index_sequence<Is...>) {
        return a(idx[Is]...);
      }

      inline element const &
      operator()(boost::array<index, Nd> const &idx) const {
        return _unroll_call(this->array, idx, std::make_index_sequence<Nd>());
      }

      inline ret_element &operator()(boost::array<index, Nd> const &idx) {
        return _unroll_call(this->array, idx, std::make_index_sequence<Nd>());
      }
    };

    template <typename T, bool mut>
    class PyToFuseArray<T, 1, mut> : public PyToFuseArrayBase<T, 1, mut> {
    public:
      enum { dimensionality = 1 };
      typedef PyToFuseArrayBase<T, 1, mut> super_t;
      using super_t::super_t;
      typedef typename super_t::element element;
      typedef typename super_t::size_type size_type;
      typedef typename super_t::index index;

      inline element const &operator[](index i) const { return this->array(i); }
      inline element &operator[](index i) { return this->array(i); }

      inline element const &
      operator()(boost::array<index, 1> const &idx) const {
        return this->array(idx[0]);
      }
      inline element &operator()(boost::array<index, 1> const &idx) {
        return this->array(idx[0]);
      }

      inline element const *begin() const { return this->array.data(0); }
      inline element const *end() const {
        return this->array.data(this->size());
      }
    };

    class pythonHolder {
    protected:
      std::shared_ptr<void> hold;

    public:
      pythonHolder(std::shared_ptr<void> hold_) : hold(hold_) {}
    };

    template <typename T>
    py::object make_shared_ptr_hold(std::shared_ptr<T> &ptr) {
      return py::capsule(new pythonHolder(ptr), [](void *ptr1) {
        delete ((pythonHolder *)ptr1);
      });
    }

    template <typename T, size_t Nd>
    py::array makeNumpy(
        boost::multi_array_ref<T, Nd> const &x,
        std::shared_ptr<void> holder = std::shared_ptr<void>()) {
      std::array<ssize_t, Nd> shapes, strides;
      std::copy(x.shape(), x.shape() + shapes.size(), shapes.begin());
      for (int i = 0; i < Nd; i++)
        strides[i] = x.strides()[i] * sizeof(T);
      if (holder) {
        auto hold = make_shared_ptr_hold(holder);
        return py::array_t<T>(shapes, strides, x.data(), hold);
      } else {
        return py::array_t<T>(shapes, strides, x.data());
      }
    }

    template <typename T, size_t Nd>
    py::array makeNumpy(
        boost::multi_array_ref<T, Nd> &x,
        std::shared_ptr<void> holder = std::shared_ptr<void>()) {
      std::array<ssize_t, Nd> shapes, strides;
      std::copy(x.shape(), x.shape() + shapes.size(), shapes.begin());
      for (int i = 0; i < Nd; i++)
        strides[i] = x.strides()[i] * sizeof(T);
      if (holder) {
        auto hold = make_shared_ptr_hold(holder);
        return py::array_t<T>(shapes, strides, x.data(), hold);
      } else {
        return py::array_t<T>(shapes, strides, x.data());
      }
    }

  } // namespace Python
} // namespace LibLSS

#endif

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019
