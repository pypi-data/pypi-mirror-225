/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/lpt/borg_fwd_lpt_adj.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2018 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

template <typename CIC>
void BorgLptModel<CIC>::lpt_ic_ag(
    PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, PhaseArrayRef &lctim) {
  ///set cosmological parameters
  ///Initial density is scaled to initial redshift!!!

  ConsoleContext<LOG_DEBUG> ctx("LPT-IC adjoint");
  Cosmology cosmo(cosmo_params);

  double an = af; ///set position ics at r_{0}, calculate till present epoch
  double anh =
      af; ///velocities are created at v_{0-1/2}, calculate till present epoch
  double Hubble = cosmo.Hubble(anh) / cosmo_params.h; ///km /sec /(Mpc/h)
  double c_volNorm = 1 / volume;

  ///allocate auxiliary Fourier array
  auto &AUX1 = *AUX1_p;
  auto &aux = *aux_p;
  auto &AUX0 = *AUX0_p;

  array::fill(AUX1, 0);

  for (int axis = 0; axis < 3; axis++) {

    ///1. Do position derivative
    ///------------------------------------------------------------------------------
#pragma omp parallel for collapse(3)
    for (int l = c_startN0; l < c_startN0 + c_localN0; l++)
      for (int m = 0; m < c_N1; m++)
        for (int n = 0; n < c_N2; n++) {
          size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);
          double DD1 = lctim[idx][0];
          double V_SCALING = lctim[idx][1];
          aux[l][m][n] =
              -DD1 * pos_ag[idx][axis] + V_SCALING * vel_ag[idx][axis];
        }

    /// FFT to F-space
    mgr->execute_r2c(c_analysis_plan, aux.data(), AUX0.data());

    size_t Ns[3] = {size_t(c_N0) / 2, size_t(c_N1) / 2, size_t(c_N2) / 2};
#pragma omp parallel for collapse(3)
    for (size_t i = c_startN0; i < c_startN0 + c_localN0; i++)
      for (size_t j = 0; j < c_N1; j++)
        for (size_t k = 0; k < c_N2_HC; k++) {
          double kk[3] = {
              kmode(i, c_N0, L0), kmode(j, c_N1, L1), kmode(k, c_N2, L2)};
          size_t ijk[3] = {i, j, k};

          double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
          double fac = -kk[axis] / ksquared * c_volNorm;

          std::complex<double> &in_delta = AUX0[i][j][k];

          if (ijk[axis] != Ns[axis])
            AUX1[i][j][k] += std::complex<double>(
                fac * in_delta.imag(), -fac * in_delta.real());
        }
  }

  //fix hermiticity...unclear how to do that
  if (c_startN0 == 0 && c_localN0 > 0) {
    AUX1[0][0][0] = 0;
    AUX1[0][0][c_N2_HC - 1] = 0;
    AUX1[0][c_N1 / 2][0] = 0;
    AUX1[0][c_N1 / 2][c_N2_HC - 1] = 0;
  }

  if (c_startN0 <= c_N0 / 2 && c_startN0 + c_localN0 > c_N0 / 2) {
    AUX1[c_N0 / 2][0][0] = 0;
    AUX1[c_N0 / 2][0][c_N2_HC - 1] = 0;
    AUX1[c_N0 / 2][c_N1 / 2][0] = 0;
    AUX1[c_N0 / 2][c_N1 / 2][c_N2_HC - 1] = 0;
  }
}

///===============================
template <typename CIC>
void BorgLptModel<CIC>::lpt_redshift_pos_ag(
    PhaseArrayRef &pos, PhaseArrayRef &vel, PhaseArrayRef &pos_ag,
    PhaseArrayRef &vel_ag, PhaseArrayRef &lctim) {
  Cosmology cosmo(cosmo_params);

  //this routine generates particle positions in redshift space
  double anh = af;
  double Hubble = cosmo.Hubble(anh) / cosmo_params.h; ///km /sec /(Mpc/h)

  // the code uses particle momenta p=a^2 dx/dt where x is the co-moving position
  // peculiar velocities are then given by v_pec = p/a

  //NOTE: Check coefficients
  boost::array<double, 3> observer = {vobs[0], vobs[1], vobs[2]};

#pragma omp parallel for
  for (size_t idx = 0; idx < redshiftInfo.localNumParticlesBefore; idx++) {
    double x0 = pos[idx][0] + xmin0;
    double x1 = pos[idx][1] + xmin1;
    double x2 = pos[idx][2] + xmin2;

    double v0 = vel[idx][0] + observer[0];
    double v1 = vel[idx][1] + observer[1];
    double v2 = vel[idx][2] + observer[2];

    double s_pos_ag0 = pos_ag[idx][0];
    double s_pos_ag1 = pos_ag[idx][1];
    double s_pos_ag2 = pos_ag[idx][2];

    double r2_los = x0 * x0 + x1 * x1 + x2 * x2;
    double v_los = x0 * v0 + x1 * v1 + x2 * v2;
    double facRSD = lctim
        [idx]
        [2]; //this factor is 1/H/a for velocities in [km/sec] an additional factor arises from momentum conversion

    double slos = s_pos_ag0 * x0 + s_pos_ag1 * x1 + s_pos_ag2 * x2;

    double A = facRSD * slos / r2_los;
    double B = -2 * facRSD * v_los * slos / square(r2_los);
    double C = facRSD * v_los / r2_los;

    pos_ag[idx][0] = s_pos_ag0 * (1 + C) + B * x0 + A * v0;
    pos_ag[idx][1] = s_pos_ag1 * (1 + C) + B * x1 + A * v1;
    pos_ag[idx][2] = s_pos_ag2 * (1 + C) + B * x2 + A * v2;

    vel_ag[idx][0] = A * x0;
    vel_ag[idx][1] = A * x1;
    vel_ag[idx][2] = A * x2;
  }
}

///===============================
template <typename CIC>
template <typename PositionArray>
void BorgLptModel<CIC>::lpt_density_obs_ag(
    PositionArray &pos, PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag,
    ArrayRef const &B, size_t numParts) {
  double nmean = double(c_N0 * c_N1 * c_N2) /
                 (box_output.N0 * box_output.N1 * box_output.N2);
  typedef UninitializedArray<boost::multi_array<double, 3>> U_Array;

  if (ALWAYS_MPI(comm)) {
    // Allocate a temporary density field with extra planes for the
    // the projection leakage
    U_Array tmp_delta(out_mgr->extents_real(CIC::MPI_PLANE_LEAKAGE));

    density_exchange_planes_ag(
        comm, tmp_delta.get_array(), B, out_mgr, CIC::MPI_PLANE_LEAKAGE);
    CIC::adjoint(
        pos, tmp_delta.get_array(), pos_ag, L0, L1, L2, box_output.N0,
        box_output.N1, box_output.N2,
        typename CIC::Periodic_MPI(
            box_output.N0, box_output.N1, box_output.N2, comm),
        nmean, numParts);
  } else {
    // This is simple, no copy, no adjustment
    CIC::adjoint(
        pos, B, pos_ag, L0, L1, L2, box_output.N0, box_output.N1, box_output.N2,
        CIC_Tools::Periodic(box_output.N0, box_output.N1, box_output.N2), nmean,
        numParts);
  }
}

template <typename CIC>
void BorgLptModel<CIC>::lpt_fwd_model_ag(
    PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, PhaseArrayRef &lctime,
    CArrayRef &out_ag) {
  ConsoleContext<LOG_DEBUG> ctx("BORG adjoint model (particles)");

  ///NOTE: ICs are generated at ai

  //N.) undo ICs
  lpt_ic_ag(pos_ag, vel_ag, lctime);

  // RESULT is in AUX1

  if (c_deltao != 0) {
    array::fill(out_ag, 0);
    lo_mgr->degrade_complex(*mgr, *AUX1_p, out_ag);
  } else {
    fwrap(out_ag) = *AUX1_p;
  }
}

template <typename CIC>
void BorgLptModel<CIC>::preallocate() {
  size_t refPartNum = size_t(c_localN0 * c_N1 * c_N2 * partFactor);
  auto partExt = boost::extents[refPartNum][3];

  if (!u_pos_ag) {
    u_pos_ag = std::make_shared<U_PArray>(partExt);
    u_vel_ag = std::make_shared<U_PArray>(partExt);
    U_PArray::array_type &pos_ag = u_pos_ag->get_array();
    U_PArray::array_type &vel_ag = u_vel_ag->get_array();

    array::fill(pos_ag, 0);
    array::fill(vel_ag, 0);
  }
}

template <typename CIC>
void BorgLptModel<CIC>::adjointModel_v2(ModelInputAdjoint<3> gradient_delta) {
  ConsoleContext<LOG_DEBUG> ctx("BORG adjoint model");
  // This function computes the adjoint gradient in place. The adjoint gradient of the final density must be provided, in exchange
  // the adjoint gradient of the initial field is returned
  //
  ///introduce adjoint quantities
  // This must be allocated in two steps to avoid the implicit
  // zero initialization.

  preallocate();
  auto &pos_ag = u_pos_ag->get_array();
  auto &vel_ag = u_vel_ag->get_array();
  auto &pos = u_pos->get_array();
  auto &vel = u_vel->get_array();

  ///re-evaluate redshift distortions from forward run
  if (do_rsd) {
    PhaseArrayRef &s_pos = u_s_pos->get_array();
    ctx.print("doing redshift space distortions.");

    ///work backwards from final to initial conditions
    //1.) undo CIC
    if (gradient_delta) {
      gradient_delta.setRequestedIO(PREFERRED_REAL);
      lpt_density_obs_ag(
          s_pos, pos_ag, vel_ag, gradient_delta.getRealConst(),
          redshiftInfo.localNumParticlesAfter);
    }

    particle_undistribute(redshiftInfo, pos_ag);

    //2.) undo redshift distortions
    lpt_redshift_pos_ag(pos, vel, pos_ag, vel_ag, *lc_timing);

  } else {
    ///work backwards from final to initial conditions
    //1.) undo CIC
    if (gradient_delta) {
      gradient_delta.setRequestedIO(PREFERRED_REAL);
      lpt_density_obs_ag(
          pos, pos_ag, vel_ag, gradient_delta.getRealConst(),
          realInfo.localNumParticlesAfter);
    }
  }
}

template <typename CIC>
void BorgLptModel<CIC>::getAdjointModelOutput(
    ModelOutputAdjoint<3> gradient_delta) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  auto &pos_ag = u_pos_ag->get_array();
  auto &vel_ag = u_vel_ag->get_array();

  if (!do_rsd)
    particle_undistribute(
        realInfo, pos_ag, make_attribute_helper(Particles::vector(vel_ag)));

  gradient_delta.setRequestedIO(PREFERRED_FOURIER);
  lpt_fwd_model_ag(
      pos_ag, vel_ag, *lc_timing, gradient_delta.getFourierOutput());

  clearAdjointGradient();
}

template <typename CIC>
void BorgLptModel<CIC>::adjointModelParticles(
    PhaseArrayRef &grad_pos, PhaseArrayRef &grad_vel) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  if (do_rsd) {
    error_helper<ErrorBadState>(
        "RSD and adjointModelParticles do not work together.");
  }

  preallocate();
  auto w_p = fwrap(u_pos_ag->get_array());
  auto w_v = fwrap(u_vel_ag->get_array());
  w_p = w_p + fwrap(grad_pos);
  w_v = w_v + fwrap(grad_vel);
}

template <typename CIC>
void BorgLptModel<CIC>::clearAdjointGradient() {
  u_pos_ag.reset();
  u_vel_ag.reset();
}
// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2014-2020
// ARES TAG: name(1) = Jens Jasche
// ARES TAG: email(1) = jens.jasche@fysik.su.se
// ARES TAG: year(1) = 2009-2018
