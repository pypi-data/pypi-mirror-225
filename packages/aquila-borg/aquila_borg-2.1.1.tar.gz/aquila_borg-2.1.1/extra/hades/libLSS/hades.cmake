
SET(EXTRA_HADES ${CMAKE_SOURCE_DIR}/extra/hades/libLSS)
SET(EXTRA_LIBLSS ${EXTRA_LIBLSS}
  ${EXTRA_HADES}/samplers/hades/base_likelihood.cpp
  ${EXTRA_HADES}/physics/likelihoods/base.cpp
  ${EXTRA_HADES}/physics/forward_model.cpp
  ${EXTRA_HADES}/samplers/rgen/hmc/hmc_density_sampler.cpp
  ${EXTRA_HADES}/samplers/hades/hades_linear_likelihood.cpp
  ${EXTRA_HADES}/samplers/core/gridLikelihoodBase.cpp
  ${EXTRA_HADES}/samplers/core/simpleLikelihood.cpp
  ${EXTRA_HADES}/samplers/core/generate_random_field.cpp
  ${EXTRA_HADES}/physics/model_io.cpp    
  ${EXTRA_HADES}/physics/forwards/primordial.cpp    
  ${EXTRA_HADES}/physics/forwards/fnl.cpp    
  ${EXTRA_HADES}/physics/forwards/transfer_ehu.cpp    
  ${EXTRA_HADES}/physics/forwards/registry.cpp    
  ${EXTRA_HADES}/physics/chain_forward_model.cpp    
  ${EXTRA_HADES}/physics/branch.cpp    
  ${EXTRA_HADES}/physics/sum.cpp    
  ${EXTRA_HADES}/physics/haar.cpp
  ${EXTRA_HADES}/physics/hades_pt.cpp    
  ${EXTRA_HADES}/physics/hades_log.cpp    
  ${EXTRA_HADES}/physics/forwards/upgrade.cpp
  ${EXTRA_HADES}/samplers/rgen/frozen/frozen_phase_density_sampler.cpp
  ${EXTRA_HADES}/samplers/model_params.cpp
  ${EXTRA_HADES}/samplers/bias_model_params.cpp
  ${EXTRA_HADES}/tools/hermiticity_fixup.cpp
)

include(${EXTRA_HADES}/../scripts/models.cmake)

hades_register_forward_models(
  libLSS/physics/forwards/primordial.hpp
  libLSS/physics/forwards/transfer_ehu.hpp
  libLSS/physics/forwards/fnl.hpp
  libLSS/physics/hades_pt.hpp
  libLSS/physics/haar.hpp
  libLSS/physics/hades_log.hpp
  libLSS/physics/forwards/upgrade.hpp
)
