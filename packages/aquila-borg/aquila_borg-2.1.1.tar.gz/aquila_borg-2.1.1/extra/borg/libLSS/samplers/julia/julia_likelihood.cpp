/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/julia/julia_likelihood.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <string>
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/tools/hermiticity_fixup.hpp"
#include "libLSS/samplers/julia/julia_likelihood.hpp"
#include "libLSS/julia/julia.hpp"
#include "libLSS/julia/julia_mcmc.hpp"
#include "libLSS/julia/julia_array.hpp"
#include "libLSS/julia/julia_ghosts.hpp"

using namespace LibLSS;
using boost::c_storage_order;
using boost::extents;
using boost::format;
typedef boost::multi_array_types::extent_range range;
using namespace LibLSS::JuliaLikelihood;
namespace LI = LibLSS::Likelihood;

JuliaDensityLikelihood::JuliaDensityLikelihood(
    MPI_Communication *comm_, LikelihoodInfo &info,
    const std::string &code_name, const std::string &_module_name)
    : super_t(comm_, LI::gridResolution(info), LI::gridSide(info)), comm(comm_),
      module_name(_module_name), volume(array::product(L)) {
  Console::instance().print<LOG_INFO>(
      "Loading code " + code_name + " in julia VM");
  Julia::load_file(code_name);
}

void JuliaDensityLikelihood::common_initialize(MarkovState &state) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  state.newElement(
      "BORG_vobs", vobs = new ArrayType1d(boost::extents[3]), true);

  model = state.get<BorgModelElement>("BORG_model")->obj;
  Ncat = state.getScalar<long>("NCAT");

  state.newElement(
      "BORG_final_density",
      borg_final_density = new ArrayType(model->out_mgr->extents_real_strict()),
      true);
  borg_final_density->setRealDims(this->N);
  final_density_field = model->out_mgr->allocate_ptr_array();

  std::string init_func = likelihood_module_initialize(module_name);
  ctx.format("JULIA: Invoking %s", init_func);
  Julia::invoke(init_func, Julia::pack(state));

  Julia::Object plane_array =
      Julia::invoke(query_planes(module_name), Julia::pack(state));
  // FIXME: May lead to corruption if type is unchecked.
  //        We need to strengthen the handling of types at boundary.
  auto planes = plane_array.unbox_array<uint64_t, 1>();

  std::vector<size_t> owned_planes(mgr->localN0);

  for (size_t i = 0; i < mgr->localN0; i++)
    owned_planes[i] = mgr->startN0 + i;

  ghosts.setup(
      comm, planes, owned_planes,
      std::array<size_t, 2>{size_t(mgr->N1), size_t(mgr->N2real)}, mgr->N0);

  notify_init.submit_ready();
}

void JuliaDensityLikelihood::initializeLikelihood(MarkovState &state) {
  common_initialize(state);

  (*vobs->array)[0] = 0;
  (*vobs->array)[1] = 0;
  (*vobs->array)[2] = 0;
}

JuliaDensityLikelihood::~JuliaDensityLikelihood() {}

/*
 * We commit the auxiliary fields inside the MarkovState element.
 */
void JuliaDensityLikelihood::commitAuxiliaryFields(MarkovState &state) {
  array::scaleAndCopyArray3d(
      *borg_final_density->array, final_density_field->get_array(), 1, true);
}

void JuliaDensityLikelihood::updateCosmology(
    CosmologicalParameters const &params) {
  cosmology = std::unique_ptr<Cosmology>(new Cosmology(params));
  model->setCosmoParams(params);
}

void JuliaDensityLikelihood::setupDefaultParameters(
    MarkovState &state, int catalog) {
  Julia::invoke(
      likelihood_set_default_parameters(module_name), Julia::pack(*p_state),
      catalog);
}

/*
 * Routines to update the internal state from the MarkovState.
 */
void JuliaDensityLikelihood::updateMetaParameters(MarkovState &state) {
  using boost::format;

  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  auto cosmo_params = state.getScalar<CosmologicalParameters>("cosmology");

  updateCosmology(cosmo_params);

  auto e_Ncat = boost::extents[Ncat];
  nmean.resize(Ncat);
  bias_params.resize(Ncat);
  biasRef.resize(Ncat);
  data.resize(Ncat);
  sel_field.resize(Ncat);

  for (int c = 0; c < Ncat; c++) {
    biasRef[c] = state.getScalar<bool>(format("galaxy_bias_ref_%d") % c);
    nmean[c] = state.getScalar<double>(format("galaxy_nmean_%d") % c);

    data[c] = state.get<ArrayType>(format("galaxy_data_%d") % c)->array;
    sel_field[c] =
        state.get<ArrayType>(format("galaxy_synthetic_sel_window_%d") % c)
            ->array;

    bias_params[c] =
        state.get<ArrayType1d>(format("galaxy_bias_%d") % c)->array;
  }

  ai = state.get<SDouble>("borg_a_initial")->value;

  p_state = &state;
}

double JuliaDensityLikelihood::logLikelihood(
    ArrayRef const &s_array, bool final_call) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);

  return logLikelihood_internal(
      ModelInput<3>(model->lo_mgr, model->get_box_model(), s_array),
      final_call);
}

double JuliaDensityLikelihood::logLikelihood(
    CArrayRef const &s_array, bool final_call) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);

  return logLikelihood_internal(
      ModelInput<3>(model->lo_mgr, model->get_box_model(), s_array),
      final_call);
}

double JuliaDensityLikelihood::logLikelihood_internal(
    ModelInput<3> input, bool final_call) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  using CosmoTool::square;
  using LibLSS::Julia::helpers::_r;

  typedef ArrayType::ArrayType::element ElementType;
  double Epoisson = 0;

  // Simulate forward model
  //setup position and velocity arrays

  auto &out_density = final_density_field->get_array();

  // Update forward model for maybe new cosmo params
  model->setCosmoParams(cosmology->getParameters());
  // Inform about the velocity of the observer
  model->setObserver(*vobs->array);
  // Compute forward model
  model->forwardModel_v2(std::move(input));
  model->getDensityFinal(ModelOutput<3>(
      model->out_mgr, model->get_box_model_output(), out_density));

  Julia::Object jl_density;
  jl_density.box_array(out_density);

  ghosts.synchronize(out_density);

  Julia::Object ret = Julia::invoke(
      likelihood_evaluate(module_name), Julia::pack(*p_state),
      Julia::newGhostManager(&ghosts, mgr->N2),
      Julia::view_array<3>(
          jl_density, {_r(1, mgr->localN0), _r(1, mgr->N1), _r(1, mgr->N2)}));
  double L = ret.unbox<double>();

  comm->all_reduce_t(MPI_IN_PLACE, &L, 1, MPI_SUM);
  return L;
}

void JuliaDensityLikelihood::gradientLikelihood(
    ArrayRef const &s, ArrayRef &grad_array, bool accumulate, double scaling) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);

  if (accumulate) {
    auto tmp_out = model->lo_mgr->allocate_array();

    gradientLikelihood_internal(
        ModelInput<3>(model->lo_mgr, model->get_box_model(), s),
        ModelOutputAdjoint<3>(
            model->lo_mgr, model->get_box_model(), tmp_out.get_array()));

    fwrap(grad_array) = fwrap(grad_array) + scaling * fwrap(tmp_out);
  } else {
    gradientLikelihood_internal(
        ModelInput<3>(model->lo_mgr, model->get_box_model(), s),
        ModelOutputAdjoint<3>(
            model->lo_mgr, model->get_box_model(), grad_array));
    fwrap(grad_array) = fwrap(grad_array) * scaling;
  }
}

void JuliaDensityLikelihood::gradientLikelihood(
    CArrayRef const &s, CArrayRef &grad_array, bool accumulate,
    double scaling) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);

  if (accumulate) {
    auto tmp_out = model->lo_mgr->allocate_complex_array();

    gradientLikelihood_internal(
        ModelInput<3>(model->lo_mgr, model->get_box_model(), s),
        ModelOutputAdjoint<3>(
            model->lo_mgr, model->get_box_model(), tmp_out.get_array()));

    fwrap(grad_array) = fwrap(grad_array) + scaling * fwrap(tmp_out);
  } else {
    gradientLikelihood_internal(
        ModelInput<3>(model->lo_mgr, model->get_box_model(), s),
        ModelOutputAdjoint<3>(
            model->lo_mgr, model->get_box_model(), grad_array));
    fwrap(grad_array) = fwrap(grad_array) * scaling;
  }
}

void JuliaDensityLikelihood::gradientLikelihood_internal(
    ModelInput<3> input, ModelOutputAdjoint<3> out_gradient) {
  using CosmoTool::square;
  typedef CArrayRef::element etype;
  using LibLSS::Julia::helpers::_r;
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);

  // Simulate forward model
  //setup position and velocity arrays

  model->setCosmoParams(cosmology->getParameters());
  model->setObserver(*vobs->array);
  model->forwardModel_v2(std::move(input));
  model->getDensityFinal(ModelOutput<3>(
      model->out_mgr, model->get_box_model_output(),
      final_density_field->get_array()));

  auto grad_p = model->out_mgr->allocate_array();
  auto& grad = grad_p.get_array();

  fwrap(grad) = 0;

  Julia::Object jl_density, jl_adjoint_gradient;
  jl_density.box_array(final_density_field->get_array());
  jl_adjoint_gradient.box_array(grad);

  ghosts.synchronize(final_density_field->get_array());
  ghosts.clear_ghosts();

  (void)Julia::invoke(
      likelihood_adjoint_gradient(module_name), Julia::pack(*p_state),
      Julia::view_array<3>(
          jl_density, {_r(1, mgr->localN0), _r(1, mgr->N1), _r(1, mgr->N2)}),
      Julia::newGhostManager(&ghosts, mgr->N2),
      Julia::view_array<3>(
          jl_adjoint_gradient,
          {_r(1, mgr->localN0), _r(1, mgr->N1), _r(1, mgr->N2)}));

  ghosts.synchronize_ag(grad);

  // Now obtain the complex gradient using adjoint fft
  model->adjointModel_v2(ModelInputAdjoint<3>(
      model->out_mgr, model->get_box_model_output(), grad));
  model->getAdjointModelOutput(std::move(out_gradient));
  model->clearAdjointGradient();
}

void JuliaDensityLikelihood::generateMockData(
    CArrayRef const &s_hat, MarkovState &state) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  using LibLSS::Julia::helpers::_r;

  model->setCosmoParams(cosmology->getParameters());
  model->setObserver(*vobs->array);
  model->forwardModel_v2(ModelInput<3>(
      model->lo_mgr, model->get_box_model(), s_hat));
  model->getDensityFinal(ModelOutput<3>(
      model->out_mgr, model->get_box_model_output(),
      final_density_field->get_array()));

  Julia::Object jl_density;
  jl_density.box_array(final_density_field->get_array());

  fwrap(*borg_final_density->array) = final_density_field->get_array();

  ghosts.synchronize(final_density_field->get_array());

  Julia::invoke(
      mock_data_generate(module_name), Julia::pack(state),
      Julia::newGhostManager(&ghosts, mgr->N2),
      Julia::view_array<3>(
          jl_density, {_r(1, mgr->localN0), _r(1, mgr->N1), _r(1, mgr->N2)}));
}

void JuliaDensityLikelihood::generateInitialConditions(MarkovState &state) {
  Julia::invoke(ic_generate(module_name), Julia::pack(state));

  auto tmp_real_p = mgr->allocate_array();
  double dV = array::product(L) / array::product(N);
  {
    auto tmp_complex_field_p = mgr->allocate_complex_array();
    auto &tmp_complex_field = tmp_complex_field_p.get_array();
    fwrap(tmp_real_p.get_array()) =
        fwrap(*state.get<ArrayType>("s_field")->array) * dV;
    mgr->execute_r2c(
        analysis_plan, tmp_real_p.get_array().data(), tmp_complex_field.data());
    fwrap(*state.get<CArrayType>("s_hat_field")->array) =
        fwrap(tmp_complex_field);
  }

  // TODO: THIS IS UGLY! Force the forward model to run
  auto const& s_hat = *state.get<CArrayType>("s_hat_field")->array;
  logLikelihood_internal(ModelInput<3>(model->lo_mgr, model->get_box_model(), s_hat));
  commitAuxiliaryFields(state);
}
