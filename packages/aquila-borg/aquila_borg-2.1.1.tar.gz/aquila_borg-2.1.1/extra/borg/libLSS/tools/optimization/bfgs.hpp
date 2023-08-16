/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tools/optimization/bfgs.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_TOOLS_OPTIMIZATION_BFGS_HPP
#  define __LIBLSS_TOOLS_OPTIMIZATION_BFGS_HPP

#  include "libLSS/tools/string_tools.hpp"
#  include <cmath>

namespace LibLSS {
  namespace Optimization {

    template <typename ArrayAllocator>
    struct lbfgs {
    public:
      enum : bool { require_gradient = true, require_function = false };
      typedef typename ArrayAllocator::holder_t holder_t;
      typedef typename ArrayAllocator::array_t array_t;
      typedef std::function<void(array_t &g)> priorFunction_t;
      typedef lbfgs<ArrayAllocator> self_t;
      ArrayAllocator allocator;
      holder_t prev_g, prev_x;
      bool strictMode;

      lbfgs(
          unsigned int numIterations_, ArrayAllocator alloc_ = ArrayAllocator())
          : numIterations(numIterations_), storedIterations(0),
            prev_delta_g(new holder_t[numIterations]),
            prev_delta_x(new holder_t[numIterations]),
            alphas(new double[numIterations]), betas(new double[numIterations]),
            allocator(alloc_), strictMode(true) {}

      void setPrior(priorFunction_t prior_) { prior = prior_; }

      ~lbfgs() {
        if (prev_delta_g != 0) {
          delete[] prev_delta_g;
          delete[] prev_delta_x;
          delete[] alphas;
          delete[] betas;
        }
      }

      void reset() { storedIterations = 0; }

      self_t &operator=(self_t const &other) {
        Console::instance().print<LOG_VERBOSE>(
            "LBFGS: Copying references from other LBFGS");
        Console::instance().c_assert(
            numIterations == other.numIterations,
            "LBFGS can copy only if memory allocation is the same.");
        storedIterations = other.storedIterations;
        for (int j = 0; j < storedIterations; j++) {
          Console::instance().print<LOG_VERBOSE>("copy");
          prev_delta_g[j] = other.prev_delta_g[j];
          prev_delta_x[j] = other.prev_delta_x[j];
        }
        Console::instance().print<LOG_VERBOSE>("finish copy 1");
        if (!prev_g && other.prev_g)
          prev_g = allocator.new_like(other.prev_g);
        Console::instance().print<LOG_VERBOSE>("finish copy 2");
        if (other.prev_g)
          *prev_g = *other.prev_g;
        Console::instance().print<LOG_VERBOSE>("finish copy 3");
        if (!prev_x && other.prev_x)
          prev_x = allocator.new_like(other.prev_x);
        Console::instance().print<LOG_VERBOSE>("finish copy 4");
        if (other.prev_x)
          *prev_x = *other.prev_x;
        Console::instance().print<LOG_VERBOSE>("done");
        return *this;
      }

      self_t &operator=(self_t &&other) {
        Console::instance().print<LOG_VERBOSE>(
            "LBFGS: Acquiring ownership of references from other LBFGS");
        if (prev_delta_g != 0)
          delete[] prev_delta_g;
        if (prev_delta_x != 0)
          delete[] prev_delta_x;
        if (alphas != 0)
          delete[] alphas;
        if (betas != 0)
          delete[] betas;
        prev_delta_g = other.prev_delta_g;
        prev_delta_x = other.prev_delta_x;
        alphas = other.alphas;
        betas = other.betas;
        storedIterations = other.storedIterations;
        numIterations = other.numIterations;
        other.alphas = 0;
        other.betas = 0;
        other.prev_delta_g = 0;
        other.prev_delta_x = 0;
        if (!prev_g && other.prev_g)
          prev_g = allocator.new_like(other.prev_g);
        if (other.prev_g)
          *prev_g = *other.prev_g;
        if (other.prev_x)
          *prev_x = *other.prev_x;
      }

      void shift_history() {
        if (storedIterations > 0) {
          for (int i = std::min(numIterations - 2, storedIterations - 1);
               i >= 0; i--) {
            prev_delta_g[i + 1] = std::move(prev_delta_g[i]);
            prev_delta_x[i + 1] = std::move(prev_delta_x[i]);
          }
        }
      }

      template <typename ArrayDeltaG, typename ArrayDeltaX>
      void
      storeDeltaStep(ArrayDeltaG const &delta_gk, ArrayDeltaX const &delta_xk) {
        shift_history();

        prev_delta_g[0] = allocator.new_like(delta_gk);
        prev_delta_x[0] = allocator.new_like(delta_xk);
        *(prev_delta_g[0]) = delta_gk; // Save gk
        *(prev_delta_x[0]) = delta_xk; // Save xk

        Console::instance().print<LOG_DEBUG>(
            boost::format("Delta gradient is %g") %
            dotprod(
                MPI_Communication::instance(), *(prev_delta_g[0]),
                *(prev_delta_g[0])));
        Console::instance().print<LOG_DEBUG>(
            boost::format("Delta position is %g") %
            dotprod(
                MPI_Communication::instance(), *(prev_delta_x[0]),
                *(prev_delta_x[0])));
        Console::instance().print<LOG_DEBUG>(
            boost::format("Delta cross is %g") %
            dotprod(
                MPI_Communication::instance(), *(prev_delta_x[0]),
                *(prev_delta_g[0])));

        storedIterations = std::min(numIterations, storedIterations + 1);
      }

      template <typename ArrayDeltaG, typename ArrayDeltaX>
      void storeNewStep_DeltaX(ArrayDeltaG const &gk, ArrayDeltaX &delta_xk) {
        storeDeltaStep(*(allocator.wrapper(gk) - *prev_g), delta_xk);
        *prev_g = gk;
        *prev_x = *prev_x + delta_xk;
      }

      template <typename G, typename X>
      void storeNewStep(G const &gk, X const &xk) {
        if (prev_g && prev_x)
          storeDeltaStep(
              *(allocator.wrapper(gk) - *prev_g),
              *(allocator.wrapper(xk) - *prev_x));
        if (!prev_g)
          prev_g = allocator.new_like(gk);
        *prev_g = gk;
        if (!prev_x)
          prev_x = allocator.new_like(xk);
        *prev_x = xk;
      }

      void setStrictMode(bool on) { strictMode = on; }

      void computeNextDirection(
          MPI_Communication *comm, array_t &new_pk, array_t const &gk,
          array_t const & /* x is ignored in BFGS*/) {
        // Make an alias
        LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
        // `q` is a wrapped array around new_pk
        auto q = allocator.wrapper(new_pk);

        // `q` is assigned the opposite of the wrapped gk
        // so new_pk contains -gk now.
        q = -allocator.wrapper(gk);
        if (storedIterations <= 1) {
          return;
        }

        unsigned int m = storedIterations;

        if (m >= 2) {
          for (unsigned int i = 0; i <= m - 2; i++) {
            auto y = *(prev_delta_g[i]);
            auto s = *(prev_delta_x[i]);
            double rho = 1.0 / dotprod(comm, y, s);
            ctx.format(
                "rho = %g, ref = %g", rho,
                std::sqrt(dotprod(comm, y, y) * dotprod(comm, s, s)));
            if (rho < 0) {
              ctx.print2<LOG_WARNING>("Hessian is negative (1).");
              if (strictMode)
                error_helper<ErrorBadState>("Hessian is bad");
            }
            alphas[i] = dotprod(comm, s, q) * rho;
            q = q - alphas[i] * y;
          }
        }
        {
          auto y = *(prev_delta_g[m - 1]);
          auto s = *(prev_delta_x[m - 1]);
          double const dp0 = dotprod(comm, y, s);
          double const dp1 = dotprod(comm, y, y);
          double const rho0 = (dotprod(comm, y, s) / dotprod(comm, y, y));
          ctx.format("rho0 = %g", rho0);
          ctx.format("dp0 = %g", dp0);
          ctx.format("dp1 = %g", dp1);
          ctx.format("dp2 = %g", dotprod(comm, s, s));
          if (rho0 < 0) {
            ctx.print2<LOG_WARNING>("Hessian is negative (2).");
            if (strictMode)
              error_helper<ErrorBadState>("Hessian is bad");
          }
          if (prior)
            prior(*q);
          q = rho0 * q;
        }
        if (m >= 2) {
          for (int i = m - 2; i >= 0; i--) {
            auto y = *(prev_delta_g[i]);
            auto s = *(prev_delta_x[i]);
            double rho = 1.0 / dotprod(comm, y, s);
            ctx.format("rho(2) = %g", rho);
            betas[i] = dotprod(comm, y, q) * rho;
            if (rho < 0) {
              ctx.print2<LOG_WARNING>("Hessian is negative (3).");
              if (strictMode)
                error_helper<ErrorBadState>("Hessian is bad");
            }
            q = q + (alphas[i] - betas[i]) * s;
          }
        }
        // Now q is the new_pk.
      }

    private:
      unsigned int numIterations, storedIterations;
      holder_t *prev_delta_g, *prev_delta_x;
      double *alphas;
      double *betas;
      priorFunction_t prior;
    };

    template <typename ArrayAllocator, typename Gradient>
    void bootstrap_lbfgs(
        lbfgs<ArrayAllocator> &dir, Gradient const &g,
        typename ArrayAllocator::array_t &x, double epsilon) {
      auto tmp_grad = dir.allocator.new_like(x);
      auto tmp_grad2 = dir.allocator.new_like(x);
      auto x2 = dir.allocator.new_like(x);
      *x2 = dir.allocator.wrapper(x) * (1 - epsilon);
      g(tmp_grad.get(), x);
      *x2 = dir.allocator.wrapper(x) * (1 + epsilon);
      g(tmp_grad2.get(), x2.get());
      *tmp_grad = *tmp_grad2 - *tmp_grad;
      dir.storeDeltaStep(
          tmp_grad.get(), *(2 * epsilon * dir.allocator.wrapper(x)));

      dir.prev_x = dir.allocator.new_like(x);
      *dir.prev_x = *x2;
      dir.prev_g = std::move(tmp_grad2);
    }

  } // namespace Optimization
} // namespace LibLSS

#endif
