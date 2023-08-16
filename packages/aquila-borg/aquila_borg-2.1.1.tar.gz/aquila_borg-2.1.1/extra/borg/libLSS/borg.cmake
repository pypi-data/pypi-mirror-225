require_ares_module(hades)

include_directories(${JULIA_INCLUDE_DIRS})
include(${CMAKE_SOURCE_DIR}/extra/hades/scripts/models.cmake)

# Retrieve current git revision
SET(save_dir ${CMAKE_CURRENT_SOURCE_DIR})
SET(CMAKE_CURRENT_SOURCE_DIR ${CMAKE_SOURCE_DIR}/extra/borg/libLSS/)
get_git_head_revision(HEAD BORG_GIT_VER)
SET(CMAKE_CURRENT_SOURCE_DIR ${save_dir})

SET(BASE_BORG_LIBLSS ${CMAKE_SOURCE_DIR}/extra/borg/libLSS/)
configure_file(${BASE_BORG_LIBLSS}/borg_version.cpp.in ${CMAKE_CURRENT_BINARY_DIR}/borg_version.cpp)

SET(EXTRA_BORG ${BASE_BORG_LIBLSS}/samplers/borg)
SET(EXTRA_PHY_BORG ${BASE_BORG_LIBLSS}/physics)
SET(EXTRA_LIBLSS ${EXTRA_LIBLSS}
      ${CMAKE_CURRENT_BINARY_DIR}/borg_version.cpp
      ${EXTRA_BORG}/borg_poisson_likelihood.cpp
      ${EXTRA_BORG}/borg_poisson_meta.cpp
      ${EXTRA_PHY_BORG}/bias/biases.cpp
      ${EXTRA_PHY_BORG}/forwards/borg_lpt.cpp
      ${EXTRA_PHY_BORG}/forwards/borg_qlpt.cpp
      ${EXTRA_PHY_BORG}/forwards/borg_qlpt_rsd.cpp
      ${EXTRA_PHY_BORG}/forwards/borg_2lpt.cpp
      ${EXTRA_PHY_BORG}/forwards/transfer.cpp
      ${EXTRA_PHY_BORG}/forwards/softplus.cpp
      ${EXTRA_PHY_BORG}/forwards/enforceMass.cpp
      ${EXTRA_PHY_BORG}/forwards/downgrade.cpp
      ${EXTRA_PHY_BORG}/forwards/patch_model.cpp
      ${EXTRA_PHY_BORG}/forwards/adapt_generic_bias.cpp
      ${EXTRA_PHY_BORG}/forwards/altair_ap.cpp
      ${EXTRA_PHY_BORG}/forwards/particle_balancer/dyn/particle_distribute.cpp
      ${EXTRA_PHY_BORG}/velocity/velocity_cic.cpp
      ${BASE_BORG_LIBLSS}/io/gadget3.cpp
      ${EXTRA_PHY_BORG}/likelihoods/robust_poisson.cpp
      ${CMAKE_SOURCE_DIR}/extra/borg/libLSS/samplers/generic/run_forward.cpp
      ${CMAKE_SOURCE_DIR}/extra/borg/libLSS/samplers/generic/impl_generic.cpp
      ${CMAKE_SOURCE_DIR}/extra/borg/libLSS/samplers/generic/impl_gaussian.cpp
      ${CMAKE_SOURCE_DIR}/extra/borg/libLSS/samplers/generic/impl_poisson.cpp
      ${CMAKE_SOURCE_DIR}/extra/borg/libLSS/samplers/generic/impl_robust.cpp
      ${CMAKE_SOURCE_DIR}/extra/borg/libLSS/samplers/generic/generic_sigma8.cpp
      ${CMAKE_SOURCE_DIR}/extra/borg/libLSS/samplers/generic/generic_sigma8_second.cpp
      ${CMAKE_SOURCE_DIR}/extra/borg/libLSS/samplers/rgen/qnhmc/qnhmc_density_sampler.cpp
      ${BASE_BORG_LIBLSS}/samplers/lya/base_lya_likelihood.cpp
      ${BASE_BORG_LIBLSS}/samplers/lya/hades_lya_likelihood.cpp
      ${BASE_BORG_LIBLSS}/samplers/lya_rsd_qlpt/hades_lya_likelihood_rsd.cpp
      ${BASE_BORG_LIBLSS}/samplers/altair/altair_meta_sampler.cpp
)

#
# Julia components
#

IF (BUILD_JULIA)
  SET(ARES_JULIA ${CMAKE_SOURCE_DIR}/extra/borg )
  SET(EXTRA_LIBLSS
    ${EXTRA_LIBLSS}
    ${ARES_JULIA}/libLSS/julia/julia_box.cpp
    ${ARES_JULIA}/libLSS/julia/julia_calls.cpp
    ${ARES_JULIA}/libLSS/julia/julia_mcmc.cpp
    ${ARES_JULIA}/libLSS/julia/julia.cpp
    ${ARES_JULIA}/libLSS/julia/julia_ghosts.cpp
    ${ARES_JULIA}/libLSS/physics/forwards/julia.cpp
    ${ARES_JULIA}/libLSS/samplers/julia/julia_likelihood.cpp
  )


  include(FindPythonInterp)

  add_custom_command(
        OUTPUT ${CMAKE_BINARY_DIR}/libLSS/julia/julia_module.hpp
        COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_SOURCE_DIR}/build_tools/gen_code_in_header.py ${ARES_JULIA}/libLSS/julia/julia_module.jl ${CMAKE_BINARY_DIR}/libLSS/julia/julia_module.hpp
        MAIN_DEPENDENCY ${ARES_JULIA}/libLSS/julia/julia_module.jl
  )

  file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/libLSS/julia)
  set_property(SOURCE ${ARES_JULIA}/libLSS/julia/julia.cpp
        APPEND PROPERTY OBJECT_DEPENDS ${CMAKE_BINARY_DIR}/libLSS/julia/julia_module.hpp
  )

  set_property(
    SOURCE
       ${ARES_JULIA}/libLSS/julia/julia.cpp
       ${ARES_JULIA}/libLSS/julia/julia_calls.cpp
       ${ARES_JULIA}/libLSS/julia/julia_box.cpp
    APPEND PROPERTY COMPILE_DEFINITIONS ${JULIA_DEFS}
  )
ENDIF()

# Add a list of includes to be specified to ensure the linker will include all the symbols for automatic registration.
hades_register_forward_models(
  libLSS/physics/forwards/transfer.hpp
  libLSS/physics/forwards/borg_lpt.hpp
  libLSS/physics/forwards/borg_qlpt.hpp
  libLSS/physics/forwards/borg_qlpt_rsd.hpp
  libLSS/physics/forwards/borg_2lpt.hpp
  libLSS/physics/forwards/downgrade.hpp
  libLSS/physics/forwards/softplus.hpp
  libLSS/physics/forwards/enforceMass.hpp
  libLSS/physics/forwards/patch_model.hpp
  libLSS/physics/forwards/adapt_generic_bias.hpp
  libLSS/physics/forwards/altair_ap.hpp
)
