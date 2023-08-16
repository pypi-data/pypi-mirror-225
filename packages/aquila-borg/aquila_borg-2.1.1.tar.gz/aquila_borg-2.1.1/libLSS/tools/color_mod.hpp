/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/color_mod.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_COLOR_MOD_HPP
#define __LIBLSS_COLOR_MOD_HPP

#include <string>
#include <boost/format.hpp>

namespace LibLSS {

    namespace Color {
    
        enum ColorValue {
            BLACK = 0,
            RED = 1,
            GREEN = 2,
            YELLOW = 3,
            BLUE = 4,
            MAGENTA = 5,
            CYAN = 6,
            WHITE = 7
        };
        
        enum ColorIntensity {
            NORMAL = 0,
            BRIGHT = 1
        };
        
        inline std::string fg(ColorValue c, const std::string& text, ColorIntensity i = NORMAL, bool is_console = true) {
            if (is_console)
                return boost::str(boost::format("\x1b[%d;%dm%s\x1b[39;0m") % ((int)c + 30) % (int)i % text);
            else
                return text;
        }

        inline std::string bg(ColorValue c, const std::string& text, ColorIntensity i = NORMAL, bool is_console = true) {
            if (is_console)
                return boost::str(boost::format("\x1b[%d;%dm%s\x1b[49;0m") % ((int)c + 40) % (int)i % text);
            else
                return text;
        }
    
    }

}

#endif
