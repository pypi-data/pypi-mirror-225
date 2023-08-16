/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/deprecated/pm/pm_grav.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/physics/forwards/pm/plane_xchg.hpp"

template <typename FIC, typename CIC>
template <typename PositionArray>
void BorgPMModel<FIC, CIC>::pm_grav_density(
    bool clear, const PositionArray &pos, size_t partNum,
    FFTW_Real_Array_ref &pot) {
  if (clear)
    array::fill(pot, 0);

  Console &cons = Console::instance();

  cons.print<LOG_DEBUG>(
      format("shape = %d,%d") % pos.shape()[0] % pos.shape()[1]);

  if (comm->size() > 1) {
    CIC::projection(
        pos, pot, L0, L1, L2, f_N0, f_N1, f_N2,
        typename CIC::Periodic_MPI(f_N0, f_N1, f_N2, comm),
        CIC_Tools::DefaultWeight(), partNum);
    // pot has MPI_PLANE_LEAKAGE extra planes. They have to be sent to the adequate nodes.
    pm_exchange_planes<true>(pot, force_mgr);
  } else {
    CIC::projection(
        pos, pot, L0, L1, L2, f_N0, f_N1, f_N2,
        CIC_Tools::Periodic(f_N0, f_N1, f_N2), CIC_Tools::DefaultWeight(),
        partNum);
  }
}

template <typename FIC, typename CIC>
template <typename OutPlaneArray, typename InPlaneArray>
void BorgPMModel<FIC, CIC>::pm_exchange_planes_ag(
    OutPlaneArray &loc_density, InPlaneArray &global_density,
    std::unique_ptr<DFT_Manager> &d_mgr) {
  density_exchange_planes_ag(
      comm, loc_density, global_density, d_mgr, CIC::MPI_PLANE_LEAKAGE);
}

template <typename FIC, typename CIC>
template <bool accum, typename PlaneArray>
void BorgPMModel<FIC, CIC>::pm_exchange_planes(
    PlaneArray &density, std::unique_ptr<DFT_Manager> &d_mgr,
    int extra_planes) {
  density_exchange_planes<accum>(comm, density, d_mgr, extra_planes);
}

template <typename FIC, typename CIC>
void BorgPMModel<FIC, CIC>::pm_gravpot(FFTW_Real_Array_ref &pot) {
  ConsoleContext<LOG_DEBUG> ctx("gravitational solver");
  double nmean = CosmoTool::cube(double(ss_factor) / f_factor);

  //transform density to F-space
  CArray &f_AUX0 = *f_AUX0_p;
  force_mgr->execute_r2c(f_analysis_plan, pot.data(), f_AUX0.data());
  double normphi = 3. / 2. * cosmo_params.omega_m / double(f_N0 * f_N1 * f_N2) *
                   (unit_r0 * unit_r0) / nmean;

#ifdef ARES_MPI_FFTW
#  pragma omp parallel for
  for (long i = f_startN1; i < f_startN1 + f_localN1; i++) {
    double sin21 = sin2K[1][i];
    for (long j = 0; j < f_N0; j++) {
      double sin20 = sin2K[0][j];
      for (long k = 0; k < f_N2_HC; k++) {
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
#endif

  force_mgr->execute_c2r(f_synthesis_plan, f_AUX0.data(), pot.data());
}
