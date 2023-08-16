/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/src/hades_julia3.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#define SAMPLER_DATA_INIT "ares_init.hpp"
#define SAMPLER_BUNDLE "julia_bundle.hpp"
#define SAMPLER_BUNDLE_INIT "julia_bundle_init.hpp"
#define SAMPLER_NAME "HADES3"
#define SAMPLER_MOCK_GENERATOR "julia_mock_gen.hpp"
#include "common/sampler_base.cpp"

#include "libLSS/tools/color_mod.hpp"
using namespace LibLSS::Color;

namespace {

  void init_splash() {

    static string splash_str[] = {

        "                                                                   ",
        "                    /\\_/\\____,          "
        "____________________________ ",
        "          ,___/\\_/\\ \\  ~     /                       " +
            fg(RED, "HADES+JULIA3", BRIGHT) + "          ",
        "          \\     ~  \\ )   XXX                                       ",
        "            XXX     /    /\\_/\\___,     (c) Jens Jasche 2012 - 2019",
        "  |---|        \\o-o/-o-o/   ~    /        Guilhem Lavaux 2014 - 2019",
        "    |           ) /     \\    XXX        "
        "____________________________ ",
        " \\  /          _|    / \\ \\_/                                       ",
        " ---        ,-/   _  \\_/   \\                                       ",
        "           / (   /____,__|  )                                      ",
        "          (  |_ (    )  \\) _|                                      ",
        "         _/ _)   \\   \\__/   (_                                     ",
        "        (,-(,(,(,/      \\,),),)                                    "
        "",
        "Please acknowledge XXXX",
    };

    static const int numSplashStr = sizeof(splash_str) / sizeof(splash_str[0]);

    for (int i = 0; i < numSplashStr; i++)
      Console::instance().print<LOG_STD>(splash_str[i]);
  }

  void close_splash() {}

  RegisterStaticInit reg_splash(init_splash, close_splash, 12);

} // namespace
