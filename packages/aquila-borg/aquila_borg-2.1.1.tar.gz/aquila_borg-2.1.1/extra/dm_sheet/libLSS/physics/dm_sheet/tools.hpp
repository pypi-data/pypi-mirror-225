/*+
    ARES/HADES/BORG Package -- ./extra/dm_sheet/libLSS/physics/dm_sheet/tools.hpp
    Copyright (C) 2016-2018 Florent Leclercq <florent.leclercq@polytechnique.org>
    Copyright (C) 2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_DMSHEET_TOOLS_HPP
#  define __LIBLSS_DMSHEET_TOOLS_HPP

#  include <cmath>

namespace LibLSS {

  namespace DM_Sheet {

    ///-------------------------------------------------------------------------------------
    /** @fn p_mod
 * Replaces function modulo, treats differently negative values
 * @param x
 * @param y should be positive, else replaced by -y
 * @return value between 0 and y
 */
    template <typename T>
    inline T p_mod(const T x, const T y) {
      if (y == 0)
        return 0;
      T yy = std::abs(y);

      return std::fmod(x + yy, yy);
    } //p_mod

    static bool sameSign(double x, double y) {
        double xy = x*y;
        return xy >= 0.;
    } //sameSign

    static void
    periodic_boundary_correct(const double xmax, double &xA, const double L0) {
      if ((xmax - xA) > (L0 - xmax) + xA)
        xA += L0;
    } //periodic_boundary_correct

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
