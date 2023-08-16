include(${CMAKE_SOURCE_DIR}/cmake_modules/test_macros.cmake)

SET(LIBS
  ${COSMOTOOL_LIB}
  ${BOOST_LIBRARIES} ${HDF5_CXX_LIBRARIES}
  ${HEALPIX_LIBRARIES} ${HDF5_LIBRARIES}
  ${GSL_LIBRARY} ${GSL_CBLAS_LIBRARY} ${FFTW_LIBRARIES}
  ${ZLIB_LIBRARY}
  ${DL_LIBRARY}
  ${EXTRA_LIB})

IF(RT_LIBRARY)
  SET(LIBS ${LIBS} ${RT_LIBRARY} ${FFTW_LIBRARIES})
ENDIF(RT_LIBRARY)

SET(TEST_LIBRARY_SRCS)
SET(TEST_targets)

SET(TEST_base_LIST
   console has_member proj
   messenger messenger2 messenger3 schechter
   rgen window3d
   slice_sweep slice_sweep_double cic mngp uninit fused_array
   supersampling gradient_supersampling array auto_interpolator
   gig fuse_wrapper tuple fused_cond cic_adjoint cg
   cpu_feature
   r3d hdf5_buffered
   overload class_interface
)

macro(ares_add_test_targets)
  list(APPEND TEST_targets ${ARGN}) 
endmacro()


IF (BUILD_TESTING)
  add_executable(test_stl_container test_stl_container.cpp)

  foreach(module  IN LISTS ARES_MODULES ITEMS base)
    add_liblss_test_module(${module})
  
    foreach(test_name IN ITEMS ${TEST_${module}_LIST})
      if (${module} STREQUAL base)
        set(_src ${CMAKE_SOURCE_DIR}/libLSS/tests)
      else()
        set(_src ${CMAKE_SOURCE_DIR}/extra/${module}/libLSS/tests)
      endif()
      add_executable(test_${test_name} ${_src}/test_${test_name}.cpp)
      SET(test_lib ${LIBS})
      if (TEST_${test_name}_LIBS)
        SET(test_lib ${test_lib} ${TEST_${test_name}_LIBS})
      endif()
      target_link_libraries(test_${test_name} test_library_LSS LSS ${test_lib})
      add_dependencies(test_${test_name} ${ares_DEPS})
      ares_add_test_targets(test_${test_name})
    endforeach(test_name)
  endforeach()


  add_library(test_library_LSS dummy_file.cpp testFramework.cpp ${TEST_LIBRARY_SOURCES})
  add_dependencies(test_library_LSS ${ares_DEPS})
  
  
  macro(list_join listname separator output)
    set(${output})
    foreach(X IN LISTS ${listname})
       set(${output} "${${output}}${separator}${X}")
    endforeach()
  endmacro()
  
  list_join(TEST_targets " " _TEST_targets)
  add_custom_target(all_tests)
  cmessage(STATUS "Meta deps : ${_TEST_targets}")
  add_dependencies(all_tests ${TEST_targets})
  
  
  add_direct_test(test_cosmo_expansion ${CMAKE_CURRENT_SOURCE_DIR}/test_cosmo_expansion.cpp)
  add_check_output_test(test_auto_interpolator ${CMAKE_CURRENT_SOURCE_DIR}/test_auto_interpolator.cpp "")
  add_test_to_run(test_overload test_overload)
  
  #add_test(NAME adam COMMAND ${CMAKE_CURRENT_BINARY_DIR}/test_adam)
  add_test(NAME cg COMMAND ${CMAKE_CURRENT_BINARY_DIR}/test_cg)

endif()
