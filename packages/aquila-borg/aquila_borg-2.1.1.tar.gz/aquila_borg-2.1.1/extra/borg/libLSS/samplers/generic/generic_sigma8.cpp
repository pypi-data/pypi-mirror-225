/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/generic/generic_sigma8.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <CosmoTool/hdf5_array.hpp>
#include <CosmoTool/algo.hpp>
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/physics/cosmo_power.hpp"
#include "libLSS/samplers/generic/generic_sigma8.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/samplers/rgen/slice_sweep.hpp"

using CosmoTool::square;
using namespace LibLSS;

GenericSigma8Sampler::~GenericSigma8Sampler() {}

void GenericSigma8Sampler::initialize(MarkovState &state) {
  N0 = state.getScalar<long>("N0");
  N1 = state.getScalar<long>("N1");
  N2 = state.getScalar<long>("N2");

  L0 = state.getScalar<double>("L0");
  L1 = state.getScalar<double>("L1");
  L2 = state.getScalar<double>("L2");

  Volume = L0 * L1 * L2;
}

void GenericSigma8Sampler::restore(MarkovState &state) { initialize(state); }

void GenericSigma8Sampler::sample(MarkovState &state) {
  using boost::format;
  ConsoleContext<LOG_VERBOSE> ctx("sampling of sigma8 (naive)");
  auto &rgen = state.get<RandomGen>("random_generator")->get();
  CosmologicalParameters &cosmo_params =
      state.getScalar<CosmologicalParameters>("cosmology");
  CArrayType::ArrayType &s_array = *state.get<CArrayType>("s_hat_field")->array;
  size_t startN0 = s_array.index_bases()[0], localN0 = s_array.shape()[0];
  size_t N2_HC = s_array.shape()[2];

  IArrayType::ArrayType &keys = *state.get<IArrayType>("k_keys")->array;
  ArrayType1d::ArrayType &Pk = *state.get<ArrayType1d>("powerspectrum")->array;

  const ssize_t alpha = 1;

  double loc_N2 = 0;
  double loc_z2 = 0;
  for (size_t i = 0; i < 2 * alpha - 2; i++)
    loc_z2 += square(rgen.gaussian());

  for (size_t i = startN0; i < startN0 + localN0; i++) {
    for (size_t j = 0; j < N1; j++) {
      for (size_t k = 0; k < N2_HC; k++) {
        auto x = s_array[i][j][k];
        auto this_key = keys[i][j][k];

        if (Pk[this_key] == 0)
          continue;

        loc_N2 += (x.real() * x.real() + x.imag() * x.imag()) / (Pk[this_key]);
        loc_z2 += square(rgen.gaussian());
      }
    }
  }

  loc_N2 /= Volume;

  double N2, z2;

  comm->all_reduce_t(&loc_N2, &N2, 1, MPI_SUM);
  comm->all_reduce_t(&loc_z2, &z2, 1, MPI_SUM);

  double scale = N2 / z2;

  cosmo_params.sigma8 *= sqrt(scale);
  ctx.print(
      format("Got sigma8=%g (rescale %g)") % cosmo_params.sigma8 % sqrt(scale));

  createCosmologicalPowerSpectrum(state, cosmo_params);
}
