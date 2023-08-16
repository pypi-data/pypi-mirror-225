/*+
    ARES/HADES/BORG Package -- ./src/common/foreground.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __ARES_FOREGROUND_HPP
#define __ARES_FOREGROUND_HPP

#include <boost/lexical_cast.hpp>
#include <boost/algorithm/string/split.hpp>
#include <cmath>
#include <string>
#include <healpix_cxx/pointing.h>
#include <healpix_cxx/healpix_map.h>
#include <healpix_cxx/healpix_map_fitsio.h>
#include "libLSS/samplers/core/main_loop.hpp"
#include "libLSS/samplers/ares/ares_sampler_option.hpp"
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/samplers/core/main_loop.hpp"
#include "preparation_tools.hpp"

namespace LibLSS_prepare {

  namespace details {

    class ForegroundAdaptor {
    protected:
      Healpix_Map<double> sky;

    public:
      // Use concepts of sky selection

      void loadSky(const std::string &fname) {
        read_Healpix_map_from_fits(fname, sky);
        for (long n = 0; n < sky.Npix(); n++) {
          if (std::isnan(sky[n]))
            sky[n] = 0;
        }
      }

      double get_sky_completeness(double x, double y, double z) const {
        return sky[sky.vec2pix(vec3(x, y, z))];
      }

      int getNumRadial() const { return 0; }

      double getRadialSelection(double r, int n) const { return 1; }
    };

  } // namespace details

  inline std::string get_foreground_group_name(int fg) {
    return boost::str(boost::format("foreground_%d") % fg);
  }

  template <typename ptree>
  void initForegrounds(
      LibLSS::MPI_Communication *comm, MarkovState &state,
      std::function<void(int, int)> add_combo, ptree &params) {
    using boost::format;
    using boost::str;
    using PrepareDetail::ArrayDimension;
    using namespace LibLSS;
    using namespace boost::algorithm;
    using std::string;

    ConsoleContext<LOG_INFO> ctx("initForegrounds");
    int Nforegrounds;
    long N0 = static_cast<SLong &>(state["N0"]),
         N1 = static_cast<SLong &>(state["N1"]),
         N2 = static_cast<SLong &>(state["N2"]),
         localN0 = static_cast<SLong &>(state["localN0"]),
         startN0 = static_cast<SLong &>(state["startN0"]);
    int Ncatalog = static_cast<SLong &>(state["NCAT"]);

    ptree sys_params = params.get_child("system");

    Nforegrounds = adapt<int>(state, sys_params, "NFOREGROUNDS", 0);

    ctx.print(format("Loading %d foreground data") % Nforegrounds);

    for (int fg = 0; fg < Nforegrounds; fg++) {
      ptree fg_params = params.get_child(get_foreground_group_name(fg));
      string fgmapname = fg_params.template get<std::string>("fgmap");

      ctx.print2<LOG_DEBUG>(format("Allocating 3d foreground %d") % fg);
      ArrayType *mask_grid = new ArrayType(
          boost::extents[range(startN0, startN0 + localN0)][N1][N2]);
      mask_grid->setRealDims(ArrayDimension(N0, N1, N2));

      state.newElement(format("foreground_3d_%d") % fg, mask_grid);
    }

    for (int c = 0; c < Ncatalog; c++) {
      ptree cat_params = params.get_child(get_catalog_group_name(c));
      int Ncoef;
      std::vector<string> fg_map_list_str, fg_map_values_str;
      bool value_provided = false;

      if (boost::optional<string> fg_option =
              cat_params.template get_optional<string>(
                  "fg_map_negative_list")) {
        ctx.print("Splitting '" + *fg_option + "'");
        split(fg_map_list_str, *fg_option, is_any_of(", "), token_compress_on);
      }
      if (boost::optional<string> fg_option =
              cat_params.template get_optional<string>(
                  "fg_map_negative_values")) {
        ctx.print("Splitting '" + *fg_option + "'");
        split(
            fg_map_values_str, *fg_option, is_any_of(", "), token_compress_on);
        value_provided = true;

        if (fg_map_values_str.size() != fg_map_list_str.size()) {
          error_helper<ErrorParams>(
              "If foreground values are provided they must have the same size "
              "as the foreground set");
        }
      }

      Ncoef = fg_map_list_str.size();

      ArrayType1d *fg_coefficient = new ArrayType1d(boost::extents[Ncoef]);
      IArrayType1d *fg_map = new IArrayType1d(boost::extents[Ncoef]);

      for (int e = 0; e < Ncoef; e++) {
        (*fg_map->array)[e] = boost::lexical_cast<int>(fg_map_list_str[e]);
        (*fg_coefficient->array)[e] =
            value_provided ? (boost::lexical_cast<double>(fg_map_values_str[e]))
                           : 0;

        adapt<bool>(
            state, sys_params,
            str(format("negative_foreground_%d_%d_blocked") % c % e), false);

        // Add a new (catalog,foreground) combo
        add_combo(c, (*fg_map->array)[e]);
      }

      state.newElement(
          format("catalog_foreground_coefficient_%d") % c, fg_coefficient,
          true);
      state.newElement(format("catalog_foreground_maps_%d") % c, fg_map);
    }
    adapt<bool>(state, sys_params, "total_foreground_blocked", false);
  }

  template <typename ptree>
  void loadForegrounds(
      LibLSS::MPI_Communication *comm, LibLSS::MainLoop &loop, ptree &params) {
    using boost::format;
    using boost::str;
    using PrepareDetail::ArrayDimension;
    using std::string;
    using namespace LibLSS;

    ConsoleContext<LOG_INFO> ctx("loadForegrounds");
    MarkovState &state = loop.get_state();
    int Nforegrounds;

    ptree sys_params = params.get_child("system");

    Nforegrounds = state.getScalar<int>("NFOREGROUNDS");
    ctx.print(format("Loading %d foregrounds") % Nforegrounds);

    for (int fg = 0; fg < Nforegrounds; fg++) {
      ptree fg_params = params.get_child(get_foreground_group_name(fg));
      string fgmapname = fg_params.template get<std::string>("fgmap");

      details::ForegroundAdaptor fg_a;

      fg_a.loadSky(fgmapname);

      ArrayType *mask_grid =
          state.get<ArrayType>(format("foreground_3d_%d") % fg);
      PrepareDetail::compute_window(
          sys_params, comm, fg_a, state, *mask_grid->array, false);
      mask_grid->loaded();
    }
  }

} // namespace LibLSS_prepare

#endif
