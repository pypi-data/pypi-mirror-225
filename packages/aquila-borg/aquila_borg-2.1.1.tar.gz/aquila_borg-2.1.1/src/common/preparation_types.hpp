/*+
    ARES/HADES/BORG Package -- ./src/common/preparation_types.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef _LIBLSS_PREPARATION_TYPES_HPP
#define _LIBLSS_PREPARATION_TYPES_HPP

#include <functional>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>
#include <boost/algorithm/string.hpp>
#include "libLSS/data/spectro_gals.hpp"
#include "libLSS/data/galaxies.hpp"
#include "libLSS/data/projection.hpp"
#include "libLSS/data/linear_selection.hpp"
#include "libLSS/data/schechter_completeness.hpp"
#include "piecewise_selection.hpp"
#include "ketable.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"

namespace LibLSS_prepare {
  using namespace LibLSS;

  typedef boost::multi_array_types::extent_range range;

#ifndef SAMPLER_GALAXY_TYPE
#  define SAMPLER_GALAXY_TYPE BaseGalaxyDescriptor
#endif

  typedef GalaxySurvey<LinearInterpolatedSelection, SAMPLER_GALAXY_TYPE>
      GalaxySurveyType;
  typedef ObjectStateElement<GalaxySurveyType, true> GalaxyElement;
  typedef RandomNumberMPI<GSL_RandomNumber> RGenType;
  typedef ScalarStateElement<GalaxySampleSelection> InfoSampleSelection;
  typedef ScalarStateElement<SchechterParameters> InfoSchechter;
  typedef std::function<size_t(
      size_t, ArrayType::ArrayType &, size_t *const &, double *const &,
      double *const &, double *const &)>
      SurveyPreparer;
  typedef ObjectStateElement<KETableCorrection, true> KECorrectionStateElement;

  using boost::format;
  using boost::to_lower_copy;
  using std::string;

  typedef boost::property_tree::iptree ptree;

} // namespace LibLSS_prepare

#endif
