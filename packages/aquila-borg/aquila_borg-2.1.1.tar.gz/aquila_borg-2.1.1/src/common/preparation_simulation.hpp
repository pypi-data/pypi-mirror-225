/*+
    ARES/HADES/BORG Package -- ./src/common/preparation_simulation.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_ARES_PREPARATION_SIMULATION_HPP
#define __LIBLSS_ARES_PREPARATION_SIMULATION_HPP

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
#include "libLSS/data/schechter_completeness.hpp"
#include "survey_cutters.hpp"
#include <CosmoTool/interpolate.hpp>
#include "libLSS/tools/ptree_vectors.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_assign.hpp"
#include "preparation.hpp"
#include <boost/tokenizer.hpp>
#include <string>

namespace LibLSS_prepare {

  using namespace LibLSS;

  typedef boost::multi_array_types::extent_range range;

  typedef RandomNumberMPI<GSL_RandomNumber> RGenType;
  typedef ScalarStateElement<GalaxySampleSelection> InfoSampleSelection;

  static GalaxySurveyType &getHaloCatalog(MarkovState &state, size_t cat_idx) {
    return state.get<GalaxyElement>(str(format("halo_catalog_%d") % cat_idx))
        ->get();
  }

  template <typename Function>
  SurveyPreparer resolveHaloSurvey(MarkovState &state, Function f) {
    return SurveyPreparer(
        [f, &state](
            size_t cat_idx, ArrayType::ArrayType &grid, size_t *const &N,
            double *const &corner, double *const &L,
            double *const &delta) -> size_t {
          //return 0;
          return f(getHaloCatalog(state, cat_idx), grid, N, corner, L, delta);
        });
  }

  static void initializeHaloSimulationCatalog(
      MarkovState &state, ptree &main_params, int cat_idx) {
    using PrepareDetail::ArrayDimension;
    size_t N[3], localNdata[6], Ndata[3];

    state.getScalarArray<long, 3>("N", N);
    state.getScalarArray<long, 3>("Ndata", Ndata);
    state.getScalarArray<long, 6>("localNdata", localNdata);
    Console &cons = Console::instance();
    ptree &params = main_params.get_child(get_catalog_group_name(cat_idx));

    // Add a catalog in the state structure
    state.newElement(
        format("halo_catalog_%d") % cat_idx,
        new GalaxyElement(new GalaxySurveyType()));
    // Add its linear bias in the MCMC structure
    SDouble *nmean = new SDouble();
    ArrayType1d *bias = new ArrayType1d(boost::extents[0]);
    state.newElement(format("galaxy_bias_%d") % cat_idx, bias, true);
    state.newElement(format("galaxy_nmean_%d") % cat_idx, nmean, true);
    bias->setAutoResize(true);

    auto data_ext = boost::extents[range(localNdata[0], localNdata[1])][range(
        localNdata[2], localNdata[3])][range(localNdata[4], localNdata[5])];
    auto data_dim = ArrayDimension(Ndata[0], Ndata[1], Ndata[2]);

    SelArrayType *sel_grid = new SelArrayType(data_ext);
    ArrayType *data_grid = new ArrayType(data_ext);

    data_grid->setRealDims(data_dim);
    sel_grid->setRealDims(data_dim);
    state.newScalar<bool>(format("galaxy_bias_ref_%d") % cat_idx, false);
    state.newElement(format("galaxy_sel_window_%d") % cat_idx, sel_grid);
    state.newElement(format("galaxy_data_%d") % cat_idx, data_grid);

    string halocut =
        to_lower_copy(params.get<string>("halo_selection", "none"));
    auto info_sel = new InfoSampleSelection();
    info_sel->value.projection =
        state.getScalar<ProjectionDataModel>("projection_model");
    state.newElement(format("galaxy_selection_info_%d") % cat_idx, info_sel);
    if (halocut == "none") {
      cons.print<LOG_DEBUG>("Apply no cut on halo catalog");
    } else if (halocut == "mass") {
      cons.print<LOG_DEBUG>("Apply mass cuts on halo catalog");
    } else if (halocut == "radius") {
      cons.print<LOG_DEBUG>("Apply radius cuts on halo catalog");
    } else if (halocut == "spin") {
      cons.print<LOG_DEBUG>("Apply spin cuts on halo catalog");
    } else if (halocut == "mixed") {
      cons.print<LOG_DEBUG>("Apply mixed cuts on halo catalog");
    }
  }

  static void buildNoneSelectionForSimulation(
      GalaxySurveyType &sim, MarkovState &state, ptree &params, int cat_idx,
      CosmologicalParameters &cosmo_params, SurveyPreparer &preparer) {
    namespace ph = std::placeholders;
    GalaxySampleSelection &infosel =
        state
            .get<InfoSampleSelection>(
                format("galaxy_selection_info_%d") % cat_idx)
            ->value;
    infosel.selector = makeSelector(
        cutterFunction(NoneCutter<GalaxySurveyType>(infosel, &sim)));

    switch (infosel.projection) {
    case NGP_PROJECTION:
      preparer = resolveHaloSurvey(
          state,
          std::bind(
              galaxySurveyToGridGeneric<
                  ModifiedNGP<double, NGPGrid::NGP, true>, CIC_Tools::Periodic,
                  GalaxySurveyType, ArrayType::ArrayType, double *, size_t *,
                  NoneCutter<GalaxySurveyType>>,
              ph::_1, ph::_2, ph::_3, ph::_4, ph::_5, ph::_6,
              NoneCutter<GalaxySurveyType>(infosel, &sim),
              std::function<void()>()));
      break;
    case LUMINOSITY_CIC_PROJECTION:
      preparer = resolveHaloSurvey(
          state, std::bind(
                     galaxySurveyToGridGeneric<
                         ClassicCloudInCell<double, true>, CIC_Tools::Periodic,
                         GalaxySurveyType, ArrayType::ArrayType, double *,
                         size_t *, NoneCutter<GalaxySurveyType>>,
                     ph::_1, ph::_2, ph::_3, ph::_4, ph::_5, ph::_6,
                     NoneCutter<GalaxySurveyType>(infosel, &sim),
                     std::function<void()>()));
      break;
    default:
      error_helper<ErrorParams>("Unsupported data projection");
      break;
    }
  }

  static void buildMassSelectionForSimulation(
      GalaxySurveyType &sim, MarkovState &state, ptree &params, int cat_idx,
      CosmologicalParameters &cosmo_params, SurveyPreparer &preparer) {
    namespace ph = std::placeholders;
    LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

    GalaxySampleSelection &infosel =
        state
            .get<InfoSampleSelection>(
                format("galaxy_selection_info_%d") % cat_idx)
            ->value;
    infosel.low_mass_cut = params.get<double>("halo_low_mass_cut");
    infosel.high_mass_cut = params.get<double>("halo_high_mass_cut");
    infosel.selector = makeSelector(
        cutterFunction(MassCutter<GalaxySurveyType>(infosel, &sim)));

    switch (infosel.projection) {
    case NGP_PROJECTION:
      preparer = resolveHaloSurvey(
          state,
          std::bind(
              galaxySurveyToGridGeneric<
                  ModifiedNGP<double, NGPGrid::NGP, true>, CIC_Tools::Periodic,
                  GalaxySurveyType, ArrayType::ArrayType, double *, size_t *,
                  MassCutter<GalaxySurveyType>>,
              ph::_1, ph::_2, ph::_3, ph::_4, ph::_5, ph::_6,
              MassCutter<GalaxySurveyType>(infosel, &sim),
              std::function<void()>()));
      break;
    case LUMINOSITY_CIC_PROJECTION:
      ctx.print("Using cic mass projection");
      preparer = resolveHaloSurvey(
          state, std::bind(
                     galaxySurveyToGridGeneric<
                         ClassicCloudInCell<double, true>, CIC_Tools::Periodic,
                         GalaxySurveyType, ArrayType::ArrayType, double *,
                         size_t *, MassCutter<GalaxySurveyType>>,
                     ph::_1, ph::_2, ph::_3, ph::_4, ph::_5, ph::_6,
                     MassCutter<GalaxySurveyType>(infosel, &sim),
                     std::function<void()>()));
      break;
    default:
      error_helper<ErrorParams>("Unsupported data projection");
      break;
    }
  }

  static void buildRadiusSelectionForSimulation(
      GalaxySurveyType &sim, MarkovState &state, ptree &params, int cat_idx,
      CosmologicalParameters &cosmo_params, SurveyPreparer &preparer) {

    GalaxySampleSelection &infosel =
        state
            .get<InfoSampleSelection>(
                format("galaxy_selection_info_%d") % cat_idx)
            ->value;
    infosel.small_radius_cut = params.get<double>("small_radius_cut");
    infosel.large_radius_cut = params.get<double>("large_radius_cut");
    infosel.selector = makeSelector(
        cutterFunction(RadiusCutter<GalaxySurveyType>(infosel, &sim)));
    namespace ph = std::placeholders;

    switch (infosel.projection) {
    case NGP_PROJECTION:
      preparer = resolveHaloSurvey(
          state,
          std::bind(
              galaxySurveyToGridGeneric<
                  ModifiedNGP<double, NGPGrid::NGP, true>, CIC_Tools::Periodic,
                  GalaxySurveyType, ArrayType::ArrayType, double *, size_t *,
                  RadiusCutter<GalaxySurveyType>>,
              ph::_1, ph::_2, ph::_3, ph::_4, ph::_5, ph::_6,
              RadiusCutter<GalaxySurveyType>(infosel, &sim),
              std::function<void()>()));
      break;
    case LUMINOSITY_CIC_PROJECTION:
      preparer = resolveHaloSurvey(
          state, std::bind(
                     galaxySurveyToGridGeneric<
                         ClassicCloudInCell<double, true>, CIC_Tools::Periodic,
                         GalaxySurveyType, ArrayType::ArrayType, double *,
                         size_t *, RadiusCutter<GalaxySurveyType>>,
                     ph::_1, ph::_2, ph::_3, ph::_4, ph::_5, ph::_6,
                     RadiusCutter<GalaxySurveyType>(infosel, &sim),
                     std::function<void()>()));
      break;
    default:
      error_helper<ErrorParams>("Unsupported data projection");
      break;
    }
  }

  static void buildSpinSelectionForSimulation(
      GalaxySurveyType &sim, MarkovState &state, ptree &params, int cat_idx,
      CosmologicalParameters &cosmo_params, SurveyPreparer &preparer) {

    GalaxySampleSelection &infosel =
        state
            .get<InfoSampleSelection>(
                format("galaxy_selection_info_%d") % cat_idx)
            ->value;
    infosel.low_spin_cut = params.get<double>("halo_low_spin_cut");
    infosel.high_spin_cut = params.get<double>("halo_high_spin_cut");
    infosel.selector = makeSelector(
        cutterFunction(SpinCutter<GalaxySurveyType>(infosel, &sim)));
    namespace ph = std::placeholders;

    switch (infosel.projection) {
    case NGP_PROJECTION:
      preparer = resolveHaloSurvey(
          state,
          std::bind(
              galaxySurveyToGridGeneric<
                  ModifiedNGP<double, NGPGrid::NGP, true>, CIC_Tools::Periodic,
                  GalaxySurveyType, ArrayType::ArrayType, double *, size_t *,
                  SpinCutter<GalaxySurveyType>>,
              ph::_1, ph::_2, ph::_3, ph::_4, ph::_5, ph::_6,
              SpinCutter<GalaxySurveyType>(infosel, &sim),
              std::function<void()>()));
      break;
    case LUMINOSITY_CIC_PROJECTION:
      preparer = resolveHaloSurvey(
          state, std::bind(
                     galaxySurveyToGridGeneric<
                         ClassicCloudInCell<double, true>, CIC_Tools::Periodic,
                         GalaxySurveyType, ArrayType::ArrayType, double *,
                         size_t *, SpinCutter<GalaxySurveyType>>,
                     ph::_1, ph::_2, ph::_3, ph::_4, ph::_5, ph::_6,
                     SpinCutter<GalaxySurveyType>(infosel, &sim),
                     std::function<void()>()));
      break;
    default:
      error_helper<ErrorParams>("Unsupported data projection");
      break;
    }
  }

  static void buildMixedSelectionForSimulation(
      GalaxySurveyType &sim, MarkovState &state, ptree &params, int cat_idx,
      CosmologicalParameters &cosmo_params, SurveyPreparer &preparer,
      boost::tokenizer<> &tokenList) {

    namespace ph = std::placeholders;
    GalaxySampleSelection &infosel =
        state
            .get<InfoSampleSelection>(
                format("galaxy_selection_info_%d") % cat_idx)
            ->value;

    MixedCutter<GalaxySurveyType> mixer;

    for (auto &tok : tokenList) {
      if (tok == "mass") {
        mixer.addCutter(MassCutter<GalaxySurveyType>(infosel, &sim));
        infosel.low_mass_cut = params.get<double>("halo_low_mass_cut");
        infosel.high_mass_cut = params.get<double>("halo_high_mass_cut");
      } else if (tok == "radius") {
        mixer.addCutter(RadiusCutter<GalaxySurveyType>(infosel, &sim));
        infosel.small_radius_cut = params.get<double>("halo_small_radius_cut");
        infosel.large_radius_cut = params.get<double>("halo_large_radius_cut");
      } else if (tok == "spin") {
        mixer.addCutter(SpinCutter<GalaxySurveyType>(infosel, &sim));
        infosel.low_spin_cut = params.get<double>("halo_low_spin_cut");
        infosel.high_spin_cut = params.get<double>("halo_high_spin_cut");
      } else {
        error_helper<ErrorParams>(
            format("Request to cut based on %s, which is not a recognized "
                   "option") %
            tok);
      }
    }

    infosel.selector = makeSelector(cutterFunction(mixer));

    switch (infosel.projection) {
    case NGP_PROJECTION:
      preparer = resolveHaloSurvey(
          state,
          std::bind(
              galaxySurveyToGridGeneric<
                  ModifiedNGP<double, NGPGrid::NGP, true>, CIC_Tools::Periodic,
                  GalaxySurveyType, ArrayType::ArrayType, double *, size_t *,
                  MixedCutter<GalaxySurveyType>>,
              ph::_1, ph::_2, ph::_3, ph::_4, ph::_5, ph::_6, mixer,
              std::function<void()>()));
      break;
    case LUMINOSITY_CIC_PROJECTION:
      preparer = resolveHaloSurvey(
          state, std::bind(
                     galaxySurveyToGridGeneric<
                         ClassicCloudInCell<double, true>, CIC_Tools::Periodic,
                         GalaxySurveyType, ArrayType::ArrayType, double *,
                         size_t *, MixedCutter<GalaxySurveyType>>,
                     ph::_1, ph::_2, ph::_3, ph::_4, ph::_5, ph::_6, mixer,
                     std::function<void()>()));
      break;
    default:
      error_helper<ErrorParams>("Unsupported data projection");
      break;
    }
  }

  static void loadHaloSimulationCatalog(
      MarkovState &state, ptree &main_params, int cat_idx,
      CosmologicalParameters &cosmo_params) {
    ConsoleContext<LOG_INFO_SINGLE> ctx(
        str(format("loadHaloSimulationCatalog(%d)") % cat_idx));
    auto &sim = getHaloCatalog(state, cat_idx);
    ptree &params = main_params.get_child(get_catalog_group_name(cat_idx));
    std::string data_format = params.get<std::string>("dataformat", "TXT");

    if (data_format == "TXT") {
      loadHaloSimulationFromText(params.get<string>("datafile"), sim);
    } else if (data_format == "HDF5") {
      loadHaloSimulationFromHDF5(
          params.get<string>("datafile"), params.get<string>("datakey"), sim);
    } else if (data_format == "NONE") {
      Console::instance().print<LOG_INFO_SINGLE>("No data to be loaded");
    } else {
      error_helper<ErrorParams>(
          boost::format("Unknown data format '%s'") % data_format);
    }

    sim.resetWeight();

    state.getScalar<bool>(format("galaxy_bias_ref_%d") % cat_idx) =
        params.get<bool>("refbias");

    ArrayType1d::ArrayType &hbias =
        *(state.get<ArrayType1d>(format("galaxy_bias_%d") % cat_idx)->array);
    if (boost::optional<std::string> bvalue =
            params.get_optional<std::string>("bias")) {
      auto bias_double = string_as_vector<double>(*bvalue, ", ");
      hbias.resize(boost::extents[bias_double.size()]);
      std::copy(bias_double.begin(), bias_double.end(), hbias.begin());
      ctx.print("Set the bias to [" + to_string(bias_double) + "]");
    } else {
      ctx.print("No initial bias value set, use bias=1");
      hbias.resize(boost::extents[1]);
      hbias[0] = 1;
    }

    double &nmean =
        state.get<SDouble>(format("galaxy_nmean_%d") % cat_idx)->value;
    if (boost::optional<double> nvalue = params.get_optional<double>("nmean")) {
      nmean = *nvalue;
    } else {
      ctx.print("No initial mean density value set, use nmean=1");
      nmean = 1;
    }
  }

  static void setupSimulationCatalog(
      MarkovState &state, ptree &main_params, int cat_idx,
      CosmologicalParameters &cosmo_params, SurveyPreparer &preparer) {
    ptree &params = main_params.get_child(get_catalog_group_name(cat_idx));
    string halocut = to_lower_copy(params.get<string>("halo_selection"));
    auto &sim = getHaloCatalog(state, cat_idx);

    GalaxySelectionType &gsel_type =
        state
            .newScalar<GalaxySelectionType>(
                format("galaxy_selection_type_%d") % cat_idx,
                GALAXY_SELECTION_FILE)
            ->value;

    if (halocut == "none") {
      gsel_type = HALO_SELECTION_NONE;
      buildNoneSelectionForSimulation(
          sim, state, params, cat_idx, cosmo_params, preparer);
    } else if (halocut == "mass") {
      gsel_type = HALO_SELECTION_MASS;
      buildMassSelectionForSimulation(
          sim, state, params, cat_idx, cosmo_params, preparer);
    } else if (halocut == "radius") {
      gsel_type = HALO_SELECTION_RADIUS;
      buildRadiusSelectionForSimulation(
          sim, state, params, cat_idx, cosmo_params, preparer);
    } else if (halocut == "spin") {
      gsel_type = HALO_SELECTION_SPIN;
      buildSpinSelectionForSimulation(
          sim, state, params, cat_idx, cosmo_params, preparer);
    } else if (halocut == "mixed") {
      gsel_type = HALO_SELECTION_MIXED;
      string cutList = to_lower_copy(params.get<string>("list_of_cuts"));
      boost::tokenizer<> tokenList(cutList);
      buildMixedSelectionForSimulation(
          sim, state, params, cat_idx, cosmo_params, preparer, tokenList);
    } else {
      error_helper<ErrorParams>(
          format("halocut has value %s, which is not recognized") % halocut);
    }
  }

  void prepareHaloSimulationData(
      MPI_Communication *comm, MarkovState &state, int cat_idx,
      CosmologicalParameters &cosmo_params, SurveyPreparer const &preparer,
      ptree &main_params) {
    using CosmoTool::InvalidRangeException;

    size_t Ndata[3], localNdata[6];
    double L[3], delta[3], corner[3];

    state.getScalarArray<long, 3>("Ndata", Ndata);
    state.getScalarArray<long, 6>("localNdata", localNdata);
    state.getScalarArray<double, 3>("L", L);
    state.getScalarArray<double, 3>("corner", corner);

    ConsoleContext<LOG_INFO_SINGLE> ctx("data preparation");
    Cosmology cosmo(cosmo_params);

    ptree &sys_params = main_params.get_child("system");
    ptree &g_params = main_params.get_child(get_catalog_group_name(cat_idx));

    ctx.print(
        format("Project data to density field grid (catalog %d)") % cat_idx);

    GalaxySurveyType &sim =
        state.get<GalaxyElement>(str(format("halo_catalog_%d") % cat_idx))
            ->get();
    ArrayType *data_grid =
        state.get<ArrayType>(format("galaxy_data_%d") % cat_idx);

    delta[0] = L[0] / Ndata[0];
    delta[1] = L[1] / Ndata[1];
    delta[2] = L[2] / Ndata[2];

    fwrap(*(data_grid->array)) = 0;

    size_t numHalos =
        preparer(cat_idx, *(data_grid->array), Ndata, corner, L, delta);
    comm->all_reduce_t(MPI_IN_PLACE, &numHalos, 1, MPI_SUM);
    if (numHalos == 0) {
      error_helper<ErrorBadState>(
          format("No halo at all in catalog %d") % cat_idx);
    }

    GalaxySelectionType &gsel_type = state.getScalar<GalaxySelectionType>(
        format("galaxy_selection_type_%d") % cat_idx);
    SelArrayType *sel_grid =
        state.get<SelArrayType>(format("galaxy_sel_window_%d") % cat_idx);
    LibLSS::array::fill(
        *sel_grid->array, 1); //fixes ambiguity when using VIRBIUS
    PrepareDetail::cleanup_data(*data_grid->array, *sel_grid->array);
  }
} // namespace LibLSS_prepare

#endif
