/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/deprecated/pm/borg_fwd_pm_adj.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

template <typename FIC, typename CIC>
void BorgPMModel<FIC, CIC>::pm_ic_ag(
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

  array::fill(AUX1, 0);

  for (int axis = 0; axis < 3; axis++) {
    ///1. Do position/velocity derivative
    ///------------------------------------------------------------------------------

    double fac_vel = -Df1 * f1 * anh * anh * Hubble / unit_v0;
#pragma omp parallel for collapse(3)
    for (long l = c_startN0; l < c_startN0 + c_localN0; l++)
      for (long m = 0; m < c_N1; m++)
        for (long n = 0; n < c_N2; n++) {
          // pos_ag and vel_ag are ordered exactly as the initial conditions,
          // so this code works
          size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);
          aux[l][m][n] = -D1 * pos_ag[idx][axis] + fac_vel * vel_ag[idx][axis];
        }

    /// FFT to F-space
    mgr->execute_r2c(c_analysis_plan, aux.data(), AUX0.data());

#pragma omp parallel for collapse(3)
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
template <typename FIC, typename CIC>
template <typename PositionArray, typename PosAgArray>
void BorgPMModel<FIC, CIC>::pm_redshift_pos_ag(
    const PositionArray &pos, const PositionArray &vel, PosAgArray &pos_ag,
    PosAgArray &vel_ag, size_t partNum) {
  Cosmology cosmo(cosmo_params);

  //this routine generates particle positions in redshift space
  double anh = af;
  double Hubble = cosmo.Hubble(anh) / cosmo_params.h; ///km /sec /(Mpc/h)

  // the code uses particle momenta p=a^2 dx/dt where x is the co-moving position
  // peculiar velocities are then given by v_pec = p/a

  //NOTE: Check coefficients
  double facRSD =
      unit_v0 / af /
      Hubble; //this factor is 1/H/a for velocities in [km/sec] an additional factor arises from momentum conversion
  double facObs = af / Hubble / (facRSD);
  boost::array<double, 3> observer = {vobs[0] * facObs, vobs[1] * facObs,
                                      vobs[2] * facObs};

#pragma omp parallel for
  for (size_t idx = 0; idx < partNum; idx++) {
    typename PositionArray::const_reference cur_pos = pos[idx];
    typename PositionArray::const_reference cur_vel = vel[idx];
    typename PosAgArray::reference cur_pos_ag = pos_ag[idx];
    typename PosAgArray::reference cur_vel_ag = vel_ag[idx];

    double x0 = cur_pos[0] + xmin0;
    double x1 = cur_pos[1] + xmin1;
    double x2 = cur_pos[2] + xmin2;

    double v0 = cur_vel[0] + observer[0];
    double v1 = cur_vel[1] + observer[1];
    double v2 = cur_vel[2] + observer[2];

    double s_pos_ag0 = cur_pos_ag[0];
    double s_pos_ag1 = cur_pos_ag[1];
    double s_pos_ag2 = cur_pos_ag[2];

    double r2_los = x0 * x0 + x1 * x1 + x2 * x2;
    double v_los = v0 * x0 + v1 * x1 + v2 * x2;
    double slos = s_pos_ag0 * x0 + s_pos_ag1 * x1 + s_pos_ag2 * x2;

    double A = facRSD * slos / r2_los;
    double B = -2 * facRSD * v_los * slos / square(r2_los);
    double C = facRSD * v_los / r2_los;

    cur_pos_ag[0] = s_pos_ag0 + C * s_pos_ag0 + B * x0 + A * v0;
    cur_pos_ag[1] = s_pos_ag1 + C * s_pos_ag1 + B * x1 + A * v1;
    cur_pos_ag[2] = s_pos_ag2 + C * s_pos_ag2 + B * x2 + A * v2;

    cur_vel_ag[0] = A * x0;
    cur_vel_ag[1] = A * x1;
    cur_vel_ag[2] = A * x2;
  }
}
///===============================
template <typename FIC, typename CIC>
template <typename PositionArray, typename OutputArray>
void BorgPMModel<FIC, CIC>::pm_density_obs_ag(
    const PositionArray &pos, OutputArray &pos_ag, OutputArray &vel_ag,
    ArrayRef &B, size_t partNum) {
  double nmean = CosmoTool::cube(ss_factor);
  typedef UninitializedArray<boost::multi_array<double, 3>> U_Array;

  if (ALWAYS_MPI(comm)) {
    // Allocate a temporary density field with extra planes for the
    // the projection leakage
    U_Array tmp_delta(lo_mgr->extents_real(CIC::MPI_PLANE_LEAKAGE));

    pm_exchange_planes_ag(tmp_delta.get_array(), B, lo_mgr);
    array::fill(pos_ag, 0);
    FIC::adjoint(
        pos, tmp_delta.get_array(), pos_ag, L0, L1, L2, N0, N1, N2,
        typename FIC::Periodic_MPI(N0, N1, N2, comm), nmean, partNum);
  } else {
    // This is simple, no copy, no adjustment
    array::fill(pos_ag, 0);
    FIC::adjoint(
        pos, B, pos_ag, L0, L1, L2, N0, N1, N2, CIC_Tools::Periodic(N0, N1, N2),
        nmean, partNum);
  }

  // Always zero here, not with RSD though
  array::fill(vel_ag, 0);
}

template <int axis, typename GravityArray>
double __gravity_interpolation_ag(
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

// This is the computation of 1st term in the paper. It corresponds
// the gradient of the interpolation kernel at the particle position
template <typename FIC, typename CIC>
template <typename PositionArray>
void BorgPMModel<FIC, CIC>::pm_force_1_ag(
    const PositionArray &pos, const PositionArray &vel, PhaseArrayRef &pos_ag,
    PhaseArrayRef &vel_ag, PhaseArrayRef &F_ag, double dtr, double dtv,
    size_t agNum) {
  // We need one additional plane to compute the interpolated gravity
  Uninit_FFTW_Real_Array g_p(
      force_mgr->extents_real(1), force_mgr->allocator_real);
  Uninit_FFTW_Real_Array pot_p(
      force_mgr->extents_real(CIC::MPI_PLANE_LEAKAGE),
      force_mgr->allocator_real);
  typedef Uninit_FFTW_Real_Array::array_type GArray;
  GArray &pot = pot_p.get_array();
  GArray &g = g_p.get_array();

  ConsoleContext<LOG_DEBUG> ctx("Build gravitational potential");
  //estimate gravitational potential
  //alternatively we can store the potential from the forward run
  //for the expense of higher memory requirements
  pm_grav_density(true, pos, agNum, pot);
  pm_gravpot(pot);

  double i_d0 = f_N0 / L0;
  double i_d1 = f_N1 / L1;
  double i_d2 = f_N2 / L2;

  // This is a hack to avoid branching all the time.
  long f_mpi_N0 = (ALWAYS_MPI(comm)) ? (f_N0 + 2) : f_N0;

  //calculate forces and update velocities
  for (int axis = 0; axis < 3; axis++) {
    ConsoleContext<LOG_DEBUG> ctx_force("axis handling");
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

    if (ALWAYS_MPI(comm)) {
      // We need to exchange a plane (thus enforcing "1")
      auto g0 = g[f_startN0 + f_localN0];
      auto g1 = g[f_startN0];
      int plane0 = (f_startN0 + f_localN0) % f_N0;
      int plane1 = (f_startN0 + f_N0 - 1) % f_N0;
      MPI_Communication::Request req_recv, req_send;
      req_recv = comm->IrecvT(
          &g0[0][0], g0.num_elements(), force_mgr->get_peer(plane0), plane0);
      req_send = comm->IsendT(
          &g1[0][0], g1.num_elements(), force_mgr->get_peer(plane1), f_startN0);
      req_recv.wait();
      req_send.wait();
      //pm_exchange_planes<false>(g, force_mgr, 1);
      // Now all planes are available to compute derivatives
    }

    ctx_force.print(format("accumulate on F_ag, axis=%d") % axis);
#pragma omp parallel for schedule(static)
    for (long i = 0; i < agNum; i++) {
      double x = pos[i][0] * i_d0;
      double y = pos[i][1] * i_d1;
      double z = pos[i][2] * i_d2;

      int ix = (int)std::floor(x);
      int iy = (int)std::floor(y);
      int iz = (int)std::floor(z);

      int jx = (ix + 1) % f_mpi_N0;
      int jy = (iy + 1) % f_N1;
      int jz = (iz + 1) % f_N2;

      double ax, ay, az;
      //derivative of cic kernel with respect to x

      ax = __gravity_interpolation_ag<0, GArray>(
               g, x, y, z, ix, iy, iz, jx, jy, jz) *
           i_d0;

      //derivative of cic kernel with respect to y
      ay = __gravity_interpolation_ag<1, GArray>(
               g, x, y, z, ix, iy, iz, jx, jy, jz) *
           i_d1;

      //derivative of cic kernel with respect to z
      az = __gravity_interpolation_ag<2, GArray>(
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

  Console::instance().print<LOG_DEBUG>("Done force_1_ag");
}

// Computation of the second term in the PM paper. That's the computation
// of the gradient of the gridded force with respect to displacements of the
// previous timesteps.
template <typename FIC, typename CIC>
template <typename PositionArray>
void BorgPMModel<FIC, CIC>::pm_force_0_ag(
    const PositionArray &pos, const PositionArray &vel, PhaseArrayRef &pos_ag,
    PhaseArrayRef &vel_ag, PhaseArrayRef &F_ag, double dtr, double dtv,
    size_t adjNum) {
  double d0 = L0 / double(N0);
  double d1 = L1 / double(N1);
  double d2 = L2 / double(N2);
  typedef boost::multi_array<double, 1> WeightArray;
  typedef UninitializedArray<WeightArray> U_WeightArray;

  FFTW_Complex_Array &f_AUX0 = *f_AUX0_p;
  Uninit_FFTW_Real_Array B_p(
      force_mgr->extents_real(), force_mgr->allocator_real);
  Uninit_FFTW_Real_Array g_p(
      force_mgr->extents_real(CIC::MPI_PLANE_LEAKAGE),
      force_mgr->allocator_real);
  Uninit_FFTW_Real_Array::array_type &g = g_p.get_array();
  Uninit_FFTW_Real_Array::array_type &B = B_p.get_array();
  U_WeightArray u_weight(boost::extents[adjNum]);
  U_WeightArray::array_type &weight = u_weight.get_array();

  array::fill(B, 0);

  for (int axis = 0; axis < 3; axis++) {
#pragma omp parallel for
    for (long i = 0; i < adjNum; i++) {
      weight[i] = pos_ag[i][axis] * dtr * dtv + vel_ag[i][axis] * dtv;
    }

    //do cic
    array::fill(g, 0);
    if (ALWAYS_MPI(comm)) {
      Console::instance().print<LOG_DEBUG>(
          "Projecting positions to recompute force (Comm > 1)");
      CIC::projection(
          pos, g, L0, L1, L2, f_N0, f_N1, f_N2,
          typename CIC::Periodic_MPI(f_N0, f_N1, f_N2, comm), weight, adjNum);
      Console::instance().print<LOG_DEBUG>("Done. Now exchanging");
      pm_exchange_planes<true>(g, force_mgr);
    } else {
      CIC::projection(
          pos, g, L0, L1, L2, f_N0, f_N1, f_N2,
          CIC_Tools::Periodic(f_N0, f_N1, f_N2), weight, adjNum);
    }

    switch (axis) {
    case 0:
      BorgPMModel<FIC, CIC>::compute_force<0, true, -1>(B, g);
      break;
    case 1:
      BorgPMModel<FIC, CIC>::compute_force<1, true, -1>(B, g);
      break;
    case 2:
      BorgPMModel<FIC, CIC>::compute_force<2, true, -1>(B, g);
      break;
    }
    Console::instance().print<LOG_DEBUG>("Accrued forces");
  }

  Console::instance().print<LOG_DEBUG>("Fourier transforming");
  //transform density to F-space
  force_mgr->execute_r2c(f_analysis_plan, B.data(), f_AUX0.data());

  double normphi = 3. / 2. * cosmo_params.omega_m / double(f_N0 * f_N1 * f_N2) /
                   (unit_r0 * unit_r0);

#ifdef ARES_MPI_FFTW
#  pragma omp parallel for
  for (int i = f_startN1; i < f_startN1 + f_localN1; i++) {
    double sin21 = sin2K[1][i];
    for (int j = 0; j < f_N0; j++) {
      double sin20 = sin2K[0][j];
      for (int k = 0; k < f_N2_HC; k++) {
        double sin22 = sin2K[2][k];

        double Greens = -normphi / (sin20 + sin21 + sin22);
        f_AUX0[i][j][k] *= Greens;
      }
    }
  }
  //fix zero mode by hand
  if (f_startN1 == 0 && f_localN1 > 0) {
    f_AUX0[0][0][0] = 0;
  }
#else
#  pragma omp parallel for
  for (int i = f_startN0; i < f_startN0 + f_localN0; i++) {
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
#endif

  force_mgr->execute_c2r(f_synthesis_plan, f_AUX0.data(), B.data());

  double nmean = CosmoTool::cube(double(ss_factor) / f_factor);

  Console::instance().print<LOG_DEBUG>(
      "Now exchange_plane_ag and final CIC adjoint for force_0");

  if (ALWAYS_MPI(comm)) {
    Uninit_FFTW_Real_Array tmp_B(
        force_mgr->extents_real(CIC::MPI_PLANE_LEAKAGE));

    pm_exchange_planes_ag(tmp_B.get_array(), B, force_mgr);
    array::fill(F_ag, 0);
    CIC::adjoint(
        pos, tmp_B.get_array(), F_ag, L0, L1, L2, f_N0, f_N1, f_N2,
        typename CIC::Periodic_MPI(f_N0, f_N1, f_N2, comm), nmean, adjNum);
  } else {
    array::fill(F_ag, 0);
    CIC::adjoint(
        pos, B, F_ag, L0, L1, L2, f_N0, f_N1, f_N2,
        CIC_Tools::Periodic(f_N0, f_N1, f_N2), nmean, adjNum);
  }
}

template <typename FIC, typename CIC>
template <typename ForceArray>
void BorgPMModel<FIC, CIC>::pm_pos_update_ag(
    PhaseArrayRef &pos_ag, const ForceArray &F_ag, double dtr, size_t agNum) {
#pragma omp parallel for
  for (long i = 0; i < agNum; i++) {
    for (int j = 0; j < 3; j++)
      pos_ag[i][j] += F_ag[i][j];
  }
}

template <typename FIC, typename CIC>
void BorgPMModel<FIC, CIC>::pm_vel_update_ag(
    PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, double dtr, size_t agNum) {
#pragma omp parallel for
  for (long i = 0; i < agNum; i++) {
    for (int j = 0; j < 3; j++)
      vel_ag[i][j] += pos_ag[i][j] * dtr;
  }
}

template <typename FIC, typename CIC>
void BorgPMModel<FIC, CIC>::pm_stepping_ag(
    int nstep, TimingArray &timing, TapeArrayRef &pos, TapeArrayRef &vel,
    PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, IdxTapeArrayRef &part_idx) {
  //define adjoint force array
  using boost::lambda::_1;
  using boost::lambda::_2;
  size_t partNumber = pos.shape()[1];
  U_PhaseArray F_ag_0_p(extents[partNumber][3]);
  U_PhaseArray::array_type &F_ag_0 = F_ag_0_p.get_array();
  U_PhaseArray F_ag_1_p(extents[partNumber][3]);
  U_PhaseArray::array_type &F_ag_1 = F_ag_1_p.get_array();
  ConsoleContext<LOG_DEBUG> ctx("stepping ag");

  // MAIN LOOP : undo Leapfrog stepping
  for (int nn = nstep - 2; nn >= 0; nn--) {
    double dtr = timing[2][nn];
    double dtv = timing[3][nn];
    size_t agNum;

    ctx.print(format("handling step = %d") % nn);
    // Now redistribute
    if (FORCE_REDISTRIBUTE || ALWAYS_MPI(comm))
      pm_distribute_particles_ag<true>(
          nn + 1, pos_ag, vel_ag, pos, vel, part_idx);

    agNum = local_usedParticles[nn];
    ctx.print(
        format("Done undoing distribution, agNum = %d, now force ag") % agNum);

    //order of force term is important as they will be added up!!!!
    //    #pragma omp task shared(pos, vel, pos_ag, vel_ag, F_ag_0)
    {
      pm_force_0_ag(pos[nn], vel[nn], pos_ag, vel_ag, F_ag_0, dtr, dtv, agNum);
    }
    //    #pragma omp task shared(pos, vel, pos_ag, vel_ag, F_ag_1)
    {
      pm_force_1_ag(pos[nn], vel[nn], pos_ag, vel_ag, F_ag_1, dtr, dtv, agNum);
    }
    //    #pragma omp taskwait
    ctx.print("Done force ag, now vel update");
    pm_vel_update_ag(pos_ag, vel_ag, dtr, agNum);
    ctx.print("Done vel update, now pos update");
    pm_pos_update_ag(
        pos_ag,
        b_fused<U_PhaseArray::array_type::element>(F_ag_0, F_ag_1, _1 + _2),
        dtr, agNum);
    ctx.print("Done pos update, finished ag stepping");
  }
}

template <typename FIC, typename CIC>
void BorgPMModel<FIC, CIC>::pm_fwd_model_ag(
    PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, IdxTapeArrayRef &part_idx,
    ArrayRef &DPSI, TimingArray &timing) {
  ConsoleContext<LOG_DEBUG> ctx("BORG-PM adjoint model");
  int nstep = pm_nsteps;
  TapeArrayRef &pos = u_pos->get_array();
  TapeArrayRef &vel = u_vel->get_array();

  ///NOTE: ICs are generated at ai

  ///introduce adjoint quantities
  typedef U_PhaseArray::array_type PhaseArrayRef;

  //2.) undo pm-stepping
  pm_stepping_ag(nstep, timing, pos, vel, pos_ag, vel_ag, u_idx->get_array());

  // Now final redistribute
  if (FORCE_REDISTRIBUTE || ALWAYS_MPI(comm)) {
    pm_distribute_particles_ag<true>(0, pos_ag, vel_ag, pos, vel, part_idx);
  }
  // Now we are back in IC configuration (including pos_ag, vel_ag ordering)

  //N.) undo ICs
  pm_ic_ag(pos_ag, vel_ag, timing);

  // Apply gradient upgrade operator
  if (c_deltao != 0) {
    ctx.print("Gradient of upgrade and FFT...");
    array::fill(tmp_complex_field->get_array(), 0);
    lo_mgr->degrade_complex(*mgr, *AUX1_p, tmp_complex_field->get_array());
    lo_mgr->execute_c2r(synthesis_plan, tmp_complex_field->get_array().data(), DPSI.data());
  } else {
    ctx.print("Finishing up with an FFT");
    lo_mgr->execute_c2r(synthesis_plan, AUX1_p->data(), DPSI.data());
  }
}
