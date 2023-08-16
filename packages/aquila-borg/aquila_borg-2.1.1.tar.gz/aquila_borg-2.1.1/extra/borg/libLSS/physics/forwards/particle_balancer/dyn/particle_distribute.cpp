/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/particle_balancer/dyn/particle_distribute.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/cconfig.h"
#include <boost/multi_array.hpp>
#include <boost/format.hpp>
#include <functional>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/physics/forwards/particle_balancer/dyn/particle_distribute.hpp"

using namespace LibLSS;
using namespace LibLSS::AbstractParticles;

Attribute::~Attribute() {}

void LibLSS::dynamic_particle_redistribute(
    MPI_Communication *comm, BalanceInfo const &info,
    std::vector<std::shared_ptr<AbstractParticles::Attribute>> attrs) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  auto &part_idx = info.u_idx->get_array();

  // First we need to reorder the attributes to prepare for shipping.
  ctx.print("Reorder dynamical attributes");
  for (auto &a : attrs) {
    a->swap(part_idx, info.localNumParticlesBefore);
  }

  // Go through each attribute and send the adequate slice to the remote.
  std::list<MPICC_Request> reqSend, reqRecv;
  std::vector<std::shared_ptr<TemporaryAttribute>> all_tmp(
      attrs.size() * comm->size());

  ctx.print("Send each slice of attributes to the remote");
  for (auto &a : attrs) {
    for (int r = 0; r < comm->size(); r++) {
      if (info.numTransfer[r] != 0 && r != comm->rank()) {
        void *data = a->getArrayData(info.offsetSend[r]);
        ctx.format("  -> %d, num = %d", r, info.numTransfer[r]);
        reqSend.push_back(comm->Isend(
            data, a->multiplicity() * info.numTransfer[r], a->mpi_type(), r,
            0));
      }
    }
  }

  ctx.print("Recv each slice of attributes from the remote");
  for (size_t a = 0; a < attrs.size(); a++) {
    for (size_t r = 0; r < comm->size(); r++) {
      size_t idx = a * comm->size() + r;
      ctx.format("  <- %d, num = %d", r, info.numReceive[r]);
      if (info.numReceive[r] != 0 && r != comm->rank()) {
        auto tmp = attrs[a]->allocateTemporary(info.numReceive[r]);
        all_tmp[idx] = tmp;
        void *data = tmp->getData();
        reqRecv.push_back(comm->Irecv(
            data, attrs[a]->multiplicity() * info.numReceive[r],
            attrs[a]->mpi_type(), r, 0));
      }
    }
  }
  ctx.print("Waiting for transfer to complete");
  for (auto &w : reqRecv)
    w.wait();
  for (auto &w : reqSend)
    w.wait();
  // DONE!

  for (size_t a = 0; a < attrs.size(); a++) {
    for (size_t r = 0; r < comm->size(); r++) {
      size_t idx = a * comm->size() + r;
      if (all_tmp[idx])
        attrs[a]->copy_from_tmp_to(all_tmp[idx], info.offsetReceive[r]);
    }
  }

  for (auto &a : all_tmp)
    a.reset();
}
