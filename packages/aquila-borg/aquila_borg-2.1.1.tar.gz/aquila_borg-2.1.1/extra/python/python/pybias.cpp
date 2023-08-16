/*+
    ARES/HADES/BORG Package -- ./extra/python/python/pybias.cpp
    Copyright (C) 2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include "pyborg.hpp"

#include "pyfuse.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "pybias.hpp"
#include "libLSS/physics/bias/linear_bias.hpp"
#include "libLSS/physics/bias/power_law.hpp"
#include "libLSS/physics/bias/double_power_law.hpp"
#include "libLSS/physics/bias/broken_power_law.hpp"
//#include "libLSS/physics/bias/2nd_order_bias.hpp"
#include "libLSS/physics/bias/many_power.hpp"
#include "libLSS/physics/bias/eft_bias.hpp"

namespace py = pybind11;
using namespace pybind11::literals;


void LibLSS::Python::pyBias(py::module m) {

  py::class_<BaseBiasModel>(m, "BaseBiasModel")
      .def(
          "compute", &BaseBiasModel::compute, "borg_model"_a, "nmean"_a,
          "bias_params"_a, "density"_a, "biased_density"_a);

  py::class_<BiasModel<bias::PowerLaw>, BaseBiasModel>(m, "PowerLawBias")
      .def(py::init<>());

  py::class_<BiasModel<bias::DoubleBrokenPowerLaw>, BaseBiasModel>(
      m, "DoubleBrokenPowerLawBias")
      .def(py::init<>());

  py::class_<BiasModel<bias::BrokenPowerLaw>, BaseBiasModel>(
      m, "BrokenPowerLawBias")
      .def(py::init<>());

  py::class_<BiasModel<bias::LinearBias>, BaseBiasModel>(m, "LinearBias")
      .def(py::init<>());

  py::class_<BiasModel<bias::EFTBiasThresh, true>, BaseBiasModel>(
      m, "EFTBiasThreshold")
      .def(
          py::init<>([](double Lambda) {
            BiasModel<bias::EFTBiasThresh, true> *bias_model;
            bias_model = new BiasModel<bias::EFTBiasThresh, true>();
            LikelihoodInfo info;
            info["EFT_Lambda"] = Lambda;
            bias_model->bias = std::make_unique<bias::EFTBiasThresh>(info);
            return bias_model;
          }),
          "Lambda"_a);

  py::class_<BiasModel<bias::EFTBiasDefault, true>, BaseBiasModel>(
      m, "EFTBiasDefault")
      .def(
          py::init<>([](double Lambda) {
            BiasModel<bias::EFTBiasDefault, true> *bias_model;
            bias_model = new BiasModel<bias::EFTBiasDefault, true>();
            LikelihoodInfo info;
            info["EFT_Lambda"] = Lambda;
            bias_model->bias = std::make_unique<bias::EFTBiasDefault>(info);
            return bias_model;
          }),
          "Lambda"_a);

  /*py::class_<BiasModel<bias::SecondOrderBias>, BaseBiasModel>(
      m, "SecondOrderBias")
      .def(py::init<>());
*/

  //  py::class_<
  //      BiasModel<bias::ManyPower<bias::ManyPowerLevels<double, 1>>, true>,
  //      BaseBiasModel>(m, "MultiScalePowerBias_1")
  //      .def(py::init<>());
  /*    py::class_<BiasModel<bias::ManyPower<bias::ManyPowerLevels<double, 1, 1>> >, BaseBiasModel>(
      m, "MultiScalePowerBias_1_1")
      .def(py::init<>());
  py::class_<BiasModel<bias::ManyPower<bias::ManyPowerLevels<double, 2>> >, BaseBiasModel>(
      m, "MultiScalePowerBias_2")
      .def(py::init<>());
  py::class_<BiasModel<bias::ManyPower<bias::ManyPowerLevels<double, 2, 2>> >, BaseBiasModel>(
      m, "MultiScalePowerBias_2_2")
      .def(py::init<>());
*/
}

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019
