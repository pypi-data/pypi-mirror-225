/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/uninitialized_type.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TOOLS_UNINITIALIZED_HPP
#define __LIBLSS_TOOLS_UNINITIALIZED_HPP
#pragma once

#include <boost/multi_array.hpp>
#include "libLSS/tools/memusage.hpp"
namespace LibLSS {

  template <
      typename T, std::size_t NumDims,
      typename Allocator = LibLSS::track_allocator<T>>
  class UninitializedAllocation {
  public:
    typedef boost::multi_array_ref<T, NumDims> array_type;

  private:
    T *ptr;
    Allocator allocator_;
    size_t maxNumElements;
    array_type *array_builder;

    UninitializedAllocation(UninitializedAllocation const &) {}
    UninitializedAllocation &operator=(UninitializedAllocation const &) {
      return *this;
    }

  public:
    // Implement a move constructor, but the copy constructor is disabled.
    UninitializedAllocation(UninitializedAllocation &&other)
        : ptr(other.ptr), array_builder(other.array_builder),
          maxNumElements(other.maxNumElements) {
      other.array_builder = 0;
      other.ptr = 0;
      other.maxNumElements = 0;
    }

    template <typename T2>
    explicit UninitializedAllocation(T2 extents, Allocator const &alloc)
        : allocator_(alloc), array_builder(new array_type(0, extents)) {
      typename Allocator::const_pointer no_hint = 0;
      ptr = allocator_.allocate(array_builder->num_elements(), no_hint);
      delete array_builder;
      array_builder = new array_type(ptr, extents);
      maxNumElements = array_builder->num_elements();
    }

    template <typename T2, typename Order>
    explicit UninitializedAllocation(
        T2 extents, Allocator const &alloc, const Order &order)
        : allocator_(alloc), array_builder(new array_type(0, extents, order)) {
      typename Allocator::const_pointer no_hint = 0;
      ptr = allocator_.allocate(array_builder->num_elements(), no_hint);
      delete array_builder;
      array_builder = new array_type(ptr, extents, order);
      maxNumElements = array_builder->num_elements();
    }

    template <typename T2>
    explicit UninitializedAllocation(T2 extents)
        : array_builder(new boost::multi_array_ref<T, NumDims>(0, extents)) {
      typename Allocator::const_pointer no_hint = 0;
      ptr = allocator_.allocate(array_builder->num_elements(), no_hint);
      delete array_builder;
      array_builder = new array_type(ptr, extents);
      maxNumElements = array_builder->num_elements();
    }

    template <typename T2>
    void reshape(T2 extents) {
      delete array_builder;
      array_builder = new array_type(ptr, extents);
      Console::instance().c_assert(
          array_builder->num_elements() <= maxNumElements, "Invalid reshaping");
    }

    ~UninitializedAllocation() {
      if (ptr != 0)
        allocator_.deallocate(ptr, array_builder->num_elements());
      if (array_builder != 0)
        delete array_builder;
    }

    T *get() { return ptr; }

    array_type &get_array() { return *array_builder; }

    operator array_type &() { return *array_builder; }
  };

  template <
      typename Array,
      typename Allocator = LibLSS::track_allocator<typename Array::element>>
  class UninitializedArray
      : public UninitializedAllocation<
            typename Array::element, Array::dimensionality, Allocator> {
  public:
    typedef UninitializedAllocation<
        typename Array::element, Array::dimensionality, Allocator>
        super_type;
    typedef typename super_type::array_type array_type;

    UninitializedArray(UninitializedArray<Array, Allocator> &&other)
        : super_type(std::forward<super_type>(other)) {}

    template <typename T2>
    explicit UninitializedArray(T2 extents, Allocator const &alloc)
        : super_type(extents, alloc) {}

    template <typename T2, typename Order>
    explicit UninitializedArray(
        T2 extents, Allocator const &alloc, const Order &order)
        : super_type(extents, alloc, order) {}

    template <typename T2>
    explicit UninitializedArray(T2 extents) : super_type(extents) {}
  };

  template <
      typename T, size_t N, typename Allocator = LibLSS::track_allocator<T>>
  using U_Array = UninitializedArray<boost::multi_array_ref<T, N>, Allocator>;
} // namespace LibLSS

#endif
