/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_rgen.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <H5Cpp.h>
#include <stdlib.h>
#include <boost/chrono.hpp>
#include <boost/format.hpp>
#include "libLSS/tools/static_init.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"

using namespace LibLSS;
using boost::chrono::system_clock;
using boost::chrono::duration;
using boost::format;
using boost::str;

static const long int LOOP_NO = 100000000;

int main()
{
    StaticInit::execute();
    
    Console::instance().setVerboseLevel<LOG_DEBUG>();
    
    RandomNumberThreaded<GSL_RandomNumber> rgen(-1);
    system_clock::time_point start = system_clock::now();
    
#pragma omp parallel for schedule(static)
    for (long l = 0; l < LOOP_NO; l++)
        rgen.get();
        
    
    duration<double> perf = system_clock::now() - start;
    
    Console::instance().print<LOG_INFO>(format("Number / sec = %lg Mint / sec") % (LOOP_NO/perf.count()/1000000) );

    {
        H5::H5File f("PRNG.state", H5F_ACC_TRUNC);
        rgen.save(f);
    }
 
    try {
        RandomNumberThreaded<GSL_RandomNumber> rgen2(2*smp_get_max_threads());
        H5::H5File f("PRNG.state", 0);
        rgen2.restore(f);
        abort();
        Console::instance().print<LOG_ERROR>("Did not get any error. Bad");
    }
    catch (const ErrorBadState& s) {
        Console::instance().print<LOG_INFO>("Got error. Exact");
    }

    try {
        RandomNumberThreaded<GSL_RandomNumber> rgen2(-1);
        H5::H5File f("PRNG.state", 0);
        rgen2.restore(f);
    }
    catch (const ErrorBase& s) {
        Console::instance().print<LOG_ERROR>("Got an error. Bad");
        abort();
    }

    
    return 0;
}
