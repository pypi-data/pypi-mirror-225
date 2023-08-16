SET(EXTRA_HMCLET ${CMAKE_SOURCE_DIR}/extra/hmclet/libLSS/tests)

SET(TEST_hmclet_LIST
  hmclet
  dense_mass
  #conv_hmc
  #weights
  #conv_hmc_julia
)

#SET(TEST_weights_LIBS ${JULIA_LIBRARY})
#SET(TEST_conv_hmc_julia_LIBS ${JULIA_LIBRARY})

IF(BUILD_JULIA)
  SET(TEST_hmclet_LIST ${TEST_hmclet_LIST} julia_hmclet)

  set_property(
    SOURCE ${EXTRA_HMCLET}/test_julia_hmclet.cpp
    APPEND PROPERTY COMPILE_DEFINITIONS
      TEST_JULIA_LIKELIHOOD_CODE="${EXTRA_HMCLET}/test_julia.jl"
  )
  SET(TEST_julia_hmclet_LIBS ${JULIA_LIBRARY})

  add_test(NAME julia_hmclet COMMAND ${CURRENT_CMAKE_BINARY_DIR}/test_julia_hmclet)


ENDIF()
