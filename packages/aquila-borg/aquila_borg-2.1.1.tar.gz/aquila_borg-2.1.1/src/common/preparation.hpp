/*+
    ARES/HADES/BORG Package -- ./src/common/preparation.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_ARES_PREPARATION_HPP
#define __LIBLSS_ARES_PREPARATION_HPP

#include <functional>
#include "libLSS/tools/console.hpp"
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>
#include "libLSS/tools/ptree_translators.hpp"
#include <boost/algorithm/string.hpp>
#include "libLSS/data/spectro_gals.hpp"
#include "libLSS/data/galaxies.hpp"
#include "libLSS/data/survey_load_txt.hpp"
#include "libLSS/data/survey_load_bin.hpp"
#include "libLSS/data/projection.hpp"
#include "libLSS/data/linear_selection.hpp"
#include "libLSS/data/window3d.hpp"
#include "libLSS/data/window3d_post.hpp"
#include "libLSS/data/schechter_completeness.hpp"
#include "survey_cutters.hpp"
#include "piecewise_selection.hpp"
#include "ketable.hpp"
#include <CosmoTool/interpolate.hpp>
#include "libLSS/tools/ptree_vectors.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_assign.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/physics/modified_ngp.hpp"
#include "libLSS/physics/classic_cic.hpp"

#include "preparation_types.hpp"
#include "preparation_tools.hpp"

namespace LibLSS_prepare {

  static void
  initSchechterVariables(MarkovState &state, ptree &params, int cat_idx) {
    state.newElement(
        format("galaxy_selection_info_%d") % cat_idx,
        new InfoSampleSelection());
    state.newElement(
        format("galaxy_schechter_%d") % cat_idx, new InfoSchechter());
  }

  static GalaxySurveyType &
  getGalaxyCatalog(MarkovState &state, size_t cat_idx) {
    return *state.get<GalaxyElement>(format("galaxy_catalog_%d") % cat_idx)
                ->obj;
  }

  template <typename Function>
  SurveyPreparer resolveGalaxySurvey(MarkovState &state, Function f) {
    return [f, &state](
               size_t cat_idx, ArrayType::ArrayType &grid, size_t *const &N,
               double *const &corner, double *const &L, double *const &delta) {
      return f(getGalaxyCatalog(state, cat_idx), grid, N, corner, L, delta);
    };
  }

  static void initializeGalaxySurveyCatalog(
      MarkovState &state, ptree &main_params, int cat_idx) {
    using PrepareDetail::ArrayDimension;
    std::array<size_t, 3> Ndata, N;
    std::array<size_t, 6> localNdata;
    size_t startN0, localN0;
    Console &cons = Console::instance();
    ptree &params = main_params.get_child(get_catalog_group_name(cat_idx));

    state.getScalarArray<long, 3>("Ndata", Ndata);
    state.getScalarArray<long, 6>("localNdata", localNdata);

    GalaxyElement *survey = new GalaxyElement();
    survey->obj = new GalaxySurveyType();
    // Add a catalog in the state structure
    state.newElement(format("galaxy_catalog_%d") % cat_idx, survey);
    // Add its linear bias in the MCMC structure
    ArrayType1d *bias = new ArrayType1d(boost::extents[0]);
    state.newElement(format("galaxy_bias_%d") % cat_idx, bias, true);
    double &nmean =
        state.newScalar<double>(format("galaxy_nmean_%d") % cat_idx, 1.0, true)
            ->value;
    bias->setAutoResize(true);

    auto data_ext = boost::extents[range(localNdata[0], localNdata[1])][range(
        localNdata[2], localNdata[3])][range(localNdata[4], localNdata[5])];
    auto data_dim = ArrayDimension(Ndata[0], Ndata[1], Ndata[2]);

    SelArrayType *sel_grid = new SelArrayType(data_ext);
    ArrayType *data_grid = new ArrayType(data_ext);

    cons.format<LOG_VERBOSE>(
        "Catalog %d: data grid is %dx%dx%d", cat_idx, Ndata[0], Ndata[1],
        Ndata[2]);
    data_grid->setRealDims(data_dim);
    sel_grid->setRealDims(data_dim);
    state.newScalar(format("galaxy_bias_ref_%d") % cat_idx, false);
    state.newElement(format("galaxy_sel_window_%d") % cat_idx, sel_grid);
    state.newElement(format("galaxy_data_%d") % cat_idx, data_grid);

    KECorrectionStateElement *ke_obj = new KECorrectionStateElement();
    KETableCorrection *ke;
    state.newElement(format("galaxy_kecorrection_%d") % cat_idx, ke_obj);
    if (boost::optional<string> ketable =
            params.get_optional<string>("ke_correction")) {
      cons.print<LOG_INFO_SINGLE>("Applying correction from file " + *ketable);
      ke = new KETableCorrection(*ketable);
    } else {
      ke = new KETableCorrection();
    }
    ke_obj->obj = ke;

    string radtype = to_lower_copy(params.get<string>("radial_selection"));
    if (radtype == "schechter") {
      cons.print<LOG_DEBUG>("initializing Schechter radial selection");
      initSchechterVariables(state, params, cat_idx);
    } else if (radtype == "piecewise") {
      cons.print<LOG_DEBUG>("initializing Piecewise selection");
      state.newElement(
          format("galaxy_selection_info_%d") % cat_idx,
          new InfoSampleSelection());
    } else if (radtype == "file") {
      state.newElement(
          format("galaxy_selection_info_%d") % cat_idx,
          new InfoSampleSelection());
    }
  }

  static void buildSchechterSelectionForSurvey(
      GalaxySurveyType &survey, MarkovState &state, ptree &params, int cat_idx,
      CosmologicalParameters &cosmo_params, SurveyPreparer &preparer,
      CorrectionFunction zcorr = LibLSS::details::nullCorrection) {
    ConsoleContext<LOG_INFO_SINGLE> ctx("schechter completeness for survey");
    Cosmology cosmo(cosmo_params);
    int Nsample = params.get<int>("schechter_sampling_rate");
    double Dmax = params.get<double>("schechter_dmax");
    boost::multi_array<double, 1> completeness(boost::extents[Nsample]);
    namespace ph = std::placeholders;

    GalaxySampleSelection &infosel =
        state
            .get<InfoSampleSelection>(
                format("galaxy_selection_info_%d") % cat_idx)
            ->value;
    SchechterParameters &infolum =
        state.get<InfoSchechter>(format("galaxy_schechter_%d") % cat_idx)
            ->value;
    KETableCorrection &ke = state
                                .get<KECorrectionStateElement>(
                                    format("galaxy_kecorrection_%d") % cat_idx)
                                ->get();

    infosel.bright_apparent_magnitude_cut =
        params.get<double>("galaxy_bright_apparent_magnitude_cut");
    infosel.faint_apparent_magnitude_cut =
        params.get<double>("galaxy_faint_apparent_magnitude_cut");
    infosel.bright_absolute_magnitude_cut =
        params.get<double>("galaxy_bright_absolute_magnitude_cut");
    infosel.faint_absolute_magnitude_cut =
        params.get<double>("galaxy_faint_absolute_magnitude_cut");
    infosel.zmin = params.get<double>("zmin", 0);
    infosel.zmax = params.get<double>("zmax", 100000);
    infosel.projection =
        state.getScalar<ProjectionDataModel>("projection_model");

    infolum.Mstar = params.get<double>("schechter_mstar");
    infolum.alpha = params.get<double>("schechter_alpha");

    buildCompletenessFromSchechterFunction(
        cosmo, infosel, infolum, completeness, Dmax,
        std::bind(
            &KETableCorrection::getZCorrection, &ke, std::placeholders::_1));

    survey.selection().setArray(completeness, Dmax);
    survey.selection().setMinMaxDistances(0, Dmax);

    switch (infosel.projection) {
    case NGP_PROJECTION:
      preparer = resolveGalaxySurvey(
          state,
          std::bind<size_t>(
              galaxySurveyToGridGeneric<
                  ModifiedNGP<double, NGPGrid::NGP, true>,
                  CIC_Tools::NonPeriodic, GalaxySurveyType,
                  ArrayType::ArrayType, double *, size_t *,
                  RedshiftMagnitudeCutter<GalaxySurveyType>>,
              ph::_1, ph::_2, ph::_3, ph::_4, ph::_5, ph::_6,
              RedshiftMagnitudeCutter<GalaxySurveyType>(infosel, &survey),
              std::function<void()>()));
      break;
    case LUMINOSITY_CIC_PROJECTION: {
      preparer = resolveGalaxySurvey(
          state,
          std::bind<size_t>(
              galaxySurveyToGridGeneric<
                  ClassicCloudInCell<double, true>, CIC_Tools::NonPeriodic,
                  GalaxySurveyType, ArrayType::ArrayType, double *, size_t *,
                  RedshiftMagnitudeCutter<GalaxySurveyType>>,
              ph::_1, ph::_2, ph::_3, ph::_4, ph::_5, ph::_6,
              RedshiftMagnitudeCutter<GalaxySurveyType>(infosel, &survey),
              std::function<void()>(std::bind(
                  &GalaxySurveyType::useLuminosityAsWeight, &survey))));
      break;
    }
    default:
      error_helper<ErrorParams>("Unsupported data projection");
      break;
    }
  }

  static void buildPiecewiseSelection(
      GalaxySurveyType &survey, MarkovState &state, ptree &params, int cat_idx,
      CosmologicalParameters &cosmo_params, SurveyPreparer &preparer) {
    namespace ph = std::placeholders;
    GalaxySampleSelection &infosel =
        state
            .get<InfoSampleSelection>(
                format("galaxy_selection_info_%d") % cat_idx)
            ->value;

    infosel.bright_apparent_magnitude_cut =
        params.get<double>("galaxy_bright_apparent_magnitude_cut");
    infosel.faint_apparent_magnitude_cut =
        params.get<double>("galaxy_faint_apparent_magnitude_cut");
    infosel.bright_absolute_magnitude_cut =
        params.get<double>("galaxy_bright_absolute_magnitude_cut");
    infosel.faint_absolute_magnitude_cut =
        params.get<double>("galaxy_faint_absolute_magnitude_cut");
    infosel.zmin = params.get<double>("zmin");
    infosel.zmax = params.get<double>("zmax");
    infosel.projection =
        state.getScalar<ProjectionDataModel>("projection_model");

    infosel.selector = makeSelector(cutterFunction(
        RedshiftMagnitudeCutter<GalaxySurveyType>(infosel, &survey)));

    switch (state.getScalar<ProjectionDataModel>("projection_model")) {
    case NGP_PROJECTION:
      preparer = resolveGalaxySurvey(
          state,
          std::bind<size_t>(
              galaxySurveyToGridGeneric<
                  ModifiedNGP<double, NGPGrid::NGP, true>,
                  CIC_Tools::NonPeriodic, GalaxySurveyType,
                  ArrayType::ArrayType, double *, size_t *,
                  RedshiftMagnitudeCutter<GalaxySurveyType>,
                  std::function<void()>>,
              ph::_1, ph::_2, ph::_3, ph::_4, ph::_5, ph::_6,
              RedshiftMagnitudeCutter<GalaxySurveyType>(infosel, &survey),
              std::function<void()>()));
      break;

    // If the projection is LUMINOSITY_CIC, then we have to use a CIC kernel
    case LUMINOSITY_CIC_PROJECTION:
      preparer = resolveGalaxySurvey(
          state,
          std::bind<size_t>(
              galaxySurveyToGridGeneric<
                  ClassicCloudInCell<double, true>, CIC_Tools::NonPeriodic,
                  GalaxySurveyType, ArrayType::ArrayType, double *, size_t *,
                  RedshiftMagnitudeCutter<GalaxySurveyType>>,
              ph::_1, ph::_2, ph::_3, ph::_4, ph::_5, ph::_6,
              RedshiftMagnitudeCutter<GalaxySurveyType>(infosel, &survey),
              std::function<void()>(std::bind(
                  &GalaxySurveyType::useLuminosityAsWeight, &survey))));
      break;
    }
  }

  static void buildFileSelectionForSurvey(
      GalaxySurveyType &survey, MarkovState &state, ptree &params, int cat_idx,
      CosmologicalParameters &cosmo_params, SurveyPreparer &preparer) {
    using LibLSS::details::safe_get;
    namespace ph = std::placeholders;
    ConsoleContext<LOG_INFO_SINGLE> ctx("file completeness for survey");
    string radial_map = params.get<string>("radial_file");

    ctx.print(format("Load radial selection function '%s'") % radial_map);
    survey.selection().loadRadial(radial_map);

    GalaxySampleSelection &selection =
        state
            .get<InfoSampleSelection>(
                format("galaxy_selection_info_%d") % cat_idx)
            ->value;

    selection.zmin = params.get<double>("zmin", 0);
    selection.zmax = params.get<double>("zmax", 100000);
    selection.projection =
        state.getScalar<ProjectionDataModel>("projection_model");

    if (!safe_get(
            params, "galaxy_bright_apparent_magnitude_cut",
            selection.bright_apparent_magnitude_cut) ||
        !safe_get(
            params, "galaxy_faint_apparent_magnitude_cut",
            selection.faint_apparent_magnitude_cut) ||
        !safe_get(
            params, "galaxy_bright_absolute_magnitude_cut",
            selection.bright_absolute_magnitude_cut) ||
        !safe_get(
            params, "galaxy_faint_absolute_magnitude_cut",
            selection.faint_absolute_magnitude_cut)) {
      ctx.print("No information on luminosity cuts. Taking all galaxies inside "
                "a d range");

      bool no_cut_catalog = true;
      if (!safe_get(params, "no_cut_catalog", no_cut_catalog) && no_cut_catalog)
        error_helper<ErrorParams>(
            boost::format(
                "You have to confirm not to cut properly your catalog %d") %
            cat_idx);

      try {
        selection.dmin = params.get<double>("file_dmin", 0);
        selection.dmax =
            params.get<double>("file_dmax", 1e6); // No cut effectively
        survey.selection().setMinMaxDistances(selection.dmin, selection.dmax);
      } catch (const std::runtime_error &) {
        error_helper<ErrorParams>(
            "Incorrect/Unknown file_dmin or file_dmax in configuration file");
      }
      preparer = resolveGalaxySurvey(
          state, std::bind<size_t>(
                     galaxySurveyToGridGeneric<
                         ModifiedNGP<double, NGPGrid::NGP, true>,
                         CIC_Tools::NonPeriodic, GalaxySurveyType,
                         ArrayType::ArrayType, double *, size_t *,
                         DistanceCutter<GalaxySurveyType>>,
                     ph::_1, ph::_2, ph::_3, ph::_4, ph::_5, ph::_6,
                     DistanceCutter<GalaxySurveyType>(selection, &survey),
                     std::function<void()>()));
    } else {
      Cosmology cosmo(cosmo_params);

      selection.dmin = cosmo.com2comph(cosmo.a2com(cosmo.z2a(selection.zmin)));
      selection.dmax = cosmo.com2comph(cosmo.a2com(cosmo.z2a(selection.zmax)));
      survey.selection().setMinMaxDistances(selection.dmin, selection.dmax);

      preparer = resolveGalaxySurvey(
          state,
          std::bind<size_t>(
              galaxySurveyToGridGeneric<
                  ModifiedNGP<double, NGPGrid::NGP, true>,
                  CIC_Tools::NonPeriodic, GalaxySurveyType,
                  ArrayType::ArrayType, double *, size_t *,
                  RedshiftMagnitudeCutter<GalaxySurveyType>>,
              ph::_1, ph::_2, ph::_3, ph::_4, ph::_5, ph::_6,
              RedshiftMagnitudeCutter<GalaxySurveyType>(selection, &survey),
              std::function<void()>()));
    }
  }

  static void loadGalaxySurveyCatalog(
      MarkovState &state, ptree &main_params, int cat_idx,
      CosmologicalParameters &cosmo) {
    ConsoleContext<LOG_INFO_SINGLE> ctx(
        str(format("loadGalaxySurveyCatalog(%d)") % cat_idx));
    GalaxyElement *survey =
        state.get<GalaxyElement>(format("galaxy_catalog_%d") % cat_idx);
    ptree &params = main_params.get_child(get_catalog_group_name(cat_idx));
    std::string data_format = params.get<std::string>("dataformat", "TXT");

    if (data_format == "TXT") {
      loadGalaxySurveyFromText(params.get<string>("datafile"), survey->get());
    } else if (data_format == "HDF5") {
      loadCatalogFromHDF5(
          params.get<string>("datafile"), params.get<string>("datakey"),
          survey->get());
    } else {
      error_helper<ErrorParams>(
          format("data_format has value %s, which is not recognized") %
          data_format);
    }

    state.getScalar<bool>(format("galaxy_bias_ref_%d") % cat_idx) =
        params.get<bool>("refbias");

    ArrayType1d::ArrayType &gbias =
        *(state.get<ArrayType1d>(format("galaxy_bias_%d") % cat_idx)->array);
    if (boost::optional<std::string> bvalue =
            params.get_optional<std::string>("bias")) {
      auto bias_double = string_as_vector<double>(*bvalue, ", ");
      gbias.resize(boost::extents[bias_double.size()]);
      std::copy(bias_double.begin(), bias_double.end(), gbias.begin());
      ctx.print("Set the bias to [" + to_string(gbias) + "]");
    } else {
      ctx.print("No initial bias value set, use bias=1");
      gbias.resize(boost::extents[1]);
      gbias[0] = 1;
    }

    double &nmean =
        state.get<SDouble>(format("galaxy_nmean_%d") % cat_idx)->value;
    if (boost::optional<double> nvalue = params.get_optional<double>("nmean")) {
      nmean = *nvalue;
    } else {
      ctx.print("No initial mean density value set, use nmean=1");
      nmean = 1;
    }

    string compl_map = params.get<string>("maskdata");
    ctx.print(format("Load sky completeness map '%s'") % compl_map);
    survey->get().selection().loadSky(
        compl_map, params.get<double>("sky_threshold", 0));
  }

  static void setupGalaxySurveyCatalog(
      MarkovState &state, ptree &main_params, int cat_idx,
      CosmologicalParameters &cosmo_params, SurveyPreparer &preparer) {
    ConsoleContext<LOG_INFO_SINGLE> ctx(
        str(format("loadGalaxySurveyCatalog(%d)") % cat_idx));
    auto &survey = getGalaxyCatalog(state, cat_idx);
    ptree &params = main_params.get_child(get_catalog_group_name(cat_idx));

    string radtype = to_lower_copy(params.get<string>("radial_selection"));

    GalaxySelectionType &gsel_type =
        state
            .newScalar<GalaxySelectionType>(
                format("galaxy_selection_type_%d") % cat_idx,
                GALAXY_SELECTION_FILE)
            ->value;

    if (radtype == "file") {
      buildFileSelectionForSurvey(
          survey, state, params, cat_idx, cosmo_params, preparer);
      gsel_type = GALAXY_SELECTION_FILE;
    } else if (radtype == "schechter") {
      buildSchechterSelectionForSurvey(
          survey, state, params, cat_idx, cosmo_params, preparer);
      gsel_type = GALAXY_SELECTION_SCHECHTER;
    } else if (radtype == "piecewise") {
      gsel_type = GALAXY_SELECTION_PIECEWISE;
      buildPiecewiseSelection(
          survey, state, params, cat_idx, cosmo_params, preparer);
    } else {
      error_helper<ErrorParams>(
          format("radtype has value %s, which is not recognized") % radtype);
    }
  }

  template <typename ptree>
  void prepareData(
      MPI_Communication *comm, MarkovState &state, int cat_idx,
      CosmologicalParameters &cosmo_params, const SurveyPreparer &preparer,
      ptree &main_params) {
    ConsoleContext<LOG_INFO_SINGLE> ctx("data preparation");
    using CosmoTool::InvalidRangeException;

    size_t Ndata[3], localNdata[6];
    double L[3], delta[3], corner[3];

    state.getScalarArray<long, 3>("Ndata", Ndata);
    state.getScalarArray<long, 6>("localNdata", localNdata);
    state.getScalarArray<double, 3>("L", L);
    state.getScalarArray<double, 3>("corner", corner);

    size_t N2_HC = static_cast<SLong &>(state["N2_HC"]),
           localN0 = static_cast<SLong &>(state["localN0"]),
           startN0 = static_cast<SLong &>(state["startN0"]);
    Cosmology cosmo(cosmo_params);
    ptree &sys_params = main_params.get_child("system");
    ptree &g_params = main_params.get_child(get_catalog_group_name(cat_idx));

    ctx.print(
        format("Project data to density field grid (catalog %d)") % cat_idx);

    GalaxySurveyType &survey =
        state.get<GalaxyElement>(str(format("galaxy_catalog_%d") % cat_idx))
            ->get();
    KECorrectionStateElement *ke = state.get<KECorrectionStateElement>(
        format("galaxy_kecorrection_%d") % cat_idx);
    try {
      survey.updateComovingDistance(
          cosmo, std::bind(
                     &KETableCorrection::getZCorrection, ke->obj,
                     std::placeholders::_1));
    } catch (const InvalidRangeException &e) {
      error_helper<ErrorBadState>(
          "Invalid range access in KE correction interpolation");
    }
    ArrayType *data_grid =
        state.get<ArrayType>(format("galaxy_data_%d") % cat_idx);

    delta[0] = L[0] / Ndata[0];
    delta[1] = L[1] / Ndata[1];
    delta[2] = L[2] / Ndata[2];

    size_t numGals =
        preparer(cat_idx, *(data_grid->array), Ndata, corner, L, delta);
    comm->all_reduce_t(MPI_IN_PLACE, &numGals, 1, MPI_SUM);
    if (numGals == 0) {
      error_helper<ErrorBadState>(
          format("No galaxy at all in catalog %d") % cat_idx);
    }

    GalaxySelectionType &gsel_type = state.getScalar<GalaxySelectionType>(
        format("galaxy_selection_type_%d") % cat_idx);
    GalaxySampleSelection &infosel =
        state
            .get<InfoSampleSelection>(
                format("galaxy_selection_info_%d") % cat_idx)
            ->value;
    if (gsel_type == GALAXY_SELECTION_PIECEWISE) {
      computeEmpiricalSelection(
          &survey, infosel, g_params.template get<double>("piecewise_dmin"),
          g_params.template get<double>("piecewise_dmax"),
          g_params.template get<int>("piecewise_Nbins"));
    }

    SelArrayType *sel_grid =
        state.get<SelArrayType>(format("galaxy_sel_window_%d") % cat_idx);

    PrepareDetail::compute_window(
        sys_params, comm, survey.selection(), state, *sel_grid->array, true);

    if (infosel.projection == LUMINOSITY_CIC_PROJECTION) {
      convolve_selection_cic(comm, *sel_grid->array, Ndata);
    }

    auto fsel = fwrap(*sel_grid->array);
    fsel = mask(fsel > 0.05, fsel, fwrap(fsel.fautowrap(0)));

    PrepareDetail::cleanup_data(*data_grid->array, *sel_grid->array);

    // Free memory at the expense of information in logs
    survey.selection().clearSky();
  }

} // namespace LibLSS_prepare

#endif
