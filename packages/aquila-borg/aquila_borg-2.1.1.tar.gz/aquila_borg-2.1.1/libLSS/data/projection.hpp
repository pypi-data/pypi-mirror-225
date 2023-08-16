/*+
    ARES/HADES/BORG Package -- ./libLSS/data/projection.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PROJECTION_HPP
#define __LIBLSS_PROJECTION_HPP

#include <algorithm>
#include <array>
#include <boost/array.hpp>
#include <boost/multi_array.hpp>
#include <boost/lambda/lambda.hpp>
#include "angtools.hpp"
#include "postools.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/physics/generic_cic.hpp"

namespace LibLSS {

  enum ProjectionDataModel { NGP_PROJECTION, LUMINOSITY_CIC_PROJECTION };

  static const int LSS_DIMENSIONS = 3;
  static const int NR_CELLS_DIM = 2;
  static const int NR_CELLS_SLICE = 4;
  static const int NR_CELLS_TOTAL = 8;
  static const double TOTAL_WEIGHT = 1.;

  struct Dimension {
    union {
      double length[LSS_DIMENSIONS];
      double position[LSS_DIMENSIONS];
    };
  };

  struct Grid {
    size_t resolution[LSS_DIMENSIONS];
  };

  namespace details {
    template <typename GSurvey>
    struct ProjectionAcceptAll {
      bool operator()(const typename GSurvey::GalaxyType &g) { return true; }
    };
  }; // namespace details

  template <
      typename Kernel, typename Periodic, class GSurvey, typename DensityField,
      typename Dimension, typename IDimension, typename Condition,
      typename PreRun = std::function<void()>>
  size_t galaxySurveyToGridGeneric(
      const GSurvey &survey, DensityField &field, const IDimension &N,
      const Dimension &corner, const Dimension &L, const Dimension &d,
      Condition condition, PreRun prerun = PreRun()) {
    const typename DensityField::size_type *localN = field.shape();
    const typename DensityField::index *base = field.index_bases();
    using boost::format;
    using boost::lambda::_1;
    size_t accepted = 0;
    double found_corners[LSS_DIMENSIONS][2];
    boost::multi_array<double, 2> xyz(boost::extents[survey.surveySize()][3]);
    boost::multi_array<double, 1> weights(boost::extents[survey.surveySize()]);

    // prerun must not be empty
    if (prerun)
      prerun();

    for (int i = 0; i < LSS_DIMENSIONS; i++) {
      found_corners[i][0] = std::numeric_limits<double>::infinity();
      found_corners[i][1] = -std::numeric_limits<double>::infinity();
    }

    array::fill(field, 0);

    for (long i = 0; i < survey.surveySize(); i++) {
      typename GSurvey::ConstRefGalaxyType g = survey[i];
      boost::array<typename DensityField::index, LSS_DIMENSIONS> ii;
      boost::array<double, LSS_DIMENSIONS> loc_xyz;

      if (!condition(g))
        continue;

      ang2vec(g.phi, g.theta, loc_xyz);

      for (int j = 0; j < LSS_DIMENSIONS; j++) {
        loc_xyz[j] = loc_xyz[j] * g.r - corner[j];
        found_corners[j][0] = std::min(loc_xyz[j], found_corners[j][0]);
        found_corners[j][1] = std::max(loc_xyz[j], found_corners[j][1]);
      }

      std::copy(loc_xyz.begin(), loc_xyz.end(), xyz[accepted].begin());
      weights[accepted] = g.final_w;
      accepted++;
    }
    Console::instance().format<LOG_VERBOSE>(
        "Using type %s for projection", typeid(Periodic).name());
    Kernel::projection(
        xyz, field, L[0], L[1], L[2], N[0], N[1], N[2],
        Periodic(N[0], N[1], N[2]), weights, accepted);

    Console::instance().print<LOG_VERBOSE>(
        format("Project to grid: accepted %d galaxies") % accepted);
    {
      std::string cstr;

      for (int j = 0; j < LSS_DIMENSIONS; j++)
        cstr += str(
            format("(%lg - %lg) ") % found_corners[j][0] % found_corners[j][1]);
      Console::instance().print<LOG_VERBOSE>(
          "Project to grid: found corners " + cstr);
    }

    return accepted;
  }

  template <
      typename Kernel, typename Periodic, class GSurvey, typename DensityField,
      typename Dimension, typename IDimension>
  size_t galaxySurveyToGrid_all(
      const GSurvey &survey, DensityField &field, const IDimension &N,
      const Dimension &corner, const Dimension &L, const Dimension &d) {
    details::ProjectionAcceptAll<GSurvey> condition;

    return galaxySurveyToGridGeneric<Kernel, Periodic>(
        survey, field, N, corner, L, d, condition);
  }

  /* This function create a mock survey based on the selection function hold in survey_in and the full density field in field.
     */
  template <class GSurvey, typename DensityField, typename Dimension>
  void createMockSurvey(
      const GSurvey &survey_in, GSurvey &survey_out, DensityField &field,
      const Dimension &corner, const Dimension &L) {}

  template <
      class GSurvey, typename DensityField, typename Grid, typename Dimension,
      typename Condition>
  size_t haloSimToGridGeneric(
      const GSurvey &sim, DensityField &field, const Grid &M,
      const Dimension &corner, const Dimension &L, const Dimension &d,
      Condition condition) {
    const typename DensityField::size_type *N = field.shape();
    const typename DensityField::index *base = field.index_bases();
    using boost::format;
    using boost::lambda::_1;

    size_t accepted = 0;
    double found_corners[LSS_DIMENSIONS][2];
    for (auto i = 0; i < LSS_DIMENSIONS; i++) {
      found_corners[i][0] = std::numeric_limits<double>::infinity();
      found_corners[i][1] = -std::numeric_limits<double>::infinity();
    }

    for (auto i = 0; i < sim.surveySize(); i++) {
      typename GSurvey::ConstRefGalaxyType h = sim[i];
      std::array<
          std::array<typename DensityField::index, LSS_DIMENSIONS>,
          NR_CELLS_TOTAL>
          ii;
      std::array<double, LSS_DIMENSIONS> xyz;
      bool validLowerSlice = true;
      bool validUpperSlice = true;

      if (!condition(h))
        continue;

      loadPosition(h.posx, h.posy, h.posz, xyz);

      for (int j = 0; j < LSS_DIMENSIONS; j++) {
        ii[0][j] = (int)std::floor((xyz[j] - corner[j]) / d[j]);
        found_corners[j][0] = std::min(xyz[j], found_corners[j][0]);
        found_corners[j][1] = std::max(xyz[j], found_corners[j][1]);
      }

      std::array<double, NR_CELLS_TOTAL> weight;
      std::array<std::array<double, LSS_DIMENSIONS>, NR_CELLS_DIM> wxyz;
      for (auto j = 0; j < LSS_DIMENSIONS; j++) {
        wxyz[1][j] = ((xyz[j] - corner[j]) / d[j]) - ii[0][j];
        wxyz[0][j] = TOTAL_WEIGHT - wxyz[1][j];
      }
      weight[0] = wxyz[0][0] * wxyz[0][1] * wxyz[0][2];
      weight[1] = wxyz[0][0] * wxyz[1][1] * wxyz[0][2];
      weight[2] = wxyz[0][0] * wxyz[0][1] * wxyz[1][2];
      weight[3] = wxyz[0][0] * wxyz[1][1] * wxyz[1][2];
      weight[4] = wxyz[1][0] * wxyz[0][1] * wxyz[0][2];
      weight[5] = wxyz[1][0] * wxyz[1][1] * wxyz[0][2];
      weight[6] = wxyz[1][0] * wxyz[0][1] * wxyz[1][2];
      weight[7] = wxyz[1][0] * wxyz[1][1] * wxyz[1][2];

      for (auto j = 0; j < LSS_DIMENSIONS; j++) {
        if ((ii[0][j] == -1) || (ii[0][j] == M[j]))
          ii[0][j] = M[j] - 1;
      }

      for (auto cell = 1; cell < NR_CELLS_TOTAL; cell++) {
        std::copy(std::begin(ii[0]), std::end(ii[0]), std::begin(ii[cell]));
      }

      ii[1][1]++;
      ii[1][1] = (size_t)std::fmod(ii[1][1], M[1]);

      ii[2][2]++;
      ii[2][2] = (size_t)std::fmod(ii[2][2], M[2]);

      ii[3][1]++;
      ii[3][1] = (size_t)std::fmod(ii[3][1], M[1]);
      ii[3][2]++;
      ii[3][2] = (size_t)std::fmod(ii[3][2], M[2]);

      ii[4][0]++;
      ii[4][0] = (size_t)std::fmod(ii[4][0], M[0]);

      ii[5][0]++;
      ii[5][0] = (size_t)std::fmod(ii[5][0], M[0]);
      ii[5][1]++;
      ii[5][1] = (size_t)std::fmod(ii[5][1], M[1]);

      ii[6][0]++;
      ii[6][0] = (size_t)std::fmod(ii[6][0], M[0]);
      ii[6][2]++;
      ii[6][2] = (size_t)std::fmod(ii[6][2], M[2]);

      for (auto j = 0; j < LSS_DIMENSIONS; j++) {
        ii[7][j]++;
        ii[7][j] = (size_t)std::fmod(ii[7][j], M[j]);
      }

      for (auto j = 0; j < LSS_DIMENSIONS; j++) {
        validLowerSlice = validLowerSlice &&
                          (ii[0][j] >= base[j] && ii[0][j] < (base[j] + N[j]));
        validUpperSlice = validUpperSlice &&
                          (ii[4][j] >= base[j] && ii[4][j] < (base[j] + N[j]));
      }
      if (validLowerSlice) {
        for (auto cell = 0; cell < NR_CELLS_SLICE; cell++) {
          field(ii[cell]) += weight[cell] * h.w;
          accepted++;
        }
      }
      if (validUpperSlice) {
        for (auto cell = NR_CELLS_SLICE; cell < NR_CELLS_TOTAL; cell++) {
          field(ii[cell]) += weight[cell] * h.w;
          accepted++;
        }
      }
    }
    Console::instance().print<LOG_VERBOSE>(
        format("Project to grid: accept and assign halos to %d cells") %
        accepted);
    {
      std::string cstr;
      for (auto j = 0; j < LSS_DIMENSIONS; j++)
        cstr += str(
            format("(%lg - %lg) ") % found_corners[j][0] % found_corners[j][1]);
      Console::instance().print<LOG_VERBOSE>(
          "Project to grid: found corners " + cstr);
    }
    return accepted;
  }

  template <
      class GSurvey, typename DensityField, typename Grid, typename Dimension>
  size_t haloSimToGrid_all(
      const GSurvey &sim, DensityField &field, const Grid &M,
      const Dimension &corner, const Dimension &L, const Dimension &d) {
    details::ProjectionAcceptAll<GSurvey> condition;
    return haloSimToGridGeneric<
        GSurvey, DensityField, Grid, Dimension,
        details::ProjectionAcceptAll<GSurvey>>(
        sim, field, M, corner, L, d, condition);
  }

}; // namespace LibLSS

CTOOL_ENUM_TYPE(
    LibLSS::ProjectionDataModel, HDF5T_ProjectionDataModel,
    (LibLSS::NGP_PROJECTION)(LibLSS::LUMINOSITY_CIC_PROJECTION))

#endif
