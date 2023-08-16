/*+
    ARES/HADES/BORG Package -- ./extra/dm_sheet/libLSS/physics/velocity/velocity_sic.cpp
    Copyright (C) 2019-2020 Florent Leclercq <florent.leclercq@polytechnique.org>
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/physics/velocity/velocity_sic.hpp"
#include "libLSS/physics/dm_sheet/dm_sheet.hpp"

using namespace LibLSS;
using namespace LibLSS::VelocityModel;

typedef U_Array<double, 4> U_VFieldType;
typedef U_Array<double, 1> U_ParticleBasedScalar;
typedef U_Array<double, 2> U_ParticleBasedArray;

typedef ParticleBasedForwardModel::PhaseSubArray::index_range range;

/**
* @brief 
* 
* This computes the velocity field by CiC projection of particles
*
* @param VelocityField 
*/
void SICModel::getVelocityField(arrayVelocityField_t VelocityField) {
  boost::multi_array_types::index_gen i_gen;
  typedef boost::multi_array_types::index_range range;

  LibLSS::ConsoleContext<LOG_DEBUG> ctx("SICModel::getVelocityField");

  // get particles' positions and velocities from the forward model
  auto ids = p_model->getLagrangianIdentifiers();
  auto positions = p_model->getParticlePositions();
  auto velocities = p_model->getParticleVelocities();
  unsigned int srate = p_model->getSupersamplingRate();

  // get number of particles, box specifications, FFTW manager and MPI communicator from forward model
  size_t numParticles = p_model->getNumberOfParticles();
  BoxModel model_box = model->get_box_model();
  BoxModel box = outputBox;
  MPI_Communication *comm = model->communicator();
  size_t startN0 = mgr.startN0;
  size_t endN0 = startN0 + mgr.localN0;
  size_t N1 = mgr.N1;
  size_t N2 = mgr.N2;
  typedef std::unique_ptr<U_Array<double, 3>> U_3d;
  typedef std::unique_ptr<U_Array<double, 4>> U_4d;

  // initialize VelocityField and MassField to zero
  fwrap(VelocityField) = 0;

  size_t thread_max = smp_get_max_threads();
  std::unique_ptr<U_3d[]> threaded_density_array(new U_3d[thread_max]);
  std::unique_ptr<U_4d[]> threaded_velocity_array(new U_4d[thread_max]);

  ctx.format("Allocating temporary output array, max_threads = %d", thread_max);
  for (size_t i = 0; i < thread_max; i++) {
    threaded_density_array[i] =
        U_3d(new U_3d::element_type(boost::extents[box.N0][box.N1][box.N2]));
    threaded_velocity_array[i] =
        U_4d(new U_4d::element_type(boost::extents[box.N0][box.N1][box.N2][3]));
  }

  ctx.print("Go parallel and compute velocity/density");

#pragma omp parallel
  {
    size_t tid = smp_get_thread_id();
    size_t id_min = tid * numParticles / smp_get_num_threads();
    size_t id_max = (tid + 1) * numParticles / smp_get_num_threads();

    fwrap(*threaded_density_array[tid]) = 0;
    fwrap(*threaded_velocity_array[tid]) = 0;

    DM_Sheet::get_mass_and_momenta_tetrahedra(
        ids[i_gen[range(id_min, id_max)]], positions, velocities, model_box.L0,
        model_box.L1, model_box.L2, srate * model_box.N0, srate * model_box.N1,
        srate * model_box.N2, box.N0, box.N1, box.N2,
        threaded_density_array[tid]->get_array(),
        threaded_velocity_array[tid]->get_array());
  }

  // divide momenta by density and normalize to get the velocity field

  ctx.print("Final reduction");
  for (size_t i = 0; i < thread_max; i++) {
    if (i > 0) {
      auto out_w = fwrap(threaded_density_array[0]->get_array());
      out_w = out_w + fwrap(threaded_density_array[i]->get_array());
    }
    for (int k = 0; k < 3; k++) {
      auto out_v = fwrap(VelocityField[k]);
      out_v =
          out_v + fwrap(threaded_velocity_array[i]
                            ->get_array()[i_gen[range()][range()][range()][k]]);
    }
  }

  auto out = fwrap(threaded_density_array[0]->get_array());
  for (unsigned int k = 0; k < 3; k++) {
    auto v = fwrap(VelocityField[i_gen[k][range()][range()][range()]]);
    v = p_model->getVelocityMultiplier() * v / out;
  }

} //getVelocityField

void SICModel::computeAdjointModel(arrayVelocityField_view_t AGVelocityField) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

} //computeAdjointModel

void LibLSS::computeSICVelocityField(
    DM_Sheet::arrayID_t const &identifiers,
    DM_Sheet::arrayPosition_t const &pos, DM_Sheet::arrayVelocity_t const &vels,
    double L, int N, int Ng, boost::multi_array_ref<double, 3> &DensityField,
    VelocityModel::ParticleBasedModel::arrayVelocityField_t &VelocityField) {
  boost::multi_array_types::index_gen i_gen;
  typedef boost::multi_array_types::index_range range;

  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  // get particles' positions and velocities from the forward model
  auto ids = identifiers[i_gen[range()]];
  auto positions = pos[i_gen[range()][range()]];
  auto velocities = vels[i_gen[range()][range()]];

  long numParticles = ids.shape()[0];

  typedef std::unique_ptr<U_Array<double, 3>> U_3d;
  typedef std::unique_ptr<U_Array<double, 4>> U_4d;

  // initialize VelocityField and MassField to zero
  fwrap(VelocityField) = 0;

  size_t thread_max = smp_get_max_threads();
  std::unique_ptr<U_3d[]> threaded_density_array(new U_3d[thread_max]);
  std::unique_ptr<U_4d[]> threaded_velocity_array(new U_4d[thread_max]);

  ctx.format("Allocating temporary output array, max_threads = %d", thread_max);
  for (size_t i = 0; i < thread_max; i++) {
    threaded_density_array[i] =
        U_3d(new U_3d::element_type(boost::extents[Ng][Ng][Ng]));
    threaded_velocity_array[i] =
        U_4d(new U_4d::element_type(boost::extents[Ng][Ng][Ng][3]));
  }

  ctx.print("Go parallel and compute velocity/density");

#pragma omp parallel
  {
    size_t tid = smp_get_thread_id();
    size_t id_min = tid * numParticles / smp_get_num_threads();
    size_t id_max = (tid + 1) * numParticles / smp_get_num_threads();

    fwrap(*threaded_density_array[tid]) = 0;
    fwrap(*threaded_velocity_array[tid]) = 0;

    DM_Sheet::get_mass_and_momenta_tetrahedra(
        ids[i_gen[range(id_min, id_max)]], positions, velocities, L, L, L, N, N,
        N, Ng, Ng, Ng, threaded_density_array[tid]->get_array(),
        threaded_velocity_array[tid]->get_array());
  }

  // divide momenta by density and normalize to get the velocity field

  ctx.print("Final reduction");
  auto out_w = fwrap(threaded_density_array[0]->get_array());
  for (size_t i = 0; i < thread_max; i++) {
    if (i > 0) {
      out_w = out_w + fwrap(threaded_density_array[i]->get_array());
    }
    for (int k = 0; k < 3; k++) {
      auto out_v = fwrap(VelocityField[k]);
      out_v =
          out_v + fwrap(threaded_velocity_array[i]
                            ->get_array()[i_gen[range()][range()][range()][k]]);
    }
  }

  for (unsigned int k = 0; k < 3; k++) {
    auto v = fwrap(VelocityField[i_gen[k][range()][range()][range()]]);
    v = v / out_w;
  }
  fwrap(DensityField) = out_w;
}

// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Florent Leclercq
// ARES TAG: year(0) = 2019-2020
// ARES TAG: email(0) = florent.leclercq@polytechnique.org
// ARES TAG: name(1) = Guilhem Lavaux
// ARES TAG: year(1) = 2019-2020
// ARES TAG: email(1) = guilhem.lavaux@iap.fr
