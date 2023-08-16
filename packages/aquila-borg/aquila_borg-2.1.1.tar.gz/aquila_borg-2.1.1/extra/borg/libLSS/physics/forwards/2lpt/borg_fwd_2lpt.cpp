/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/2lpt/borg_fwd_2lpt.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

// Be advised that deltao is already scaled. So the first fourier transform from deltao -> real space
// is free of scaling. But none of the others, which has to be scaled by 1/(L^3)

#include "../pm/plane_xchg.hpp"

template <typename CIC>
void Borg2LPTModel<CIC>::lpt2_ic(
    CArrayRef &deltao, PhaseArrayRef &pos, PhaseArrayRef &vel,
    PhaseArrayRef &lctim) {
  // set cosmological parameters
  // Initial density is scaled to initial redshift!
  ConsoleContext<LOG_DEBUG> ctx("lpt2_ic");
  Cosmology cosmo(cosmo_params);
  double fft_normalization = 1.0 / (c_N0 * c_N1 * c_N2);
  double inv_volume = 1 / (L0 * L1 * L2);

  typedef UninitializedArray<
      FFTW_Complex_Array, FFTW_Allocator<std::complex<double>>>
      U_CArray;
  typedef U_CArray::array_type Ref_CArray;

  U_CArray tmp_p(mgr->extents_complex(), mgr->allocator_complex);
  Ref_CArray &tmp = tmp_p.get_array();

  for (int axis = 0; axis < 3; axis++) {
#pragma omp parallel for collapse(3)
    for (size_t i = c_startN0; i < c_startN0 + c_localN0; i++)
      for (size_t j = 0; j < c_N1; j++)
        for (size_t k = 0; k < c_N2_HC; k++) {
          double kk[3] = {kmode(i, c_N0, L0), kmode(j, c_N1, L1),
                          kmode(k, c_N2, L2)};

          double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
          double fac = -kk[axis] / ksquared * inv_volume;

          std::complex<double> &in_delta = deltao[i][j][k];

          tmp[i][j][k] = std::complex<double>(
              -in_delta.imag() * fac, in_delta.real() * fac);

          std::complex<double> &aux = tmp[i][j][k];

          // calculate second order LPT terms
          if (axis == 0) {
            /* disp0,0 */
            (*c_psi_00)[i][j][k] =
                std::complex<double>(-aux.imag() * kk[0], aux.real() * kk[0]);

            /* disp0,1 */
            (*c_psi_01)[i][j][k] =
                std::complex<double>(-aux.imag() * kk[1], aux.real() * kk[1]);

            /* disp0,2 */
            (*c_psi_02)[i][j][k] =
                std::complex<double>(-aux.imag() * kk[2], aux.real() * kk[2]);
          }

          // calculate second order LPT terms
          if (axis == 1) {
            /* disp1,1 */
            (*c_psi_11)[i][j][k] =
                std::complex<double>(-aux.imag() * kk[1], aux.real() * kk[1]);

            /* disp1,2 */
            (*c_psi_12)[i][j][k] =
                std::complex<double>(-aux.imag() * kk[2], aux.real() * kk[2]);
          }

          // calculate second order LPT terms
          if (axis == 2) {
            /* disp2,2 */
            (*c_psi_22)[i][j][k] =
                std::complex<double>(-aux.imag() * kk[2], aux.real() * kk[2]);
          }
        }

    if (c_startN0 == 0 && c_localN0 > 0) {
      tmp[0][0][0] = 0;
      tmp[0][0][c_N2_HC - 1] = 0;
      tmp[0][c_N1 / 2][0] = 0;
      tmp[0][c_N1 / 2][c_N2_HC - 1] = 0;

      (*c_psi_00)[0][0][0] = 0;
      (*c_psi_00)[0][0][c_N2_HC - 1] = 0;
      (*c_psi_00)[0][c_N1 / 2][0] = 0;
      (*c_psi_00)[0][c_N1 / 2][c_N2_HC - 1] = 0;

      (*c_psi_01)[0][0][0] = 0;
      (*c_psi_01)[0][0][c_N2_HC - 1] = 0;
      (*c_psi_01)[0][c_N1 / 2][0] = 0;
      (*c_psi_01)[0][c_N1 / 2][c_N2_HC - 1] = 0;

      (*c_psi_02)[0][0][0] = 0;
      (*c_psi_02)[0][0][c_N2_HC - 1] = 0;
      (*c_psi_02)[0][c_N1 / 2][0] = 0;
      (*c_psi_02)[0][c_N1 / 2][c_N2_HC - 1] = 0;

      (*c_psi_11)[0][0][0] = 0;
      (*c_psi_11)[0][0][c_N2_HC - 1] = 0;
      (*c_psi_11)[0][c_N1 / 2][0] = 0;
      (*c_psi_11)[0][c_N1 / 2][c_N2_HC - 1] = 0;

      (*c_psi_12)[0][0][0] = 0;
      (*c_psi_12)[0][0][c_N2_HC - 1] = 0;
      (*c_psi_12)[0][c_N1 / 2][0] = 0;
      (*c_psi_12)[0][c_N1 / 2][c_N2_HC - 1] = 0;

      (*c_psi_22)[0][0][0] = 0;
      (*c_psi_22)[0][0][c_N2_HC - 1] = 0;
      (*c_psi_22)[0][c_N1 / 2][0] = 0;
      (*c_psi_22)[0][c_N1 / 2][c_N2_HC - 1] = 0;
    }

    if (c_startN0 <= c_N0 / 2 && c_startN0 + c_localN0 > c_N0 / 2) {
      tmp[c_N0 / 2][0][0] = 0;
      tmp[c_N0 / 2][0][c_N2_HC - 1] = 0;
      tmp[c_N0 / 2][c_N1 / 2][0] = 0;
      tmp[c_N0 / 2][c_N1 / 2][c_N2_HC - 1] = 0;

      (*c_psi_00)[c_N0 / 2][0][0] = 0;
      (*c_psi_00)[c_N0 / 2][0][c_N2_HC - 1] = 0;
      (*c_psi_00)[c_N0 / 2][c_N1 / 2][0] = 0;
      (*c_psi_00)[c_N0 / 2][c_N1 / 2][c_N2_HC - 1] = 0;

      (*c_psi_01)[c_N0 / 2][0][0] = 0;
      (*c_psi_01)[c_N0 / 2][0][c_N2_HC - 1] = 0;
      (*c_psi_01)[c_N0 / 2][c_N1 / 2][0] = 0;
      (*c_psi_01)[c_N0 / 2][c_N1 / 2][c_N2_HC - 1] = 0;

      (*c_psi_02)[c_N0 / 2][0][0] = 0;
      (*c_psi_02)[c_N0 / 2][0][c_N2_HC - 1] = 0;
      (*c_psi_02)[c_N0 / 2][c_N1 / 2][0] = 0;
      (*c_psi_02)[c_N0 / 2][c_N1 / 2][c_N2_HC - 1] = 0;

      (*c_psi_11)[c_N0 / 2][0][0] = 0;
      (*c_psi_11)[c_N0 / 2][0][c_N2_HC - 1] = 0;
      (*c_psi_11)[c_N0 / 2][c_N1 / 2][0] = 0;
      (*c_psi_11)[c_N0 / 2][c_N1 / 2][c_N2_HC - 1] = 0;

      (*c_psi_12)[c_N0 / 2][0][0] = 0;
      (*c_psi_12)[c_N0 / 2][0][c_N2_HC - 1] = 0;
      (*c_psi_12)[c_N0 / 2][c_N1 / 2][0] = 0;
      (*c_psi_12)[c_N0 / 2][c_N1 / 2][c_N2_HC - 1] = 0;

      (*c_psi_22)[c_N0 / 2][0][0] = 0;
      (*c_psi_22)[c_N0 / 2][0][c_N2_HC - 1] = 0;
      (*c_psi_22)[c_N0 / 2][c_N1 / 2][0] = 0;
      (*c_psi_22)[c_N0 / 2][c_N1 / 2][c_N2_HC - 1] = 0;
    }

    // FFT to Realspace
    mgr->execute_c2r(c_synthesis_plan, tmp.data(), c_tmp_real_field->data());

#pragma omp parallel for collapse(2)
    for (int l = c_startN0; l < c_startN0 + c_localN0; l++)
      for (int m = 0; m < c_N1; m++)
        for (int n = 0; n < c_N2; n++) {
          size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);
          vel[idx][axis] = (*c_tmp_real_field)[l][m][n];
        }
  }

  // FFT to Realspace 2lpt
  mgr->execute_c2r(c_synthesis_plan, c_psi_00->data(), r_psi_00->data());
  mgr->execute_c2r(c_synthesis_plan, c_psi_01->data(), r_psi_01->data());
  mgr->execute_c2r(c_synthesis_plan, c_psi_02->data(), r_psi_02->data());
  mgr->execute_c2r(c_synthesis_plan, c_psi_11->data(), r_psi_11->data());
  mgr->execute_c2r(c_synthesis_plan, c_psi_12->data(), r_psi_12->data());
  mgr->execute_c2r(c_synthesis_plan, c_psi_22->data(), r_psi_22->data());

// Calculate source for second order displacement
#pragma omp parallel for collapse(2)
  for (int l = c_startN0; l < c_startN0 + c_localN0; l++)
    for (int m = 0; m < c_N1; m++)
      for (int n = 0; n < c_N2; n++) {
        // Calculates source for second order displacement
        // RHS of eq. (D6) in Scoccimarro 1998, MNRAS 299, 1097

        double t00 = (*r_psi_00)[l][m][n]; // 0
        double t01 = (*r_psi_01)[l][m][n]; // 1
        double t02 = (*r_psi_02)[l][m][n]; // 2
        double t11 = (*r_psi_11)[l][m][n]; // 3
        double t12 = (*r_psi_12)[l][m][n]; // 4
        double t22 = (*r_psi_22)[l][m][n]; // 5

        (*c_tmp_real_field)[l][m][n] =
            t00 * (t11 + t22) + t11 * t22 - t01 * t01 - t02 * t02 - t12 * t12;
        (*c_tmp_real_field)[l][m][n] *=
            fft_normalization; // Multiply here to be ready for the r2c and c2r. L^3 cancels out.
      }

  // FFT to Fourier-space
  mgr->execute_r2c(
      c_analysis_plan, c_tmp_real_field->data(), c_tmp_complex_field->data());

  // create dummy array for second order displacement
  UninitializedArray<PhaseArray> vel2(extents[c_localN0 * c_N1 * c_N2][3]);

  for (int axis = 0; axis < 3; axis++) {
#pragma omp parallel for collapse(2)
    for (int i = c_startN0; i < c_startN0 + c_localN0; i++)
      for (int j = 0; j < c_N1; j++)
        for (int k = 0; k < c_N2_HC; k++) {
          double kk[3] = {kmode(i, c_N0, L0), kmode(j, c_N1, L1),
                          kmode(k, c_N2, L2)};

          double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
          double fac = -kk[axis] / ksquared;

          std::complex<double> &aux = (*c_tmp_complex_field)[i][j][k];

          tmp[i][j][k] =
              std::complex<double>(-aux.imag() * fac, aux.real() * fac);
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

    // FFT to Realspace
    mgr->execute_c2r(c_synthesis_plan, tmp.data(), c_tmp_real_field->data());

    size_t c_endN0 = c_startN0 + c_localN0;
    auto &v_array = vel2.get_array();
#pragma omp parallel for collapse(3)
    for (size_t l = c_startN0; l < c_endN0; l++)
      for (size_t m = 0; m < c_N1; m++)
        for (size_t n = 0; n < c_N2; n++) {
          size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);
          v_array[idx][axis] = (*c_tmp_real_field)[l][m][n];
        }
  }

  auto &ids = *lagrangian_id;
  size_t base_id = c_N2 * c_N1 * c_startN0;

#pragma omp parallel for collapse(2)
  for (int l = c_startN0; l < c_startN0 + c_localN0; l++)
    for (int m = 0; m < c_N1; m++)
      for (int n = 0; n < c_N2; n++) {
        // sort particles on equidistant grid
        double q0 = L0 / double(c_N0) * double(l);
        double q1 = L1 / double(c_N1) * double(m);
        double q2 = L2 / double(c_N2) * double(n);

        size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);

        double DD1 = lctim[idx][0];
        double DD2 = lctim[idx][3];
        auto displ = vel[idx];
        auto displ_2 = vel2.get_array()[idx];

        double x = q0 - DD1 * displ[0] + DD2 * displ_2[0];
        double y = q1 - DD1 * displ[1] + DD2 * displ_2[1];
        double z = q2 - DD1 * displ[2] + DD2 * displ_2[2];

        // enforce periodic boundary conditions
        pos[idx][0] = periodic_fix(x, 0., L0);
        pos[idx][1] = periodic_fix(y, 0., L1);
        pos[idx][2] = periodic_fix(z, 0., L2);

        ids[idx] = idx + base_id;

        // NOTE: displacements are already stored in the velocity vectors. Only need to multiply by prefactor

        // store velocities in km/sec
        // note we multiply by a^2 to get the correct momentum variable for the particle mesh code
        // and normalize to code units
        double v1_scaling = lctim[idx][1];
        double v2_scaling = lctim[idx][4];
        displ[0] = displ[0] * v1_scaling + v2_scaling * displ_2[0];
        displ[1] = displ[1] * v1_scaling + v2_scaling * displ_2[1];
        displ[2] = displ[2] * v1_scaling + v2_scaling * displ_2[2];
      }

  realInfo.localNumParticlesAfter = realInfo.localNumParticlesBefore =
      c_localN0 * c_N1 * c_N2;
  redshiftInfo.localNumParticlesBefore = realInfo.localNumParticlesAfter;
  redshiftInfo.localNumParticlesAfter = realInfo.localNumParticlesAfter;
}

template <typename CIC>
void Borg2LPTModel<CIC>::lpt2_redshift_pos(
    PhaseArrayRef &pos, PhaseArrayRef &vel, PhaseArrayRef &s_pos,
    PhaseArrayRef &lctim) {
  Cosmology cosmo(cosmo_params);

  // this routine generates particle positions in redshift space
  // the code uses particle momenta p=a^2 dx/dt where x is the co-moving position
  // peculiar velocities are then given by v_pec = p/a

  // NOTE: Check coefficients
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
        [2]; // this factor is 1/H/a for velocities in [km/sec] an additional factor arises from momentum conversion

    double A = facRSD * v_los / r2_los;

    double s0 = x0g + A * x0;
    double s1 = x1g + A * x1;
    double s2 = x2g + A * x2;

    // enforce periodic boundary conditions
    s_pos[idx][0] = periodic_fix(s0, 0., L0);
    s_pos[idx][1] = periodic_fix(s1, 0., L1);
    s_pos[idx][2] = periodic_fix(s2, 0., L2);
  }
  // Update the info for redshift particles
  redshiftInfo.localNumParticlesAfter = redshiftInfo.localNumParticlesBefore =
      realInfo.localNumParticlesAfter;
}

template <typename CIC>
void Borg2LPTModel<CIC>::lpt2_density_obs(
    PhaseArrayRef &pos, ArrayRef &deltao, size_t numParts) {
  double const nmean = double(c_N0*c_N1*c_N2)/(box_output.N0*box_output.N1*box_output.N2);

  if (ALWAYS_MPI(comm)) {
    typedef UninitializedArray<boost::multi_array<double, 3>> U_Array;
    typedef U_Array::array_type::index_range i_range;
    U_Array::array_type::index_gen indices;
    // Here we have to introduce ghost planes.
    U_Array tmp_delta(out_mgr->extents_real(CIC::MPI_PLANE_LEAKAGE));

    array::fill(tmp_delta.get_array(), 0);
    Console::instance().print<LOG_VERBOSE>(format("numParts = %d") % numParts);
    CIC::projection(
        pos, tmp_delta.get_array(), L0, L1, L2, out_mgr->N0, out_mgr->N1, out_mgr->N2,
        typename CIC::Periodic_MPI(out_mgr->N0, out_mgr->N1, out_mgr->N2, comm),
        CIC_Tools::DefaultWeight(), numParts);
    // CIC has MPI_PLANE_LEAKAGE extra planes. They have to be sent to the adequate nodes.
    density_exchange_planes<true>(
        comm, tmp_delta.get_array(), out_mgr, CIC::MPI_PLANE_LEAKAGE);

   fwrap(deltao[out_mgr->strict_range()]) =
           tmp_delta.get_array()[out_mgr->strict_range()];
  } else {
    array::fill(deltao, 0);
    cic.projection(
        pos, deltao, L0, L1, L2, out_mgr->N0, out_mgr->N1, out_mgr->N2, CIC_Tools::Periodic(out_mgr->N0, out_mgr->N1, out_mgr->N2),
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
void Borg2LPTModel<CIC>::lpt2_fwd_model(
    CArrayRef &deltao, PhaseArrayRef &pos, PhaseArrayRef &vel,
    PhaseArrayRef &lctim) {
  ConsoleContext<LOG_DEBUG> ctx("BORG forward model");

  if (c_deltao != 0) {
    array::fill(*c_deltao, 0);
    mgr->upgrade_complex(*lo_mgr, deltao, *c_deltao);
    lpt2_ic(*c_deltao, pos, vel, lctim);
  } else {
    // NOTE: ICs are generated at ai
    lpt2_ic(deltao, pos, vel, lctim);
  }
}

template <typename CIC>
void Borg2LPTModel<CIC>::forwardModelRsdField(
    ArrayRef &deltaf, double *vobs_ext) {
  ConsoleContext<LOG_DEBUG> ctx("BORG forward model rsd density calculation");

  // introduce redshift distortions
  if (do_rsd) {
    // ArrayType1d::ArrayType& dummy = vobs;

    // set vobs to input
    double dummy[3];

    dummy[0] = vobs[0];
    dummy[1] = vobs[1];
    dummy[2] = vobs[2];

    vobs[0] = vobs_ext[0];
    vobs[1] = vobs_ext[1];
    vobs[2] = vobs_ext[2];
    // ctx.print(format("old_v = %g,%g,%g   vnew = %g,%g,%g") % vobs[0] % vobs[1] % vobs[2] % vobs_ext[0] % vobs_ext[1] % vobs_ext[2]);

    ctx.print("doing redshift space distortions.");
    lpt2_redshift_pos(
        u_pos->get_array(), u_vel->get_array(), u_s_pos->get_array(),
        lc_timing->get_array());

    // Reset indexes
    LibLSS::initIndexes(
        redshiftInfo.u_idx->get_array(), redshiftInfo.localNumParticlesBefore);
    particle_redistribute(
        redshiftInfo, u_s_pos->get_array(),
        typename CIC::Distribution(lo_mgr, L0, L1, L2));

    lpt2_density_obs(
        u_s_pos->get_array(), deltaf, redshiftInfo.localNumParticlesAfter);

    // reset vobs
    vobs[0] = dummy[0];
    vobs[1] = dummy[1];
    vobs[2] = dummy[2];
  }
}

template <typename CIC>
void Borg2LPTModel<CIC>::test_lpt2_velocities(MarkovState &state) {
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
      new PhaseArrayElement(extents[c_localN0 * c_N1 * c_N2][5]);

  state.newElement("lpt2_pos", pos_e);
  state.newElement("lpt2_vel", vel_e);

  auto &pos = *pos_e->array;
  auto &vel = *vel_e->array;
  auto &lc_timing = *timing_e->array;

  gen_light_cone_timing(lc_timing);

  array::EigenMap<CArray>::map(s_hat).fill(0);
  s_hat[k0_test][k1_test][k2_test] = std::sqrt(A_k) / volume;

  // Hermiticity_fixup(s_hat);

  state.newScalar<double>("A_k_test", std::sqrt(A_k));
  ArrayType1d *e_k_pos;
  state.newElement("k_pos_test", e_k_pos = new ArrayType1d(extents[3]));
  ArrayType1d::ArrayType &a_k_pos = *(e_k_pos->array);

  a_k_pos[0] = kmode(k0_test, N0, L0);
  a_k_pos[1] = kmode(k1_test, N1, L1);
  a_k_pos[2] = kmode(k2_test, N2, L2);

  lpt2_ic(s_hat, pos, vel, lc_timing);
}

template <typename CIC>
void Borg2LPTModel<CIC>::gen_light_cone_timing(PhaseArrayRef &lctim) {
  Cosmology cosmo(cosmo_params);
  double D0 = cosmo.d_plus(a_init);

  double a_lc = af;

  double D1 = cosmo.d_plus(a_lc) / D0;
  double f1 = cosmo.g_plus(a_lc);
  double Hubble = cosmo.Hubble(a_lc) / cosmo_params.h; // km /sec /(Mpc/h)
  double v_scaling = -D1 * f1 * a_lc * a_lc * Hubble;
  double facRSD = 1. / a_lc / Hubble;

  if (lctime) {
    using boost::lambda::_1;

    double r0 = 0.;
    double r1 =
        2. * sqrt(
                 (L0 + xmin0) * (L0 + xmin0) + (L1 + xmin1) * (L1 + xmin1) +
                 (L2 + xmin2) * (L2 + xmin2));
    double step = 1.;

    auto auxDplus = build_auto_interpolator(
        boost::bind(&Cosmology::comph2d_plus, &cosmo, _1), r0, r1, step,
        cosmo.comph2d_plus(r0), cosmo.comph2d_plus(r1));
    auto auxGplus = build_auto_interpolator(
        boost::bind(&Cosmology::comph2g_plus, &cosmo, _1), r0, r1, step,
        cosmo.comph2g_plus(r0), cosmo.comph2g_plus(r1));
    auto auxHubble = build_auto_interpolator(
        boost::bind(&Cosmology::comph2Hubble, &cosmo, _1), r0, r1, step,
        cosmo.comph2Hubble(r0), cosmo.comph2Hubble(r1));
    auto auxa = build_auto_interpolator(
        boost::bind(&Cosmology::comph2a, &cosmo, _1), r0, r1, step,
        cosmo.comph2a(r0), cosmo.comph2a(r1));

    // For every particle calculate distance to observer
    size_t c_endN0 = c_startN0 + c_localN0;
#pragma omp parallel for collapse(3)
    for (size_t l = c_startN0; l < c_endN0; l++)
      for (size_t m = 0; m < c_N1; m++)
        for (size_t n = 0; n < c_N2; n++) {
          size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);

          // sort particles on equidistant grid
          double x0 = L0 / double(c_N0) * double(l) + xmin0;
          double x1 = L1 / double(c_N1) * double(m) + xmin1;
          double x2 = L2 / double(c_N2) * double(n) + xmin2;

          double r_obs = sqrt(x0 * x0 + x1 * x1 + x2 * x2);

          D1 = auxDplus(r_obs) / D0;
          f1 = auxGplus(r_obs);
          Hubble = auxHubble(r_obs) / cosmo_params.h; // km /sec /(Mpc/h)
          a_lc = auxa(r_obs);
          v_scaling = -D1 * f1 * Hubble * a_lc * a_lc;
          facRSD = 1. / a_lc / Hubble;

          lctim[idx][0] = D1;
          lctim[idx][1] = v_scaling;
          lctim[idx][2] = facRSD;
          lctim[idx][3] = -3. / 7. * D1 * D1;
          lctim[idx][4] = -3. / 7. * D1 * D1 * 2.0 * f1 * Hubble * a_lc * a_lc;
        }
  } else {
    size_t c_endN0 = c_startN0 + c_localN0;
#pragma omp parallel for collapse(3)
    for (size_t l = c_startN0; l < c_endN0; l++)
      for (size_t m = 0; m < c_N1; m++)
        for (size_t n = 0; n < c_N2; n++) {
          size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);

          lctim[idx][0] = D1;
          lctim[idx][1] = v_scaling;
          lctim[idx][2] = facRSD;
          lctim[idx][3] = -3. / 7. * D1 * D1;
          lctim[idx][4] = -3. / 7. * D1 * D1 * 2.0 * f1 * Hubble * a_lc * a_lc;
        }
  }
}

template <typename CIC>
void Borg2LPTModel<CIC>::getDensityFinal(ModelOutput<3> delta_output) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  delta_output.setRequestedIO(PREFERRED_REAL);

  try {
    // introduce redshift distortions
    if (do_rsd) {

      ctx.print("doing redshift space distortions.");
      lpt2_redshift_pos(
          u_pos->get_array(), u_vel->get_array(), u_s_pos->get_array(),
          lc_timing->get_array());

      particle_redistribute(
          redshiftInfo, u_s_pos->get_array(),
          typename CIC::Distribution(out_mgr, L0, L1, L2),
          make_attribute_helper(Particles::scalar(*lagrangian_id)));

      // Now we can project
      lpt2_density_obs(
          u_s_pos->get_array(), delta_output.getRealOutput(),
          redshiftInfo.localNumParticlesAfter);
    } else {
      particle_redistribute(
          realInfo, u_pos->get_array(),
          typename CIC::Distribution(out_mgr, L0, L1, L2),
          make_attribute_helper(
              Particles::vector(u_vel->get_array()),
              Particles::scalar(*lagrangian_id)));
      // Project now
      lpt2_density_obs(
          u_pos->get_array(), delta_output.getRealOutput(),
          realInfo.localNumParticlesAfter);
      redshiftInfo.localNumParticlesAfter = realInfo.localNumParticlesAfter;
    }
  } catch (const ErrorLoadBalance &) {
    // If load balance failure it means our sample is deeply wrong. Free resources and inform the caller.
    releaseParticles();
    forwardModelHold = false;
    throw;
  }
  /*
  if (!forwardModelHold && !adjointNext) {
    releaseParticles();
  }*/
  forwardModelHold = false;
}

template <typename CIC>
void Borg2LPTModel<CIC>::forwardModel_v2(ModelInput<3> delta_init) {
  ConsoleContext<LOG_DEBUG> ctx("BORG 2LPT MODEL SIMPLE");
  size_t partNum = size_t(c_localN0 * c_N1 * c_N2 * partFactor);

  delta_init.setRequestedIO(PREFERRED_FOURIER);
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

  updateCosmo();

  delta_init.needDestroyInput();
  lpt2_fwd_model(
      delta_init.getFourier(), u_pos->get_array(), u_vel->get_array(),
      lc_timing->get_array());
}
