/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/log_traits.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <boost/preprocessor/seq/for_each.hpp>
#include "log_traits.hpp"
#include "libLSS/tools/color_mod.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/static_auto.hpp"
#include <iostream>

using namespace LibLSS;
using namespace std;

#define IMPLEMENT_LOG_TRAIT(T) \
string LibLSS::T::prefix = ""; \
string LibLSS::T::prefix_c = ""; \
ostream *LibLSS::T::os[LibLSS::T::numOutput];

#define DO_IMPLEMENT(r, DATA, E) IMPLEMENT_LOG_TRAIT(E)

#if !defined(DOXYGEN_SHOULD_SKIP_THIS)
BOOST_PP_SEQ_FOR_EACH(DO_IMPLEMENT, DATA,
  (LOG_STD)
  (LOG_WARNING)
  (LOG_ERROR)
  (LOG_INFO)
  (LOG_DEBUG)
  (LOG_VERBOSE)
  (LOG_INFO_SINGLE)
);
#endif

bool LibLSS::QUIET_CONSOLE_START = false;


namespace  {
void initializeConsole()
{
    using namespace LibLSS::Color;

    if (!LibLSS::QUIET_CONSOLE_START)
      cout << "Initializing console." << endl;
    LOG_STD::prefix   =     "[STD    ] ";
    LOG_STD::prefix_c =     "[STD    ] ";
    LOG_STD::os[0] = &std::cout;

    LOG_WARNING::prefix   = "[WARNING] ";
    LOG_WARNING::prefix_c = "[" + fg(MAGENTA,"WARNING",BRIGHT) + "] ";
    LOG_WARNING::os[0] = &std::cout;
    LOG_WARNING::os[1] = &std::cerr;

    LOG_ERROR::prefix     =   "[ERROR  ] ";
    LOG_ERROR::prefix_c   =   "[" + fg(RED, "ERROR",BRIGHT) +"  ] ";
    LOG_ERROR::os[0] = &std::cerr;

    LOG_INFO::prefix  =     "[INFO   ] ";
    LOG_INFO::prefix_c=     "[" + bg(BLACK,fg(YELLOW, "INFO", BRIGHT)) +"   ] ";
    LOG_INFO::os[0] = &std::cout;

    LOG_INFO_SINGLE::prefix  =     "[INFO S ] ";
    LOG_INFO_SINGLE::prefix_c=     "[" + bg(BLACK,fg(YELLOW, "INFO S", BRIGHT)) +" ] ";
    LOG_INFO_SINGLE::os[0] = &std::cout;

    LOG_DEBUG::prefix  =    "[DEBUG  ] ";
    LOG_DEBUG::prefix_c=    "[DEBUG  ] ";
    LOG_DEBUG::os[0] = &std::cout;

    LOG_VERBOSE::prefix  =  "[VERBOSE] ";
    LOG_VERBOSE::prefix_c=  "[" + bg(BLACK,fg(CYAN, "VERBOSE", BRIGHT)) + "] ";
    LOG_VERBOSE::os[0] = &std::cout;

    if (LibLSS::QUIET_CONSOLE_START)
      Console::instance().setVerboseLevel<LOG_ERROR>();
}

RegisterStaticInit reg(initializeConsole, 0);

}

AUTO_REGISTRATOR_IMPL(LogTraits);
