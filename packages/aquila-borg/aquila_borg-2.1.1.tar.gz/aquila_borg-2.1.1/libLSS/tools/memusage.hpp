#ifndef __LIBLSS_TOOLS_MEMUSAGE_HPP
#define __LIBLSS_TOOLS_MEMUSAGE_HPP

#include <sys/types.h>
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/static_auto.hpp"
#include "libLSS/tools/errors.hpp"
#include <map>
#include <string>

namespace LibLSS {
  struct AllocationDetail {
     ssize_t allocated, freed;
     size_t peak;
  };

  void report_allocation(size_t sz, const void *ptr);
  void report_free(size_t sz, const void *ptr);

  std::map<std::string, AllocationDetail> memoryReport();
  void clearReport();


  template<typename T>
  struct track_allocator: public std::allocator<T> {
  public:
    typedef typename std::allocator<T> parent;
    typedef typename parent::pointer pointer;
    typedef typename parent::size_type size_type;
    template<typename U> struct rebind { typedef track_allocator<U> other; };

    track_allocator() throw(): std::allocator<T>() {}
    track_allocator(const track_allocator& alloc) throw(): std::allocator<T>(alloc) {}
    template<typename U>
    track_allocator(const track_allocator<U>& alloc) throw(): std::allocator<T>(alloc) {}

    pointer allocate(size_type _Count, const void *_Hint = 0) {
      pointer p = std::allocator<T>::allocate(_Count, _Hint);
      if (p) {
	report_allocation(_Count*sizeof(T), _Hint);
      } else {
        error_helper<ErrorMemory>(boost::format("Memory allocation failed to allocate %d bytes") % (sizeof(T)*_Count));
      }
      return p;
    }
    void deallocate(pointer _Ptr, size_type _Count) {
      std::allocator<T>::deallocate(_Ptr, _Count);
      report_free(_Count*sizeof(T), _Ptr);
  }
  };
}

AUTO_REGISTRATOR_DECL(memory_alloc);

#endif
