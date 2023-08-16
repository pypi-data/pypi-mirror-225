/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/hmclet/julia_hmclet.cpp
    Copyright (C) 2014-2020 2018-2019 <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <string>
#include <boost/format.hpp>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/julia/julia.hpp"
#include "libLSS/julia/julia_mcmc.hpp"
#include "libLSS/hmclet/julia_hmclet.hpp"
#include "libLSS/hmclet/hmclet_qnhmc.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/rgen/slice_sweep.hpp"
#include "libLSS/samplers/julia/julia_likelihood.hpp"
#include "libLSS/julia/julia_ghosts.hpp"
#include "libLSS/julia/julia_array.hpp"
#include "libLSS/hmclet/diagonal_mass.hpp"
#include "libLSS/hmclet/dense_mass.hpp"
#include "libLSS/hmclet/mass_burnin.hpp"
#include "libLSS/tools/itertools.hpp"
#include "libLSS/hmclet/mass_saver.hpp"

using namespace LibLSS;
using namespace LibLSS::JuliaLikelihood;
using namespace LibLSS::JuliaHmclet::details;
using boost::format;
using LibLSS::Julia::helpers::_r;

static constexpr int ROOT_RANK = 0;

// ----------------------------------------------------------------------------
// JuliaHmcletMeta

JuliaHmcletMeta::JuliaHmcletMeta(
    MPI_Communication *comm_, std::shared_ptr<JuliaDensityLikelihood> likelihood_,
    const std::string &likelihood_module_, MatrixType matrixType,
    size_t burnin_, size_t memorySize_, double limiter_, bool frozen_)
    : MarkovSampler(), comm(comm_), module_name(likelihood_module_),
      likelihood(likelihood_), massMatrixType(matrixType),
      burnin(burnin_), memorySize(memorySize_), limiter(limiter_), frozen(frozen_) {
  ConsoleContext<LOG_INFO> ctx("JuliaHmcletMeta::JuliaHmcletMeta");
}

JuliaHmcletMeta::~JuliaHmcletMeta() {}

void JuliaHmcletMeta::initialize(MarkovState &state) { restore(state); }

static void julia_helper_diagonal_mass_matrix(
    std::string const &module_name,
    std::unique_ptr<AbstractSimpleSampler> &hmc_, Julia::Object &jl_state,
    size_t burnin, size_t memorySize, bool frozen) {
  auto hmc =
      dynamic_cast<SimpleSampler<MassMatrixWithBurnin<DiagonalMassMatrix>> *>(
          hmc_.get());
  Julia::Object jl_mass =
      Julia::invoke(module_name + ".fill_diagonal_mass_matrix", jl_state);
  auto mass = jl_mass.unbox_array<double, 1>();

  auto &hmc_mass = hmc->getMass();
  hmc_mass.setInitialMass(mass);
  hmc_mass.clear();
  hmc_mass.setBurninMax(burnin);
  hmc_mass.setMemorySize(memorySize);
  if (frozen)
    hmc_mass.freeze();
}

static void julia_helper_diagonal_mass_matrix_qn(
    std::string const &module_name,
    std::unique_ptr<AbstractSimpleSampler> &hmc_, Julia::Object &jl_state) {
  Console::instance().print<LOG_DEBUG>("Initializing mass matrix QN");
  auto hmc =
      dynamic_cast<QNHMCLet::Sampler<DiagonalMassMatrix, QNHMCLet::BDense> *>(
          hmc_.get());
  Julia::Object jl_mass =
      Julia::invoke(module_name + ".fill_diagonal_mass_matrix", jl_state);
  auto mass = jl_mass.unbox_array<double, 1>();

  Console::instance().print<LOG_DEBUG>("Got some mass-> " + to_string(mass));

  auto &hmc_mass = hmc->getMass();
  hmc_mass.setInitialMass(mass);
  hmc_mass.clear();
  hmc_mass.freeze();
}

static void julia_helper_dense_mass_matrix(
    std::string const &module_name,
    std::unique_ptr<AbstractSimpleSampler> &hmc_, Julia::Object &jl_state,
    size_t burnin, size_t memorySize, double limiter, bool frozen) {
  auto hmc =
      dynamic_cast<SimpleSampler<MassMatrixWithBurnin<DenseMassMatrix>> *>(
          hmc_.get());
  Julia::Object jl_mass =
      Julia::invoke(module_name + ".fill_dense_mass_matrix", jl_state);
  auto mass = jl_mass.unbox_array<double, 2>();

  auto &hmc_mass = hmc->getMass();
  Console::instance().print<LOG_INFO>("Setup IC mass matrix");
  hmc_mass.setInitialMass(mass);
  hmc_mass.clear();
  hmc_mass.setBurninMax(burnin);
  hmc_mass.setMemorySize(memorySize);
  hmc_mass.setCorrelationLimiter(limiter);
  if (frozen)
    hmc_mass.freeze();
}

std::tuple<samplerBuilder_t, massMatrixInit_t>
JuliaHmcletMeta::getAdequateSampler() {
  ConsoleContext<LOG_VERBOSE> ctx("JuliaHmcletMeta::getAdequateSampler");
  samplerBuilder_t f;
  massMatrixInit_t f2;

  if (massMatrixType == DIAGONAL) {
    ctx.print("Using DIAGONAL mass matrix");
    f = [](std::shared_ptr<JuliaHmcletPosterior> &posterior, MarkovState &state,
           std::string const &name) {
      typedef SimpleSampler<MassMatrixWithBurnin<DiagonalMassMatrix>> sampler_t;
      auto sampler = std::unique_ptr<sampler_t>(new sampler_t(posterior));
      add_saver(state, name, sampler);
      return sampler;
    };
    f2 = std::bind(
        &julia_helper_diagonal_mass_matrix, module_name, std::placeholders::_1,
        std::placeholders::_2, burnin, memorySize, frozen);
  } else if (massMatrixType == QN_DIAGONAL) {
    f = [](std::shared_ptr<JuliaHmcletPosterior> &posterior, MarkovState &state,
           std::string const &name) {
      typedef QNHMCLet::Sampler<DiagonalMassMatrix,QNHMCLet::BDense> sampler_t;
      auto sampler = std::unique_ptr<sampler_t>(new sampler_t(posterior));
      add_saver(state, name, sampler);
      return sampler;
    };
    f2 = std::bind(
        &julia_helper_diagonal_mass_matrix_qn, module_name, std::placeholders::_1,
        std::placeholders::_2);
  } else if (massMatrixType == DENSE) {
    ctx.print("Using DENSE mass matrix");
    f = [](std::shared_ptr<JuliaHmcletPosterior> &posterior, MarkovState &state,
           std::string const &name) {
      typedef SimpleSampler<MassMatrixWithBurnin<DenseMassMatrix>> sampler_t;
      auto sampler = std::unique_ptr<sampler_t>(new sampler_t(posterior));
      add_saver(state, name, sampler);
      return sampler;
    };
    f2 = std::bind(
        &julia_helper_dense_mass_matrix, module_name, std::placeholders::_1,
        std::placeholders::_2, burnin, memorySize, limiter, frozen);
  }
  return std::make_tuple(f, f2);
}

void JuliaHmcletMeta::restore(MarkovState &state) {
  ConsoleContext<LOG_INFO> ctx("JuliaHmcletMeta::restore");

  N0 = state.getScalar<long>("N0");
  N1 = state.getScalar<long>("N1");
  N2 = state.getScalar<long>("N2");
  Ncatalog = state.getScalar<long>("NCAT");

  FFTW_Manager_3d<double> mgr(N0, N1, N2, comm);

  N2real = mgr.N2real;

  localN0 = mgr.localN0;
  long startN0 = mgr.startN0;

  Julia::Object plane_array =
      Julia::invoke(query_planes(module_name), Julia::pack(state));
  auto planes = plane_array.unbox_array<uint64_t, 1>();

  std::vector<size_t> owned_planes(localN0);

  for (size_t i = 0; i < localN0; i++)
    owned_planes[i] = startN0 + i;

  ghosts.setup(comm, planes, owned_planes, std::array<size_t, 2>{N1, N2}, N0);

  ctx.print("Resize posteriors");
  posteriors.resize(Ncatalog);
  hmcs.resize(Ncatalog);

  samplerBuilder_t samplerBuilder;


  state.newScalar<int>("hmclet_badreject", 0, true);

  std::tie(samplerBuilder, massMatrixInit) = getAdequateSampler();

  ctx.print("Register to likelihood post init");
  likelihood->getPendingInit().ready([this, &state, samplerBuilder]() {
    ConsoleContext<LOG_INFO> ctx2("JuliaHmcletMeta::restore::post_init");
    for (size_t c = 0; c < Ncatalog; c++) {
      auto &bias = *state.get<ArrayType1d>(format("galaxy_bias_%d") % c)->array;
      ctx2.print("Make posterior");
      posteriors[c] = std::make_shared<JuliaHmcletPosterior>(
          comm, module_name, c, bias.size());
      ctx2.print("Make hmclet");
      hmcs[c] = samplerBuilder(
          posteriors[c], state, str(format("galaxy_hmclet_%d") % c));
    }
    ready_hmclet.submit_ready();
  });
}

void JuliaHmcletMeta::sample(MarkovState &state) {
  ConsoleContext<LOG_VERBOSE> ctx("JuliaHmcletMeta::sample");

  if (state.getScalar<bool>("bias_sampler_blocked"))
    return;

  Julia::Object jl_density;
  auto &out_density = *state.get<ArrayType>("BORG_final_density")->array;
  auto jl_state = Julia::pack(state);
  long MCMC_STEP = state.getScalar<long>("MCMC_STEP");
  RandomGen *rgen = state.get<RandomGen>("random_generator");

  // Now we gather all the required planes on this node and dispatch
  // our data to peers.
  ghosts.synchronize(out_density);

  Julia::Object jl_ghosts = Julia::newGhostManager(&ghosts, N2);

  jl_density.box_array(out_density);

  Julia::Object v_density =
      Julia::view_array<3>(jl_density, {_r(1, localN0), _r(1, N1), _r(1, N2)});

  if (MCMC_STEP == 0) {
    for (size_t cat_idx = 0; cat_idx < Ncatalog; cat_idx++) {
      VectorType &bias =
          *(state.get<ArrayType1d>(format("galaxy_bias_%d") % cat_idx)->array);

      if (!massMatrixInit) {
        error_helper<ErrorBadState>(
            "No mass matrix initializer provided to JuliaHmclet");
      }

      try {
        massMatrixInit(hmcs[cat_idx], jl_state);
      } catch (Julia::JuliaException const &) {
        ctx.print2<LOG_WARNING>("Mass matrix not provided. Auto-seeding.");
        size_t Nbias = bias.size();
        boost::multi_array<double, 1> initial_step(boost::extents[Nbias]);

        for (size_t j = 0; j < Nbias; j++)
          initial_step[j] =
              Julia::invoke(
                  module_name + ".get_step_hint", jl_state, cat_idx, j)
                  .unbox<double>();

        posteriors[cat_idx]->updateGhosts(jl_ghosts);
        posteriors[cat_idx]->updateState(jl_state, v_density);
        hmcs[cat_idx]->calibrate(comm, rgen->get(), 10, bias, initial_step);
      }
    }
    ctx.print("Done initializing mass matrix");
  }

  for (size_t cat_idx = 0; cat_idx < Ncatalog; cat_idx++) {
    posteriors[cat_idx]->updateGhosts(jl_ghosts);
    posteriors[cat_idx]->updateState(jl_state, v_density);
    try {
      hmcs[cat_idx]->newSample(
        comm, rgen->get(),
        *state.get<ArrayType1d>(format("galaxy_bias_%d") % cat_idx)->array);
    } catch (LibLSS::HMCLet::ErrorBadReject const& e) {
      state.getScalar<int>("hmclet_badreject")++;
      ctx.print2<LOG_ERROR>("Bad reject. Note down and reset the hmc");
      hmcs[cat_idx]->reset();
    }
  }
  // Do not use posteriors beyond this without reupdating all arrays.
}

// ----------------------------------------------------------------------------
// JuliaHmcletPosterior

size_t JuliaHmcletPosterior::getNumberOfParameters() const {
  return numBiasParams;
}

double JuliaHmcletPosterior::evaluate(VectorType const &params) {
  ConsoleContext<LOG_DEBUG> ctx("JuliaHmcletPosterior::evaluate");
  boost::multi_array<double, 1> a = params;
  Julia::Object jl_p;

  jl_p.box_array(a);

  double L =
      Julia::invoke(param_priors_name, *state, cat_id, jl_p).unbox<double>();

  if (L == std::numeric_limits<double>::infinity())
    return std::numeric_limits<double>::infinity();

  L += Julia::invoke(likelihood_name, *state, *ghosts, *density, cat_id, jl_p)
           .unbox<double>();

  ctx.print("Reduce likelihood");
  comm->all_reduce_t(MPI_IN_PLACE, &L, 1, MPI_SUM);
  ctx.print("Returning L=" + to_string(L));
  return L;
}

void JuliaHmcletPosterior::adjointGradient(
    VectorType const &params, VectorType &params_gradient) {
  ConsoleContext<LOG_DEBUG> ctx("JuliaHmcletPosterior::adjointGradient");
  Julia::Object jl_p, jl_gradient;
  boost::multi_array<double, 1> a(boost::extents[numBiasParams]);
  int bad_gradient_count = 0;

  fwrap(a) = params;
  jl_p.box_array(a);
  jl_gradient.box_array(params_gradient);

  comm->broadcast_t(a.data(), numBiasParams, ROOT_RANK);
  try {
    Julia::invoke(
        adjoint_name, *state, *ghosts, *density, cat_id, jl_p, jl_gradient);
  } catch (Julia::JuliaException &e) {
    if (Julia::isBadGradient(e))
      bad_gradient_count = 1;
    else
      throw;
  }
  comm->all_reduce_t(MPI_IN_PLACE, &bad_gradient_count, 1, MPI_SUM);
  if (bad_gradient_count > 0)
    throw HMCLet::ErrorBadGradient("Bad gradient from Julia");

  Console::instance().print<LOG_VERBOSE>("Got a gradient: " + to_string(params_gradient));

  comm->all_reduce_t(
      (double *)MPI_IN_PLACE, params_gradient.data(), numBiasParams, MPI_SUM);
}
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: name(0) = 2018-2019
