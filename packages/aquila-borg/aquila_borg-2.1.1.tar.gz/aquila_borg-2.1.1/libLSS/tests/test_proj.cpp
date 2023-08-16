/*+
    ARES/HADES/BORG Package -- ./libLSS/tests/test_proj.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <H5Cpp.h>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/data/spectro_gals.hpp"
#include "libLSS/data/projection.hpp"
#include "libLSS/data/galaxies.hpp"

using namespace LibLSS;

int main(int argc, char **argv)
{
    MPI_Communication *comm = setupMPI(argc, argv);
    H5::H5File f("toto.h5", H5F_ACC_TRUNC);
    typedef GalaxySurvey<NoSelection, BaseGalaxyDescriptor> SurveyType;

    SurveyType survey;
    SurveyType::GalaxyType galaxy;

    galaxy.id = 0;
    galaxy.phi = 1.0;
    galaxy.theta = 0.1;
    galaxy.r = 10.;
    galaxy.zo = 1000;

    survey.addGalaxy(galaxy);

    survey.save(f);
    survey.restoreMain(f);
    return 0;
}

