check_ares_module(DM_SHEET_PRESENT dm_sheet)


set(EXTRA_BORG ${CMAKE_SOURCE_DIR}/extra/borg/src)

include_directories(${CMAKE_SOURCE_DIR}/src)
include_directories(${EXTRA_BORG})

add_library(borg_models ${EXTRA_BORG}/bias_generator.cpp)
add_dependencies(borg_models ${ares_DEPS})

add_executable(borg_forward ${EXTRA_BORG}/borg_forward.cpp)
target_link_libraries(borg_forward borg_models hades LSS ${DEP_LIBS})
add_dependencies(borg_forward ${ares_DEPS})

if (DM_SHEET_PRESENT)
  set_property(
    SOURCE
       ${EXTRA_BORG}/borg_forward.cpp
    APPEND PROPERTY COMPILE_DEFINITIONS DM_SHEET_PRESENT
  )
endif()


set_property(SOURCE ${extra_hades}/hades3.cpp APPEND PROPERTY OBJECT_DEPENDS
    ${EXTRA_BORG}/borg_generic_bundle.hpp)

add_executable(borg2gadget3 ${EXTRA_BORG}/borg2gadget3.cpp)
target_link_libraries(borg2gadget3 LSS ${DEP_LIBS})
add_dependencies(borg2gadget3 ${ares_DEPS})

#
# Lyman-alpha support
#

FILE(WRITE ${CMAKE_BINARY_DIR}/src/hades_lya_option.hpp ${HADES_OPTION_LYA})

add_executable(hades_lya ${EXTRA_BORG}/hades_lya.cpp)
target_link_libraries(hades_lya hades LSS ${DEP_LIBS})
add_dependencies(hades_lya ${ares_DEPS})
set_property(SOURCE ${EXTRA_BORG}/hades_lya.cpp APPEND PROPERTY OBJECT_DEPENDS
  ${EXTRA_BORG}/hades_lya_bundle.hpp
  ${EXTRA_BORG}/hades_lya_bundle_init.hpp
  ${CMAKE_SOURCE_DIR}/src/ares_init.hpp
)

