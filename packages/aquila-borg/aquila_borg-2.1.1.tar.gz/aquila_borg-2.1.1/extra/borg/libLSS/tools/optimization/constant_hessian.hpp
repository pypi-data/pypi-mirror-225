/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tools/optimization/constant_hessian.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TOOLS_OPTIMIZATION_CONSTANT_HESSIAN_HPP
#define __LIBLSS_TOOLS_OPTIMIZATION_CONSTANT_HESSIAN_HPP

#include "libLSS/tools/string_tools.hpp"
#include <cmath>

namespace LibLSS {
  namespace Optimization {

    template <typename ArrayAllocator>
    struct constantHessian {
    public:
      enum : bool { require_gradient = false, require_function = false };
      typedef typename ArrayAllocator::holder_t holder_t;
      typedef typename ArrayAllocator::array_t array_t;
      typedef std::function<void(array_t& g)> priorFunction_t;

      constantHessian(
          double const mulFactor_, ArrayAllocator alloc_ = ArrayAllocator())
          : mulFactor(mulFactor_),
            allocator(alloc_) {}

      void setPrior(priorFunction_t prior_) { prior = prior_; }

      ~constantHessian() {
      }

      void computeNextDirection(
          array_t &new_pk, array_t const &gk, array_t const &xk, bool const update = true) {
        // Make an alias
        auto q = allocator.wrapper(new_pk);

        q = -mulFactor*allocator.wrapper(gk);

	if (prior)
          prior(*q);
        // Now q is the new_pk.
      }

    private:
      ArrayAllocator allocator;
      priorFunction_t prior;
      double mulFactor;
    };
  } // namespace Optimization
} // namespace LibLSS

#endif
