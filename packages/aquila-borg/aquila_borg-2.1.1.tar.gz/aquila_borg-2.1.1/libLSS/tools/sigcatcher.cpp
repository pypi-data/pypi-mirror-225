/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/sigcatcher.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <algorithm>
#include <cstring>
#include <unistd.h>
#include <signal.h>
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/log_traits.hpp"
#include "libLSS/tools/sigcatcher.hpp"

AUTO_REGISTRATOR_IMPL(sigCatcher);

namespace LibLSS {

  namespace {

      template<typename iterator>
      iterator int_to_str_safe(iterator start, iterator max_end, int value)
      {
        int dec_place = 0;
        int save = value;
        iterator i = start, end;

        if (value == 0) {
          if (i == max_end) return i;
          *i++ = '0';
          return i;
        }

        while (i < max_end && value > 0) {
          *i = '0' + (value % 10);
          value /= 10;
          i++;
        }
        end = i;
        if (i != max_end) i--;
          
        
        while (start < i) {
          std::swap(*start, *i);
          start++;
          i--;
        }
        
        return end;
      }

      static void signalCatcher(int s) {
        static const int Nmax=1024;
        static char staticBuffer[Nmax];
        
        Console& cons = Console::instance();
        int rank = MPI_Communication::instance()->rank();
        int l;
        char *end;
        int rc;
        static const char SEGV_msg[] = "****** Handling SEGV ******\n";
        static const char SEGV_base[] = "SEGV on rank=";
        
        rc = write(2, SEGV_msg, sizeof(SEGV_msg)-1);
        strncpy(staticBuffer, SEGV_base, Nmax);
        l = sizeof(SEGV_base)-1;
        end = int_to_str_safe(staticBuffer + l, staticBuffer + Nmax, rank);
        
        if (end-staticBuffer < sizeof(staticBuffer))
          *end++ = '\n';
        
        rc = write(2, staticBuffer, end - staticBuffer);
        close(2);
        abort();
      }
    
      struct sigaction old_act;

      void initializeSigCatcher() {
        struct sigaction act;
        
        act.sa_handler = &signalCatcher;
        sigfillset(&act.sa_mask);
        act.sa_flags = SA_RESETHAND;
        sigaction(SIGSEGV, &act, &old_act);
      }

      void doneSigCatcher() {
        sigaction(SIGSEGV, &old_act, 0);
      }

      LibLSS::RegisterStaticInit reg(initializeSigCatcher, doneSigCatcher, 1, "SIGCATCHER"); // Just after console is initialized

  }
  
}
