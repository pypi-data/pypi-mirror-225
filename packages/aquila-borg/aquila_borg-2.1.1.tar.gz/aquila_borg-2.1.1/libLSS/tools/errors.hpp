/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/errors.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TOOLS_ERRORS_HPP
#define __LIBLSS_TOOLS_ERRORS_HPP

#include "libLSS/tools/console.hpp"
#include <exception>
#include <string>

namespace LibLSS {

    class ErrorBase: virtual public std::exception {
    private:
        std::string message;
        ErrorBase() {}
    public:
        ErrorBase(const std::string& m) : message(m) {}
        ErrorBase(const boost::format& m) : message(m.str()) {}
        virtual ~ErrorBase() throw () {}
        
        virtual const char *what() const throw() { return message.c_str(); }
    };

#define LIBLSS_NEW_ERROR(TNAME) \
    class TNAME: virtual public ErrorBase { \
    public: \
        TNAME(const std::string& m): ErrorBase(m) {} \
        TNAME(const boost::format& m): ErrorBase(m) {} \
        virtual ~TNAME() throw () {} \
    };

    LIBLSS_NEW_ERROR(ErrorIO);
    LIBLSS_NEW_ERROR(ErrorBadState);
    LIBLSS_NEW_ERROR(ErrorMemory);
    LIBLSS_NEW_ERROR(ErrorParams);
    LIBLSS_NEW_ERROR(ErrorBadCast);
    LIBLSS_NEW_ERROR(ErrorNotImplemented);
    LIBLSS_NEW_ERROR(ErrorGSL);
    LIBLSS_NEW_ERROR(ErrorLoadBalance);

    template<typename Error>
    [[ noreturn ]] void error_helper(const std::string& msg) {
        Console::instance().print<LOG_ERROR>(msg);
        Console::instance().print_stack_trace();
        throw Error(msg);
    }

    template<typename Error>
    [[ noreturn ]] void error_helper(const boost::format& msg) {
        Console::instance().print<LOG_ERROR>(msg.str());
        Console::instance().print_stack_trace();
        throw Error(msg);
    }

};

#endif
