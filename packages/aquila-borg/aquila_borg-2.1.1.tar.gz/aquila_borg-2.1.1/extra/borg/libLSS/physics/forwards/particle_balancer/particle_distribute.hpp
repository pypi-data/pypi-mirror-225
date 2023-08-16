/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/particle_balancer/particle_distribute.hpp
    Copyright (C) 2017-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PARTICLE_DISTRIBUTE_HPP
#define __LIBLSS_PARTICLE_DISTRIBUTE_HPP

#include <boost/multi_array.hpp>
#include <boost/format.hpp>
#include <functional>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/uninitialized_type.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/physics/forwards/particle_balancer/attributes.hpp"
#include "libLSS/physics/forwards/particle_balancer/part_swapper.hpp"

namespace LibLSS {

  static const bool ULTRA_CHECK = false;

  template <typename PartIdxArray>
  inline void initIndexes(PartIdxArray part_idx, size_t numParts) {
    typename PartIdxArray::index_gen i_gen;
    typedef typename PartIdxArray::index_range i_range;
    // initialize array with a range 0, 1, 2, 3, 4, ... numParts
    copy_array_rv(
        part_idx[i_gen[i_range(0, numParts)]],
        b_fused_idx<long, 1>(boost::lambda::_1));
  }

  // This is an example of an integrated storage for all the ancillary parameters required
  // by the particle redistribute algorithm
  struct BalanceInfo {
    typedef boost::multi_array<ssize_t, 1> IdxArray;

    IdxArray offsetReceive, offsetSend, numTransfer, numReceive;
    UninitializedArray<IdxArray> *u_idx;
    size_t localNumParticlesBefore, localNumParticlesAfter;
    MPI_Communication *comm;

    BalanceInfo() : u_idx(0), comm(0) {}

    void allocate(MPI_Communication *newComm, size_t partNum) {
      LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
      auto extComm = boost::extents[newComm->size()];

      comm = newComm;
      clear();
      u_idx = new UninitializedArray<IdxArray>(boost::extents[partNum]);
      initIndexes(u_idx->get_array(), partNum);
      offsetReceive.resize(extComm);
      offsetSend.resize(extComm);
      numTransfer.resize(extComm);
      numReceive.resize(extComm);
    }

    void clear() {
      if (u_idx != 0) {
        delete u_idx;
        u_idx = 0;
      }
    }
  };

  template <
      typename ParticleArray, typename IndexArray, typename CountArray,
      typename OffsetArray, typename ParticleSelector,
      typename AuxiliaryAttributes = NoAuxiliaryAttributes>
  void particle_redistribute(
      MPI_Communication *comm, ParticleArray &in_pos, IndexArray &part_idx,
      size_t inParticles, size_t &outParticles, CountArray &numTransferStep,
      CountArray &numReceiveStep, OffsetArray &offsetReceiveStep,
      OffsetArray &offsetSendStep, ParticleSelector selector,
      AuxiliaryAttributes attrs = AuxiliaryAttributes()) {
    ConsoleContext<LOG_DEBUG> ctx("particle distribution");
    typedef boost::multi_array<long, 1> LongArray;

    using boost::extents;
    using boost::format;
    using boost::lambda::_1;
    typedef LongArray::index_range range;
    LongArray::index_gen indices;
    typedef typename ParticleArray::reference PosElt;
    typedef typename IndexArray::reference IdxTapeElt;
    typedef LongArray::element LongElt;
    typedef size_t CommT;
    CommT thisRank = comm->rank();
    CommT commSize = comm->size();


    if (commSize == 1) {
      outParticles = inParticles;
      return;
    }
    ParticleSwapper<ParticleArray &, AuxiliaryAttributes> swapper(
        in_pos, attrs);

    LongArray numTransfer(extents[commSize]);
    LongArray numReceive(extents[commSize]);
    LongArray offsetTransfer(extents[1 + commSize]);
    LongArray offsetIncoming(extents[1 + commSize]);
    LongArray offsetRangeTransfer(extents[1 + commSize]);

    LongElt totalIncoming;
    LongElt baseOffset;

    RequestArray reqRecv_pos(extents[commSize]), reqSend_pos(extents[commSize]);
    RequestArray reqRecv_attr(
        extents[AuxiliaryAttributes::numAttributes * commSize]),
        reqSend_attr(extents[AuxiliaryAttributes::numAttributes * commSize]);

    ctx.format("Computing particles to be exchanged, (inParticles=%d)", inParticles);
    // There is something to parallelize here
    for (size_t i = 0; i < inParticles; i++) {
      PosElt loc_pos = in_pos[i];
      numTransfer[selector(loc_pos, attrs.tuple_get(i))]++;
    }

    // MPI: do particle exchange to restablish localities
    ctx.print("all2all...");
    comm->all2allT(numTransfer.data(), 1, numReceive.data(), 1);
    numReceive[thisRank] = 0;
    ctx.print("Done");

    // Here we do sanity check, if there is a memory error
    // we must check this hear and have all nodes stop operations
    // together
    size_t totalParticles[2] = {inParticles, in_pos.shape()[0]};
    for (CommT i = 0; i < commSize; i++) {
      if (i == thisRank)
        continue;
      totalParticles[0] += numReceive[i];
      totalParticles[0] -= numTransfer[i];
    }
    ctx.print(boost::format("totalParticles = %ld") % totalParticles[0]);

    boost::multi_array<size_t, 1> totalArray(boost::extents[2 * comm->size()]);
    comm->all_gather_t(totalParticles, 2, totalArray.data(), 2);

    for (CommT i = 0; i < commSize; i++) {
      ctx.print(
          boost::format("Node %d: totalParticles = %ld / %ld") % i %
          totalArray[2 * i] % totalArray[2 * i + 1]);
      if (totalArray[2 * i] >= totalArray[2 * i + 1] &&
          totalArray[2 * i] != 0) {
        // This is thrown on all nodes
        error_helper<ErrorLoadBalance>(
            "Not enough particles per node. Increase particle alloc factor");
      }
    }

    for (CommT i = 0; i < commSize; i++)
      ctx.print(
          format(" - peer=%d, recv = %ld, send = %ld ") % i % numReceive[i] %
          numTransfer[i]);

    // Figure out the offsets of in the buffers that will be transferred
    // to other nodes
    offsetTransfer[0] = 0;
    offsetIncoming[0] = 0;
    for (CommT r = 1; r <= commSize; r++) {
      offsetTransfer[r] = offsetTransfer[r - 1] + numTransfer[r - 1];
      offsetIncoming[r] = offsetIncoming[r - 1] + numReceive[r - 1];
    }
    for (CommT r = 0; r < thisRank; r++) {
      offsetTransfer[r] += numTransfer[thisRank];
    }

    // Adjust the amount to transfer for this node
    // The positions for the particles going to this node is zero to promote locality
    offsetTransfer[thisRank] = 0;
    totalIncoming = offsetIncoming[commSize];
    offsetRangeTransfer = offsetTransfer;

    for (CommT i = 0; i < commSize; i++) {
      if (numTransfer[i] != 0)
        ctx.print(
            format(" - peer=%d, offsetIncoming = %ld, offsetTransfer = "
                   "[%ld,%ld]") %
            i % offsetIncoming[i] % offsetTransfer[i] %
            (offsetTransfer[i] + numTransfer[i]));
    }

    // Now reorder them to push them for transfer
    {
      ConsoleContext<LOG_DEBUG> loc_ctx("sorting particles");
      LongElt i = 0;
      size_t doneComm = 0;

      for (CommT j = 0; j < commSize; j++) {
        if (numTransfer[j] == 0)
          doneComm++;
      }

      while (doneComm != commSize) {
        PosElt loc_pos = in_pos[i];

        LongElt node = selector(loc_pos, attrs.tuple_get(i));
        LongElt minOffsetNode = offsetRangeTransfer[node];
        LongElt maxOffsetNode = minOffsetNode + numTransfer[node];

        if (minOffsetNode <= i && maxOffsetNode > i) {
          // Particle is already located where it should be.
          i++;
        } else {
          IdxTapeElt loc_idx = part_idx[i];
          // Particle is not in place. Move it to its bin
          LongElt offset = offsetTransfer[node];
          IdxTapeElt target_idx = part_idx[offset];

          swapper.do_swap(offset, i);
          std::swap(loc_idx, target_idx);
          // now the particle in i is different and not yet processed
        }

        // Increase occupation number
        offsetTransfer[node]++;

        // If we are full mark the comm as done
        if (offsetTransfer[node] == maxOffsetNode)
          doneComm++;
      }
    }

    {
      typedef UninitializedArray<boost::multi_array<double, 2>> U_PhaseArray;
      U_PhaseArray posRecv_p(extents[totalIncoming][3]);
      U_PhaseArray::array_type &posRecv = posRecv_p.get_array();
      // Obtain a new set of arrays holding all the attributes.
      // These are temporary arrays for a max of totalIncoming.
      auto temp_attrs = swapper.allocateTemporary(totalIncoming);

      ctx.print(format("Exchanging particles (bufsize = %d)") % totalIncoming);

      for (CommT i = 0; i < commSize; i++) {
        if (i == thisRank || numTransfer[i] == 0)
          continue;
        ctx.print(format(" -> %d: %d particles (offset %d)") % i % numTransfer[i] % offsetRangeTransfer[i]);
        // First send particle positions
        reqSend_pos[i] = comm->IsendT(
            &in_pos[offsetRangeTransfer[i]][0], 3 * numTransfer[i], i, 0);
        // Now send all the other attributes.
        for (size_t a_id = 0; a_id < AuxiliaryAttributes::numAttributes;
             a_id++) {
          ctx.print(format(" -> %d: sending attribute %d") % i % a_id);
          reqSend_attr[i + a_id * commSize] = comm->Isend(
              swapper.getArrayData(a_id, offsetRangeTransfer[i]),
              numTransfer[i],
              swapper.mpi_type(a_id), // use the proper MPI type here
              i, a_id + 1);
        }
      }
      for (CommT i = 0; i < commSize; i++) {
        if (i == thisRank || numReceive[i] == 0)
          continue;
        ctx.print(format(" <- %d: %d particles (offset %d)") % i % numReceive[i] % offsetIncoming[i]);
        reqRecv_pos[i] = comm->IrecvT(
            posRecv.data() + 3 * offsetIncoming[i], 3 * numReceive[i], i, 0);
        for (size_t a_id = 0; a_id < AuxiliaryAttributes::numAttributes;
             a_id++) {
          ctx.print(
              format(" <- %d: receiving attribute %d, buffer %p, offset %d") %
              i % a_id % temp_attrs.getArrayData(a_id, 0) % offsetIncoming[i]);
          reqRecv_attr[i + a_id * commSize] = comm->Irecv(
              temp_attrs.getArrayData(a_id, offsetIncoming[i]), numReceive[i],
              temp_attrs.mpi_type(a_id), // use the proper MPI type here
              i, a_id + 1);
        }
      }

      // Now we ensure that all data in the output queue have been sent so that
      // we can reuse the buffer
      for (CommT i = 0; i < commSize; i++) {
        if (i == thisRank)
          continue;

        if (numTransfer[i] > 0) {
          reqSend_pos[i].wait();
          for (size_t a_id = 0; a_id < AuxiliaryAttributes::numAttributes;
               a_id++)
            reqSend_attr[i + a_id * commSize].wait();
        }
      }
      ctx.print("Done sent");

      baseOffset = numTransfer[thisRank];

      for (CommT i = 0; i < commSize; i++) {
        if (i == thisRank)
          continue;

        if (numReceive[i] > 0) {
          reqRecv_pos[i].wait();
          for (size_t a_id = 0; a_id < AuxiliaryAttributes::numAttributes;
               a_id++)
            reqRecv_attr[i + a_id * commSize].wait();

          size_t shape0 = in_pos.shape()[0];
          // Put the particles in place now that the buffer is unused
          for (LongElt j = 0; j < numReceive[i]; j++) {

            swapper.copy_in_pos(baseOffset, posRecv, offsetIncoming[i] + j);
            swapper.copy_in_all_attrs(
                baseOffset, temp_attrs, offsetIncoming[i] + j);

            baseOffset++;
            if (baseOffset == shape0) {
              error_helper<ErrorBadState>(
                  "Invalid state. Not enough particles per node. Increase "
                  "particle alloc factor");
            }
          }
        }
      }

      ctx.print("Done recv");

      outParticles = baseOffset;

      if (ULTRA_CHECK) {
        for (long i = 0; i < baseOffset; i++) {
          Console::instance().c_assert(
              selector(in_pos[i], attrs.tuple_get(i)) == comm->rank(), "Incorrect node");
        }
      }
      ctx.print(
          format("New number of particles on this node: %ld / max = %ld") %
          outParticles % in_pos.shape()[0]);

      LibLSS::copy_array(numTransferStep, numTransfer);
      LibLSS::copy_array(numReceiveStep, numReceive);

      LibLSS::copy_array(
          offsetReceiveStep,
          b_fused<long>(offsetIncoming, _1 + numTransfer[thisRank]));
      LibLSS::copy_array(offsetSendStep, offsetRangeTransfer);
    }
  }

  template <
      typename ParticleArray, typename IndexArray, typename CountArray,
      typename OffsetArray,
      typename AuxiliaryAttributes = NoAuxiliaryAttributes>
  void particle_undistribute(
      MPI_Communication *comm, ParticleArray &pos_ag, IndexArray &part_idx,
      size_t inParticles, size_t target_usedParticles, CountArray &numTransfer,
      CountArray &numReceive, OffsetArray &offsetReceive,
      OffsetArray &offsetSend,
      AuxiliaryAttributes attrs = AuxiliaryAttributes()) {
    ConsoleContext<LOG_DEBUG> ctx("distribute_particles_ag");

    using boost::extents;
    using boost::format;
    typedef boost::multi_array<long, 1> LongArray;
    typedef LongArray::element LongT;
    typedef LongArray::index_range range;
    using boost::lambda::_1;

    long thisRank = comm->rank();
    long commSize = comm->size();

    if (commSize == 1) {
      return;
    }

    typedef ParticleSwapper<ParticleArray &, AuxiliaryAttributes> Swapper;
    Swapper swapper(pos_ag, attrs);

    typename IndexArray::index_gen indices;

    // Step == 0 is very special. It has two boundary: the input to the integrator and the output of IC generation.
    // Distribution occurs just after IC generation, technically that's really the
    // input at istep==0
    // but when istep==0 we want the redistributed particles as they were for IC
    // generation.

    // Reserve some space for request ids
    RequestArray reqRecv_pos(extents[commSize]), reqSend_pos(extents[commSize]);
    RequestArray reqSend_attr(
        extents[AuxiliaryAttributes::numAttributes * commSize]),
        reqRecv_attr(extents[AuxiliaryAttributes::numAttributes * commSize]);

    // Schedule exchanges with other nodes for AG data
    for (long i = 0; i < commSize; i++) {
      if (i == thisRank)
        continue;

      LongT offs = offsetReceive[i];

      // Received becomes send with AG
      ctx.print(
          format(
              "Schedule send with ofs=%d to comm=%d (pos_ag_len=%d len=%d)") %
          offs % i % pos_ag.shape()[0] % numReceive[i]);
      if (numReceive[i] > 0) {
        reqSend_pos[i] =
            comm->IsendT(&pos_ag[offs][0], 3 * numReceive[i], i, 0);
        for (size_t a_id = 0; a_id < AuxiliaryAttributes::numAttributes;
             a_id++) {
          reqSend_attr[i + a_id * commSize] = comm->Isend(
              attrs.getArrayData(a_id, offs), numReceive[i],
              attrs.mpi_type(a_id), // use the proper MPI type here
              i, a_id + 1);
        }
      }
    }

    ctx.print(
        format("send scheduled, current_parts = %d, balance = %d") %
        inParticles % (long)(target_usedParticles - inParticles));

    {
      typedef UninitializedArray<boost::multi_array<double, 2>> U_PhaseArray;
      LongT refOffset = numTransfer[thisRank];
      // Number of particles to be exchanged. We do not allocate too much here.
      LongT exchange_usedParticles = target_usedParticles - refOffset;

      ctx.print(
          format("Number of parts to reexchange = %d (refOffset = %d)") %
          exchange_usedParticles % refOffset);

      // Create temporary buffer for receiving incoming data
      U_PhaseArray pos_ag_recv_p(extents[exchange_usedParticles][3]);
      U_PhaseArray::array_type &pos_ag_recv = pos_ag_recv_p.get_array();
      auto temp_attrs = swapper.allocateTemporary(exchange_usedParticles);

      for (long i = 0; i < commSize; i++) {
        if (i == thisRank)
          continue;

        long offs = offsetSend[i] - refOffset;

        ctx.print(
            format("Schedule recv with ofs=%d from comm=%d (len=%d)") % offs %
            i % numTransfer[i]);
        if (numTransfer[i] > 0) {
          reqRecv_pos[i] =
              comm->IrecvT(&pos_ag_recv[offs][0], 3 * numTransfer[i], i, 0);
          for (size_t a_id = 0; a_id < AuxiliaryAttributes::numAttributes;
               a_id++) {
            reqRecv_attr[i + a_id * commSize] = comm->Irecv(
                temp_attrs.getArrayData(a_id, offs), numTransfer[i],
                temp_attrs.mpi_type(a_id), i, a_id + 1);
          }
        }
      }
      ctx.print("Scheduled");

      // Now wait for all send to settle
      for (long i = 0; i < commSize; i++) {
        if (i == thisRank)
          continue;

        if (numReceive[i] > 0) {
          reqSend_pos[i].wait();
          for (size_t a_id = 0; a_id < AuxiliaryAttributes::numAttributes;
               a_id++)
            reqSend_attr[i + a_id * commSize].wait();
        }
      }

      ctx.print("IO done. Reshuffle");

      // All data sent, it is safe to modify now

      // Now handle recvs
      for (long i = 0; i < commSize; i++) {
        if (i == thisRank)
          continue;

        if (numTransfer[i] == 0)
          continue;

        reqRecv_pos[i].wait();
        for (size_t a_id = 0; a_id < AuxiliaryAttributes::numAttributes; a_id++)
          reqRecv_attr[i + a_id * commSize].wait();

        long offs = offsetSend[i] - refOffset;

        ctx.print(
            format("(rank=%d) Copying phase info to ofs=%d") % i %
            offsetSend[i]);

        range range_output =
            offsetSend[i] <= range() < (offsetSend[i] + numTransfer[i]);
        range range_input = offs <= range() < (offs + numTransfer[i]);
        auto indices_input = indices[range_input][range()];
        auto indices_output = indices[range_output][range()];

        // Reposition incoming data in the original buffer
        copy_array_rv(
            // extract the slice for the given node
            pos_ag[indices_output],
            // original data in the recv buffer
            pos_ag_recv[indices_input]);

#pragma omp parallel for
        for (size_t k = 0; k < numTransfer[i]; k++) {
          // This should be extremely simple when optimized by compiler.
          // Basically a set of assignment from the arrays in temp_attrs to
          // the target arrays in swapper. No loop. Nothing.
          swapper.copy_in_all_attrs(k + offsetSend[i], temp_attrs, k + offs);
        }
      }

      ctx.print(
          boost::format("reorder particles (target=%ld)") %
          target_usedParticles);

      array::reorder(
          part_idx[indices[range(0, target_usedParticles)]],
          std::bind(
              &Swapper::do_swap, &swapper, std::placeholders::_1,
              std::placeholders::_2));
    }
  }

  template <
      typename ParticleArray, typename ParticleSelector,
      typename AuxiliaryAttributes = NoAuxiliaryAttributes>
  void particle_redistribute(
      BalanceInfo &info, ParticleArray &in_pos, ParticleSelector selector,
      AuxiliaryAttributes aux = AuxiliaryAttributes()) {
    particle_redistribute(
        info.comm, in_pos, info.u_idx->get_array(),
        info.localNumParticlesBefore, info.localNumParticlesAfter,
        info.numTransfer, info.numReceive, info.offsetReceive, info.offsetSend,
        selector, aux);
  }

  template <
      typename ParticleArray,
      typename AuxiliaryAttributes = NoAuxiliaryAttributes>
  void particle_undistribute(
      BalanceInfo &info, ParticleArray &pos_ag,
      AuxiliaryAttributes aux = AuxiliaryAttributes()) {
    particle_undistribute(
        info.comm, pos_ag, info.u_idx->get_array(), info.localNumParticlesAfter,
        info.localNumParticlesBefore, info.numTransfer, info.numReceive,
        info.offsetReceive, info.offsetSend, aux);
  }

} // namespace LibLSS

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2017-2020
