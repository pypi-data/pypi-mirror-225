/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/generic/generic_foreground_impl.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/samplers/rgen/slice_sweep.hpp"
#include <boost/iterator/zip_iterator.hpp>
#include <boost/iterator/counting_iterator.hpp>
#include "libLSS/tools/fusewrapper.hpp"

static inline LibLSS::ArrayType::ArrayType &
get_fgmap(LibLSS::MarkovState &state, int id) {
  return *state.get<LibLSS::ArrayType>(boost::format("foreground_3d_%d") % id)
              ->array;
}

template <typename Likelihood>
LibLSS::GenericForegroundSampler<Likelihood>::~GenericForegroundSampler() {}

template <typename Likelihood>
void LibLSS::GenericForegroundSampler<Likelihood>::addMap(int fgmap) {
  fgmap_list.push_back(fgmap);
}

// This function is intended to evaluate the value of the posterior distribution
// when a single catalog is considered for data.  It is intended for parameters
// that relate the final dark matter density to the observed galaxy distribution.

template <typename Likelihood>
double LibLSS::GenericForegroundSampler<Likelihood>::bound_posterior(
    double fgval, double fgvalmin, double fgvalmax, DensityArray &gdata,
    DensityArray &fg_field, ArrayReal &pre_selection_field,
    DensityArray &original_selection, TupleResidual &r_tuple) {
  using boost::format;
  // Build the effective new selected density field with the provided
  // value.
  ConsoleContext<LOG_VERBOSE> ctx("likelihood evaluation");

  ctx.print(format("fgval is %g") % fgval);

  if (fgval <= fgvalmin || fgval >= fgvalmax)
    return -std::numeric_limits<double>::infinity();

  auto final_density =
      (1 - fgval * fwrap(fg_field)) * fwrap(pre_selection_field);
  double loc_L = 0, L = 0;

  // Build the mask of log probability on top of the original selection.
  auto mask = b_va_fused<bool>(_p1 > 0, original_selection);

  // Compute masked log-probability.
  loc_L = this->likelihood->log_probability(
      gdata, std::tuple_cat(std::make_tuple(*final_density), r_tuple), mask);
  ctx.print(format("loc_L is %g") % loc_L);

  Console::instance().c_assert(!std::isnan(loc_L), "Likelihood is NaN.");

  // Reduction to the root
  comm->reduce_t(&loc_L, &L, 1, MPI_SUM, 0);
  if (comm->rank() == 0)
    ctx.print(format("global L is %g") % L);
  return L;
}

template <typename Likelihood>
void LibLSS::GenericForegroundSampler<Likelihood>::foregroundLoaded(
    MarkovState &state, int fgid) {
  using boost::format;
  ConsoleContext<LOG_VERBOSE> ctx(
      str(format("initialization of foreground id %d") % fgid));

  DensityArray &fg = get_fgmap(state, fgmap_list[fgid]);
  ctx.print(
      format("Got map for %d (%dx%dx%d)") % fgmap_list[fgid] % fg.shape()[0] %
      fg.shape()[1] % fg.shape()[2]);
  double abs_max_val = 0, max_val = 0, min_val = 0;
  double loc_abs_max_val = 0, loc_max_val = 0, loc_min_val = 0;
  size_t startN0 = mgr->startN0, endN0 = mgr->startN0 + mgr->localN0;

#pragma omp parallel for collapse(3) reduction(max                             \
                                               : loc_max_val, loc_abs_max_val) \
    reduction(min                                                              \
              : loc_min_val)
  for (size_t ix = startN0; ix < endN0; ix++)
    for (size_t iy = 0; iy < N1; iy++)
      for (size_t iz = 0; iz < N2; iz++) {
        double val = fg[ix][iy][iz];
        loc_abs_max_val = std::max(std::abs(val), loc_abs_max_val);
        loc_max_val = std::max(val, loc_max_val);
        loc_min_val = std::min(val, loc_min_val);
      }
  comm->all_reduce_t(&loc_max_val, &max_val, 1, MPI_MAX);
  comm->all_reduce_t(&loc_abs_max_val, &abs_max_val, 1, MPI_MAX);
  comm->all_reduce_t(&loc_min_val, &min_val, 1, MPI_MIN);

  // We put generic constraints that 0 < 1 - alpha F < 1
  // The upper boundary is not strictly necessary but
  // *sounds* like fair. If we have to correct the selection
  // by more than 100% we are already doomed in practice.

  // 1- alpha F > 0 => alpha F < 1
  // alpha Fmax < 1 =>
  //    if Fmax>0, alpha < 1/Fmax
  //    if Fmax<0, alpha > 1/Fmax
  //
  const double inf = std::numeric_limits<double>::infinity();
  const double inv_max = 1 / max_val;
  const double inv_min = 1 / min_val;

  double alpha_max = inf;
  double alpha_min = -inf;

  auto update_max = [&alpha_max](double x) {
    alpha_max = std::min(alpha_max, x);
  };
  auto update_min = [&alpha_min](double x) {
    alpha_min = std::max(alpha_min, x);
  };

  // 2 > 1- alpha F > 0 => -1 < alpha F < 1

  // -1 < alpha Fmin < alpha F < 1 =>
  //    if Fmin>0, -1/Fmin < alpha < 1/Fmin
  //    if Fmin<0, -1/Fmin > alpha > 1/Fmin
  update_max(std::abs(inv_min));
  update_min(-std::abs(inv_min));

  // -1 < alpha F < alpha Fmax < 1 ->
  //   Fmax > 0 => -1/Fmax < alpha < 1/Fmax
  //   Fmax < 0 => -1/Fmax > alpha > 1/Fmax
  update_max(std::abs(inv_max));
  update_min(-std::abs(inv_max));

  fgvalmax[fgid] = alpha_max;
  fgvalmin[fgid] = alpha_min;
  step_norm[fgid] = 1.0 / abs_max_val;
  ctx.print(
      format("step_norm,alpha_maxval for fgmap (map=%d,id=%d) is %g, %g, %g") %
      fgmap_list[fgid] % fgid % step_norm[fgid] % (1 / max_val) %
      (1 / min_val));
  ctx.print(format(" range = [%g, %g]") % fgvalmin[fgid] % fgvalmax[fgid]);
  Console::instance().c_assert(
      fgvalmax[fgid] - fgvalmin[fgid] > 0,
      "Invalid allowed foreground range of values");
}

template <typename Likelihood>
void LibLSS::GenericForegroundSampler<Likelihood>::local_initialize(
    MarkovState &state) {
  using boost::format;
  ConsoleContext<LOG_VERBOSE> ctx(
      str(format("initialization of GenericForegroundSampler(catalog=%d)") %
          catalog));
  model = state.get<BorgModelElement>("BORG_model")->obj;

  N0 = state.getScalar<long>("N0");
  N1 = state.getScalar<long>("N1");
  N2 = state.getScalar<long>("N2");

  mgr = std::make_shared<DFT_Manager>(N0, N1, N2, comm);

  ctx.print(
      format("Preparing foreground steps (fg size=%d)") % fgmap_list.size());
  step_norm.resize(fgmap_list.size());
  fgvalmax.resize(fgmap_list.size());
  fgvalmin.resize(fgmap_list.size());

  for (int fgid = 0; fgid < fgmap_list.size(); fgid++) {
    state.get<ArrayType>(format("foreground_3d_%d") % fgmap_list[fgid])
        ->subscribeLoaded(std::bind(
            &GenericForegroundSampler<Likelihood>::foregroundLoaded, this,
            std::ref(state), fgid));
  }
}

template <typename Likelihood>
void LibLSS::GenericForegroundSampler<Likelihood>::initialize(
    MarkovState &state) {
  local_initialize(state);
}

template <typename Likelihood>
void LibLSS::GenericForegroundSampler<Likelihood>::restore(MarkovState &state) {
  local_initialize(state);
}

template <typename Likelihood>
void LibLSS::GenericForegroundSampler<Likelihood>::sample(MarkovState &state) {
  using boost::format;
  ConsoleContext<LOG_VERBOSE> ctx(
      str(format("sampling of foregrounds for catalog %d") % catalog));

  if (state.getScalar<bool>("total_foreground_blocked"))
    return;

  // This lambda function is just an alias to grab the array
  // stored in foreground_3d_%d

  // Grab the final matter density
  DensityArray &matter_density =
      *state.get<ArrayType>("BORG_final_density")->array;
  // Retrieve the random number generator
  auto &rgen = state.get<RandomGen>("random_generator")->get();

  // Allocate some temporary space for the biased galaxy density
  U_ArrayReal fg_galaxy_field_p(mgr->extents_real(), mgr->allocator_real);
  ArrayReal &fg_galaxy_field = fg_galaxy_field_p.get_array();

  // Allocate some more for the precomputed partially selected galaxy density
  U_ArrayReal pre_selection_field_p(mgr->extents_real(), mgr->allocator_real);
  auto pre_selection_field = fwrap(pre_selection_field_p.get_array());

  // Capture the foreground coefficients
  auto &fg_coefficient =
      *state
           .get<ArrayType1d>(
               format("catalog_foreground_coefficient_%d") % catalog)
           ->array;
  // Capture the galaxy data
  DataArray &gdata =
      *state.template get<ArrayType>(format("galaxy_data_%d") % catalog)->array;
  // The provided base selection field
  SelectionArray &sel_field =
      *state.template get<ArrayType>(format("galaxy_sel_window_%d") % catalog)
           ->array;

  double &nmean =
      state.template getScalar<double>(format("galaxy_nmean_%d") % catalog);
  BiasParamArray &bias_params =
      *state.template get<ArrayType1d>(format("galaxy_bias_%d") % catalog)
           ->array;

  // Prepare the bias function with the provided parameters.
  this->bias->prepare(*model, matter_density, nmean, bias_params, true);
  // Derive the galaxy density expression.
  BiasTuple biased_density = this->bias->compute_density(matter_density);

  // We have to specialize here to the classic selection model.
  // We unwrap the actual biased density. Be sure it is precomputed
  // and stored in the provided array.
  LibLSS::copy_array(fg_galaxy_field, std::get<0>(biased_density));

  // and save the rest
  // FIXME: This only works for some of the simplest likelihoods
  // FIXME: with no correlations between the density and the other fields.
  // FIXME: We need to find a better scheme later.
  SelectedDensityTuple sel_density =
      this->bias->selection_adaptor.apply(sel_field, biased_density);
  TupleResidual rest_of_bias = last_of_tuple<1>(sel_density);

  for (size_t e = 0; e < fgmap_list.size(); e++) {
    int fg_id = fgmap_list[e];

    if (state.getScalar<bool>(
            format("negative_foreground_%d_%d_blocked") % catalog % fg_id))
      continue;

    auto &fgmap_data = get_fgmap(state, fg_id);

    // Build the partially selected field.
    pre_selection_field = fwrap(sel_field) * fg_galaxy_field;

    for (size_t e_tilde = 0; e_tilde < fgmap_list.size(); e_tilde++) {
      if (e == e_tilde)
        continue;
      pre_selection_field =
          pre_selection_field *
          (1 - fg_coefficient[e_tilde] *
                   fwrap(get_fgmap(state, fgmap_list[e_tilde])));
    }

    // Now sample the coefficient.
    fg_coefficient[e] = slice_sweep(
        comm, rgen,
        std::bind(
            &GenericForegroundSampler<Likelihood>::bound_posterior, this,
            std::placeholders::_1, fgvalmin[e], fgvalmax[e], std::ref(gdata),
            std::ref(fgmap_data), std::ref(*pre_selection_field),
            std::ref(sel_field), std::ref(rest_of_bias)),
        fg_coefficient[e], step_norm[e]);
    ctx.print(
        format("Got value %g for foreground/catalog = (%d,%d)") %
        fg_coefficient[e] % fg_id % catalog);
  }
}
