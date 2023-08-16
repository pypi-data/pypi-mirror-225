/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/tests/generic_mock.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TEST_GENERIC_MOCK_HPP
#define __LIBLSS_TEST_GENERIC_MOCK_HPP

#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/physics/likelihoods/voxel_poisson.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include <CosmoTool/hdf5_array.hpp>

template <typename Likelihood>
void generate_mock_data(
    LibLSS::MPI_Communication *comm, LibLSS::MarkovState &state, size_t const N,
    double const L) {
  using namespace LibLSS;
  typedef typename Likelihood::bias_t bias_t;
  double const nmean = state.getScalar<double>("galaxy_nmean_0");
  auto const &bias_params = *state.get<ArrayType1d>("galaxy_bias_0")->array;
  auto model = state.get<BorgModelElement>("BORG_model")->obj;

  // Make three sinus
  double const epsilon = 0.1;

  typedef FFTW_Manager_3d<double> FFT_Manager;
  FFT_Manager mgr(N, N, N, comm);
  FFT_Manager::ArrayReal ic_field(
      mgr.extents_real(), boost::c_storage_order(), mgr.allocator_real);
  FFT_Manager::ArrayReal final_density(
      model->out_mgr->extents_real(), boost::c_storage_order(), model->out_mgr->allocator_real);
  FFT_Manager::ArrayFourier ic_field_hat(
      mgr.extents_complex(), boost::c_storage_order(), mgr.allocator_complex);

  auto rhom = fwrap(ic_field);

  rhom = LibLSS::b_fused_idx<double, 3>(
      [N, epsilon](size_t const i, size_t const j, size_t const k) -> double {
        double x = double(i) / N;
        double z = double(j) / N;
        double y = double(k) / N;

        return epsilon * sin(M_PI * x) * sin(M_PI * y) * sin(M_PI * z);
      });

  // Compute the Fourier transform, as that is the required input for the forward
  // model.
  auto w_ic_hat = fwrap(ic_field_hat);
  FFT_Manager::plan_type aplan =
      mgr.create_r2c_plan(ic_field.data(), ic_field_hat.data());
  mgr.execute_r2c(aplan, ic_field.data(), ic_field_hat.data());
  w_ic_hat = w_ic_hat * double((L * L * L) / (N * N * N));
  fwrap(*state.get<CArrayType>("s_hat_field")->array) = ic_field_hat;

  auto vobs = state.get<ArrayType1d>("BORG_vobs")->array;

  typedef ScalarStateElement<CosmologicalParameters> CosmoElement;
  GenericDetails::compute_forward(
      model->lo_mgr, model, state.get<CosmoElement>("cosmology")->value,
      state.getScalar<double>("borg_a_initial"), *vobs, ModelInput<3>(model->lo_mgr, model->get_box_model(), ic_field_hat),
      ModelOutput<3>(model->out_mgr, model->get_box_model_output(), final_density), false);

  auto data = fwrap(*state.get<ArrayType>("galaxy_data_0")->array);

  RandomNumber &rgen = state.get<RandomGen>("random_generator")->get();

  // Make nmean=3, data
  bias_t bias_func;
  bias_func.prepare(*model, final_density, nmean, bias_params, true);
  Console::instance().print<LOG_VERBOSE>(
      "Density field ready. Now do joint selection + sample of mock data");
  data = Likelihood::likelihood_t::sample(
      rgen, bias_func.selection_adaptor.apply(
                b_fused_idx<double, 3>(
                    FuseWrapper_detail::constantFunctor<double>(1),
                    boost::extents[N][N][N]),
                bias_func.compute_density(final_density)));
  Console::instance().print<LOG_VERBOSE>("Done with mock. Save now.");
  bias_func.cleanup();

  H5::H5File f("mock.h5", H5F_ACC_TRUNC);
  CosmoTool::hdf5_write_array(f, "data", *data);
  CosmoTool::hdf5_write_array(f, "ic_field", ic_field);
  CosmoTool::hdf5_write_array(f, "ic_hat_field", ic_field_hat);
  CosmoTool::hdf5_write_array(f, "final_density", final_density);
}

#endif
