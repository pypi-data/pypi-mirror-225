/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/hmclet/julia_slice.cpp
    Copyright (C) 2014-2020 2018-2019 <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <string>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/julia/julia.hpp"
#include "libLSS/julia/julia_mcmc.hpp"
#include "libLSS/hmclet/julia_slice.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/rgen/slice_sweep.hpp"
#include "libLSS/samplers/julia/julia_likelihood.hpp"
#include "libLSS/julia/julia_ghosts.hpp"
#include "libLSS/julia/julia_array.hpp"
#include "libLSS/hmclet/mass_saver.hpp"

using namespace LibLSS;
using namespace LibLSS::JuliaLikelihood;
using LibLSS::Julia::helpers::_r;

JuliaMetaSlice::JuliaMetaSlice(
    MPI_Communication *comm_, const std::string &likelihood_module_,
    std::shared_ptr<JuliaDensityLikelihood> likelihood_, size_t burnin_, size_t memorySize_)
    : MarkovSampler(), module_name(likelihood_module_), comm(comm_),
      likelihood(likelihood_), burnin(burnin_), memorySize(memorySize_) {}

JuliaMetaSlice::~JuliaMetaSlice() {}

void JuliaMetaSlice::initialize(MarkovState &state) { restore(state); }

void JuliaMetaSlice::restore(MarkovState &state) {
  N0 = state.getScalar<long>("N0");
  N1 = state.getScalar<long>("N1");
  N2 = state.getScalar<long>("N2");
  N2real = state.getScalar<long>("N2real");
  localN0 = state.getScalar<long>("localN0");
  Ncatalog = state.getScalar<long>("NCAT");

  Julia::Object plane_array =
      Julia::invoke(query_planes(module_name), Julia::pack(state));
  auto planes = plane_array.unbox_array<uint64_t, 1>();

  std::vector<size_t> owned_planes(localN0);

  for (size_t i = 0; i < localN0; i++)
    owned_planes[i] = startN0 + i;

  // Create and introduce the covariance matrix in the state.
  // However this matrix is fully owned by JuliaMetaSlice. Only the saver
  // is introduced as a mechanism to automatically save/restore the matrix.
  //
  likelihood->getPendingInit().ready([this, &state]() {
    covariances.clear();
    for (size_t i = 0; i < Ncatalog; i++) {
      auto &bias =
          *state.get<ArrayType1d>(boost::format("galaxy_bias_%d") % i)->array;
      size_t numParams = bias.size();
      auto covar = std::shared_ptr<mass_t>(new mass_t(numParams));
      auto obj = new ObjectStateElement<HMCLet::MassSaver<mass_t>, true>();
      obj->obj = new HMCLet::MassSaver<mass_t>(*covar.get());
      state.newElement(boost::str(boost::format("galaxy_slice_%d") % i), obj, true);
      covariances.push_back(covar);
        
      Julia::Object jl_mass =
        Julia::invoke(module_name + ".fill_dense_mass_matrix", Julia::pack(state));
     auto mass = jl_mass.unbox_array<double, 2>();
     Console::instance().print<LOG_INFO>("Setup IC mass matrix");
     covar->setInitialMass(mass);
     covar->clear();
     covar->setBurninMax(burnin);
     covar->setMemorySize(memorySize);
     covar->setCorrelationLimiter(0.001); // The minimum to avoid blow up
    }
  });

  ghosts.setup(
      comm, planes, owned_planes, std::array<size_t, 2>{N1, N2real}, N0);
}

void JuliaMetaSlice::sample(MarkovState &state) {
  using namespace Eigen;
  ConsoleContext<LOG_VERBOSE> ctx("JuliaMetaSlice::sample");
  Julia::Object jl_density;

  if (state.getScalar<bool>("bias_sampler_blocked"))
    return;

  auto &out_density = *state.get<ArrayType>("BORG_final_density")->array;
  auto jl_state = Julia::pack(state);

  // Now we gather all the required planes on this node and dispatch
  // our data to peers.
  ghosts.synchronize(out_density);

  RandomGen *rgen = state.get<RandomGen>("random_generator");
  auto jl_ghosts = Julia::newGhostManager(&ghosts, N2);

  jl_density.box_array(out_density);

  std::string likelihood_name = likelihood_evaluate_bias(module_name);

  std::string param_priors_name = module_name + ".log_prior_bias";

  auto v_density =
      Julia::view_array<3>(jl_density, {_r(1, localN0), _r(1, N1), _r(1, N2)});

  for (int cat_idx = 0; cat_idx < Ncatalog; cat_idx++) {
    auto &bias = *state.get<ArrayType1d>(galaxy_bias_name(cat_idx))->array;
    size_t Nbiases = bias.size();
    Map<VectorXd> current_bias(bias.data(), Nbiases);
    VectorXd transformed_bias(Nbiases);
    VectorXd new_transformed_bias(Nbiases);
    boost::multi_array_ref<double, 1> new_bias(
        &new_transformed_bias(0), boost::extents[Nbiases]);

    Julia::Object jl_bias;
    jl_bias.box_array(new_bias);

    covariances[cat_idx]->computeMainComponents();

    auto mean = covariances[cat_idx]->getMean();
    auto components = covariances[cat_idx]->components();

    transformed_bias.noalias() = components.adjoint() * (current_bias - mean);

    for (int j = 0; j < Nbiases; j++) {
      ctx.print(boost::format("catalog %d / bias %d") % cat_idx % j);

      auto likelihood = [&, this, j, cat_idx](double x) -> double {
        new_transformed_bias = transformed_bias;
        new_transformed_bias(j) = x;
        new_transformed_bias = components * new_transformed_bias + mean;

        double L = Julia::invoke(
                       likelihood_name, jl_state, jl_ghosts, v_density, cat_idx,
                       jl_bias)
                       .unbox<double>();

        ctx.print("Reduce likelihood");
        comm->all_reduce_t(MPI_IN_PLACE, &L, 1, MPI_SUM);
        ctx.print("Returning L=" + to_string(L));
        L += Julia::invoke(param_priors_name, jl_state, cat_idx, jl_bias)
                 .unbox<double>();

        return -L;
      };

      double step =
          Julia::invoke(module_name + ".get_step_hint", jl_state, cat_idx, j)
              .unbox<double>();

      ctx.print("Advised step is " + to_string(step));
      transformed_bias(j) = slice_sweep(
          comm, rgen->get(), likelihood, transformed_bias(j), step, 0);
    }
    new_transformed_bias = components * transformed_bias + mean;
    current_bias = new_transformed_bias;
    covariances[cat_idx]->addMass(bias);
  }
}
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: name(0) = 2018-2019
