/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/lya/base_lya_likelihood.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <CosmoTool/algo.hpp>
#include <cmath>
#include <Eigen/Core>
#include <boost/format.hpp>
#include <boost/bind.hpp>
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/samplers/lya/base_lya_likelihood.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/samplers/rgen/slice_sweep.hpp"

using namespace LibLSS;
using boost::extents;
using boost::format;

using CosmoTool::square;

using boost::c_storage_order;
typedef boost::multi_array_types::extent_range range;

static const int ROOT_RANK = 0;

namespace LI = LibLSS::Likelihood;

HadesBaseDensityLyaLikelihood::HadesBaseDensityLyaLikelihood(
    LikelihoodInfo &info, size_t numBiasParams_)
    : super_t(LI::getMPI(info), LI::gridResolution(info), LI::gridSide(info)),
      corners(LI::gridCorners(info)), numBiasParams(numBiasParams_),
      volume(array::product(L)) {}

HadesBaseDensityLyaLikelihood::~HadesBaseDensityLyaLikelihood() {}

void HadesBaseDensityLyaLikelihood::updateCosmology(
    CosmologicalParameters const &cosmo_params) {
  cosmology = std::unique_ptr<Cosmology>(new Cosmology(cosmo_params));
  model->setCosmoParams(cosmo_params);
}

void HadesBaseDensityLyaLikelihood::updateMetaParameters(MarkovState &state) {
  LIBLSS_AUTO_CONTEXT(LOG_VERBOSE, ctx);
  auto cosmo_params = state.getScalar<CosmologicalParameters>("cosmology");

  Ncat = state.getScalar<long>("NCAT");

  //initialize model uncertainty
  model = state.get<BorgModelElement>("BORG_model")->obj;

  ai = state.getScalar<double>("borg_a_initial");

  // Update forward model for maybe new cosmo params
  updateCosmology(cosmo_params);

  auto e_Ncat = boost::extents[Ncat];
  //data.resize(Ncat);
  sel_field.resize(Ncat);
  
  for (int c = 0; c < Ncat; c++) {
    setupDefaultParameters(state, c);
  


    
  }
}

double HadesBaseDensityLyaLikelihood::logLikelihood(
    ArrayRef const &s_array, bool final_call) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  using CosmoTool::square;
  typedef ArrayType::ArrayType::element ElementType;
  double L = 0;
  Cosmology &cosmo = *cosmology.get();

  ctx.print("Run forward");
  // Simulate forward model
  auto box = model->get_box_model();
  auto out_density_p = mgr->allocate_array();
  auto &out_density = out_density_p.get_array();
  model->setAdjointRequired(false);
  model->forwardModel_v2(ModelInput<3>(mgr, box, s_array));
  model->getDensityFinal(ModelOutput<3>(mgr, box, out_density));

  L = logLikelihoodSpecific(out_density);
  comm->all_reduce_t(MPI_IN_PLACE, &L, 1, MPI_SUM);

  return L;
}

double HadesBaseDensityLyaLikelihood::logLikelihood(
    CArrayRef const &s_array, bool final_call) {
  using CosmoTool::square;
  typedef ArrayType::ArrayType::element ElementType;
  double L = 0;
  auto &out_density = final_density_field->get_array();

  auto box = model->get_box_model();
  model->setAdjointRequired(false);
  model->forwardModel_v2(ModelInput<3>(mgr, box, s_array));
  model->getDensityFinal(ModelOutput<3>(mgr, box, out_density));

  L = logLikelihoodSpecific(out_density);
  comm->all_reduce_t(MPI_IN_PLACE, &L, 1, MPI_SUM);

  return L;
}

void HadesBaseDensityLyaLikelihood::gradientLikelihood_internal(
    ModelInput<3> input_field, ModelOutputAdjoint<3> grad_array) {
  using CosmoTool::square;
  typedef ArrayType::ArrayType::element ElementType;
  double Epoisson = 0;

  auto box = model->get_box_model();
  auto &out_density = final_density_field->get_array();

  model->setAdjointRequired(true);
  model->forwardModel_v2(std::move(input_field));
  model->getDensityFinal(ModelOutput<3>(mgr, box, out_density));

  auto tmp_grad_p = model->out_mgr->allocate_array();
  auto &tmp_grad = tmp_grad_p.get_array();
  gradientLikelihoodSpecific(out_density, tmp_grad);

  model->adjointModel_v2(ModelInputAdjoint<3>(mgr, box, tmp_grad));
  model->getAdjointModelOutput(std::move(grad_array));
  model->clearAdjointGradient();
}

void HadesBaseDensityLyaLikelihood::gradientLikelihood(
    ArrayRef const &s_array, ArrayRef &grad_array, bool accumulate,
    double scaling) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);

  auto box = model->get_box_model();

  if (!accumulate) {
    gradientLikelihood_internal(
        ModelInput<3>(mgr, box, s_array),
        ModelOutputAdjoint<3>(mgr, box, grad_array));
    fwrap(grad_array) = fwrap(grad_array) * scaling;
  } else {
    auto real_gradient_p = mgr->allocate_array();
    auto &real_gradient = real_gradient_p.get_array();

    gradientLikelihood_internal(
        ModelInput<3>(mgr, box, s_array),
        ModelOutputAdjoint<3>(mgr, box, real_gradient));
    fwrap(grad_array) = fwrap(grad_array) + scaling * fwrap(real_gradient);
  }
}

void HadesBaseDensityLyaLikelihood::gradientLikelihood(
    CArrayRef const &parameters, CArrayRef &grad_array, bool accumulate,
    double scaling) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  //  auto real_gradient_p = mgr->allocate_array();
  //  auto &real_gradient = real_gradient_p.get_array();
  auto box = model->get_box_model();

  {
    if (!accumulate) {
      gradientLikelihood_internal(
          ModelInput<3>(mgr, box, parameters),
          ModelOutputAdjoint<3>(mgr, box, grad_array));
      fwrap(grad_array) = fwrap(grad_array) * scaling;
    } else {
      auto tmp_complex_field = mgr->allocate_complex_array();
      gradientLikelihood_internal(
          ModelInput<3>(mgr, box, parameters),
          ModelOutputAdjoint<3>(mgr, box, tmp_complex_field.get_array()));

      fwrap(grad_array) =
          fwrap(grad_array) + fwrap(tmp_complex_field.get_array()) * scaling;
    }
  }
}

void HadesBaseDensityLyaLikelihood::generateMockData(
    CArrayRef const &parameters, MarkovState &state) {
  LIBLSS_AUTO_CONTEXT(LOG_INFO, ctx);

  auto &out_density = final_density_field->get_array();
  auto box = model->get_box_model();

  model->setAdjointRequired(false);
  model->forwardModel_v2(ModelInput<3>(mgr, box, parameters));
  model->getDensityFinal(ModelOutput<3>(model->out_mgr, model->get_box_model_output(), out_density));

  generateMockSpecific(out_density, state);
  commitAuxiliaryFields(state);
}

void HadesBaseDensityLyaLikelihood::initializeLikelihood(MarkovState &state) {
  Ncat = state.getScalar<long>("NCAT");
  model = state.get<BorgModelElement>("BORG_model")->obj;
  borg_final_density = new ArrayType(model->out_mgr->extents_real_strict());
  final_density_field = model->out_mgr->allocate_ptr_array();

  std::array<ssize_t, 3> out_N, local_N;
  model->get_box_model_output().fill(out_N);
  borg_final_density->setRealDims(out_N);

  std::copy(
      borg_final_density->array->shape(),
      borg_final_density->array->shape() + 3, local_N.begin());

  for (size_t c = 0; c < Ncat; c++) {
    
      setupDefaultParameters(state, c);
    

    
  }

  state.newElement("BORG_final_density", borg_final_density, true);
}

void HadesBaseDensityLyaLikelihood::commitAuxiliaryFields(MarkovState &state) {
  array::scaleAndCopyArray3d(
      *borg_final_density->array, final_density_field->get_array(), 1, true);
}

void HadesBaseDensityLyaLikelihood::updateNmean(int catalog, double nmean_) {
  //nmean[catalog] = nmean_;
}

void HadesBaseDensityLyaLikelihood::updateBiasParameters(
    int catalog, BiasArray const &params) {
  fwrap(*bias[catalog]) = fwrap(params);
}

void HadesMetaLyaSampler::initialize(MarkovState &state) {
  Ncat = state.getScalar<long>("NCAT");
}

void HadesMetaLyaSampler::restore(MarkovState &state) {
  Ncat = state.getScalar<long>("NCAT");
}

void HadesMetaLyaSampler::sample(MarkovState &state) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  RandomGen *rng = state.get<RandomGen>("random_generator");

  if (state.getScalar<bool>("bias_sampler_blocked"))
    return;

  auto const &density = *state.get<ArrayType>("BORG_final_density")->array;
  double const ares_heat = state.getScalar<double>("ares_heat");

  likelihood->updateMetaParameters(state);

  //for (int c = 0; c < Ncat; c++) {
   // auto const &sel_array =
   //     *state.get<SelArrayType>(format("galaxy_sel_window_%d") % c)->array;
    
    
    //ctx.print(format("considering catalog %d") % c);

    /*nmean = slice_sweep_double(
        comm, rng->get(),
        [&](double x) -> double {
          likelihood->updateNmean(c, x);
          return -ares_heat * likelihood->logLikelihoodSpecific(density);
        },
        nmean, 0.1);

    likelihood->updateNmean(c, nmean);

    for (int ib = 0; ib < bias.size(); ib++) {
      bias[ib] = slice_sweep(
          comm, rng->get(),
          [&](double x) -> double {
            boost::multi_array<double, 1> loc_bias = bias;
            loc_bias[ib] = x;
            likelihood->updateBiasParameters(c, loc_bias);
            return -ares_heat * likelihood->logLikelihoodSpecific(density);
          },
          bias[ib], 0.1);
      likelihood->updateBiasParameters(c, bias);
    }
  }*/
  
}
