set(DEP_LIBS
  ${COSMOTOOL_LIB}
  ${BOOST_LIBRARIES}
  ${HEALPIX_LIBRARIES}
  ${HDF5_CXX_LIBRARIES}
  ${HDF5_LIBRARIES}
  ${FFTW_LIBRARIES}
  ${GSL_LIBRARY}
  ${GSL_CBLAS_LIBRARY}
  ${ZLIB_LIBRARY}
  ${DL_LIBRARY}
  ${EXTRA_LIB}
)

IF(RT_LIBRARY)
  SET(DEP_LIBS ${DEP_LIBS} ${RT_LIBRARY})
ENDIF(RT_LIBRARY)

include_directories(${ARES_INCLUDE_PATH}
  ${CMAKE_CURRENT_SOURCE_DIR}
  ${CMAKE_CURRENT_BINARY_DIR}
  ${Boost_INCLUDE_DIRS})

add_executable(ares3 ares3.cpp)
target_link_libraries(ares3 LSS ${DEP_LIBS})
add_dependencies(ares3 ${ares_DEPS})
set_property(SOURCE ares3.cpp APPEND PROPERTY OBJECT_DEPENDS
   ${CMAKE_CURRENT_SOURCE_DIR}/ares_mock_gen.hpp
   ${CMAKE_CURRENT_SOURCE_DIR}/ares_bundle.hpp
   ${CMAKE_CURRENT_SOURCE_DIR}/ares_bundle_init.hpp
   ${CMAKE_CURRENT_SOURCE_DIR}/ares_init.hpp)

foreach(module IN LISTS ARES_MODULES)
  set(_fname ${CMAKE_SOURCE_DIR}/extra/${module}/src/tools.cmake)
  if (EXISTS ${_fname})
    SET(ARES_MODULE_DIR ${CMAKE_SOURCE_DIR}/extra/${module})
    include(${_fname})
  endif()
endforeach()
