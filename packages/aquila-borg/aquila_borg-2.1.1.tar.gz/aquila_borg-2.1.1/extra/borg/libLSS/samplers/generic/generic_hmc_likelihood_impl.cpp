/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/generic/generic_hmc_likelihood_impl.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

static const bool VERBOSE_WRITE_BORG = false;

template <class AbstractBiasType, class VoxelLikelihoodType>
void LibLSS::GenericHMCLikelihood<AbstractBiasType, VoxelLikelihoodType>::
    updateCosmology(CosmologicalParameters const &cosmo_params) {
  cosmology = std::unique_ptr<Cosmology>(new Cosmology(cosmo_params));
  model->setCosmoParams(cosmo_params);
}

template <class AbstractBiasType, class VoxelLikelihoodType>
void LibLSS::GenericHMCLikelihood<AbstractBiasType, VoxelLikelihoodType>::
    setupDefaultParameters(MarkovState &state, int catalog) {
  ArrayType1d::ArrayType &bias_params =
      *state.formatGet<ArrayType1d>("galaxy_bias_%d", catalog)->array;
  bias_params.resize(boost::extents[bias_t::numParams]);
  bias_t::setup_default(bias_params);
}

template <class AbstractBiasType, class VoxelLikelihoodType>
void LibLSS::GenericHMCLikelihood<AbstractBiasType, VoxelLikelihoodType>::
    updateMetaParameters(MarkovState &state) {
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

  state.getScalarArray<long, 6>("localNdata", localNdata);

  ares_heat = state.getScalar<double>("ares_heat");

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
}

template <class AbstractBiasType, class VoxelLikelihoodType>
double LibLSS::GenericHMCLikelihood<AbstractBiasType, VoxelLikelihoodType>::
    logLikelihoodBias(
        int catalog, double nmean,
        boost::multi_array_ref<double, 1> &bias_params) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  auto &out_density = final_density_field->get_array();
  double L = 0;

  // Enforce nmean and bias constraints
  if ((!bias_t::NmeanIsBias && nmean <= 0) ||
      !bias->check_bias_constraints(bias_params)) {
    return -std::numeric_limits<double>::infinity();
  }

  bias->prepare(*model, out_density, nmean, bias_params, false);

  auto strict_range = array::generate_slice(localNdata);

  // Create the biased density array
  auto biased_array = bias->compute_density(out_density);
  // Transform this array with the help of bias function
  auto select_array = bias->selection_adaptor.apply(
      *sel_field[catalog],
      // Provide the biased density array derived previously
      biased_array);
  // We only want voxels with a positive selection, all the others are masked out
  auto mask = b_va_fused<bool>(_p1 > 0, *sel_field[catalog]);
  // Now compute the log likelihood
  L = likelihood->log_probability(
      array::slice_array(*data[catalog], strict_range), select_array, mask);

  bias->cleanup();
  comm->all_reduce_t(MPI_IN_PLACE, &L, 1, MPI_SUM);

  return ares_heat * L + LibLSS::bias::bias_get_log_prior(*bias, bias_params);
}

template <class AbstractBiasType, class VoxelLikelihoodType>
double LibLSS::GenericHMCLikelihood<AbstractBiasType, VoxelLikelihoodType>::
    logLikelihood(ArrayRef const &s_array, bool gradientIsNext) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  using boost::format;
  using CosmoTool::square;

  auto tmp_fourier_p = mgr->allocate_complex_array();
  auto &tmp_fourier = tmp_fourier_p.get_array();
  {
    auto local_s_p = mgr->allocate_array();
    auto &local_s = local_s_p.get_array();

    fwrap(local_s[s_range()]) =
        fwrap(s_array[s_range()]) * volume / array::product(N);

    mgr->execute_r2c(analysis_plan, local_s.data(), tmp_fourier.data());
  }

  return logLikelihood(tmp_fourier, gradientIsNext);
}

template <class AbstractBiasType, class VoxelLikelihoodType>
double LibLSS::GenericHMCLikelihood<AbstractBiasType, VoxelLikelihoodType>::
    logLikelihood(CArrayRef const &s_array, bool gradientIsNext) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  using boost::format;
  using CosmoTool::square;
  auto &cosmo = *cosmology.get();

  typedef ArrayType::ArrayType::element ElementType;
  double Epoisson = 0;

  // Simulate forward model
  //setup position and velocity arrays

  auto &out_density = final_density_field->get_array();

  GenericDetails::compute_forward(
      mgr, model, cosmo.getParameters(), 0.0, *vobs->array,
      ModelInput<3>(model->lo_mgr, model->get_box_model(), s_array),
      ModelOutput<3>(
          model->out_mgr, model->get_box_model_output(), out_density),
      false);

  ctx.format(
      "Using strict range=[%d-%d]x[%d-%d]x[%d-%d]", localNdata[0],
      localNdata[1], localNdata[2], localNdata[3], localNdata[4],
      localNdata[5]);
  ctx.format(
      "Out density shape is %d x %d x %d", out_density.shape()[0],
      out_density.shape()[1], out_density.shape()[2]);
  auto strict_range = array::generate_slice(localNdata);

  for (int c = 0; c < Ncat; c++) {
    ctx.format(
        "Data[%d] shape is %d x %d x %d", c, data[c]->shape()[0],
        data[c]->shape()[1], data[c]->shape()[2]);

    bias->prepare(*model, out_density, nmean[c], *bias_params[c], (c == 0));

    // Create the biased density array
    auto biased_array = bias->compute_density(out_density);
    // Transform this array with the help of bias function
    auto select_array = bias->selection_adaptor.apply(
        *sel_field[c],
        // Provide the biased density array derived previously
        biased_array);
    // We only want voxels with a positive selection, all the others are masked out
    auto mask = b_va_fused<bool>(_p1 > 0, *sel_field[c]);
    // Now compute the log likelihood
    Epoisson += likelihood->log_probability(
        array::slice_array(*data[c], strict_range), select_array, mask);

    bias->cleanup();
  }

  comm->all_reduce_t(MPI_IN_PLACE, &Epoisson, 1, MPI_SUM);

  // We want - log Posterior here.
  return -Epoisson;
}

template <class AbstractBiasType, class VoxelLikelihoodType>
void LibLSS::GenericHMCLikelihood<AbstractBiasType, VoxelLikelihoodType>::
    commonInitialize(MarkovState &state) {
  using boost::extents;

  model = state.get<BorgModelElement>("BORG_model")->obj;

  xmin0 = state.get<SDouble>("corner0")->value;
  xmin1 = state.get<SDouble>("corner1")->value;
  xmin2 = state.get<SDouble>("corner2")->value;

  Ncat = state.getScalar<long>("NCAT");

  state.newElement("BORG_vobs", vobs = new ArrayType1d(extents[3]), true);
  state.newElement(
      "BORG_final_density",
      borg_final_density = new ArrayType(model->out_mgr->extents_real_strict()),
      true);
  std::array<ssize_t, 3> out_N;
  model->get_box_model_output().fill(out_N);
  borg_final_density->setRealDims(out_N);

  final_density_field = std::unique_ptr<Mgr::U_ArrayReal>(new Mgr::U_ArrayReal(
      model->out_mgr->extents_real(), model->out_mgr->allocator_real));

  Likelihood::GridSize gs(boost::extents[3]), mpi_gs(boost::extents[6]);
  std::copy(this->N.begin(), this->N.end(), gs.begin());
  mpi_gs[0] = model->out_mgr->startN0;
  mpi_gs[1] = model->out_mgr->startN0 + model->out_mgr->localN0;
  mpi_gs[2] = 0;
  mpi_gs[3] = model->out_mgr->N1;
  mpi_gs[4] = 0;
  mpi_gs[5] = model->out_mgr->N2;

  info[Likelihood::MPI] = comm;
  info[Likelihood::GRID] = gs;
  info[Likelihood::MPI_GRID] = mpi_gs;

  likelihood = std::make_shared<likelihood_t>(info);
  bias = std::make_shared<bias_t>(info);

  // We notify all the other samplers interested in our two objects
  // that those ones are fairly initialized. Mind you, they are not prepared
  // just ready for sharing.
  ready(likelihood, bias);
}

template <class AbstractBiasType, class VoxelLikelihoodType>
void LibLSS::GenericHMCLikelihood<AbstractBiasType, VoxelLikelihoodType>::
    initializeLikelihood(MarkovState &state) {
  using boost::extents;
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);

  commonInitialize(state);

  (*vobs->array)[0] = 0;
  (*vobs->array)[1] = 0;
  (*vobs->array)[2] = 0;

  for (int c = 0; c < Ncat; c++) {
    ArrayType1d::ArrayType &bias_params =
        *state.get<ArrayType1d>(boost::format("galaxy_bias_%d") % c)->array;
    if (bias_params.num_elements() < bias_t::numParams) {
      Console::instance().print<LOG_WARNING>(
          "Parameters for bias model are not sufficiently specified in the "
          "configuration file. Using internal defaults.");
      bias_params.resize(boost::extents[bias_t::numParams]);
      bias_t::setup_default(bias_params);
    }
  }
}

template <class AbstractBiasType, class VoxelLikelihoodType>
void LibLSS::GenericHMCLikelihood<AbstractBiasType, VoxelLikelihoodType>::
    commitAuxiliaryFields(MarkovState &state) {
  Console::instance().print<LOG_INFO_SINGLE>("Saving final density");
  array::scaleAndCopyArray3d(
      *borg_final_density->array, final_density_field->get_array(), 1, true);

  LibLSS::bias::bias_dump_fields(*bias, state);
}

namespace LibLSS {
  namespace GenericLikelihood_Details {
    // This helper allows to do a recursive reduction on element of a tuple (in U& in).
    // The reduction is accumulated and written to out. Beware that out is not cleared.
    template <size_t opid>
    struct ArrayReducer {
      template <typename T, typename U>
      static inline void apply(T &&out, const U &in) {
        ArrayReducer<opid - 1>::apply(out, in);
        LibLSS::apply_array<typename std::remove_reference<T>::type &>(
            _p1 -= _p2,            // Use phoenix accumulator
            out,                   // Specify the output array
            std::get<opid - 1>(in) // Grab the virtual array in the tuple
        );
      }
    };

    template <>
    struct ArrayReducer<0> {
      template <typename T, typename U>
      static inline void apply(T &&out, const U &in) {}
    };
  } // namespace GenericLikelihood_Details
} // namespace LibLSS

template <class AbstractBiasType, class VoxelLikelihoodType>
void LibLSS::GenericHMCLikelihood<AbstractBiasType, VoxelLikelihoodType>::
    gradientLikelihood(
        ArrayRef const &s, ArrayRef &grad_array, bool accumulate,
        double scaling) {
  ConsoleContext<LOG_DEBUG> ctx("GENERIC HMC likelihood gradient [real]");
  if (!accumulate) {
    gradientLikelihood_internal(
        ModelInput<3>(model->lo_mgr, model->get_box_model(), s),
        ModelOutputAdjoint<3>(
            model->lo_mgr, model->get_box_model(), grad_array));
    if (scaling != 1)
      fwrap(grad_array) = fwrap(grad_array) * scaling;
  } else {
    auto tmp_grad_p = mgr->allocate_array();
    auto &tmp_grad = tmp_grad_p.get_array();

    gradientLikelihood_internal(
        ModelInput<3>(model->lo_mgr, model->get_box_model(), s),
        ModelOutputAdjoint<3>(model->lo_mgr, model->get_box_model(), tmp_grad));
    fwrap(grad_array) = fwrap(grad_array) + fwrap(tmp_grad) * scaling;
  }
}

template <class AbstractBiasType, class VoxelLikelihoodType>
void LibLSS::GenericHMCLikelihood<AbstractBiasType, VoxelLikelihoodType>::
    gradientLikelihood(
        CArrayRef const &s, CArrayRef &grad_array, bool accumulate,
        double scaling) {
  ConsoleContext<LOG_DEBUG> ctx("GENERIC HMC likelihood gradient");
  if (!accumulate) {
    gradientLikelihood_internal(
        ModelInput<3>(mgr, model->get_box_model(), s),
        ModelOutputAdjoint<3>(mgr, model->get_box_model(), grad_array));
    if (scaling != 1)
      fwrap(grad_array) = fwrap(grad_array) * scaling;
  } else {
    auto tmp_gradient_p = mgr->allocate_complex_array();
    auto &tmp_gradient = tmp_gradient_p.get_array();

    gradientLikelihood_internal(
        ModelInput<3>(mgr, model->get_box_model(), s),
        ModelOutputAdjoint<3>(mgr, model->get_box_model(), tmp_gradient));
    fwrap(grad_array) = fwrap(grad_array) + scaling * fwrap(tmp_gradient);
  }
}

template <class AbstractBiasType, class VoxelLikelihoodType>
void LibLSS::GenericHMCLikelihood<AbstractBiasType, VoxelLikelihoodType>::
    gradientLikelihood_internal(
        ModelInput<3> s, ModelOutputAdjoint<3> real_gradient) {
  using CosmoTool::square;
  typedef CArrayRef::element etype;
  using boost::extents;
  using boost::format;
  using namespace LibLSS::GenericLikelihood_Details;

  ConsoleContext<LOG_DEBUG> ctx("GENERIC HMC likelihood gradient (internal)");

  auto &out_density = final_density_field->get_array();
  auto &cosmo = *cosmology.get();

  GenericDetails::compute_forward(
      mgr, model, cosmo.getParameters(), ai, *vobs->array, std::move(s),
      ModelOutput<3>(
          model->out_mgr, model->get_box_model_output(), out_density),
      true);

  auto strict_range = array::generate_slice(localNdata);
  auto density_gradient_p = model->out_mgr->allocate_array();
  auto &density_gradient = density_gradient_p.get_array();

  fwrap(density_gradient) = 0;

  // First compute the gradient in real space, and then go to
  // the fourier space and use chain rule.

  for (int c = 0; c < Ncat; c++) {
    // This prepare phase could probably be saved
    bias->prepare(*model, out_density, nmean[c], *bias_params[c], (c == 0));

    // Now we prepare the expression to collape.
    // First we derive the biased density
    auto biased_array = bias->compute_density(out_density);
    auto select_array =
        bias->selection_adaptor.apply(*sel_field[c], biased_array);
    // We only want voxels with a positive selection, all the others are masked out
    auto mask = b_va_fused<bool>(_p1 > 0, *sel_field[c]);

    // Now we start going backward, the gradient of the likelihood
    // w.r.t to all its hidden parameters held in the bias density
    auto likelihood_gradient =
        likelihood->template diff_log_probability(*data[c], select_array, mask);

    // Undo the selection
    auto ag_select = bias->selection_adaptor.adjoint_gradient(
        likelihood_gradient, *sel_field[c], biased_array);

    // Now we transform this tuple into a new by applying the adjoint gradient of the bias
    // function to each element of the tuple.
    // Undo the bias, here the bias function has to know how to collapse the tuple
    // from selection and make a new tuple.
    auto bias_gradient =
        bias->template apply_adjoint_gradient(out_density, ag_select);
    typedef decltype(bias_gradient) BiasType;

    // This adds bias_gradient elements to real_gradient, one by one.
    // Beware that openmp collapse rule is used in the process.
    // For the bifunctor we use boost::phoenix lambda operators.
    // This must be done to each element of the tuple bias_gradient. The actual
    // computation is in practice executed here and hopefully collapsed at maximum
    // density by the compiler. Also note that no real computation is done before this step.
    // The other operators above are just helping at building an expression.
    ctx.print(boost::format("Gradient array reduction for catalog %d") % c);
    ArrayReducer<std::tuple_size<BiasType>::value>::apply(
        array::slice_array(density_gradient, strict_range), bias_gradient);
    ctx.print("Done reduction");
    bias->cleanup();
  }

  ctx.print("Adjoint of forward model");
  // We have the complete likelihood gradient before forward model now.
  // Apply the adjoint gradient to this vector.
  model->adjointModel_v2(ModelInputAdjoint<3>(
      model->out_mgr, model->get_box_model_output(), density_gradient));
  model->getAdjointModelOutput(std::move(real_gradient));
  model->clearAdjointGradient();
}

template <class AbstractBiasType, class VoxelLikelihoodType>
void LibLSS::GenericHMCLikelihood<AbstractBiasType, VoxelLikelihoodType>::
    generateMockData(CArrayRef const &parameters, MarkovState &state) {
  using boost::extents;
  using boost::format;

  ConsoleContext<LOG_INFO> ctx("Borg mock data generation");

  CosmologicalParameters &cosmo_params =
      state.getScalar<CosmologicalParameters>("cosmology");
  Cosmology cosmo(cosmo_params);

  auto &out_density = final_density_field->get_array();
  auto strict_range = array::generate_slice(localNdata);

  // Run a forward model starting from these ICs.
  GenericDetails::compute_forward(
      mgr, model, cosmo_params, ai, *vobs->array,
      ModelInput<3>(model->lo_mgr, model->get_box_model(), parameters),
      ModelOutput<3>(
          model->out_mgr, model->get_box_model_output(), out_density),
      false);

  auto &real_density = *borg_final_density->array;

  // Save the generated final state
  LibLSS::copy_array(real_density, out_density);

  // The user asks for the full mock.
  // Take each subcatalog and generate the adequate data that satisfies
  // the implemented statistics.
  for (int c = 0; c < Ncat; c++) {
    ctx.format("Generating mock data %d", c);

    SelArrayType::ArrayType &sel_field =
        *state.get<SelArrayType>(format("galaxy_synthetic_sel_window_%d") % c)
             ->array;
    ArrayType::ArrayType &g_field =
        *state.get<ArrayType>(format("galaxy_data_%d") % c)->array;
    ArrayType1d::ArrayType &bias_params =
        *state.get<ArrayType1d>(format("galaxy_bias_%d") % c)->array;
    double nmean = state.get<SDouble>(format("galaxy_nmean_%d") % c)->value;

    ctx.print("Prepare");
    // Prepare the bias model
    bias->prepare(*model, real_density, nmean, bias_params, (c == 0));

    auto biased_array = bias->compute_density(real_density);
    auto select_array = bias->selection_adaptor.apply(sel_field, biased_array);

    RandomGen *rgen = state.get<RandomGen>("random_generator");

    // Generate a statistical sample from the Likelihood
    auto generator = likelihood->sample(rgen->get(), select_array);
    ctx.format(
        "Filling up/ %dx%dx%d => %dx%dx%d", generator.shape()[0],
        generator.shape()[1], generator.shape()[2], g_field.shape()[0],
        g_field.shape()[1], g_field.shape()[2]);
    ctx.format(
        "Base/ %dx%dx%d => %dx%dx%d", generator.index_bases()[0],
        generator.index_bases()[1], generator.index_bases()[2],
        g_field.index_bases()[0], g_field.index_bases()[1],
        g_field.index_bases()[2]);
    LibLSS::copy_array(g_field, generator);

    // Cleanup the bias
    ctx.print("Cleaning up");
    bias->cleanup();
  }
  ctx.print("Exiting...");
}

template <class AbstractBiasType, class VoxelLikelihoodType>
LibLSS::GenericHMCLikelihood<AbstractBiasType, VoxelLikelihoodType>::
    GenericHMCLikelihood(LikelihoodInfo &base_info)
    : super_t(
          Likelihood::getMPI(base_info), Likelihood::gridResolution(base_info),
          Likelihood::gridSide(base_info)),
      ares_heat(1.0), info(base_info), volume(array::product(this->L)) {
  mgr = std::make_shared<Mgr>(this->N[0], this->N[1], this->N[2], comm);
}
