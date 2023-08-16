/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/mpi_fftw/nyquist_downgrade.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

template<typename T>
struct Nyquist_adjust<T, false> {
    typedef FFTW_Manager<T,3> Mgr;
    typedef typename Mgr::Plane Plane;
    typedef typename Mgr::U_Plane U_Plane;
    typedef typename Mgr::U_Array U_Array;

    typedef internal::copy_utils<false, T> c_util;

    template<typename InArray, typename OutArray>
    static void handle(
          const Mgr& small_mgr, const Mgr& big_mgr,
          std::vector<U_Plane *>& request_planes,
          std::vector<bool>& request_io,
          RequestArray& request_array,
          const InArray& in_modes, OutArray& out_modes) {
      MPI_Status status;
      long N0 = small_mgr.N0;
      long N1 = small_mgr.N1;
      long N2 = small_mgr.N2;
      long half_N0 = small_mgr.N0/2;
      long big_conjugate_plane = big_mgr.N0-half_N0;
      Console& cons = Console::instance();


      if (small_mgr.on_core(half_N0)) {
        if(big_mgr.on_core(half_N0)) {
          // both planes are here. push them into out_modes
          c_util::_copy_sub_2d_plane(big_mgr, small_mgr, out_modes[half_N0], in_modes[half_N0], AccumOperator<T>());
        } else {
          // Hmm... we have to grab the request plane
          assert(request_array[half_N0].is_active());
          request_array[half_N0].wait(&status);
          request_io[half_N0] = false;
          c_util::_copy_sub_2d_plane_flat(big_mgr, small_mgr, out_modes[half_N0], request_planes[half_N0]->get_array(), AccumOperator<T>());
          internal::safe_delete(request_planes[half_N0]);
        }

        if (big_mgr.on_core(big_conjugate_plane)) {
          // both planes are here. push them into out_modes
          c_util::_copy_sub_2d_plane(big_mgr, small_mgr, out_modes[half_N0], in_modes[big_conjugate_plane], AccumOperator<T>());
        } else {
          assert(request_array[N0].is_active());
          request_array[N0].wait(&status);
          request_io[N0] = false;
          c_util::_copy_sub_2d_plane_flat(big_mgr, small_mgr, out_modes[half_N0], request_planes[N0]->get_array(), AccumOperator<T>());
          internal::safe_delete(request_planes[N0]);
        }

        // Clear up imaginary parts
        out_modes[half_N0][N1/2][0].imag(0);
        out_modes[half_N0][N1/2][N2/2].imag(0);
        out_modes[half_N0][0][0].imag(0);
        out_modes[half_N0][0][N2/2].imag(0);
      }

      if (small_mgr.on_core(0)) {
        out_modes[0][N1/2][0].imag(0);
        out_modes[0][N1/2][N2/2].imag(0);
      }
        // There is no point for those two.
        //out_modes[0][0][0].imag() = 0;
        //out_modes[0][0][N2/2].imag() = 0;
    }

};
