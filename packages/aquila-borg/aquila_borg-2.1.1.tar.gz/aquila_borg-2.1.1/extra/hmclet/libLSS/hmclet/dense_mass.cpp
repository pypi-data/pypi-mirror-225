/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/hmclet/dense_mass.cpp
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
#include "libLSS/hmclet/dense_mass.hpp"
#include "libLSS/tools/string_tools.hpp"
#include "libLSS/tools/hdf5_scalar.hpp"

using namespace LibLSS;
using namespace LibLSS::HMCLet;
namespace ph = std::placeholders;
using boost::format;

void DenseMassMatrix::saveMass(CosmoTool::H5_CommonFileGroup &g) {
  boost::multi_array<double, 2> mass_buf(boost::extents[numParams][numParams]);
  boost::multi_array<double, 1> mean_buf(boost::extents[numParams]);
  Eigen::Map<Eigen::MatrixXd> map_buf(mass_buf.data(), numParams, numParams);

  map_buf.noalias() = covariances;
  Eigen::Map<Eigen::VectorXd>(mean_buf.data(), numParams).noalias() = mean;
  CosmoTool::hdf5_write_array(g, "covariance", mass_buf);
  CosmoTool::hdf5_write_array(g, "mean", mean_buf);

  map_buf.noalias() = icCovar;
  CosmoTool::hdf5_write_array(g, "icCovariance", mass_buf);
  hdf5_save_scalar(g, "numInMass", numInMass);

  map_buf.noalias() = finishedCovariances;
  CosmoTool::hdf5_write_array(g, "finishedCovariances", mass_buf);
}

void DenseMassMatrix::loadMass(CosmoTool::H5_CommonFileGroup &g) {
  boost::multi_array<double, 2> mass_buf(boost::extents[numParams][numParams]);
  boost::multi_array<double, 1> mean_buf(boost::extents[numParams]);
  Eigen::Map<Eigen::MatrixXd> map_buf(mass_buf.data(), numParams, numParams);
  auto& cons = Console::instance();

  CosmoTool::hdf5_read_array(g, "covariance", mass_buf, false);
  covariances = map_buf;
  CosmoTool::hdf5_read_array(g, "icCovariance", mass_buf, false);
  icCovar = map_buf;
  CosmoTool::hdf5_read_array(g, "finishedCovariances", mass_buf, false);
  finishedCovariances.noalias() = map_buf;
  CosmoTool::hdf5_read_array(g, "mean", mean_buf, false);
  numInMass = hdf5_load_scalar<size_t>(g, "numInMass");
  mean = Eigen::Map<Eigen::VectorXd>(mean_buf.data(), numParams);
  Console::instance().print<LOG_INFO>("loaded mass.");

  lltOfCovariances.compute(finishedCovariances);
}

void DenseMassMatrix::addMass(VectorType const &params) {
  if (frozen)
    return;
    
  using CosmoTool::square;
  auto f_params = Eigen::Map<const Eigen::VectorXd>(params.data(), numParams);
  double coef = double(numInMass) / double(numInMass + 1);
  double coef2 = 1 / double(numInMass);
  double coef3 = 1 / double(numInMass + 1);

  if (numInMass == 0)
    mean = f_params;
  else
    mean = coef * mean + coef3 * f_params;

  if (numInMass >= 1) {
    auto c = f_params - mean;
    covariances = coef * covariances + coef2 * c * c.adjoint();
  }

  numInMass++;
  finishMass();
}

void DenseMassMatrix::finishMass() {
  ConsoleContext<LOG_DEBUG> ctx("DenseMassMatrix::finishMass");

  double w = initialMassWeight / double(initialMassWeight + numInMass);
  double const corrector = limiter;

  finishedCovariances = (1-w)*covariances + w*icCovar;
  for (int i = 0; i < numParams; i++) {
    for (int j = 0; j < numParams; j++) {
      if (i!=j)
	    finishedCovariances(i,j) /= (1+corrector);
    }
  }
  lltOfCovariances.compute(finishedCovariances);
}

void DenseMassMatrix::clear() {
  ConsoleContext<LOG_DEBUG> ctx("DenseMassMatrix::clear");
  covariances.fill(0);
  finishedCovariances.fill(0);
  mean.fill(0);
  numInMass = 0;
  initialMassWeight = 10;
  finishMass();
}

void DenseMassMatrix::setInitialMass(
    boost::multi_array_ref<double, 2> const &massMatrix) {
  if (massMatrix.shape()[0] != numParams || massMatrix.shape()[1] != numParams)
    error_helper<ErrorBadState>("Invalid mass matrix size");

  for (size_t i = 0; i < numParams; i++) {
    for (size_t j = 0; j < numParams; j++) {
      icCovar(i, j) = massMatrix[i][j];
    }
  }
  initialMassWeight = 10;
  finishMass();
}
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: name(0) = 2019
