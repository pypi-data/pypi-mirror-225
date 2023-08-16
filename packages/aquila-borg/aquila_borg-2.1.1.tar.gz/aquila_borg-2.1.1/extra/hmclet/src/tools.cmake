check_ares_module(BORG_PRESENT borg)

set(extra_hmclet ${CMAKE_SOURCE_DIR}/extra/hmclet/src)

SET(HADES_OPTION)

include_directories(${extra_hmclet})

IF (BUILD_JULIA)

  cmessage(STATUS "Activate Hades_Julia core")

  add_executable(hades_julia3 ${extra_hmclet}/hades_julia3.cpp ${extra_hmclet}/julia_mock_gen.hpp)
  target_link_libraries(hades_julia3 hades borg_models LSS ${DEP_LIBS} ${JULIA_LIBRARY})
  add_dependencies(hades_julia3 ${ares_DEPS})
  set_property(SOURCE ${extra_hmclet}/hades_julia3.cpp APPEND PROPERTY OBJECT_DEPENDS
    ${extra_hmclet}/julia_mock_gen.hpp
    ${extra_hmclet}/julia_bundle.hpp
    ${extra_hmclet}/julia_bundle_init.hpp
    ${CMAKE_SOURCE_DIR}/src/ares_init.hpp)
ELSE()
    cmessage(CWARNING "Julia missing, Hades_Julia disabled")
ENDIF()
