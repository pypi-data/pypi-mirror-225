#include "libLSS/physics/classic_cic.hpp"

template <typename Array, typename SourceArray>
void rebuild_density(
    std::shared_ptr<FFTW_Manager_3d<double>> &mgr, Array &&out,
    SourceArray &&src) {
  ConsoleContext<LOG_VERBOSE> ctx("Rebuilding a field");
  MPI_Communication *comm = mgr->getComm();
  boost::multi_array<size_t, 1> Nplanes(boost::extents[comm->size()]);

  // Build number of planes on each core
  {
    int core = 0;
    for (size_t i = 0; i < mgr->N0; i++) {
      if (mgr->get_peer(i) != core) {
        core++;
      }
      Nplanes[core]++;
    }
  }

  auto mpi_t =
      translateMPIType<typename std::remove_reference<Array>::type::element>();

  if (comm->rank() == 0) {
    size_t plane = 0;
    typedef typename std::remove_reference<SourceArray>::type source_t;
    typedef typename std::remove_reference<Array>::type array_t;
    typename array_t::index_gen i_gen;
    typename source_t::index_gen i_gen_s;
    typedef typename array_t::index_range range;

    // This will copy the first elements in the output
    ctx.print(
        format("Copy source part (shape %d x %d x %d) to local (shape %d x %d "
               "x %d)") %
        src.shape()[0] % src.shape()[1] % src.shape()[2] % out.shape()[0] %
        out.shape()[1] % out.shape()[2]);

    LibLSS::copy_array_rv(
        out[i_gen[range(0, mgr->localN0)][range()][range(0, mgr->N2)]],
        src[i_gen_s[range(0, mgr->localN0)][range()][range(0, mgr->N2)]]);
    // Now copy the rest
    plane = Nplanes[0];
    for (int c = 1; c < comm->size(); c++) {
      ctx.print(boost::format("Receiving %d planes from %d") % Nplanes[c] % c);
      for (size_t p = 0; p < Nplanes[c]; p++) {
        for (size_t l = 0; l < mgr->N1; l++) {
          comm->recv(&out[plane + p][l][0], mgr->N2, mpi_t, c, p * mgr->N1 + l);
        }
      }
      plane += Nplanes[c];
    }
  } else {
    ctx.print("Sending bulks");
    for (size_t p = 0; p < mgr->localN0; p++) {
      for (size_t l = 0; l < mgr->N1; l++) {
        comm->send(
            &src[mgr->startN0 + p][l][0], mgr->N2, mpi_t, 0, p * mgr->N1 + l);
      }
    }
    //    comm->send(&src[0][0][0], mgr->localN0*mgr->N1*mgr->N2, MPI_DOUBLE, 0, 0);
  }
}

void build_velocity_field(
    ParticleBasedForwardModel *model, const BoxModel &box,
    U_VFieldType::array_type &vfield) {
  ConsoleContext<LOG_INFO> ctx("build_velocity_field");
  // First put particles in bins
  typedef ParticleBasedForwardModel Model;
  typedef typename Model::PhaseSubArray ParticleArray;
  typedef typename Model::PhaseSubArray VelocityArray;
  typedef boost::multi_array<double, 2> VectorArray;
  typedef UninitializedArray<VectorArray> U_VectorArray;

  size_t Np = size_t(model->getNumberOfParticles());
  U_VectorArray pos(boost::extents[Np][3]);
  U_VectorArray vel(boost::extents[Np][3]);
  U_VectorArray::array_type &positions = pos.get_array();
  U_VectorArray::array_type &velocities = vel.get_array();

  // The model already load balance correctly the particles for MPI
  LibLSS::copy_array(positions, model->getParticlePositions());
  LibLSS::copy_array(velocities, model->getParticleVelocities());
  fwrap(velocities) = fwrap(velocities) * model->getVelocityMultiplier(); // Output velocity at the correct af, in the correct unit

  boost::multi_array<double, 3> mass(boost::extents[box.N0][box.N1][box.N2]);
  double i_x = box.N0 / box.L0;
  double i_y = box.N1 / box.L1;
  double i_z = box.N2 / box.L2;
  double c0 = box.xmin0;
  double c1 = box.xmin1;
  double c2 = box.xmin2;
  auto &lo_mgr = dynamic_cast<BORGForwardModel *>(model)->lo_mgr;

  ctx.print(boost::format("Binning %d particles") % Np);

  LibLSS::array::fill(vfield, 0);
  if (CIC_WEIGHING) {
    typedef ClassicCloudInCell<double> CIC;
    typedef U_VFieldType::array_type::index_range range;
    U_VFieldType::array_type::index_gen i_gen;
    typename boost::remove_reference<VelocityArray>::type::index_gen i_gen_v;
    MPI_Communication *comm = lo_mgr->getComm();

    U_VFieldType u_loc_vfield(
        lo_mgr->extents_real(boost::extents[3], CIC::MPI_PLANE_LEAKAGE));
    auto &loc_vfield = u_loc_vfield.get_array();
    U_DensityType u_loc_mass(lo_mgr->extents_real(CIC::MPI_PLANE_LEAKAGE));
    auto &loc_mass = u_loc_mass.get_array();
    /*
    BalanceInfo balancing;


    balancing.allocate(comm, Np);
    particle_redistribute(balancing,
                          positions, ParticleArray& in_pos, VelocityArray& in_vel,
                          ParticleSelector selector);
*/

    fwrap(loc_vfield) = 0;
    fwrap(loc_mass) = 0;

#ifdef ARES_MPI_FFTW
    CIC_Tools::Periodic_MPI periodic(box.N0, box.N1, box.N2, comm);
#else
    CIC_Tools::Periodic periodic(box.N0, box.N1, box.N2);
#endif

    for (int k = 0; k < 3; k++) {
      auto v = loc_vfield[k];
      CIC::projection(
          positions, v, box.L0, box.L1, box.L2, box.N0, box.N1, box.N2,
          periodic, velocities[i_gen_v[range()][k]], Np);
    }

    CIC::projection(
        positions, loc_mass, box.L0, box.L1, box.L2, box.N0, box.N1, box.N2,
        periodic, CIC_Tools::DefaultWeight(), Np);

#ifdef ARES_MPI_FFTW
    // Now need to do reduction on the boundary planes
    density_exchange_planes<true>(
        comm, loc_mass, lo_mgr, CIC::MPI_PLANE_LEAKAGE);
    for (int k = 0; k < 3; k++)
      density_exchange_planes<true>(
          comm, loc_vfield[k], lo_mgr, CIC::MPI_PLANE_LEAKAGE);
#endif

    rebuild_density(lo_mgr, mass, loc_mass);
    for (int k = 0; k < 3; k++)
      rebuild_density(lo_mgr, vfield[k], loc_vfield[k]);
  }

  ctx.print("Weighing");
  if (lo_mgr->getComm()->rank() == 0) {
#pragma omp parallel for schedule(static) collapse(3)
    for (long ix = 0; ix < box.N0; ix++)
      for (long iy = 0; iy < box.N1; iy++)
        for (long iz = 0; iz < box.N2; iz++) {
          double M = mass[ix][iy][iz];
          if (M == 0)
            for (int k = 0; k < 3; k++)
              vfield[k][ix][iy][iz] = 0;
          else
            for (int k = 0; k < 3; k++)
              vfield[k][ix][iy][iz] /= M;
        }
  }
}
