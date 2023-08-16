/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_julia_core.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#define BOOST_TEST_MODULE julia_bind
#define BOOST_TEST_NO_MAIN
#define BOOST_TEST_ALTERNATIVE_INIT_API
#include <boost/test/included/unit_test.hpp>
#include <boost/test/data/test_case.hpp>

#include "libLSS/julia/julia.hpp"
#include "libLSS/julia/julia_mcmc.hpp"
#include "libLSS/julia/julia_array.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/mcmc/state_element.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/console.hpp"
#include "src/common/preparation_types.hpp"

namespace utf = boost::unit_test;

using namespace LibLSS;
using namespace LibLSS_prepare;

struct JuliaFixture {
  static LibLSS::MPI_Communication *comm;
};

MPI_Communication *JuliaFixture::comm = 0;

BOOST_GLOBAL_FIXTURE(JuliaFixture);

BOOST_AUTO_TEST_CASE(julia_print) {
  Julia::evaluate("libLSS.print(libLSS.LOG_STD, repr(sqrt(2.0)))");

  Julia::evaluate(
      "function test_ares(x)\n"
      "  libLSS.print(libLSS.LOG_STD,\"from julia $x -> \" * repr(x / 2))\n"
      "  libLSS.print(libLSS.LOG_STD,\"from julia $x -> \" * repr(x *100))\n"
      "end");

  Julia::invoke("test_ares", 4.0);
}

BOOST_AUTO_TEST_CASE(julia_likelihood) {
  Julia::evaluate("module TestLikelihood\n"
                  "  using ...libLSS\n"
                  "  function squareop(x)\n"
                  "    x.^2\n"
                  "  end\n"
                  "  function likelihood(x)\n"
                  "   sum(x.^2)\n"
                  "  end\n"
                  "  function fillup(x)\n"
                  "    x[:].=10.0\n"
                  "  end\n"
                  "end\n");

  Console::instance().print<LOG_STD>("Compiled test likelihood");

  Julia::Object ret = Julia::evaluate("TestLikelihood.squareop([0,1,2,3,4,5])");

  Console::instance().print<LOG_STD>("Got a square. Unbox it");
  auto a = ret.unbox_array<int64_t, 1>();

  for (size_t i = 0; i < 6; i++)
    BOOST_CHECK_EQUAL(a[i], i * i);

  Console::instance().print<LOG_STD>("Checked square");

  int64_t sumret =
      Julia::evaluate("TestLikelihood.likelihood([0,1,2,3])").unbox<int64_t>();

  Console::instance().print<LOG_STD>("Sum done.");

  BOOST_CHECK_EQUAL(sumret, 14);

  boost::multi_array<double, 1> b(boost::extents[5]);
  Julia::Object a_obj;
  Console::instance().print<LOG_STD>("Boxing array.");
  a_obj.box_array(b);
  Console::instance().print<LOG_STD>("fillup in julia");
  Julia::manual_invoke("TestLikelihood.fillup", {a_obj});
  for (size_t i = 0; i < 5; i++)
    BOOST_CHECK_CLOSE(b[i], 10.0, 1e-6);
  Console::instance().print<LOG_STD>("good. tearing down.");
}

BOOST_AUTO_TEST_CASE(julia_mcmc) {
  MarkovState state;

  Julia::Object j_state = Julia::pack(state);

  Julia::evaluate(
    "function new_array_test(state::libLSS.State)\n"
    "  libLSS.print(libLSS.LOG_STD,\"Hello\")\n"
    "  a = libLSS.new_array(state, \"test_mcmc\", 10, Cint)\n"
    "  a[:] = range(0,length=10)\n"
    "  b = libLSS.new_array(state, \"test_mcmc_2\", 10, Cdouble)\n"
    "  b[:] = range(0,length=10)/10.\n"
    "  libLSS.new(state, \"test_int_2\", Int32(10))\n"
    "  libLSS.print(libLSS.LOG_STD, string(libLSS.get(state, \"test_int_2\", Int32)))\n"
    "  c = libLSS.get_array(state, \"test_mcmc_2\", Cdouble, libLSS.d1d)\n"
    "  libLSS.autosize_array(state, \"test_mcmc_2\", true, Cdouble, libLSS.d1d)\n"
    "end\n");

  Julia::invoke("new_array_test", j_state);

  bool exc_thrown = false;
  std::shared_ptr<ArrayStateElement<int,1>::ArrayType> a_ptr;
  std::shared_ptr<ArrayStateElement<double,1>::ArrayType> b_ptr;
  long c;
  try {
    a_ptr = state.get<ArrayStateElement<int,1>>("test_mcmc")->array;
    b_ptr = state.get<ArrayStateElement<double,1>>("test_mcmc_2")->array;
    c = state.getScalar<int>("test_int_2");
  } catch(ErrorBase const&) {
    exc_thrown = true;
  }
  auto &a = *a_ptr;
  auto &b = *b_ptr;

  BOOST_REQUIRE(!exc_thrown);
  BOOST_CHECK_EQUAL(a.size(), 10);
  BOOST_CHECK_EQUAL(b.size(), 10);
  BOOST_CHECK_EQUAL(c, 10);

  for (size_t i = 0; i < 10; i++) {
    BOOST_CHECK_EQUAL(a[i], i);
    BOOST_CHECK_CLOSE(b[i], i / 10., 1e-6);
  }

  Julia::evaluate("function test_exception(state::libLSS.State)\n"
                  "   libLSS.get_array_1d(state, \"test_mcmc\", Float64)\n"
                  "end\n");

  BOOST_TEST_INFO("Testing expected thrown exception.");
  try {
    Julia::invoke("test_exception", j_state);
    BOOST_ERROR("Exception not thrown");
  } catch (Julia::JuliaException &e) {
    BOOST_CHECK_EQUAL(
        std::string(e.what()),
        "ErrorException: Bad cast in access to test_mcmc");
  }
}

BOOST_AUTO_TEST_CASE(test_array) {
  using Julia::helpers::_r;

  Julia::Object a = Julia::evaluate("a = reshape([0,1,2,3,4,5],2,3)");
  Julia::Object b = Julia::view_array<2>(a, {_r(1, 2), _r(2, 3)});

  Julia::global("b", b);

  BOOST_CHECK_EQUAL(
      Julia::evaluate("a[1,2]").unbox<uint64_t>(),
      Julia::evaluate("b[1,1]").unbox<uint64_t>());
}

BOOST_AUTO_TEST_CASE(test_galaxies) {
  MarkovState state;

  Julia::Object j_state = Julia::pack(state);
  GalaxyElement *g_elt = new GalaxyElement();
  GalaxySurveyType::GalaxyType g;
  g_elt->obj = new GalaxySurveyType();

  g.id = 0;
  g.phi = 0.5;
  g.theta = 0.5;
  g.m = -1;
  g.M_abs = -1;
  auto &survey = g_elt->get();
  survey.addGalaxy(g);
  g.id = 1;
  survey.addGalaxy(g);
  g.id = 2;
  survey.addGalaxy(g);
  survey.optimize();

  state.newElement("galaxy_catalog_0", g_elt);

  Julia::evaluate("function test_galaxy_survey_type(state::libLSS.State)\n"
                  "  g = libLSS.get_galaxy_descriptor(state, 0)\n"
                  "  [Cint(e.id) for e in g]\n"
                  "end\n");

  Julia::Object ret = Julia::invoke("test_galaxy_survey_type", j_state);

  auto ids = ret.unbox_array<int, 1>();
  BOOST_CHECK_EQUAL(ids.size(), 3);
  BOOST_CHECK_EQUAL(ids[0], 0);
  BOOST_CHECK_EQUAL(ids[1], 1);
  BOOST_CHECK_EQUAL(ids[2], 2);
}

int main(int argc, char *argv[]) {
  LibLSS::QUIET_CONSOLE_START = false; //true;
  JuliaFixture::comm = setupMPI(argc, argv);
  StaticInit::execute();

  int ret = utf::unit_test_main(&init_unit_test, argc, argv);

  StaticInit::finalize();
  doneMPI();
  return ret;
}
