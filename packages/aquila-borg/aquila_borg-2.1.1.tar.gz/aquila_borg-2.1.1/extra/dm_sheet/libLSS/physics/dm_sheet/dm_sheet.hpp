/*+
    ARES/HADES/BORG Package -- ./extra/dm_sheet/libLSS/physics/dm_sheet/dm_sheet.hpp
    Copyright (C) 2016-2018 Florent Leclercq <florent.leclercq@polytechnique.org>
    Copyright (C) 2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2019-2020 James Prideaux-Ghee <j.prideaux-ghee19@imperial.ac.uk>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_DMSHEET_HPP
#  define __LIBLSS_DMSHEET_HPP

#  include <boost/multi_array.hpp>
#  include "libLSS/physics/dm_sheet/tetrahedron_tools.hpp"

namespace LibLSS {

  namespace DM_Sheet {
    typedef boost::multi_array_ref<particleID_t, 1> arrayID_t;
    typedef boost::multi_array_ref<double, 2> arrayPosition_t;
    typedef boost::multi_array_ref<double, 2> arrayVelocity_t;
    typedef arrayID_t::const_array_view<1>::type arrayID_view_t;
    typedef arrayPosition_t::const_array_view<2>::type arrayPosition_view_t;
    typedef arrayVelocity_t::const_array_view<2>::type arrayVelocity_view_t;

    /**
     * This function computes projects tetrahedra on the provided density grid
     * with the indicated flow tracers.
     *
     * @param flowtracers_Ids lagrangian ids of the flowtracers
     * @param flowtracers_positions Eulerian position of the flowtracers
     * @param L0 first dimension of the box
     * @param L1 second dimension of the box
     * @param L2 third dimension of hte box
     * @param Np0 first dimension of the Lagrangian grid
     * @param Np1 second dimension of the Lagrangian grid
     * @param Np2 third dimension of the Lagrangian grid
     * @param N0 first dimension of the expected Eulerian grid
     * @param N1 second dimension of the expected Eulerian grid
     * @param N2 third dimension of the expected Eulerian grid
     * @param density_grid unnormalized mass density
     */
    void get_nbstreams_tetrahedra(
        arrayID_view_t flowtracers_Ids,
        arrayPosition_view_t flowtracers_positions, const double L0,
        const double L1, const double L2, const int Np0, const int Np1,
        const int Np2, const int N0, const int N1, const int N2,
        boost::multi_array_ref<double, 3> &nbstreams_grid);

    /**
     * This function computes the density field from tetrahedra on the provided density grid
     * with the indicated flow tracers.
     *
     * @param flowtracers_Ids lagrangian ids of the flowtracers
     * @param flowtracers_positions Eulerian position of the flowtracers
     * @param L0 first dimension of the box
     * @param L1 second dimension of the box
     * @param L2 third dimension of hte box
     * @param Np0 first dimension of the Lagrangian grid
     * @param Np1 second dimension of the Lagrangian grid
     * @param Np2 third dimension of the Lagrangian grid
     * @param N0 first dimension of the expected Eulerian grid
     * @param N1 second dimension of the expected Eulerian grid
     * @param N2 third dimension of the expected Eulerian grid
     * @param density_grid unnormalized mass density
     */
    void get_density_tetrahedra(
        arrayID_view_t flowtracers_Ids,
        arrayPosition_view_t flowtracers_positions, const double L0,
        const double L1, const double L2, const int Np0, const int Np1,
        const int Np2, const int N0, const int N1, const int N2,
        boost::multi_array_ref<double, 3> &density_grid);

    /**
     * This function computes the \emph{momenta} from tetrahedra
     * on the provided momenta grid with the indicated flow tracers.
     *
     * @param flowtracers_Ids lagrangian ids of the flowtracers
     * @param flowtracers_positions Eulerian position of the flowtracers
     * @param L0 first dimension of the box
     * @param L1 second dimension of the box
     * @param L2 third dimension of hte box
     * @param Np0 first dimension of the Lagrangian grid
     * @param Np1 second dimension of the Lagrangian grid
     * @param Np2 third dimension of the Lagrangian grid
     * @param N0 first dimension of the expected Eulerian grid
     * @param N1 second dimension of the expected Eulerian grid
     * @param N2 third dimension of the expected Eulerian grid
     * @param momenta_grid output momenta grid
     */
    void get_momenta_tetrahedra(
        arrayID_view_t flowtracers_Ids,
        arrayPosition_view_t flowtracers_positions,
        arrayVelocity_view_t flowtracers_velocities, const double L0,
        const double L1, const double L2, const int Np0, const int Np1,
        const int Np2, const int N0, const int N1, const int N2,
        boost::multi_array_ref<double, 4> &momenta_grid);

    /**
     * This function computes density and \emph{momenta} fields from tetrahedra
     * on the provided grids with the indicated flow tracers.
     *
     * @param flowtracers_Ids lagrangian ids of the flowtracers
     * @param flowtracers_positions Eulerian position of the flowtracers
     * @param L0 first dimension of the box
     * @param L1 second dimension of the box
     * @param L2 third dimension of hte box
     * @param Np0 first dimension of the Lagrangian grid
     * @param Np1 second dimension of the Lagrangian grid
     * @param Np2 third dimension of the Lagrangian grid
     * @param N0 first dimension of the expected Eulerian grid
     * @param N1 second dimension of the expected Eulerian grid
     * @param N2 third dimension of the expected Eulerian grid
     * @param density_grid output mass density
     * @param momenta_grid output momenta grid
     */
    void get_mass_and_momenta_tetrahedra(
        arrayID_view_t flowtracers_Ids,
        arrayPosition_view_t flowtracers_positions,
        arrayVelocity_view_t flowtracers_velocities, const double L0,
        const double L1, const double L2, const int Np0, const int Np1,
        const int Np2, const int N0, const int N1, const int N2,
        boost::multi_array_ref<double, 3> &density_grid,
        boost::multi_array_ref<double, 4> &momenta_grid);

    void get_nbstreams_mass_and_momenta_tetrahedra(
        arrayID_view_t flowtracers_Ids,
        arrayPosition_view_t flowtracers_positions,
        arrayVelocity_view_t flowtracers_velocities, const double L0,
        const double L1, const double L2, const int Np0, const int Np1,
        const int Np2, const int N0, const int N1, const int N2,
        boost::multi_array_ref<double, 3> &nbstreams_grid,
        boost::multi_array_ref<double, 3> &density_grid,
        boost::multi_array_ref<double, 4> &momenta_grid);

    void get_velocity_dispersion_tetrahedra(
        arrayID_view_t flowtracers_Ids,
        arrayPosition_view_t flowtracers_positions,
        arrayVelocity_view_t flowtracers_velocities, const double L0,
        const double L1, const double L2, const int Np0, const int Np1,
        const int Np2, const int N0, const int N1, const int N2,
        boost::multi_array_ref<double, 3> &
            nbstreams_grid, // Introduce a 3d array with the no. dm streams per point.
        boost::multi_array_ref<double, 3> &
            density_grid, // Introduce a 3d array with the density at each point
        boost::multi_array_ref<double, 4> &
            momenta_grid, // Introduce a 4d array, with the velocity components at each point
        boost::multi_array_ref<double, 4> &
            dispersion_grid); // Introduce a 5d array with the velocity dispersion tensor

    void get_nbstreams_mass_momenta_and_velocity_dispersion_tetrahedra(
        arrayID_view_t flowtracers_Ids,
        arrayPosition_view_t flowtracers_positions,
        arrayVelocity_view_t flowtracers_velocities, const double L0,
        const double L1, const double L2, const int Np0, const int Np1,
        const int Np2, const int N0, const int N1, const int N2,
        boost::multi_array_ref<double, 3> &nbstreams_grid,
        boost::multi_array_ref<double, 3> &density_grid,
        boost::multi_array_ref<double, 4> &momenta_grid,
        boost::multi_array_ref<double, 4> &dispersion_grid);

  } // namespace DM_Sheet

} // namespace LibLSS

#endif
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
#pragma once
