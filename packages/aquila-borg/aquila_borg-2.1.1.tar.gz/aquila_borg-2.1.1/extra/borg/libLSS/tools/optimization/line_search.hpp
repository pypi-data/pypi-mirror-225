/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tools/optimization/line_search.hpp
    Copyright (C) 2018-2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TOOLS_OPTIMIZATION_LINE_SEARCH_HPP
#define __LIBLSS_TOOLS_OPTIMIZATION_LINE_SEARCH_HPP

#include "libLSS/tools/string_tools.hpp"

namespace LibLSS {

  namespace Optimization {

    class lineSearchOnlyGrad {
    public:
      enum : bool { require_gradient = true, require_function = false };

    private:
      double c2, reducer;
      unsigned int maxIteration;
      double alpha_start;

    public:
      lineSearchOnlyGrad(
          double c2_, double reducer_, unsigned int maxIter,
          double alpha_start_ = 1.0)
          : c2(c2_), reducer(reducer_), maxIteration(maxIter),
            alpha_start(alpha_start_) {}

      template <typename GradientFunction, typename Array, typename Allocator>
      double lineSearch(
          GradientFunction const &gf, Array const &x0, Array const &pk,
          Array &pktmp, Allocator &alloc) {
        static_assert(is_holder<Array>::value, "Array must be a holder type");
        double alpha = alpha_start * (1 - 0.01*drand48());
        double r;
        // pktmp is the gradient
        // r2 = -c2 × (pk ⋅ ∇f(x0))
        double r2 = -dotprod(*pk, *pktmp);
        unsigned int iter = 0;


        auto x1 = alloc.new_like(x0.get());

        // pk is the search direction (typically the opposite of the gradient)
        do {
          if (iter > 0)
            alpha *= reducer * (1  - 0.01*drand48());
          *x1 = *x0 + alpha * (*pk);
          gf(pktmp.get(), x1.get());
          // r = -(pk ⋅ ∇f(x1))
          r = -dotprod(*pk, *pktmp);
          iter++;
          Console::instance().print<LOG_DEBUG>(boost::format("r is %g, r2 is %g") % r % r2);
          if (r > r2) { // if slope is higher then break
            Console::instance().print<LOG_DEBUG>(boost::format("Breaking because slope is increasing negatively ((r=%g) > (r2=%g))") % r % r2);
            break;
          } else if (std::abs(r) < c2*std::abs(r2)) { // Otherwise we need the amplitude to be lower
            Console::instance().print<LOG_DEBUG>(boost::format("Breaking because slope is flattening (abs(r=%g) < c2*abs(r2=%g))") % r % r2);
            break;
          }
        } while (iter < maxIteration);
        return alpha;
      }
    };

  } // namespace Optimization
} // namespace LibLSS

#endif

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2018-2019
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
