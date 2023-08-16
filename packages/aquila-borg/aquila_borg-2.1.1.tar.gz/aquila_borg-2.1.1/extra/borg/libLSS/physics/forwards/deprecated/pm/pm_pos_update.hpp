/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/deprecated/pm/pm_pos_update.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

template <typename FIC, typename CIC>
void BorgPMModel<FIC, CIC>::pm_pos_update(
    TapeArrayRef &pos, TapeArrayRef &vel, IdxTapeArrayRef &part_idx, double dtr,
    int istep) {
  ConsoleContext<LOG_DEBUG> ctx("pos update");
  typedef TapeArrayRef::reference::reference TapeElt;
  typedef IdxTapeArrayRef::reference::reference IdxTapeElt;

#pragma omp parallel for
  for (long i = 0; i < local_usedParticles[istep]; i++) {
    TapeElt prev_loc_pos = pos[istep][i];
    TapeElt prev_loc_vel = vel[istep + 1][i];
    TapeElt loc_pos = pos[istep + 1][i];
    double x = prev_loc_pos[0] + prev_loc_vel[0] * dtr;
    double y = prev_loc_pos[1] + prev_loc_vel[1] * dtr;
    double z = prev_loc_pos[2] + prev_loc_vel[2] * dtr;

    loc_pos[0] = periodic_fix(x, 0., L0);
    loc_pos[1] = periodic_fix(y, 0., L1);
    loc_pos[2] = periodic_fix(z, 0., L2);
  }

  // No MPI: exit now to save CPU cycles
  if (SKIP_MPI_FOR_SINGLE_NODE && comm->size() == 1) {
    local_usedParticles[istep + 1] = local_usedParticles[istep];
    return;
  }
}

template <typename FIC, typename CIC>
template <bool doVel, typename Projector>
void BorgPMModel<FIC, CIC>::pm_distribute_particles(
    std::unique_ptr<DFT_Manager> &dmgr, int istep, TapeArrayRef &pos,
    TapeArrayRef &vel, IdxTapeArrayRef &part_idx, size_t inParticles) {
  ConsoleContext<LOG_DEBUG> ctx("pre pm_distribute_particles");

  auto in_pos = pos[istep];
  // One pick the first time step because we need an argument. But in practice it is not used
  auto io_part_idx = part_idx[istep];
  auto io_numTransferStep = numTransferStep[istep];
  auto io_numReceiveStep = numReceiveStep[istep];
  auto io_offsetReceiveStep = offsetReceiveStep[istep];
  auto io_offsetSendStep = offsetSendStep[istep];

  if (doVel) {
    auto in_vel = vel[istep];
    particle_redistribute(
        comm, in_pos, io_part_idx, inParticles, local_usedParticles[istep],
        io_numTransferStep, io_numReceiveStep, io_offsetReceiveStep,
        io_offsetSendStep, typename Projector::Distribution(dmgr, L0),
        make_attribute_helper(
            Particles::vector(in_vel), Particles::scalar(*lagrangian_id)));
  } else {
    particle_redistribute(
        comm, in_pos, io_part_idx, inParticles, local_usedParticles[istep],
        io_numTransferStep, io_numReceiveStep, io_offsetReceiveStep,
        io_offsetSendStep, typename Projector::Distribution(dmgr, L0),
        make_attribute_helper(Particles::scalar(*lagrangian_id))

    );
  }
}

// This function do not compute a gradient per-se. But it redistributes the pos_ag and vel_ag on MPI nodes according to the earlier
// forward reshuffling.
// Input state:
//   pos_ag, vel_ag must have local_usedParticles[istep] elements
//   pos, vel, part_idx are the full tape arrays of this node
template <typename FIC, typename CIC>
template <bool doVel>
void BorgPMModel<FIC, CIC>::pm_distribute_particles_ag(
    int istep, PhaseArrayRef &pos_ag, PhaseArrayRef &vel_ag, TapeArrayRef &pos,
    TapeArrayRef &vel, IdxTapeArrayRef &part_idx) {
  auto io_part_idx = part_idx[istep];
  auto numTransfer = numTransferStep[istep];
  auto numReceive = numReceiveStep[istep];
  auto offsetReceive = offsetReceiveStep[istep];
  auto offsetSend = offsetSendStep[istep];
  size_t target_usedParticles =
      istep == 0 ? (c_localN0 * c_N1 * c_N2) : (local_usedParticles[istep - 1]);

  if (doVel) {
    particle_undistribute(
        comm, pos_ag, io_part_idx, local_usedParticles[istep],
        target_usedParticles, numTransfer, numReceive, offsetReceive,
        offsetSend, make_attribute_helper(Particles::vector(vel_ag)));
  } else {
    particle_undistribute(
        comm, pos_ag, io_part_idx, local_usedParticles[istep],
        target_usedParticles, numTransfer, numReceive, offsetReceive,
        offsetSend);
  }
}
