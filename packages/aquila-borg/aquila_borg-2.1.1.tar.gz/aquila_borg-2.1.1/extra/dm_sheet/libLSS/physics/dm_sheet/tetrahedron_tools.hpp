/*+
    ARES/HADES/BORG Package -- ./extra/dm_sheet/libLSS/physics/dm_sheet/tetrahedron_tools.hpp
    Copyright (C) 2016-2018 Florent Leclercq <florent.leclercq@polytechnique.org>
    Copyright (C) 2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_DMSHEET_TETRAHEDRON_TOOLS_HPP
#  define __LIBLSS_DMSHEET_TETRAHEDRON_TOOLS_HPP

#  include <array>
#  include <Eigen/Dense>
#  include "libLSS/physics/dm_sheet/tools.hpp"

namespace LibLSS {
  namespace DM_Sheet {
    typedef size_t particleID_t;
    typedef size_t massparticleID_t;
#if defined(__GNUC__) && !(defined(__clang__) || defined(__INTEL_COMPILER))
    static constexpr double INV_SQRT_5 = 1.0 / std::sqrt(5.0);
    static constexpr double ONE_MINUS_INV_SQRT_5 = 1 - 1.0 / std::sqrt(5.0);
#else
    static const double INV_SQRT_5 = 1.0 / std::sqrt(5.0);
    static const double ONE_MINUS_INV_SQRT_5 = 1 - 1.0 / std::sqrt(5.0);
#endif

    ///-------------------------------------------------------------------------
    /** @fn get_Lagrangian_indices
      * Get indices on the Lagrangian grid from particle Id
      * @param Id particle id
      * @param Np0 particle mesh size x
      * @param Np1 particle mesh size y
      * @param Np2 particle mesh size z
      * @param indices output indices
      * \warning Assumes row major!
      */
    static inline void get_Lagrangian_indices(
        const particleID_t Id, const size_t Np0, const size_t Np1,
        const size_t Np2, std::array<size_t, 3> &indices) {
      // assumes Id = k+Np2*(j+Np1*i)
      size_t i = (Id / (Np1 * Np2)) % Np0;
      size_t j = ((Id - Np1 * Np2 * i) / Np2) % Np1;
      size_t k = ((Id - Np2 * j - Np2 * Np1 * i)) % Np2;

      indices[0] = i;
      indices[1] = j;
      indices[2] = k;
    } //get_Lagrangian_indices

    ///-------------------------------------------------------------------------
    /** @fn get_index
    * Get mapping from 3D to 1D array
    * @param i index x
    * @param j index y
    * @param k index z
    * @param N0 array size x
    * @param N1 array size y
    * @param N2 array size z
    * @return index
    * \warning Assumes row major!
    */
    static inline size_t get_index(
        const int i, const int j, const int k, const int, const int N1,
        const int N2) {
      return size_t(k + N2 * (j + N1 * i));
    } //get_index

    ///-------------------------------------------------------------------------
    /** @fn get_Lagrangian_Id
   * Get particle Id from indices on the Lagrangian grid
   * @param mp0 index x
   * @param mp1 index y
   * @param mp2 index z
   * @param Np0 particle mesh size x
   * @param Np1 particle mesh size y
   * @param Np2 particle mesh size z
   * @return particle id
   * \warning Assumes row major!
   */
    static inline particleID_t get_Lagrangian_Id(
        const size_t mp0, const size_t mp1, const size_t mp2, const size_t Np0,
        const size_t Np1, const size_t Np2) {
      return particleID_t(get_index(mp0, mp1, mp2, Np0, Np1, Np2));
    } //get_Lagrangian_Id

    ///-------------------------------------------------------------------------
    /** @fn get_tetrahedron_indices
    * Get the particle indices of a tetrahedron
    * @param Id particle id
    * @param itet the id of the tetrahedron (0 to 5)
    * @param Np0 particle mesh size x
    * @param Np1 particle mesh size y
    * @param Np2 particle mesh size z
    * @param TetrahedronIndices output tetrahedron particle indices
    */
    static inline void get_tetrahedron_indices(
        const particleID_t Id, const size_t itet, const size_t Np0,
        const size_t Np1, const size_t Np2, particleID_t *TetrahedronIndices) {
      std::array<size_t, 3> indices;
      get_Lagrangian_indices(Id, Np0, Np1, Np2, indices);
      size_t i = indices[0];
      size_t j = indices[1];
      size_t k = indices[2];
      size_t ii = (i + 1) % Np0;
      size_t jj = (j + 1) % Np1;
      size_t kk = (k + 1) % Np2;

      particleID_t mpA, mpB, mpC, mpD;

      switch (itet) {
      case 0:
        // Tetrahedron 1: (0,1,3,4)
        mpA = get_Lagrangian_Id(i, j, k, Np0, Np1, Np2);  //0
        mpB = get_Lagrangian_Id(ii, j, k, Np0, Np1, Np2); //1
        mpC = get_Lagrangian_Id(i, jj, k, Np0, Np1, Np2); //3
        mpD = get_Lagrangian_Id(i, j, kk, Np0, Np1, Np2); //4
        break;

      case 1:
        // Tetrahedron 2: (1,3,4,7)
        mpA = get_Lagrangian_Id(ii, j, k, Np0, Np1, Np2);  //1
        mpB = get_Lagrangian_Id(i, jj, k, Np0, Np1, Np2);  //3
        mpC = get_Lagrangian_Id(i, j, kk, Np0, Np1, Np2);  //4
        mpD = get_Lagrangian_Id(i, jj, kk, Np0, Np1, Np2); //7
        break;

      case 2:
        // Tetrahedron 3: (1,4,5,7)
        mpA = get_Lagrangian_Id(ii, j, k, Np0, Np1, Np2);  //1
        mpB = get_Lagrangian_Id(i, j, kk, Np0, Np1, Np2);  //4
        mpC = get_Lagrangian_Id(ii, j, kk, Np0, Np1, Np2); //5
        mpD = get_Lagrangian_Id(i, jj, kk, Np0, Np1, Np2); //7
        break;

      case 3:
        // Tetrahedron 4: (1,2,5,7)
        mpA = get_Lagrangian_Id(ii, j, k, Np0, Np1, Np2);  //1
        mpB = get_Lagrangian_Id(ii, jj, k, Np0, Np1, Np2); //2
        mpC = get_Lagrangian_Id(ii, j, kk, Np0, Np1, Np2); //5
        mpD = get_Lagrangian_Id(i, jj, kk, Np0, Np1, Np2); //7
        break;

      case 4:
        // Tetrahedron 5: (1,2,3,7)
        mpA = get_Lagrangian_Id(ii, j, k, Np0, Np1, Np2);  //1
        mpB = get_Lagrangian_Id(ii, jj, k, Np0, Np1, Np2); //2
        mpC = get_Lagrangian_Id(i, jj, k, Np0, Np1, Np2);  //3
        mpD = get_Lagrangian_Id(i, jj, kk, Np0, Np1, Np2); //7
        break;

      case 5:
        // Tetrahedron 6: (2,5,6,7)
        mpA = get_Lagrangian_Id(ii, jj, k, Np0, Np1, Np2);  //2
        mpB = get_Lagrangian_Id(ii, j, kk, Np0, Np1, Np2);  //5
        mpC = get_Lagrangian_Id(ii, jj, kk, Np0, Np1, Np2); //6
        mpD = get_Lagrangian_Id(i, jj, kk, Np0, Np1, Np2);  //7
        break;
      }

      TetrahedronIndices[0] = mpA;
      TetrahedronIndices[1] = mpB;
      TetrahedronIndices[2] = mpC;
      TetrahedronIndices[3] = mpD;
    } //get_tetrahedron_indices

    ///-------------------------------------------------------------------------
    /** @fn get_tetrahedron_coords
     * Get physical coordinates of the tetrahedron vertices
     * @param positions particles' positions
     * @param mpA particle Id first vertex
     * @param mpB particle Id second vertex
     * @param mpC particle Id third vertex
     * @param mpD particle Id fourth vertex
     * @param TetrahedronCoords output tetrahedron vertices coordinates
     */
    template <typename ArrayPosition>
    static inline void get_tetrahedron_coords(
        const ArrayPosition &positions, const size_t mpA, const size_t mpB,
        const size_t mpC, const size_t mpD, const double L0, const double L1,
        const double L2, double *TetrahedronCoords) {
      double xA = positions[mpA][0], yA = positions[mpA][1],
             zA = positions[mpA][2];
      double xB = positions[mpB][0], yB = positions[mpB][1],
             zB = positions[mpB][2];
      double xC = positions[mpC][0], yC = positions[mpC][1],
             zC = positions[mpC][2];
      double xD = positions[mpD][0], yD = positions[mpD][1],
             zD = positions[mpD][2];

      // Correction for periodic boundary conditions
      double xmax = std::max({xA, xB, xC, xD});
      periodic_boundary_correct(xmax, xA, L0);
      periodic_boundary_correct(xmax, xB, L0);
      periodic_boundary_correct(xmax, xC, L0);
      periodic_boundary_correct(xmax, xD, L0);

      double ymax = std::max({yA, yB, yC, yD});
      periodic_boundary_correct(ymax, yA, L1);
      periodic_boundary_correct(ymax, yB, L1);
      periodic_boundary_correct(ymax, yC, L1);
      periodic_boundary_correct(ymax, yD, L1);

      double zmax = std::max({zA, zB, zC, zD});
      periodic_boundary_correct(zmax, zA, L2);
      periodic_boundary_correct(zmax, zB, L2);
      periodic_boundary_correct(zmax, zC, L2);
      periodic_boundary_correct(zmax, zD, L2);

      TetrahedronCoords[0] = xA;
      TetrahedronCoords[1] = yA;
      TetrahedronCoords[2] = zA;
      TetrahedronCoords[3] = xB;
      TetrahedronCoords[4] = yB;
      TetrahedronCoords[5] = zB;
      TetrahedronCoords[6] = xC;
      TetrahedronCoords[7] = yC;
      TetrahedronCoords[8] = zC;
      TetrahedronCoords[9] = xD;
      TetrahedronCoords[10] = yD;
      TetrahedronCoords[11] = zD;
    } //get_tetrahedron_coords

    ///-------------------------------------------------------------------------
    /** @fn get_tetrahedron_volume
     * Get volume of a tetrahedron
     * @param TetrahedronCoords input tetrahedron vertices positions
     * @return volume in UnitLength**3 (typically (Mpc/h)**3)
     */
    static inline double
    get_tetrahedron_volume(const double *TetrahedronCoords) {
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
      
      // triple scalar product of the vectors
      // a factor of 6 because the cube is tessellated into 6 tetrahedra
      // (section 2.2 in Abel, Hahn & Kaehler 2012)
      Eigen::Matrix3d M;
      M << xB - xA, xC - xA, xD - xA,
           yB - yA, yC - yA, yD - yA,
           zB - zA, zC - zA, zD - zA;
      return (double)M.determinant() / 6.;

    } //get_tetrahedron_volume

    ///-------------------------------------------------------------------------------------
    /** @fn isInTetrahedron
 * Check if a spatial position is inside a tetrahedron
 * @param TetrahedronCoords input tetrahedron vertices coordinates
 * @param xP position x
 * @param yP position y
 * @param zP position z
 */
    static bool isInTetrahedron(
        const double *TetrahedronCoords, const double D0, const double xP,
        const double yP, const double zP) {
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
      
      Eigen::Matrix4d M1, M2, M3, M4;
      
      // As a consistency check, D0 should be D1+D2+D3+D4
      M1 << xP, yP, zP, 1., xB, yB, zB, 1., xC, yC, zC, 1., xD, yD, zD, 1.;
      double D1 = M1.determinant();
      if (!sameSign(D1, D0))
        return false;
      
      M2 << xA, yA, zA, 1., xP, yP, zP, 1., xC, yC, zC, 1., xD, yD, zD, 1.;
      double D2 = M2.determinant();
      if (!sameSign(D2, D0))
        return false;

      M3 << xA, yA, zA, 1., xB, yB, zB, 1., xP, yP, zP, 1., xD, yD, zD, 1.;
      double D3 = M3.determinant();
      if (!sameSign(D3, D0))
        return false;

      M4 << xA, yA, zA, 1., xB, yB, zB, 1., xC, yC, zC, 1., xP, yP, zP, 1.;
      double D4 = M4.determinant();
      if (!sameSign(D4, D0))
        return false;

      return true;
    } //isInTetrahedron

    ///-------------------------------------------------------------------------
    /** @fn aux_get_masstracer_coords
     * Subroutine of get_masstracer_coords
     */
    static void aux_get_masstracer_coords(
        const double xS, const double yS, const double zS, const double xM,
        const double yM, const double zM, double *MassTracerCoords) {
      // Matches the monopole and quadrupole moments
      // of the mass distribution of the homogeneous tetrahedron
      // (section 2.2 in Hahn, Abel & Kaehler 2013)
      MassTracerCoords[0] = INV_SQRT_5 * xS + ONE_MINUS_INV_SQRT_5 * xM;
      MassTracerCoords[1] = INV_SQRT_5 * yS + ONE_MINUS_INV_SQRT_5 * yM;
      MassTracerCoords[2] = INV_SQRT_5 * zS + ONE_MINUS_INV_SQRT_5 * zM;
    } //aux_get_masstracer_coords

    ///-------------------------------------------------------------------------
    /** @fn get_masstracer_coords
     * Get coordinates of the mass tracer for one side of a tetrahedron
     * @param TetrahedronCoords input tetrahedron vertices coordinates
     * @param iside the id of the tetrahedron side (0 to 4)
     * @param MassTracerCoords output coordinates of the mass tracer
     */
    static void get_masstracer_coords(
        const double *TetrahedronCoords, const int iside,
        double *MassTracerCoords) {
      double xA, yA, zA, xB, yB, zB, xC, yC, zC, xD, yD, zD, xM, yM, zM;
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
      xM = (xA + xB + xC + xD) / 4;
      yM = (yA + yB + yC + yD) / 4;
      zM = (zA + zB + zC + zD) / 4;

      switch (iside) {
      case 0:
        aux_get_masstracer_coords(xA, yA, zA, xM, yM, zM, MassTracerCoords);
        break;

      case 1:
        aux_get_masstracer_coords(xB, yB, zB, xM, yM, zM, MassTracerCoords);
        break;

      case 2:
        aux_get_masstracer_coords(xC, yC, zC, xM, yM, zM, MassTracerCoords);
        break;

      case 3:
        aux_get_masstracer_coords(xD, yD, zD, xM, yM, zM, MassTracerCoords);
        break;
      }
    } //get_masstracer_coords

  } // namespace DM_Sheet
} // namespace LibLSS

#endif
// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Florent Leclercq
// ARES TAG: year(0) = 2016-2018
// ARES TAG: email(0) = florent.leclercq@polytechnique.org
// ARES TAG: name(1) = Guilhem Lavaux
// ARES TAG: year(1) = 2018
// ARES TAG: email(1) = guilhem.lavaux@iap.fr
