/*+
    ARES/HADES/BORG Package -- ./src/common/piecewise_selection.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PIECEWISE_SELECTION_HPP
#define __LIBLSS_PIECEWISE_SELECTION_HPP
/*
#include <boost/accumulators/accumulators.hpp>
#include <boost/accumulators/statistics/density.hpp>
*/
#include <CosmoTool/algo.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/data/spectro_gals.hpp"
#include "libLSS/data/spectro_gals.hpp"
#include "libLSS/data/galaxies.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"

namespace LibLSS {

  template <typename GalaxySurvey>
  void computeEmpiricalSelection(
      GalaxySurvey *survey, GalaxySampleSelection &infosel, double dMin,
      double dMax, int Nbins) {
    using CosmoTool::cube;
    boost::multi_array<double, 1> completeness(boost::extents[Nbins]);

    std::fill(
        completeness.data(), completeness.data() + completeness.num_elements(),
        0);

    for (int i = 0; i < survey->surveySize(); i++) {
      if (!(*infosel.selector)((*survey)[i]))
        continue;

      double d = (*survey)[i].r;
      int iD = (int)floor((d - dMin) * (Nbins) / (dMax - dMin));

      if (iD < Nbins && iD >= 0)
        completeness[iD]++;
    }

    double c_max = 0;
    for (int i = 0; i < Nbins; i++) {
      double r0 = dMin + i * (dMax - dMin) / (Nbins);
      double r1 = dMin + (i + 1) * (dMax - dMin) / (Nbins);

      completeness[i] /= cube(r1) - cube(r0);
      c_max = std::max(completeness[i], c_max);
    }

    for (int i = 0; i < Nbins; i++) {
      completeness[i] /= c_max;
    }

    survey->selection().setArray(completeness, dMax);
    survey->selection().setMinMaxDistances(0, dMax);
  }
}; // namespace LibLSS

#endif
