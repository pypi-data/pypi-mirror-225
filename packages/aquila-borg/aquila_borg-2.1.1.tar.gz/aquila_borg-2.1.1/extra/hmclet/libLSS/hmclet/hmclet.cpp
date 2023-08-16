/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/hmclet/hmclet.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <boost/format.hpp>
#include <functional>
#include <cmath>
#include "libLSS/tools/console.hpp"
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/tools/symplectic_integrator.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/samplers/rgen/slice_sweep.hpp"
#include "libLSS/hmclet/hmclet.hpp"
#include "libLSS/tools/string_tools.hpp"
#include "libLSS/tools/itertools.hpp"

using namespace LibLSS;
using namespace LibLSS::HMCLet;
namespace ph = std::placeholders;
using boost::format;

constexpr static int ROOT_RANK = 0;

template <typename MassType>
SimpleSampler<MassType>::SimpleSampler(
    std::shared_ptr<JointPosterior> _posterior)
    : numParams(_posterior->getNumberOfParameters()), massMatrix(numParams),
      posterior(_posterior), momentum(boost::extents[numParams]) {
  ConsoleContext<LOG_DEBUG> ctx("hmclet constructor");
  fwrap(momentum) = 0;
}

template <typename MassType>
SimpleSampler<MassType>::~SimpleSampler() {}

template <typename MassType>
void SimpleSampler<MassType>::calibrate(
    MPI_Communication *comm, RandomNumber &rng, size_t numSteps,
    VectorType const &initial_params, VectorType const &initial_step) {
  ConsoleContext<LOG_DEBUG> ctx("hmcLet calibrate");

  using CosmoTool::square;
  boost::multi_array<double, 1> params(boost::extents[numParams]);

  fwrap(params) = initial_params;

  massMatrix.clear();

  // We do a few loops to have an idea of the width of the posterior.
  for (size_t i = 0; i < numSteps; i++) {
    for (size_t j = 0; j < numParams; j++) {

      params[j] = slice_sweep_double(
          comm, rng,
          [this, j, &params](double x) -> double {
            params[j] = x;
            return -posterior->evaluate(params);
          },
          params[j], initial_step[j]);
    }

    massMatrix.addMass(params);
  }
  massMatrix.freezeInitial();
}

template <typename MassType>
void SimpleSampler<MassType>::newSample(
    MPI_Communication *comm, RandomNumber &rgen, VectorType &params) {
  ConsoleContext<LOG_DEBUG> ctx("hmcLet singleSampler");
  auto paramSize = boost::extents[numParams];

  SymplecticIntegrators integrator;

  boost::multi_array<double, 1> tmp_gradient(paramSize), saveParams(paramSize),
      savedMomentum(paramSize);
  double Hstart, Hend, delta_H;

  double epsilon;
  int Ntime;

  if (comm->rank() == ROOT_RANK) {
    epsilon = maxEpsilon * (1 - rgen.uniform());
    Ntime = 1 + int(maxNtime * rgen.uniform());
    fwrap(momentum) = momentumScale * fwrap(momentum) + std::sqrt(1-momentumScale*momentumScale)* massMatrix.sample(rgen);
  }

  comm->broadcast_t(&epsilon, 1, ROOT_RANK);
  comm->broadcast_t(&Ntime, 1, ROOT_RANK);
  comm->broadcast_t(momentum.data(), numParams, ROOT_RANK);
  fwrap(savedMomentum) = momentum;

  LibLSS::copy_array(saveParams, params);

  Hstart = posterior->evaluate(saveParams);

  // Do the integration
  ctx.print(boost::format("Integrate epsilon=%g ntime=%d") % epsilon % Ntime);
  try {
    integrator.integrate_dense(
        std::bind(
            &JointPosterior::adjointGradient, posterior.get(), ph::_1, ph::_2),
        massMatrix, epsilon, Ntime, saveParams, momentum, tmp_gradient);

    Hend = posterior->evaluate(saveParams);

    double delta_Ekin;
    {
      auto p = fwrap(momentum);
      auto old_p = fwrap(savedMomentum);
      delta_Ekin = (0.5 * (p - old_p) * massMatrix(p + old_p)).sum();
    }

    delta_H = Hend - Hstart + delta_Ekin;
    double log_u;

    if (comm->rank() == ROOT_RANK)
      log_u = std::log(1 - rgen.uniform());

    comm->broadcast_t(&log_u, 1, ROOT_RANK);

    ctx.print(
        boost::format("deltaEkin = %g, delta_L = %g, deltaH = %g, log_u = %g") %
        delta_Ekin % (Hend - Hstart) % delta_H % log_u);

    if (log_u <= -delta_H) {
      // Accept
      LibLSS::copy_array(params, saveParams);
      ctx.print("Accept");
    }
  } catch (HMCLet::ErrorBadGradient const &) {
    ctx.print2<LOG_ERROR>(
        "A bad gradient computation occured. Reject the sample");
  }

  massMatrix.addMass(params);
}

#include "libLSS/hmclet/diagonal_mass.hpp"
template class LibLSS::HMCLet::SimpleSampler<DiagonalMassMatrix>;

#include "libLSS/hmclet/dense_mass.hpp"
template class LibLSS::HMCLet::SimpleSampler<DenseMassMatrix>;

#include "libLSS/hmclet/mass_burnin.hpp"
template class LibLSS::HMCLet::SimpleSampler<MassMatrixWithBurnin<DiagonalMassMatrix>>;
template class LibLSS::HMCLet::SimpleSampler<MassMatrixWithBurnin<DenseMassMatrix>>;
