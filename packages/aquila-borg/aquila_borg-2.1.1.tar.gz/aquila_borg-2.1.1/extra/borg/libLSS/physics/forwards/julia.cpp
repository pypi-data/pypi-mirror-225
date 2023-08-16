/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/julia.cpp
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <boost/format.hpp>
#include "libLSS/julia/julia.hpp"
#include "libLSS/physics/forwards/julia.hpp"

using namespace LibLSS;
using boost::format;
using boost::str;

static inline std::string forward_module_initialize(std::string const &mname) {
  return mname + ".Forward";
}

static inline std::string forward_module_adjoint(std::string const &mname) {
  return mname + ".adjoint_gradient";
}

static inline std::string forward_module_forward(std::string const &mname) {
  return mname + ".forward";
}

Julia::Object Julia::make_simulation_box(const BoxModel &box) {
  Object o;

  return Julia::evaluate(
      str(format("libLSS.BoxModel((%g,%g,%g),[%u,%u,%u])") % box.L0 % box.L1 %
          box.L2 % box.N0 % box.N1 % box.N2));
}

JuliaForward::JuliaForward(
    MPI_Communication *comm, const BoxModel &box, const std::string &code_name,
    const std::string &_module_name)
    : BORGForwardModel(comm, box), module_name(_module_name) {
  Console::instance().print<LOG_INFO>(
      "Loading code " + code_name + " in julia VM");
  // TODO, only reevaluate if needed
  Julia::evaluate("include(\"" + code_name + "\")");

  // Create the adequate julia object.
  forward_object = Julia::invoke(
      forward_module_initialize(module_name), Julia::make_simulation_box(box));
}

JuliaForward::~JuliaForward() {
  // forward_object self destruct here.
}

void JuliaForward::forwardModel_v2(ModelInput<3> delta_init) {
//  Julia::Object init_d = Julia::box(delta_init);
//
//  Julia::invoke(
//      forward_module_forward(module_name), forward_object, init_d); 
}

void JuliaForward::getDensityFinal(ModelOutput<3> delta_out) {
}


void JuliaForward::adjointModel_v2(ModelInputAdjoint<3> in_gradient) {}
void JuliaForward::getAdjointModelOutput(ModelOutputAdjoint<3> in_gradient) {}

void JuliaForward::releaseParticles() {}

void JuliaForward::updateCosmo() {}

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019-2020
