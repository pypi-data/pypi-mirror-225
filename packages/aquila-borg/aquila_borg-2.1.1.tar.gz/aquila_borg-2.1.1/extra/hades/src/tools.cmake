check_ares_module(BORG_PRESENT borg)

set(extra_hades ${CMAKE_SOURCE_DIR}/extra/hades/src)

SET(HADES_OPTION)

set(BORG_CODE)
IF(BORG_PRESENT)
  cmessage(STATUS "HADES found BORG")
  SET(HADES_OPTION "${HADES_OPTION}#define HADES_SUPPORT_BORG 1\n")

  IF(BUILD_JULIA)
    cmessage(STATUS "HADES will support JULIA likelihood")
    SET(HADE_OPTION "${HADES_OPTION}#define HADES_SUPPORT_JULIA 1\n")
  else()
    cmessage(CWARNING "HADES did not find JULIA")
  endif()
else()
  cmessage(CWARNING "HADES did not find BORG")
ENDIF()

FILE(WRITE ${CMAKE_BINARY_DIR}/src/hades_option.hpp ${HADES_OPTION})
include_directories(${extra_hades})

add_library(hades ${extra_hades}/likelihood_info.cpp ${BORG_CODE})
add_dependencies(hades ${ares_DEPS})

add_executable(hades3 ${extra_hades}/hades3.cpp ${extra_hades}/hades_mock_gen.hpp )

target_link_libraries(hades3 hades LSS ${DEP_LIBS})
add_dependencies(hades3 ${ares_DEPS})
set_property(SOURCE ${extra_hades}/hades3.cpp APPEND PROPERTY OBJECT_DEPENDS
  ${extra_hades}/hades_mock_gen.hpp
  ${extra_hades}/hades_bundle.hpp
  ${extra_hades}/hades_bundle_init.hpp
  ${CMAKE_BINARY_DIR}/libLSS/physics/forwards/all_models.hpp
  ${CMAKE_SOURCE_DIR}/src/ares_init.hpp)

