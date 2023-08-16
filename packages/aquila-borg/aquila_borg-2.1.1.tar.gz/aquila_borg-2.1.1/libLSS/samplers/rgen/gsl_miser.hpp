/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/rgen/gsl_miser.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __GSL_RANDOM_NUMBER_MISER_HPP
#define __GSL_RANDOM_NUMBER_MISER_HPP

#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_monte.h>
#include <gsl/gsl_monte_miser.h>
#include <cstring>
#include "libLSS/tools/errors.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"

namespace LibLSS {

  /**
   * This is an adaptor class for the MISER integrator in GSL.
   * It handles the life cycle of the MISER object, and support for a generic
   * functor for the integrand.
   */
  class GSL_Miser {
  protected:
    gsl_monte_miser_state *state;
    size_t Nd;

    template<typename Functor>
    struct MiserCall {
      Functor f;
      
      MiserCall(Functor g) : f(g) {}
    };

    template<typename Functor>
    static double adaptor_functor(double *x, size_t, void *params)
    {
      MiserCall<Functor> *c = (MiserCall<Functor> *) params;
      
      return c->f(x);
    }
  
  public:
    /**
     * Constructor.
     * @param dim number of dimensions over which the integration will occur.
     */
    GSL_Miser(size_t dim) 
      : state(0), Nd(dim) {
      state = gsl_monte_miser_alloc(dim);
    }
    
    /**
     * Destructor.
     */
    ~GSL_Miser() {
      gsl_monte_miser_free(state);
    }
    
    /**
     * Integrate the provided integrand over some range, with a maximum number of calls. A bound
     * on the maximum error is returned.
     * Here is a use example:
     *
     * @code
     *   // ...
     *   size_t calls = 10;
     *   double xl[2] = {0, 0};
     *   double xu[2] = {1, 2};
     *   double value;
     *
     *   GSL_Miser miser(2);   // 2-dimensions
     *   value = miser.integrate(rng, [](double *x) {
     *     // do something with x[0], x[1]
     *     return x[0]*x[0] + x[1]*x[1]; // for example sum(x^2)
     *   }, xl, xu, calls, abserr);
     *   //...
     * @endcode
     *
     * @param rng Class adapting the GSL random number generator
     * @param f Functor representing the integrand. It must have one pointer to double and return a double.
     * @param xl lower bound for integration (N-dimension contiguous C-array)
     * @param xu upper bound for integration
     * @param calls maximum number of calls
     * @param abserr return medium for estimated maximum absolute error
     *
     */
    // Only valid for GSL
    template<typename Functor,typename A>
    double integrate(GSL_RandomNumber& rng, Functor f, A& xl, A& xu, size_t calls, double &abserr) {
      gsl_monte_function mf;
      MiserCall<Functor> call(f);
      double result;
      int err;

      mf.f = &adaptor_functor<Functor>;
      mf.dim = Nd;
      mf.params = &call;
      
      if ((err = gsl_monte_miser_integrate(&mf, &xl[0], &xu[0], Nd, calls, rng.rng, state, &result, &abserr)) != GSL_SUCCESS)
        error_helper<ErrorGSL>(boost::format("Error while doing monte carlo integration: error code = %d ") % err);
      return result;
    }
    
    /**
     * Use a multi-threaded random number generator deriving from a base "Rng".
     * This is a helper class to unwrap the GSL base class for the random number generation.
     * @see integrate(GSL_RandomNumber& rng, Functor f, A& xl, A& xu, size_t calls, double &abserr) 
     */ 
    template<typename Rng, typename Functor, typename A>
    double integrate(RandomNumberThreaded<Rng>& rng, Functor f, A& xl, A& xu, size_t calls, double &abserr) {
      return integrate(rng.base(), f, xl, xu, calls, abserr);
    }
  };

}

#endif
