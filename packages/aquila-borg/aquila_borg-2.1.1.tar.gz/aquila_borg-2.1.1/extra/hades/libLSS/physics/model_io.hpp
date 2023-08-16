/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/model_io.hpp
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_PHYSICS_MODELIO_HPP
#  define __LIBLSS_PHYSICS_MODELIO_HPP

#  include <memory>
#  include "libLSS/physics/cosmo.hpp"
#  include "libLSS/mpi/generic_mpi.hpp"
#  include "libLSS/tools/mpi_fftw_helper.hpp"
#  include "libLSS/tools/errors.hpp"
#  include "libLSS/samplers/core/types_samplers.hpp"
#  include <boost/variant.hpp>

#  include "libLSS/physics/model_io/box.hpp"
#  include "libLSS/physics/model_io/base.hpp"
#  include "libLSS/physics/model_io/input.hpp"
#  include "libLSS/physics/model_io/output.hpp"

namespace LibLSS {

  using detail_input::ModelInput;
  using detail_input::ModelInputAdjoint;
  using detail_input::ModelInputBase;
  using detail_output::ModelOutput;
  using detail_output::ModelOutputAdjoint;
  using detail_output::ModelOutputBase;

} // namespace LibLSS

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019-2020
