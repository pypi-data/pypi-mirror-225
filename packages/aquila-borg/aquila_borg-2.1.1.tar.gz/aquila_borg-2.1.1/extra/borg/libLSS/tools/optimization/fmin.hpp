#ifndef __LIBLSS_TOOLS_OPTIMIZATION_FMIN_HPP
#define __LIBLSS_TOOLS_OPTIMIZATION_FMIN_HPP

#include <functional>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/optimization/array_helper.hpp"

namespace LibLSS {

  namespace Optimization {

    static constexpr double SMALL_NUMBER = 1e-15;

    template<typename A>
    using Function = std::function<void(
            typename A::array_t &,
            typename A::array_t &)>;

    template <typename Search, typename Direction, typename ArrayAllocator>
    auto fmin(
        MPI_Communication* comm,
        Search &&search_function, Direction &&direction_function,
        Function<ArrayAllocator> gf,
        typename ArrayAllocator::array_t const &xstart,
        ArrayAllocator allocator = ArrayAllocator(), double const gtol = 1e-5,
        ssize_t maxIter = -1) -> decltype(allocator.new_like(xstart)) {
      auto xtmp = allocator.new_like(xstart);
      auto pk = allocator.new_like(xstart);
      auto pktmp = allocator.new_like(xstart);
      unsigned int k = 0;
      LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);

      static_assert(
          std::remove_reference<Search>::type::require_gradient,
          "This minimizer requires a search with gradient");
      static_assert(
          !std::remove_reference<Search>::type::require_function,
          "This minimizer requires not having access to the function itself.");

      *xtmp = xstart;

      while (k < maxIter or maxIter < 0) {
        double alpha;

        // Compute gradient at current position.
        gf(pktmp.get(), xtmp.get());
        if (k > 0)
          direction_function.storeNewStep_DeltaX(pktmp.get(), *(alpha*(*pk)));
        else
          direction_function.storeNewStep(pktmp.get(), xtmp.get());
        // Give this the direction algorithm
        direction_function.computeNextDirection(
            comm, pk.get(), pktmp.get(), xtmp.get());

        // pktmp is still the gradient

        // Give it also to lineSearch for seeding and tmp space.
        alpha = search_function.lineSearch(gf, xtmp, pk, pktmp, allocator);

        // Update position.
        *xtmp = *xtmp + alpha * (*pk);

        double pknorm = std::sqrt(dotprod(comm, *pk,*pk));
        double xnorm = std::sqrt(dotprod(comm, *xtmp,*xtmp));

        ctx.print(boost::format("k = %d, alpha = %g, pknorm = %g, xnorm = %g") % k % alpha % pknorm % xnorm);// % pk.get()[0] % xtmp.get()[0]);
        double eps1 = alpha*pknorm, eps2 = gtol*xnorm;
        ctx.print(boost::format("eps1 = %g, eps2 = %g") % eps1 % eps2);
        if (k >= 1) {
          ctx.print("Now we check");
          if (eps1 < eps2 || (xnorm < SMALL_NUMBER && eps1 < SMALL_NUMBER)) // If solution is zero we do not want eps1 to be infinitisimally small
           return xtmp;
          //ctx.print("Nope. Break it");
          //return xtmp;
        }
        k++;
      }
      return xtmp;
    }


    template <typename Search, typename Direction, typename ArrayAllocator, typename FunctionDelta>
    auto fminDeltaGradient(
        MPI_Communication* comm,
        Search &&search_function, Direction &&direction_function,
        Function<ArrayAllocator> gf,
        FunctionDelta gf_delta,
        typename ArrayAllocator::array_t const &xstart,
        ArrayAllocator allocator = ArrayAllocator(), double const gtol = 1e-5,
        ssize_t maxIter = -1) -> decltype(allocator.new_like(xstart)) {
      auto xtmp = allocator.new_like(xstart);
      auto pk = allocator.new_like(xstart);
      auto pktmp = allocator.new_like(xstart);
      auto delta_x = allocator.new_like(xstart);
      unsigned int k = 0;
      LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);

      static_assert(
          std::remove_reference<Search>::type::require_gradient,
          "This minimizer requires a search with gradient");
      static_assert(
          !std::remove_reference<Search>::type::require_function,
          "This minimizer requires not having access to the function itself.");

      *xtmp = xstart;

      gf(pktmp.get(), xtmp.get());

      while (k < maxIter or maxIter < 0) {
        double alpha;

        // Give this the direction algorithm
        direction_function.computeNextDirection(
            comm, pk.get(), pktmp.get(), xtmp.get());

        // pktmp is still the gradient

        // Give it also to lineSearch for seeding and tmp space.
        alpha = search_function.lineSearch(gf, xtmp, pk, pktmp, allocator);

        // Update position.
        *xtmp = *xtmp + alpha * (*pk);

        double pknorm = std::sqrt(dotprod(comm, *pk,*pk));
        double xnorm = std::sqrt(dotprod(comm, *xtmp,*xtmp));

        ctx.print(boost::format("k = %d, alpha = %g, pknorm = %g, xnorm = %g") % k % alpha % pknorm % xnorm);// % pk.get()[0] % xtmp.get()[0]);
        double eps1 = alpha*pknorm, eps2 = gtol*xnorm;
        ctx.print(boost::format("eps1 = %g, eps2 = %g") % eps1 % eps2);
        if (k >= 1) {
          ctx.print("Now we check");
          if (eps1 < eps2 || (xnorm < SMALL_NUMBER && eps1 < SMALL_NUMBER)) // If solution is zero we do not want eps1 to be infinitisimally small
           return xtmp;
          //ctx.print("Nope. Break it");
          //return xtmp;
        }

        // Compute gradient at current position.
        gf_delta(pktmp.get(), xtmp.get(), alpha*(*pk));
        direction_function.storeDeltaStep(pktmp.get(), *(alpha*(*pk)));

        k++;
      }
      return xtmp;
    }

  } // namespace Optimization
} // namespace LibLSS

#endif
