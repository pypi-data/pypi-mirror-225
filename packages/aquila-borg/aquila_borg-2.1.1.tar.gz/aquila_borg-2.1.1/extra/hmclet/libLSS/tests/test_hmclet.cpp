/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/tests/test_hmclet.cpp
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

#include "libLSS/tools/console.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"
#include "libLSS/mpi/generic_mpi.hpp"
#include <CosmoTool/algo.hpp>
#include <memory>
#include <H5Cpp.h>
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/hmclet/hmclet.hpp"
#include "libLSS/hmclet/hmclet_qnhmc.hpp"
#include "libLSS/hmclet/diagonal_mass.hpp"

namespace utf = boost::unit_test;

using CosmoTool::square;
using namespace LibLSS;
using namespace LibLSS::HMCLet;

static const double C[2][2] = { { 9. , 1.}, {1., 4.}};
static const double inv_C[2][2] = { { 0.11428571428571427 , -0.028571428571428574}, {-0.028571428571428574, 0.2571428571428572}};


class TestPosterior : virtual public JointPosterior {
public:
  TestPosterior() : JointPosterior() {}
  virtual ~TestPosterior() {}

  virtual size_t getNumberOfParameters() const { return 2; }

  virtual double evaluate(VectorType const &params) {
    double const u0 = params[0] - 1;
    double const u1 = params[1] - 4;

    return 0.5 * (u0*u0 * inv_C[0][0] + 2*u0*u1*inv_C[1][0] + u1*u1*inv_C[1][1]);
  }

  virtual void
  adjointGradient(VectorType const &params, VectorType &params_gradient) {
    double const u0 = params[0] - 1;
    double const u1 = params[1] - 4;

    params_gradient[0] = u0 * inv_C[0][0] + 2*u1 * inv_C[0][1];
    params_gradient[1] = u1 * inv_C[1][1] + 2*u0* inv_C[0][1];
  }
};

BOOST_AUTO_TEST_CASE(hmclet_launch) {
  auto posterior_ptr = std::make_shared<TestPosterior>();
  SimpleSampler<DiagonalMassMatrix> sampler(posterior_ptr);

  MPI_Communication *comm = MPI_Communication::instance();
  RandomNumberMPI<GSL_RandomNumber> rgen(comm, -1);

  boost::multi_array<double, 1> init_params(boost::extents[2]);
  boost::multi_array<double, 1> init_step(boost::extents[2]);

  init_params[0] = 100;
  init_params[1] = 100;
  init_step[0] = 1;
  init_step[1] = 1;

  boost::multi_array<double, 1> initMass(boost::extents[2]);

  initMass[0] = 1;
  initMass[1] = 1;

  sampler.getMass().setInitialMass(initMass);
  sampler.getMass().freeze();

//  sampler.calibrate(comm, rgen, 2, init_params, init_step);

  boost::multi_array<double, 2> p(boost::extents[10000][2]);
  for (size_t i = 0; i < p.size(); i++) {
    sampler.newSample(comm, rgen, init_params);
    p[i][0] = init_params[0];
    p[i][1] = init_params[1];
  }

  H5::H5File ff("test_sample.h5", H5F_ACC_TRUNC);
  CosmoTool::hdf5_write_array(ff, "hmclet", p);
}


BOOST_AUTO_TEST_CASE(qnhmclet_launch) {
  auto posterior_ptr = std::make_shared<TestPosterior>();
  QNHMCLet::Sampler<DiagonalMassMatrix,QNHMCLet::BDense> sampler(posterior_ptr);

  MPI_Communication *comm = MPI_Communication::instance();
  RandomNumberMPI<GSL_RandomNumber> rgen(comm, -1);

  boost::multi_array<double, 1> init_params(boost::extents[2]);
  boost::multi_array<double, 1> init_step(boost::extents[2]);

  boost::multi_array<double, 1> initMass(boost::extents[2]);

  initMass[0] = 1;
  initMass[1] = 1;

  sampler.getMass().setInitialMass(initMass);
  sampler.getMass().freeze();

  init_params[0] = 100;
  init_params[1] = 100;
  init_step[0] = 1;
  init_step[1] = 1;

  boost::multi_array<double, 2> p(boost::extents[10000][2]);
  H5::H5File ff("test_sample_qn.h5", H5F_ACC_TRUNC);
  for (size_t i = 0; i < p.size(); i++) {
    sampler.newSample(comm, rgen, init_params);
    p[i][0] = init_params[0];
    p[i][1] = init_params[1];
//    auto gg = ff.createGroup(boost::str(boost::format("B_%d") % i));
//    sampler.getB().save(gg);
  }

  CosmoTool::hdf5_write_array(ff, "qn_hmclet", p);
}


int main(int argc, char *argv[]) {
  setupMPI(argc, argv);
  StaticInit::execute();

  int ret = utf::unit_test_main(&init_unit_test, argc, argv);

  StaticInit::finalize();
  doneMPI();
  return ret;
}
