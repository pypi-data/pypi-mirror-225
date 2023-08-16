/*+
    ARES/HADES/BORG Package -- ./src/common/preparation_tools.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_ARES_COMMON_PREPARATION_TOOLS_HPP
#define __LIBLSS_ARES_COMMON_PREPARATION_TOOLS_HPP

#include <functional>
#include "libLSS/tools/console.hpp"
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>
#include "libLSS/tools/ptree_translators.hpp"
#include <boost/algorithm/string.hpp>
#include <boost/optional/optional.hpp>
#include "libLSS/data/spectro_gals.hpp"
#include "libLSS/data/galaxies.hpp"
#include "libLSS/data/projection.hpp"
#include "libLSS/data/linear_selection.hpp"
#include "libLSS/data/window3d.hpp"
#include "libLSS/data/window3d_post.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/data/schechter_completeness.hpp"
#include <CosmoTool/interpolate.hpp>
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_assign.hpp"
#include "libLSS/tools/fusewrapper.hpp"

#include "preparation_types.hpp"

namespace LibLSS_prepare {

  namespace PrepareDetail {
    static boost::array<int, 3> ArrayDimension(int a, int b, int c) {
      boost::array<int, 3> A;

      A[0] = a;
      A[1] = b;
      A[2] = c;
      return A;
    }

    static boost::array<int, 4> ArrayDimension(int a, int b, int c, int d) {
      boost::array<int, 4> A;
      A[0] = a;
      A[1] = b;
      A[2] = c;
      A[3] = d;
      return A;
    }

    template <typename ptree, typename SelFunction3d, typename SelGrid>
    void compute_window(
        ptree &sys_params, MPI_Communication *comm, SelFunction3d &fg,
        LibLSS::MarkovState &state, SelGrid &sel_grid, bool filter_mask) {

      ConsoleContext<LOG_DEBUG> ctx("compute_window");
      size_t N[3];
      double L[3], delta[3], corner[3];

      N[0] = state.getScalar<long>("Ndata0");
      N[1] = state.getScalar<long>("Ndata1");
      N[2] = state.getScalar<long>("Ndata2");

      L[0] = state.getScalar<double>("L0");
      L[1] = state.getScalar<double>("L1");
      L[2] = state.getScalar<double>("L2");

      corner[0] = state.getScalar<double>("corner0");
      corner[1] = state.getScalar<double>("corner1");
      corner[2] = state.getScalar<double>("corner2");

      delta[0] = L[0] / N[0];
      delta[1] = L[1] / N[1];
      delta[2] = L[2] / N[2];

      double precision = sys_params.get("mask_precision", 0.01);

      RGenType &rng = dynamic_cast<RGenType &>(
          state.get<RandomGen>("random_generator")->get());

      ctx.print(format("Use precision=%lg") % precision);

      compute_window_value_elem(
          comm, rng, fg, sel_grid, L, delta, corner, filter_mask, precision);
    }

    template <typename DataGrid, typename SelGrid>
    void cleanup_data(DataGrid &data, SelGrid &sel_grid) {
      LibLSS::copy_array(
          data,
          b_fused<double>(data, sel_grid, [](double d, double s) -> double {
            if (s <= 0)
              return 0;
            else
              return d;
          }));
    }
  } // namespace PrepareDetail

  static void
  buildGrowthFactor(MarkovState &state, CosmologicalParameters &cosmo_param) {
    Cosmology cosmo(cosmo_param);
    ArrayType::ArrayType &growth =
        *state.get<ArrayType>("growth_factor")->array;

    // No growth factor here
    std::fill(growth.data(), growth.data() + growth.num_elements(), 1);
  }

} // namespace LibLSS_prepare

namespace LibLSS {

  inline std::string get_catalog_group_name(int i) {
    return boost::str(boost::format("catalog_%d") % i);
  }

  enum RestoreOption { RESTORE, DO_NOT_RESTORE };

  template <typename T, typename PTree>
  T adapt_optional(
      MarkovState &state, boost::optional<PTree> &params,
      const std::string &name, T const &defval, RestoreOption restore = RESTORE,
      std::string const &target_name = "") {
    T r = defval;
    std::string target = (target_name == "") ? name : target_name;
    if (params) {
      r = params->template get<T>(name, defval);
    }
    auto state_scalar = state.newScalar<T>(target, r);
    state_scalar->setDoNotRestore(restore == DO_NOT_RESTORE);
    return r;
  }

  template <typename T, typename PTree>
  T adapt(
      MarkovState &state, PTree &params, const std::string &name,
      RestoreOption restore = RESTORE, std::string const &target_name = "") {
    std::string target = (target_name == "") ? name : target_name;
    T r = params.template get<T>(name);
    state.newScalar<T>(target, r)->setDoNotRestore(restore == DO_NOT_RESTORE);
    return r;
  }

  template <typename T, typename PTree>
  T adapt(
      MarkovState &state, PTree &params, const std::string &name,
      const T &defval, RestoreOption restore = RESTORE,
      std::string const &target_name = "") {
    std::string target = (target_name == "") ? name : target_name;
    T r = params.template get<T>(name, defval);
    state.newScalar<T>(target, r)->setDoNotRestore(restore == DO_NOT_RESTORE);
    return r;
  }

  namespace details {
    template <typename T, typename PTree>
    bool safe_get(PTree &t, const std::string &n, T &value) {
      boost::optional<T> v = t.template get_optional<T>(n);
      if (!v)
        return false;
      value = *v;
      return true;
    }

    template <typename T, typename PTree>
    T property_accessor(PTree &t, const std::string &n) {
      return t.template get<T>(n);
    }
  } // namespace details
} // namespace LibLSS

#endif
