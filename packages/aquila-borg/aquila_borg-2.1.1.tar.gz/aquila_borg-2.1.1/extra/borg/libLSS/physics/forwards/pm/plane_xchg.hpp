/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/pm/plane_xchg.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TOOLS_PLANE_XCHG_HPP
#define __LIBLSS_TOOLS_PLANE_XCHG_HPP

#include <boost/lambda/lambda.hpp>
#include <boost/multi_array.hpp>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/uninitialized_type.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/tools/push_operators.hpp"
#include <memory>

namespace LibLSS {

  template <bool accum, typename PlaneArray, typename Mgr_p>
  void density_exchange_planes(
      MPI_Communication *comm, PlaneArray &&density, Mgr_p &d_mgr,
      int extra_planes) {
    ConsoleContext<LOG_DEBUG> ctx("exchanging nearby planes after projection");

    using boost::extents;
    using boost::format;
    using boost::lambda::_1;

    typedef Uninit_FFTW_Real_Array U_Array;
    MPI_Communication::Request req_send, req_recv;

    long d_N2real = d_mgr->N2real;
    long d_N1 = d_mgr->N1;
    long d_N2 = d_mgr->N2;
    long d_N0 = d_mgr->N0;
    long d_startN0 = d_mgr->startN0;
    long d_localN0 = d_mgr->localN0;
    U_Array tmp_plane_r_p(extents[extra_planes][d_N1][d_N2real]);

    if (d_localN0 == 0)
      return;

    U_Array::array_type &tmp_plane_r = tmp_plane_r_p.get_array();
    long high_plane_id = (d_startN0 + d_localN0) % d_N0;
    long low_plane_id = d_startN0;
    long low_plane_peer = d_mgr->get_peer((d_startN0 + d_N0 - 1) % d_N0);
    typedef
        typename std::remove_reference<PlaneArray>::type::reference plane_ref_t;
    plane_ref_t plane = density[d_startN0 + d_localN0];
    plane_ref_t low_plane = density[d_startN0];

    ctx.print(
        format("high_id=%d -> peer=%d") % high_plane_id %
        d_mgr->get_peer(high_plane_id));
    ctx.print(format("low_id=%d -> peer=%d") % low_plane_id % low_plane_peer);

    // Missing some logic here if the planes are scattered on different nodes (happens for extra_planes > 1)
    req_send = comm->IsendT(
        &plane[0][0], plane.num_elements(), d_mgr->get_peer(high_plane_id),
        high_plane_id);
    req_recv = comm->IrecvT(
        tmp_plane_r.data(), tmp_plane_r.num_elements(), low_plane_peer,
        low_plane_id);

    req_recv.wait();

    // This should use the fused infrastructure. But it does not support
    // sub array yet.
    for (long i = 0; i < d_N1; i++)
      for (long j = 0; j < d_N2; j++)
        push_to<accum>::apply(low_plane[i][j], tmp_plane_r[0][i][j]);

    req_send.wait();
  }

  template <
      typename OutPlaneArray, typename InPlaneArray, typename Mgr_p>
  void density_exchange_planes_ag(
      MPI_Communication *comm, OutPlaneArray &loc_density,
      InPlaneArray &global_density, Mgr_p &d_mgr, unsigned int extra_planes) {
    using boost::format;
    using boost::lambda::_1;
    typedef Uninit_FFTW_Real_Array U_Array;

    ConsoleContext<LOG_DEBUG> ctx(
        "exchanging nearby planes before taking adjoint gradient");
    MPI_Communication::Request req_send, req_recv;

    long d_N2real = d_mgr->N2real;
    long d_N1 = d_mgr->N1;
    long d_N2 = d_mgr->N2;
    long d_N0 = d_mgr->N0;
    long d_startN0 = d_mgr->startN0;
    long d_localN0 = d_mgr->localN0;
    long high_plane_id = (d_startN0 + d_localN0);
    long high_plane_peer = d_mgr->get_peer(high_plane_id % d_N0);
    long low_plane_id = d_startN0;
    long low_plane_peer = d_mgr->get_peer((d_startN0 + d_N0 - 1) % d_N0);
    typedef typename OutPlaneArray::index_range o_range;
    typename OutPlaneArray::index_gen o_indices;
    typedef typename InPlaneArray::index_range i_range;
    typename InPlaneArray::index_gen i_indices;

    if (d_localN0 == 0)
      return;

    // Missing some logic here if the planes are scattered on different nodes (happens for extra_planes > 1)
    auto loc_view =
        loc_density[o_indices[o_range(d_startN0, d_startN0 + d_localN0)]
                             [o_range()][o_range(0, d_N2)]];
    auto glob_view =
        global_density[i_indices[i_range(d_startN0, d_startN0 + d_localN0)]
                                [i_range()][i_range(0, d_N2)]];

    copy_array_rv(loc_view, glob_view, false);

    ctx.print(
        format("Receiving plane = %d from %d") % high_plane_id %
        high_plane_peer);
    req_recv = comm->IrecvT(
        &loc_density[high_plane_id][0][0],
        loc_density[high_plane_id].num_elements(), high_plane_peer,
        high_plane_id % d_N0);
    ctx.print(
        format("Sending plane = %d to %d") % low_plane_id % low_plane_peer);
    req_send = comm->IsendT(
        &loc_density[low_plane_id][0][0],
        loc_density[low_plane_id].num_elements(), low_plane_peer, low_plane_id);

    req_recv.wait();
    req_send.wait();
  }

} // namespace LibLSS

#endif
