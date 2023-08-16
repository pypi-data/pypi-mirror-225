/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/generic/generic_meta_impl.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/samplers/rgen/slice_sweep.hpp"
#include "libLSS/physics/bias/base.hpp"

// This function is intended to evaluate the value of the posterior distribution
// when a single catalog is considered for data.  It is intended for parameters
// that relate the final dark matter density to the observed galaxy distribution.
template <typename Likelihood, typename MetaSelector>
double
LibLSS::GenericMetaSampler<Likelihood, MetaSelector, true>::bound_posterior(
    double H, double x, CatalogData &catalog) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  double loc_L, L;
  double nmean = catalog.nmean;
  boost::array<double, bias_t::numParams> bias_params;

  // Copy the parameters in a safe temporary storage (bias_params)
  std::copy(
      catalog.bias_params.begin(), catalog.bias_params.end(),
      bias_params.begin());

  // Select copy x to one of the entry. We can then use the values blindly to evaluate the posterior.
  MetaSelector::select(x, nmean, bias_params);

  // Prepare the bias function
  auto &local_bias = *this->bias;

  // Enforce nmean and bias constraints
  if (nmean <= 0 || !local_bias.check_bias_constraints(bias_params)) {
    ctx.format("Fail bias constraints: %g", x);
    return -std::numeric_limits<double>::infinity();
  }

  // We indicate that the density field has already been used by this
  // bias previously. So no need to update internal buffers.
  local_bias.prepare(
      *model, catalog.matter_density, nmean, bias_params, false,
      MetaSelector());
  // Derive the density
  auto biased_density = local_bias.compute_density(catalog.matter_density);
  // Apply selection
  auto select_density =
      local_bias.selection_adaptor.apply(catalog.sel_field, biased_density);
  // We only want voxels with a positive selection, all the others are masked out
  auto mask = b_va_fused<bool>(_p1 > 0, catalog.sel_field);
  // Compute log_probability
  loc_L = this->likelihood->log_probability(catalog.data, select_density, mask);
  // Cleanup
  local_bias.cleanup();

  // Reduction to the root
  comm->reduce_t(&loc_L, &L, 1, MPI_SUM, 0);

  return H * L + bias::bias_get_log_prior(local_bias, bias_params);
}

template <typename Likelihood, typename MetaSelector>
void LibLSS::GenericMetaSampler<Likelihood, MetaSelector, true>::initialize(
    MarkovState &state) {
  Ncat = state.getScalar<long>("NCAT");
  model = state.get<BorgModelElement>("BORG_model")->obj;
}

template <typename Likelihood, typename MetaSelector>
void LibLSS::GenericMetaSampler<Likelihood, MetaSelector, true>::restore(
    MarkovState &state) {
  initialize(state);
}

template <typename Likelihood, typename MetaSelector>
void LibLSS::GenericMetaSampler<Likelihood, MetaSelector, true>::sample(
    MarkovState &state) {
  using boost::format;
  ConsoleContext<LOG_VERBOSE> ctx(
      std::string("sampling of meta parameter: ") + MetaSelector::name());
  DensityArray &matter_density =
      *state.get<ArrayType>("BORG_final_density")->array;
  auto &rgen = state.get<RandomGen>("random_generator")->get();
  double const ares_heat = state.getScalar<double>("ares_heat");

  if (false) {
    H5::H5File f("matter_density.h5", H5F_ACC_TRUNC);
    CosmoTool::hdf5_write_array(f, "matter", matter_density);
  }

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

    // Double check that the bias parameters are exactly compatible with the model.
    Console::instance().c_assert(
        bias_params.size() == bias_t::numParams,
        "Incompatible bias parameters");
    CatalogData catalog{nmean, bias_params, sel_field, matter_density, gdata};

    // Use slice_sweep to sample the parameter
    // We enforce to pass down a reference to the catalog data. No need to add construction etc.
    double result = slice_sweep_double(
        comm, rgen,
        std::bind(
            &GenericMetaSampler<Likelihood, MetaSelector>::bound_posterior,
            this, ares_heat, std::placeholders::_1, std::ref(catalog)),
        MetaSelector::get_value(nmean, bias_params),
        MetaSelector::step_advisor);

    ctx.print(boost::format("Got %g for catalog %d") % result % c);

    // Copy the new sample in place
    MetaSelector::select(result, nmean, bias_params);
  }
}
