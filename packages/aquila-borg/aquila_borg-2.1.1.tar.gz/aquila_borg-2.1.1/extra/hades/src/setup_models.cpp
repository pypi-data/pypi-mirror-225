/*+
    ARES/HADES/BORG Package -- ./extra/hades/src/setup_models.cpp
    Copyright (C) 2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <tuple>
#include <map>
#include <string>
#include <H5Cpp.h>
#include <boost/format.hpp>
#include "libLSS/tools/hdf5_error.hpp"
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/tools/console.hpp"
#include <functional>
#include "libLSS/tools/errors.hpp"

#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/physics/forwards/borg_lpt.hpp"
#include "libLSS/physics/forwards/borg_2lpt.hpp"
#include "libLSS/physics/forwards/borg_multi_pm.hpp"
#include "libLSS/physics/hades_pt.hpp"
#include "libLSS/tools/static_init.hpp"

#include "common/preparation.hpp"

#include "model_generator.hpp"

using namespace LibLSS;
using boost::format;

template <typename Model>
void borgForwardSaveTiming(CosmoTool::H5_CommonFileGroup &fg, Model &model) {
  auto &lc = model.lightConeTiming();

  CosmoTool::hdf5_write_array(fg, "timing", lc);
}

template <typename Model>
std::shared_ptr<BORGForwardModel> setup_LPT_model(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params,
    ParticleSaver_t &save_particles, TimingSaver_t &save_timing, int &nstep) {
  namespace ph = std::placeholders;
  int ss_factor = params.get<int>("supersampling");
  int f_factor = params.get<int>("forcesampling");
  double ai = params.get<double>("a_initial");
  double af = params.get<double>("a_final");
  double p_factor = params.get<double>("part_factor", 1.2);
  bool rsd = params.get<bool>("do_rsd", false);
  bool lightcone = params.get<bool>("lightcone", false);
  double lightcone_boost = params.get<double>(
      "lightcone_boost",
      1.0); // This is an artificial factor just to make cool plots.

  auto model = std::make_shared<Model>(
      comm, box, box, rsd, ss_factor, p_factor, ai, af, lightcone,
      lightcone_boost);

  save_particles = std::bind(
      borgSaveParticles<Model>, ph::_1, std::ref(*model), ph::_2, ph::_3,
      ph::_4);
  save_timing =
      std::bind(borgForwardSaveTiming<Model>, ph::_1, std::ref(*model));

  nstep = 1;
  return model;
}

template <typename Model>
std::shared_ptr<BORGForwardModel> setup_2LPT_model(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params,
    ParticleSaver_t &save_particles, TimingSaver_t &save_timing, int &nstep) {
  namespace ph = std::placeholders;
  int ss_factor = params.get<int>("supersampling");
  int f_factor = params.get<int>("forcesampling");
  double ai = params.get<double>("a_initial");
  double af = params.get<double>("a_final");
  double p_factor = params.get<double>("part_factor", 1.2);
  bool rsd = params.get<bool>("do_rsd", false);
  bool lightcone = params.get<bool>("lightcone", false);
  double lightcone_boost = params.get<double>(
      "lightcone_boost",
      1.0); // This is an artificial factor just to make cool plots.

  auto model = std::make_shared<Model>(
      comm, box, rsd, ss_factor, p_factor, ai, af, lightcone);

  save_particles = std::bind(
      borgSaveParticles<Model>, ph::_1, std::ref(*model), ph::_2, ph::_3,
      ph::_4);
  //save_timing =
  //      std::bind(borgForwardSaveTiming<Model>, ph::_1, std::ref(*model));

  nstep = 1;
  return model;
}

template <typename Model>
std::shared_ptr<BORGForwardModel> setup_PM_model(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params,
    ParticleSaver_t &save_particles, TimingSaver_t &save_timing, int &nstep) {
  namespace ph = std::placeholders;
  int ss_factor = params.get<int>("supersampling");
  int f_factor = params.get<int>("forcesampling");
  double ai = params.get<double>("a_initial");
  double af = params.get<double>("a_final");
  double p_factor = params.get<double>("part_factor", 1.2);
  bool rsd = params.get<bool>("do_rsd", false);
  bool lightcone = params.get<bool>("lightcone", false);
  int pm_nsteps = params.get<int>("pm_nsteps", 30);
  double z_start = params.get<double>("pm_start_z", 69.);
  bool tcola = params.get<bool>("tCOLA", false);

  Model *model = new Model(
      comm, box, ss_factor, f_factor, pm_nsteps, p_factor, rsd, ai, af, z_start,
      tcola);

  save_particles = std::bind(
      borgSaveParticles<Model>, ph::_1, std::ref(*model), ph::_2, ph::_3,
      ph::_4);
  nstep = pm_nsteps;
  model->setAdjointRequired(false);
  return model;
}

std::shared_ptr<BORGForwardModel> setup_Linear_model(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params,
    ParticleSaver_t &save_particles, TimingSaver_t &save_timing, int &nstep) {
  double ai = params.get<double>("a_initial");
  nstep = 1;
  return std::make_shared<HadesLinear>(comm, box, box, ai);
}

ModelSetup_t LibLSS::setup_forward_model(std::string const &model_name) {
  std::map<std::string, std::tuple<std::string, ModelSetup_t>> models = {
      {"HADES_LINEAR", {"Linear scaling model", setup_Linear_model}},
      {"LPT",
       {"LPT model with Quad projection",
        setup_LPT_model<BorgLptModel<ModifiedNGP<double, NGPGrid::Quad>>>}},
      {"LPT_CIC",
       {"LPT model with CIC projection",
        setup_LPT_model<BorgLptModel<ClassicCloudInCell<double>>>}},
      {"LPT_DBL",
       {"LPT model with Double projection",
        setup_LPT_model<BorgLptModel<ModifiedNGP<double, NGPGrid::Double>>>}},
      {"2LPT",
       {"2LPT model with Quad projection",
        setup_2LPT_model<Borg2LPTModel<ModifiedNGP<double, NGPGrid::Quad>>>}},
      {"2LPT_CIC",
       {"2LPT model with CIC projection",
        setup_2LPT_model<Borg2LPTModel<ClassicCloudInCell<double>>>}},
      {"2LPT_DBL",
       {"2LPT model with Double projection",
        setup_2LPT_model<Borg2LPTModel<ModifiedNGP<double, NGPGrid::Double>>>}},
      {"PM_CIC",
       {"Particle mesh model with CIC projection",
        setup_PM_model<MetaBorgPMModel<ClassicCloudInCell<double>>>}}};

  if (models.find(model_name) == models.end()) {
    error_helper<ErrorParams>("Unknown BORG model '" + model_name + "'");
  }

  Console::instance().print<LOG_INFO_SINGLE>(
      format("Selecting model %s: %s") % model_name %
      std::get<0>(models[model_name]));

  return std::get<1>(models[model_name]);
}

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2018
