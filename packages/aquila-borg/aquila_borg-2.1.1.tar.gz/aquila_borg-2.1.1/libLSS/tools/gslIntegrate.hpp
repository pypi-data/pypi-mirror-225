/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/gslIntegrate.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_INTEGRATE_HPP
#define __LIBLSS_INTEGRATE_HPP

#include <gsl/gsl_integration.h>
#include "libLSS/tools/gsl_error.hpp"

namespace LibLSS {

    namespace details {
        template<typename FunT>
        double gslSpecialFunction(double x, void *param)
        {
            const FunT *f = (const FunT *)param;

            return (*f)(x);
        }
    }

    template<typename FunT>
    double gslIntegrate(const FunT& v, double a, double b, double prec, int NPTS = 1024)
    {
        gsl_integration_workspace *w = gsl_integration_workspace_alloc(NPTS);
        gsl_function f;
        double result;
        double abserr;

        f.function = &details::gslSpecialFunction<FunT>;
        f.params = (void*)&v;

        gsl_integration_qag(&f, a, b, prec, 0, NPTS, GSL_INTEG_GAUSS61,
                    w, &result, &abserr);

        gsl_integration_workspace_free(w);

        return result;
    }

}

#endif
