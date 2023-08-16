/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_console.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/timing_db.hpp"
#include "libLSS/tools/hdf5_error.hpp"

using namespace std;
using LibLSS::LOG_STD;
using LibLSS::LOG_WARNING;
using LibLSS::LOG_ERROR;
using boost::format;

static void funInit()
{
    cout << "Dummy static init test" << endl;
}

LibLSS::RegisterStaticInit test_reg(funInit);

int main(int argc, char **argv)
{
    LibLSS::MPI_Communication *mpi_world = LibLSS::setupMPI(argc, argv);

    LibLSS::StaticInit::execute();
    LibLSS::Console& console = LibLSS::Console::instance();

    unlink("timings.h5");
    {
    H5::H5File f("timings.h5", H5F_ACC_TRUNC);
    LibLSS::timings::load(f);
    }

    console.print<LOG_STD>("Test console");
    console.print<LOG_WARNING>("Test warning console");
    console.print<LOG_ERROR>("Test error console");

    LibLSS::Progress<LOG_STD>& p = console.start_progress<LOG_STD>("Test progress", 10);

    console.indent();
    console.print<LOG_STD>("test indent");

    for (int j = 0; j < 10; j++)
    {
        p.update(j);
        console.print<LOG_STD>("indented");
        console.indent();
    }
    p.destroy();
    
    console.print<LOG_STD>(format("This is a formatter test %d, %g") % -2 % 4.3);
    console.format<LOG_STD>("This is a formatter test2 %d, %g", -2, 4.3);

    {
      LIBLSS_AUTO_CONTEXT(LOG_STD, ctx);
      ctx.print("Now in context");
    }

    {
    H5::H5File f("timings.h5", H5F_ACC_TRUNC);
    LibLSS::timings::save(f);
    }

    console.print_stack_trace();

    LibLSS::StaticInit::finalize();
    return 0;
}
