/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/lep/borg_fwd_lep_adj.cpp
    Copyright (C) 2014-2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2018 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

template <typename CIC>
void BorgLEPModel<CIC>::lep_ic_ag(
    PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, TimingArray &timing) {
  ///set cosmological parameters
  ///Initial density is scaled to initial redshift!!!
  Cosmology cosmo(cosmo_params);

  double an =
      timing[0][0]; ///set position ics at r_{0}, calculate till present epoch
  double anh = timing
      [1]
      [0]; ///velocities are created at v_{0-1/2}, calculate till present epoch
  double D0 = cosmo.d_plus(ai);
  double D1 = cosmo.d_plus(an) / D0;
  double Df1 = cosmo.d_plus(anh) / D0;
  double f1 = cosmo.g_plus(anh);
  double Hubble = cosmo.Hubble(anh) / cosmo_params.h; ///km /sec /(Mpc/h)

  ///allocate auxiliary Fourier array
  FFTW_Complex_Array &AUX1 = *AUX1_p;
  FFTW_Real_Array &aux = *aux_p;
  FFTW_Complex_Array &AUX0 = *AUX0_p;

  for (int axis = 0; axis < 3; axis++) {
    ///1. Do position/velocity derivative
    ///------------------------------------------------------------------------------

    double fac_vel = -Df1 * f1 * anh * anh * Hubble / unit_v0;
#pragma omp parallel for
    for (long l = c_startN0; l < c_startN0 + c_localN0; l++)
      for (long m = 0; m < c_N1; m++)
        for (long n = 0; n < c_N2; n++) {
          size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);
          aux[l][m][n] = -D1 * pos_ag[idx][axis] + fac_vel * vel_ag[idx][axis];
        }

    /// FFT to F-space
    mgr->execute_r2c(c_analysis_plan, aux.data(), AUX0.data());

#pragma omp parallel for
    for (long i = c_startN0; i < c_startN0 + c_localN0; i++) {
      for (long j = 0; j < c_N1; j++) {
        for (long k = 0; k < c_N2_HC; k++) {
          double kk[3];
          kk[0] = kmode(i, c_N0, L0);
          kk[1] = kmode(j, c_N1, L1);
          kk[2] = kmode(k, c_N2, L2);

          double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
          double fac = -kk[axis] / ksquared * volNorm;

          std::complex<double> &in_delta = AUX0[i][j][k];

          AUX1[i][j][k] += std::complex<double>(
              fac * in_delta.imag(), -fac * in_delta.real());
        }
      }
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
template <typename PositionArray, typename PosAgArray>
void BorgLEPModel<CIC>::lep_redshift_pos_ag(
    const PositionArray &pos, const PositionArray &vel, PosAgArray &pos_ag,
    PosAgArray &vel_ag) {
  Cosmology cosmo(cosmo_params);

  //this routine generates particle positions in redshift space
  double af = 1.; ///km /sec /Mpc
  double anh = 1.;
  double Hubble = cosmo.Hubble(anh) / cosmo_params.h; ///km /sec /(Mpc/h)

  // the code uses particle momenta p=a^2 dx/dt where x is the co-moving position
  // peculiar velocities are then given by v_pec = p/a

  //NOTE: Check coefficients
  ArrayType1d::ArrayType &observer = vobs;
  double facRSD =
      1. / af /
      Hubble; //this factor is 1/H/a for velocities in [km/sec] an additional factor arises from momentum conversion

#pragma omp parallel for
  for (long l = startN0; l < c_startN0 + c_localN0; l++)
    for (long m = 0; m < N1; m++)
      for (long n = 0; n < N2; n++) {
        size_t idx = n + c_N2 * m + c_N1 * c_N2 * (l - c_startN0);
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
        double v_los = v0 * x0 + v1 * x1 + v2 * x2;
        double slos = s_pos_ag0 * x0 + s_pos_ag1 * x1 + s_pos_ag2 * x2;

        double A = facRSD * slos / r2_los;
        double B = -2 * facRSD * v_los * slos / square(r2_los);
        double C = facRSD * v_los / r2_los;

        pos_ag[idx][0] = s_pos_ag0 + C * s_pos_ag0 + B * x0 + A * v0;
        pos_ag[idx][1] = s_pos_ag1 + C * s_pos_ag1 + B * x1 + A * v1;
        pos_ag[idx][2] = s_pos_ag2 + C * s_pos_ag2 + B * x2 + A * v2;

        vel_ag[idx][0] = A * x0;
        vel_ag[idx][1] = A * x1;
        vel_ag[idx][2] = A * x2;
      }
}
///===============================
template <typename CIC>
template <typename PositionArray, typename OutputArray>
void BorgLEPModel<CIC>::lep_density_obs_ag(
    const PositionArray &pos, OutputArray &pos_ag, OutputArray &vel_ag,
    ArrayRef &B) {
  double nmean = CosmoTool::cube(ss_factor);

  CIC::adjoint(pos, B, pos_ag, L0, L1, L2, N0, N1, N2, nmean);
  array::fill(vel_ag, 0);
}

template <int axis, typename GravityArray>
double __lep_gravity_interpolation_ag(
    const GravityArray &g, double x, double y, double z, int ix, int iy, int iz,
    int jx, int jy, int jz) {
  double rx, ry, rz, qx, qy, qz;

  switch (axis) {
  case 0:
    rx = 1;
    ry = (y - iy);
    rz = (z - iz);
    qx = -1;
    qy = 1 - ry;
    qz = 1 - rz;
    break;
  case 1:
    rx = (x - ix);
    ry = 1;
    rz = (z - iz);
    qx = 1 - rx;
    qy = -1;
    qz = 1 - rz;
    break;
  case 2:
    rx = (x - ix);
    ry = (y - iy);
    rz = 1;

    qx = 1 - rx;
    qy = 1 - ry;
    qz = -1;
    break;
  }

  return g[ix][iy][iz] * qx * qy * qz + g[ix][iy][jz] * qx * qy * rz +
         g[ix][jy][iz] * qx * ry * qz + g[ix][jy][jz] * qx * ry * rz +
         g[jx][iy][iz] * rx * qy * qz + g[jx][iy][jz] * rx * qy * rz +
         g[jx][jy][iz] * rx * ry * qz + g[jx][jy][jz] * rx * ry * rz;
}

template <typename CIC>
template <typename PositionArray>
void BorgLEPModel<CIC>::lep_force_1_ag(
    const PositionArray &pos, const PositionArray &vel, PhaseArrayRef &pos_ag,
    PhaseArrayRef &vel_ag, PhaseArrayRef &F_ag, double dtr, double dtv) {
  Uninit_FFTW_Real_Array g_p(
      force_mgr->extents_real(), force_mgr->allocator_real);
  Uninit_FFTW_Real_Array pot_p(
      force_mgr->extents_real(), force_mgr->allocator_real);
  typedef Uninit_FFTW_Real_Array::array_type GArray;
  GArray &pot = pot_p.get_array();
  GArray &g = g_p.get_array();

  //estimate gravitational potential
  //alternatively we can store the potential from the forward run
  //for the expense of higher memory requirements
  lep_gravpot(pos, pot);

  double i_d0 = f_N0 / L0;
  double i_d1 = f_N1 / L1;
  double i_d2 = f_N2 / L2;

  long Np = pos.shape()[0];

  //calculate forces and update velocities
  for (int axis = 0; axis < 3; axis++) {
    switch (axis) {
    case 0:
      array::fill(F_ag, 0);
      compute_force<0, false, 1>(g, pot);
      break;
    case 1:
      compute_force<1, false, 1>(g, pot);
      break;
    case 2:
      compute_force<2, false, 1>(g, pot);
      break;
    }

#pragma omp parallel for schedule(static)
    for (long i = 0; i < Np; i++) {
      double x = pos[i][0] * i_d0;
      double y = pos[i][1] * i_d1;
      double z = pos[i][2] * i_d2;

      int ix = (int)std::floor(x);
      int iy = (int)std::floor(y);
      int iz = (int)std::floor(z);

      int jx = (ix + 1) % f_N0;
      int jy = (iy + 1) % f_N1;
      int jz = (iz + 1) % f_N2;

      double ax, ay, az;
      //derivative of cic kernel with respect to x

      ax = __lep_gravity_interpolation_ag<0, GArray>(
               g, x, y, z, ix, iy, iz, jx, jy, jz) *
           i_d0;

      //derivative of cic kernel with respect to y
      ay = __lep_gravity_interpolation_ag<1, GArray>(
               g, x, y, z, ix, iy, iz, jx, jy, jz) *
           i_d1;

      //derivative of cic kernel with respect to z
      az = __lep_gravity_interpolation_ag<2, GArray>(
               g, x, y, z, ix, iy, iz, jx, jy, jz) *
           i_d2;

      //now add terms to force

      F_ag[i][0] +=
          ax * pos_ag[i][axis] * dtr * dtv + ax * vel_ag[i][axis] * dtv;
      F_ag[i][1] +=
          ay * pos_ag[i][axis] * dtr * dtv + ay * vel_ag[i][axis] * dtv;
      F_ag[i][2] +=
          az * pos_ag[i][axis] * dtr * dtv + az * vel_ag[i][axis] * dtv;
    }
  }
}

template <typename CIC>
template <typename PositionArray>
void BorgLEPModel<CIC>::lep_force_0_ag(
    const PositionArray &pos, const PositionArray &vel, PhaseArrayRef &pos_ag,
    PhaseArrayRef &vel_ag, PhaseArrayRef &F_ag, double dtr, double dtv) {
  long Np = pos_ag.shape()[0];

  double d0 = L0 / double(N0);
  double d1 = L1 / double(N1);
  double d2 = L2 / double(N2);
  typedef boost::multi_array<double, 1> WeightArray;

  FFTW_Complex_Array &f_AUX0 = *f_AUX0_p;
  Uninit_FFTW_Real_Array B_p(
      force_mgr->extents_real(), force_mgr->allocator_real);
  Uninit_FFTW_Real_Array g_p(
      force_mgr->extents_real(), force_mgr->allocator_real);
  Uninit_FFTW_Real_Array::array_type &g = g_p.get_array();
  Uninit_FFTW_Real_Array::array_type &B = B_p.get_array();
  WeightArray weight(boost::extents[Np]);

  array::fill(B, 0);

  for (int axis = 0; axis < 3; axis++) {
#pragma omp parallel for
    for (long i = 0; i < Np; i++) {
      weight[i] = pos_ag[i][axis] * dtr * dtv + vel_ag[i][axis] * dtv;
    }

    //do cic
    array::fill(g, 0);
    CIC::projection(
        pos, g, L0, L1, L2, f_N0, f_N1, f_N2,
        CIC_Tools::Periodic(f_N0, f_N1, f_N2), weight);

    switch (axis) {
    case 0:
      BorgLEPModel<CIC>::compute_force<0, true, -1>(B, g);
      break;
    case 1:
      BorgLEPModel<CIC>::compute_force<1, true, -1>(B, g);
      break;
    case 2:
      BorgLEPModel<CIC>::compute_force<2, true, -1>(B, g);
      break;
    }
  }

  //transform density to F-space
  force_mgr->execute_r2c(f_analysis_plan, B.data(), f_AUX0.data());

  double normphi = 3. / 2. * cosmo_params.omega_m / double(f_N0 * f_N1 * f_N2) /
                   (unit_r0 * unit_r0);

#pragma omp parallel for
  for (int i = 0; i < f_startN0 + f_localN0; i++) {
    double sin20 = sin2K[0][i];
    for (int j = 0; j < f_N1; j++) {
      double sin21 = sin2K[1][j];
      for (int k = 0; k < f_N2_HC; k++) {
        double sin22 = sin2K[2][k];

        double Greens = -normphi / (sin20 + sin21 + sin22);
        f_AUX0[i][j][k] *= Greens;
      }
    }
  }

  //fix zero mode by hand
  if (f_startN0 == 0 && f_localN0 > 0) {
    f_AUX0[0][0][0] = 0;
  }

  force_mgr->execute_c2r(f_synthesis_plan, f_AUX0.data(), B.data());

  double nmean = CosmoTool::cube(double(ss_factor) / f_factor);
  CIC::adjoint(pos, B, F_ag, L0, L1, L2, f_N0, f_N1, f_N2, nmean);
}

template <typename CIC>
template <typename ForceArray>
void BorgLEPModel<CIC>::lep_pos_update_ag(
    PhaseArrayRef &pos_ag, const ForceArray &F_ag, double dtr) {
  long Np = pos_ag.shape()[0];

#pragma omp parallel for
  for (long i = 0; i < Np; i++) {
    for (int j = 0; j < 3; j++)
      pos_ag[i][j] += F_ag[i][j];
  }
}

template <typename CIC>
void BorgLEPModel<CIC>::lep_vel_update_ag(
    PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, double dtr) {
  long Np = pos_ag.shape()[0];

#pragma omp parallel for
  for (long i = 0; i < Np; i++) {
    for (int j = 0; j < 3; j++)
      vel_ag[i][j] += pos_ag[i][j] * dtr;
  }
}

template <typename CIC>
void BorgLEPModel<CIC>::lep_stepping_ag(
    TapeArrayRef &pos, TapeArrayRef &vel, PhaseArrayRef &pos_ag,
    PhaseArrayRef &vel_ag, int nstep, TimingArray &timing) {
  //define adjoint force array
  using boost::lambda::_1;
  using boost::lambda::_2;
  U_PhaseArray F_ag_0_p(extents[c_localN0 * c_N1 * c_N2][3]);
  U_PhaseArray::array_type &F_ag_0 = F_ag_0_p.get_array();
  U_PhaseArray F_ag_1_p(extents[c_localN0 * c_N1 * c_N2][3]);
  U_PhaseArray::array_type &F_ag_1 = F_ag_1_p.get_array();

  // MAIN LOOP : undo Leapfrog stepping
  for (int nn = nstep - 2; nn > -1; nn--) {
    double dtr = timing[2][nn];
    double dtv = timing[3][nn];

    //order of force term is important as they will be added up!!!!
#pragma omp task shared(pos, vel, pos_ag, vel_ag, F_ag_0)
    { lep_force_0_ag(pos[nn], vel[nn], pos_ag, vel_ag, F_ag_0, dtr, dtv); }
#pragma omp task shared(pos, vel, pos_ag, vel_ag, F_ag_1)
    { lep_force_1_ag(pos[nn], vel[nn], pos_ag, vel_ag, F_ag_1, dtr, dtv); }
#pragma omp taskwait
    lep_vel_update_ag(pos_ag, vel_ag, dtr);
    lep_pos_update_ag(
        pos_ag,
        b_fused<U_PhaseArray::array_type::element>(F_ag_0, F_ag_1, _1 + _2),
        dtr);
  }
}

template <typename CIC>
void BorgLEPModel<CIC>::lep_fwd_model_ag(
    ArrayRef &B, TapeArrayRef &pos, TapeArrayRef &vel, ArrayRef &DPSI,
    TimingArray &timing) {
  ConsoleContext<LOG_DEBUG> ctx("BORG-lep adjoint model");
  int nstep = timing.shape()[1];

  ///NOTE: ICs are generated at ai

  ///introduce adjoint quantities
  typedef U_PhaseArray::array_type PhaseArrayRef;
  U_PhaseArray pos_ag_p(extents[c_localN0 * c_N1 * c_N2][3]);
  U_PhaseArray vel_ag_p(extents[c_localN0 * c_N1 * c_N2][3]);

  PhaseArrayRef &pos_ag = pos_ag_p.get_array();
  PhaseArrayRef &vel_ag = vel_ag_p.get_array();

  if (do_redshift) {
    ctx.print("doing redshift space distortions.");

    U_PhaseArray s_pos_u(extents[c_localN0 * c_N1 * c_N2][3]);
    PhaseArrayRef &s_pos = s_pos_u.get_array();

    lep_redshift_pos(pos[nstep - 1], vel[nstep - 1], s_pos);
    ///work backwards from final to initial conditions
    //1.) undo CIC
    lep_density_obs_ag(s_pos, pos_ag, vel_ag, B);

    //2.) undo redshift distortions
    lep_redshift_pos_ag(pos[nstep - 1], vel[nstep - 1], pos_ag, vel_ag);
  } else {
    lep_density_obs_ag(pos[nstep - 1], pos_ag, vel_ag, B);
  }

  //2.) undo lep-stepping
  lep_stepping_ag(pos, vel, pos_ag, vel_ag, nstep, timing);

  //N.) undo ICs
  lep_ic_ag(pos_ag, vel_ag, timing);

  // Apply gradient upgrade operator
  if (c_deltao != 0) {
    array::fill(*tmp_complex_field, 0);
    lo_mgr->degrade_complex(*mgr, *AUX1_p, *tmp_complex_field);
    lo_mgr->execute_c2r(synthesis_plan, tmp_complex_field->data(), DPSI.data());
  } else {
    lo_mgr->execute_c2r(synthesis_plan, AUX1_p->data(), DPSI.data());
  }
}
// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2014-2018
// ARES TAG: name(1) = Jens Jasche
// ARES TAG: email(1) = jens.jasche@fysik.su.se
// ARES TAG: year(1) = 2009-2018
~
