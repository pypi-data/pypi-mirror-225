#include "libLSS/samplers/hades/hades_linear_likelihood.hpp"
#include "libLSS/physics/hades_pt.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/physics/likelihoods/base.hpp"
#include "libLSS/physics/forwards/registry.hpp"
#include "libLSS/physics/forwards/patch_model.hpp"
#include "libLSS/physics/forwards/softplus.hpp"
#include "libLSS/physics/chain_forward_model.hpp"
#include "libLSS/tools/ptree_proxy_map.hpp"

namespace L = LibLSS::Likelihood;
using LibLSS::LikelihoodInfo;
using LibLSS::HMCDensitySampler;

static const int DOWNGRADE_DATA = 1;

HMCDensitySampler::Likelihood_t makeLikelihood(LikelihoodInfo& info) {
   return std::make_shared<LibLSS::HadesLinearDensityLikelihood>(info);
}


auto makeModel(LibLSS::MPI_Communication * comm, LibLSS::MarkovState& state, LibLSS::BoxModel box, LibLSS::BoxModel box2) {
   using namespace LibLSS;
   auto factory = LibLSS::ForwardRegistry::instance().get("PATCH_MODEL");
   PropertyFromMap properties;

   properties.set("ai", 0.1);
   properties.set("af", 1.0);
   properties.set("k_transition", 0.1);
   
   auto chain = std::make_shared<ChainForwardModel>(comm, box);
   chain->addModel(factory(comm, box, properties));  
   auto softplus = std::make_shared<ForwardSoftPlus>(comm, box);
   softplus->setHardness(3.0);
   chain->addModel(softplus);

   return chain;
}


#include "generic_gradient_test.cpp"

