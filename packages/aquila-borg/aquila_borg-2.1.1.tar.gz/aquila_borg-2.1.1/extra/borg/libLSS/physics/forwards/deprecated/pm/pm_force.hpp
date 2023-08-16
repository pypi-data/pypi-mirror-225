/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/deprecated/pm/pm_force.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

template <typename FIC, typename CIC>
template <int axis, bool accum, int sign, typename PotentialArray>
void BorgPMModel<FIC, CIC>::codelet_force(
    int i, FFTW_Real_Array_ref &g, PotentialArray &pot_plus,
    PotentialArray &pot_minus) {
  long N[3] = {f_N0, f_N1, f_N2};
  double i_d[3] = {sign * f_N0 / (unit_r0 * L0), sign * f_N1 / (unit_r0 * L1),
                   sign * f_N2 / (unit_r0 * L2)};

  typedef FFTW_Real_Array::index index_type;

#pragma omp parallel for collapse(2)
  for (long j = 0; j < f_N1; j++)
    for (long k = 0; k < f_N2; k++) {
      boost::array<index_type, 3> idxp = {i, j, k};
      boost::array<index_type, 3> idxm = {i, j, k};

      idxp[axis]++;
      idxm[axis]--;
      if (idxp[axis] >= N[axis])
        idxp[axis] -= N[axis];
      if (idxm[axis] < 0)
        idxm[axis] += N[axis];
      double value = -0.5 * (pot_plus(idxp) - pot_minus(idxm)) * i_d[axis];
      push_to<accum>::apply(g[i][j][k], value);
    }
}

template <typename FIC, typename CIC>
template <int axis, bool accum, int sign>
void BorgPMModel<FIC, CIC>::compute_force(
    FFTW_Real_Array_ref &g, FFTW_Real_Array_ref &pot) {
  ConsoleContext<LOG_DEBUG> ctx("force computation");

  // For all axis other than the first, it is easy
  if (axis != 0) {
#pragma omp parallel for
    for (long i = f_startN0; i < f_startN0 + f_localN0; i++)
      codelet_force<axis, accum, sign>(i, g, pot, pot);

    return;
  }

  ctx.print("Force axis-0: Handling traditional case");
#pragma omp parallel for
  for (long i = f_startN0 + 1; i < f_startN0 + f_localN0 - 1; i++)
    codelet_force<0, accum, sign>(i, g, pot, pot);

  // No real MPI here. Just do direct computation
  if (SKIP_MPI_FOR_SINGLE_NODE && f_localN0 == f_N0) {
    ctx.print("No MPI: finish off");
    codelet_force<0, accum, sign>(f_startN0, g, pot, pot);
    codelet_force<0, accum, sign>(f_startN0 + f_localN0 - 1, g, pot, pot);
    return;
  }

  // No force. No data. Nothing. Skip.
  if (f_localN0 == 0) {
    ctx.print("No plane living here: finish");
    return;
  }

  // Here we exchange with neighbours to be able to compute the gradient in this slice
  long f_N2real = force_mgr->N2real;
  int lower_0 = (f_startN0 + f_N0 - 1) % f_N0;
  int upper_0 = (f_startN0 + f_localN0) % f_N0;

  typedef Uninit_FFTW_Real_Array U_Array;
  typedef U_Array::array_type U_ArrayType;
  U_Array lower_pot_plane_recv_p(
      extents[range(lower_0, lower_0 + 1)][f_N1][f_N2real]);
  U_Array upper_pot_plane_recv_p(
      extents[range(upper_0, upper_0 + 1)][f_N1][f_N2real]);
  U_Array lower_pot_plane_send_p(
      extents[range(f_startN0, f_startN0 + 1)][f_N1][f_N2real]);
  U_Array upper_pot_plane_send_p(extents[range(
      f_startN0 + f_localN0 - 1, f_startN0 + f_localN0)][f_N1][f_N2real]);
  U_ArrayType &lower_pot_plane_recv = lower_pot_plane_recv_p.get_array(),
              lower_pot_plane_send = lower_pot_plane_send_p.get_array(),
              upper_pot_plane_recv = upper_pot_plane_recv_p.get_array(),
              upper_pot_plane_send = upper_pot_plane_send_p.get_array();

  MPI_Communication::Request lower_req_recv, upper_req_recv;
  MPI_Communication::Request lower_req_send, upper_req_send;

  ctx.print(
      format("Copy arrays to be sent (%d, %d)") % f_startN0 %
      (f_startN0 + f_localN0 - 1));

  copy_array_rv(lower_pot_plane_send[f_startN0], pot[f_startN0]);
  copy_array_rv(
      upper_pot_plane_send[f_startN0 + f_localN0 - 1],
      pot[f_startN0 + f_localN0 - 1]);

  ctx.print("Sending/Receiving");

  lower_req_send = comm->IsendT(
      lower_pot_plane_send.data(), lower_pot_plane_send.num_elements(),
      force_mgr->get_peer(lower_0), f_startN0);
  upper_req_send = comm->IsendT(
      upper_pot_plane_send.data(), upper_pot_plane_send.num_elements(),
      force_mgr->get_peer(upper_0), f_startN0 + f_localN0 - 1);

  lower_req_recv = comm->IrecvT(
      lower_pot_plane_recv.data(), lower_pot_plane_recv.num_elements(),
      force_mgr->get_peer(lower_0), lower_0);
  upper_req_recv = comm->IrecvT(
      upper_pot_plane_recv.data(), upper_pot_plane_recv.num_elements(),
      force_mgr->get_peer(upper_0), upper_0);

  ctx.print("I/O scheduled.");
  if (f_localN0 > 1) {

    lower_req_recv.wait();
    ctx.print(" * Handling lower_pot_plane_recv");
    codelet_force<0, accum, sign>(f_startN0, g, pot, lower_pot_plane_recv);

    upper_req_recv.wait();
    ctx.print(" * Handling upper_pot_plane_recv");
    codelet_force<0, accum, sign>(
        f_startN0 + f_localN0 - 1, g, upper_pot_plane_recv, pot);
    ctx.print("Done handling");
  } else {
    ctx.print(" * Degenerate case, f_localN0 == 1");
    lower_req_recv.wait();
    upper_req_recv.wait();
    codelet_force<0, accum, sign>(
        f_startN0, g, upper_pot_plane_recv, lower_pot_plane_recv);
  }
  lower_req_send.wait();
  upper_req_send.wait();
}
