/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/fftw_allocator.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_FFTW_ALLOCATOR_HPP
#define __LIBLSS_FFTW_ALLOCATOR_HPP

#include "libLSS/tools/align_helper.hpp"
#include "libLSS/tools/errors.hpp"
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/tools/memusage.hpp"

namespace LibLSS {

    template<typename T>
    class FFTW_Allocator {
    public:
        typedef T value_type;
        typedef T *pointer;
        typedef T& reference;
        typedef const T* const_pointer;
        typedef const T& const_reference;
        typedef size_t size_type;
        typedef ptrdiff_t difference_type;
        size_type minAllocSize;
        template<class U> struct rebind { typedef FFTW_Allocator<U> other; };

        pointer address(reference x) const { return &x; }
        const_pointer address(const_reference x) const { return &x; }

        FFTW_Allocator() : minAllocSize(0) {}

        pointer allocate(size_type n, const void *p = 0) {
            if (n > this->max_size()) {
                error_helper<ErrorMemory>("Failed allocation");
            }
            n = std::max(n, minAllocSize) * sizeof(T);
        //    Console::instance().print_memory<LOG_DEBUG>(n);
            pointer ret = (pointer)fftw_malloc(n);
            if (ret == 0)
              error_helper<ErrorMemory>(boost::format("FFTW malloc failed to allocate %d elements") % n);
            report_allocation(n, ret);
            return ret;
        }

        void deallocate(pointer p, size_type n) {
            fftw_free(p);
            report_free(n*sizeof(T), p);
        }

        size_t max_size() const throw() {
            return size_t(-1) / sizeof(T);
        }

        void construct(pointer p, const_reference val) {
            ::new((void *)p) T(val);
        }

        void destroy(pointer p) {
            p->~T();
        }
    };

    template<typename T> inline bool operator==(const FFTW_Allocator<T>&, const FFTW_Allocator<T>&) { return true; }
    template<typename T> inline bool operator!=(const FFTW_Allocator<T>&, const FFTW_Allocator<T>&) { return false; }

    template<typename T>
    struct DetectAlignment<FFTW_Allocator<T> > {
        enum { Align = Eigen::Aligned };
    };

}

#endif
