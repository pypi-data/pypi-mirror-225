/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/lep/borg_fwd_lep.cpp
    Copyright (C) 2014-2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2018 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
template <typename CIC>
void BorgLEPModel<CIC>::lep_ic(
    CArrayRef &deltao, TapeArrayRef &pos, TapeArrayRef &vel,
    TimingArray &timing) {
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

  Console::instance().print<LOG_DEBUG>(
      format("D0=%g, D1=%g, Df1=%g, f1=%g, Hubble=%g") % D0 % D1 % Df1 % f1 %
      Hubble);

  typedef UninitializedArray<
      FFTW_Complex_Array, FFTW_Allocator<std::complex<double>>>
      U_CArray;
  typedef U_CArray::array_type Ref_CArray;

  U_CArray tmp_p(mgr->extents_complex(), mgr->allocator_complex);
  Ref_CArray &tmp = tmp_p.get_array();

  ///allocate new array for Eulerian grav-pot calculculation
  U_CArray tmp_g(mgr->extents_complex(), mgr->allocator_complex);
  Ref_CArray &tmp_grav = tmp_g.get_array();

  Uninit_FFTW_Real_Array pot_p(mgr->extents_real(), mgr->allocator_real);
  Uninit_FFTW_Real_Array::array_type &pot = pot_p.get_array();

  ///set gravitational potential normalization
  //scale potential to first timestep
  double normphi =
      D1 * 3. / 2. * cosmo_params.omega_m *
      (unit_r0 * unit_r0); ///maybe we miss a Fourier normalization here

  for (int axis = 0; axis < 3; axis++) {
#pragma omp parallel for
    for (int i = c_startN0; i < c_startN0 + c_localN0; i++)
      for (int j = 0; j < c_N1; j++)
        for (int k = 0; k < c_N2_HC; k++) {
          double kk[3];
          kk[0] = kmode(i, c_N0, L0);
          kk[1] = kmode(j, c_N1, L1);
          kk[2] = kmode(k, c_N2, L2);

          double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
          double fac = -kk[axis] / (ksquared);

          std::complex<double> &in_delta = deltao[i][j][k];

          //calculate large scale gravitational potential
          tmp_grav[i][j][k] =
              (-1) * normphi * in_delta / (ksquared); //check sign!!!

          tmp[i][j][k] = std::complex<double>(
              -fac * in_delta.imag(), fac * in_delta.real()

          );
        }

    if (c_startN0 == 0 && c_localN0 > 0) {
      tmp[0][0][0] = 0;
      tmp[0][0][c_N2 / 2] = 0;
      tmp[0][c_N1 / 2][0] = 0;
      tmp[0][c_N1 / 2][c_N2 / 2] = 0;
      tmp_grav[0][0][0] = 0;
      tmp_grav[0][0][c_N2 / 2] = 0;
      tmp_grav[0][c_N1 / 2][0] = 0;
      tmp_grav[0][c_N1 / 2][c_N2 / 2] = 0;
    }

    if (c_startN0 <= c_N0 / 2 && c_startN0 + c_localN0 > c_N0 / 2) {
      tmp[c_N0 / 2][0][0] = 0;
      tmp[c_N0 / 2][0][c_N2 / 2] = 0;
      tmp[c_N0 / 2][c_N1 / 2][0] = 0;
      tmp[c_N0 / 2][c_N1 / 2][c_N2 / 2] = 0;
      tmp_grav[c_N0 / 2][0][0] = 0;
      tmp_grav[c_N0 / 2][0][c_N2 / 2] = 0;
      tmp_grav[c_N0 / 2][c_N1 / 2][0] = 0;
      tmp_grav[c_N0 / 2][c_N1 / 2][c_N2 / 2] = 0;
    }

    ///Now build lep forces and use pot->data() as temporary field
    mgr->execute_c2r(c_synthesis_plan, tmp_grav.data(), pot.data());

    compute_lep_force<0, false, 1>(g_lep0->get_array(), pot);
    compute_lep_force<1, false, 1>(g_lep1->get_array(), pot);
    compute_lep_force<2, false, 1>(g_lep2->get_array(), pot);

#pragma omp parallel for
    for (long l = c_startN0; l < c_startN0 + c_localN0; l++)
      for (long m = 0; m < c_N1; m++)
        for (long n = 0; n < c_N2; n++) {
          size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);
          vel[0][idx][axis] = (*c_tmp_real_field)[l][m][n];
        }
  }

  double vScaling = -Df1 * Hubble * f1 * anh * anh / unit_v0;

#pragma omp parallel for
  for (long l = c_startN0; l < c_startN0 + c_localN0; l++)
    for (long m = 0; m < c_N1; m++)
      for (long n = 0; n < c_N2; n++) {
        /// sort particles on equidistant grid
        double q0 = L0 / double(c_N0) * double(l);
        double q1 = L1 / double(c_N1) * double(m);
        double q2 = L2 / double(c_N2) * double(n);

        size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);
        double x = q0 - D1 * vel[0][idx][0];
        double y = q1 - D1 * vel[0][idx][1];
        double z = q2 - D1 * vel[0][idx][2];

        ///enforce periodic boundary conditions
        pos[0][idx][0] = periodic_fix(x, 0., L0);
        pos[0][idx][1] = periodic_fix(y, 0., L1);
        pos[0][idx][2] = periodic_fix(z, 0., L2);

        ///store velocities in km/sec
        ///note we multiply by a² to get the correct momentum variable for the lep code
        ///and normalize to code units
        vel[0][idx][0] *= vScaling;
        vel[0][idx][1] *= vScaling;
        vel[0][idx][2] *= vScaling;
      }
}

template <typename CIC>
template <typename PositionArray, typename RedshiftPosition>
void BorgLEPModel<CIC>::lep_redshift_pos(
    const PositionArray &pos, const PositionArray &vel,
    RedshiftPosition &s_pos) {
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
  for (long l = c_startN0; l < c_startN0 + c_localN0; l++)
    for (long m = 0; m < c_N1; m++)
      for (long n = 0; n < c_N2; n++) {
        size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);
        double x0g = pos[idx][0];
        double x1g = pos[idx][1];
        double x2g = pos[idx][2];

        double x0 = x0g + xmin0;
        double x1 = x1g + xmin1;
        double x2 = x2g + xmin2;

        double v0 = vel[idx][0] + observer[0];
        double v1 = vel[idx][1] + observer[1];
        double v2 = vel[idx][2] + observer[2];

        double r2_los = x0 * x0 + x1 * x1 + x2 * x2;
        double v_los = v0 * x0 + v1 * x1 + v2 * x2;

        double A = facRSD * v_los / r2_los;

        double s0 = x0g + A * x0;
        double s1 = x1g + A * x1;
        double s2 = x2g + A * x2;

        ///enforce periodic boundary conditions
        s_pos[idx][0] = periodic_fix(s0, 0., L0);
        s_pos[idx][1] = periodic_fix(s1, 0., L1);
        s_pos[idx][2] = periodic_fix(s2, 0., L2);
      }
}

template <typename CIC>
template <typename PositionArray>
void BorgLEPModel<CIC>::lep_gravpot(
    const PositionArray &pos, FFTW_Real_Array_ref &pot) {
  ConsoleContext<LOG_DEBUG> ctx("gravitational solver");
  double nmean = CosmoTool::cube(double(ss_factor) / f_factor);

  array::fill(pot, 0);
  CIC::projection(pos, pot, L0, L1, L2, f_N0, f_N1, f_N2);
  array::density_rescale(pot, nmean);

  //transform density to F-space
  CArray &f_AUX0 = *f_AUX0_p;
  force_mgr->execute_r2c(f_analysis_plan, pot.data(), f_AUX0.data());
  double normphi = 3. / 2. * cosmo_params.omega_m / double(f_N0 * f_N1 * f_N2) *
                   (unit_r0 * unit_r0);

#pragma omp parallel for
  for (long i = f_startN0; i < f_startN0 + f_localN0; i++) {
    double sin20 = sin2K[0][i];
    for (long j = 0; j < f_N1; j++) {
      double sin21 = sin2K[1][j];
      for (long k = 0; k < f_N2_HC; k++) {
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

  force_mgr->execute_c2r(f_synthesis_plan, f_AUX0.data(), pot.data());
}

template <typename CIC>
template <int axis, bool accum, int sign>
void BorgLEPModel<CIC>::compute_lep_force(
    FFTW_Real_Array_ref &g, FFTW_Real_Array_ref &pot) {
  long N[3] = {N0, N1, N2};
  double i_d[3] = {sign * N0 / (unit_r0 * L0), sign * N1 / (unit_r0 * L1),
                   sign * N2 / (unit_r0 * L2)};
  typedef FFTW_Real_Array::index index_type;

#pragma omp parallel for
  for (long i = startN0; i < startN0 + localN0; i++)
    for (long j = 0; j < N1; j++)
      for (long k = 0; k < N2; k++) {
        boost::array<index_type, 3> idxp = {i, j, k};
        boost::array<index_type, 3> idxm = {i, j, k};

        idxp[axis]++;
        idxm[axis]--;
        if (idxp[axis] > N[axis] - 1)
          idxp[axis] -= N[axis];
        if (idxm[axis] < 0)
          idxm[axis] += N[axis];

        double value = -0.5 * (pot(idxp) - pot(idxm)) * i_d[axis];
        push_to<accum>::apply(g[i][j][k], value);
      }
}

template <typename CIC>
template <int axis, bool accum, int sign>
void BorgLEPModel<CIC>::compute_force(
    FFTW_Real_Array_ref &g, FFTW_Real_Array_ref &pot) {
  long N[3] = {f_N0, f_N1, f_N2};
  double i_d[3] = {sign * f_N0 / (unit_r0 * L0), sign * f_N1 / (unit_r0 * L1),
                   sign * f_N2 / (unit_r0 * L2)};
  typedef FFTW_Real_Array::index index_type;

#pragma omp parallel for
  for (long i = f_startN0; i < f_startN0 + f_localN0; i++)
    for (long j = 0; j < f_N1; j++)
      for (long k = 0; k < f_N2; k++) {
        boost::array<index_type, 3> idxp = {i, j, k};
        boost::array<index_type, 3> idxm = {i, j, k};

        idxp[axis]++;
        idxm[axis]--;
        if (idxp[axis] > N[axis] - 1)
          idxp[axis] -= N[axis];
        if (idxm[axis] < 0)
          idxm[axis] += N[axis];

        double value = -0.5 * (pot(idxp) - pot(idxm)) * i_d[axis];
        push_to<accum>::apply(g[i][j][k], value);
      }
}

template <typename CIC>
void BorgLEPModel<CIC>::lep_vel_update(
    TapeArrayRef &pos, TapeArrayRef &vel, double dtv, double dDv, int istep) {
  ConsoleContext<LOG_DEBUG> ctx("vel update");

  double i_d0 = f_N0 / L0;
  double i_d1 = f_N1 / L1;
  double i_d2 = f_N2 / L2;

  long Np = pos.shape()[1];

  //calculate forces and update velocities
  for (int axis = 0; axis < 3; axis++) {
    ///interpolate lep forces to particles

#pragma omp parallel for schedule(static)
    for (long i = 0; i < Np; i++) {

      double x = pos[istep][i][0] * i_d0;
      double y = pos[istep][i][1] * i_d1;
      double z = pos[istep][i][2] * i_d2;

      int ix = (int)std::floor(x);
      int iy = (int)std::floor(y);
      int iz = (int)std::floor(z);

      int jx = (ix + 1) % f_N0;
      int jy = (iy + 1) % f_N1;
      int jz = (iz + 1) % f_N2;

      double rx = (x - ix);
      double ry = (y - iy);
      double rz = (z - iz);

      double qx = 1 - rx;
      double qy = 1 - ry;
      double qz = 1 - rz;

      double force = 0.;
      switch (axis) {
      case 0:
        force = g_lep0->get_array()[ix][iy][iz] * qx * qy * qz +
                g_lep0->get_array()[ix][iy][jz] * qx * qy * rz +
                g_lep0->get_array()[ix][jy][iz] * qx * ry * qz +
                g_lep0->get_array()[ix][jy][jz] * qx * ry * rz +
                g_lep0->get_array()[jx][iy][iz] * rx * qy * qz +
                g_lep0->get_array()[jx][iy][jz] * rx * qy * rz +
                g_lep0->get_array()[jx][jy][iz] * rx * ry * qz +
                g_lep0->get_array()[jx][jy][jz] * rx * ry * rz;
        break;
      case 1:
        force = g_lep1->get_array()[ix][iy][iz] * qx * qy * qz +
                g_lep1->get_array()[ix][iy][jz] * qx * qy * rz +
                g_lep1->get_array()[ix][jy][iz] * qx * ry * qz +
                g_lep1->get_array()[ix][jy][jz] * qx * ry * rz +
                g_lep1->get_array()[jx][iy][iz] * rx * qy * qz +
                g_lep1->get_array()[jx][iy][jz] * rx * qy * rz +
                g_lep1->get_array()[jx][jy][iz] * rx * ry * qz +
                g_lep1->get_array()[jx][jy][jz] * rx * ry * rz;
        break;
      case 2:
        force = g_lep2->get_array()[ix][iy][iz] * qx * qy * qz +
                g_lep2->get_array()[ix][iy][jz] * qx * qy * rz +
                g_lep2->get_array()[ix][jy][iz] * qx * ry * qz +
                g_lep2->get_array()[ix][jy][jz] * qx * ry * rz +
                g_lep2->get_array()[jx][iy][iz] * rx * qy * qz +
                g_lep2->get_array()[jx][iy][jz] * rx * qy * rz +
                g_lep2->get_array()[jx][jy][iz] * rx * ry * qz +
                g_lep2->get_array()[jx][jy][jz] * rx * ry * rz;
        break;
      }
      force *=
          dDv; //multiply with linear growth factor for lep potential evolution
      vel[istep + 1][i][axis] = vel[istep][i][axis] + force * dtv;
    }
  }
}

template <typename CIC>
void BorgLEPModel<CIC>::lep_pos_update(
    TapeArrayRef &pos, TapeArrayRef &vel, double dtr, double dDr, int istep) {
  ConsoleContext<LOG_DEBUG> ctx("pos update");
  long Np = pos.shape()[1];

#pragma omp parallel for
  for (long i = 0; i < Np; i++) {
    //NOTE: we stored the initial displacement vector in the initial velocity component
    double x = pos[istep][i][0] + vel[istep + 1][i][0] * dtr;
    double y = pos[istep][i][1] + vel[istep + 1][i][1] * dtr;
    double z = pos[istep][i][2] + vel[istep + 1][i][2] * dtr;

    pos[istep + 1][i][0] = periodic_fix(x, 0., L0);
    pos[istep + 1][i][1] = periodic_fix(y, 0., L1);
    pos[istep + 1][i][2] = periodic_fix(z, 0., L2);
  }
}

template <typename CIC>
void BorgLEPModel<CIC>::lep_stepping(
    TapeArrayRef &pos, TapeArrayRef &vel, int nstep, TimingArray &timing) {
  ConsoleContext<LOG_DEBUG> ctx("BORG-lep stepping");

  ctx.print(format("Doing  %d timesteps of lep") % (nstep - 1));

  ///________________________________________________________
  /// lep code forward model
  ///________________________________________________________

  for (int nn = 0; nn < nstep - 1; nn++) {
    double dtr = timing[2][nn];
    double dtv = timing[3][nn];
    double dDr = timing[4][nn];
    double dDv = timing[5][nn];

    lep_vel_update(pos, vel, dtv, dDv, nn);
    lep_pos_update(pos, vel, dtr, dDr, nn);
  }
}

template <typename CIC>
void BorgLEPModel<CIC>::lep_gen_timesteps(
    double ai, double af, TimingArray &timing, int nstep) {
  ConsoleContext<LOG_DEBUG> ctx("BORG-lep gen_timesteps");
  Cosmology cosmo(cosmo_params);

  ctx.print(
      format("Building timesteps from ai=%g to af=%d in %d steps") % ai % af %
      nstep);

  double du = (log(af) - log(ai)) / double(nstep - 1);

  //need to scale lep potential according to pm initial conds.
  double D00 = cosmo.d_plus(ai);

  for (int i = 0; i < nstep; i++) {
    double an0 = ai * exp(du * i);
    double an1 = ai * exp(du * (i + 1));

    double anh0 = (an0 + ai * exp(du * (i - 1))) / 2.;
    double anh1 = (an0 + an1) / 2.;

    double dtr = cosmo.dtr(an0, an1);
    double dtv = cosmo.dtv(anh0, anh1);

    double D0 = cosmo.d_plus(ai);
    double dDr = (cosmo.d_plus(an1) - cosmo.d_plus(an0)) / D0;
    //double dDv=cosmo.d_plus(an0)/D00;
    //need to do a propper integral here
    //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    double dDv = 0.5 * (cosmo.d_plus(an1) + cosmo.d_plus(an0)) / D00;
    //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    timing[0][i] = an0;
    timing[1][i] = anh0;
    timing[2][i] = dtr;
    timing[3][i] = dtv;
    timing[4][i] = dDr;
    timing[5][i] = dDv;
  }
}

template <typename CIC>
template <typename PositionArray>
void BorgLEPModel<CIC>::lep_density_obs(
    const PositionArray &pos, ArrayRef &deltao) {
  double nmean = CosmoTool::cube(ss_factor);

  array::fill(deltao, 0);
  CIC::projection(pos, deltao, L0, L1, L2, N0, N1, N2);
  array::density_rescale(deltao, nmean);
}

template <typename CIC>
void BorgLEPModel<CIC>::forwardModelRsdField(
    ArrayRef &deltaf, double *vobs_ext) {

  std::cout << "ERROR: VOBS META_SAMPLER NOT IMPLEMENTED" << std::endl;
  exit(0);
  /*
    ConsoleContext<LOG_DEBUG> ctx("BORG forward model rsd density calculation");

    ///introduce redshift distortions
    if (do_rsd) {
        UninitializedArray<PhaseArray> s_pos_p(extents[c_localN0*c_N1*c_N2][3]);
        
        //ArrayType1d::ArrayType& dummy = vobs;
        
        //set vobs to input
        double dummy[3];
        
        dummy[0]=vobs[0];
        dummy[1]=vobs[1];
        dummy[2]=vobs[2];
        
        vobs[0]=vobs_ext[0];
        vobs[1]=vobs_ext[1];
        vobs[2]=vobs_ext[2];
        
        ctx.print("doing redshift space distortions.");
        lpt_redshift_pos(u_pos->get_array(), u_vel->get_array(), s_pos_p.get_array());
        
        lpt_density_obs(s_pos_p.get_array(), deltaf);
        
        //reset vobs
        vobs[0]=dummy[0];
        vobs[1]=dummy[1];
        vobs[2]=dummy[2];
        ;
        
    }
 */
}

template <typename CIC>
void BorgLEPModel<CIC>::lep_fwd_model(
    CArrayRef &deltao, ArrayRef &deltaf, TapeArrayRef &pos, TapeArrayRef &vel,
    TimingArray &timing) {
  ConsoleContext<LOG_DEBUG> ctx("BORG-LEP forward model");
  ///NOTE: ICs are generated at ai
  ///but the lepcode starts at ao and finishes at af
  double ao = 1. / (1. + z_start);
  double af = 1.;

  /// we also choose some time steps
  int nstep = timing.shape()[1];

  //generate time steps
  lep_gen_timesteps(ao, af, timing, nstep);

  //generate initial conditions at ao
  if (c_deltao != 0) {
    array::fill(*c_deltao, 0);
    mgr->upgrade_complex(*lo_mgr, deltao, *c_deltao);
    lep_ic(*c_deltao, pos, vel, timing);
  } else
    lep_ic(deltao, pos, vel, timing);

  //do the lep stepping
  lep_stepping(pos, vel, nstep, timing);

  //build density field
  if (do_redshift) {
    UninitializedArray<PhaseArray> s_pos_p(extents[c_localN0 * c_N1 * c_N2][3]);
    ctx.print("doing redshift space distortions.");
    lep_redshift_pos(pos[nstep - 1], vel[nstep - 1], s_pos_p.get_array());
    lep_density_obs(s_pos_p.get_array(), deltaf);
  } else {
    lep_density_obs(pos[nstep - 1], deltaf);
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
