/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/hmclet/diagonal_mass.cpp
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
#include "libLSS/hmclet/diagonal_mass.hpp"
#include "libLSS/tools/string_tools.hpp"
#include "libLSS/tools/hdf5_scalar.hpp"

using namespace LibLSS;
using namespace LibLSS::HMCLet;
namespace ph = std::placeholders;
using boost::format;

void DiagonalMassMatrix::saveMass(CosmoTool::H5_CommonFileGroup &g) {
  CosmoTool::hdf5_write_array(g, "mass", masses);
  CosmoTool::hdf5_write_array(g, "mean", mean);
  CosmoTool::hdf5_write_array(g, "icMass", icMass);
  hdf5_save_scalar(g, "numInMass", numInMass);
  hdf5_save_scalar(g, "frozen", frozen);
}

void DiagonalMassMatrix::loadMass(CosmoTool::H5_CommonFileGroup &g) {
  CosmoTool::hdf5_read_array(g, "mass", masses);
  CosmoTool::hdf5_read_array(g, "mean", mean);
  CosmoTool::hdf5_read_array(g, "icMass", icMass);
  numInMass = hdf5_load_scalar<size_t>(g, "numInMass");
  frozen = hdf5_load_scalar<bool>(g, "frozen");
  fwrap(inv_sqrt_masses) = std::sqrt(1 / fwrap(masses));
}

void DiagonalMassMatrix::addMass(VectorType const &params) {

  if (frozen)
    return;

  using CosmoTool::square;
  auto f_mean = fwrap(mean);
  auto f_variances = fwrap(variances);
  auto f_params = fwrap(params);
  double coef = double(numInMass) / double(numInMass + 1);
  double coef2 = 1 / double(numInMass);
  double coef3 = 1 / double(numInMass + 1);

  if (numInMass == 0)
    f_mean = f_params;
  else
    f_mean = coef * f_mean + coef3 * f_params;
  if (numInMass >= 1) {
    auto c = f_params - f_mean;
    f_variances = coef * f_variances + coef2 * c * c;
  }

  numInMass++;
  finishMass();
}

void DiagonalMassMatrix::finishMass() {
  ConsoleContext<LOG_DEBUG> ctx("DiagonalMassMatrix::finishMass");

  auto fm = fwrap(variances);

  double w = initialMassWeight / double(initialMassWeight + numInMass);
  auto f_M = fwrap(masses);
  auto f_inv_sq = fwrap(inv_sqrt_masses);

  f_M = (1 - w) * fm + w * fwrap(icMass);
  f_inv_sq = std::sqrt(1 / f_M);

  ctx.print("mass weight = " + to_string(f_M.max() * 1e5));
  ctx.print("inv_sqrt_masses weight = " + to_string(f_inv_sq.max()));
}

void DiagonalMassMatrix::clear() {
  fwrap(variances) = 0;
  fwrap(masses) = 0;
  fwrap(mean) = 0;
  numInMass = 0;
  initialMassWeight = 5;
  finishMass();
}

void DiagonalMassMatrix::setInitialMass(
    VectorType const &diagonal_mass_matrix) {
  fwrap(icMass) = diagonal_mass_matrix;
  initialMassWeight = 5;
  finishMass();
}
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: name(0) = 2019
