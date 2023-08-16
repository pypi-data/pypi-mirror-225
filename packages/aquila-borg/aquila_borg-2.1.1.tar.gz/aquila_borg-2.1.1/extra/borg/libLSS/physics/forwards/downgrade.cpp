/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/forwards/downgrade.cpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <string>
#include "libLSS/tools/console.hpp"
#include "libLSS/physics/model_io.hpp"
#include "libLSS/physics/forwards/downgrade.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/physics/forwards/registry.hpp"
#include "libLSS/tools/ptree_proxy.hpp"
#include <boost/phoenix/stl/cmath.hpp>
#include "libLSS/tools/tuple_helper.hpp"
#include "libLSS/physics/bias/base.hpp"
#include "libLSS/physics/bias/level_combinator.hpp"

using namespace LibLSS;

static BoxModel half_box(BoxModel const &box) {
  BoxModel box2 = box;

  box2.N0 /= 2;
  box2.N1 /= 2;
  box2.N2 /= 2;
  return box2;
}

ForwardDowngrade::ForwardDowngrade(MPI_Communication *comm, BoxModel const &box)
    : BORGForwardModel(comm, box, half_box(box)) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  std::tuple<ssize_t, ssize_t> bounds[2];
  //Level_t::numLevel];
  //
  bounds[1] = std::make_tuple(0,0);//out_mgr->startN0, out_mgr->startN0 + out_mgr->localN0);
  bounds[0] = std::make_tuple(out_mgr->startN0, out_mgr->startN0 + out_mgr->localN0);

  for (int r = 0; r < Level_t::numLevel; r++) {
    ctx.format(
        ".. Level %d (bounds=[%d - %d])", r,
        std::get<0>(bounds[r]), std::get<1>(bounds[r]));
  }

  level.allocate(
      box.N0, box.N1, box.N2, lo_mgr->N2real, lo_mgr->startN0, lo_mgr->localN0,
      bounds);
  level.setup(ghosts, comm);

  ag_array = std::make_shared<U_Array>(lo_mgr->extents_real_strict());
}

void ForwardDowngrade::forwardModel_v2(ModelInput<3> delta_init) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  // Setup the IO basis that is required for this forward.
  delta_init.setRequestedIO(PREFERRED_REAL);

  ghosts.updatePlaneDims(std::array<ssize_t,2>{lo_mgr->N1, lo_mgr->N2real});
  ghosts.synchronize(delta_init.getReal());
  // Now build the different levels from the planes.
  level.buildLevels(ghosts, delta_init.getReal());

  hold_input = std::move(delta_init);
}

void ForwardDowngrade::getDensityFinal(ModelOutput<3> delta_output) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  delta_output.setRequestedIO(PREFERRED_REAL);
  auto w_delta_output = fwrap(array::slice_array(
      delta_output.getRealOutput(), out_mgr->strict_range()));

  ctx.format(
      "out = %dx%dx%d", (*w_delta_output).shape()[0],
      (*w_delta_output).shape()[1], (*w_delta_output).shape()[2]);
  ctx.format("in = %dx%dx%d", N0, N1, N2);

  w_delta_output =
      fwrap(b_fused_idx<double, 3>([this](size_t i, size_t j, size_t k) {
        constexpr int const numLevel = Level_t::numLevel;
        double out;
        if (k >= N2 / 2) {
          auto &cons = Console::instance();
          cons.format<LOG_ERROR>("Going above limits!");
          MPI_Communication::instance()->abort();
          return 0.0;
        }
        out = level.template get_density_level<1>(
            hold_input.getReal(), i, j, k);
        if (std::isnan(out) || std::isinf(out)) {
          auto &cons = Console::instance();
          //cons.c_assert(!std::isnan(out[numLevel-1]), "Nan in density");
          cons.format<LOG_ERROR>(
              "Nan (%g) in density at %dx%dx%d", out, i, j, k);
          MPI_Communication::instance()->abort();
        }
        return out;
      }));
}

void ForwardDowngrade::adjointModel_v2(ModelInputAdjoint<3> in_gradient_delta) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  // Build strict range views (we do not want to see the
  // the FFTW padding, ensure that the view object lives till the end of this function.

  in_gradient_delta.setRequestedIO(PREFERRED_REAL);

  ghosts.release();
  ghosts.updatePlaneDims(std::array<ssize_t,2>{lo_mgr->N1, lo_mgr->N2});
  ghosts.allocate();
  ghosts.clear_ghosts();
  level.clear_cache();

  fwrap(*ag_array) = 0;

  size_t startN0 = out_mgr->startN0;
  size_t endN0 = startN0 + out_mgr->localN0;
  size_t N1 = out_mgr->N1;
  size_t N2 = out_mgr->N2;

  auto &in_grad = in_gradient_delta.getRealConst();

#pragma omp parallel for collapse(3)
  for (size_t i = startN0; i < endN0; i++) {
    for (size_t j = 0; j < N1; j++) {
      for (size_t k = 0; k < N2; k++) {
        level.template push_ag_density_level<1>(
            in_grad[i][j][k], ag_array->get_array(), i, j, k);
      }
    }
  }

  level.ag_buildLevels(ghosts, ag_array->get_array());

  ghosts.synchronize_ag(ag_array->get_array());
}

void ForwardDowngrade::getAdjointModelOutput(
    ModelOutputAdjoint<3> out_gradient_delta) {
  out_gradient_delta.setRequestedIO(PREFERRED_REAL);
  // Remember: the output of the gradient is conformal to the input of the model (thus slicing with lo_mgr).
  auto w_out_gradient = fwrap(array::slice_array(out_gradient_delta.getRealOutput(), lo_mgr->strict_range()));

  w_out_gradient = fwrap(*ag_array);
}

static std::shared_ptr<BORGForwardModel> build_downgrade(
    MPI_Communication *comm, BoxModel const &box, PropertyProxy const &params) {

  // TODO: Setup transfer function
  auto model = std::make_shared<ForwardDowngrade>(comm, box);
  return model;
}

LIBLSS_REGISTER_FORWARD_IMPL(Downgrade, build_downgrade);

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
