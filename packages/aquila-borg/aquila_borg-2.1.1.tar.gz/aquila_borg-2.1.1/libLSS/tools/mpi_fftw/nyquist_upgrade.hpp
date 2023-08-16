/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/mpi_fftw/nyquist_upgrade.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
template<typename T> struct Nyquist_adjust<T, true> {
    typedef FFTW_Manager<T,3> Mgr;
    typedef typename Mgr::Plane Plane;
    typedef typename Mgr::U_Plane U_Plane;
    typedef typename Mgr::U_Array U_Array;

    typedef internal::copy_utils<true, T> c_util;


    template<typename InArray, typename OutArray>
    static void handle(
            const Mgr& small_mgr, const Mgr& big_mgr,
            std::vector<U_Plane *>& request_planes,
            std::vector<bool>& request_io,
            RequestArray& request_array,
            const InArray& in_modes, OutArray& out_modes) {
      using boost::format;
      Console& cons = Console::instance();
      MPI_Status status;
      MPI_Communication *comm = small_mgr.comm;

      long half_N0 = small_mgr.N0/2;
      long conjugate_big_plane = big_mgr.N0 - half_N0;

      if (small_mgr.on_core(small_mgr.N0/2) && big_mgr.on_core(small_mgr.N0/2)) {
        c_util::_copy_sub_2d_plane(big_mgr, small_mgr, out_modes[small_mgr.N0/2], in_modes[small_mgr.N0/2]);
      }
      if (small_mgr.on_core(small_mgr.N0/2) && big_mgr.on_core(conjugate_big_plane)) {
        c_util::_copy_sub_2d_plane(big_mgr, small_mgr, out_modes[big_mgr.N0-small_mgr.N0/2], in_modes[small_mgr.N0/2]);
      }

      if (!small_mgr.on_core(half_N0) && big_mgr.on_core(half_N0)) {
        U_Array& a_plane = request_planes[half_N0]->get_array();

        cons.c_assert(request_planes[half_N0] != 0, "No half_N0 plane, though we need it here");
        // Wait for the recv to complete
        request_array[half_N0].wait(&status);
        request_io[half_N0] = false;
        cons.print<LOG_DEBUG>(format("Received plane %d (big is %d)") % half_N0 % half_N0);

        // Copy the plane
        c_util::_copy_sub_2d_plane_flat(big_mgr, small_mgr, out_modes[half_N0], a_plane);

        // If the other plane is on this core, copy the data.
        if (big_mgr.on_core(conjugate_big_plane)) {
          c_util::_copy_sub_2d_plane_flat(big_mgr, small_mgr, out_modes[conjugate_big_plane], a_plane);
        }
        // Cleanup
        internal::safe_delete(request_planes[half_N0]);
      } else
        if (!small_mgr.on_core(half_N0) && big_mgr.on_core(conjugate_big_plane)) {
          // If we do not have the half_N0 plane and we are in the negative freq range
          // just wait for the transfer to finish.

          cons.print<LOG_DEBUG>(format("Half plane, big = %d") % conjugate_big_plane);
          cons.c_assert(request_io[small_mgr.N0], "Invalid I/O state");
          U_Array& a_plane = request_planes[small_mgr.N0]->get_array();

          request_array[small_mgr.N0].wait(&status);
          request_io[small_mgr.N0] = false;
          cons.print<LOG_DEBUG>(format("Received plane %d (big is %d)") % half_N0 % conjugate_big_plane);
          c_util::_copy_sub_2d_plane_flat(big_mgr, small_mgr, out_modes[conjugate_big_plane], a_plane);
          internal::safe_delete(request_planes[half_N0]);
        }
    }
};
