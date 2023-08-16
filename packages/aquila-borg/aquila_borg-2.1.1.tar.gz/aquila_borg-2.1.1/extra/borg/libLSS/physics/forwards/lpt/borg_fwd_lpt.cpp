/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/lpt/borg_fwd_lpt.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2018 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

#include "../pm/plane_xchg.hpp"

template <typename CIC>
void BorgLptModel<CIC>::lpt_ic(
    CArrayRef &deltao, PhaseArrayRef &pos, PhaseArrayRef &vel,
    PhaseArrayRef &lctim) {
  ///set cosmological parameters
  ///Initial density is scaled to initial redshift!!!
  Cosmology cosmo(cosmo_params);
  ConsoleContext<LOG_DEBUG> ctx("lpt_ic");

  double an = af; ///set position ics at r_{0}, calculate till present epoch
  double anh =
      af; ///velocities are created at v_{0-1/2}, calculate till present epoch
  size_t endN0 = c_startN0 + c_localN0;
  double inv_volume = 1 / (L0 * L1 * L2);
  double Hubble = cosmo.Hubble(anh) / cosmo_params.h; ///km /sec /(Mpc/h)

  typedef UninitializedArray<
      FFTW_Complex_Array, FFTW_Allocator<std::complex<double>>>
      U_CArray;
  typedef U_CArray::array_type Ref_CArray;

  U_CArray tmp_p(mgr->extents_complex(), mgr->allocator_complex);
  Ref_CArray &tmp = tmp_p.get_array();

  size_t Ns[3] = {size_t(c_N0) / 2, size_t(c_N1) / 2, size_t(c_N2) / 2};
  for (int axis = 0; axis < 3; axis++) {
#pragma omp parallel for collapse(3) schedule(static)
    for (size_t i = c_startN0; i < endN0; i++)
      for (size_t j = 0; j < c_N1; j++)
        for (size_t k = 0; k < c_N2_HC; k++) {
          double kk[3] = {
              kmode(i, c_N0, L0), kmode(j, c_N1, L1), kmode(k, c_N2, L2)};
          size_t ijk[3] = {i, j, k};

          double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
          double fac = -kk[axis] / ksquared * inv_volume;

          std::complex<double> &in_delta = deltao[i][j][k];

          if (ijk[axis] == Ns[axis]) {
            tmp[i][j][k] = 0;
          } else {
            tmp[i][j][k] = std::complex<double>(
                -in_delta.imag() * fac, in_delta.real() * fac);
          }
        }
    if (c_startN0 == 0 && c_localN0 > 0) {
      tmp[0][0][0] = 0;
      tmp[0][0][c_N2_HC - 1] = 0;
      tmp[0][c_N1 / 2][0] = 0;
      tmp[0][c_N1 / 2][c_N2_HC - 1] = 0;
    }

    if (c_startN0 <= c_N0 / 2 && c_startN0 + c_localN0 > c_N0 / 2) {
      tmp[c_N0 / 2][0][0] = 0;
      tmp[c_N0 / 2][0][c_N2_HC - 1] = 0;
      tmp[c_N0 / 2][c_N1 / 2][0] = 0;
      tmp[c_N0 / 2][c_N1 / 2][c_N2_HC - 1] = 0;
    }

    /// FFT to Realspace
    mgr->execute_c2r(c_synthesis_plan, tmp.data(), c_tmp_real_field->data());

#pragma omp parallel for collapse(3) schedule(static)
    for (size_t l = c_startN0; l < endN0; l++)
      for (size_t m = 0; m < c_N1; m++)
        for (size_t n = 0; n < c_N2; n++) {
          size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);
          vel[idx][axis] = (*c_tmp_real_field)[l][m][n];
        }
  }

  auto &ids = *lagrangian_id;
  size_t base_id = c_N2 * c_N1 * c_startN0;
#pragma omp parallel for collapse(3) schedule(static)
  for (size_t l = c_startN0; l < endN0; l++)
    for (size_t m = 0; m < c_N1; m++)
      for (size_t n = 0; n < c_N2; n++) {
        /// sort particles on equidistant grid
        double q0 = L0 / double(c_N0) * double(l);
        double q1 = L1 / double(c_N1) * double(m);
        double q2 = L2 / double(c_N2) * double(n);

        size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);

        double DD1 = lctim[idx][0];

        double x = q0 - DD1 * vel[idx][0];
        double y = q1 - DD1 * vel[idx][1];
        double z = q2 - DD1 * vel[idx][2];

        ///enforce periodic boundary conditions
        pos[idx][0] = periodic_fix(x, 0., L0);
        pos[idx][1] = periodic_fix(y, 0., L1);
        pos[idx][2] = periodic_fix(z, 0., L2);

        ids[idx] = idx + base_id;
        ///NOTE: displacements are already stored in the velocity vectors. Only need to multiply by prefactor

        ///store velocities in km/sec
        ///note we multiply by a^2 to get the correct momentum variable for the particle mesh code
        ///and normalize to code units
        double V_SCALING = lctim[idx][1];
        vel[idx][0] *= V_SCALING;
        vel[idx][1] *= V_SCALING;
        vel[idx][2] *= V_SCALING;
      }

  realInfo.localNumParticlesAfter = realInfo.localNumParticlesBefore =
      c_localN0 * c_N1 * c_N2;
  // This is for noting down which particles to copy. This
  // is inoccuous as long as redshift load balancing is properly called
  // in its right time.
  redshiftInfo.localNumParticlesAfter = realInfo.localNumParticlesAfter;
}

template <typename CIC>
void BorgLptModel<CIC>::lpt_redshift_pos(
    PhaseArrayRef &pos, PhaseArrayRef &vel, PhaseArrayRef &s_pos,
    PhaseArrayRef &lctim) {
  Cosmology cosmo(cosmo_params);

  //this routine generates particle positions in redshift space
  double anh = af;
  double Hubble = cosmo.Hubble(anh) / cosmo_params.h; ///km /sec /(Mpc/h)

  // the code uses particle momenta p=a^2 dx/dt where x is the co-moving position
  // peculiar velocities are then given by v_pec = p/a

  //NOTE: Check coefficients
  ArrayType1d::ArrayType &observer = vobs;

#pragma omp parallel for
  for (size_t idx = 0; idx < realInfo.localNumParticlesAfter; idx++) {
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

    double facRSD = lctim
        [idx]
        [2]; //this factor is 1/H/a for velocities in [km/sec] an additional factor arises from momentum conversion

    double A = facRSD * v_los / r2_los;

    double s0 = x0g + A * x0;
    double s1 = x1g + A * x1;
    double s2 = x2g + A * x2;

    ///enforce periodic boundary conditions
    s_pos[idx][0] = periodic_fix(s0, 0., L0);
    s_pos[idx][1] = periodic_fix(s1, 0., L1);
    s_pos[idx][2] = periodic_fix(s2, 0., L2);
  }
  // Update the info for redshift particles
  redshiftInfo.localNumParticlesAfter = redshiftInfo.localNumParticlesBefore =
      realInfo.localNumParticlesAfter;
}

template <typename CIC>
void BorgLptModel<CIC>::lpt_density_obs(
    PhaseArrayRef &pos, ArrayRef &deltao, size_t numParts) {
  double const nmean = double(c_N0 * c_N1 * c_N2) /
                       (box_output.N0 * box_output.N1 * box_output.N2);

  if (ALWAYS_MPI(comm)) {
    typedef UninitializedArray<boost::multi_array<double, 3>> U_Array;
    typedef U_Array::array_type::index_range i_range;
    U_Array::array_type::index_gen indices;
    // Here we have to introduce ghost planes.
    U_Array tmp_delta(out_mgr->extents_real(CIC::MPI_PLANE_LEAKAGE));

    array::fill(tmp_delta.get_array(), 0);
    Console::instance().format<LOG_DEBUG>("numParts = %d", numParts);
    CIC::projection(
        pos, tmp_delta.get_array(), box_output.L0, box_output.L1, box_output.L2,
        box_output.N0, box_output.N1, box_output.N2,
        typename CIC::Periodic_MPI(
            box_output.N0, box_output.N1, box_output.N2, comm),
        CIC_Tools::DefaultWeight(), numParts);

    // CIC has MPI_PLANE_LEAKAGE extra planes. They have to be sent to the adequate nodes.
    density_exchange_planes<true>(
        comm, tmp_delta.get_array(), out_mgr, CIC::MPI_PLANE_LEAKAGE);

    fwrap(deltao[out_mgr->strict_range()]) =
        tmp_delta.get_array()[out_mgr->strict_range()];
  } else {
    array::fill(deltao, 0);
    Console::instance().format<LOG_DEBUG>("projection with deltao");
    CIC::projection(
        pos, deltao, box_output.L0, box_output.L1, box_output.L2, box_output.N0,
        box_output.N1, box_output.N2,
        CIC_Tools::Periodic(box_output.N0, box_output.N1, box_output.N2),
        CIC_Tools::DefaultWeight(), numParts);
  }

  array::density_rescale(deltao, nmean);

  if (DUMP_BORG_DENSITY) {
    std::string fname = str(format("borg_density_%d.h5") % comm->rank());
    H5::H5File f(fname, H5F_ACC_TRUNC);
    CosmoTool::hdf5_write_array(f, "density", deltao);
  }
}

template <typename CIC>
void BorgLptModel<CIC>::lpt_fwd_model(
    CArrayRef &deltao, PhaseArrayRef &pos, PhaseArrayRef &vel,
    PhaseArrayRef &lctim) {
  ConsoleContext<LOG_DEBUG> ctx("BORG forward model");

  if (false) {
    static int step = 0;
    std::string fname = str(format("fwd_ic_%d_%d.h5") % step % comm->rank());
    H5::H5File f(fname, H5F_ACC_TRUNC);
    CosmoTool::hdf5_write_array(f, "deltao", deltao);
    step++;
  }

  if (c_deltao != 0) {
    array::fill(*c_deltao, 0);
    mgr->upgrade_complex(*lo_mgr, deltao, *c_deltao);
    lpt_ic(*c_deltao, pos, vel, lctim);
  } else {
    ///NOTE: ICs are generated at ai
    lpt_ic(deltao, pos, vel, lctim);
  }
}

template <typename CIC>
void BorgLptModel<CIC>::forwardModelRsdField(
    ArrayRef &deltaf, double *vobs_ext) {
  ConsoleContext<LOG_DEBUG> ctx("BORG forward model rsd density calculation");

  ///introduce redshift distortions
  if (do_rsd) {
    //ArrayType1d::ArrayType& dummy = vobs;

    //set vobs to input
    double dummy[3];

    dummy[0] = vobs[0];
    dummy[1] = vobs[1];
    dummy[2] = vobs[2];

    vobs[0] = vobs_ext[0];
    vobs[1] = vobs_ext[1];
    vobs[2] = vobs_ext[2];
    //ctx.print(format("old_v = %g,%g,%g   vnew = %g,%g,%g") % vobs[0] % vobs[1] % vobs[2] % vobs_ext[0] % vobs_ext[1] % vobs_ext[2]);

    ctx.print("doing redshift space distortions.");
    lpt_redshift_pos(
        u_pos->get_array(), u_vel->get_array(), u_s_pos->get_array(),
        lc_timing->get_array());

    // Reset indexes
    LibLSS::initIndexes(
        redshiftInfo.u_idx->get_array(), redshiftInfo.localNumParticlesBefore);
    particle_redistribute(
        redshiftInfo, u_s_pos->get_array(),
        typename CIC::Distribution(lo_mgr, L0, L1, L2));

    lpt_density_obs(
        u_s_pos->get_array(), deltaf, redshiftInfo.localNumParticlesAfter);

    //reset vobs
    vobs[0] = dummy[0];
    vobs[1] = dummy[1];
    vobs[2] = dummy[2];
  }
}

template <typename CIC>
void BorgLptModel<CIC>::test_lpt_velocities(MarkovState &state) {
  typedef ArrayStateElement<double, 2> PhaseArrayElement;
  auto s_hat_p = mgr->allocate_complex_array();
  auto &s_hat = s_hat_p.get_array();
  IArrayType::ArrayType &key_array = *state.get<IArrayType>("k_keys")->array;
  ArrayType1d::ArrayType &pspec =
      *state.get<ArrayType1d>("powerspectrum")->array;
  int k0_test = 2, k1_test = 5, k2_test = 3;
  double A_k = pspec[key_array[k0_test][k1_test][k2_test]] * volume;

  PhaseArrayElement *pos_e =
      new PhaseArrayElement(extents[c_localN0 * c_N1 * c_N2][3]);
  PhaseArrayElement *vel_e =
      new PhaseArrayElement(extents[c_localN0 * c_N1 * c_N2][3]);
  PhaseArrayElement *timing_e =
      new PhaseArrayElement(extents[c_localN0 * c_N1 * c_N2][2]);

  state.newElement("lpt_pos", pos_e);
  state.newElement("lpt_vel", vel_e);

  auto &pos = *pos_e->array;
  auto &vel = *vel_e->array;
  auto &lc_timing = *timing_e->array;

  gen_light_cone_timing(lc_timing);

  fwrap(s_hat) = 0;
  s_hat[k0_test][k1_test][k2_test] = std::sqrt(A_k) / volume;

  //    Hermiticity_fixup(s_hat);

  state.newScalar<double>("A_k_test", std::sqrt(A_k));
  ArrayType1d *e_k_pos;
  state.newElement("k_pos_test", e_k_pos = new ArrayType1d(extents[3]));
  ArrayType1d::ArrayType &a_k_pos = *(e_k_pos->array);

  a_k_pos[0] = kmode(k0_test, N0, L0);
  a_k_pos[1] = kmode(k1_test, N1, L1);
  a_k_pos[2] = kmode(k2_test, N2, L2);

  lpt_ic(s_hat, pos, vel, lc_timing);
}

template <typename CIC>
void BorgLptModel<CIC>::gen_light_cone_timing(PhaseArrayRef &lctim) {
  Cosmology cosmo(cosmo_params);
  ConsoleContext<LOG_VERBOSE> ctx("lightcone computation");

  cosmo.precompute_d_plus();
  cosmo.precompute_com2a();

  double an = af; ///set position ics at r_{0}, calculate till present epoch
  double anh =
      af; ///velocities are created at v_{0-1/2}, calculate till present epoch
  double D0 = cosmo.d_plus(a_init);

  double a_lc = af;

  double D1 = cosmo.d_plus(a_lc) / D0;
  double f1 = cosmo.g_plus(a_lc);
  double Hubble = cosmo.Hubble(a_lc) / cosmo_params.h; ///km /sec /(Mpc/h)
  double v_scaling = -D1 * f1 * a_lc * a_lc * Hubble;
  double facRSD = 1. / a_lc / Hubble;

  if (lctime) {
    using boost::lambda::_1;

    double r0 = 0.;
    double r1 = 2. * lcboost *
                sqrt(
                    (L0 + xmin0) * (L0 + xmin0) + (L1 + xmin1) * (L1 + xmin1) +
                    (L2 + xmin2) * (L2 + xmin2));
    double step = 2.;

    ctx.print("Tabulating D+");
    auto auxDplus = build_auto_interpolator(
        boost::bind(&Cosmology::comph2d_plus, &cosmo, _1), r0, r1, step,
        cosmo.comph2d_plus(r0), cosmo.comph2d_plus(r1));
    ctx.print("Tabulating G+");
    auto auxGplus = build_auto_interpolator(
        boost::bind(&Cosmology::comph2g_plus, &cosmo, _1), r0, r1, step,
        cosmo.comph2g_plus(r0), cosmo.comph2g_plus(r1));
    ctx.print("Tabulating H");
    auto auxHubble = build_auto_interpolator(
        boost::bind(&Cosmology::comph2Hubble, &cosmo, _1), r0, r1, step,
        cosmo.comph2Hubble(r0), cosmo.comph2Hubble(r1));
    ctx.print("Tabulating a");
    auto auxa = build_auto_interpolator(
        boost::bind(&Cosmology::comph2a, &cosmo, _1), r0, r1, step,
        cosmo.comph2a(r0), cosmo.comph2a(r1));

    ctx.print("Extruding lightcone");
///For every particle calculate distance to observer
#pragma omp parallel for collapse(3)
    for (int l = c_startN0; l < c_startN0 + c_localN0; l++)
      for (int m = 0; m < c_N1; m++)
        for (int n = 0; n < c_N2; n++) {
          size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);

          /// sort particles on equidistant grid
          double x0 = L0 / double(c_N0) * double(l) + xmin0;
          double x1 = L1 / double(c_N1) * double(m) + xmin1;
          double x2 = L2 / double(c_N2) * double(n) + xmin2;
          double r_obs = sqrt(x0 * x0 + x1 * x1 + x2 * x2) * lcboost;
          D1 = auxDplus(r_obs) / D0;
          f1 = auxGplus(r_obs);
          Hubble = auxHubble(r_obs) / cosmo_params.h; ///km /sec /(Mpc/h)
          a_lc = auxa(r_obs);
          v_scaling = -D1 * f1 * a_lc * a_lc * Hubble;
          facRSD = 1. / a_lc / Hubble;

          lctim[idx][0] = D1;
          lctim[idx][1] = v_scaling;
          lctim[idx][2] = facRSD;
        }
  } else {
#pragma omp parallel for collapse(3)
    for (int l = c_startN0; l < c_startN0 + c_localN0; l++)
      for (int m = 0; m < c_N1; m++)
        for (int n = 0; n < c_N2; n++) {
          size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);

          lctim[idx][0] = D1;
          lctim[idx][1] = v_scaling;
          lctim[idx][2] = facRSD;
        }
  }
}

template <typename CIC>
void BorgLptModel<CIC>::forwardModel_v2(ModelInput<3> delta_init) {
  ConsoleContext<LOG_DEBUG> ctx("BORG LPT MODEL");

  delta_init.setRequestedIO(PREFERRED_FOURIER);

  size_t partNum = size_t(c_localN0 * c_N1 * c_N2 * partFactor);

  u_pos.reset();
  u_vel.reset();
  lagrangian_id.reset();

  lagrangian_id = std::unique_ptr<IdxArray>(new IdxArray(extents[partNum]));
  u_pos = std::make_shared<U_PArray>(extents[partNum][3]);
  u_vel = std::make_shared<U_PArray>(extents[partNum][3]);

  realInfo.allocate(comm, partNum);
  if (do_rsd) {
    u_s_pos = std::make_shared<U_PArray>(extents[partNum][3]);
    redshiftInfo.allocate(comm, partNum);
  }

  delta_init.needDestroyInput();
  lpt_fwd_model(
      delta_init.getFourier(), u_pos->get_array(), u_vel->get_array(),
      lc_timing->get_array());

  try {
    ///introduce redshift distortions
    if (do_rsd) {

      ctx.print("doing redshift space distortions.");
      // Particle redistribution, real space, this step could be avoided I think (i.e. just remove the line)
      lpt_redshift_pos(
          u_pos->get_array(), u_vel->get_array(), u_s_pos->get_array(),
          lc_timing->get_array());

      particle_redistribute(
          redshiftInfo, u_s_pos->get_array(),
          typename CIC::Distribution(out_mgr, L0, L1, L2),
          make_attribute_helper(Particles::scalar(*lagrangian_id)));
    } else {
      particle_redistribute(
          realInfo, u_pos->get_array(),
          typename CIC::Distribution(out_mgr, L0, L1, L2),
          make_attribute_helper(
              Particles::vector(u_vel->get_array()),
              Particles::scalar(*lagrangian_id)));
      redshiftInfo.localNumParticlesAfter = realInfo.localNumParticlesAfter;
    }
  } catch (const ErrorLoadBalance &) {
    // If load balance failure it means our sample is deeply wrong. Free resources and inform the caller.
    releaseParticles();
    forwardModelHold = false;
    throw;
  }
}

template <typename CIC>
void BorgLptModel<CIC>::getDensityFinal(ModelOutput<3> delta_output) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  this->invalidCache = false;
  delta_output.setRequestedIO(PREFERRED_REAL);

  ctx.format(
      "output shape is %dx%dx%d", delta_output.getRealOutput().shape()[0],
      delta_output.getRealOutput().shape()[1],
      delta_output.getRealOutput().shape()[2]);

  if (do_rsd) {
    // Now we can project
    lpt_density_obs(
        u_s_pos->get_array(), delta_output.getRealOutput(),
        redshiftInfo.localNumParticlesAfter);
  } else {
    lpt_density_obs(
        u_pos->get_array(), delta_output.getRealOutput(),
        realInfo.localNumParticlesAfter);
  }

  /* if (!forwardModelHold && !adjointRequired) {
    releaseParticles();
  }*/
  forwardModelHold = false;
}
// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2014-2020
// ARES TAG: name(1) = Jens Jasche
// ARES TAG: email(1) = jens.jasche@fysik.su.se
// ARES TAG: year(1) = 2009-2018

