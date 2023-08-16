/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/example/example_likelihood.cpp
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
#include <boost/lambda/lambda.hpp>
#include <CosmoTool/hdf5_array.hpp>
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/samplers/borg/borg_linear_likelihood.hpp"
#include "libLSS/samplers/borg/borg_linear_meta.hpp"
#include "libLSS/tools/fused_array.hpp"

using namespace LibLSS;
using boost::extents;
using boost::format;

using CosmoTool::hdf5_write_array;
using CosmoTool::square;

using boost::c_storage_order;
typedef boost::multi_array_types::extent_range range;

/*! \brief Constructor of the density sampler.
 *
 * You can do a few initializations here. However at that point,
 * the parameters of the run are not available (box size, grid size, cosmology...)
 * and it is delayed till the call to restore or initialize. 
 *
 * @params[in] comm        An MPI communicator
 */
ExampleDensitySampler::ExampleDensitySampler(MPI_Communication *comm)
    : HMCDensitySampler(comm) {}

/*! \brief Restore the state of the sampler from a markov state
 *
 * 
 * @params[in,out] state  MarkovState
 */
void ExampleDensitySampler::restore(MarkovState &state) {
  // This creates a local context which is automatically destroyed
  // when leaving this function. The default printing level is
  // indicated through the template argument. In production mode,
  // LOG_DEBUG messages are not emitted (sometimes even optimized away
  // by the compiler).
  ConsoleContext<LOG_DEBUG> ctx("restore example density sampler");

  // This call is mandatory when working with HMC. It allows to
  // the HMC to perform its own initialization and should be called
  // before your own initialization.
  restore_HMC(state);

  xmin0 = state.get<SDouble>("corner0")->value;
  xmin1 = state.get<SDouble>("corner1")->value;
  xmin2 = state.get<SDouble>("corner2")->value;

  ctx.print("Create final density");
  state.newElement(
      "BORG_final_density",
      borg_final_density = new ArrayType(
          boost::extents[range(startN0, startN0 + localN0)][N1][N2]),
      true);
  borg_final_density->setRealDims(ArrayDimension(N0, N1, N2));

  ctx.print("Grab model");
  model = state.get<BorgModelElement>("BORG_model")->obj;

  ctx.print("Ensure biases are correctly dimensioned");
  for (int c = 0; c < Ncat; c++)
    BORG::ensure_linear_bias(state, c);
}

/*! \brief Initialize the state of the sampler from a markov state
 *
 * This is called by the main loop initialization. However, 
 * @params[in,out] state MarkovState
 */
void ExampleDensitySampler::initialize(MarkovState &state) {
  // Same as for restore, console context is created for better
  // formatting.
  ConsoleContext<LOG_DEBUG> ctx("initialize example density sampler");

  // This call is mandatory when working with HMC. It allows to
  // the HMC to perform its own initialization and should be called
  // before your own initialization.
  initialize_HMC(state);

  // This grabs the value of the lower corner of the box, in unit of Mpc/h.
  // getScalar<double> ensures that the content can be safely casted
  // to the requested type. If not, at runtime, there will be a loud complaint
  // and the code would stop cleanly.
  xmin0 = state.getScalar<double>("corner0");
  xmin1 = state.getScalar<double>("corner1");
  xmin2 = state.getScalar<double>("corner2");

  // The building of this density field can be stored at your request.
  // By default only the initial density field is stored by the HMC, whereas other
  // fields must be done specifically. This happens in saveAuxiliaryAcceptedFields.
  state.newElement(
      "BORG_final_density",
      borg_final_density = new ArrayType(
          boost::extents[range(startN0, startN0 + localN0)][N1][N2]),
      true);
  borg_final_density->setRealDims(ArrayDimension(N0, N1, N2));

  //initialize model uncertainty
  model = state.get<BorgModelElement>("BORG_model")->obj;

  for (int c = 0; c < Ncat; c++)
    BORG::ensure_linear_bias(state, c);
}

ExampleDensitySampler::~ExampleDensitySampler() {}

void ExampleDensitySampler::saveAuxiliaryAcceptedFields(MarkovState &state) {
  array::scaleAndCopyArray3d(
      *borg_final_density->array, *tmp_real_field, 1, true);
}

/*! \brief Compute the value of the likelihood component of the posterior. 
 *
 * This is called by the HMC sampler at the initialization and finalization state of the integrator.
 * @params[in,out] state MarkovState
 * @params[in] s_array the complex parameters for which we need the data likelihood. In most cases it corresponds to the initial
 *                     conditions of some simulations. Note that this complex array is conventionally set to z=0 with physical units
 *                     (Mpc/h)^3
 * @params[in] final_call Set to false if an adjoint call must be expected after this call with the same initial conditions, true otherwise.  
 */
HMCDensitySampler::HamiltonianType
ExampleDensitySampler::computeHamiltonian_Likelihood(
    MarkovState &state, CArray &s_array, bool final_call) {
  using boost::lambda::_1;
  using CosmoTool::square;
  CosmologicalParameters &cosmo_params =
      state.getScalar<CosmologicalParameters>("cosmology");
  Cosmology cosmo(cosmo_params);

  ArrayType::ArrayType &growth = *state.get<ArrayType>("growth_factor")->array;
  double ai = state.get<SDouble>("borg_a_initial")->value;
  double D_init = cosmo.d_plus(ai) /
                  cosmo.d_plus(1.0); // Scale factor for initial conditions

  typedef ArrayType::ArrayType::element ElementType;
  HamiltonianType Epoisson = 0;

  // Protect the input
  array::scaleAndCopyArray3d(*tmp_complex_field, s_array, (D_init / volume));
  Hermiticity_fixup(*tmp_complex_field);

  // Simulate forward model
  //setup position and velocity arrays

  ArrayType::ArrayType *out_density = tmp_real_field;

  // Update forward model for maybe new cosmo params
  model->setCosmoParams(state.getScalar<CosmologicalParameters>("cosmology"));
  // Inform about the velocity of the observer
  model->setObserver(*vobs->array);
  // Compute forward model
  model->forwardModel(*tmp_complex_field, *out_density, false);

  for (int c = 0; c < Ncat; c++) {
    bool biasRef = state.get<SBool>(format("galaxy_bias_ref_%d") % c)->value;
    SelArrayType &sel_field =
        *state.get<SelArrayType>(format("galaxy_sel_window_%d") % c);
    ArrayType::ArrayType &g_field =
        *state.get<ArrayType>(format("galaxy_data_%d") % c)->array;
    SDouble *g_nmean = state.get<SDouble>(format("galaxy_nmean_%d") % c);
    double nmean = g_nmean->value;
    double *p_bias;
    double *p_sig2model;
    double bias;
    double sig2model;

    BORG::extract_linear_bias(state, c, p_bias, p_sig2model);
    bias = *p_bias;
    sig2model = *p_sig2model;

    SelArrayType::ArrayType sel_array = *sel_field.array;

#pragma omp parallel for schedule(static) reduction(+ : Epoisson)
    for (long n0 = startN0; n0 < startN0 + localN0; n0++) {
      for (long n1 = 0; n1 < N1; n1++) {
        for (long n2 = 0; n2 < N2; n2++) {
          double selection = sel_array[n0][n1][n2];

          if (selection > 0) {
            double Nobs = g_field[n0][n1][n2];
            double d_galaxy =
                bias * (EPSILON_VOIDS + (*out_density)[n0][n1][n2]);

            Epoisson += square(selection * nmean * (1 + d_galaxy) - Nobs) /
                        (selection * nmean *
                         (selection * nmean * bias * bias * sig2model + 1.));
          }
        }
      }
    }
  }

  Epoisson *= 0.5;

  comm->all_reduce_t(MPI_IN_PLACE, &Epoisson, 1, MPI_SUM);

  return Epoisson;
}

void ExampleDensitySampler::computeGradientPsi_Likelihood(
    MarkovState &state, CArray &s, CArrayRef &grad_array, bool accumulate) {
  using CosmoTool::square;
  typedef CArray::element etype;

  ConsoleContext<LOG_DEBUG> ctx("BORG_LINEAR likelihood gradient");

  CosmologicalParameters &cosmo_params =
      state.getScalar<CosmologicalParameters>("cosmology");
  Cosmology cosmo(cosmo_params);

  ArrayType::ArrayType &growth = *state.get<ArrayType>("growth_factor")->array;
  double ai = state.get<SDouble>("borg_a_initial")->value;
  double D_init = cosmo.d_plus(ai) /
                  cosmo.d_plus(1.0); // Scale factor for initial conditions

  // Have to protect the input array against destruction
  ctx.print(format("Scale initial conditions, D = %lg") % D_init);

  array::scaleAndCopyArray3d(*tmp_complex_field, s, D_init / volume);
  Hermiticity_fixup(*tmp_complex_field);

  // Simulate forward model
  //setup position and velocity arrays

  model->setCosmoParams(state.getScalar<CosmologicalParameters>("cosmology"));
  model->setObserver(*vobs->array);
  model->forwardModel(*tmp_complex_field, *tmp_real_field, true);

  Uninit_FFTW_Real_Array real_gradient_p(
      extents[range(startN0, startN0 + localN0)][N1][N2real], allocator_real);
  Uninit_FFTW_Real_Array::array_type &real_gradient = real_gradient_p;

  array::fill(real_gradient, 0);

  // First compute the gradient in real space, and then do
  // the fourier space and use chain rule.

  for (int c = 0; c < Ncat; c++) {
    bool biasRef = state.get<SBool>(format("galaxy_bias_ref_%d") % c)->value;
    SelArrayType::ArrayType &sel_field =
        *state.get<SelArrayType>(format("galaxy_sel_window_%d") % c)->array;
    ArrayType::ArrayType &g_field =
        *state.get<ArrayType>(format("galaxy_data_%d") % c)->array;
    double nmean = state.get<SDouble>(format("galaxy_nmean_%d") % c)->value;
    double *p_bias;
    double *p_sig2model;
    double bias;
    double sig2model;

    BORG::extract_linear_bias(state, c, p_bias, p_sig2model);
    bias = *p_bias;
    sig2model = *p_sig2model;

#pragma omp parallel for
    for (int n0 = startN0; n0 < startN0 + localN0; n0++) {
      for (int n1 = 0; n1 < N1; n1++) {
        for (int n2 = 0; n2 < N2; n2++) {
          double delta = EPSILON_VOIDS + (*tmp_real_field)[n0][n1][n2];
          double d_galaxy = bias * (delta);
          double selection = sel_field[n0][n1][n2];
          double Nobs = g_field[n0][n1][n2];

          if (selection == 0)
            continue;

          //modification of likelihood by model uncertainty sig2model
          //See equation 3.7 in BORG pm paper
          //sid2model=0 returns the original likelihood
          real_gradient[n0][n1][n2] +=
              (selection * nmean * (1 + d_galaxy) - Nobs) * bias /
              (selection * nmean * bias * bias * sig2model + 1.);
        }
      }
    }
  }

  // Now obtain the complex gradient using adjoint fft
  model->adjointModel(real_gradient); // real_gradient is input and output.
  //undo scaling of input field
  array::scaleArray3d(real_gradient, D_init / volume);
  computeFourierSpace_GradientPsi(state, real_gradient, grad_array, accumulate);
}

/*! \brief initial_density_filter
 *
 * This member function is called at the initialization of the chain to allow
 * for the developper to provide a more adequate initial conditions for the chain
 * instead of simple Gaussian random numbers. This is mostly a relic and the general
 * advice is to leave this function empty.
 *
 * @param[in,out]  state  the state of the markov chain that is in being initialized.
 */
void ExampleDensitySampler::initial_density_filter(MarkovState &state) {}

void ExampleDensitySampler::generateMockData(
    MarkovState &state, bool only_forward) {
  ConsoleContext<LOG_INFO> ctx("Borg mock data generation");

  ArrayType1d::ArrayType &pspec =
      *state.get<ArrayType1d>("powerspectrum")->array;
  IArrayType::ArrayType &adjust_array =
      *state.get<IArrayType>("adjust_mode_multiplier")->array;
  IArrayType::ArrayType &key_array = *state.get<IArrayType>("k_keys")->array;
  CArrayType::ArrayType &s_hat0 = *state.get<CArrayType>("s_hat_field")->array;
  ArrayType::ArrayType &s = *state.get<ArrayType>("s_field")->array;
  RandomGen *rgen = state.get<RandomGen>("random_generator");

  CosmologicalParameters &cosmo_params =
      state.getScalar<CosmologicalParameters>("cosmology");
  Cosmology cosmo(cosmo_params);

  double ai = state.get<SDouble>("borg_a_initial")->value;
  double D_init = cosmo.d_plus(ai) /
                  cosmo.d_plus(1.0); // Scale factor for initial conditions

  generateRandomField(state);

  array::scaleAndCopyArray3d(*tmp_complex_field, s_hat0, D_init / volume);

  model->setCosmoParams(state.getScalar<CosmologicalParameters>("cosmology"));
  model->setObserver(*vobs->array);
  model->forwardModel(*tmp_complex_field, *tmp_real_field, false);

  if (!only_forward) {
    for (int c = 0; c < Ncat; c++) {
      double nmean = state.get<SDouble>(format("galaxy_nmean_%d") % c)->value;
      double *p_bias;
      double *p_sig2model;
      double bias;
      double sig2model;

      BORG::extract_linear_bias(state, c, p_bias, p_sig2model);
      bias = *p_bias;
      sig2model = *p_sig2model;

      SelArrayType::ArrayType &sel_field =
          *state.get<SelArrayType>(format("galaxy_sel_window_%d") % c)->array;
      ArrayType::ArrayType &g_field =
          *state.get<ArrayType>(format("galaxy_data_%d") % c)->array;

      ctx.print(format("Generating mock data %d") % c);

#pragma omp parallel for schedule(static)
      for (long n0 = startN0; n0 < startN0 + localN0; n0++) {
        for (long n1 = 0; n1 < N1; n1++) {
          for (long n2 = 0; n2 < N2; n2++) {
            double R = nmean * sel_field[n0][n1][n2];
            double gmean = R * (1 + bias * (*tmp_real_field)[n0][n1][n2]);
            g_field[n0][n1][n2] = rgen->get().gaussian() * sqrt(R) + gmean;
          }
        }
      }
    }
  } else {
    for (int c = 0; c < Ncat; c++) {
      array::copyArray3d(
          *state.get<ArrayType>(format("galaxy_data_%d") % c)->array,
          *tmp_real_field, true);
    }
  }
}
