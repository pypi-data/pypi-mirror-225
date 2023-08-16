/*+
    ARES/HADES/BORG Package -- ./extra/hades/src/likelihood_info.cpp
    Copyright (C) 2018 Natalia Porqueres <natalia_porqueres@hotmail.com>
    Copyright (C) 2018 Doogesh Kodi Ramanah <ramanah@iap.fr>
    Copyright (C) 2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2018 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <string>
#include "libLSS/tools/console.hpp"
#include "common/preparation_types.hpp"
#include "common/preparation_tools.hpp"
#include "likelihood_info.hpp"
#include "libLSS/physics/likelihoods/base.hpp"
#include "libLSS/data/integer_window3d.hpp"
#include <healpix_cxx/pointing.h>
#include <healpix_cxx/healpix_map.h>
#include <healpix_cxx/healpix_map_fitsio.h>
#include <H5Cpp.h>
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/tools/fuse/healpix.hpp"

using namespace LibLSS;

namespace {
  class ColorAdaptor {

  public:
    Healpix_Map<double> sky;
    double rmin, rmax;
    int slices;
    unsigned int max_color;
    // Use concepts of sky selection

    ColorAdaptor(double rmin_, double rmax_, int slices_)
        : rmin(rmin_), rmax(rmax_), slices(slices_) {}

    void loadSky(const std::string &fname) {
      read_Healpix_map_from_fits(fname, sky);
      for (long n = 0; n < sky.Npix(); n++) {
        if (std::isnan(sky[n]))
          sky[n] = 0;
      }
      max_color = fwrap(sky).max() + 1;
    }

    unsigned int get_sky_completeness(double x, double y, double z) const {
      return sky[sky.vec2pix(vec3(x, y, z))];
    }

    int getNumRadial() const { return 0; }

    unsigned int getRadialSelection(double r, int) const {
      int slice = std::floor(slices * (r - rmin) / (rmax - rmin));
      if ((slice < 0) or (slice > slices)) {
        Console::instance().format<LOG_ERROR>(
            "Slice is %d (max=%d) for r=%g", slice, slices, r);
        error_helper<ErrorParams>("Invalid radial position.");
      }
      return max_color * (unsigned int)(slice);
    }
  };

} // namespace

void LibLSS_prepare::setupLikelihoodInfo(
    MPI_Communication *comm, LibLSS::MarkovState &state, LikelihoodInfo &info,
    LibLSS_prepare::ptree &params, bool resuming) {
  ConsoleContext<LOG_DEBUG> ctx("setupLikelihoodInfo");

  Likelihood::GridLengths gridLength(boost::extents[6]);
  gridLength[0] = state.getScalar<double>("corner0");
  gridLength[1] = gridLength[0] + state.getScalar<double>("L0");
  gridLength[2] = state.getScalar<double>("corner1");
  gridLength[3] = gridLength[2] + state.getScalar<double>("L1");
  gridLength[4] = state.getScalar<double>("corner2");
  gridLength[5] = gridLength[4] + state.getScalar<double>("L2");

  info[Likelihood::GRID_LENGTH] = gridLength;

  Likelihood::GridSize grid(boost::extents[3]);
  state.getScalarArray<long, 3>("N", grid);
  info[Likelihood::GRID] = grid;
  state.getScalarArray<long, 3>("Ndata", grid);
  info[Likelihood::DATA_GRID] = grid;

  info[Likelihood::MPI] = comm;

  auto like_params = params.get_child_optional("likelihood");
  if (!like_params) {
    ctx.print2<LOG_WARNING>("No [likelihood] section in params tree");
    return;
  }

  ctx.print("Inspecting likelihood options");
  if (auto eft_lambda =
          like_params->template get_optional<double>("EFT_Lambda")) {
    info["EFT_Lambda"] = *eft_lambda;
  }

  if (auto manypower_prior =
          like_params->template get_optional<double>("ManyPower_prior_width")) {
    info["ManyPower_prior_width"] = *manypower_prior;
  }

  // === sigma8 sampler-specific part ===
  if (auto val =
          like_params->template get_optional<double>("sigma8_step")) {
    info["sigma8_step"] = *val;
  }
  if (auto val =
          like_params->template get_optional<double>("sigma8_min")) {
    info["sigma8_min"] = *val;
  }
  if (auto val =
          like_params->template get_optional<double>("sigma8_max")) {
    info["sigma8_max"] = *val;
  }

  // ==================================

  if (auto robust_map =
          like_params->template get_optional<std::string>("colormap_3d")) {

    ctx.print2<LOG_INFO_SINGLE>("Robust MAP provided: " + (*robust_map));
    H5::H5File f(*robust_map, H5F_ACC_RDONLY);

    long N0 = state.getScalar<long>("N0");
    long N1 = state.getScalar<long>("N1");
    long N2 = state.getScalar<long>("N2");

    auto cmap_like = std::shared_ptr<boost::multi_array<long, 3>>(
        new boost::multi_array<long, 3>(boost::extents[N0][N1][N2]));
    CosmoTool::hdf5_read_array(f, "map", *cmap_like);

    info[Likelihood::COLOR_MAP] = cmap_like;
  } else if (
      auto robust_map =
          like_params->template get_optional<std::string>("colormap_sky")) {
    ctx.print2<LOG_INFO_SINGLE>("Robust SKYMAP provided: " + (*robust_map));

    double rmax = like_params->template get<double>("rmax");
    int numSlices = like_params->template get<int>("slices");

    auto &rng = state.get<RandomGen>("random_generator")->get();
    long startN0 = state.getScalar<long>("startN0");
    long localN0 = state.getScalar<long>("localN0");
    double L[3];
    size_t Ndata[3];
    double xmin[3];
    size_t localNdata[6];

    state.getScalarArray<double, 3>("L", L);
    state.getScalarArray<double, 3>("corner", xmin);
    state.getScalarArray<long, 3>("Ndata", Ndata);
    state.getScalarArray<long, 6>("localNdata", localNdata);

    double delta[3];
    std::transform(
        L, L + 3, Ndata, delta, [](double l, size_t n) { return l / n; });

    ColorAdaptor colormap(0, rmax, numSlices);
    auto colormapElement =
        new ArrayStateElement<long, 3, track_allocator<long>, true>(
            boost::extents[range(localNdata[0], localNdata[1])][Ndata[1]]
                          [Ndata[2]]);
    colormapElement->setRealDims(ArrayDimension(Ndata[0], Ndata[1], Ndata[2]));

    state.newElement("colormap3d", colormapElement);

    colormap.loadSky(*robust_map);

    std::shared_ptr<boost::multi_array_ref<long, 3>> cmap =
        colormapElement->array;
    auto promise = make_promise_pointer(cmap);
    info[Likelihood::COLOR_MAP] = promise;

    if (!resuming) {
      computeMajorityVoteWindow3d(
          comm, rng, colormap, *colormapElement->array, L, delta, xmin, Ndata, 1000);
      promise.defer.submit_ready();
    } else {
      colormapElement->deferLoad.ready(
          [promise]() mutable { promise.defer.submit_ready(); });
    }

    {
      std::string fname = "dump_colormap.h5_" + std::to_string(comm->rank());
      H5::H5File f(fname.c_str(), H5F_ACC_TRUNC);
      CosmoTool::hdf5_write_array(f, "cmap", *colormapElement->array);
      CosmoTool::hdf5_write_array(
          f, "sky",
          boost::multi_array_ref<double, 1>(
              (double *)&colormap.sky.Map()[0],
              boost::extents[colormap.sky.Npix()]));
    }
  }
}

// ARES TAG: authors_num = 4
// ARES TAG: name(0) = Natalia Porqueres
// ARES TAG: email(0) = natalia_porqueres@hotmail.com
// ARES TAG: year(0) = 2018
// ARES TAG: name(1) = Doogesh Kodi Ramanah
// ARES TAG: email(1) = ramanah@iap.fr
// ARES TAG: year(1) = 2018
// ARES TAG: name(2) = Guilhem Lavaux
// ARES TAG: email(2) = guilhem.lavaux@iap.fr
// ARES TAG: year(2) = 2018
// ARES TAG: name(3) = Jens Jasche
// ARES TAG: email(3) = jens.jasche@fysik.su.se
// ARES TAG: year(3) = 2018
