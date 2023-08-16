/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/deprecated/pm/pm_vel_update.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

template <typename FIC, typename CIC>
template <typename TapePos, typename TapeVel, typename Grav>
void BorgPMModel<FIC, CIC>::codelet_vel_update(
    int axis, int istep, double dtv, int i_g_plus, TapePos &pos, TapeVel &vel,
    Grav &g_plus, Grav &g) {
  double i_d0 = f_N0 / L0;
  double i_d1 = f_N1 / L1;
  double i_d2 = f_N2 / L2;

  long Np = local_usedParticles[istep];

  typename TapeVel::reference vel_next = vel[istep + 1];
  typename TapePos::reference pos_current = pos[istep];
  typename TapeVel::reference vel_current = vel[istep];

#pragma omp parallel for schedule(static)
  for (long i = 0; i < Np; i++) {
    typename TapePos::reference::reference i_pos = pos_current[i];

    double x = i_pos[0] * i_d0;
    double y = i_pos[1] * i_d1;
    double z = i_pos[2] * i_d2;

    int ix = (int)std::floor(x);
    int iy = (int)std::floor(y);
    int iz = (int)std::floor(z);

    int jx = ix + 1; if (jx >= f_N0) jx -= f_N0;
    int jy = iy + 1; if (jy >= f_N1) jy -= f_N1;
    int jz = iz + 1; if (jz >= f_N2) jz -= f_N2;

    double rx = (x - ix);
    double ry = (y - iy);
    double rz = (z - iz);

    double qx = 1 - rx;
    double qy = 1 - ry;
    double qz = 1 - rz;

    Grav &g1 = (jx == i_g_plus) ? g_plus : g;

    auto &v1 = vel_next[i][axis];
    auto &v0 = vel_current[i][axis];

    double force =
        g[ix][iy][iz] * qx * qy * qz + g[ix][iy][jz] * qx * qy * rz +
        g[ix][jy][iz] * qx * ry * qz + g[ix][jy][jz] * qx * ry * rz +
        g1[jx][iy][iz] * rx * qy * qz + g1[jx][iy][jz] * rx * qy * rz +
        g1[jx][jy][iz] * rx * ry * qz + g1[jx][jy][jz] * rx * ry * rz;

    v1 = v0 + force * dtv;
  }
}

template <typename FIC, typename CIC>
void BorgPMModel<FIC, CIC>::pm_vel_update(
    TapeArrayRef &pos, TapeArrayRef &vel, IdxTapeArrayRef &part_idx, double dtv,
    int istep) {
  ConsoleContext<LOG_DEBUG> ctx("vel update");

  typedef Uninit_FFTW_Real_Array U_Array;
  long f_N2real = force_mgr->N2real;
  long lower_0 = (f_startN0 + f_N0 - 1) % f_N0;
  long upper_0 = (f_startN0 + f_localN0) % f_N0;

  U_Array g_p(force_mgr->extents_real(), force_mgr->allocator_real);
  U_Array pot_p(
      force_mgr->extents_real(CIC::MPI_PLANE_LEAKAGE),
      force_mgr->allocator_real);
  U_Array g_plus_p(extents[range(upper_0, upper_0 + 1)][f_N1][f_N2real]);
  U_Array g_minus_send_p(
      extents[range(f_startN0, f_startN0 + 1)][f_N1][f_N2real]);
  U_Array::array_type &g = g_p.get_array();
  U_Array::array_type &pot = pot_p.get_array();
  U_Array::array_type &g_plus = g_plus_p.get_array();
  U_Array::array_type &g_minus_send = g_minus_send_p.get_array();
  MPI_Communication::Request req_minus_recv, req_plus_recv, req_minus_send,
      req_plus_send;
  TapeArrayRef::index_gen indices;
  typedef TapeArrayRef::index_range range;

  //estimate gravitational potential
  ctx.print(format("Projecting %ld particles") % local_usedParticles[istep]);
  pm_grav_density(true, pos[istep], local_usedParticles[istep], pot);
  pm_gravpot(pot);

  //calculate forces and update velocities
  for (int axis = 0; axis < 3; axis++) {
    switch (axis) {
    case 0:
      compute_force<0, false, 1>(g, pot);
      break;
    case 1:
      compute_force<1, false, 1>(g, pot);
      break;
    case 2:
      compute_force<2, false, 1>(g, pot);
      break;
    }

    if (f_localN0 == f_N0) {
      codelet_vel_update(axis, istep, dtv, -1, pos, vel, g, g);
    } else {
      ctx.print("Exchange one force plane");
      // This grabs and distribute the extra plane required for the interpolation at the edge.
      req_plus_recv = comm->IrecvT(
          g_plus.data(), g_plus.num_elements(), force_mgr->get_peer(upper_0),
          upper_0);
      copy_array_rv(g_minus_send[f_startN0], g[f_startN0], false);
      req_minus_send = comm->IsendT(
          g_minus_send.data(), g_minus_send.num_elements(),
          force_mgr->get_peer(lower_0), f_startN0);
      req_plus_recv.wait();
      // Done receiving we can do computations

      ctx.print("Computing accelerations");
      codelet_vel_update(
          axis, istep, dtv, (f_startN0 + f_localN0) % f_N0, pos, vel, g_plus,
          g);

      // Ensure the sending is done
      req_minus_send.wait();
    }
  }
}
