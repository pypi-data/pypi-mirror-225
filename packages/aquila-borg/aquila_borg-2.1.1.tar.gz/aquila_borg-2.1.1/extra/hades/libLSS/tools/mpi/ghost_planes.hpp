/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/tools/mpi/ghost_planes.hpp
    Copyright (C) 2018-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_TOOLS_MPI_GHOST_PLANES_HPP
#  define __LIBLSS_TOOLS_MPI_GHOST_PLANES_HPP

#  include <map>
#  include <memory>
#  include "libLSS/tools/uninitialized_type.hpp"
#  include "libLSS/mpi/generic_mpi.hpp"
#  include "libLSS/tools/array_tools.hpp"
#  include "libLSS/tools/string_tools.hpp"
#  include "libLSS/samplers/core/types_samplers.hpp"

namespace LibLSS {

  /**
   * This class provides some types to abbreviate the long array specification
   * for ghost planes.
   */
  template <typename T, size_t Nd>
  struct GhostPlaneTypes {
    typedef boost::multi_array_ref<T, Nd> ArrayType;
    typedef UninitializedArray<ArrayType> U_ArrayType;

    typedef std::map<size_t, std::shared_ptr<U_ArrayType>> MapGhosts;
  };

  /**
   * @file
   * This enumeration allows to choose between different kind of "ghosts".
   */
  enum GhostMethod {
    GHOST_COPY, ///< in synchronize mode, the plane is copied. In AG mode, it is accumulated.
    GHOST_ACCUMULATE ///< in synchronize mode, the plane is accumulated. In AG mode, it is copied.
  };

  /**
  * This class handles the generic problems of ghost planes management with MPI.
  * The concept of ghost planes (and ghost particles in another module), comes
  * from the distinction of which MPI task owns the plane and which task needs
  * the plane to do further computation. A ghost plane is not designed to be an
  * "active" plane on the node that needs it. Though there is a slight variant
  * that may allow such things at the cost of a final synchronization.
  *
  * The work flow of using ghostplanes is the following:
  *   GhostPlanes object creation
  *   call setup method to indicate what are the provided data and requirements
  *   do stuff
  *   call synchronize before needing the ghost planes
  *   use the ghost planes with getPlane()
  *   Repeat synchronize if needed
  *
  * There is an adjoint gradient variant of the synchronization step which
  * does sum reduction of the adjoint gradient arrays corresponding to the
  * ghost planes.
  *
  */
  template <typename T, size_t Nd>
  struct GhostPlanes : GhostPlaneTypes<T, Nd> {
    typedef GhostPlaneTypes<T, Nd> super;
    typedef typename super::ArrayType ArrayType;
    typedef typename super::U_ArrayType U_ArrayType;
    typedef typename super::MapGhosts MapGhosts;

  private:
    static constexpr bool CHECK_DIMENSIONS = true;
    static constexpr bool ULTRA_VERBOSE = false;
    MPI_Communication *comm;
    MapGhosts ghosts, ag_ghosts;
    size_t maxPlaneId;
    std::map<size_t, size_t> plane_peer;
    std::array<size_t, Nd> setupDims;

    typedef LibLSS::multi_array<int, 1> int_array;
    typedef LibLSS::multi_array<int, 1> size_array;
    typedef std::set<int> size_set;

    LibLSS::multi_array<int, 1> other_requested_planes, other_requested_count,
        other_requested_displ;

    std::map<size_t, std::shared_ptr<MPI_Communication>> owned_plane_dispatch;
    size_set req_plane_set;

    template <typename PlaneSet>
    inline size_array fill_with_planes(PlaneSet &&owned_planes) {
      size_array plane_set(boost::extents[owned_planes.size()]);
      size_t i = 0;
      for (auto plane : owned_planes) {
        plane_set[i] = plane;
        i++;
      }
      return plane_set;
    }

    template <typename Array>
    inline std::string array_to_str(Array const &s, char const *sep) {
      std::ostringstream oss;
      auto iter = s.begin();

      if (iter == s.end())
        return "";

      oss << *iter;
      ++iter;

      while (iter != s.end()) {
        oss << sep << *iter;
        ++iter;
      }
      return oss.str();
    }

    template <typename PlaneSet>
    inline void dispatch_plane_map(
        PlaneSet &&owned_planes, int_array &other_planes,
        int_array &other_planes_count, int_array &other_planes_displ) {
      size_t cSize = comm->size();
      auto e_cSize = boost::extents[cSize];
      ConsoleContext<LOG_DEBUG> ctx("dispatch_plane_map");
      int_array tmp_data(e_cSize), send_displ(e_cSize), send_count(e_cSize);

      // Now find out which rank has the planes.
      // Everybody send their planeset for that.
      auto plane_set = fill_with_planes(owned_planes);
      size_t Nplanes = plane_set.size();
      array::fill(tmp_data, Nplanes);
      array::fill(send_count, 1);

      // Costly but we hopefully do it only once in a while.
      // Get all the plane number count from everybody.
      ctx.print("Dispatch our planeset, number is " + to_string(tmp_data));
      comm->all2allT(tmp_data.data(), 1, other_planes_count.data(), 1);

      for (size_t i = 1; i < comm->size(); i++) {
        other_planes_displ[i] =
            other_planes_displ[i - 1] + other_planes_count[i - 1];
      }

      size_t total_planes =
          other_planes_displ[cSize - 1] + other_planes_count[cSize - 1];

      ctx.print(boost::format("Total planes = %d") % total_planes);
      other_planes.resize(boost::extents[total_planes]);

      ctx.print(
          boost::format("Now gather plane ids send_count=%s; send_displ=%s; "
                        "other_planes_count=%s; other_planes_displ=%s") %
          array_to_str(tmp_data, ",") % array_to_str(send_displ, ",") %
          array_to_str(other_planes_count, ",") %
          array_to_str(other_planes_displ, ","));
      // Get plane id from everybody
      comm->all2allv_t(
          plane_set.data(), tmp_data.data(), send_displ.data(),
          other_planes.data(), other_planes_count.data(),
          other_planes_displ.data());
      ctx.print(
          boost::format("Got other task planeset: %s") %
          array_to_str(other_planes, ","));
    }

    typedef std::map<size_t, std::list<size_t>> MapPlaneToPeer;

    inline MapPlaneToPeer gather_peer_by_plane(
        int_array const &required_planes,
        int_array const &required_planes_count,
        int_array const &required_planes_displ) {
      MapPlaneToPeer plane_to_peer;
      int peer = 0;
      size_t cSize = comm->size();
      size_t cRank = comm->rank();
      ConsoleContext<LOG_DEBUG> ctx("gather_peer_by_plane");

      for (size_t i = 0; i < required_planes.num_elements(); i++) {
        if (peer + 1 < cSize && i >= required_planes_displ[peer + 1]) {
          peer++;
        }
        ctx.print(
            boost::format("Peer %d provides %d") % peer % required_planes[i]);
        if (peer != cRank) {
          plane_to_peer[required_planes[i]].push_back(peer);
        }
      }
      return plane_to_peer;
    }

    static inline void null_destroy(void *) {}

    std::map<
        GhostMethod,
        std::function<MPICC_Request(MPI_Communication *, T const *, int)>>
        ghost_methods;
    std::map<
        GhostMethod,
        std::function<MPICC_Request(MPI_Communication *, T *, T *, int)>>
        ghost_methods_ag;

    static MPICC_Request
    ghost_copy_method(MPI_Communication *c, T const *data, int num) {
      return c->IbroadcastT((T *)data, num, 0);
    }

    static MPICC_Request
    ghost_accumulate_method(MPI_Communication *c, T const *data, int num) {
      return c->IallReduceT((T *)MPI_IN_PLACE, (T *)data, num, MPI_SUM);
    }

    static MPICC_Request ghost_accumulate_method_ag(
        MPI_Communication *c, T *indata, T const *data, int num) {
      return c->IgatherT((T *)indata, num, (T *)data, num, 0);
    }

    static MPICC_Request
    ghost_copy_method_ag(MPI_Communication *c, T *indata, T *data, int num) {
      return c->IreduceT(indata, data, num, MPI_SUM, 0);
    }

  public:
    /**
     * Constructor.
     */
    GhostPlanes() {
      ghost_methods[GHOST_COPY] = &ghost_copy_method;
      ghost_methods[GHOST_ACCUMULATE] = &ghost_accumulate_method;
      ghost_methods_ag[GHOST_COPY] = &ghost_copy_method_ag;
      ghost_methods_ag[GHOST_ACCUMULATE] = &ghost_accumulate_method_ag;
      std::fill(setupDims.begin(), setupDims.end(), 0);
    }

    /**
     *  Return the current dimensions of the planes.
     *
     * @return A container with the dimensions.
     */
    auto const &dims() const { return setupDims; }

    /**
     * This function allows the user to change the dimensions of the planes.
     *
     * @params dims (N-1)-d dimension of each plane.
     */
    template <typename DimList>
    void updatePlaneDims(DimList &&dims) {
      LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
      auto i1 = dims.begin();
      auto i2 = setupDims.begin();
      int d = 0;
      for (d = 0; d < Nd; d++) {
        if (*i1 != *i2)
          break;
        ++i1;
        ++i2;
      }
      // Everything already correct. Exit now.
      if (d == Nd) {
        ctx.print("No change needed.");
        return;
      }

      ctx.format("New shape is %dx%d", dims[0], dims[1]);

      for (auto &g : ghosts) {
        if (g.second)
          g.second.reset(); //reshape(dims);
      }
      for (auto &g : ag_ghosts) {
        if (g.second)
          g.second.reset(); //reshape(dims);
      }
      std::copy(dims.begin(), dims.end(), setupDims.begin());
    }

    /**
      * This function setups the ghost plane object for usage. It can be called
      * several times, in that case the previous setup is forgotten and a new
      * one is initiated.
      *
      * @param mpi MPI Communicator with the same topology as the planes
      * @param planes a list of planes that are required from other nodes. The
      *               list must be a sort of container.
      * @param owned_planes a list of the planes that are owned by the current
      *                     node.
      * @param dims dimensions of the planes (barring the first one, i.e. 2D if
      *              the entire set is 3D))
      * @param maxPlaneId_ this is convenience to avoid a global communication
      *            to figure out what is the maximum id of the considered
      *            planes.
      */
    template <typename PlaneList, typename PlaneSet, typename DimList>
    void setup(
        MPI_Communication *comm_, PlaneList &&planes, PlaneSet &&owned_planes,
        DimList &&dims, size_t maxPlaneId_) {
      LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
      size_t cSize = comm_->size();
      auto e_cSize = boost::extents[cSize];
      int_array other_planes, other_planes_count(e_cSize),
          other_planes_displ(e_cSize);
      size_set owned_plane_set;
      //        required_planes, required_planes_count,
      //        required_planes_displ;

      maxPlaneId = maxPlaneId_;
      req_plane_set = size_set(planes.begin(), planes.end());
      owned_plane_set = size_set(owned_planes.begin(), owned_planes.end());

      ghosts.clear();
      comm = comm_;
      std::copy(dims.begin(), dims.end(), setupDims.begin());

      // Create a map betwen requested planes and peers.
      dispatch_plane_map(
          owned_planes, other_planes, other_planes_count, other_planes_displ);

      // Now we know about the requirements of other peer for own set of planes
      auto plane_to_peer = gather_peer_by_plane(
          //        required_planes, required_planes_count, required_planes_displ
          other_planes, other_planes_count, other_planes_displ);

      ctx.print("Required planes: " + to_string(req_plane_set));
      ctx.print("Owned planes: " + to_string(owned_plane_set));

      for (size_t plane = 0; plane < maxPlaneId; plane++) {
        std::shared_ptr<MPI_Communication> cptr;
        auto peer = plane_to_peer.find(plane);

        if (owned_plane_set.count(plane) > 0) {
          // Mark this task as root (key==0)
          cptr = std::shared_ptr<MPI_Communication>(comm->split(plane, 0));
          if (ULTRA_VERBOSE)
            ctx.format("Data for plane %d is present here.", plane);
        } else if (req_plane_set.find(plane) != req_plane_set.end()) {
          // Mark this task as non root (key!=0)
          cptr = std::shared_ptr<MPI_Communication>(comm->split(plane, 1));
          if (ULTRA_VERBOSE)
            ctx.format("Data for plane %d is NEEDED here.", plane);
        } else {
          // Ignore this one, but we have to run it nonetheless as split is a collective operation.
          comm->split();
          if (ULTRA_VERBOSE)
            ctx.format("Ignore this process for plane %d.", plane);
        }
        if (cptr &&
            cptr->size() <=
                1) { // Should even be 2 , but then we have a rank problem later.
          // We do not a need a new communicator for that in the end.
          // This will reaffect cptr and frees the communicator we have just
          // created.
          cptr.reset();
          if (ULTRA_VERBOSE)
            ctx.format(
                "Communicator has only one process for plane %d, reset.",
                plane);
        }
        owned_plane_dispatch[plane] = cptr;
      }
    }

    /**
     * @brief Pre-allocate memory for synchronization.
     * 
     * Warning! Previous memory is freed.
     * 
     */
    void allocate() {
      // Allocate memory for the ghost planes
      for (auto plane : req_plane_set) {
        if (!ghosts[plane])
          ghosts[plane] = std::make_shared<U_ArrayType>(setupDims);
        if (!ag_ghosts[plane])
          ag_ghosts[plane] = std::make_shared<U_ArrayType>(setupDims);
      }
    }

    /**
     * @brief Release memory for synchronization
     * 
     */
    void release() {
      for (auto plane : req_plane_set) {
        ghosts[plane].reset();
        ag_ghosts[plane].reset();
      }
    }

    /**
     * Clear the internal ghost cache for the computation
     * of the adjoint gradient.
     */
    void clear_ghosts() {
      for (auto &ag : ag_ghosts) {
        array::fill(ag.second->get_array(), 0);
      }
    }

    /**
      * This creates a virtual contiguous array of all the planes that are
      * requested and owned by the current task. There is a bit of overhead for
      * each plane lookup so please use wisely by caching plane access.
      *
      * @param planes  contiguous multi_array of planes to be synchronized. The
      *                the multi_array is assumed to range from min_local_plane
      *                to max_local_plane (according to the list given in
      *                setup).
      * @param method  a method to compute the synchronization
      */
    void synchronize(
        boost::multi_array_ref<T, (Nd + 1)> const &planes,
        GhostMethod method = GHOST_COPY) {
      // Synchronize operations with other members of comm
      ConsoleContext<LOG_DEBUG> ctx("ghost synchronize");
      RequestArray requests(boost::extents[maxPlaneId]);
      StatusArray statuses(boost::extents[maxPlaneId]);

      allocate();

      // Check that the planes do have the correct shape
      if (CHECK_DIMENSIONS) {
        auto shape_in = planes.shape();
        auto iter = ghosts.begin();

        if (iter != ghosts.end()) {
          auto shape_out = iter->second->get_array().shape();

          for (size_t i = 1; i < Nd; i++) {
            if (shape_in[i] != shape_out[i - 1]) {
              error_helper<ErrorBadState>(
                  "Invalid dimensions of the array to synchronize (" +
                  to_string(shape_in[i]) +
                  " != " + to_string(shape_out[i - 1]) + ")");
            }
          }
        }
      }

      for (size_t plane = 0; plane < maxPlaneId; plane++) {
        auto iter = owned_plane_dispatch.find(plane);
        if (iter != owned_plane_dispatch.end()) {
          int num;

          if (!iter->second) {
            if (ULTRA_VERBOSE)
              ctx.print("Empty communicator. Skip.");
            continue;
          }

          if (req_plane_set.count(plane) == 0) {
            //Console::instance().c_assert(plane >= idMin && plane < idMax, "Missing plane id for broadcasting");
            auto one_plane = planes[plane];
            T const *data =
                one_plane
                    .origin(); // This assumes that index_bases is zero for dims > 1
            num = one_plane.num_elements();
            ctx.format("Send our plane %d (num=%d)", plane, num);
            requests[plane] =
                ghost_methods[method](iter->second.get(), data, num);
          } else {
            auto &one_plane = (ghosts[plane]->get_array());
            auto data = one_plane.data();
            num = one_plane.num_elements();
            ctx.format(
                "Receive some plane %d (num=%d), ptr=%p", plane, num,
                (void *)data);
            requests[plane] =
                ghost_methods[method](iter->second.get(), data, num);
          }
        }
        // If we do not have anything to exchange just skip the communication.
      }

      if (ULTRA_VERBOSE)
        ctx.print("Wait for completion");
      MPI_Communication::WaitAll(requests, statuses);
    }

    /**
      * This function allows to compute an "adjoint gradient" of the ghost
      * plane algorithm.
      *
      * @param ag_planes similar to synchronize, except that ag_planes is
      *                  modified through communication with sibling nodes.
      * @param method  a method to compute the synchronization
      * @see GhostMethod
      */
    void synchronize_ag(
        boost::multi_array_ref<T, (Nd + 1)> &ag_planes,
        GhostMethod method = GHOST_COPY) {
      // Synchronize operations with other members of comm
      ConsoleContext<LOG_DEBUG> ctx(
          "ghost synchronize_ag, maxPlaneId=" + to_string(maxPlaneId));
      RequestArray requests(boost::extents[maxPlaneId]);
      StatusArray statuses(boost::extents[maxPlaneId]);
      std::vector<std::unique_ptr<T[]>> all_tmps;

      for (size_t plane = 0; plane < maxPlaneId; plane++) {
        auto iter = owned_plane_dispatch.find(plane);
        if (iter != owned_plane_dispatch.end()) {
          int num;

          if (!iter->second) {
            if (ULTRA_VERBOSE)
              ctx.print("Empty communicator. Skip.");
            continue;
          }

          if (req_plane_set.count(plane) == 0) {
            //Console::instance().c_assert(plane >= idMin && plane < idMax, "Missing plane id for broadcasting");
            auto one_plane = ag_planes[plane];
            T *tmp_buf;
            T *data =
                one_plane
                    .origin(); // WARNING: This assumes that index_bases is zero for dims > 1
            num = one_plane.num_elements();
            ctx.format("Receive and reduce our plane %d (num=%d)", plane, num);
            Console::instance().c_assert(
                iter->second->rank() == 0,
                "For reception, local rank has to be zero.");
            all_tmps.push_back(std::unique_ptr<T[]>(tmp_buf = new T[num]));
            LibLSS::copy_array_rv(
                boost::multi_array_ref<T, 2>(
                    tmp_buf,
                    boost::extents[one_plane.shape()[0]][one_plane.shape()[1]]),
                one_plane);
            requests[plane] = ghost_methods_ag[method](
                iter->second.get(), tmp_buf, data, num);
          } else {
            auto &one_plane = (ag_ghosts[plane]->get_array());
            auto data = one_plane.data();
            T *tmp_buf;

            num = one_plane.num_elements();
            ctx.format(
                "Send and reduce some plane %d (num=%d), ptr=%p", plane, num,
                (void *)data);
            Console::instance().c_assert(
                iter->second->rank() != 0,
                "For sending, local rank must not be zero.");
            all_tmps.push_back(std::unique_ptr<T[]>(tmp_buf = new T[num]));
            LibLSS::copy_array_rv(
                boost::multi_array_ref<T, 2>(
                    tmp_buf,
                    boost::extents[one_plane.shape()[0]][one_plane.shape()[1]]),
                one_plane);
            requests[plane] = ghost_methods_ag[method](
                iter->second.get(), tmp_buf, data, num);
          }
        }
        // If we do not have anything to exchange just skip the communication.
      }

      MPI_Communication::WaitAll(requests, statuses);
    }

    /**
      * Return the adjoint gradient plane indicated by the parameter i.
      * @param i plane of interest.
      */
    ArrayType &ag_getPlane(size_t i) {
      auto iter = ag_ghosts.find(i);
      Console::instance().c_assert(
          iter != ag_ghosts.end(), "Invalid ag ghost plane access");
      return iter->second->get_array();
    }

    /**
      * Return the ghost plane indicated by the parameter i.
      * @param i plane of interest.
      */
    ArrayType &getPlane(size_t i) {
      auto iter = ghosts.find(i);
      if (iter == ghosts.end()) {
        Console::instance().print<LOG_ERROR>(
            boost::format("no such ghost plane %d") % i);
        error_helper<ErrorBadState>("Invalid ghost plane access");
      }
      return iter->second->get_array();
    }

    /**
      * Return the ghost plane indicated by the parameter i.
      * @param i plane of interest.
      */
    ArrayType const &getPlane(size_t i) const {
      auto iter = ghosts.find(i);
      if (iter == ghosts.end()) {
        Console::instance().print<LOG_ERROR>(
            boost::format("no such ghost plane %d") % i);
        error_helper<ErrorBadState>("Invalid ghost plane access");
      }
      return iter->second->get_array();
    }
  };

} // namespace LibLSS

#endif
// ARES TAG: num_authors = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2018-2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
