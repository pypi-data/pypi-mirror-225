/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/hdf5_error.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <H5Cpp.h>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/static_init.hpp"
#include <boost/format.hpp>
#include "libLSS/tools/hdf5_error.hpp"

using namespace LibLSS;

namespace {
    
    herr_t console_h5e_walker(unsigned int n, const H5E_error_t *err_desc, void *client_data)
    {
        const char *maj_str = NULL;
        const char *min_str = NULL;
        const int indent = 2;
        ConsoleContext<LOG_ERROR> *ctx = (ConsoleContext<LOG_ERROR> *)client_data;
        
        /* Check arguments */
        assert (err_desc);

        /* Get descriptions for the major and minor error numbers */
        maj_str = H5Eget_major (err_desc->maj_num);
        min_str = H5Eget_minor (err_desc->min_num);
        
        /* Print error message */
        ctx->print(boost::format("#%03d: %s line %u in %s(): %s") % n
                  % err_desc->file_name
                  % err_desc->line
                  % err_desc->func_name
                  % err_desc->desc);
    
        return 0;
        
    }
    
    herr_t console_errorPrinter(hid_t, void *cdata)
    {
        ConsoleContext<LOG_ERROR> ctx("HDF5 error");
        H5::Exception::walkErrorStack (H5E_WALK_DOWNWARD, console_h5e_walker, &ctx);
    
        return 0;
    }
    
    void initializeHDF5()  {
        H5E_auto2_t func = console_errorPrinter;
        H5::Exception::setAutoPrint(func, 0);
    }
    
    // After console initialization.
    RegisterStaticInit reg(initializeHDF5, 1);
}

AUTO_REGISTRATOR_IMPL(HDF5);
