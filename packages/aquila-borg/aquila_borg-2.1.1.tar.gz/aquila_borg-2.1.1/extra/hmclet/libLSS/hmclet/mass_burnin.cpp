/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/hmclet/mass_burnin.cpp
    Copyright (C) 2014-2020 2019 <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

#include <boost/format.hpp>
#include <functional>
#include <cmath>
#include "libLSS/tools/console.hpp"
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/tools/symplectic_integrator.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/samplers/rgen/slice_sweep.hpp"
#include "libLSS/hmclet/mass_burnin.hpp"
#include "libLSS/tools/string_tools.hpp"
#include "libLSS/tools/hdf5_scalar.hpp"
#include "libLSS/tools/itertools.hpp"

using namespace LibLSS;
using namespace LibLSS::HMCLet;
namespace ph = std::placeholders;
using boost::format;

template <typename Matrix>
void MassMatrixWithBurnin<Matrix>::saveMass(CosmoTool::H5_CommonFileGroup &g) {

  super_t::saveMass(g);

  hdf5_save_scalar(g, "stepID", stepID);
  Console::instance().print<LOG_VERBOSE>("Handling memory");
  for (auto m : itertools::enumerate(memory)) {
    int id = m.template get<0>();
    auto const &a = m.template get<1>();
    std::string s = str(boost::format("memory_%d") % id);
    Console::instance().print<LOG_VERBOSE>(
        boost::format("Saving memory %d / %s") % id % s);
    CosmoTool::hdf5_write_array(g, s, a);
  }
}

template <typename Matrix>
void MassMatrixWithBurnin<Matrix>::loadMass(CosmoTool::H5_CommonFileGroup &g) {
  super_t::loadMass(g);

  stepID = hdf5_load_scalar<size_t>(g, "stepID");
  if (stepID > burninMaxIteration)
    return;

  memory.clear();
  for (auto r : itertools::range(0, memorySize)) {
    boost::multi_array<double, 1> m;
    try {
      CosmoTool::hdf5_read_array(g, str(boost::format("memory_%d") % r), m);
    } catch (H5::Exception) {
      break;
    }
    memory.push_back(m);
  }
}

template <typename Matrix>
void MassMatrixWithBurnin<Matrix>::clear() {
  super_t::clear();
  memory.clear();
}

template <typename Matrix>
void MassMatrixWithBurnin<Matrix>::addMass(VectorType const &params) {
  stepID++;
  // If burnin is done, just proceed normally.
  if (stepID > burninMaxIteration) {
//    memory.clear();
//    super_t::addMass(params);
    return;
  }

  memory.push_back(params);

  if (memory.size() > memorySize) {
    memory.pop_front();
    super_t::clear();
    // Very dumb algorithm
    for (auto &old_params : memory)
      super_t::addMass(old_params);
  } else {
    super_t::addMass(params);
  }
}

#include "libLSS/hmclet/diagonal_mass.hpp"
template class LibLSS::HMCLet::MassMatrixWithBurnin<DiagonalMassMatrix>;
#include "libLSS/hmclet/dense_mass.hpp"
template class LibLSS::HMCLet::MassMatrixWithBurnin<DenseMassMatrix>;

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: name(0) = 2019
