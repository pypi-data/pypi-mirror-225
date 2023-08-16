/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/mpi_fftw/copy_utils_degrade.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

// target_mgr < init_mgr here
template<typename T>
struct copy_utils<false, T> {
  typedef T element;
  typedef FFTW_Manager<T,3> Mgr;
  typedef std::complex<T> complex_element;


  template<typename OutArray, typename InArray, typename Func >
  static
  void _copy_sub_2d_plane(const Mgr& init_mgr, const Mgr& target_mgr, OutArray out, const InArray& in_array, const Func& func)
  {
    long last_plane = target_mgr.N2_HC-1;
    typedef typename OutArray::reference OutRef;
    typedef typename InArray::const_reference InRef;

    for (long i = 0; i < target_mgr.N1/2; i++) {
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
    
    base = 0;
    base2 = init_mgr.N1 - target_mgr.N1;
    out1_half_N1 = target_mgr.N1/2;
    out2_half_N1 = target_mgr.N1/2;
    in1_half_N1 = target_mgr.N1/2;
    in2_half_N1 = init_mgr.N1-target_mgr.N1/2;

    {
      OutRef out1 = out[out1_half_N1];
      OutRef out2 = out[out2_half_N1];
      InRef in1 = in_array[in1_half_N1];
      InRef in2 = in_array[in2_half_N1];

      for (long j = 0; j < last_plane; j++) {
        func(out1[j], in1[j], true, false);
        func(out2[j], in2[j], true, false);
      }
      func(out1[last_plane], in1[last_plane], true, true);
    }

    for (long i = target_mgr.N1/2+1; i < target_mgr.N1; i++) {
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
  // the current manager object if the high resolution and init_mgr is the low 
  // resolution descriptor. It transfers then the two Fourier square ([0:N1/2, 0:N2_HC] and [N1/2:N1, 0:N2_HC] to their
  // adequate position in the target array.
  // The array must have a 1D flat topology.
  template<typename OutArray, typename FlatPlane, typename Func >
  static
  void _copy_sub_2d_plane_flat(const Mgr& init_mgr, const Mgr& target_mgr, 
                               OutArray out, const FlatPlane& flat,
                               const Func& func = Func())
  {
    typedef typename OutArray::reference OutRef;
    ConsoleContext<LOG_DEBUG> ctx("_copy_sub_2d_plane_flat");
    long h_N2 = target_mgr.N2_HC-1;

    for (long i = 0; i < target_mgr.N1/2; i++) {
      for (long j = 0; j < h_N2; j++) {
        func(out[i][j], flat[i*init_mgr.N2_HC + j], false, false);
      }
      func(out[i][h_N2], flat[i*init_mgr.N2_HC + h_N2], false, true);
    }

    long half1 = target_mgr.N1/2;
    long half2 = init_mgr.N1 - target_mgr.N1/2;
    OutRef out_half = out[half1];

    for (long j = 0; j < h_N2; j++) {
      func(out_half[j], flat[half1*init_mgr.N2_HC + j], true, false);
      func(out_half[j], flat[half2*init_mgr.N2_HC + j], true, false);
    }
    func(out_half[h_N2], flat[half1*init_mgr.N2_HC + h_N2], true, true);
    func(out_half[h_N2], flat[half2*init_mgr.N2_HC + h_N2], true, true);

    long base = init_mgr.N1-target_mgr.N1; 
    for (long i = target_mgr.N1/2+1; i < target_mgr.N1; i++) {
      for (long j = 0; j < h_N2; j++) {
        func(out[i][j], flat[(base+i)*init_mgr.N2_HC + j], false, false);
      }
      func(out[i][h_N2], flat[(base+i)*init_mgr.N2_HC + h_N2], false, true);
    }
  }


  template<typename OutArray, typename InArray >
  static
  void _copy_sub_2d_plane(const Mgr& init_mgr, const Mgr& target_mgr, 
                          OutArray out, const InArray& in_array)
  {
    _copy_sub_2d_plane(init_mgr, target_mgr, out, in_array, internal::AssignOperator<T,false>());
  }

  template<typename OutArray, typename FlatPlane >
  static
  void _copy_sub_2d_plane_flat(const Mgr& init_mgr, const Mgr& target_mgr, 
                               OutArray out, const FlatPlane& flat)
  {
    _copy_sub_2d_plane_flat(init_mgr, target_mgr, out, flat, internal::AssignOperator<T,false>());
  }

  static inline
  const Mgr& source(const Mgr& big_mgr, const Mgr& small_mgr) { return big_mgr; }

  static inline
  const Mgr& target(const Mgr& big_mgr, const Mgr& small_mgr) { return small_mgr; }

  template<typename OutArray, typename InArray>
  static
  void _flat_copy_2d_array(const Mgr& init_mgr, const Mgr& target_mgr,
                           OutArray& out, const InArray& in)
  {
    ConsoleContext<LOG_DEBUG> ctx("_flat_copy_2d_array");
    boost::multi_array_ref<complex_element, 2> out_ref(out.data(), boost::extents[init_mgr.N1][init_mgr.N2_HC]);
    LibLSS::copy_array(out_ref, in);
  } 
};
