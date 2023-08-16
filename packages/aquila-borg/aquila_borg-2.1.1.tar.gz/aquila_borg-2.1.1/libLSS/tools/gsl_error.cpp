/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/gsl_error.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/static_init.hpp"
#include <boost/format.hpp>
#include "libLSS/tools/gsl_error.hpp"
#include <gsl/gsl_errno.h>

using namespace LibLSS;

namespace {

  bool s_gsl_error_fatal = true;

  void console_errorPrinter(const char *reason, const char *file, int line, int gsl_errno)
  {
    ConsoleContext<LOG_ERROR> ctx("GSL error");
    ctx.print(boost::format("An error has occurred at %1%:%2%, the given reason is \"%3%\"")
      % file % line % reason);

    if (s_gsl_error_fatal) {
      ctx.print("Aborting run");
      MPI_Communication::instance()->abort();
    }
  }



  void initializeGSL_Error()  {
    Console::instance().print<LOG_DEBUG>("Initialize GSL error reporter");
    gsl_set_error_handler (console_errorPrinter);
  }

  // After console initialization.
  RegisterStaticInit reg(initializeGSL_Error, 1);
}

void LibLSS::setGSLFatality(bool on ) {
  s_gsl_error_fatal = on;
}

AUTO_REGISTRATOR_IMPL(GSL_Error);
