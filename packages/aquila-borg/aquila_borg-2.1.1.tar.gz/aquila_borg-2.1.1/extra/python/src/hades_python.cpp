/*+
    ARES/HADES/BORG Package -- ./extra/python/src/hades_python.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#define SAMPLER_DATA_INIT "ares_init.hpp"
#define SAMPLER_BUNDLE "python_bundle.hpp"
#define SAMPLER_BUNDLE_INIT "python_bundle_init.hpp"
#define SAMPLER_NAME "HADES-PYTHON3"
#define SAMPLER_MOCK_GENERATOR "python_mock_gen.hpp"
#include "common/sampler_base.cpp"

#include "libLSS/tools/color_mod.hpp"
using namespace LibLSS::Color;

namespace {

  void init_splash() {

    static std::vector<std::string> splash_str = {
	 " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
	 "       PPPPPPP  YY  YY   TTTTTT  HH   HH     ooo     NN     N",
         "      PPP   PP  YY YY      TT    HH   HH   oO  Oo    NNn    N",
	 "     PP   PPP    YYY       TT    HH   HH  oOO  OOo   N Nn   N",
	 "     PPPPPP      YYY       TT    HHHHHHH  Oo    oO   N  Nn  N",
	 "     PPP         iYi       ll    HH   HH  oO    Oo   N  nN nN",
         "     PP           Y        ii    hh   hh   OO  OO    N   Nn n",
         "     P            Y        ii    hh   hh    oooo     n    NNN",
	 " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
         " This is HADES-Python"
    };

    Console::instance().print<LOG_STD>(splash_str);
  }

  void close_splash() {}

  RegisterStaticInit reg_splash(init_splash, close_splash, 12);

} // namespace
