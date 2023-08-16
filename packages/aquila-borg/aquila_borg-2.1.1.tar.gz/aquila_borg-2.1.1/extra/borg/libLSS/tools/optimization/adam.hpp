#ifndef __LIBLSS_TOOLS_OPTIMIZATION_ADAM_HPP
#define __LIBLSS_TOOLS_OPTIMIZATION_ADAM_HPP

#include <functional>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/optimization/array_helper.hpp"

namespace LibLSS {

  namespace Optimization {

    template <typename ArrayAllocator>
    auto adam(std::function<void(
            typename ArrayAllocator::array_t &,
            typename ArrayAllocator::array_t &)>
            gf,
        typename ArrayAllocator::array_t const &xstart,
        ArrayAllocator allocator = ArrayAllocator(), double const alpha = 1e-2,
	double const beta_1 = 0.9, 
	double const beta_2 = 0.999, 
	double const epsilon = 1e-8,
	 double const epsstop = 1e-6, 
	ssize_t   T = 10000) -> decltype(allocator.new_like(xstart)) {

	auto xtmp = allocator.new_like(xstart);
	auto  g_t = allocator.new_like(xstart);
      	auto  m_t = allocator.new_like(xstart);
	auto  m_cap = allocator.new_like(xstart);
      	auto  v_t = allocator.new_like(xstart);  
	auto  v_cap = allocator.new_like(xstart);

      unsigned int t = 0;
      LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);

      //set initial values	
      *xtmp = xstart;

      // Compute gradient at current position.
      gf(g_t.get(), xtmp.get());

      double gn = dotprod(*g_t, *g_t); //get gradient norm

      while ((t < T) and (gn > epsstop * epsstop)) {

	gn = 0.0;

	*m_t = beta_1 * (*m_t) +
                   (1.0 - beta_1) *
                       (*g_t); //updates the moving averages of the gradient
          (*v_t) =
              beta_2 * (*v_t) +
              (1.0 - beta_2) *
                  ((*g_t) *
                   (*g_t)); //updates the moving averages of the squared gradient

          (*m_cap) =
              (*m_t) /
              (1.0 -
               (pow(beta_1, t + 1))); //calculates the bias-corrected estimates
          (*v_cap) =
              (*v_t) /
              (1.0 -
               (pow(beta_2, t + 1))); //calculates the bias-corrected estimates

          (*xtmp) = (*xtmp)-
              (alpha * (*m_cap) /
               (sqrt((*v_cap)) + epsilon)); //updates the parameters

          gn = dotprod(*g_t, *g_t); //get gradient norm

	// Compute gradient at current position.
      	gf(g_t.get(), xtmp.get());	

	 t++;
	}
	
      return xtmp;
    }
  } // namespace Optimization
} // namespace LibLSS

#endif
