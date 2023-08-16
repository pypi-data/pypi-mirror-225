/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/hmclet/hmclet_qnhmc.cpp
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
#include "libLSS/hmclet/hmclet_qnhmc.hpp"
#include "libLSS/tools/string_tools.hpp"
#include "libLSS/tools/itertools.hpp"

using namespace LibLSS;
using namespace LibLSS::QNHMCLet;
namespace ph = std::placeholders;
using boost::format;

constexpr static int ROOT_RANK = 0;

template <typename MassType, typename BMatrixType>
Sampler<MassType,BMatrixType>::Sampler(
    std::shared_ptr<JointPosterior> _posterior)
    : numParams(_posterior->getNumberOfParameters()), massMatrix(numParams),
      posterior(_posterior), momentum(boost::extents[numParams]),
      B(numParams) {
  ConsoleContext<LOG_DEBUG> ctx("qnhmclet constructor");
  fwrap(momentum) = 0;
}

template <typename MassType, typename BMatrixType>
Sampler<MassType,BMatrixType>::~Sampler() {}

template <typename MassType, typename BMatrixType>
void Sampler<MassType,BMatrixType>::newSample(
    MPI_Communication *comm, RandomNumber &rgen, VectorType &params) {
  ConsoleContext<LOG_DEBUG> ctx("qnhmcLet singleSampler");
  auto paramSize = boost::extents[numParams];

  SymplecticIntegrators integrator;
  BMatrixType C(B);

  boost::multi_array<double, 1> tmp_gradient(paramSize), integrateParams(paramSize),
      savedMomentum(paramSize);
  double Hstart, Hend, delta_H;

  double epsilon;
  int Ntime;

  if (comm->rank() == ROOT_RANK) {
    epsilon = maxEpsilon * (1 - rgen.uniform());
    Ntime = 1 + int(maxNtime * rgen.uniform());
    fwrap(momentum) = momentumScale * fwrap(momentum) + std::sqrt(1-momentumScale*momentumScale)* massMatrix.sample(rgen);
  }

  ctx.print("Momentum is " + to_string(momentum ));

  comm->broadcast_t(&epsilon, 1, ROOT_RANK);
  comm->broadcast_t(&Ntime, 1, ROOT_RANK);
  comm->broadcast_t(momentum.data(), numParams, ROOT_RANK);
  fwrap(savedMomentum) = momentum;

  LibLSS::copy_array(integrateParams, params);

  Hstart = posterior->evaluate(integrateParams);

  // Do the integration
  ctx.print(boost::format("Integrate epsilon=%g ntime=%d") % epsilon % Ntime);
  try {
    integrator.integrate_dense(
        [this,&C,&ctx](Vector const& position, Vector& gradient) {
          posterior->adjointGradient(position, gradient);
	  ctx.print("QN gradient  " + to_string(gradient));
          B.addInfo(position, gradient);
          C(gradient);
	  ctx.print("QN[2] gradient  " + to_string(gradient));
        },
        [this,&C](Vector const& p, auto& tmp_p) {
          fwrap(tmp_p) = massMatrix(p);
          C(tmp_p);
          return fwrap(tmp_p);
        }, epsilon, Ntime, integrateParams, momentum, tmp_gradient
    );

    Hend = posterior->evaluate(integrateParams);

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
      LibLSS::copy_array(params, integrateParams);
      ctx.print("Accept");
      auto& q = B.get();
      ctx.print(boost::format("B=[%g,%g;%g,%g]") % q[0][0] % q[0][1] % q[1][0] % q[1][1]);
    } else {
      if (std::isnan(delta_H)) {
        // Try to recover by resetting completely B
	throw HMCLet::ErrorBadReject("Bad integration"); 
      } else {
      // Reject
      B = C; // Reset the drift matrix
      }
    }
  } catch (HMCLet::ErrorBadGradient const &) {
    ctx.print2<LOG_ERROR>(
        "A bad gradient computation occured. Reject the sample");
    throw HMCLet::ErrorBadReject("Bad gradient");
  }

}

#include "libLSS/hmclet/diagonal_mass.hpp"
template class LibLSS::QNHMCLet::Sampler<HMCLet::DiagonalMassMatrix,BDense>;

#include "libLSS/hmclet/dense_mass.hpp"
template class LibLSS::QNHMCLet::Sampler<HMCLet::DenseMassMatrix,BDense>;
