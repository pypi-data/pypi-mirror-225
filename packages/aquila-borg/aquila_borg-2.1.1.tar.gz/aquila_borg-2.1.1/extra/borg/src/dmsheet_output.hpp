

#ifdef DM_SHEET_PRESENT

#  include "libLSS/physics/dm_sheet/dm_sheet.hpp"

void build_dmsheet_density(
    BORGForwardModel *model, boost::multi_array_ref<double, 3> &out_n_field,
    boost::multi_array_ref<double, 3> &out_field,
    boost::multi_array_ref<double, 4> &out_v_field, size_t Ng0, size_t Ng1,
    size_t Ng2) {
  boost::multi_array_types::index_gen i_gen;
  typedef boost::multi_array_types::index_range range;

  ConsoleContext<LOG_VERBOSE> ctx("dmsheet density computation");
  auto p_model = dynamic_cast<ParticleBasedForwardModel *>(model);

  if (p_model == 0)
    error_helper<ErrorBadState>("Not a particle based forward model.");

  auto ids = p_model->getLagrangianIdentifiers();
  size_t numParticles = p_model->getNumberOfParticles();
  BoxModel box = model->get_box_model();
  unsigned int srate = p_model->getSupersamplingRate();

  auto positions = p_model->getParticlePositions();
  auto velocities = p_model->getParticleVelocities();

  LibLSS::array::fill(out_n_field, 0);
  LibLSS::array::fill(out_field, 0);
  LibLSS::array::fill(out_v_field, 0);

  size_t thread_max = smp_get_max_threads();
  typedef std::unique_ptr<U_Array<double, 3>> U_3d;
  typedef std::unique_ptr<U_Array<double, 4>> U_4d;
  std::unique_ptr<U_3d[]> threaded_nbstreams_array(new U_3d[thread_max]);
  std::unique_ptr<U_3d[]> threaded_density_array(new U_3d[thread_max]);
  std::unique_ptr<U_4d[]> threaded_velocity_array(new U_4d[thread_max]);

  ctx.print(
      format("Allocating temporary output array, max_threads = %d") %
      thread_max);
  for (size_t i = 0; i < thread_max; i++) {
    threaded_nbstreams_array[i] =
        U_3d(new U_3d::element_type(boost::extents[Ng0][Ng1][Ng2]));
    threaded_density_array[i] =
        U_3d(new U_3d::element_type(boost::extents[Ng0][Ng1][Ng2]));
    threaded_velocity_array[i] =
        U_4d(new U_4d::element_type(boost::extents[Ng0][Ng1][Ng2][3]));
  }

  ctx.print("Go parallel and compute velocity/density");

// This is strongly inefficient memory wise. However we need to make the
// API flexible to allow for array views to be passed to get_density_tetrahedra
// for efficiency to happen.
#  pragma omp parallel
  {
    size_t tid = smp_get_thread_id();
    size_t id_min = tid * numParticles / smp_get_num_threads();
    size_t id_max = (tid + 1) * numParticles / smp_get_num_threads();
    fwrap(*threaded_nbstreams_array[tid]) = 0;
    fwrap(*threaded_density_array[tid]) = 0;
    fwrap(*threaded_velocity_array[tid]) = 0;

    DM_Sheet::get_nbstreams_mass_and_momenta_tetrahedra(
        ids[i_gen[range(id_min, id_max)]], positions, velocities, box.L0,
        box.L1, box.L2, srate * box.N0, srate * box.N1, srate * box.N2, Ng0,
        Ng1, Ng2, threaded_nbstreams_array[tid]->get_array(),
        threaded_density_array[tid]->get_array(),
        threaded_velocity_array[tid]->get_array());
  }

  ctx.print("Final reduction");
  auto out_n = fwrap(out_n_field);
  auto out = fwrap(out_field);
  auto out_v = fwrap(out_v_field);
  for (size_t i = 0; i < thread_max; i++) {
    out_n = out_n + fwrap(threaded_nbstreams_array[i]->get_array());
    out = out + fwrap(threaded_density_array[i]->get_array());
    out_v = out_v + fwrap(threaded_velocity_array[i]->get_array());
  }

  // divide momenta by density and normalize to get the velocity field
  for (unsigned int k = 0; k < 3; k++) {
    auto v = fwrap(out_v_field[i_gen[range()][range()][range()][k]]);
    v = p_model->getVelocityMultiplier() * v / out;
  }
}

#else

void build_dmsheet_density(
    BORGForwardModel *model, boost::multi_array_ref<double, 3> &out_n_field,
    boost::multi_array_ref<double, 3> &out_field,
    boost::multi_array_ref<double, 4> &out_v_field, size_t Ng0, size_t Ng1,
    size_t Ng2) {
  error_helper<ErrorNotImplemented>("DM_Sheet module is not bundled.");
}

#endif

std::vector<int> build_dimensions(std::string const &s_dims) {
  std::vector<int> dims;
  std::vector<std::string> a_dims;

  iter_split(a_dims, s_dims, boost::first_finder("x"));

  for (auto const &elt : a_dims) {
    dims.push_back(boost::lexical_cast<int>(elt));
  }
  return dims;
}

void handle_dmsheet(
    po::variables_map &vm, std::shared_ptr<CosmoTool::H5_CommonFileGroup> f,
    BORGForwardModel *model) {
  auto box = model->get_box_model();
  int Ng0, Ng1, Ng2;
  if (vm.count("dmsheet_grid")) {
    auto Ngs = build_dimensions(vm["dmsheet_grid"].as<std::string>());
    if (Ngs.size() != 3)
      error_helper<ErrorParams>("Dimensions must be 3");
    Ng0 = Ngs[0];
    Ng1 = Ngs[1];
    Ng2 = Ngs[2];
  } else {
    Ng0 = box.N0;
    Ng1 = box.N1;
    Ng2 = box.N2;
  }
  U_DensityType nfield(boost::extents[Ng0][Ng1][Ng2]);
  U_DensityType dmfield(boost::extents[Ng0][Ng1][Ng2]);
  U_VFieldType vfield(boost::extents[Ng0][Ng1][Ng2][3]);

  build_dmsheet_density(
      model, nfield.get_array(), dmfield.get_array(), vfield.get_array(), Ng0,
      Ng1, Ng2);
  if (f) {
    hdf5_write_array(*f, "dmsheet_nbstreams", nfield.get_array());
    hdf5_write_array(*f, "dmsheet_density", dmfield.get_array());
    hdf5_write_array(*f, "dmsheet_velocity", vfield.get_array());
  } else {
    error_helper<ErrorBadState>("File must be opened on all nodes.");
  }
}
