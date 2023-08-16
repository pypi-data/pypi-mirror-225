/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/generic_borg_fwd_test.cpp
    Copyright (C) 2014-2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2018 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/tools/static_init.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/samplers/rgen/gsl_random_number.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/physics/cosmo_power.hpp"
#include <CosmoTool/cosmopower.hpp>
#include <CosmoTool/algo.hpp>
#include <boost/format.hpp>
#include "libLSS/tools/powerspectrum/measure.hpp"
#include "libLSS/physics/cosmo_power.hpp"
#include "libLSS/tests/setup_hades_test_run.hpp"
#include "libLSS/samplers/hades/hades_linear_likelihood.hpp"
#include "libLSS/physics/forwards/pm/plane_xchg.hpp"

using namespace LibLSS;
using boost::format;
using CosmoTool::square;
using std::string;

typedef boost::multi_array<double, 3> DensityType;
typedef UninitializedArray<DensityType> U_DensityType;

typedef boost::multi_array<double, 4> VFieldType;
typedef UninitializedArray<VFieldType> U_VFieldType;

static const bool CIC_WEIGHING = true;

#include "src/cic_output.hpp"

static size_t const GridSize = 128;
static size_t const BoxLength = 1000.;

typedef boost::multi_array_types::extent_range range;

typedef RandomNumberMPI<GSL_RandomNumber> RGenType;

namespace {
#if defined(ARES_MPI_FFTW)
  RegisterStaticInit reg0(fftw_mpi_init, fftw_mpi_cleanup, 9, "MPI/FFTW");
#endif
  RegisterStaticInit reg1(
      CosmoTool::init_fftw_wisdom, CosmoTool::save_fftw_wisdom, 10,
      "FFTW/WISDOM");
}; // namespace

class DummyPowerSpectrum : public PowerSpectrumSampler_Base {
public:
  DummyPowerSpectrum(MPI_Communication *comm)
      : PowerSpectrumSampler_Base(comm) {}

  virtual void initialize(MarkovState &state) { initialize_base(state); }
  virtual void restore(MarkovState &state) { restore_base(state); }

  virtual void sample(MarkovState &state) {}
};

int main(int argc, char **argv) {
  MPI_Communication *comm = setupMPI(argc, argv);
  StaticInit::execute();
#if !defined(ARES_MPI_FFTW) && defined(_OPENMP)
  fftw_plan_with_nthreads(smp_get_max_threads());
#endif

  Console &cons = Console::instance();
  cons.setVerboseLevel<LOG_DEBUG>();
  cons.outputToFile(boost::str(format("fwd_test_rank_%d.txt") % comm->rank()));
  {
    MarkovState state;
    auto randgen = std::make_unique<RGenType>(comm, -1);
    BoxModel box;
    LikelihoodInfo info;

    randgen->seed(23480986);

    state.newElement(
        "random_generator",
        new RandomStateElement<RandomNumber>(randgen.get()));

    LibLSS_test::setup_hades_test_run(comm, GridSize, BoxLength, state);
    LibLSS_test::setup_box(state, box);
    LibLSS_test::setup_likelihood_info(state, info);

    auto likelihood = std::make_shared<HadesLinearDensityLikelihood>(info);
    auto model = makeModel(state, box, info);
    model->setAdjointRequired(false);
    HMCDensitySampler hmc(comm, likelihood);
    auto mgr = std::make_shared<FFTW_Manager<double, 3>>(
        GridSize, GridSize, GridSize, comm);
    auto tmp_complex_field_p = mgr->allocate_complex_array();
    auto &tmp_complex_field = tmp_complex_field_p.get_array();
    auto tmp_real_field_p = mgr->allocate_array();
    auto &tmp_real_field = tmp_real_field_p.get_array();
    auto analysis_plan =
        mgr->create_r2c_plan(tmp_real_field.data(), tmp_complex_field.data());
    double dVol = std::pow(BoxLength, 3) / std::pow(GridSize, 3);

    BorgModelElement *model_element = new BorgModelElement();
    model_element->obj = model;
    state.newElement("BORG_model", model_element);

    // Initialize (data,s)->t sampler

    hmc.init_markov(state);
    model->holdParticles();
    hmc.generateMockData(state);

    ArrayType1d::ArrayType power(
        boost::extents[state.getScalar<long>("NUM_MODES")]);
    ArrayType1d::ArrayType power_v(
        boost::extents[state.getScalar<long>("NUM_MODES")]);

    fwrap(tmp_real_field) =
        fwrap(*state.get<ArrayType>("BORG_final_density")->array) * dVol;

    mgr->execute_r2c(
        analysis_plan, tmp_real_field.data(), tmp_complex_field.data());

    U_VFieldType vfield(boost::extents[3][box.N0][box.N1][box.N2]);

    mgr->destroy_plan(analysis_plan);

    PowerSpectrum::computePower(
        power, tmp_complex_field, *state.get<IArrayType>("k_keys"),
        *state.get<IArrayType>("adjust_mode_multiplier"),
        *state.get<IArrayType1d>("k_nmodes"), std::pow(BoxLength, 3));

    comm->all_reduce_t(
        MPI_IN_PLACE, power.data(), power.num_elements(), MPI_SUM);

    double vmultiplier = 1.0;

    if (auto pfwd = dynamic_cast<ParticleBasedForwardModel *>(model.get())) {
      build_velocity_field(pfwd, box, vfield.get_array());
      vmultiplier = pfwd->getVelocityMultiplier();
    }

    {
      auto single = comm->split(comm->rank() == 0);
      auto &k_keys = *state.get<IArrayType>("k_keys")->array;
      auto &k_nmodes = *state.get<IArrayType1d>("k_nmodes")->array;

      //rebuild_density(mgr, k_keys, *state.get<IArrayType>("k_keys")->array);
      //rebuild_density(
      //    mgr, adjuster,
      //    *state.get<IArrayType>("adjust_mode_multiplier")->array);

      if (comm->rank() == 0) {
        auto mgr_single = std::make_unique<FFTW_Manager<double, 3>>(
            GridSize, GridSize, GridSize, single);
        auto single_tmp_real_field = mgr_single->allocate_array();
        auto single_tmp_complex_field = mgr_single->allocate_complex_array();

        auto single_plan = mgr_single->create_r2c_plan(
            single_tmp_real_field.get_array().data(),
            single_tmp_complex_field.get_array().data());

        fwrap(power_v) = 0;
        for (int ax = 0; ax < 3; ax++) {
          fwrap(single_tmp_real_field.get_array()) =
              fwrap(vfield.get_array()[ax]) * vmultiplier;
          mgr_single->execute_r2c(
              single_plan, single_tmp_real_field.get_array().data(),
              single_tmp_complex_field.get_array().data());

          auto shat = fwrap(single_tmp_complex_field.get_array());
          auto vP = ipow<2>(std::real(shat)) + ipow<2>(std::imag(shat));

          for (size_t i = 0; i < box.N0; i++)
            for (size_t j = 0; j < box.N1; j++)
              for (size_t k = 0; k <= box.N2 / 2; k++)
                power_v[k_keys[i][j][k]] += (*vP)[i][j][k];
        }

        fwrap(power_v) =
            fwrap(power_v) / std::pow(BoxLength, 3) / fwrap(k_nmodes);

        mgr_single->destroy_plan(single_plan);
      }
      delete single;
    }

    {
      std::shared_ptr<H5::H5File> f;

      if (comm->rank() == 0)
        f = std::make_shared<H5::H5File>("dump.h5", H5F_ACC_TRUNC);

      state.mpiSaveState(f, comm, false);

      if (f) {
        CosmoTool::hdf5_write_array(*f, "power", power);
        CosmoTool::hdf5_write_array(*f, "power_v", power_v);
      }
      //auto pos = model->getParticlePositions();
      //boost::multi_array<double, 2> out_pos(
      //    boost::extents[pos.shape()[0]][3]);
      //fwrap(out_pos) = pos;
      //CosmoTool::hdf5_write_array(f, "pos", out_pos);
      //fwrap(out_pos) = model->getParticleVelocities();
      //CosmoTool::hdf5_write_array(f, "vel", out_pos);
    }
  }
  StaticInit::finalize();
  doneMPI();

  return 0;
}
// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2014-2018
// ARES TAG: name(1) = Jens Jasche
// ARES TAG: email(1) = jens.jasche@fysik.su.se
// ARES TAG: year(1) = 2009-2018
