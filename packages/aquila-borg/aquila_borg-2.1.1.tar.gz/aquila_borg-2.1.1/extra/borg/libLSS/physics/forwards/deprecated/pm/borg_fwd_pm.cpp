/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/deprecated/pm/borg_fwd_pm.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

template <typename FIC, typename CIC>
void BorgPMModel<FIC, CIC>::pm_ic(
    CArrayRef &deltao, TapeArrayRef &pos, TapeArrayRef &vel,
    IdxTapeArrayRef &part_idx, TimingArray &timing) {
  ///set cosmological parameters
  ///Initial density is scaled to initial redshift!!!
  ConsoleContext<LOG_DEBUG> ctx("PM init ic");
  Cosmology cosmo(cosmo_params);
  TapeArrayRef::index_gen i_gen;
  typedef TapeArrayRef::index_range i_range;

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

  ctx.print(
      format("D0=%g, D1=%g, Df1=%g, f1=%g, Hubble=%g") % D0 % D1 % Df1 % f1 %
      Hubble);

  typedef UninitializedArray<
      FFTW_Complex_Array, FFTW_Allocator<std::complex<double>>>
      U_CArray;
  typedef U_CArray::array_type Ref_CArray;

  U_CArray tmp_p(mgr->extents_complex(), mgr->allocator_complex);
  Ref_CArray &tmp = tmp_p.get_array();

  for (int axis = 0; axis < 3; axis++) {
    ctx.print(format("Initialize displacement, axis=%d") % axis);

#pragma omp parallel for collapse(3)
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

          tmp[i][j][k] = std::complex<double>(
              -fac * in_delta.imag(), fac * in_delta.real());
        }

    if (c_startN0 == 0 && c_localN0 > 0) {
      tmp[0][0][0] = 0;
      tmp[0][0][c_N2 / 2] = 0;
      tmp[0][c_N1 / 2][0] = 0;
      tmp[0][c_N1 / 2][c_N2 / 2] = 0;
    }

    if (c_startN0 <= c_N0 / 2 && c_startN0 + c_localN0 > c_N0 / 2) {
      tmp[c_N0 / 2][0][0] = 0;
      tmp[c_N0 / 2][0][c_N2 / 2] = 0;
      tmp[c_N0 / 2][c_N1 / 2][0] = 0;
      tmp[c_N0 / 2][c_N1 / 2][c_N2 / 2] = 0;
    }

    /// FFT to Realspace
    mgr->execute_c2r(c_synthesis_plan, tmp.data(), c_tmp_real_field->data());

#pragma omp parallel for collapse(3)
    for (long l = c_startN0; l < c_startN0 + c_localN0; l++)
      for (long m = 0; m < c_N1; m++)
        for (long n = 0; n < c_N2; n++) {
          size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);
          vel[0][idx][axis] = (*c_tmp_real_field)[l][m][n];
        }
  }

  double vScaling = -Df1 * Hubble * f1 * anh * anh / unit_v0;

  ctx.print("Move particles and rescale velocities");
  auto &ids = *lagrangian_id;
  size_t base_id = c_N2 * c_N1 * c_startN0;

#pragma omp parallel for collapse(3)
  for (long l = c_startN0; l < c_startN0 + c_localN0; l++)
    for (long m = 0; m < c_N1; m++)
      for (long n = 0; n < c_N2; n++) {
        /// sort particles on equidistant grid
        double q0 = L0 / double(c_N0) * double(l);
        double q1 = L1 / double(c_N1) * double(m);
        double q2 = L2 / double(c_N2) * double(n);
        size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);
        TapeArray::reference::reference loc_pos = pos[0][idx];
        TapeArray::reference::reference loc_vel = vel[0][idx];

        double x = q0 - D1 * loc_vel[0];
        double y = q1 - D1 * loc_vel[1];
        double z = q2 - D1 * loc_vel[2];

        ///enforce periodic boundary conditions
        loc_pos[0] = periodic_fix(x, 0., L0);
        loc_pos[1] = periodic_fix(y, 0., L1);
        loc_pos[2] = periodic_fix(z, 0., L2);

        ids[idx] = idx + base_id;

        ///NOTE: displacements are already sttored in the velocity vectors. Only need to multiply by prefactor

        ///store velocities in km/sec
        ///note we multiply by a² to get the correct momentum variable for the particle mesh code
        ///and normalize to code units
        loc_vel[0] *= vScaling;
        loc_vel[1] *= vScaling;
        loc_vel[2] *= vScaling;
      }

  // Start evenly distributed
  local_usedParticles[0] = size_t(c_localN0) * c_N1 * c_N2;
  copy_array_rv(
      part_idx[i_gen[0][i_range(0, local_usedParticles[0])]],
      b_fused_idx<long, 1>(boost::lambda::_1));
}

template <typename FIC, typename CIC>
template <typename PositionArray, typename RedshiftPosition>
void BorgPMModel<FIC, CIC>::pm_redshift_pos(
    const PositionArray &pos, const PositionArray &vel, RedshiftPosition &s_pos,
    size_t numParticles) {
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
  double facObs = af / Hubble / facRSD;

  size_t usedParts = s_pos.shape()[0];
  boost::array<double, 3> observer = {vobs[0] * facObs, vobs[1] * facObs,
                                      vobs[2] * facObs};

#pragma omp parallel for
  for (size_t idx = 0; idx < numParticles; idx++) {
    typename PositionArray::const_reference cur_pos = pos[idx];
    typename PositionArray::const_reference cur_vel = vel[idx];

    double x0g = cur_pos[0];
    double x1g = cur_pos[1];
    double x2g = cur_pos[2];

    double x0 = x0g + xmin0;
    double x1 = x1g + xmin1;
    double x2 = x2g + xmin2;

    double v0 = cur_vel[0] + observer[0];
    double v1 = cur_vel[1] + observer[1];
    double v2 = cur_vel[2] + observer[2];

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

#include "pm_force.hpp"
#include "pm_grav.hpp"
#include "pm_vel_update.hpp"
#include "pm_pos_update.hpp"

template <typename FIC, typename CIC>
void BorgPMModel<FIC, CIC>::pm_stepping(
    int nstep, TimingArray &timing, TapeArrayRef &pos, TapeArrayRef &vel,
    IdxTapeArrayRef &part_idx) {
  ConsoleContext<LOG_DEBUG> ctx("BORG-PM stepping");
  TapeArrayRef::index_gen i_gen;
  typedef TapeArrayRef::index_range i_range;

  ctx.print(format("Doing  %d timesteps of PM") % (nstep - 1));

  ///________________________________________________________
  /// PM code forward model
  ///________________________________________________________

  for (int nn = 0; nn < nstep - 1; nn++) {
    double dtr = timing[2][nn];
    double dtv = timing[3][nn];
    long loc_used = local_usedParticles[nn];

    initIndexes(part_idx[nn + 1], loc_used);
    pm_vel_update(pos, vel, part_idx, dtv, nn);
    pm_pos_update(pos, vel, part_idx, dtr, nn);
    // The last step is special
    if (nn < nstep - 2)
      pm_distribute_particles<true>(
          force_mgr, nn + 1, pos, vel, part_idx, local_usedParticles[nn]);
  }
  pm_distribute_particles<true, FIC>(
      lo_mgr, nstep - 1, pos, vel, part_idx, local_usedParticles[nstep - 2]);
}

template <typename FIC, typename CIC>
void BorgPMModel<FIC, CIC>::pm_gen_timesteps(
    double ai, double af, TimingArray &timing, int nstep) {
  ConsoleContext<LOG_DEBUG> ctx("BORG-PM gen_timesteps");
  Cosmology cosmo(cosmo_params);

  ctx.print(
      format("Building timesteps from ai=%g to af=%d in %d steps") % ai % af %
      nstep);
  double du = (log(af) - log(ai)) / double(nstep - 1);

  for (int i = 0; i < nstep; i++) {
    double an0 = ai * exp(du * i);
    double an1 = ai * exp(du * (i + 1));

    double anh0 = (an0 + ai * exp(du * (i - 1))) / 2.;
    double anh1 = (an0 + an1) / 2.;

    double dtr = cosmo.dtr(an0, an1);
    double dtv = cosmo.dtv(anh0, anh1);

    timing[0][i] = an0;
    timing[1][i] = anh0;
    timing[2][i] = dtr;
    timing[3][i] = dtv;
  }
}

template <typename FIC, typename CIC>
template <typename PositionArray>
void BorgPMModel<FIC, CIC>::pm_density_obs(
    const PositionArray &pos, ArrayRef &deltao) {
  double nmean = CosmoTool::cube(ss_factor);

  if (ALWAYS_MPI(comm)) {
    typedef UninitializedArray<boost::multi_array<double, 3>> U_Array;
    typedef U_Array::array_type::index_range i_range;
    U_Array::array_type::index_gen indices;
    // Here we have to introduce ghost planes.
    U_Array tmp_delta(lo_mgr->extents_real(CIC::MPI_PLANE_LEAKAGE));

    array::fill(tmp_delta.get_array(), 0);
    FIC::projection(
        pos, tmp_delta.get_array(), L0, L1, L2, N0, N1, N2,
        typename FIC::Periodic_MPI(N0, N1, N2, comm),
        CIC_Tools::DefaultWeight(), pos.shape()[0]);
    // pot has MPI_PLANE_LEAKAGE extra planes. They have to be sent to the adequate nodes.
    pm_exchange_planes<true>(tmp_delta.get_array(), lo_mgr);

    copy_array_rv(
        deltao[indices[i_range(startN0, startN0 + localN0)][i_range()]
                      [i_range(0, N2)]],
        tmp_delta.get_array()[indices[i_range(startN0, startN0 + localN0)]
                                     [i_range()][i_range()]]);
  } else {
    array::fill(deltao, 0);
    FIC::projection(
        pos, deltao, L0, L1, L2, N0, N1, N2, CIC_Tools::Periodic(N0, N1, N2),
        CIC_Tools::DefaultWeight(), pos.shape()[0]);
  }

  array::density_rescale(deltao, nmean);
}

template <typename FIC, typename CIC>
void BorgPMModel<FIC, CIC>::forwardModelRsdField(
    ArrayRef &deltaf, double *vobs_ext) {
  TapeArrayRef::index_gen i_gen;
  typedef TapeArrayRef::index_range i_range;

  ConsoleContext<LOG_DEBUG> ctx("BORG forward model rsd density calculation");
  /// we also choose some time steps
  int nstep = pm_nsteps;
  int last_step = nstep - 1;
  TapeArrayRef &pos = u_pos->get_array();
  TapeArrayRef &vel = u_vel->get_array();
  IdxTapeArrayRef &part_idx = u_idx->get_array();

  ///introduce redshift distortions
  if (do_redshift) {
    //ArrayType1d::ArrayType& dummy = vobs;
    int s_step = last_step + 1;
    TapeArrayRef::reference s_pos = pos[s_step];
    size_t loc_used = local_usedParticles[last_step];

    //set vobs to input
    double dummy[3];

    dummy[0] = vobs[0];
    dummy[1] = vobs[1];
    dummy[2] = vobs[2];

    vobs[0] = vobs_ext[0];
    vobs[1] = vobs_ext[1];
    vobs[2] = vobs_ext[2];

    ctx.print("doing redshift space distortions.");
    // Move particles to their redshift position in the s_pos buffer (actually last entry of pos tape array)
    pm_redshift_pos(pos[last_step], vel[last_step], s_pos, loc_used);
    // Reinit indexes to 0, 1, ..., loc_used-1
    initIndexes(part_idx[s_step], loc_used);
    // Domain decomposition.
    pm_distribute_particles<false, FIC>(
        lo_mgr, s_step, pos, vel, part_idx, loc_used);
    // pos[s_step] is now guaranteed to live only in the acceptable domain for deltaf
    pm_density_obs(
        s_pos[i_gen[i_range(0, local_usedParticles[s_step])][i_range()]],
        deltaf);

    //reset vobs, last index has been destroyed. AG will not be correct
    vobs[0] = dummy[0];
    vobs[1] = dummy[1];
    vobs[2] = dummy[2];
  }
}

template <typename FIC, typename CIC>
void BorgPMModel<FIC, CIC>::pm_fwd_model(
    CArrayRef &deltao, TapeArrayRef &pos, TapeArrayRef &vel,
    IdxTapeArrayRef &part_idx, TimingArray &timing) {
  ConsoleContext<LOG_DEBUG> ctx("BORG-PM forward model");
  ///NOTE: ICs are generated at ai
  ///but the pmcode starts at ao and finishes at af
  double ao = 1. / (1. + z_start);

  /// we also choose some time steps
  int nstep = pm_nsteps;
  int last_step = nstep - 1;

  //generate time steps
  pm_gen_timesteps(ao, af, timing, nstep);

  //generate initial conditions at ao
  if (c_deltao != 0) {
    array::fill(*c_deltao, 0);
    mgr->upgrade_complex(*lo_mgr, deltao, *c_deltao);
    pm_ic(*c_deltao, pos, vel, part_idx, timing);
  } else
    pm_ic(deltao, pos, vel, part_idx, timing);

  if ((FORCE_REDISTRIBUTE || ALWAYS_MPI(comm)))
    // Redistribute first
    pm_distribute_particles<true>(
        force_mgr, 0, pos, vel, part_idx, local_usedParticles[0]);

  //do the pm stepping
  pm_stepping(nstep, timing, pos, vel, part_idx);
}
