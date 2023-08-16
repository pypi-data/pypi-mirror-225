/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/samplers/core/splitLikelihood.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/tools/console.hpp"
#include "libLSS/samplers/core/splitLikelihood.hpp"
#include "libLSS/tools/overload.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include <boost/variant.hpp>
#include <functional>

using namespace LibLSS;

SplitAndReshapeLikelihood::SplitAndReshapeLikelihood(MPI_Communication *comm_)
    : comm(comm_) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
}

SplitAndReshapeLikelihood::~SplitAndReshapeLikelihood() {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
}

void SplitAndReshapeLikelihood::initializeLikelihood(MarkovState &state) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  for (auto &l : parameterLikelihood) {
    boost::apply_visitor(
        [&state](std::shared_ptr<LikelihoodBase> &likelihood) {
          likelihood->initializeLikelihood(state);
        },
        std::get<1>(l));
  }
}

void SplitAndReshapeLikelihood::updateMetaParameters(MarkovState &state) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  for (auto &l : parameterLikelihood) {
    boost::apply_visitor(
        [&state](std::shared_ptr<LikelihoodBase> &likelihood) {
          likelihood->updateMetaParameters(state);
        },
        std::get<1>(l));
  }
}
void SplitAndReshapeLikelihood::setupDefaultParameters(
    MarkovState &state, int catalog) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  for (auto &l : parameterLikelihood) {
    boost::apply_visitor(
        [&state, catalog](std::shared_ptr<LikelihoodBase> &likelihood) {
          likelihood->setupDefaultParameters(state, catalog);
        },
        std::get<1>(l));
  }
}

void SplitAndReshapeLikelihood::updateCosmology(
    CosmologicalParameters const &params) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  for (auto &l : parameterLikelihood) {
    boost::apply_visitor(
        [&params](std::shared_ptr<LikelihoodBase> &likelihood) {
          likelihood->updateCosmology(params);
        },
        std::get<1>(l));
  }
}

void SplitAndReshapeLikelihood::commitAuxiliaryFields(MarkovState &state) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  for (auto &l : parameterLikelihood) {
    boost::apply_visitor(
        [&state](std::shared_ptr<LikelihoodBase> &likelihood) {
          likelihood->commitAuxiliaryFields(state);
        },
        std::get<1>(l));
  }
}

/*
 * ---------------------------------------------------------------------
 * getTotalNumberOfParameters
 *
 * getTotalNumberOfParameters needs to implement explicitly the function
 * for each variant of likelihood.
 */

static unsigned int computeNumberOfParametersGrid(
    std::shared_ptr<GridDensityLikelihoodBase<3>> grid) {
  auto mgr = grid->getManager();

  return mgr->localN0 * mgr->N1 * mgr->N2_HC * 2;
}

static unsigned int computeNumberOfParametersSimple(
    MPI_Communication *comm, std::shared_ptr<SimpleLikelihood> simple) {
  // The node with rank 0 will be in charge of generating the required
  // random numbers/proposals.
  return comm->rank() == 0 ? simple->numDimensions() : 0;
}

unsigned int SplitAndReshapeLikelihood::getTotalNumberOfParameters() {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  unsigned int total = 0;
  for (auto &l : parameterLikelihood) {
    total += boost::apply_visitor(
        overload(
            computeNumberOfParametersGrid,
            std::bind(
                &computeNumberOfParametersSimple, comm, std::placeholders::_1)),
        std::get<1>(l));
  }
  return total;
}

// ---------------------------------------------------------------------

void SplitAndReshapeLikelihood::addNamedParameter(
    std::string parameter, LikelihoodVariant likelihood) {
  parameterLikelihood.push_back(std::make_tuple(parameter, likelihood));
}

/*
 * ---------------------------------------------------------------------
 * logLikelihood needs a separate treatment based on each variant
 * 
 */

static double logLikelihoodSimple(
    MPI_Communication *comm, ParameterSpace &global,
    std::shared_ptr<SimpleLikelihood> simple, unsigned int start,
    boost::const_multi_array_ref<double, 1> const &params) {
  unsigned int num = simple->numDimensions();
  boost::multi_array<double, 1> paramsSubSet(boost::extents[num]);
  typedef boost::multi_array_types::index_range range;

  fwrap(paramsSubSet) = fwrap(params[range(start, start + num)]);
  double loc_L = simple->logLikelihoodSimple(global, params);
  double L = 0;

  comm->all_reduce_t(&loc_L, &L, 1, MPI_SUM);
  return L;
}

double SplitAndReshapeLikelihood::logLikelihood(
    LibLSS::const_multi_array_ref<double, 1> &params) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  unsigned int start = 0;
  ParameterSpace global;
  double L = 0;

  for (auto &l : parameterLikelihood) {
    L += boost::apply_visitor(
        overload(std::bind(&logLikelihoodSimple, comm, global, start, params)),
        std::get<1>(l));
  }

  return L;
}