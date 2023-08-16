/*+
    ARES/HADES/BORG Package -- ./src/ares3.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#define SAMPLER_DATA_INIT "../ares_init.hpp"
#define SAMPLER_BUNDLE "../ares_bundle.hpp"
#define SAMPLER_BUNDLE_INIT "../ares_bundle_init.hpp"
#define SAMPLER_NAME "ARES3"
#define SAMPLER_MOCK_GENERATOR "../ares_mock_gen.hpp"
#include "common/sampler_base.cpp"

#include "libLSS/tools/color_mod.hpp"
using namespace LibLSS::Color;

namespace {

  void init_splash() {

    static string splash_str[] = {
        "                                               ",
        "       o                                       ",
        "    ,-.|____________________                   ",
        " O==+-|(>-------- --  -     .>                 ",
        "    `- |\"\"\"\"\"\"\"d88b\"\"\"\"\"\"\"\"\"                   ",
        "     | o     d8P 88b                           ",
        "     |  \\    98=, =88                          ",
        "     |   \\   8b _, 88b                         ",
        "     `._ `.   8`..'888                         ",
        "      |    \\--'\\   `-8___        __________________________________",
        "      \\`-.              \\                        " +
            fg(RED, "ARES3", BRIGHT) + "             ",
        "        `. \\ -       - / <          (c) Jens Jasche 2012 - 2019    ",
        "          \\ `---   ___/|_-\\             Guilhem Lavaux 2014 - 2019 ",
        "           |._      _. |_-|      __________________________________",
        "           \\  _     _  /.-\\                    ",
        "            | -! . !- ||   |                   ",
        "            \\ \"| ^ |\" /\\   |                   ",
        "            =oO)<>(Oo=  \\  /                   ",
        "             d8888888b   < \\                   ",
        "            d888888888b  \\_/                   ",
        "            d888888888b                        ",
        "",
        "Please acknowledge:",
        " - Jasche, Kitaura, Wandelt, 2010, MNRAS, 406, 1 (arxiv 0911.2493)",
        " - Jasche & Lavaux, 2015, MNRAS, 447, 2 (arxiv 1402.1763)",
        " - Lavaux & Jasche, 2016, MNRAS, 455, 3 (arxiv 1509.05040)"};

    static const int numSplashStr = sizeof(splash_str) / sizeof(splash_str[0]);

    for (int i = 0; i < numSplashStr; i++)
      Console::instance().print<LOG_STD>(splash_str[i]);
  }

  void close_splash() {}

  RegisterStaticInit reg_splash(init_splash, close_splash, 12);

} // namespace
