/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/rgen/gsl_random_number.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __GSL_RANDOM_NUMBER_HPP
#define __GSL_RANDOM_NUMBER_HPP

#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <cstring>
#include "libLSS/tools/errors.hpp"
#include "libLSS/samplers/core/random_number.hpp"

namespace LibLSS {

  class GSL_RandomNumber: public RandomNumber
  {
  public:
    gsl_rng *rng;

    GSL_RandomNumber() :
        rng(gsl_rng_alloc(gsl_rng_mt19937)) {
    }

    ~GSL_RandomNumber() {
        gsl_rng_free(rng);
    }

    virtual double uniform() {
        return gsl_rng_uniform(rng);
    }

    virtual double unitexp() {
          return gsl_ran_exponential(rng, 1.);
    }

    virtual void seed(unsigned long i) {
        Console::instance().print<LOG_DEBUG>(boost::format("GSL: Changing random number generation seed with %ld") % i);
        gsl_rng_set(rng, i);
    }

    virtual unsigned long get() {
        return gsl_rng_get(rng);
    }

    using RandomNumber::poisson;
    using RandomNumber::gaussian;
    using RandomNumber::gamma;
    using RandomNumber::negative_binomial;

    virtual unsigned int poisson(double mean) {
        return gsl_ran_poisson(rng, mean);
    }

    virtual unsigned int negative_binomial(double p, double n) {
        return gsl_ran_negative_binomial(rng, p, n);
    }

    virtual double gamma(double a, double b) {
        return gsl_ran_gamma(rng, a, b);
    }

    virtual void save(H5_CommonFileGroup& g) {
        boost::multi_array<char, 1> out(boost::extents[gsl_rng_size(rng)]);
        ::memcpy(out.origin(), gsl_rng_state(rng), gsl_rng_size(rng));
        CosmoTool::hdf5_write_array(g, "state", out);
    }

    virtual void restore(H5_CommonFileGroup& g, bool flexible) {
        size_t sz = gsl_rng_size(rng);
        boost::multi_array<char, 1> in;

        CosmoTool::hdf5_read_array(g, "state", in);


        if (in.shape()[0] != sz) {
            error_helper<ErrorIO>("Could not read state in GSL_RandomNumber");
        }
        memcpy(gsl_rng_state(rng), in.origin(), sz);
    }
  };


};

#endif
