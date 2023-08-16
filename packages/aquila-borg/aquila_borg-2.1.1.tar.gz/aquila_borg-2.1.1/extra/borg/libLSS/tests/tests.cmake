SET(EXTRA_BORG ${CMAKE_SOURCE_DIR}/extra/borg/libLSS/tests)

include(${CMAKE_SOURCE_DIR}/extra/hades/scripts/gradient_tests.cmake)
include(${CMAKE_SOURCE_DIR}/extra/borg/scripts/borg_tests.cmake)

set(TEST_LIBRARY_SOURCES ${EXTRA_HADES}/setup_hades_test_run.cpp)

include_directories(${EXTRA_HADES} ${CMAKE_SOURCE_DIR}/extra/borg/src ${CMAKE_SOURCE_DIR}/src)

#add_executable(borg_lpt_benchmark ${EXTRA_BORG}/borg_lpt_benchmark.cpp)
#target_link_libraries(borg_lpt_benchmark LSS ${LIBS})
#add_dependencies(borg_lpt_benchmark ${ares_DEPS})

SET(TEST_borg_LIST
    part_swapper aux_attributes generic_likelihood_base
    generic_likelihood_s_field generic_likelihood_bias
    ghost_planes
    many_power fmin
    robust_poisson
    generic_likelihood_foreground
    power_law_1
    patch_model
    forward_velocity
)

hades_add_gradient_test(borg_gradients ${EXTRA_BORG}/borg_gradients.py_config)
hades_add_forward_test(borg_base ${EXTRA_BORG}/borg_forward.py_config)
borg_add_vobs_test(borg_vobs ${EXTRA_BORG}/borg_vobs.py_config)

set_property(
  SOURCE ${EXTRA_BORG}/test_borg_many_power_gradient.cpp
  APPEND PROPERTY COMPILE_DEFINITIONS
    HADES_SUPPORT_BORG=1
)

add_executable(benchmark_generic_likelihood ${EXTRA_BORG}/benchmark_generic_likelihood.cpp)
target_link_libraries(benchmark_generic_likelihood test_library_LSS LSS ${LIBS})

if (BUILD_JULIA)
 SET(TEST_borg_LIST ${TEST_borg_LIST} julia_core julia_likelihood)
 SET(TEST_julia_core_LIBS ${JULIA_LIBRARY})
 SET(TEST_julia_likelihood_LIBS ${JULIA_LIBRARY})

 add_executable(julia_gradient_test ${EXTRA_BORG}/julia_gradient_test.cpp)
 target_link_libraries(julia_gradient_test test_library_LSS LSS ${LIBS} ${JULIA_LIBRARY})

 set_property(
   SOURCE ${EXTRA_BORG}/test_julia_likelihood.cpp
   APPEND PROPERTY COMPILE_DEFINITIONS
     TEST_JULIA_LIKELIHOOD_CODE="${EXTRA_BORG}/test_julia.jl"
 )

 add_test_to_run(julia_core test_julia_core)
 add_test_to_run(julia_likelihood test_julia_likelihood)
endif()

add_test_to_run(fmin test_fmin)
add_test_to_run(power_law_bias1 test_power_law_1 )

add_executable(test_fuse_reduce ${EXTRA_BORG}/test_fuse_reduce.cpp)
add_dependencies(test_fuse_reduce ${ares_DEPS})
target_link_libraries(test_fuse_reduce LSS ${LIBS})

add_failing_test(borg_poisson_param ${EXTRA_BORG}/test_voxel_poisson_fail.cpp)
add_check_output_test(borg_poisson_success ${EXTRA_BORG}/test_voxel_poisson.cpp "")
add_check_output_test(power_law_bias_0 ${EXTRA_BORG}/test_power_law_0.cpp "")
#add_check_output_test(power_law_bias_1 ${EXTRA_BORG}/test_power_law_1.cpp "")
add_check_output_test(broken_power_law_bias ${EXTRA_BORG}/test_broken_power_law.cpp "")

foreach (N test_forward_lpt test_forward_2lpt test_forward_qlpt test_forward_qlpt_rsd test_aux_attributes)
	add_test(NAME BORG_${N} COMMAND ${CURRENT_CMAKE_BINARY_DIR}/${N})
endforeach()
