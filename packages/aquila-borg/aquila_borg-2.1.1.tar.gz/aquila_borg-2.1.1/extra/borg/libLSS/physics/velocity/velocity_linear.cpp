/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/velocity/velocity_linear.cpp
    Copyright (C) 2019-2020 Florent Leclercq <florent.leclercq@polytechnique.org>
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/physics/velocity/velocity_linear.hpp"

using namespace LibLSS;
using namespace LibLSS::VelocityModel;

typedef boost::multi_array<double, 4> VFieldType;
typedef UninitializedArray<VFieldType> U_VFieldType;

void LinearModel::getVelocityField(ARGS) {

  LibLSS::ConsoleContext<LOG_DEBUG> ctx("LinearModel::getVelocityField");

//.....
  
} //getVelocityField

void LinearModel::pushAG(ARGS) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
//.....
  }
} //pushAG

// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Florent Leclercq
// ARES TAG: year(0) = 2019-2020
// ARES TAG: email(0) = florent.leclercq@polytechnique.org
// ARES TAG: name(1) = Guilhem Lavaux
// ARES TAG: year(1) = 2019-2020
// ARES TAG: email(1) = guilhem.lavaux@iap.fr
