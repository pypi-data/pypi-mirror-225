/*+
    ARES/HADES/BORG Package -- ./extra/borg/src/hades_lya.cpp
    Copyright (C) 2020 Natalia Porqueres <n.porqueres@imperial.ac.uk>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#define SAMPLER_DATA_INIT "hades_lya_init.hpp"
#define SAMPLER_BUNDLE "hades_lya_bundle.hpp"
#define SAMPLER_BUNDLE_INIT "hades_lya_bundle_init.hpp"
#define SAMPLER_NAME "HADES_LYA"
#define SAMPLER_MOCK_GENERATOR "hades_mock_gen.hpp"
#include "common/sampler_base.cpp"


#include "libLSS/tools/color_mod.hpp"
using namespace LibLSS::Color;

namespace {

void init_splash()
{

static string splash_str[] = {

 "                                                                   ",
 "                    /\\_/\\____,          ____________________________ ",
 "          ,___/\\_/\\ \\  ~     /                       " + fg(RED, "HADES_LYA", BRIGHT) + "      ",
 "          \\     ~  \\ )   XXX                                       ",
 "            XXX     /    /\\_/\\___,     (c) Jens Jasche 2012 - 2017",
 "               \\o-o/-o-o/   ~    /        Guilhem Lavaux 2014 - 2017",
 "                ) /     \\    XXX        ____________________________ ",
 "               _|    / \\ \\_/                                       ",
 "            ,-/   _  \\_/   \\                                       ",
 "           / (   /____,__|  )                                      ",
 "          (  |_ (    )  \\) _|                                      ",
 "         _/ _)   \\   \\__/   (_                                     ",
 "        (,-(,(,(,/      \\,),),)                                    "
 "",
 "Please acknowledge XXXX",
};

static const int numSplashStr = sizeof(splash_str)/sizeof(splash_str[0]);

    for (int i = 0; i < numSplashStr; i++)
        Console::instance().print<LOG_STD>(splash_str[i]);
}

void close_splash()  {}

RegisterStaticInit reg_splash(init_splash, close_splash, 12);

}
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Natalia Porqueres
// ARES TAG: email(0) = n.porqueres@imperial.ac.uk
// ARES TAG: year(0) = 2020

