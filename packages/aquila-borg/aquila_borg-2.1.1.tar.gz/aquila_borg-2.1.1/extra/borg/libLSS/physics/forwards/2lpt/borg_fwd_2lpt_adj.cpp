/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/2lpt/borg_fwd_2lpt_adj.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

#include "libLSS/tools/tuple_helper.hpp"
#include "libLSS/tools/fused_assign.hpp"

template <typename CIC>
void Borg2LPTModel<CIC>::lpt2_ic_ag(
    PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, PhaseArrayRef &lctim) {
  // Initial density is scaled to initial redshift!!!

  ConsoleContext<LOG_DEBUG> ctx("2LPT-IC adjoint");
  Cosmology cosmo(cosmo_params);
  double c_volNorm = 1 / volume;

  // allocate auxiliary Fourier array
  auto &AUX1 = *AUX1_p;
  auto &aux = *aux_p;
  auto &AUX0 = *AUX0_p;

  array::fill(AUX1, 0);

  // Do position derivative 1st order
  //------------------------------------------------------------------------------
  for (unsigned axis = 0; axis < 3; axis++) {
#pragma omp parallel for collapse(3)
    for (size_t l = c_startN0; l < c_startN0 + c_localN0; l++)
      for (size_t m = 0; m < c_N1; m++)
        for (size_t n = 0; n < c_N2; n++) {
          size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);
          double DD1 = lctim[idx][0];
          double v1_scaling = lctim[idx][1];
          aux[l][m][n] =
              -DD1 * pos_ag[idx][axis] + v1_scaling * vel_ag[idx][axis];
        }

    // FFT to F-space
    mgr->execute_r2c(c_analysis_plan, aux.data(), AUX0.data());

#pragma omp parallel for collapse(3)
    for (size_t i = c_startN0; i < c_startN0 + c_localN0; i++)
      for (size_t j = 0; j < c_N1; j++)
        for (size_t k = 0; k < c_N2_HC; k++) {
          double kk[3] = {kmode(i, c_N0, L0), kmode(j, c_N1, L1),
                          kmode(k, c_N2, L2)};

          double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
          double fac = -kk[axis] / ksquared * c_volNorm;

          std::complex<double> const &in_delta = AUX0[i][j][k];

          AUX1[i][j][k] += std::complex<double>(
              fac * in_delta.imag(), -fac * in_delta.real());
        }

    // Do position derivative 2nd order
    //--------------------------------------------------------------------------

    lpt2_add_to_derivative(
        AUX1, pos_ag, vel_ag, lctim, axis,
        std::make_tuple(
            std::make_tuple(
                0, 0, 1.0,
                std::make_tuple(std::cref(*r_psi_11), std::cref(*r_psi_22))),
            std::make_tuple(
                1, 1, 1.0,
                std::make_tuple(std::cref(*r_psi_22), std::cref(*r_psi_00))),
            std::make_tuple(
                2, 2, 1.0,
                std::make_tuple(std::cref(*r_psi_00), std::cref(*r_psi_11))),
            std::make_tuple(0, 1, -2.0, std::make_tuple(std::cref(*r_psi_01))),
            std::make_tuple(0, 2, -2.0, std::make_tuple(std::cref(*r_psi_02))),
            std::make_tuple(
                1, 2, -2.0, std::make_tuple(std::cref(*r_psi_12)))));
  }

  // fix hermiticity...unclear how to do that
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

namespace {
  inline double tuple_sum(ssize_t, ssize_t, ssize_t, std::tuple<>) { return 0; }

  template <typename H, typename... A>
  inline double
  tuple_sum(ssize_t i, ssize_t j, ssize_t k, std::tuple<H, A...> const &t) {
    return std::get<0>(t)[i][j][k] + tuple_sum(i, j, k, last_of_tuple<1>(t));
  }
} // namespace

template <typename CIC>
template <typename... ArrayTuple>
void Borg2LPTModel<CIC>::lpt2_add_to_derivative(
    U_F_Array::array_type &result, const PhaseArrayRef &pos_ag,
    const PhaseArrayRef &vel_ag, const PhaseArrayRef &lctim, const int axis0,
    std::tuple<ArrayTuple...> const &tuple_psi) {
  auto r_pos_psi = c_tmp_real_field;
  auto c_pos_psi = c_tmp_complex_field;

  size_t const endN0 = c_startN0 + c_localN0;
#pragma omp parallel for collapse(3)
  for (size_t l = c_startN0; l < endN0; l++)
    for (size_t m = 0; m < c_N1; m++)
      for (size_t n = 0; n < c_N2; n++) {
        size_t idx = n + c_N2 * m + c_N2 * c_N1 * (l - c_startN0);
        double DD2 = lctim[idx][3];
        double DD2v = lctim[idx][4];
        (*r_pos_psi)[l][m][n] =
            (DD2 * pos_ag[idx][axis0] + DD2v * vel_ag[idx][axis0]);
      }

  // FFT to F-space
  mgr->execute_r2c(c_analysis_plan, r_pos_psi->data(), c_pos_psi->data());

  double const inv_N = 1.0 / (c_N0 * c_N1 * c_N2);

#pragma omp parallel for collapse(3)
  for (size_t i = c_startN0; i < endN0; i++)
    for (size_t j = 0; j < c_N1; j++)
      for (size_t k = 0; k < c_N2_HC; k++) {
        double const kk[3] = {kmode(i, c_N0, L0), kmode(j, c_N1, L1),
                              kmode(k, c_N2, L2)};

        double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
        double fac = -kk[axis0] / ksquared * inv_N;

        std::complex<double> &pos_psi_ijk = (*c_pos_psi)[i][j][k];
        pos_psi_ijk = std::complex<double>(
            fac * pos_psi_ijk.imag(), -fac * pos_psi_ijk.real());
      }

  if (c_startN0 == 0 && c_localN0 > 0) {
    (*c_pos_psi)[0][0][0] = 0;
  }

  // FFT to realspace
  mgr->execute_c2r(c_synthesis_plan, c_pos_psi->data(), r_pos_psi->data());

  auto &AUX2 = *aux_p;
  LibLSS::copy_array(AUX2, *r_pos_psi);

  tuple_for_each(tuple_psi, [&](auto const &t) {
    unsigned int const axis1 = std::get<0>(t);
    unsigned int const axis2 = std::get<1>(t);
    double const prefactor = std::get<2>(t);
    auto const &psi_list = std::get<3>(t);

#pragma omp parallel for collapse(3)
    for (size_t l = c_startN0; l < endN0; l++)
      for (size_t m = 0; m < c_N1; m++)
        for (size_t n = 0; n < c_N2; n++) {
          double &pos_ijk = (*r_pos_psi)[l][m][n];
          pos_ijk = prefactor * AUX2[l][m][n] * tuple_sum(l, m, n, psi_list);
        }

    // FFT to F-space
    mgr->execute_r2c(c_analysis_plan, r_pos_psi->data(), c_pos_psi->data());

    double const inv_volume = 1 / volume;

#pragma omp parallel for collapse(3)
    for (int i = c_startN0; i < endN0; i++)
      for (int j = 0; j < c_N1; j++)
        for (int k = 0; k < c_N2_HC; k++) {
          double kk[3] = {kmode(i, c_N0, L0), kmode(j, c_N1, L1),
                          kmode(k, c_N2, L2)};

          double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
          double fac = kk[axis1] * kk[axis2] / ksquared * inv_volume;

          std::complex<double> &pos_psi_ijk = (*c_pos_psi)[i][j][k];

          result[i][j][k] += fac * pos_psi_ijk;
        }
  });
};

template <typename CIC>
void Borg2LPTModel<CIC>::lpt2_redshift_pos_ag(
    PhaseArrayRef &pos, PhaseArrayRef &vel, PhaseArrayRef &pos_ag,
    PhaseArrayRef &vel_ag, PhaseArrayRef &lctim) {
  Cosmology cosmo(cosmo_params);

  // this routine generates particle positions in redshift space
  // the code uses particle momenta p=a^2 dx/dt where x is the co-moving position
  // peculiar velocities are then given by v_pec = p/a

  // NOTE: Check coefficients
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
        [2]; // this factor is 1/H/a for velocities in [km/sec] an additional factor arises from momentum conversion

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

template <typename CIC>
template <typename PositionArray>
void Borg2LPTModel<CIC>::lpt2_density_obs_ag(
    PositionArray &pos, PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag,
    ArrayRef &B, size_t numParts) {
  double const nmean = double(c_N0*c_N1*c_N2)/(box_output.N0*box_output.N1*box_output.N2);

  typedef UninitializedArray<boost::multi_array<double, 3>> U_Array;

  if (ALWAYS_MPI(comm)) {
    // Allocate a temporary density field with extra planes for the
    // the projection leakage
    U_Array tmp_delta(out_mgr->extents_real(CIC::MPI_PLANE_LEAKAGE));

    density_exchange_planes_ag(
        comm, tmp_delta.get_array(), B, out_mgr, CIC::MPI_PLANE_LEAKAGE);
    array::fill(pos_ag, 0);
    CIC::adjoint(
        pos, tmp_delta.get_array(), pos_ag, L0, L1, L2, out_mgr->N0, out_mgr->N1, out_mgr->N2,
        typename CIC::Periodic_MPI(out_mgr->N0, out_mgr->N1, out_mgr->N2, comm), nmean, numParts);
  } else {
    // This is simple, no copy, no adjustment
    array::fill(pos_ag, 0);
    CIC::adjoint(
        pos, B, pos_ag, L0, L1, L2, out_mgr->N0, out_mgr->N1, out_mgr->N2, CIC_Tools::Periodic(out_mgr->N0, out_mgr->N1, out_mgr->N2),
        nmean, numParts);
  }

  array::fill(vel_ag, 0);
}

template <typename CIC>
void Borg2LPTModel<CIC>::lpt2_fwd_model_ag(
    PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, PhaseArrayRef &lctime,
    CArrayRef &DPSI) {
  ConsoleContext<LOG_DEBUG> ctx("BORG adjoint model (particles)");

  ///NOTE: ICs are generated at ai

  //N.) undo ICs
  lpt2_ic_ag(pos_ag, vel_ag, lctime);

  // RESULT is in AUX1

  if (c_deltao != 0) {
    array::fill(DPSI, 0);
    lo_mgr->degrade_complex(*mgr, *AUX1_p, DPSI);
  } else {
    fwrap(DPSI) = *AUX1_p;
  }
}

template <typename CIC>
void Borg2LPTModel<CIC>::adjointModelParticles(
    PhaseArrayRef &grad_pos, PhaseArrayRef &grad_vel) {
  //lpt2_fwd_model_ag(grad_pos, grad_vel, *lc_timing, gradient_delta);
  releaseParticles();
}

template <typename CIC>
void Borg2LPTModel<CIC>::adjointModel_v2(ModelInputAdjoint<3> gradient_delta) {
  ConsoleContext<LOG_DEBUG> ctx("BORG adjoint model");

  // This function computes the adjoint gradient in place. The adjoint gradient of the final density must be provided, in exchange
  // the adjoint gradient of the initial field is returned

  // introduce adjoint quantities
  // This must be allocated in two steps to avoid the implicit
  // zero initialization.
  size_t refPartNum = size_t(c_localN0 * c_N1 * c_N2 * partFactor);

  // gradient_delta may be empty (if for example we use other way to feed the adjoint gradients
  // directly to particle (e.g. velocity field)
  // if empty, we just ignore it and work with the current state of pos_ag,vel_ag

  u_pos_ag.reset();
  u_vel_ag.reset();

  u_pos_ag = std::make_shared<U_PArray>(extents[refPartNum][3]);
  u_vel_ag = std::make_shared<U_PArray>(extents[refPartNum][3]);
  auto &pos_ag = u_pos_ag->get_array();
  auto &vel_ag = u_vel_ag->get_array();
  auto &pos = u_pos->get_array();
  auto &vel = u_vel->get_array();

  // re-evaluate redshift distortions from forward run
  if (do_rsd) {
    ctx.print("doing redshift space distortions.");
    PhaseArrayRef &s_pos = u_s_pos->get_array();

    if (gradient_delta) {
      gradient_delta.setRequestedIO(PREFERRED_REAL);
      gradient_delta.needDestroyInput();

      ///work backwards from final to initial conditions
      //1.) undo CIC
      lpt2_density_obs_ag(
          s_pos, pos_ag, vel_ag, gradient_delta.getReal(),
          redshiftInfo.localNumParticlesAfter);
    }
    particle_undistribute(redshiftInfo, pos_ag);

    //2.) undo redshift distortions
    lpt2_redshift_pos_ag(pos, vel, pos_ag, vel_ag, *lc_timing);
  } else {
    // work backwards from final to initial conditions
    // 1.) undo CIC
    if (gradient_delta) {
      gradient_delta.setRequestedIO(PREFERRED_REAL);
      lpt2_density_obs_ag(
          pos, pos_ag, vel_ag, gradient_delta.getReal(),
          realInfo.localNumParticlesAfter);
    }
    particle_undistribute(
        realInfo, pos_ag, make_attribute_helper(Particles::vector(vel_ag)));
  }
}

template <typename CIC>
void Borg2LPTModel<CIC>::getAdjointModelOutput(
    ModelOutputAdjoint<3> gradient_delta) {
  auto &pos_ag = u_pos_ag->get_array();
  auto &vel_ag = u_vel_ag->get_array();

  gradient_delta.setRequestedIO(PREFERRED_FOURIER);

  lpt2_fwd_model_ag(
      pos_ag, vel_ag, *lc_timing, gradient_delta.getFourierOutput());

  clearAdjointGradient();
}

template <typename CIC>
void Borg2LPTModel<CIC>::clearAdjointGradient() {

  u_pos_ag.reset();
  u_vel_ag.reset();
}
