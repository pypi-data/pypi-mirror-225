/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/generic/generic_vobs_impl.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/samplers/rgen/slice_sweep.hpp"
#include "libLSS/tools/string_tools.hpp"

template <typename Likelihood>
LibLSS::GenericVobsSampler<Likelihood>::~GenericVobsSampler() {}

// This function is intended to evaluate the value of the posterior distribution
// when a single catalog is considered for data.  It is intended for parameters
// that relate the final dark matter density to the observed galaxy distribution.
template <typename Likelihood>
double LibLSS::GenericVobsSampler<Likelihood>::bound_posterior(
    double x, int j, MarkovState &state) {
  using boost::format;
  double loc_L, L;
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);

  loc_L = 0;
  L = 0;

  auto &matter_field = *vobs_matter_field;
  double current_vobs[3];

  std::copy(vobs->begin(), vobs->end(), current_vobs);
  current_vobs[j] = x;

  ctx.print("V = " + LibLSS::to_string(x));

  // Re-Execute the last bit of the forward model to incorporate
  // the effect of current_vobs
  model->forwardModelRsdField(matter_field, current_vobs);

  bias_t b;

  // Loop over all catalog to build the likelihood
  for (int c = 0; c < Ncat; c++) {
    double &nmean =
        state.template getScalar<double>(format("galaxy_nmean_%d") % c);
    BiasParamArray &bias_params =
        *state.template get<ArrayType1d>(format("galaxy_bias_%d") % c)->array;
    SelectionArray &sel_field =
        *state
             .template get<ArrayType>(
                 format("galaxy_synthetic_sel_window_%d") % c)
             ->array;
    DataArray &gdata =
        *state.template get<ArrayType>(format("galaxy_data_%d") % c)->array;

    // Prepare the bias function
    b.prepare(*model, matter_field, nmean, bias_params, true);

    // Derive the density
    auto biased_density = b.compute_density(matter_field);
    // Apply selection
    auto select_density =
        b.selection_adaptor.apply(sel_field, biased_density);
    // We only want voxels with a positive selection, all the others are masked out
    auto mask = b_va_fused<bool>(_p1 > 0, sel_field);
    // Compute log_probability
    loc_L += this->likelihood->log_probability(gdata, select_density, mask);

    // Cleanup of bias for the next catalog
    b.cleanup();
  }

  // Reduction to the root
  comm->reduce_t(&loc_L, &L, 1, MPI_SUM, 0);

  return L;
}

template <typename Likelihood>
void LibLSS::GenericVobsSampler<Likelihood>::initialize(MarkovState &state) {
  Ncat = state.getScalar<long>("NCAT");
  model = state.get<BorgModelElement>("BORG_model")->obj;

  long N0 = state.getScalar<long>("N0");
  long N1 = state.getScalar<long>("N1");
  long N2 = state.getScalar<long>("N2");

  mgr = std::make_shared<DFT_Manager>(N0, N1, N2, comm);

  vobs_matter_field = std::make_unique<DensityArray>(
      mgr->extents_real(), boost::c_storage_order(), mgr->allocator_real);
}

template <typename Likelihood>
void LibLSS::GenericVobsSampler<Likelihood>::restore(MarkovState &state) {
  initialize(state);
}

template <typename Likelihood>
void LibLSS::GenericVobsSampler<Likelihood>::sample(MarkovState &state) {
  using boost::format;
  ConsoleContext<LOG_DEBUG> ctx("sampling of velocity of the observer");
  DensityArray &matter_density =
      *state.get<ArrayType>("BORG_final_density")->array;
  auto &rgen = state.get<RandomGen>("random_generator")->get();

  vobs = state.get<ArrayType1d>("BORG_vobs")->array;

  CosmologicalParameters &cosmo_params =
      state.getScalar<CosmologicalParameters>("cosmology");
  double ai = state.get<SDouble>("borg_a_initial")->value;
  CArrayType::ArrayType &s_array = *state.get<CArrayType>("s_hat_field")->array;

  // This is a slight abuse of API. This forward should be a standalone function of
  // the generic framework.
  GenericDetails::compute_forward(
      mgr, model, cosmo_params, ai, *vobs,
      ModelInput<3>(model->lo_mgr, model->get_box_model(), s_array),
      ModelOutput<3>(
          model->out_mgr, model->get_box_model_output(), *vobs_matter_field),
      true);

  // Use slice_sweep to sample the parameter
  // We enforce to pass down a reference to the catalog data. No need to add construction etc.
  for (int j = 0; j < 3; j++) {
    (*vobs)[j] = slice_sweep(
        comm, rgen,
        std::
            bind( // bind the second parameter of bound posterior to 'j' (vobs component)
                &GenericVobsSampler<Likelihood>::bound_posterior, this,
                std::placeholders::_1, j, std::ref(state)),
        (*vobs)[j],
        20 // use 20 km/s step for the likelihood evaluation
    );
  }
  ctx.print(
      format("Got Vobs=(%g,%g,%g)") % (*vobs)[0] % (*vobs)[1] % (*vobs)[2]);

  // Do a final recomputation of the matter field with the obtained velocity
  // no need to do a full evaluation
  model->forwardModelRsdField(
      *state.get<ArrayType>("BORG_final_density")->array, vobs->data());
  // Update vobs
  model->setObserver(*vobs);
  // Release held particles
  model->releaseParticles();
}
