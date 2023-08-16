/// Docs for forward_model
/*+
    ARES/HADES/BORG Package -- -- ./libLSS/physics/forward_model.hpp
    Copyright (C) 2014-2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2019 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2016-2019)

    This program is free software; you can redistribute it and/or modify it
    under the terms of either the CeCILL license or the GNU General Public
    license, as included with the software package.

    The text of the license is located in Licence_CeCILL_V2.1-en.txt
    and GPL.txt in the root directory of the source package.

+*/

#include <boost/preprocessor/stringize.hpp>
#include <boost/preprocessor/seq/for_each.hpp>
#include <boost/multi_array.hpp>
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/errors.hpp"
#include "libLSS/tools/hdf5_type.hpp"
#include "libLSS/physics/forward_model.hpp"

using namespace LibLSS;

void BORGForwardModel::setup(bool distinct_io) {
  Console::instance().print<LOG_VERBOSE>("Setup FWD");
  LibLSS::ConsoleContext<LOG_VERBOSE> ctx("BORGForwardModel::setup");
  volume = L0 * L1 * L2;
  volNorm = volume / (N0 * N1 * N2);

  vobs.resize(boost::extents[3]);

  lo_mgr = std::make_unique<DFT_Manager>(
      box_input.N0, box_input.N1, box_input.N2, comm);

  startN0 = lo_mgr->startN0;
  localN0 = lo_mgr->localN0;
  N2_HC = lo_mgr->N2_HC;
  N2real = lo_mgr->N2real;

  if (distinct_io) {
    out_mgr = std::make_unique<DFT_Manager>(
        box_output.N0, box_output.N1, box_output.N2, comm);
  } else
    out_mgr = lo_mgr;

  analysis_plan = 0;
  synthesis_plan = 0;
}

void BORGForwardModel::setupDefault() {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  ctx.print("Allocate real");
  tmp_real_field = lo_mgr->allocate_ptr_array();
  ctx.print("Allocate complex");
  tmp_complex_field = lo_mgr->allocate_ptr_complex_array();

  ctx.print("Plan r2c");
  analysis_plan = lo_mgr->create_r2c_plan(
      tmp_real_field->get_array().data(),
      tmp_complex_field->get_array().data());
  ctx.print("Plan 2c2r");
  synthesis_plan = lo_mgr->create_c2r_plan(
      tmp_complex_field->get_array().data(),
      tmp_real_field->get_array().data());
}

void BORGForwardModel::setCosmoParams(
    const CosmologicalParameters &p_cosmo_params) {
  this->cosmo_params = p_cosmo_params;
  this->params["cosmology"] = p_cosmo_params;
  updateCosmo();
}

#define COSMO_ATTRIBUTE(r, q, element)                                         \
  {                                                                            \
    BOOST_PP_STRINGIZE(element),                                               \
        [](CosmologicalParameters &p, double v) { p.element = v; }             \
  },

// clang-format off
static std::map<
    std::string, std::function<void(CosmologicalParameters &, double)>>
    g_dispatcher{
  BOOST_PP_SEQ_FOR_EACH(COSMO_ATTRIBUTE, _,
       (sigma8)(omega_r)
       (omega_m)(omega_k)(omega_b)(omega_q)(w)(n_s)(fnl)(wprime)(h)
  )
};
// clang-format on

void BORGForwardModel::setModelParams(ModelDictionnary const &params) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  bool runUpdateCosmo = false;
  for (auto &x : params) {
    // Special cases, cosmology can also be updated that way.
    if (x.first.rfind("cosmology.") == 0) {
      ctx.format("Updating cosmo params %s", x.first.substr(10));
      g_dispatcher[x.first.substr(10)](
          this->cosmo_params, boost::any_cast<double>(x.second));
      runUpdateCosmo = true;
    } else
      this->params[x.first] = x.second;
  }
  if (runUpdateCosmo)
    setCosmoParams(this->cosmo_params);
}
