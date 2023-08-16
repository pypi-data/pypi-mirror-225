/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/velocity/velocity_cic.cpp
    Copyright (C) 2019-2020 Florent Leclercq <florent.leclercq@polytechnique.org>
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/physics/velocity/velocity_cic.hpp"

using namespace LibLSS;
using namespace LibLSS::VelocityModel;

typedef U_Array<double, 4> U_VFieldType;
typedef U_Array<double, 1> U_ParticleBasedScalar;
typedef U_Array<double, 2> U_ParticleBasedArray;

ParticleBasedForwardModel::PhaseSubArray::index_gen i_gen_v;
typedef ParticleBasedForwardModel::PhaseSubArray::index_range range;

/**
* @brief 
* 
* This computes the velocity field by CiC projection of particles
*
* @param VelocityField 
*/
void CICModel::getVelocityField(arrayVelocityField_t VelocityField) {

  LibLSS::ConsoleContext<LOG_DEBUG> ctx("CICModel::getVelocityField");

  // get particles' positions and velocities from the forward model
  auto positions = p_model->getParticlePositions();
  auto velocities = p_model->getParticleVelocities();

  // get number of particles, box specifications, FFTW manager and MPI communicator from forward model
  size_t Np = size_t(p_model->getNumberOfParticles());
  BoxModel box = outputBox;
  MPI_Communication *comm = model->communicator();
  size_t startN0 = mgr.startN0;
  size_t endN0 = startN0 + mgr.localN0;
  size_t N1 = mgr.N1;
  size_t N2 = mgr.N2;
#ifdef ARES_MPI_FFTW
  CIC_Tools::Periodic_MPI periodic(box.N0, box.N1, box.N2, comm);
#else
  CIC_Tools::Periodic periodic(box.N0, box.N1, box.N2);
#endif

  // allocate array for mass field
  auto MassField_p = mgr.allocate_array(CIC::MPI_PLANE_LEAKAGE);
  auto &MassField = MassField_p.get_array();
  auto tmp_v_p = mgr.allocate_array(CIC::MPI_PLANE_LEAKAGE);
  auto &tmp_v = tmp_v_p.get_array();

  // initialize VelocityField and MassField to zero
  fwrap(VelocityField) = 0;
  fwrap(MassField) = 0;

  // compute the momentum field, to be divided by the mass field
  for (int k = 0; k < 3; k++) {
    auto v = VelocityField[k];
    fwrap(tmp_v) = 0;
    CIC::projection(
        positions, tmp_v, box.L0, box.L1, box.L2, box.N0, box.N1, box.N2,
        periodic, velocities[i_gen_v[range()][k]], Np);
    fwrap(v[mgr.strict_range()]) = tmp_v[mgr.strict_range()];
  }

  // compute the mass field
  CIC::projection(
      positions, MassField, box.L0, box.L1, box.L2, box.N0, box.N1, box.N2,
      periodic, CIC_Tools::DefaultWeight(), Np);

#if 0
  // TODO: Try that vectorization operation.
  fwrap(VelocityField[k]) =
      fwrap(VelocityField[k]) /
      mask(fwrap(MassField) == 0, zero<double, 3>(), 1.0 / fwrap(MassField));
#endif

// divide the momentum field by the mass field to get velocity field
#pragma omp parallel for collapse(3) schedule(static)
  for (long ix = startN0; ix < endN0; ix++)
    for (long iy = 0; iy < N1; iy++)
      for (long iz = 0; iz < N2; iz++) {
        double M = MassField[ix][iy][iz];
        if (M == 0) //FIXME this might be an issue
          for (unsigned int k = 0; k < 3; k++)
            VelocityField[k][ix][iy][iz] = 0;
        else
          for (unsigned int k = 0; k < 3; k++)
            VelocityField[k][ix][iy][iz] /= M;
      }
} //getVelocityField

/**
* @brief 
* 
* This computes the adjoint gradient on the particle positions, velocities
*
* @param AGVelocityField 
*/
void CICModel::computeAdjointModel(arrayVelocityField_view_t AGVelocityField) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  // declare arrays
  size_t Np = size_t(p_model->getNumberOfParticles());
  U_ParticleBasedArray xtilde_p(boost::extents[Np][3]);
  auto &xtilde = xtilde_p.get_array();
  U_ParticleBasedArray vtilde_p(boost::extents[Np][3]);
  auto &vtilde = vtilde_p.get_array();

  // get particles' positions and velocities from the forward model
  auto positions = p_model->getParticlePositions();
  auto velocities = p_model->getParticleVelocities();

  // get number of particles, box specifications, FFTW manager and MPI communicator from forward model
  BoxModel box = model->get_box_model();
  MPI_Communication *comm = model->communicator();
#ifdef ARES_MPI_FFTW
  CIC_Tools::Periodic_MPI periodic(box.N0, box.N1, box.N2, comm);
#else
  CIC_Tools::Periodic periodic(box.N0, box.N1, box.N2);
#endif

  // allocate array for mass field
  auto MassField_p = mgr.allocate_array(CIC::MPI_PLANE_LEAKAGE);
  auto &MassField = MassField_p.get_array();

  // initialize MassField to zero
  fwrap(MassField) = 0;

  ctx.print("project mass field");
  // compute the mass field
  CIC::projection(
      positions, MassField, box.L0, box.L1, box.L2, box.N0, box.N1, box.N2,
      periodic, CIC_Tools::DefaultWeight(), Np);

  // ------------------
  // First part: vtilde
  // ------------------

  // compute vtildeField = AGVelocityField / MassField
  U_VFieldType vtildeField_p(
      mgr.extents_real(boost::extents[3], CIC::MPI_PLANE_LEAKAGE));
  auto &vtildeField = vtildeField_p.get_array();
  size_t startN0 = mgr.startN0;
  size_t endN0 = startN0 + mgr.localN0;
  size_t N1 = mgr.N1;
  size_t N2 = mgr.N2;

  ctx.print("vtieldField");
#pragma omp parallel for collapse(3) schedule(static)
  for (long ix = startN0; ix < endN0; ix++)
    for (long iy = 0; iy < box.N1; iy++)
      for (long iz = 0; iz < box.N2; iz++) {
        double M = MassField[ix][iy][iz];
        if (M == 0) //FIXME this might be an issue
          for (unsigned int k = 0; k < 3; k++)
            vtildeField[k][ix][iy][iz] = 0;
        else
          for (unsigned int k = 0; k < 3; k++)
            vtildeField[k][ix][iy][iz] = AGVelocityField[k][ix][iy][iz] / M;
      }
  //  we are missing a replicate at ix==endN0 -> MPI_PLANE_LEAKAGE

  // interpolate vtildeField at the positions of the particles to get vtilde
  ctx.print("interpolate");
  CIC::interpolation(
      vtilde, positions, vtildeField, box.L0, box.L1, box.L2, box.N0, box.N1,
      box.N2, periodic, CIC_Tools::DefaultWeightDim2(), Np);

  // --------------------------------
  // Second part: xtilde - first term
  // --------------------------------

  // initialize xtilde to zero
  fwrap(xtilde) = 0;

  U_ParticleBasedScalar aux_p(boost::extents[Np]);
  boost::multi_array_ref<double, 1> &aux = aux_p.get_array();

  // compute xtilde1
  ctx.print("adjoint interpolation");
  for (unsigned int k = 0; k < 3; k++) {
    for (unsigned int a = 0; a < 3; a++) {
      typedef U_VFieldType::array_type::index_range range;
      //typename boost::remove_reference<VFieldType>::type::index_gen i_gen_v;

      CIC::adjoint_interpolation_scalar(
          k, aux, positions,
          vtildeField[boost::indices[a][range()][range()][range()]], box.L0,
          box.L1, box.L2, box.N0, box.N1, box.N2, periodic,
          CIC_Tools::DefaultWeight(), Np);

#pragma omp parallel for schedule(static)
      for (long i = 0; i < Np; i++)
        xtilde[i][k] += aux[i] * velocities[i][a];
    }
  }

  // --------------------------------
  // Third part: xtilde - second term
  // --------------------------------

  // compute momentum field
  U_VFieldType MomentumField_p(boost::extents[3][box.N0][box.N1][box.N2]);
  boost::multi_array_ref<double, 4> &MomentumField =
      MomentumField_p.get_array();
  fwrap(MomentumField) = 0;

  CIC::projection(
      positions, MomentumField, box.L0, box.L1, box.L2, box.N0, box.N1, box.N2,
      periodic, velocities, Np);

  // compute the field neeeded for xtilde2: v x vtilde
  U_VFieldType vtimesvtildeField_p(boost::extents[3][box.N0][box.N1][box.N2]);
  boost::multi_array_ref<double, 4> &vtimesvtildeField =
      vtimesvtildeField_p.get_array();

#pragma omp parallel for collapse(3) schedule(static)
  for (long ix = startN0; ix < endN0; ix++)
    for (long iy = 0; iy < box.N1; iy++)
      for (long iz = 0; iz < box.N2; iz++) {
        double M = MassField[ix][iy][iz];
        if (M == 0) //FIXME this might be an issue
          for (unsigned int k = 0; k < 3; k++)
            vtimesvtildeField[k][ix][iy][iz] = 0;
        else
          for (unsigned int k = 0; k < 3; k++)
            vtimesvtildeField[k][ix][iy][iz] = MomentumField[k][ix][iy][iz] *
                                               AGVelocityField[k][ix][iy][iz] /
                                               (M * M);
      }

  // compute xtilde2
  for (unsigned int k = 0; k < 3; k++) {
    for (unsigned int a = 0; a < 3; a++) {
      U_ParticleBasedScalar aux_p(boost::extents[Np]);
      boost::multi_array_ref<double, 1> &aux = aux_p.get_array();

      typedef U_VFieldType::array_type::index_range range;
      U_VFieldType::array_type::index_gen i_gen_v;

      CIC::adjoint_interpolation_scalar(
          k, aux, positions,
          vtimesvtildeField[i_gen_v[a][range()][range()][range()]], box.L0,
          box.L1, box.L2, box.N0, box.N1, box.N2, periodic,
          CIC_Tools::DefaultWeight(), Np);

#pragma omp parallel for schedule(static)
      for (long i = 0; i < Np; i++)
        xtilde[i][k] -= aux[i];
    }
  }

  p_model->adjointModelParticles(xtilde, vtilde);
} //computeAdjointModel

// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Florent Leclercq
// ARES TAG: year(0) = 2019-2020
// ARES TAG: email(0) = florent.leclercq@polytechnique.org
// ARES TAG: name(1) = Guilhem Lavaux
// ARES TAG: year(1) = 2019-2020
// ARES TAG: email(1) = guilhem.lavaux@iap.fr
