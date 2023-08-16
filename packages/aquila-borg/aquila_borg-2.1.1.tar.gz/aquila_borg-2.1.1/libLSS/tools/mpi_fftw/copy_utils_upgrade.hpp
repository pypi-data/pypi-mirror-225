/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/mpi_fftw/copy_utils_upgrade.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
template<typename T>
struct copy_utils<true, T> {
  typedef T element;
  typedef FFTW_Manager_3d<T> Mgr;
  typedef std::complex<T> complex_element;



  // This function upgrades the input array to output array. It assumes
  // the current manager object if the high resolution and small_mgr is the low
  // resolution descriptor. It transfers then the two Fourier square ([0:N1/2, 0:N2_HC] and [N1/2:N1, 0:N2_HC] to their
  // adequate position in the target array.
  // The array must have a 2D shape topology.
  template<typename OutArray, typename InArray, typename Func >
  static
  void _copy_sub_2d_plane(Mgr const& target_mgr, Mgr const& init_mgr,
                          OutArray out, const InArray& in_array, const Func& func)
  {
    long last_plane = init_mgr.N2_HC-1;
    typedef typename OutArray::reference OutRef;
    typedef typename OutArray::const_reference InRef;

    for (long i = 0; i < init_mgr.N1/2; i++) {
      for (long j = 0; j < last_plane; j++) {
        func(out[i][j], in_array[i][j], false, false);
      }
      func(out[i][last_plane], in_array[i][last_plane], false, true);
      // There is missing half sum here. But the data are not necessarily here. (conjugate on the last plane).
      // The final sum is delayed.
    }

    long base, base2;
    long out1_half_N1, out2_half_N1;
    long in1_half_N1, in2_half_N1;

    base = target_mgr.N1-init_mgr.N1;
    base2 = 0;
    out1_half_N1 = init_mgr.N1/2;
    out2_half_N1 = target_mgr.N1-init_mgr.N1/2;
    in1_half_N1 = init_mgr.N1/2;
    in2_half_N1 = init_mgr.N1/2;

    {
      OutRef out1 = out[out1_half_N1];
      OutRef out2 = out[out2_half_N1];
      InRef in1 = in_array[in1_half_N1];
      InRef in2 = in_array[in2_half_N1];

      for (long j = 0; j < last_plane; j++) {
        func(out1[j], in_array[in1_half_N1][j], true, false);
        func(out2[j], in_array[in2_half_N1][j], true, false);
      }
      func(out1[last_plane], in1[last_plane], true, true);
      func(out2[last_plane], in2[last_plane], true, true);
    }

    for (long i = init_mgr.N1/2+1; i < init_mgr.N1; i++) {
      OutRef out_i = out[base+i];
      InRef in_i = in_array[base2+i];

      for (long j = 0; j < last_plane; j++) {
        func(out_i[j], in_i[j], false, false);
      }
      func(out_i[last_plane], in_i[last_plane], false, true);
      // There is missing half sum here. But the data are not necessarily here. (conjugate on the last plane).
      // The final sum is delayed.
    }
  }



  // This function up/downgrades the input array to output array. It assumes
  // the current manager object if the high resolution and small_mgr is the low
  // resolution descriptor. It transfers then the two Fourier square ([0:N1/2, 0:N2_HC] and [N1/2:N1, 0:N2_HC] to their
  // adequate position in the target array.
  // The array must have a 1D flat topology.
  template<typename OutArray, typename FlatPlane, typename Func >
  static
  void _copy_sub_2d_plane_flat(Mgr const& target_mgr, Mgr const& init_mgr,
                               OutArray out, const FlatPlane& flat,
                               const Func& func = Func())
  {
    typedef typename OutArray::reference OutRef;
    ConsoleContext<LOG_DEBUG> ctx("_copy_sub_2d_plane_flat");

    for (long i = 0; i < init_mgr.N1/2; i++) {
      for (long j = 0; j < init_mgr.N2_HC; j++) {
        func(out[i][j], flat[i*init_mgr.N2_HC + j], false, false);
      }
    }

    long base = target_mgr.N1-init_mgr.N1;
    long half1 = init_mgr.N1/2;
    long half2 = target_mgr.N1 - init_mgr.N1/2;
    OutRef out_half1 = out[half1];
    OutRef out_half2 = out[half2];

    for (long j = 0; j < init_mgr.N2_HC; j++) {
      func(out_half1[j], flat[half1*init_mgr.N2_HC + j], true, false);
      func(out_half2[j], flat[half1*init_mgr.N2_HC + j], true, false);
    }

    for (long i = init_mgr.N1/2+1; i < init_mgr.N1; i++) {
      OutRef out_i = out[base+i];
      for (long j = 0; j < init_mgr.N2_HC; j++) {
        func(out_i[j], flat[i*init_mgr.N2_HC + j], false, false);
      }
    }
  }

  template<typename OutArray, typename InArray >
  static
  void _copy_sub_2d_plane(Mgr const& target_mgr, Mgr const& init_mgr,
                          OutArray out,
                          const InArray& in_array)
  {
    _copy_sub_2d_plane(target_mgr, init_mgr, out, in_array, internal::AssignOperator<T,true>());
  }

  template<typename OutArray, typename FlatPlane >
  static
  void _copy_sub_2d_plane_flat(Mgr const& target_mgr, const Mgr& init_mgr,
                               OutArray out, const FlatPlane& flat)
  {
    _copy_sub_2d_plane_flat(target_mgr, init_mgr, out, flat, internal::AssignOperator<T,true>());
  }

  // This function transforms 2D like array into a flattened 1D array.
  // This assumes that the array has the correct shape (N1 x N2_HC)
  // init_mgr is always the small one
  template<typename OutArray, typename InArray, typename Func>
  static
  void _flat_copy_2d_array(const Mgr& target_mgr, const Mgr& init_mgr,
                           OutArray& out, const InArray& in, const Func& func)
  {
    boost::multi_array_ref<complex_element, 2> out_ref(out.data(), boost::extents[init_mgr.N1][init_mgr.N2_HC]);
    LibLSS::copy_array(out_ref, in);
  }

  template<typename OutArray, typename InArray>
  static
  void _flat_copy_2d_array(const Mgr& target_mgr, const Mgr& init_mgr,
                           OutArray& out, const InArray& in)
  {
    _flat_copy_2d_array(target_mgr, init_mgr, out, in, internal::AssignOperator<T,true>());
  }


};
