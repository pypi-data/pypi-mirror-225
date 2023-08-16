/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_part_swapper.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#define BOOST_TEST_MODULE part_swapper
#define BOOST_TEST_NO_MAIN
#define BOOST_TEST_ALTERNATIVE_INIT_API
#include <boost/test/included/unit_test.hpp>
#include <boost/test/data/test_case.hpp>

#include <iostream>
#include <boost/format.hpp>
#include <boost/multi_array.hpp>

#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_assign.hpp"

#include "libLSS/physics/forwards/particle_balancer/attributes.hpp"
#include "libLSS/physics/forwards/particle_balancer/part_swapper.hpp"
#include "libLSS/physics/forwards/particle_balancer/particle_distribute.hpp"
#include "libLSS/physics/forwards/particle_balancer/dyn/particle_distribute.hpp"
#include "libLSS/physics/forwards/particle_balancer/dyn/scalar.hpp"
#include "libLSS/physics/forwards/particle_balancer/dyn/vector.hpp"
//#include "libLSS/physics/forwards/pm/particle_distribute.hpp"

namespace utf = boost::unit_test;
using boost::extents;
using boost::format;

struct SwapperFixture {
  static LibLSS::MPI_Communication *comm;

  SwapperFixture() {}

  ~SwapperFixture() {}
};

// Setup a naive selector that sends to two MPI task
// depending on whether x[0] < 0.5 or not.
struct NaiveSelector {
  NaiveSelector() {}

  template <typename Position, typename... U>
  int operator()(Position const &pos, U &&...) const {
    if (pos[0] < 0.5)
      return 0;
    else
      return 1;
  }
};

struct ParamSelector {
  double threshold;

  ParamSelector(double threshold) { this->threshold = threshold; }

  template <typename Position, typename... U>
  int operator()(Position const &pos, U &&...) const {
    if (pos[0] < this->threshold)
      return 0;
    else
      return 1;
  }
};

struct AttrSelector {
  AttrSelector() {}

  template <typename Position>
  int operator()(Position const &pos, std::tuple<int> a) const {
    return std::get<0>(a);
  }
};

LibLSS::MPI_Communication *SwapperFixture::comm = 0;

typedef boost::multi_array<double, 1> Array1d;
typedef Array1d::index_range i_range;
Array1d::index_gen indices;

BOOST_GLOBAL_FIXTURE(SwapperFixture);

BOOST_AUTO_TEST_CASE(part_swapper_scalar_element) {
  boost::multi_array<double, 1> p(extents[10]);
  boost::multi_array<double, 1> p2(extents[10]);
  LibLSS::Particles::ScalarAttribute<decltype(p2) &> swapper(p2);

  for (int i = 0; i < 10; i++) {
    p[i] = 10 - i;
    p2[i] = i;
  }

  auto tmpattrs = swapper.allocateTemporary(8);
}

BOOST_AUTO_TEST_CASE(part_swapper_vector_element) {
  boost::multi_array<double, 1> p(extents[10]);
  boost::multi_array<double, 2> p2(extents[10][3]);
  LibLSS::Particles::VectorAttribute<decltype(p2) &> swapper(p2);

  for (int i = 0; i < 10; i++) {
    p[i] = 10 - i;
    p2[i][0] = 3 * i;
    p2[i][1] = 3 * i + 1;
    p2[i][2] = 3 * i + 2;
  }

  auto tmpattrs = swapper.allocateTemporary(8);
}

struct PositionFixture {
  boost::multi_array<double, 2> in_pos;
  ssize_t last_index;

  PositionFixture() : in_pos(extents[20][3]) {
    if (SwapperFixture::comm->rank() == 0) {
      for (int i = 0; i < 10; i++) {
        in_pos[i][0] = i / 10.;
        in_pos[i][1] = 0;
        in_pos[i][2] = 0;
      }
      last_index = 10;
    } else {
      last_index = 0;
    }
  }

  void check(LibLSS::BalanceInfo const &info) {
    int rank = SwapperFixture::comm->rank();

    BOOST_CHECK_EQUAL(info.localNumParticlesAfter, 5);

    for (int i = 0; i < 5; i++) {
      int j = (rank == 0) ? i : (i + 5);
      BOOST_CHECK_CLOSE(in_pos[i][0], j / 10., 1e-6);
      BOOST_CHECK_CLOSE(in_pos[i][1], 0., 1e-6);
      BOOST_CHECK_CLOSE(in_pos[i][2], 0., 1e-6);
    }
  }
};

BOOST_AUTO_TEST_CASE(part_swapper_no_attributes) {
  LibLSS::BalanceInfo info;
  NaiveSelector selector;
  PositionFixture pos;

  // 10 particles
  info.allocate(SwapperFixture::comm, 20);

  info.localNumParticlesBefore = pos.last_index;
  LibLSS::particle_redistribute(info, pos.in_pos, selector);

  pos.check(info);
}

BOOST_AUTO_TEST_CASE(part_swapper_no_attributes_parameter) {
  LibLSS::BalanceInfo info;
  double threshold = 0.5;
  ParamSelector selector(threshold);
  PositionFixture pos;

  // 10 particles
  info.allocate(SwapperFixture::comm, 20);

  info.localNumParticlesBefore = pos.last_index;
  LibLSS::particle_redistribute(info, pos.in_pos, selector);

  pos.check(info);
}

BOOST_AUTO_TEST_CASE(part_swapper_no_attributes_parameter_dyn) {
  LibLSS::BalanceInfo info;
  double threshold = 0.5;
  ParamSelector selector(threshold);
  PositionFixture pos;

  // 10 particles
  info.allocate(SwapperFixture::comm, 20);

  info.localNumParticlesBefore = pos.last_index;

  boost::multi_array<int, 1> scalar(boost::extents[20]);
  boost::multi_array<int, 2> vec(boost::extents[20][2]);

  for (int i = 0; i < info.localNumParticlesBefore; i++) {
    scalar[i] = pos.in_pos[i][0] < threshold;
    vec[i][0] = pos.in_pos[i][0] < threshold;
    vec[i][1] = SwapperFixture::comm->rank();
  }

  LibLSS::particle_redistribute(info, pos.in_pos, selector);

  LibLSS::dynamic_particle_redistribute(
      SwapperFixture::comm, info,
      {LibLSS::AbstractParticles::scalar(scalar),
       LibLSS::AbstractParticles::vector(vec)});

  pos.check(info);

  for (int i = 0; i < info.localNumParticlesAfter; i++) {
    if (SwapperFixture::comm->rank() == 0) {
      BOOST_CHECK_EQUAL(scalar[i], 1);
      BOOST_CHECK_EQUAL(vec[i][0], 1);
    } else {
      BOOST_CHECK_EQUAL(scalar[i], 0);
      BOOST_CHECK_EQUAL(vec[i][0], 0);
    }
    BOOST_CHECK_EQUAL(vec[i][1], 0);
  }
}

BOOST_AUTO_TEST_CASE(part_swapper_attr_selection) {
  LibLSS::BalanceInfo info;
  AttrSelector selector;
  PositionFixture pos;

  // 10 particles
  info.allocate(SwapperFixture::comm, 20);
  boost::multi_array<int, 1> core(boost::extents[20]);

  for (int i = 0; i < 10; i++)
    core[i] = 1;

  info.localNumParticlesBefore = pos.last_index;
  LibLSS::particle_redistribute(
      info, pos.in_pos, selector,
      LibLSS::make_attribute_helper(LibLSS::Particles::scalar(core)));
}

struct VelocityFixture {
  boost::multi_array<double, 2> in_vel;
  double this_shift;

  VelocityFixture(double shift = 0) : in_vel(extents[20][3]), this_shift(0) {
    if (SwapperFixture::comm->rank() == 0) {
      for (int i = 0; i < 10; i++) {
        in_vel[i][0] = i + this_shift;
        in_vel[i][1] = 2 * i + this_shift;
        in_vel[i][2] = 3 * i + this_shift;
      }
    }
  }

  void check(LibLSS::BalanceInfo &info) {
    int rank = SwapperFixture::comm->rank();

    for (int i = 0; i < 5; i++) {
      int j = (rank == 0) ? i : (i + 5);
      BOOST_CHECK_CLOSE(in_vel[i][0], j + this_shift, 1e-6);
      BOOST_CHECK_CLOSE(in_vel[i][1], 2 * j + this_shift, 1e-6);
      BOOST_CHECK_CLOSE(in_vel[i][2], 3 * j + this_shift, 1e-6);
    }
  }
};

BOOST_AUTO_TEST_CASE(part_swapper_vel_attributes) {
  LibLSS::BalanceInfo info;
  NaiveSelector selector;
  PositionFixture pos;
  VelocityFixture vel;

  // 10 particles
  info.allocate(SwapperFixture::comm, 20);

  info.localNumParticlesBefore = pos.last_index;
  LibLSS::particle_redistribute(
      info, pos.in_pos, selector,
      LibLSS::make_attribute_helper(LibLSS::Particles::vector(vel.in_vel)));

  pos.check(info);
  vel.check(info);
}

BOOST_AUTO_TEST_CASE(part_swapper_vel2_attributes) {
  LibLSS::BalanceInfo info;
  NaiveSelector selector;
  PositionFixture pos;
  VelocityFixture vel(0), vel2(1);

  // 10 particles
  info.allocate(SwapperFixture::comm, 20);

  info.localNumParticlesBefore = pos.last_index;
  LibLSS::particle_redistribute(
      info, pos.in_pos, selector,
      LibLSS::make_attribute_helper(
          LibLSS::Particles::vector(vel.in_vel),
          LibLSS::Particles::vector(vel2.in_vel)));

  pos.check(info);
  vel.check(info);
  vel2.check(info);
}

struct OtherFixture {
  boost::multi_array<double, 1> in_scalar;
  OtherFixture() : in_scalar(boost::extents[20]) {
    if (SwapperFixture::comm->rank() == 0) {
      for (int i = 0; i < 10; i++) {
        in_scalar[i] = std::exp(i / 10.);
      }
    }
  }

  void check(LibLSS::BalanceInfo &info) {
    int rank = SwapperFixture::comm->rank();

    for (int i = 0; i < 5; i++) {
      int j = (rank == 0) ? i : (i + 5);
      BOOST_CHECK_CLOSE(in_scalar[i], std::exp(j / 10.), 1e-6);
    }
  }
};

BOOST_AUTO_TEST_CASE(part_swapper_multi_attributes) {
  LibLSS::BalanceInfo info;
  NaiveSelector selector;
  PositionFixture pos;
  VelocityFixture vel(0), vel2(1);
  OtherFixture other;

  // 10 particles
  info.allocate(SwapperFixture::comm, 20);

  info.localNumParticlesBefore = pos.last_index;
  LibLSS::particle_redistribute(
      info, pos.in_pos, selector,
      LibLSS::make_attribute_helper(
          LibLSS::Particles::vector(vel.in_vel),
          LibLSS::Particles::scalar(other.in_scalar),
          LibLSS::Particles::vector(vel2.in_vel)));

  pos.check(info);
  vel.check(info);
  vel2.check(info);
}

int main(int argc, char *argv[]) {
  using namespace LibLSS;

  QUIET_CONSOLE_START = true;
  SwapperFixture::comm = setupMPI(argc, argv);
  StaticInit::execute();
  auto &cons = Console::instance();
  //  cons.setVerboseLevel<LOG_ERROR>();
  cons.setVerboseLevel<LOG_DEBUG>();
  if (SwapperFixture::comm->size() != 2) {
    cons.print<LOG_ERROR>("This test needs a communicator with two tasks.");
    SwapperFixture::comm->abort();
  }
  cons.outputToFile(
      str(format("partswapper.log_%d") % SwapperFixture::comm->rank()));
  int ret = utf::unit_test_main(&init_unit_test, argc, argv);
  StaticInit::finalize();
  doneMPI();
  return ret;
}
