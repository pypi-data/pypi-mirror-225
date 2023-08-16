/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/qlpt/borg_fwd_qlpt.cpp
    Copyright (C) 2020 Guilhem Lavaux <n.porqueres@imperial.ac.uk>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

#include "../pm/plane_xchg.hpp"

void BorgQLptModel::qlpt_ic(CArrayRef &deltao, PhaseArrayRef &lctim) {
  ///set cosmological parameters
  ///Initial density is scaled to initial redshift!!!
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  Cosmology cosmo(cosmo_params);

  double an = af; ///set position ics at r_{0}, calculate till present epoch
  double anh =
      af; ///velocities are created at v_{0-1/2}, calculate till present epoch
  double Hubble = cosmo.Hubble(anh) / cosmo_params.h; ///km /sec /(Mpc/h)

  double volNorm = 1. / (L0 * L1 * L2);

  typedef UninitializedArray<
      FFTW_Complex_Array, FFTW_Allocator<std::complex<double>>>
      U_CArray;
  typedef U_CArray::array_type Ref_CArray;

  auto &phi0 = potential->get_array();

  U_CArray tmp_p(mgr->extents_complex(), mgr->allocator_complex);
  Ref_CArray &tmp = tmp_p.get_array();

#pragma omp parallel for collapse(3)
  for (int i = startN0; i < startN0 + localN0; i++)
    for (int j = 0; j < N1; j++)
      for (int k = 0; k < N2_HC; k++) {
        double kk[3] = {kmode(i, N0, L0), kmode(j, N1, L1), kmode(k, N2, L2)};

        double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
        double fac = -1. / ksquared;
        std::complex<double> &in_delta = deltao[i][j][k];
        tmp[i][j][k] = fac * in_delta * volNorm;
      }

  if (startN0 == 0 && localN0 > 0) {
    tmp[0][0][0] = 0;
    tmp[0][0][N2_HC - 1] = 0;
    tmp[0][N1 / 2][0] = 0;
    tmp[0][N1 / 2][N2_HC - 1] = 0;
  }

  if (startN0 <= N0 / 2 && startN0 + localN0 > N0 / 2) {
    tmp[N0 / 2][0][0] = 0;
    tmp[N0 / 2][0][N2_HC - 1] = 0;
    tmp[N0 / 2][N1 / 2][0] = 0;
    tmp[N0 / 2][N1 / 2][N2_HC - 1] = 0;
  }

#pragma omp parallel for collapse(3)
  for (int i = startN0; i < startN0 + localN0; i++)
    for (int j = 0; j < N1; j++)
      for (int k = 0; k < N2_HC; k++) {
        (tmp_complex_field->get_array())[i][j][k] = tmp[i][j][k];
      }

  lo_mgr->execute_c2r(
      synthesis_plan, tmp_complex_field->get_array().data(), phi0.data());
}

void BorgQLptModel::qlpt_density_obs(ArrayRef &deltao, size_t numParts) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  bool do_velocities = 0;

  Cosmology cosmo(cosmo_params);
  double an = af; ///set position ics at r_{0}, calculate till present epoch
  double anh =
      af; ///velocities are created at v_{0-1/2}, calculate till present epoch

  auto &phi0 = potential->get_array();

  //std::string fname = "phi.h5";
  //H5::H5File f(fname, H5F_ACC_TRUNC);
  //CosmoTool::hdf5_write_array(f, "phi", phi0);

  auto array_in_t = lo_mgr->allocate_c2c_array();
  auto &array_in = array_in_t.get_array();
  auto array_out_t = lo_mgr->allocate_c2c_array();
  auto &array_out = array_out_t.get_array();

#pragma omp parallel for collapse(3)
  for (int i = startN0; i < startN0 + localN0; i++)
    for (int j = 0; j < N1; j++)
      for (int k = 0; k < N2; k++) {
        double p = phi0[i][j][k];
        std::complex<double> exponent(0, -phi0[i][j][k] / hbar);
        array_in[i][j][k] = exp(exponent);
      }

  DFT_Manager::Calls::plan_type plan =
      lo_mgr->create_c2c_plan(array_in.data(), array_out.data(), -1);
  lo_mgr->execute_c2c(plan, array_in.data(), array_out.data());
  lo_mgr->destroy_plan(plan);

  std::complex<double> vol(1. / (N0 * N1 * N2), 0);

#pragma omp parallel for collapse(3)
  for (int i = startN0; i < startN0 + localN0; i++)
    for (int j = 0; j < N1; j++)
      for (int k = 0; k < N2; k++) {
        double kk[3] = {kmode(i, N0, L0), kmode(j, N1, L1), kmode(k, N2, L2)};
        double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
        std::complex<double> exponent(0, -0.5 * hbar * ksquared * D1);
        array_in[i][j][k] = exp(exponent) * array_out[i][j][k] * vol;
      }

  plan = lo_mgr->create_c2c_plan(array_in.data(), array_out.data(), 1);
  lo_mgr->execute_c2c(plan, array_in.data(), array_out.data());
  lo_mgr->destroy_plan(plan);

#pragma omp parallel for collapse(3)
  for (int i = startN0; i < startN0 + localN0; i++)
    for (int j = 0; j < N1; j++)
      for (int k = 0; k < N2; k++) {
        std::complex<double> psi = array_out[i][j][k];
        deltao[i][j][k] = std::real(psi * std::conj(psi)) - 1.;
      }

  if (do_velocities) {
    std::string fname = "psi.h5";
    H5::H5File f(fname, H5F_ACC_TRUNC);
    CosmoTool::hdf5_write_array(f, "psi", array_out);
    CosmoTool::hdf5_write_array(f, "density", deltao);
  }

  if (DUMP_BORG_DENSITY) {
    std::string fname = str(format("borg_density_%d.h5") % comm->rank());
    H5::H5File f(fname, H5F_ACC_TRUNC);
    CosmoTool::hdf5_write_array(f, "density", deltao);
  }
}

void BorgQLptModel::qlpt_fwd_model(CArrayRef &deltao, PhaseArrayRef &lctim) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  if (false) {
    static int step = 0;
    std::string fname = str(format("fwd_ic_%d_%d.h5") % step % comm->rank());
    H5::H5File f(fname, H5F_ACC_TRUNC);
    CosmoTool::hdf5_write_array(f, "deltao", deltao);
    step++;
  }

  qlpt_ic(deltao, lctim);
}

void BorgQLptModel::forwardModelRsdField(ArrayRef &deltaf, double *vobs_ext) {
  ConsoleContext<LOG_DEBUG> ctx("BORG forward model rsd density calculation");
}

void BorgQLptModel::test_qlpt_velocities(MarkovState &state) {}

void BorgQLptModel::forwardModel_v2(ModelInput<3> delta_init) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  delta_init.setRequestedIO(PREFERRED_FOURIER);

  delta_init.needDestroyInput();
  qlpt_fwd_model(delta_init.getFourier(), lc_timing->get_array());
}

void BorgQLptModel::getDensityFinal(ModelOutput<3> delta_output) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  delta_output.setRequestedIO(PREFERRED_REAL);

  qlpt_density_obs(
      delta_output.getRealOutput(), realInfo.localNumParticlesAfter);

  /* if (!forwardModelHold && !adjointRequired) {
    releaseParticles();
  }*/
  forwardModelHold = false;
}
// ARES TAG: num_authors = 1
// ARES TAG: author(0) = Natalia Porqueres
// ARES TAG: email(0) = n.porqueres@imperial.ac.uk
// ARES TAG: year(0) = 2020

