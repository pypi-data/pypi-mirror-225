/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/tests/test_modelio.cpp
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#define BOOST_TEST_MODULE modelio
#define BOOST_TEST_NO_MAIN
#define BOOST_TEST_ALTERNATIVE_INIT_API
#include <boost/test/included/unit_test.hpp>
#include <boost/test/data/test_case.hpp>
#include <H5Cpp.h>
#include <boost/multi_array.hpp>
#include "libLSS/tools/static_init.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/physics/model_io.hpp"
#include "libLSS/physics/hades_pt.hpp"
#include "libLSS/physics/hades_log.hpp"
#include "libLSS/tests/testFramework.hpp"
#include "libLSS/physics/hades_log.hpp"
#include "libLSS/tools/hdf5_error.hpp"
#include "libLSS/physics/chain_forward_model.hpp"
#include "libLSS/physics/forwards/primordial.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"

using namespace LibLSS;
using boost::extents;
using namespace CosmoTool;

namespace utf = boost::unit_test;

BOOST_AUTO_TEST_CASE(test_modelio_input) {
  BoxModel box{0, 0, 0, 100, 100, 100, 32, 32, 32};

  BOOST_CHECK_EQUAL(box.N0, 32);
  BOOST_CHECK_EQUAL(box.N1, 32);
  BOOST_CHECK_EQUAL(box.N2, 32);

  BOOST_TEST_CHECKPOINT("initialize manager");
  auto mgr = std::make_shared<FFTW_Manager<double, 3>>(
      box.N0, box.N1, box.N2, MPI_Communication::instance());

  BOOST_TEST_CHECKPOINT("allocate arrays");
  auto input_array_p = mgr->allocate_array();
  auto &input_array = input_array_p.get_array();

  BOOST_TEST_CHECKPOINT("fill up value");
  fwrap(input_array) = 1;

  {
    BOOST_TEST_CHECKPOINT("init modelio");
    ModelInput<3> io1(mgr, box, input_array);

    BOOST_TEST_CHECKPOINT("request output format");
    io1.setRequestedIO(PREFERRED_REAL);

    auto const &d = io1.getReal();
    BOOST_CHECK_CLOSE(d[0][0][0], 1, 0.1);
  }

  {
    BOOST_TEST_CHECKPOINT("init modelio");
    ModelInput<3> io1(mgr, box, input_array);

    BOOST_TEST_CHECKPOINT("request output format");
    io1.setRequestedIO(PREFERRED_FOURIER);

    BOOST_TEST_CHECKPOINT("obtain output");
    auto const &dhat = io1.getFourierConst();
    double dVol = std::pow(box.L0, 3);
    BOOST_CHECK_CLOSE(dhat[0][0][0].real(), dVol, 0.1);
  }
}

BOOST_AUTO_TEST_CASE(test_modelio_output) {
  BoxModel box{0, 0, 0, 100, 100, 100, 32, 32, 32};

  BOOST_CHECK_EQUAL(box.N0, 32);
  BOOST_CHECK_EQUAL(box.N1, 32);
  BOOST_CHECK_EQUAL(box.N2, 32);

  BOOST_TEST_CHECKPOINT("initialize manager");
  auto mgr = std::make_shared<FFTW_Manager<double, 3>>(
      box.N0, box.N1, box.N2, MPI_Communication::instance());

  BOOST_TEST_CHECKPOINT("allocate arrays");
  auto output_array_p = mgr->allocate_array();
  auto &output_array = output_array_p.get_array();

  {
    BOOST_TEST_CHECKPOINT("init modelio");
    ModelOutput<3> io1(mgr, box, output_array);

    BOOST_TEST_CHECKPOINT("request output format");
    io1.setRequestedIO(PREFERRED_REAL);

    auto &d = io1.getRealOutput();
    fwrap(d) = 1;
  }
  BOOST_CHECK_CLOSE(output_array[0][0][0], 1, 0.1);

  {
    BOOST_TEST_CHECKPOINT("init modelio");
    ModelOutput<3> io1(mgr, box, output_array);

    BOOST_TEST_CHECKPOINT("request output format");
    io1.setRequestedIO(PREFERRED_FOURIER);

    BOOST_TEST_CHECKPOINT("obtain fourier output");
    auto &dhat = io1.getFourierOutput();
    fwrap(dhat) = 0;
    dhat[0][0][0] = std::complex<double>(1.0, 0.0);
  }

  BOOST_CHECK_CLOSE(output_array[0][0][0], 1.0 / (100. * 100. * 100.), 0.1);
}

BOOST_AUTO_TEST_CASE(test_move) {
  BoxModel box{0, 0, 0, 100, 100, 100, 32, 32, 32};
  auto mgr = std::make_shared<FFTW_Manager<double, 3>>(
      box.N0, box.N1, box.N2, MPI_Communication::instance());

  BOOST_TEST_CHECKPOINT("allocate arrays");
  auto input_array_p = mgr->allocate_array();
  auto &input_array = input_array_p.get_array();

  BOOST_TEST_CHECKPOINT("fill up value");
  fwrap(input_array) = 1;

  {
    BOOST_TEST_CHECKPOINT("init modelio");
    ModelInput<3> io1(mgr, box, input_array);
    ModelInput<3> io2;

    io2 = std::move(io1);

    BOOST_TEST_CHECKPOINT("request output format");
    io2.setRequestedIO(PREFERRED_REAL);

    auto const &d = io2.getReal();
    BOOST_CHECK_CLOSE(d[0][0][0], 1, 0.1);
  }
}

BOOST_AUTO_TEST_CASE(test_modelio_pt) {
  BoxModel box{0, 0, 0, 100, 100, 100, 32, 32, 32};
  CosmologicalParameters cparams;

  cparams.a0 = 1.0;
  cparams.fnl = 0;
  cparams.h = 0.67;
  cparams.omega_b = 0.05;
  cparams.omega_k = 0.0;
  cparams.omega_m = 0.3;
  cparams.omega_q = 0.7;
  cparams.omega_r = 0.0;
  cparams.w = -1;
  cparams.wprime = 0;

  Cosmology cosmo(cparams);

  auto mgr = std::make_shared<FFTW_Manager<double, 3>>(
      box.N0, box.N1, box.N2, MPI_Communication::instance());

  HadesLinear fwd(MPI_Communication::instance(), box, box, 0.1, 1.0);
  auto input_delta_p = mgr->allocate_array();
  auto input_delta_c_p = mgr->allocate_complex_array();
  auto output_delta_p = mgr->allocate_array();
  auto ag_input_p = mgr->allocate_array();
  auto ag_output_c_p = mgr->allocate_complex_array();
  auto ag_output_p = mgr->allocate_array();
  auto output_delta_c_p = mgr->allocate_complex_array();

  auto &input_delta = input_delta_p.get_array();
  auto &input_delta_c = input_delta_c_p.get_array();
  auto &output_delta = output_delta_p.get_array();
  auto &output_delta_c = output_delta_c_p.get_array();
  auto &ag_input = ag_input_p.get_array();
  auto &ag_output_c = ag_output_c_p.get_array();
  auto &ag_output = ag_output_p.get_array();
  auto &ag_input_c = ag_output_c_p.get_array();

  array::fill(ag_input, 1.0);

  fwd.setCosmoParams(cparams);

  {
    LibLSS_tests::loadReferenceInput(box.N0, input_delta);
    double ref = input_delta[0][0][0];

    fwrap(input_delta) =
        fwrap(input_delta) * cosmo.d_plus(0.1) / cosmo.d_plus(1.0);

    fwd.forwardModel_v2(ModelInput<3>(mgr, box, input_delta));
    fwd.getDensityFinal(ModelOutput<3>(mgr, box, output_delta));

    BOOST_CHECK_CLOSE(output_delta[0][0][0], ref, 0.1);

    fwd.adjointModel_v2(ModelInputAdjoint<3>(mgr, box, ag_input));
    fwd.getAdjointModelOutput(ModelOutputAdjoint<3>(mgr, box, ag_input));

    double scale = cosmo.d_plus(0.1) / cosmo.d_plus(1.0);
    BOOST_CHECK_CLOSE(ag_input[0][0][0], 1.0 / scale, 0.1);
  }

  {
    LibLSS_tests::loadReferenceInput(box.N0, input_delta);
    LibLSS_tests::loadReferenceInput(box.N0, input_delta_c);

    fwrap(input_delta_c) = fwrap(input_delta_c) * ((box.L0 * box.L1 * box.L2) /
                                                   (box.N0 * box.N1 * box.N2));

    fwrap(input_delta) =
        fwrap(input_delta) * cosmo.d_plus(0.1) / cosmo.d_plus(1.0);
    fwd.forwardModel_v2(ModelInput<3>(mgr, box, input_delta));
    fwd.getDensityFinal(ModelOutput<3>(mgr, box, output_delta_c));

    BOOST_CHECK_CLOSE(
        output_delta_c[0][0][0].real(), input_delta_c[0][0][0].real(), 0.1);
    BOOST_CHECK_CLOSE(
        output_delta_c[0][0][1].real(), input_delta_c[0][0][1].real(), 0.1);

    array::fill(ag_input_c, 1.0);
    /*    fwd.adjointModel_v2(ModelInputAdjoint<3>(mgr, box, ag_input_c));
    fwd.getAdjointModelOutput(ModelOutputAdjoint<3>(mgr, box, ag_output));
    auto scale = std::real(fwrap(ag_input_c)).sum() * 1.0 /
                 (box.L0 * box.L1 * box.L2) * cosmo.d_plus(1.0) /
                 cosmo.d_plus(0.1);
    BOOST_CHECK_CLOSE(ag_output[0][0][0], scale, 0.1);*/
  }
}

BOOST_AUTO_TEST_CASE(test_chain_model) {
  BoxModel box{0, 0, 0, 100, 100, 100, 32, 32, 32};
  CosmologicalParameters cparams;

  cparams.a0 = 1.0;
  cparams.fnl = 0;
  cparams.h = 0.67;
  cparams.omega_b = 0.05;
  cparams.omega_k = 0.0;
  cparams.omega_m = 0.3;
  cparams.omega_q = 0.7;
  cparams.omega_r = 0.0;
  cparams.w = -1;
  cparams.wprime = 0;

  Cosmology cosmo(cparams);

  auto mgr = std::make_shared<FFTW_Manager<double, 3>>(
      box.N0, box.N1, box.N2, MPI_Communication::instance());
  auto comm = MPI_Communication::instance();

  auto fwd = std::make_shared<HadesLinear>(comm, box, box, 0.1, 1.0);
  auto fwd_log = std::make_shared<HadesLog>(comm, box, 1.0);

  {
    ChainForwardModel chain(comm, box);

    chain.addModel(fwd);
    chain.addModel(fwd_log);

    auto input_delta_p = mgr->allocate_array();
    auto output_delta_p = mgr->allocate_array();
    auto output_delta_c_p = mgr->allocate_complex_array();

    auto &input_delta = input_delta_p.get_array();
    auto &output_delta = output_delta_p.get_array();
    auto &output_delta_c = output_delta_c_p.get_array();

    {
      LibLSS_tests::loadReferenceInput(box.N0, input_delta);
      double ref = fwrap(input_delta).sum() * (box.L0 * box.L1 * box.L2) /
                   (box.N0 * box.N1 * box.N2);

      fwrap(input_delta) =
          fwrap(input_delta) * cosmo.d_plus(0.1) / cosmo.d_plus(1.0);
      chain.forwardModel_v2(ModelInput<3>(mgr, box, input_delta));
      chain.getDensityFinal(ModelOutput<3>(mgr, box, output_delta_c));
    }
  }

  {
    ChainForwardModel chain(comm, box);
    size_t const Nmodes = 1000;
    auto primordial = std::make_shared<ForwardPrimordial>(comm, box, 1.0);

    CosmologicalParameters cosmo_pars;

    cosmo_pars.omega_b = 0.049;
    cosmo_pars.omega_k = 0;
    cosmo_pars.omega_m = 0.315;
    cosmo_pars.omega_q = 0.785;
    cosmo_pars.omega_r = 0;
    cosmo_pars.w = -1;
    cosmo_pars.wprime = 0;
    cosmo_pars.z0 = 0;
    cosmo_pars.sigma8 = 0.8;
    cosmo_pars.h = 0.68;

    primordial->setCosmoParams(cosmo_pars);

    chain.addModel(primordial);
    chain.addModel(fwd_log);

    auto input_delta_p = mgr->allocate_array();
    auto output_delta_p = mgr->allocate_array();
    auto output_delta_c_p = mgr->allocate_complex_array();

    auto &input_delta = input_delta_p.get_array();
    auto &output_delta = output_delta_p.get_array();
    auto &output_delta_c = output_delta_c_p.get_array();

    {
      LibLSS_tests::loadReferenceInput(box.N0, input_delta);
      double ref = fwrap(input_delta).sum() * (box.L0 * box.L1 * box.L2) /
                   (box.N0 * box.N1 * box.N2);

      fwrap(input_delta) =
          fwrap(input_delta) * (1.0 / std::sqrt(box.N0 * box.N1 * box.N2));
      chain.forwardModel_v2(ModelInput<3>(mgr, box, input_delta));
      chain.getDensityFinal(ModelOutput<3>(mgr, box, output_delta));

      BOOST_CHECK_CLOSE(output_delta[0][0][0], -1, 0.1);
      BOOST_CHECK_CLOSE(output_delta[0][4][0], -1, 0.1);
      BOOST_CHECK_CLOSE(output_delta[15][5][22], -0.99879686176352611, 0.1);
    }
  }
}

int main(int argc, char **argv) {
  setupMPI(argc, argv);
  LibLSS::QUIET_CONSOLE_START = true;
  StaticInit::execute();
  LibLSS::Console::instance().setVerboseLevel<LOG_STD>();

  int ret = utf::unit_test_main(&init_unit_test, argc, argv);

  StaticInit::finalize();
  doneMPI();
  return 0;
}
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2019-2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
