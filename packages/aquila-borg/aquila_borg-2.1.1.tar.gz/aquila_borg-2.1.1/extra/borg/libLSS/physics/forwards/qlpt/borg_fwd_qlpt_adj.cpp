/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/qlpt/borg_fwd_qlpt_adj.cpp
    Copyright (C) 2020 Guilhem Lavaux <n.porqueres@imperial.ac.uk>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

void BorgQLptModel::qlpt_fwd_model_ag(
    PhaseArrayRef &lctime, ArrayRef &in_ag, ArrayRef &out_ag) {
  ConsoleContext<LOG_DEBUG> ctx("BORG adjoint model (particles)");

  Cosmology cosmo(cosmo_params);
  double an = af; ///set position ics at r_{0}, calculate till present epoch
  double anh =
      af; ///velocities are created at v_{0-1/2}, calculate till present epoch

  auto &phi0 = potential->get_array();

  auto array_in_t = lo_mgr->allocate_c2c_array();
  auto &array_in = array_in_t.get_array();
  auto array_out_t = lo_mgr->allocate_c2c_array();
  auto &array_out = array_out_t.get_array();

  auto array_in3_t = lo_mgr->allocate_c2c_array();
  auto &array_in3 = array_in3_t.get_array();
  auto array_out3_t = lo_mgr->allocate_c2c_array();
  auto &array_out3 = array_out3_t.get_array();

  auto psi_t = lo_mgr->allocate_c2c_array();
  auto &psi = psi_t.get_array();

  double volNorm = volume / (N0 * N1 * N2);

#pragma omp parallel for collapse(3)
  for (int i = startN0; i < startN0 + localN0; i++)
    for (int j = 0; j < N1; j++)
      for (int k = 0; k < N2; k++) {
        double p = phi0[i][j][k];
        std::complex<double> exponent(0, -phi0[i][j][k] / hbar);
        array_in[i][j][k] = exp(exponent);
      }

  auto psi0_t = lo_mgr->allocate_c2c_array();
  auto &psi0 = psi0_t.get_array();
  psi0 = array_in;

  plan = lo_mgr->create_c2c_plan(array_in.data(), array_out.data(), -1);
  lo_mgr->execute_c2c(plan, array_in.data(), array_out.data());
  lo_mgr->destroy_plan(plan);

  std::complex<double> vol(1. / (N0 * N1 * N2), 0);

  auto propagator_t = lo_mgr->allocate_c2c_array();
  auto &propagator = propagator_t.get_array();

#pragma omp parallel for collapse(3)
  for (int i = startN0; i < startN0 + localN0; i++)
    for (int j = 0; j < N1; j++)
      for (int k = 0; k < N2; k++) {
        double kk[3] = {kmode(i, N0, L0), kmode(j, N1, L1), kmode(k, N2, L2)};
        double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
        std::complex<double> exponent(0, -0.5 * hbar * ksquared * D1);
        propagator[i][j][k] = exp(exponent);
        array_in[i][j][k] = exp(exponent) * array_out[i][j][k] * vol;
      }

  plan = lo_mgr->create_c2c_plan(array_in.data(), psi.data(), 1);
  lo_mgr->execute_c2c(plan, array_in.data(), psi.data());
  lo_mgr->destroy_plan(plan);

#pragma omp parallel for collapse(3)
  for (int i = startN0; i < startN0 + localN0; i++)
    for (int j = 0; j < N1; j++)
      for (int k = 0; k < N2; k++) {
        array_in[i][j][k] = in_ag[i][j][k] * std::conj(psi[i][j][k]);
        array_in3[i][j][k] = std::conj(array_in[i][j][k]);
      }

  plan = lo_mgr->create_c2c_plan(array_in.data(), array_out.data(), -1);
  lo_mgr->execute_c2c(plan, array_in.data(), array_out.data());
  lo_mgr->destroy_plan(plan);

  plan = lo_mgr->create_c2c_plan(array_in3.data(), array_out3.data(), -1);
  lo_mgr->execute_c2c(plan, array_in3.data(), array_out3.data());
  lo_mgr->destroy_plan(plan);

#pragma omp parallel for collapse(3)
  for (int i = startN0; i < startN0 + localN0; i++)
    for (int j = 0; j < N1; j++)
      for (int k = 0; k < N2; k++) {
        array_in[i][j][k] = propagator[i][j][k] * array_out[i][j][k] * vol;
        array_in3[i][j][k] =
            std::conj(propagator[i][j][k]) * array_out3[i][j][k] * vol;
      }

  plan = lo_mgr->create_c2c_plan(array_in.data(), array_out.data(), 1);
  lo_mgr->execute_c2c(plan, array_in.data(), array_out.data());
  lo_mgr->destroy_plan(plan);

  plan = lo_mgr->create_c2c_plan(array_in3.data(), array_out3.data(), 1);
  lo_mgr->execute_c2c(plan, array_in3.data(), array_out3.data());
  lo_mgr->destroy_plan(plan);

  for (int i = startN0; i < startN0 + localN0; i++)
    for (int j = 0; j < N1; j++)
      for (int k = 0; k < N2; k++) {
        std::complex<double> iunit(0, 1 / hbar);
        std::complex<double> element = psi0[i][j][k];
        array_in[i][j][k] = -iunit * element * array_out[i][j][k] +
                            iunit * std::conj(element) * array_out3[i][j][k];
      }

  plan = lo_mgr->create_c2c_plan(array_in.data(), array_out.data(), -1);
  lo_mgr->execute_c2c(plan, array_in.data(), array_out.data());
  lo_mgr->destroy_plan(plan);

  for (int i = startN0; i < startN0 + localN0; i++)
    for (int j = 0; j < N1; j++)
      for (int k = 0; k < N2; k++) {
        double kk[3] = {kmode(i, N0, L0), kmode(j, N1, L1), kmode(k, N2, L2)};
        double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
        double fac = -1. / ksquared / (N0 * N1 * N2);

        if (std::isinf(fac))
          fac = 0.;

        if (startN0 == 0 && localN0 > 0) {
          if (i == 0) {
            if (j == 0) {
              if (k == 0 or k == N2_HC - 1) {
                fac = 0.;
              }
            }
            if (j == N1 / 2) {
              if (k == 0 or k == N2_HC - 1) {
                fac = 0.;
              }
            }
          }
        }

        if (startN0 <= N0 / 2 && startN0 + localN0 > N0 / 2) {

          if (i == N0 / 2) {
            if (j == 0) {
              if (k == 0 or k == N2_HC - 1) {
                fac = 0.;
              }
            }
            if (j == N1 / 2) {
              if (k == 0 or k == N2_HC - 1) {
                fac = 0.;
              }
            }
          }
        }

        array_in[i][j][k] = fac * array_out[i][j][k];
      }

  plan = lo_mgr->create_c2c_plan(array_in.data(), array_out.data(), 1);
  lo_mgr->execute_c2c(plan, array_in.data(), array_out.data());
  lo_mgr->destroy_plan(plan);

#pragma omp parallel for collapse(3)
  for (int i = startN0; i < startN0 + localN0; i++)
    for (int j = 0; j < N1; j++)
      for (int k = 0; k < N2; k++) {
        out_ag[i][j][k] = std::real(array_out[i][j][k]);
      }
}

void BorgQLptModel::preallocate() {}

void BorgQLptModel::adjointModel_v2(ModelInputAdjoint<3> gradient_delta) {

  preallocate();

  ///re-evaluate redshift distortions from forward run

  ///work backwards from final to initial conditions

  if (gradient_delta) {
    gradient_delta.setRequestedIO(PREFERRED_REAL);
    hold_in_gradient = std::move(gradient_delta);
  }
}

void BorgQLptModel::getAdjointModelOutput(
    ModelOutputAdjoint<3> gradient_delta) {

  gradient_delta.setRequestedIO(PREFERRED_REAL);
  qlpt_fwd_model_ag(
      *lc_timing, hold_in_gradient.getReal(), gradient_delta.getRealOutput());

  clearAdjointGradient();
}

void BorgQLptModel::clearAdjointGradient() {}
// ARES TAG: num_authors = 1
// ARES TAG: author(0) = Natalia Porqueres
// ARES TAG: email(0) = n.porqueres@imperial.ac.uk
// ARES TAG: year(0) = 2020
