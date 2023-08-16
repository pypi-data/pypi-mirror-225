/*+
    ARES/HADES/BORG Package -- ./extra/dm_sheet/libLSS/physics/dm_sheet/dm_sheet.cpp
    Copyright (C) 2016-2018 Florent Leclercq <florent.leclercq@polytechnique.org>
    Copyright (C) 2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2019-2020 James Prideaux-Ghee <j.prideaux-ghee19@imperial.ac.uk>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <cmath>
#include <algorithm>
#include <boost/multi_array.hpp>
#include <Eigen/Dense>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/log_traits.hpp"
#include "libLSS/tools/string_tools.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/physics/dm_sheet/dm_sheet.hpp"
#include "libLSS/physics/dm_sheet/tools.hpp"
#include "libLSS/physics/dm_sheet/tetrahedron_tools.hpp"

using namespace LibLSS;
using namespace LibLSS::DM_Sheet;

///-------------------------------------------------------------------------------------
/** @fn project_tetrahedron
 * Project a tetrahedron to the Eulerian grid
 * @param TetrahedronCoords input tetrahedron vertices coordinates
 * @param N0 mesh size x
 * @param N1 mesh size y
 * @param N2 mesh size z
 * @param L0 box size x
 * @param L1 box size y
 * @param L2 box size z
 * @param f functor to use for projection
 */
template <typename Functor>
void project_tetrahedron(
    const double *TetrahedronCoords, const size_t N0, const size_t N1,
    const size_t N2, const double L0, const double L1, const double L2,
    Functor f) {
  const double d0 = L0 / N0;
  const double d1 = L1 / N1;
  const double d2 = L2 / N2;

  double xA, yA, zA, xB, yB, zB, xC, yC, zC, xD, yD, zD;
  xA = TetrahedronCoords[0];
  yA = TetrahedronCoords[1];
  zA = TetrahedronCoords[2];
  xB = TetrahedronCoords[3];
  yB = TetrahedronCoords[4];
  zB = TetrahedronCoords[5];
  xC = TetrahedronCoords[6];
  yC = TetrahedronCoords[7];
  zC = TetrahedronCoords[8];
  xD = TetrahedronCoords[9];
  yD = TetrahedronCoords[10];
  zD = TetrahedronCoords[11];

  double xmin = std::min({xA, xB, xC, xD}), xmax = std::max({xA, xB, xC, xD});
  double ymin = std::min({yA, yB, yC, yD}), ymax = std::max({yA, yB, yC, yD});
  double zmin = std::min({zA, zB, zC, zD}), zmax = std::max({zA, zB, zC, zD});

  ssize_t imin = ssize_t(floor(xmin / d0)), imax = ssize_t(floor(xmax / d0));
  ssize_t jmin = ssize_t(floor(ymin / d1)), jmax = ssize_t(floor(ymax / d1));
  ssize_t kmin = ssize_t(floor(zmin / d2)), kmax = ssize_t(floor(zmax / d2));

  Eigen::Matrix4d M;
  M << xA, yA, zA, 1., xB, yB, zB, 1., xC, yC, zC, 1., xD, yD, zD, 1.;
  double D0 = M.determinant();

  // Check if this grid point is in the tetrahedron and project
  /// \note in this loop it is possible to have i>N0, j>N1, k>N2 !!
  for (ssize_t i = imin; i <= imax; i++)
    for (ssize_t j = jmin; j <= jmax; j++)
      for (ssize_t k = kmin; k <= kmax; k++) {
        // check the current grid point
        double x = i * d0;
        double y = j * d1;
        double z = k * d2;
        if (isInTetrahedron(TetrahedronCoords, D0, x, y, z)) {
          // important: check periodic boundary conditions here
          size_t igrid = p_mod(i, ssize_t(N0));
          size_t jgrid = p_mod(j, ssize_t(N1));
          size_t kgrid = p_mod(k, ssize_t(N2));

          // interpolate with Shepard's method (1/distance^2 weights)
          double wA = 1 / ((x - xA) * (x - xA) + (y - yA) * (y - yA) +
                           (z - zA) * (z - zA));
          double wB = 1 / ((x - xB) * (x - xB) + (y - yB) * (y - yB) +
                           (z - zB) * (z - zB));
          double wC = 1 / ((x - xC) * (x - xC) + (y - yC) * (y - yC) +
                           (z - zC) * (z - zC));
          double wD = 1 / ((x - xD) * (x - xD) + (y - yD) * (y - yD) +
                           (z - zD) * (z - zD));
          double w = wA + wB + wC + wD;

          f(igrid, jgrid, kgrid, wA, wB, wC, wD, w);
        }
      }
} //project_tetrahedron
///-------------------------------------------------------------------------------------
static massparticleID_t get_NpM(const particleID_t NpF) {
  // There is exactly 24 times more mass tracers than flow tracers
  return massparticleID_t(24) * NpF;
} //get_NpM
///-------------------------------------------------------------------------------------
/** @fn get_masstracers
 * Return a Snapshot *containing the mass tracers
 * @warning Take care to use the same type for flow tracers and mass tracers IDs in this function!
 */
void get_masstracers(
    const arrayID_view_t &flowtracers_Ids,
    const arrayPosition_view_t &flowtracers_positions, const double L0,
    const double L1, const double L2, const size_t Np0, const size_t Np1,
    const size_t Np2, arrayPosition_t &masstracers_positions) {
  const particleID_t NpF = flowtracers_positions.shape()[0];
  const massparticleID_t NpM = get_NpM(NpF);
  // Types should match here!

  // Loop on flow tracers
#pragma omp parallel for schedule(static)
  for (particleID_t mpF = 0; mpF < NpF; mpF++) {
    particleID_t Id = flowtracers_Ids[mpF];
    // Loop on the 6 tetrahedra for this particle
    for (int itet = 0; itet < 6; itet++) {
      particleID_t mpM, mpA, mpB, mpC, mpD;

      // Get the indices of the 4 vertices
      particleID_t TetrahedronIndices[4];
      get_tetrahedron_indices(Id, itet, Np0, Np1, Np2, TetrahedronIndices);
      mpA = TetrahedronIndices[0];
      mpB = TetrahedronIndices[1];
      mpC = TetrahedronIndices[2];
      mpD = TetrahedronIndices[3];

      // Get the coordinates
      double TetrahedronCoords[12];
      get_tetrahedron_coords(
          flowtracers_positions, mpA, mpB, mpC, mpD, L0, L1, L2,
          TetrahedronCoords);

      // Loop on the 4 sides for this tetrahedron
      for (unsigned int iside = 0; iside < 4; iside++) {
        // Get the positions of the mass tracers
        mpM = 24 * mpF + 4 * itet + iside;
        double MassTracerCoords[3];
        get_masstracer_coords(TetrahedronCoords, iside, MassTracerCoords);

        // check periodic boundary conditions here
        masstracers_positions[mpM][0] = p_mod(MassTracerCoords[0], L0);
        masstracers_positions[mpM][1] = p_mod(MassTracerCoords[1], L1);
        masstracers_positions[mpM][2] = p_mod(MassTracerCoords[2], L2);
      } //end loop on sides
    }   //end loop on tetrahedra
  }     //end loop on flow tracers
} //get_masstracers
///-------------------------------------------------------------------------------------
/** @fn lagrangian_transport
 * Do the Lagrangian transport of various quantities
 */
template <
    typename ParticlePropertyArray, typename ApplyPropertyFunctor,
    typename WeightFunctor>
void lagrangian_transport(
    const arrayID_view_t &flowtracers_Ids,
    const arrayPosition_view_t &flowtracers_positions,
    const ParticlePropertyArray &properties, WeightFunctor weighter,
    const double L0, const double L1, const double L2, const size_t Np0,
    const size_t Np1, const size_t Np2, const size_t N0, const size_t N1,
    const size_t N2, ApplyPropertyFunctor applier) {
  const double m = 1.0;
  const double d = L0 / Np0;
  const size_t N = N0 * N1 * N2;
  const particleID_t NpF = flowtracers_Ids.shape()[0];

  Console::instance().print<LOG_VERBOSE>("Npf = " + to_string(NpF));

  // loop on particles
  for (particleID_t mpF = 0; mpF < NpF; mpF++) {
    particleID_t Id = flowtracers_Ids[mpF];

    // loop on the 6 tetrahedra for this particle
    for (unsigned int itet = 0; itet < 6; itet++) {
      particleID_t mpA, mpB, mpC, mpD;

      // get the indices of the 4 vertices
      particleID_t TetrahedronIndices[4];
      get_tetrahedron_indices(Id, itet, Np0, Np1, Np2, TetrahedronIndices);
      mpA = TetrahedronIndices[0];
      mpB = TetrahedronIndices[1];
      mpC = TetrahedronIndices[2];
      mpD = TetrahedronIndices[3];

      // get the coordinates
      double TetrahedronCoords[12];
      get_tetrahedron_coords(
          flowtracers_positions, mpA, mpB, mpC, mpD, L0, L1, L2,
          TetrahedronCoords);

      // get the volume and mass
      double Vtet = get_tetrahedron_volume(TetrahedronCoords);
      double rhotet =
          m / (6 * std::abs(Vtet)); //equation (6) in Abel, Hahn & Kaehler 2012

      // get weights for each vertex
      auto pA = weighter(properties[mpA], rhotet),
           pB = weighter(properties[mpB], rhotet),
           pC = weighter(properties[mpC], rhotet),
           pD = weighter(properties[mpD], rhotet);

      // project tetrahedron
      project_tetrahedron(
          TetrahedronCoords, N0, N1, N2, L0, L1, L2,
          [&pA, &pB, &pC, &pD, &applier](
              size_t i, size_t j, size_t k, double wA, double wB, double wC,
              double wD, double w) {
            applier(i, j, k, pA, wA, pB, wB, pC, wC, pD, wD, w);
          });

    } //end loop on tetrahedra
  }   //end loop on particles
} //lagrangian_transport

namespace LibLSS {
  namespace DM_Sheet {

    void get_nbstreams_tetrahedra(
        arrayID_view_t flowtracers_Ids,
        arrayPosition_view_t flowtracers_positions, const double L0,
        const double L1, const double L2, const int Np0, const int Np1,
        const int Np2, const int N0, const int N1, const int N2,
        boost::multi_array_ref<double, 3> &nbstreams_grid) {
      auto mass_array =
          b_fused_idx<double, 2>([](int, int) -> double { return 1; });
      typedef decltype(mass_array[0]) Mass_t;

      auto weighter = [](const Mass_t &, double rhotet) -> double {
        return 1.;
      };
      auto applier = [&nbstreams_grid](
                         size_t i, size_t j, size_t k, double, double wA,
                         double, double wB, double, double wC, double,
                         double wD,
                         double w) { nbstreams_grid[i][j][k] += 1.; };

      lagrangian_transport(
          flowtracers_Ids, flowtracers_positions, mass_array, weighter, L0, L1,
          L2, Np0, Np1, Np2, N0, N1, N2, applier);
    } //get_nbstreams_tetrahedra

    void get_density_tetrahedra(
        arrayID_view_t flowtracers_Ids,
        arrayPosition_view_t flowtracers_positions, const double L0,
        const double L1, const double L2, const int Np0, const int Np1,
        const int Np2, const int N0, const int N1, const int N2,
        boost::multi_array_ref<double, 3> &density_grid) {
      auto mass_array =
          b_fused_idx<double, 2>([](int, int) -> double { return 1; });
      typedef decltype(mass_array[0]) Mass_t;

      auto weighter = [](const Mass_t &, double rhotet) -> double {
        return rhotet;
      };
      auto applier = [&density_grid](
                         size_t i, size_t j, size_t k, double rho, double wA,
                         double, double wB, double, double wC, double,
                         double wD, double w) { density_grid[i][j][k] += rho; };

      lagrangian_transport(
          flowtracers_Ids, flowtracers_positions, mass_array, weighter, L0, L1,
          L2, Np0, Np1, Np2, N0, N1, N2, applier);
    } //get_density_tetrahedra

    void get_momenta_tetrahedra(
        arrayID_view_t flowtracers_Ids,
        arrayPosition_view_t flowtracers_positions,
        arrayVelocity_view_t flowtracers_velocities, const double L0,
        const double L1, const double L2, const int Np0, const int Np1,
        const int Np2, const int N0, const int N1, const int N2,
        boost::multi_array_ref<double, 4> &momenta_grid) {
      typedef decltype(flowtracers_velocities[0]) Flow_t;
      typedef std::tuple<Flow_t, double> TupleV;
      typedef TupleV const &TupleV_c;

      auto weighter = [](Flow_t v, double rhotet) -> TupleV {
        return TupleV(v, rhotet);
      };
      auto applier = [&momenta_grid](
                         size_t i, size_t j, size_t k, TupleV_c tA, double wA,
                         TupleV_c tB, double wB, TupleV_c tC, double wC,
                         TupleV_c tD, double wD, double w) {
        auto vg = momenta_grid[i][j][k];
        auto const &vA = std::get<0>(tA);
        auto const &vB = std::get<0>(tB);
        auto const &vC = std::get<0>(tC);
        auto const &vD = std::get<0>(tD);
        double rhotet_w = std::get<1>(tA) / w;

        for (unsigned int l = 0; l < 3; l++)
          vg[l] +=
              rhotet_w * (vA[l] * wA + vB[l] * wB + vC[l] * wC + vD[l] * wD);
      };

      lagrangian_transport(
          flowtracers_Ids, flowtracers_positions, flowtracers_velocities,
          weighter, L0, L1, L2, Np0, Np1, Np2, N0, N1, N2, applier);
    } //get_momenta_tetrahedra

    void get_mass_and_momenta_tetrahedra(
        arrayID_view_t flowtracers_Ids,
        arrayPosition_view_t flowtracers_positions,
        arrayVelocity_view_t flowtracers_velocities, const double L0,
        const double L1, const double L2, const int Np0, const int Np1,
        const int Np2, const int N0, const int N1, const int N2,
        boost::multi_array_ref<double, 3> &density_grid,
        boost::multi_array_ref<double, 4> &momenta_grid) {
      typedef decltype(flowtracers_velocities[0]) Flow_t;
      typedef std::tuple<Flow_t, double> TupleV;
      typedef TupleV const &TupleV_c;

      auto weighter = [](Flow_t v, double rhotet) -> TupleV {
        return TupleV(v, rhotet);
      };
      auto applier = [&density_grid, &momenta_grid](
                         size_t i, size_t j, size_t k, TupleV_c tA, double wA,
                         TupleV_c tB, double wB, TupleV_c tC, double wC,
                         TupleV_c tD, double wD, double w) {
        auto vg = momenta_grid[i][j][k];
        auto const &vA = std::get<0>(tA);
        auto const &vB = std::get<0>(tB);
        auto const &vC = std::get<0>(tC);
        auto const &vD = std::get<0>(tD);
        double rhotet = std::get<1>(tA);
        double rhotet_w = rhotet / w;

        for (unsigned int l = 0; l < 3; l++)
          vg[l] +=
              rhotet_w * (vA[l] * wA + vB[l] * wB + vC[l] * wC + vD[l] * wD);

        density_grid[i][j][k] += rhotet;
      };

      lagrangian_transport(
          flowtracers_Ids, flowtracers_positions, flowtracers_velocities,
          weighter, L0, L1, L2, Np0, Np1, Np2, N0, N1, N2, applier);
    } //get_mass_and_momenta_tetrahedra

    void get_velocity_dispersion_tetrahedra(
        arrayID_view_t flowtracers_Ids,
        arrayPosition_view_t flowtracers_positions,
        arrayVelocity_view_t flowtracers_velocities, const double L0,
        const double L1, const double L2, const int Np0, const int Np1,
        const int Np2, const int N0, const int N1, const int N2,
        boost::multi_array_ref<double, 3> &nbstreams_grid,
        boost::multi_array_ref<double, 3> &density_grid,
        boost::multi_array_ref<double, 4> &momenta_grid,
        boost::multi_array_ref<double, 4> &dispersion_grid) {
      typedef decltype(flowtracers_velocities[0]) Flow_t;
      typedef std::tuple<Flow_t, double> TupleV;
      typedef TupleV const &TupleV_c;

      auto weighter = [](Flow_t v, double rhotet) -> TupleV {
        return TupleV(v, rhotet);
      };
      auto applier = [&momenta_grid, &dispersion_grid](
                         size_t i, size_t j, size_t k, TupleV_c tA, double wA,
                         TupleV_c tB, double wB, TupleV_c tC, double wC,
                         TupleV_c tD, double wD, double w) {
        auto vg = momenta_grid[i][j][k];
        auto vp = dispersion_grid[i][j][k];
        auto const &vA = std::get<0>(tA);
        auto const &vB = std::get<0>(tB);
        auto const &vC = std::get<0>(tC);
        auto const &vD = std::get<0>(tD);
        double rhotet = std::get<1>(tA);
        double rhotet_w = rhotet / w;

        for (unsigned int l = 0; l < 3; l++) {
          vg[l] +=
              rhotet_w * (vA[l] * wA + vB[l] * wB + vC[l] * wC + vD[l] * wD);
        }

        vp[0] += rhotet_w * (vA[0] * vA[0] * wA + vB[0] * vB[0] * wB +
                             vC[0] * vC[0] * wC + vD[0] * vD[0] * wD);
        vp[1] += rhotet_w * (vA[1] * vA[1] * wA + vB[1] * vB[1] * wB +
                             vC[1] * vC[1] * wC + vD[1] * vD[1] * wD);
        vp[2] += rhotet_w * (vA[2] * vA[2] * wA + vB[2] * vB[2] * wB +
                             vC[2] * vC[2] * wC + vD[2] * vD[2] * wD);
        vp[3] += rhotet_w * (vA[0] * vA[1] * wA + vB[0] * vB[1] * wB +
                             vC[0] * vC[1] * wC + vD[0] * vD[1] * wD);
        vp[4] += rhotet_w * (vA[0] * vA[2] * wA + vB[0] * vB[2] * wB +
                             vC[0] * vC[2] * wC + vD[0] * vD[2] * wD);
        vp[5] += rhotet_w * (vA[1] * vA[2] * wA + vB[1] * vB[2] * wB +
                             vC[1] * vC[2] * wC + vD[1] * vD[2] * wD);
      };

      lagrangian_transport(
          flowtracers_Ids, flowtracers_positions, flowtracers_velocities,
          weighter, L0, L1, L2, Np0, Np1, Np2, N0, N1, N2, applier);

    } // get_velocity_dispersion_tetrahedra

    void get_nbstreams_mass_and_momenta_tetrahedra(
        arrayID_view_t flowtracers_Ids,
        arrayPosition_view_t flowtracers_positions,
        arrayVelocity_view_t flowtracers_velocities, const double L0,
        const double L1, const double L2, const int Np0, const int Np1,
        const int Np2, const int N0, const int N1, const int N2,
        boost::multi_array_ref<double, 3> &nbstreams_grid,
        boost::multi_array_ref<double, 3> &density_grid,
        boost::multi_array_ref<double, 4> &momenta_grid) {
      typedef decltype(flowtracers_velocities[0]) Flow_t;
      typedef std::tuple<Flow_t, double> TupleV;
      typedef TupleV const &TupleV_c;

      auto weighter = [](Flow_t v, double rhotet) -> TupleV {
        return TupleV(v, rhotet);
      };
      auto applier = [&nbstreams_grid, &density_grid, &momenta_grid](
                         size_t i, size_t j, size_t k, TupleV_c tA, double wA,
                         TupleV_c tB, double wB, TupleV_c tC, double wC,
                         TupleV_c tD, double wD, double w) {
        auto vg = momenta_grid[i][j][k];
        auto const &vA = std::get<0>(tA);
        auto const &vB = std::get<0>(tB);
        auto const &vC = std::get<0>(tC);
        auto const &vD = std::get<0>(tD);
        double rhotet = std::get<1>(tA);
        double rhotet_w = rhotet / w;

        for (unsigned int l = 0; l < 3; l++)
          vg[l] +=
              rhotet_w * (vA[l] * wA + vB[l] * wB + vC[l] * wC + vD[l] * wD);

        density_grid[i][j][k] += rhotet;
        nbstreams_grid[i][j][k] += 1.;
      };

      lagrangian_transport(
          flowtracers_Ids, flowtracers_positions, flowtracers_velocities,
          weighter, L0, L1, L2, Np0, Np1, Np2, N0, N1, N2, applier);
    } //get_nbstreams_mass_and_momenta_tetrahedra

    //get_nbstreams_mass_momenta_and_velocity_dispersion_tetrahedra

    void get_nbstreams_mass_momenta_and_velocity_dispersion_tetrahedra(
        arrayID_view_t flowtracers_Ids,
        arrayPosition_view_t flowtracers_positions,
        arrayVelocity_view_t flowtracers_velocities, const double L0,
        const double L1, const double L2, const int Np0, const int Np1,
        const int Np2, const int N0, const int N1, const int N2,
        boost::multi_array_ref<double, 3> &nbstreams_grid,
        boost::multi_array_ref<double, 3> &density_grid,
        boost::multi_array_ref<double, 4> &momenta_grid,
        boost::multi_array_ref<double, 4> &dispersion_grid) {
      typedef decltype(flowtracers_velocities[0]) Flow_t;
      typedef std::tuple<Flow_t, double> TupleV;
      typedef TupleV const &TupleV_c;

      auto weighter = [](Flow_t v, double rhotet) -> TupleV {
        return TupleV(v, rhotet);
      };
      auto applier = [&nbstreams_grid, &density_grid, &momenta_grid,
                      &dispersion_grid](
                         size_t i, size_t j, size_t k, TupleV_c tA, double wA,
                         TupleV_c tB, double wB, TupleV_c tC, double wC,
                         TupleV_c tD, double wD, double w) {
        auto vg = momenta_grid[i][j][k];
        auto vp = dispersion_grid[i][j][k];
        auto const &vA = std::get<0>(tA);
        auto const &vB = std::get<0>(tB);
        auto const &vC = std::get<0>(tC);
        auto const &vD = std::get<0>(tD);
        double rhotet = std::get<1>(tA);
        double rhotet_w = rhotet / w;

        for (unsigned int l = 0; l < 3; l++) {
          vg[l] +=
              rhotet_w * (vA[l] * wA + vB[l] * wB + vC[l] * wC + vD[l] * wD);
        }

        vp[0] += rhotet_w * (vA[0] * vA[0] * wA + vB[0] * vB[0] * wB +
                             vC[0] * vC[0] * wC + vD[0] * vD[0] * wD);
        vp[1] += rhotet_w * (vA[1] * vA[1] * wA + vB[1] * vB[1] * wB +
                             vC[1] * vC[1] * wC + vD[1] * vD[1] * wD);
        vp[2] += rhotet_w * (vA[2] * vA[2] * wA + vB[2] * vB[2] * wB +
                             vC[2] * vC[2] * wC + vD[2] * vD[2] * wD);
        vp[3] += rhotet_w * (vA[0] * vA[1] * wA + vB[0] * vB[1] * wB +
                             vC[0] * vC[1] * wC + vD[0] * vD[1] * wD);
        vp[4] += rhotet_w * (vA[0] * vA[2] * wA + vB[0] * vB[2] * wB +
                             vC[0] * vC[2] * wC + vD[0] * vD[2] * wD);
        vp[5] += rhotet_w * (vA[1] * vA[2] * wA + vB[1] * vB[2] * wB +
                             vC[1] * vC[2] * wC + vD[1] * vD[2] * wD);

        density_grid[i][j][k] += rhotet;
        nbstreams_grid[i][j][k] += 1.;
      };

      lagrangian_transport(
          flowtracers_Ids, flowtracers_positions, flowtracers_velocities,
          weighter, L0, L1, L2, Np0, Np1, Np2, N0, N1, N2, applier);
    } //get_nbstreams_mass_momenta_and_velocity_dispersion_tetrahedra

  } // namespace DM_Sheet
} // namespace LibLSS

// ARES TAG: authors_num = 3
// ARES TAG: name(0) = Florent Leclercq
// ARES TAG: year(0) = 2016-2018
// ARES TAG: email(0) = florent.leclercq@polytechnique.org
// ARES TAG: name(1) = Guilhem Lavaux
// ARES TAG: year(1) = 2018
// ARES TAG: email(1) = guilhem.lavaux@iap.fr
// ARES TAG: name(2) = James Prideaux-Ghee
// ARES TAG: year(2) = 2019-2020
// ARES TAG: email(2) = j.prideaux-ghee19@imperial.ac.uk

