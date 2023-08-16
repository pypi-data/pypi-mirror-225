/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tools/optimization/newton.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TOOLS_OPTIMIZATION_NEWTON_HPP
#define __LIBLSS_TOOLS_OPTIMIZATION_NEWTON_HPP

#include "libLSS/tools/fused_assign.hpp"

namespace LibLSS {
  namespace Optimization {

    template <typename ArrayAllocator>
    struct newton {
    public:
      enum : bool { require_gradient = true, require_function = false };
      typedef typename ArrayAllocator::holder_t holder_t;
      typedef typename ArrayAllocator::array_t array_t;
      typedef std::function<void(array_t &H_g, array_t const &x)>
          hessian_func_t;

      hessian_func_t hessian;
      ArrayAllocator allocator;

      newton(hessian_func_t hessian_, ArrayAllocator alloc_ = ArrayAllocator())
          : hessian(hessian_), allocator(alloc_) {}
      ~newton() {}

      template<typename ArrayDeltaG,typename ArrayDeltaX>
      void storeNewStep(ArrayDeltaG const&, ArrayDeltaX const& ) {}
      template<typename ArrayDeltaG,typename ArrayDeltaX>
      void storeDeltaStep(ArrayDeltaG const&, ArrayDeltaX const& ) {}
      template<typename ArrayDeltaG,typename ArrayDeltaX>
      void storeNewStep_DeltaX(ArrayDeltaG const&, ArrayDeltaX const& ) {}

      void computeNextDirection(
          MPI_Communication* comm, array_t &new_pk, array_t const &gk, array_t const &xk) {
        auto q = allocator.wrapper(new_pk);
        q = allocator.wrapper(gk);
        hessian(new_pk, xk);
        q = -q;
      }
    };

  } // namespace Optimization
} // namespace LibLSS

#endif
