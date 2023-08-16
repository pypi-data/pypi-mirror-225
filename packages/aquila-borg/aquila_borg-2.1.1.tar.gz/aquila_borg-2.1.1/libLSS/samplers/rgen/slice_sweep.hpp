/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/rgen/slice_sweep.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef _LIBLSS_SLICE_SWEEP_HPP
#define _LIBLSS_SLICE_SWEEP_HPP

#include "libLSS/mpi/generic_mpi.hpp"
#include <cmath>

// These algorithms are described in https://www.aquila-consortium.org/wiki/index.php/File:Slice_sampling_Neal_97.pdf


namespace LibLSS {

  namespace slice_details {
    template<typename LogLikelihood>
    double request(MPI_Communication *comm, LogLikelihood lh, double a, int ROOT) {
      int job = 1;
      comm->broadcast_t(&job, 1, ROOT);
      comm->broadcast_t(&a, 1, ROOT);
      return lh(a);
    }

    inline void shutdown(MPI_Communication *comm, double a, int ROOT) {
      int job = 0;
      comm->broadcast_t(&job, 1, ROOT);
      comm->broadcast_t(&a, 1, ROOT);
    }

    inline int grab_job(MPI_Communication *comm, double& a, int ROOT) {
      int job;
      comm->broadcast_t(&job, 1, ROOT);
      comm->broadcast_t(&a, 1, ROOT);
      return job;
    }
  }

  template<typename Random, typename LogLikelihood>
  double slice_sweep(MPI_Communication *comm, Random& rng, LogLikelihood lh, double a0, double step, int ROOT = 0)
  {
Console::instance().print<LOG_DEBUG>("Doing slicesweep EARLY init");
    if (comm->rank() != ROOT) {
      double v;
      while (slice_details::grab_job(comm, v, ROOT)) {
        lh(v);
      }
      return v;
    }

Console::instance().print<LOG_DEBUG>("Doing slicesweep init");
    double logp0 = slice_details::request(comm, lh, a0, ROOT);
    double logu = logp0 + std::log(1-rng.uniform());//draw from (0,1], to avoid log(0)
    Console::instance().c_assert(!std::isnan(logu), "logu must not be a NaN");
    double rr = rng.uniform();
    double al = a0 - rr*step;
    double ar = a0 + (1-rr)*step;
    
Console::instance().print<LOG_DEBUG>(boost::format("First loop (logu = %lg)") % logu);
    while (true) {
      double logpl = slice_details::request(comm, lh, al, ROOT);
      if (logpl < logu)
        break;
      al -= step;
    }
    
Console::instance().print<LOG_DEBUG>("Second loop");
    while (true) { 
      double logpr = slice_details::request(comm, lh, ar, ROOT);
      if (logpr < logu)
        break;
      ar += step;
    }
    
Console::instance().print<LOG_DEBUG>("Last loop");
    while (true) {
      double a1 = rng.uniform() * (ar - al) + al;
      double logp1 = slice_details::request(comm, lh, a1, ROOT);
      
      if (logp1 > logu) {
        slice_details::shutdown(comm, a1, ROOT);
        return a1;
      } else {
        // Shrink bracket
        if (a1 > a0) 
          ar = a1;
        else
          al = a1;
      }
    }
  }

  template<typename Random, typename LogLikelihood>
  double slice_sweep(Random& rng, LogLikelihood lh, double a0, double step)
  {
    double logp0 = lh(a0);
    double logu = logp0 + std::log(1-rng.uniform());//draw from (0,1], to avoid log(0)
    Console::instance().c_assert(!std::isnan(logu), "logu must not be a NaN");
    double rr = rng.uniform();
    double al = a0 - rr*step;
    double ar = a0 + (1-rr)*step;
    
    while (true) {
      double logpl = lh(al);
      if (logpl < logu)
        break;
      al -= step;
    }
    
    while (true) { 
      double logpr = lh(ar);
      if (logpr < logu)
        break;
      ar += step;
    }
    
    while (true) {
      double a1 = rng.uniform() * (ar - al) + al;
      double logp1 = lh(a1);
      
      if (logp1 > logu) {
        return a1;
      } else {
        // Shrink bracket
        if (a1 > a0) 
          ar = a1;
        else
          al = a1;
      }
    }
  }

  template<typename Random, typename LogLikelihood>
  double slice_sweep_double(MPI_Communication *comm, Random& rng, LogLikelihood lh, double a0, double step, int ROOT = 0)
  {
    ConsoleContext<LOG_DEBUG> ctx("slicesweep_double");

    if (comm->rank() != ROOT) {
      double v;
      while (slice_details::grab_job(comm, v, ROOT)) {
        lh(v);
      }
      return v;
    }

    ctx.print("INIT");
    // Find the initial likelihood and the slice level
    double logp0 = slice_details::request(comm, lh, a0, ROOT);
    double logu = logp0 + std::log(1-rng.uniform());//draw from (0,1], to avoid log(0)
    Console::instance().c_assert(!std::isnan(logu), "logu must not be a NaN");

    double rr = rng.uniform();
    double al = a0 - rr*step;
    double ar = a0 + (1-rr)*step;
    
    ctx.print(boost::format("Step defining loop (logu = %lg)") % logu);
    double logpl = slice_details::request(comm, lh, al, ROOT);
    double logpr = slice_details::request(comm, lh, ar, ROOT);
    while (logpl >= logu || logpr >= logu) {
      double v= rng.uniform();
      if (v < 0.5) {
        al -= (ar - al);
        logpl = slice_details::request(comm, lh, al, ROOT);
        ctx.print(boost::format("new al=%g, logpl = %g") % al % logpl);
      } else {
        ar += (ar - al);
        logpr = slice_details::request(comm, lh, ar, ROOT);
        ctx.print(boost::format("new ar=%g, logpr = %g") % ar % logpr);
      }
    }
    
    ctx.print("Sampling loop");
    while (true) {
      double a1 = rng.uniform() * (ar - al) + al;
      double logp1 = slice_details::request(comm, lh, a1, ROOT);
      
      if (logp1 > logu) {
        double ar_hat = ar;
        double al_hat = al;
        double logpl_hat = slice_details::request(comm, lh, al_hat, ROOT);
        double logpr_hat = slice_details::request(comm, lh, ar_hat, ROOT);
        bool not_accepted = false;

        ctx.print(boost::format("Got a candidate at a1=%g") % a1);

        while ((ar_hat - al_hat) > (1.1*step) && !not_accepted) {
          double am = 0.5 * (ar_hat+al_hat);

          bool D = ((a0 < am && a1 >= am) || (a0 >= am && a1 < am));

          if (a1 < am) {
            ar_hat = am;
            logpr_hat = slice_details::request(comm, lh, ar_hat, ROOT);
          } else {
            al_hat = am;
            logpl_hat = slice_details::request(comm, lh, al_hat, ROOT);
          }

          ctx.print(boost::format("ar_hat=%lg, al_hat=%lg, logpl_hat=%lg, logpr_hat=%lg, D=%d") % ar_hat % al_hat % logpl_hat % logpr_hat % D);

          if (D && logu >= logpl_hat && logu >= logpr_hat) {
            // Not acceptable. Try again.
            ctx.print("Not good");
            not_accepted = true;
          }
        }

        // Go back outside
        if (not_accepted)
          continue;

        slice_details::shutdown(comm, a1, ROOT);
        return a1;
      } else {
        // Shrink bracket
        if (a1 > a0) 
          ar = a1;
        else
          al = a1;
      }
    }
  }

}

#endif
