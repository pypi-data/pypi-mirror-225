SET(ARES_INCLUDE_PATH ${CMAKE_BINARY_DIR} ${r3d_SOURCE_DIR})

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/ares_version.cpp.in ${CMAKE_CURRENT_BINARY_DIR}/ares_version.cpp)

set(ares_LINK)

set(LIBLSS_CONFIG_FILE_NAME ${CMAKE_BINARY_DIR}/libLSS/cconfig.h)
set(LIBLSS_CONFIG_NEW_FILE_NAME ${CMAKE_BINARY_DIR}/libLSS/cconfig_new.h)

function(CHECK_PRETTY)
  FILE(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/CMakeFiles/check_pretty.dir)
  FILE(WRITE ${CMAKE_CURRENT_BINARY_DIR}/CMakeFiles/check_pretty.dir/check.cpp "int main() { const char *s = __PRETTY_FUNCTION__; return 0;}")
  try_compile(RESULT_CHECK_FUNCTION ${CMAKE_CURRENT_BINARY_DIR}/CMakeFiles/check_pretty.dir SOURCES ${CMAKE_CURRENT_BINARY_DIR}/CMakeFiles/check_pretty.dir/check.cpp)

  if (RESULT_CHECK_FUNCTION)
    set(_DEF_PRETTY "#define __LIBLSS_PRETTY_FUNCTION_AVAILABLE 1\n")
  else()
    set(_DEF_PRETTY "#undef __LIBLSS_PRETTY_FUNCTION_AVAILABLE\n")
  endif()
  file(APPEND ${LIBLSS_CONFIG_NEW_FILE_NAME} ${_DEF_PRETTY})
  file(APPEND ${LIBLSS_CONFIG_NEW_FILE_NAME} "#define BOOST_BIND_GLOBAL_PLACEHOLDERS 1\n")
  if (STACKTRACE_USE_BACKTRACE)
    file(APPEND ${LIBLSS_CONFIG_NEW_FILE_NAME} "#define BOOST_STACKTRACE_USE_BACKTRACE 1\n")
  endif()
  file(APPEND ${LIBLSS_CONFIG_NEW_FILE_NAME} "#define BOOST_DISABLE_PRAGMA_MESSAGE 1\n")
  if (${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    file(APPEND ${LIBLSS_CONFIG_NEW_FILE_NAME} "#define BOOST_STACKTRACE_GNU_SOURCE_NOT_REQUIRED 1\n")
  endif()
  file(APPEND ${LIBLSS_CONFIG_NEW_FILE_NAME} "#define __LIBLSS_TEST_REFERENCE_PATH \"${CMAKE_SOURCE_DIR}/libLSS/tests/data/reference_data.h5\"\n")
endfunction()

CHECK_PRETTY()


IF(ENABLE_MPI)
    SET(EXTRA_LIBLSS mpi/real_mpi/mpi_communication.cpp)
ELSE(ENABLE_MPI)
    SET(EXTRA_LIBLSS mpi/fake_mpi/mpi_communication.cpp)
ENDIF(ENABLE_MPI)

include(ares_module)

SET(ARES
    samplers/ares/gibbs_messenger.cpp
    samplers/ares/powerspectrum_a_sampler.cpp
    samplers/ares/powerspectrum_b_sampler.cpp
    samplers/ares/powerspectrum_c_sampler.cpp
    samplers/ares/linbias_sampler.cpp
    samplers/ares/synthetic_selection.cpp
)
SET(MODULE_BUILT "")
foreach(module IN LISTS ARES_MODULES)
  add_liblss_module(${module})
  IF (BUILD_ARES_MODULE_${module})
    SET(MODULE_BUILT "${MODULE_BUILT}\n#define ARES_SUPPORT_${module} 1")
  ENDIF()
endforeach()
FILE(WRITE ${CMAKE_BINARY_DIR}/libLSS/samplers/ares/ares_sampler_option.hpp "${MODULE_BUILT}")

SET(ARES_INCLUDE_PATH ${ARES_INCLUDE_PATH} PARENT_SCOPE)

include_directories(${ARES_INCLUDE_PATH} ${HDF5_INCLUDE_DIR} ${EIGEN_INCLUDE_DIRS})

add_library(LSS
    ${CMAKE_CURRENT_BINARY_DIR}/ares_version.cpp
    physics/cosmo.cpp
    physics/class_cosmo.cpp
    tools/static_init.cpp
    tools/log_traits.cpp
    tools/console.cpp
    tools/sigcatcher.cpp
    mcmc/state_element.cpp
    samplers/core/main_loop.cpp
    samplers/core/gig_sampler.cc
    samplers/core/powerspec_tools.cpp
    tools/fftw_allocator.cpp
    tools/hdf5_error.cpp
    tools/gsl_error.cpp
    tools/memusage.cpp
    tools/string_tools.cpp
    tools/domains.cpp
    ${EXTRA_LIBLSS}
    ${ARES}
    ${r3d_SOURCE_DIR}/r3d.c
)
target_link_libraries(LSS ${ares_LINK} ${BOOST_LIBRARIES} ${LIBCLASS_PATH} ${BACKTRACE_LIBRARY})
if (ENABLE_FULL_WARNINGS)
  target_compile_options(LSS PRIVATE
    $<$<CXX_COMPILER_ID:MSVC>:/W4>
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall>
  )
endif()
set_property(TARGET LSS PROPERTY POSITION_INDEPENDENT_CODE ${BUILD_PYTHON_EXTENSION})

cmessage(WARNING "ARES deps are : ${ares_DEPS}")
add_dependencies(LSS ${ares_DEPS})

if (EXISTS ${LIBLSS_CONFIG_FILE_NAME})
  file(SHA256 ${CMAKE_BINARY_DIR}/libLSS/cconfig_new.h _CONFIG_HASH_NEW)
  file(SHA256 ${CMAKE_BINARY_DIR}/libLSS/cconfig.h _CONFIG_HASH)

  IF(${_CONFIG_HASH} STREQUAL ${_CONFIG_HASH_NEW})
     file(REMOVE ${LIBLSS_CONFIG_NEW_FILE_NAME})
  ELSE()
     file(REMOVE ${LIBLSS_CONFIG_FILE_NAME})
     file(RENAME ${LIBLSS_CONFIG_NEW_FILE_NAME} ${LIBLSS_CONFIG_FILE_NAME})
  ENDIF()
ELSE()
  file(RENAME ${LIBLSS_CONFIG_NEW_FILE_NAME} ${LIBLSS_CONFIG_FILE_NAME})
ENDIF()

execute_process(COMMAND bash ${CMAKE_SOURCE_DIR}/get-aquila-modules.sh --report -q
                OUTPUT_VARIABLE _GIT_STATE
                WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)
FILE(WRITE ${CMAKE_CURRENT_BINARY_DIR}/CMakeFiles/git_report.txt "${_GIT_STATE}")
execute_process(COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_SOURCE_DIR}/build_tools/gen_code_in_header.py 
        ${CMAKE_CURRENT_BINARY_DIR}/CMakeFiles/git_report.txt ${CMAKE_CURRENT_BINARY_DIR}/git_state.cpp
)

subdirs(tests)
