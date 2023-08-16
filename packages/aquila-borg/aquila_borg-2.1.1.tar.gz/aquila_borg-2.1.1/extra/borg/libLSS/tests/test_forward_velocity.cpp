/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_forward_velocity.cpp
    Copyright (C) 2019-2020 Florent Leclercq <florent.leclercq@polytechnique.org>
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

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
#include <CosmoTool/cosmopower.hpp>
#include <CosmoTool/algo.hpp>
#include <boost/format.hpp>
#include "libLSS/tools/powerspectrum/measure.hpp"
#include "libLSS/physics/cosmo_power.hpp"
#include "libLSS/tests/setup_hades_test_run.hpp"
#include "libLSS/samplers/hades/hades_linear_likelihood.hpp"
#include "libLSS/physics/velocity/velocity_cic.hpp"

using namespace LibLSS;
using boost::format;
using CosmoTool::square;
using std::string;

static size_t const GridSize = 64;
static size_t const BoxLength = 600.;

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

#include "libLSS/physics/forwards/borg_lpt.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/physics/likelihoods/base.hpp"
#include "libLSS/physics/forward_model.hpp"

namespace L = LibLSS::Likelihood;
using LibLSS::BoxModel;
using LibLSS::HMCDensitySampler;
using LibLSS::LikelihoodInfo;
using LibLSS::MarkovState;

auto makeModel(MarkovState &state, BoxModel const &box, LikelihoodInfo &info) {
  auto comm = L::getMPI(info);
  return std::make_shared<LibLSS::BorgLptModel<>>(
      comm, box, box, false /* norsd
*/
      ,
      2 /* ss factor */, 2.0, 0.001, 1.0, false);
}

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

    randgen->seed(2348098);

    state.newElement(
        "random_generator",
        new RandomStateElement<RandomNumber>(randgen.get()));

    LibLSS_test::setup_hades_test_run(comm, GridSize, BoxLength, state);
    LibLSS_test::setup_box(state, box);
    LibLSS_test::setup_likelihood_info(state, info);

    DummyPowerSpectrum dummy_p(comm);
    auto likelihood = std::make_shared<HadesLinearDensityLikelihood>(info);
    auto model = makeModel(state, box, info);
    HMCDensitySampler hmc(comm, likelihood);
    auto mgr = std::make_unique<FFTW_Manager<double, 3>>(
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
    dummy_p.init_markov(state);
    hmc.init_markov(state);
    model->holdParticles();
    hmc.generateMockData(state);

    ArrayType1d::ArrayType power(
        boost::extents[state.getScalar<long>("NUM_MODES")]);

    fwrap(tmp_real_field) =
        fwrap(*state.get<ArrayType>("BORG_final_density")->array) * dVol;

    mgr->execute_r2c(
        analysis_plan, tmp_real_field.data(), tmp_complex_field.data());

    mgr->destroy_plan(analysis_plan);

    // Declare and allocate velocity forward and adjoint variables
    VelocityModel::CICModel vmodel(model->get_box_model_output(), model);
    LibLSS::U_Array<double, 4> velocityField(
        mgr->extents_real_strict(boost::extents[3]));
    size_t const Np = model->getNumberOfParticles();

    // Get (forward) velocity field
    vmodel.getVelocityField(velocityField.get_array());

    // Compute adjoint gradient
    vmodel.computeAdjointModel_array(velocityField.get_array() /*_ag*/);

    PowerSpectrum::computePower(
        power, tmp_complex_field, *state.get<IArrayType>("k_keys"),
        *state.get<IArrayType>("adjust_mode_multiplier"),
        *state.get<IArrayType1d>("k_nmodes"), std::pow(BoxLength, 3));

    comm->all_reduce_t(
        MPI_IN_PLACE, power.data(), power.num_elements(), MPI_SUM);

    {
      std::shared_ptr<H5::H5File> f;

      if (comm->rank() == 0)
        f = std::make_shared<H5::H5File>("dump.h5", H5F_ACC_TRUNC);

      state.mpiSaveState(f, comm, false);

      if (f)
        CosmoTool::hdf5_write_array(*f, "power", power);
    }
  }
  StaticInit::finalize();
  doneMPI();

  return 0;
}

// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Florent Leclercq
// ARES TAG: year(0) = 2019-2020
// ARES TAG: email(0) = florent.leclercq@polytechnique.org
// ARES TAG: name(1) = Guilhem Lavaux
// ARES TAG: year(1) = 2019-2020
// ARES TAG: email(1) = guilhem.lavaux@iap.fr
