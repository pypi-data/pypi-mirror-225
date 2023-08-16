
template <typename T>
class FFTW_Manager<T, 3> {
public:
  static const bool FFTW_HELPER_CHATTY = false;
  typedef FFTW_Manager<T, 3> self_t;
  typedef FFTW_Allocator<T> AllocReal;
  typedef FFTW_Allocator<std::complex<T>> AllocComplex;
#ifdef ARES_MPI_FFTW
  typedef CosmoTool::FFTW_MPI_Calls<T> Calls;
#else
  typedef CosmoTool::FFTW_Calls<T> Calls;
#endif
  typedef boost::multi_array_types::extent_gen::gen_type<3>::type Extent3d;
  typedef typename Calls::plan_type plan_type;
  typedef T element;
  typedef std::complex<T> complex_element;

  template <typename T2, bool>
  friend struct internal::Nyquist_adjust;

  long N0, N1, N2, N2_HC, N2real;

  std::array<size_t, 3> N;
  long N_HC, N_real;

  AllocReal allocator_real, allocator_real_strict, allocator_t_real;
  AllocComplex allocator_complex, allocator_t_complex;

  typedef boost::multi_array<element, 3, AllocReal> ArrayReal;
  typedef boost::multi_array<element, 2> ArrayRealPlane;
  typedef boost::multi_array<complex_element, 3, AllocComplex> ArrayFourier;
  typedef boost::multi_array<complex_element, 2> ArrayFourierPlane;

  typedef UninitializedArray<ArrayReal, AllocReal> U_ArrayReal;
  typedef UninitializedArray<ArrayFourier, AllocComplex> U_ArrayFourier;

  typedef
      typename ArrayReal::index_gen::template gen_type<3, 3>::type StrictRange;

  boost::multi_array<int, 1> peer;
  ptrdiff_t local_size, local_size_t, localN0, startN0, localN1, startN1;

protected:
  MPI_Communication *comm;

public: /*
      FFTW_Manager(size_t N[3], MPI_Communication *comm)
        : FFTW_Manager_3d<T>(N[0], N[1], N[2], comm) {
      }*/
  FFTW_Manager(long pN0, long pN1, long pN2, MPI_Communication *c) {
    N[0] = N0 = pN0;
    N[1] = N1 = pN1;
    N[2] = N2 = pN2;
    comm = c;

    N_HC = N2_HC = N2 / 2 + 1;

#ifdef ARES_MPI_FFTW
    local_size =
        Calls::local_size_3d(N0, N1, N2, comm->comm(), &localN0, &startN0);
    // Local size when first two dims are swapped
    local_size_t =
        Calls::local_size_3d(N1, N0, N2, comm->comm(), &localN1, &startN1);
    N_real = N2real = N2_HC * 2;
#else
    local_size_t = local_size = N0 * N1 * (N2 / 2 + 1);

    localN0 = N0;
    startN0 = 0;
    startN1 = 0;
    localN1 = N1;
    N2real = N2;
#endif

    allocator_real.minAllocSize = local_size * 2;
    allocator_complex.minAllocSize = local_size;

    allocator_real_strict.minAllocSize = 0;

    allocator_t_real.minAllocSize = local_size_t * 2;
    allocator_t_complex.minAllocSize = local_size_t;

    init_peer_upgrade_system();
  }

  U_ArrayReal allocate_array(
      int extra_plane_leakage = 0, int extra_negative_plane_leakage = 0) {
    return U_ArrayReal(
        extents_real(extra_plane_leakage, extra_negative_plane_leakage),
        allocator_real, boost::c_storage_order());
  }

  U_ArrayReal allocate_array_strict(int extra_plane_leakage = 0) {
    return U_ArrayReal(
        extents_real_strict(extra_plane_leakage), allocator_real_strict,
        boost::c_storage_order());
  }

  auto allocate_ptr_array(int extra_plane_leakage = 0) {
    return std::unique_ptr<U_ArrayReal>(new U_ArrayReal(
        extents_real(extra_plane_leakage), allocator_real,
        boost::c_storage_order()));
  }

  U_ArrayFourier allocate_complex_array() {
    return U_ArrayFourier(
        extents_complex(), allocator_complex, boost::c_storage_order());
  }

  auto allocate_ptr_complex_array(bool transposed = false) {
    return std::unique_ptr<U_ArrayFourier>(new U_ArrayFourier(
        transposed ? extents_complex_transposed() : extents_complex(),
        allocator_complex, boost::c_storage_order()));
  }

  MPI_Communication *getComm() { return comm; }
  MPI_Communication const *getComm() const { return comm; }

  // This function returns an index range that strictly
  // reduces the view to the allowed part of the multi_array.
  // This can be used on multi_array 'a' using a[strict_range()].
  StrictRange strict_range() const {
    typedef boost::multi_array_types::index_range i_range;
    //        typename ArrayReal::index_gen indices;

    // We cannot use this as it changes the actual limits
    // of indices for the first axis. We just limit the
    // last one.
    // return indices[i_range(startN0, startN0+localN0)][i_range()][i_range(0, N2)];
    return boost::indices[i_range::all()][i_range::all()][i_range(0, N2)];
  }

  auto complex_range() const {
    typedef boost::multi_array_types::index_range i_range;
    return boost::indices[i_range(startN0, startN0+localN0)][i_range::all()][i_range(0, N2_HC)];
  }

  StrictRange extra_strict_range() const {
    typedef boost::multi_array_types::index_range i_range;
    //        typename ArrayReal::index_gen indices;

    // WARNING: this changes the origin of the first axis
    return boost::indices[i_range(startN0, startN0 + localN0)][i_range()]
                         [i_range(0, N2)];
  }

  Extent3d extents_complex() const {
    using boost::extents;
    typedef boost::multi_array_types::extent_range range;

    return extents[range(startN0, startN0 + localN0)][N1][N2_HC];
  }

  Extent3d extents_complex_transposed() const {
    using boost::extents;
    typedef boost::multi_array_types::extent_range range;

#ifdef ARES_MPI_FFTW
    return extents[range(startN1, startN1 + localN1)][N0][N2_HC];
#else
    return extents[N0][N1][N2_HC];
#endif
  }

  // Build 3d extents. Optional parameter to state how many
  // _positive_ extra planes are required.
  Extent3d extents_real(
      int extra_plane_leakage = 0, int negative_plane_leakage = 0) const {
    typedef boost::multi_array_types::extent_range range;
    using boost::extents;

#ifdef ARES_MPI_FFTW
    return extents[range(
        startN0 - negative_plane_leakage,
        startN0 + localN0 + extra_plane_leakage)][N1][N2real];
#else
    return extents[range(startN0, startN0 + localN0)][N1][N2];
#endif
  }

  template <typename ExtentList>
  auto extents_real(ExtentList lst, int extra_plane_leakage = 0) const {
    typedef boost::multi_array_types::extent_range range;

#ifdef ARES_MPI_FFTW
    return lst[range(startN0, startN0 + localN0 + extra_plane_leakage)][N1]
              [N2real];
#else
    return lst[range(startN0, startN0 + localN0)][N1][N2];
#endif
  }

  template <typename ExtentList>
  auto extents_real_strict(ExtentList lst, int extra_plane_leakage = 0) const {
    typedef boost::multi_array_types::extent_range range;

    return lst[range(startN0, startN0 + localN0 + extra_plane_leakage)][N1][N2];
  }

  Extent3d extents_real_strict(int extra_plane_leakage = 0) const {
    typedef boost::multi_array_types::extent_range range;
    using boost::extents;

    return extents[range(startN0, startN0 + localN0 + extra_plane_leakage)][N1]
                  [N2];
  }

  Extent3d extents_c2c() const {
    typedef boost::multi_array_types::extent_range range;
    using boost::extents;

    return extents[range(startN0, startN0 + localN0)][N1][N2];
  }

  U_ArrayFourier allocate_c2c_array() {
    return U_ArrayFourier(
        extents_c2c(), allocator_complex, boost::c_storage_order());
  }

  plan_type
  create_c2c_plan(std::complex<T> *in, std::complex<T> *out, int sign) {
    unsigned int flags = FFTW_DESTROY_INPUT | FFTW_MEASURE;

    return Calls::plan_dft_3d(
        N0, N1, N2, (typename Calls::complex_type *)in,
        (typename Calls::complex_type *)out,
#ifdef ARES_MPI_FFTW
        comm->comm(),
#endif
        sign, flags);
  }

  plan_type
  create_c2c_plan_2d(std::complex<T> *in, std::complex<T> *out, int sign) {
    unsigned int flags = FFTW_DESTROY_INPUT | FFTW_MEASURE;

    return Calls::plan_dft_2d(
        N0, N1, (typename Calls::complex_type *)in,
        (typename Calls::complex_type *)out,
#ifdef ARES_MPI_FFTW
        comm->comm(),
#endif
        sign, flags);
  }
  

  plan_type
  create_r2c_plan(T *in, std::complex<T> *out, bool transposed_out = false) {
    ConsoleContext<LOG_DEBUG> ctx("FFTW_Manager::create_r2c_plan");
    unsigned int flags = FFTW_DESTROY_INPUT | FFTW_MEASURE;
#ifdef ARES_MPI_FFTW
    if (transposed_out)
      flags |= FFTW_MPI_TRANSPOSED_OUT;
#endif

    return Calls::plan_dft_r2c_3d(
        N0, N1, N2, in, (typename Calls::complex_type *)out,
#ifdef ARES_MPI_FFTW
        comm->comm(),
#endif
        flags);
  }

  plan_type
  create_c2r_plan(std::complex<T> *in, T *out, bool transposed_in = false) {
    ConsoleContext<LOG_DEBUG> ctx("FFTW_Manager::create_c2r_plan");
    int flags = FFTW_DESTROY_INPUT | FFTW_MEASURE;
#ifdef ARES_MPI_FFTW
    if (transposed_in)
      flags |= FFTW_MPI_TRANSPOSED_IN;
#endif

    return Calls::plan_dft_c2r_3d(
        N0, N1, N2, (typename Calls::complex_type *)in, out,
#ifdef ARES_MPI_FFTW
        comm->comm(),
#endif
        flags);
  }

  void destroy_plan(plan_type p) const {
    ConsoleContext<LOG_DEBUG> ctx("FFTW_Manager::destroy_plan");
    return Calls::destroy_plan(p);
  }

  template <typename InType, typename OutType>
  static void execute_r2c(plan_type p, InType *in, OutType *out) {
    ConsoleContext<LOG_DEBUG> ctx("FFTW_Manager::execute_r2c");
    Calls::execute_r2c(p, in, out);
  }

  template <typename InType, typename OutType>
  static void execute_c2r(plan_type p, InType *in, OutType *out) {
    ConsoleContext<LOG_DEBUG> ctx("FFTW_Manager::execute_c2r");
    Calls::execute_c2r(p, in, out);
  }

  template <typename InType, typename OutType>
  static void execute_c2c(plan_type p, InType *in, OutType *out) {
    ConsoleContext<LOG_DEBUG> ctx("FFTW_Manager::execute_c2c");
    Calls::execute_c2c(p, in, out);
  }

  typedef boost::multi_array_ref<complex_element, 1> Plane;
  typedef UninitializedArray<Plane> U_Plane;
  typedef typename U_Plane::array_type U_Array;

  U_Plane *_newPlane() const { return new U_Plane(boost::extents[N1 * N2_HC]); }

  bool on_core(long i) const {
    return (i >= startN0 && i < (startN0 + localN0));
  }

  long get_peer(long i) const { return peer[i]; }

  template <bool upgrading, typename InArray, typename OutArray>
  static typename boost::enable_if<
      boost::is_same<typename InArray::element, complex_element>>::type
  _ud_grade(
      self_t const &out_mgr, self_t const &small_mgr, self_t const &big_mgr,
      const InArray &in_modes, OutArray &out_modes) {
    using boost::format;
    MPI_Status status;
    MPI_Communication *comm = small_mgr.comm;
    long thisRank = comm->rank();
    U_Plane *tmp_plane;
    std::vector<U_Plane *> request_planes(small_mgr.N0 + 1);
    RequestArray request_array(boost::extents[small_mgr.N0 + 1]);
    std::vector<bool> request_io(small_mgr.N0 + 1);
    Console &cons = Console::instance();
    typedef internal::copy_utils<upgrading, T> c_util;

    std::fill(request_planes.begin(), request_planes.end(), (U_Plane *)0);
    std::fill(request_io.begin(), request_io.end(), false);

    long half_N0 = small_mgr.N0 / 2;

    // First pass: here we schedule I/O on lines that are no
    for (long i = 0; i < small_mgr.N0; i++) {
      long big_plane = i <= half_N0 ? i : (big_mgr.N0 - small_mgr.N0 + i);
      bool on_core_small = small_mgr.on_core(i),
           on_core_big = big_mgr.on_core(big_plane);
      bool double_on_core = on_core_small && on_core_big;
      bool double_not_on_core = !on_core_small && !on_core_big;
      // Send the line that are here (by construction from startN0, localN0), but that the remote needs (peer tells it)
      if ((i != half_N0 && (double_on_core || double_not_on_core)) ||
          (i == half_N0 && double_on_core &&
           big_mgr.on_core(big_mgr.N0 - half_N0))) {
        continue;
      }

      // Allocate a new plane
      tmp_plane = upgrading ? small_mgr._newPlane() : big_mgr._newPlane();

      U_Array &a_plane = tmp_plane->get_array();
      long io_id = i;
      bool on_core_source;
      bool on_core_target;
      long peer_source, peer_target;
      long plane_source;

      if (upgrading) {
        on_core_source = on_core_small;
        on_core_target = on_core_big;
        peer_source = small_mgr.peer[i];
        peer_target = big_mgr.peer[big_plane];
        plane_source = i;
      } else {
        on_core_source = on_core_big;
        on_core_target = on_core_small;
        peer_source = big_mgr.peer[big_plane];
        peer_target = small_mgr.peer[i];
        plane_source = big_plane;
      }
      if (FFTW_HELPER_CHATTY)
        cons.print<LOG_DEBUG>(
            format("Plane %d / %d, on_core_small = %d, on_core_big = %d") % i %
            big_plane % on_core_small % on_core_big);
      if (!on_core_source && on_core_target) {
        if (FFTW_HELPER_CHATTY)
          cons.print<LOG_DEBUG>(
              format("Scheduling to recv plane %d (low) from %d") % i %
              peer_source);
        // This is not in our range. Schedule a receive.

        request_array[i] = comm->Irecv(
            a_plane.data(), a_plane.num_elements(),
            translateMPIType<complex_element>(), peer_source, io_id);
        request_io[i] = true;
        if (FFTW_HELPER_CHATTY)
          cons.print<LOG_DEBUG>("Finished");
      } else if (on_core_source && !on_core_target) {
        if (FFTW_HELPER_CHATTY)
          cons.print<LOG_DEBUG>(
              format("Scheduling to send plane %d (low) to %d") % i %
              peer_target);
        // This is in the range of the other node. Schedule a send.

        // Flatten the data into it
        c_util::_flat_copy_2d_array(
            big_mgr, small_mgr, a_plane, in_modes[plane_source]);
        // Isend the data.
        request_array[i] = comm->Isend(
            a_plane.data(), a_plane.num_elements(),
            translateMPIType<complex_element>(), peer_target, io_id);
        request_io[i] = true;
        if (FFTW_HELPER_CHATTY)
          cons.print<LOG_DEBUG>("Finished");
      }

      if (upgrading) {
        if (i == half_N0 && on_core_small &&
            !big_mgr.on_core(big_mgr.N0 - half_N0)) {
          long peer = big_mgr.get_peer(big_mgr.N0 - half_N0);
          if (FFTW_HELPER_CHATTY)
            cons.print<LOG_DEBUG>(
                format("Scheduling to send plane %d (low, 2) to %d") % i %
                peer);
          request_array[small_mgr.N0] = comm->Isend(
              a_plane.data(), a_plane.num_elements(),
              translateMPIType<complex_element>(), peer, io_id);
          request_planes[small_mgr.N0] = tmp_plane;
          request_io[small_mgr.N0] = true;
          if (FFTW_HELPER_CHATTY)
            cons.print<LOG_DEBUG>("Finished");
        }
        if (i == half_N0 && !on_core_small &&
            big_mgr.on_core(big_mgr.N0 - half_N0)) {
          long peer = small_mgr.get_peer(half_N0);
          if (FFTW_HELPER_CHATTY)
            cons.print<LOG_DEBUG>(
                format("Scheduling to recv plane %d (low, 2) from %d") % i %
                peer);
          request_array[small_mgr.N0] = comm->Irecv(
              a_plane.data(), a_plane.num_elements(),
              translateMPIType<complex_element>(), peer, io_id);
          request_planes[small_mgr.N0] = tmp_plane;
          request_io[small_mgr.N0] = true;
          if (FFTW_HELPER_CHATTY)
            cons.print<LOG_DEBUG>("Finished");
        }
      } else {
        if (i == half_N0 && on_core_small &&
            !big_mgr.on_core(big_mgr.N0 - half_N0)) {
          long peer = big_mgr.get_peer(big_mgr.N0 - half_N0);
          cons.print<LOG_DEBUG>(
              format("Scheduling to send plane %d (low, 3) to %d") % i % peer);
          U_Plane *tmp2_plane = big_mgr._newPlane();
          request_array[small_mgr.N0] = comm->Irecv(
              tmp2_plane->get_array().data(),
              tmp2_plane->get_array().num_elements(),
              translateMPIType<complex_element>(), peer, io_id);
          request_planes[small_mgr.N0] = tmp2_plane;
          request_io[small_mgr.N0] = true;
          if (FFTW_HELPER_CHATTY)
            cons.print<LOG_DEBUG>("Finished");
        }
        if (i == half_N0 && !on_core_small &&
            big_mgr.on_core(big_mgr.N0 - half_N0)) {
          long peer = small_mgr.get_peer(half_N0);
          if (FFTW_HELPER_CHATTY)
            cons.print<LOG_DEBUG>(
                format("Scheduling to recv plane %d (low, 3) from %d") % i %
                peer);

          U_Plane *tmp2_plane = big_mgr._newPlane();

          c_util::_flat_copy_2d_array(
              big_mgr, small_mgr, tmp2_plane->get_array(),
              in_modes[big_mgr.N0 - half_N0]);

          request_array[small_mgr.N0] = comm->Isend(
              tmp2_plane->get_array().data(),
              tmp2_plane->get_array().num_elements(),
              translateMPIType<complex_element>(), peer, io_id);
          request_planes[small_mgr.N0] = tmp2_plane;
          request_io[small_mgr.N0] = true;
          if (FFTW_HELPER_CHATTY)
            cons.print<LOG_DEBUG>("Finished");
        }
      }

      // Note down for later destruction
      request_planes[i] = tmp_plane;
    }

    // Now do copy of lines already present. First the positive low freq
    for (long i = 0; i < small_mgr.N0 / 2; i++) {
      if (!small_mgr.on_core(i) || !big_mgr.on_core(i))
        continue;

      if (FFTW_HELPER_CHATTY)
        cons.print<LOG_DEBUG>(
            format("copying plane in place %d -> %d") % i % i);
      c_util::_copy_sub_2d_plane(big_mgr, small_mgr, out_modes[i], in_modes[i]);
    }

    // Next the negative low freq
    for (long i = small_mgr.N0 / 2 + 1; i < small_mgr.N0; i++) {
      long big_plane = big_mgr.N0 - small_mgr.N0 + i;
      if (!small_mgr.on_core(i) || !big_mgr.on_core(big_plane))
        continue;

      long input_plane = upgrading ? i : big_plane;
      long output_plane = upgrading ? big_plane : i;

      if (FFTW_HELPER_CHATTY)
        cons.print<LOG_DEBUG>(
            format("copying plane in place %d -> %d") % input_plane %
            output_plane);
      c_util::_copy_sub_2d_plane(
          big_mgr, small_mgr, out_modes[output_plane], in_modes[input_plane]);
    }

    for (long i = 0; i < small_mgr.N0 / 2; i++) {
      if (FFTW_HELPER_CHATTY)
        cons.print<LOG_DEBUG>(
            format("small.on_core(%d) = %d, big_mgr.on_core(%d) = %d") % i %
            small_mgr.on_core(i) % i % big_mgr.on_core(i));
      if ((upgrading && (small_mgr.on_core(i) || !big_mgr.on_core(i))) ||
          (!upgrading && (!small_mgr.on_core(i) || big_mgr.on_core(i))))
        continue;

      cons.c_assert(
          request_planes[i] != 0,
          str(format("There should be a pending recv I/O for %d") % i));

      if (FFTW_HELPER_CHATTY)
        cons.print<LOG_DEBUG>(
            format("Importing plane %d (big is %d)") % i % (i));

      request_array[i].wait(&status);
      c_util::_copy_sub_2d_plane_flat(
          big_mgr, small_mgr, out_modes[i], request_planes[i]->get_array());
      internal::safe_delete(request_planes[i]);
    }

    // Half N0 is special. It may broadcast or gather from several cores.

    if (FFTW_HELPER_CHATTY)
      cons.print<LOG_DEBUG>("Half plane");

    internal::Nyquist_adjust<T, upgrading>::handle(
        small_mgr, big_mgr, request_planes, request_io, request_array, in_modes,
        out_modes);

    if (FFTW_HELPER_CHATTY)
      cons.print<LOG_DEBUG>("Half plane done");

    for (long i = small_mgr.N0 / 2 + 1; i < small_mgr.N0; i++) {
      long big_plane = big_mgr.N0 - small_mgr.N0 + i;
      if (FFTW_HELPER_CHATTY)
        cons.print<LOG_DEBUG>(
            format("small.on_core(%d) = %d, big_mgr.on_core(%d) = %d") % i %
            small_mgr.on_core(i) % big_plane % big_mgr.on_core(big_plane));

      long input_plane = upgrading ? i : big_plane;
      long output_plane = upgrading ? big_plane : i;

      if ((upgrading &&
           (small_mgr.on_core(i) || !big_mgr.on_core(big_plane))) ||
          (!upgrading && (!small_mgr.on_core(i) || big_mgr.on_core(big_plane))))
        continue;

      cons.c_assert(
          request_planes[i] != 0,
          str(format("There should be a pending recv I/O for %d") % i));

      if (FFTW_HELPER_CHATTY)
        cons.print<LOG_DEBUG>(
            format("Importing plane %d (big is %d)") % i % big_plane);

      request_array[i].wait(&status);
      request_io[i] = false;
      c_util::_copy_sub_2d_plane_flat(
          big_mgr, small_mgr, out_modes[output_plane],
          request_planes[i]->get_array());
      internal::safe_delete(request_planes[i]);
    }

    // Cleanup the send queue.
    for (long i = 0; i <= small_mgr.N0; i++) {
      if (request_io[i]) {
        if (FFTW_HELPER_CHATTY)
          cons.print<LOG_DEBUG>(format("Waiting for I/O on  plane %d ") % i);
        request_array[i].wait(&status);
      }
    }
    // No "=" here. The last plane is a potential duplicate.
    long last_plane = upgrading ? small_mgr.N0 : small_mgr.N0 + 1;
    for (long i = 0; i < last_plane; i++) {
      internal::safe_delete(request_planes[i]);
    }
  }

  template <typename Plane>
  void fixBaseNyquist(Plane &plane, self_t const &in_mgr) {
    typedef typename Plane::index_range range;
    typename Plane::index_gen indices;

    if (N1 > in_mgr.N1) {
      array::scalePlane(plane[indices[range()][in_mgr.N1 / 2][range()]], 0.5);
      array::scalePlane(
          plane[indices[range()][N1 - in_mgr.N1 / 2][range()]], 0.5);
    }
    if (N2 > in_mgr.N2) {
      array::scalePlane(plane[indices[range()][range()][in_mgr.N2 / 2]], 0.5);
    }
  }

  /* This function upgrade the multi_array in_modes, described by in_mgr
       * to out_modes described by this manager.
       */
  template <typename InArray, typename OutArray>
  void upgrade_complex(
      self_t const &in_mgr, const InArray &in_modes, OutArray &out_modes) {
    ConsoleContext<LOG_DEBUG> ctx("Upgrading modes");
    using namespace boost::lambda;
    using boost::lambda::_1;

    ctx.print(
        boost::format("Going from (%d,%d,%d) to (%d,%d,%d)") % in_mgr.N0 %
        in_mgr.N1 % in_mgr.N2 % N0 % N1 % N2);

    if (in_mgr.N0 == N0 && in_mgr.N1 == N1 && in_mgr.N2 == N2) {
      LibLSS::copy_array(out_modes, in_modes);
      return;
    }

    // Same ordering please
    Console::instance().c_assert(
        N0 >= in_mgr.N0, "N0 is not bigger than in_mgr.N0");
    Console::instance().c_assert(
        N1 >= in_mgr.N1, "N1 is not bigger than in_mgr.N1");
    Console::instance().c_assert(
        N2 >= in_mgr.N2, "N2 is not bigger than in_mgr.N2");

    _ud_grade<true>(*this, in_mgr, *this, in_modes, out_modes);

    // Now we have to correct Nyquist planes as they are twice too big
    if (N0 != in_mgr.N0) {
      if (on_core(in_mgr.N0 / 2)) {
        array::scalePlane(out_modes[in_mgr.N0 / 2], 0.5);
      }
      if (on_core(N0 - in_mgr.N0 / 2)) {
        array::scalePlane(out_modes[N0 - in_mgr.N0 / 2], 0.5);
      }
    }
    fixBaseNyquist(out_modes, in_mgr);
  }

  template <
      typename InArray, typename NyqArray, typename Functor1, typename Functor2>
  void _degradeExchange(
      self_t const &in_mgr, const InArray &in_modes, NyqArray &nyqPlane,
#ifdef DEBUG_MPI_DEGRADE
      boost::multi_array<bool, 1> &nyqCheck,
#endif
      const Functor1 &f, ptrdiff_t s, ptrdiff_t e, const Functor2 &g,
      ptrdiff_t in_s, ptrdiff_t in_e, RequestArray &req,
      RequestArray &req_send) {
    typedef typename InArray::index_range in_range;
    typename InArray::index_gen in_indices;
    long half_N2 = N2 / 2;
    Console &cons = Console::instance();
    long thisRank = comm->rank();

    for (long i = std::max(s, startN0); i < std::min(e, startN0 + localN0);
         i++) {
      long ci = f(i);
      long peer = in_mgr.get_peer(ci);
      long req_idx = ci;

      if (!in_mgr.on_core(ci)) {
        // One comm only please
        if (!req[req_idx].is_active()) {
          if (FFTW_HELPER_CHATTY)
            cons.print<LOG_DEBUG>(
                boost::format("Need plane %lg on core %d") % ci % peer);
          req[req_idx] = comm->IrecvT(&nyqPlane[ci][0], in_mgr.N1, peer, ci);
          nyqCheck[ci] = true;
        }
      } else {
        cons.c_assert(on_core(i), "Both lines are not on core");
        cons.print<LOG_DEBUG>(
            boost::format("Copying line %ld (sz=%ld -> %ld)") % ci %
            in_modes.shape()[1] % nyqPlane.shape()[1]);
        copy_array_rv(
            nyqPlane[ci],
            in_modes[in_indices[ci][in_range(0, in_mgr.N1)][half_N2]]);
        nyqCheck[ci] = true;
        if (FFTW_HELPER_CHATTY)
          cons.print<LOG_DEBUG>("Done");
      }
    }

    if (FFTW_HELPER_CHATTY)
      cons.print<LOG_DEBUG>(
          boost::format("For loop (in_s=%d, in_e=%d)") % in_s % in_e);
    for (long ci = std::max(in_s, in_mgr.startN0);
         ci < std::min(in_e, in_mgr.startN0 + in_mgr.localN0); ci++) {
      long i = g(ci);
      long peer = get_peer(i);
      long req_idx = peer + comm->size() * ci;
      if (FFTW_HELPER_CHATTY)
        cons.print<LOG_DEBUG>(
            boost::format("Consider to send plane %lg (%ld) to core %d") % ci %
            i % peer);
      if (!req_send[req_idx].is_active() && peer != thisRank) {
        if (FFTW_HELPER_CHATTY)
          cons.print<LOG_DEBUG>(
              boost::format("Send plane %lg to core %d") % ci % peer);
        cons.c_assert(!req[ci].is_active(), "Plane already allotted");
        copy_array_rv(
            nyqPlane[ci],
            in_modes[in_indices[ci][in_range(0, in_mgr.N1)][half_N2]]);
        req_send[req_idx] = comm->IsendT(&nyqPlane[ci][0], in_mgr.N1, peer, ci);
      }
    }
  }

  template <typename InArray, typename OutArray>
  void degrade_complex(
      self_t const &in_mgr, const InArray &in_modes, OutArray &out_modes) {
    ConsoleContext<LOG_DEBUG> ctx("Degrading modes");
    using namespace boost::lambda;
    using boost::lambda::_1;
    typedef typename Plane::index_range range;
    typename Plane::index_gen indices;

    ctx.print(
        boost::format("Going from (%d,%d,%d) to (%d,%d,%d)") % in_mgr.N0 %
        in_mgr.N1 % in_mgr.N2 % N0 % N1 % N2);

    if (in_mgr.N0 == N0 && in_mgr.N1 == N1 && in_mgr.N2 == N2) {
      LibLSS::copy_array(out_modes, in_modes);
      return;
    }

    // Same ordering please
    Console::instance().c_assert(
        N0 <= in_mgr.N1, "N0 is not smaller than in_mgr.N0");
    Console::instance().c_assert(
        N1 <= in_mgr.N1, "N1 is not smaller than in_mgr.N1");
    Console::instance().c_assert(
        N2 <= in_mgr.N2, "N2 is not smaller than in_mgr.N2");

    _ud_grade<false>(*this, *this, in_mgr, in_modes, out_modes);

    if (N2 != in_mgr.N2) {
      typedef typename ArrayFourierPlane::const_reference InArrayPlane;
      typedef typename OutArray::reference OutArrayPlane;
      using boost::lambda::_1;
      ArrayFourierPlane nyqPlane(boost::extents[in_mgr.N0][in_mgr.N1]);
#ifdef DEBUG_MPI_DEGRADE
      boost::multi_array<bool, 1> nyqCheck(boost::extents[in_mgr.N0]);
#endif
      RequestArray req(boost::extents[in_mgr.N0]);
      RequestArray req_send(boost::extents[in_mgr.N0 * comm->size()]);
      StatusArray status(boost::extents[in_mgr.N0]);
      StatusArray status_send(boost::extents[in_mgr.N0 * comm->size()]);

      long half_N2 = N2 / 2;
      long in_half_N2 = N2 / 2;

      // One half sum has not been done.
      // In MPI it will require recapturing part of the N2_HC plane and
      // adding half of its value with conjugation.

      //
      // First we gather all required lines for the collapse of Nyquist plane
      //

      // One round for the forward conjugate planes
      _degradeExchange(
          in_mgr, in_modes, nyqPlane,
#ifdef DEBUG_MPI_DEGRADE
          nyqCheck,
#endif
          // Forward
          ((in_mgr.N0 - _1) %
           in_mgr.N0), // transform local plane -> conjugate index
          0, N0 / 2 + 1,
          // Inverse
          (in_mgr.N0 - _1), // transform conjugate index -> local plane
          in_mgr.N0 - N0 / 2, in_mgr.N0,

          req, req_send);

      // One round for the not conjugate planes
      _degradeExchange(
          in_mgr, in_modes, nyqPlane,
#ifdef DEBUG_MPI_DEGRADE
          nyqCheck,
#endif
          // Forward
          _1, // identity
          0, N0 / 2 + 1,
          // Inverse
          _1, // identity
          0, N0 / 2 + 1,

          req, req_send);

      // One round for the backward not conjugate planes
      _degradeExchange(
          in_mgr, in_modes, nyqPlane,
#ifdef DEBUG_MPI_DEGRADE
          nyqCheck,
#endif
          // Forward
          N0 - _1, N0 / 2, N0,
          // Inverse
          (N0 - _1) % N0, 0, N0 / 2 + 1,

          req, req_send);

      // One round for the backward conjugate planes
      _degradeExchange(
          in_mgr, in_modes, nyqPlane,
#ifdef DEBUG_MPI_DEGRADE
          nyqCheck,
#endif
          // Forward
          in_mgr.N0 - N0 + _1, N0 / 2, N0,
          // Inverse
          N0 - in_mgr.N0 + _1, in_mgr.N0 - N0 / 2, in_mgr.N0,

          req, req_send);

      if (FFTW_HELPER_CHATTY)
        ctx.print("All IOs scheduled");

      for (long i = startN0; i < std::min(N0 / 2, startN0 + localN0); i++) {
        long ci = (in_mgr.N0 - i) % in_mgr.N0, qi = i;
        OutArrayPlane out_i = out_modes[i];
        InArrayPlane in_qi = nyqPlane[qi], in_ci = nyqPlane[ci];

        if (FFTW_HELPER_CHATTY)
          ctx.print(boost::format("wait for ci=%d") % ci);
        req[ci].wait();
        if (FFTW_HELPER_CHATTY)
          ctx.print(boost::format("wait for qi=%d") % qi);
        req[qi].wait();
        if (FFTW_HELPER_CHATTY)
          ctx.print("Done waiting");
        CHECK_NYQ(qi);
        CHECK_NYQ(ci);

        for (long j = 0; j < N1 / 2; j++) {
          long cj = (in_mgr.N1 - j) % in_mgr.N1;
          long qj = j;
          out_modes[i][j][half_N2] = 0.5 * (in_qi[qj] + std::conj(in_ci[cj]));
        }

        {
          long cj = N1 / 2, qj = in_mgr.N1 - N1 / 2;

          out_i[N1 / 2][half_N2] = 0.25 * in_qi[cj];
          out_i[N1 / 2][half_N2] += 0.25 * std::conj(in_ci[qj]);
          out_i[N1 / 2][half_N2] += 0.25 * (in_qi[qj]);
          out_i[N1 / 2][half_N2] += 0.25 * std::conj(in_ci[cj]);
        }

        for (long j = N1 / 2 + 1; j < N1; j++) {
          long cj = (N1 - j), qj = in_mgr.N1 - N1 + j;
          out_i[j][half_N2] = 0.5 * (in_qi[qj]);
          out_i[j][half_N2] += 0.5 * std::conj(in_ci[cj]);
        }
      }

      // This one is easier
      if (on_core(N0 / 2)) {
        long i = N0 / 2, qi = N0 / 2, ci = in_mgr.N0 - N0 / 2;
        OutArrayPlane out_i = out_modes[i];
        InArrayPlane in_qi = nyqPlane[qi], in_ci = nyqPlane[ci];

        req[ci].wait();
        req[qi].wait();
        CHECK_NYQ(qi);
        CHECK_NYQ(ci);
        for (long j = 0; j < N1 / 2; j++) {
          long cj = (in_mgr.N1 - j) % in_mgr.N1;
          long qj = j;

          out_i[j][half_N2] = 0.25 * (in_ci[qj]);
          out_i[j][half_N2] += 0.25 * std::conj(in_qi[cj]);
          out_i[j][half_N2] += 0.25 * (in_qi[qj]);
          out_i[j][half_N2] += 0.25 * std::conj(in_ci[cj]);
        }

        {
          long cj = in_mgr.N1 - N1 / 2;
          long qj = N1 / 2;
          long j = N1 / 2;

          out_modes[i][j][half_N2] =
              0.25 * (in_qi[qj].real() + in_ci[qj].real() + in_qi[cj].real() +
                      in_ci[cj].real());
        }

        for (long j = N1 / 2 + 1; j < N1; j++) {
          long cj = (N1 - j), qj = in_mgr.N1 - N1 + j;
          out_modes[i][j][half_N2] = 0.25 * (in_ci[qj]);
          out_modes[i][j][half_N2] += 0.25 * std::conj(in_qi[cj]);
          out_modes[i][j][half_N2] += 0.25 * (in_qi[qj]);
          out_modes[i][j][half_N2] += 0.25 * std::conj(in_ci[cj]);
        }
      }

      // Resume the conjugate planes. It is [N0/2+1,N0[ intersected with [startN0, startN0+localN0[.
      for (long i = std::max(startN0, N0 / 2 + 1);
           i < std::min(startN0 + localN0, N0); i++) {
        long ci = N0 - i, qi = in_mgr.N0 - N0 + i;
        // Problem: we need ci and qi planes.
        InArrayPlane in_qi = nyqPlane[qi], in_ci = nyqPlane[ci];
        OutArrayPlane out_i = out_modes[i];

        if (FFTW_HELPER_CHATTY)
          ctx.print(boost::format("wait for ci=%d") % ci);
        req[ci].wait();
        if (FFTW_HELPER_CHATTY)
          ctx.print(boost::format("wait for qi=%d") % qi);
        req[qi].wait();
        if (FFTW_HELPER_CHATTY)
          ctx.print("Done waiting");
        CHECK_NYQ(qi);
        CHECK_NYQ(ci);

        for (long j = 0; j < N1 / 2; j++) {
          long cj = (in_mgr.N1 - j) % in_mgr.N1;
          long qj = j;
          out_i[j][half_N2] = 0.5 * (in_qi[qj]);
          out_i[j][half_N2] += 0.5 * std::conj(in_ci[cj]);
        }

        {
          long cj = N1 / 2, qj = in_mgr.N1 - N1 / 2;
          typename OutArrayPlane::reference::reference node =
              out_i[N1 / 2][half_N2];

          node = 0.25 * in_qi[cj];
          node += 0.25 * std::conj(in_ci[qj]);
          node += 0.25 * (in_qi[qj]);
          node += 0.25 * std::conj(in_ci[cj]);
        }

        for (long j = N1 / 2 + 1; j < N1; j++) {
          long cj = (N1 - j), qj = in_mgr.N1 - N1 + j;
          out_i[j][half_N2] = 0.5 * (in_qi[qj]);
          out_i[j][half_N2] += 0.5 * std::conj(in_ci[cj]);
        }
      }

      if (FFTW_HELPER_CHATTY)
        ctx.print("Wait for all receive operations to finish");
      comm->WaitAll(req, status);
      if (FFTW_HELPER_CHATTY)
        ctx.print("Wait for all send operations to finish");
      comm->WaitAll(req_send, status_send);
    }
  }

  template <typename InArray, typename OutArray>
  void degrade_real(
      self_t const &in_mgr, const InArray &in_density, OutArray &out_density) {
    int rx = in_mgr.N0 / N0, ry = in_mgr.N1 / N1, rz = in_mgr.N2 / N2;

    array::fill(out_density, 0);

#pragma omp parallel for schedule(static)
    for (long ix = 0; ix < in_mgr.N0; ix++) {
      int qx = ix / rx;

      for (long iy = 0; iy < in_mgr.N1; iy++) {
        int qy = iy / ry;

        for (long iz = 0; iz < in_mgr.N2; iz++) {
          int qz = iz / rz;
          out_density[qx][qy][qz] += in_density[ix][iy][iz];
        }
      }
    }

    array::scaleArray3d(
        out_density, 1 / (double(rx) * double(ry) * double(rz)));
  }

private:
  void init_peer_upgrade_system() {
    using boost::extents;
    using boost::format;
    ConsoleContext<LOG_DEBUG> ctx("Initializing peer system");

    ctx.format("Comm size is %d", comm->size());

    boost::multi_array<ptrdiff_t, 1> all_N0s(extents[comm->size()]);
    int localAccumN0 = 0;

    peer.resize(extents[N0]);

    // Figure out the peer for each line of Nyquist planes
    // First gather the MPI structure

    comm->all_gather_t(&localN0, 1, all_N0s.data(), 1);

    if (FFTW_HELPER_CHATTY)
      ctx.print("Peers: ");

    for (int p = 0; p < comm->size(); p++) {
      if (FFTW_HELPER_CHATTY)
        ctx.format(" N0[%d] = %d", p, all_N0s[p]);
      // Find the position of the mirror of this line
      for (int i = 0; i < all_N0s[p]; i++)
        peer[i + localAccumN0] = p;
      localAccumN0 += all_N0s[p];
    }
  }
};
