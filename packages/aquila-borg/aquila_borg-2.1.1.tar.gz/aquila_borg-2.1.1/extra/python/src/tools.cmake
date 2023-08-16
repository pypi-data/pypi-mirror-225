option(BUILD_PYTHON_EMBEDDER OFF)


if (BUILD_PYTHON_EXTENSION AND BUILD_PYTHON_EMBEDDER)

  cmessage(STATUS "Activate Hades_python")

  include_directories(${ARES_MODULE_DIR}/src ${ARES_MODULE_DIR}/python)
  find_library(UTIL_LIBRARY util)

  add_executable(hades_python ${ARES_MODULE_DIR}/src/hades_python.cpp ${ARES_MODULE_DIR}/src/python_bundle_init.cpp ${ARES_MODULE_DIR}/src/python_mock_gen.cpp)
  target_link_libraries(hades_python python_borg hades borg_models LSS ${DEP_LIBS} pybind11::embed ${UTIL_LIBRARY} ${DL_LIBRARY})
  add_dependencies(hades_python ${ares_DEPS})
  if (NOT APPLE)
    target_link_options(hades_python PUBLIC -export-dynamic)
  endif()
  set_property(SOURCE ${extra_hmclet}/hades_julia3.cpp APPEND PROPERTY OBJECT_DEPENDS
    ${ARES_MODULE_DIR}/src/python_mock_gen.hpp
    ${ARES_MODULE_DIR}/src/python_bundle.hpp
    ${ARES_MODULE_DIR}/src/python_bundle_init.hpp
    ${CMAKE_SOURCE_DIR}/src/ares_init.hpp)

endif()
