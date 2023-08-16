cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0074 NEW)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_VISIBILITY_PRESET hidden)

list(INSERT CMAKE_MODULE_PATH  0 "${CMAKE_CURRENT_SOURCE_DIR}/cmake_modules")

IF(DEFINED ARES_PREFIX_PATH)
  SET(ENV{CMAKE_PREFIX_PATH} "${ARES_PREFIX_PATH}")
  SET(CMAKE_PREFIX_PATH "${ARES_PREFIX_PATH}")
ENDIF()

SET(CMAKE_SKIP_BUILD_RPATH FALSE)
SET(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

option(BUILD_JULIA "Activate the Julia support" OFF)

PROJECT(ARES CXX C)

set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS Debug Release RelWithDebInfo)

# Import required cmake modules
include(color_msg)
include(GetGitRevisionDescription)
include(ExternalProject)
include(CTest)
# Not used anymore
#include(GenOptMacro)
include(CheckCXXCompilerFlag)
include(CheckCCompilerFlag)
#include(FortranCInterface)
include(FindOpenMP)
include(FindPkgConfig)
include(clang-format)
include(FetchContent)


IF (CMAKE_C_COMPILER_ID MATCHES "AppleClang" OR CMAKE_CXX_COMPILER_ID MATCHES "AppleClang")
  IF (NOT ${CMAKE_C_COMPILER_ID} STREQUAL ${CMAKE_CXX_COMPILER_ID})
    message(WARNING "C and C++ compiler have different IDs: ${CMAKE_C_COMPILER_ID} != ${CMAKE_CXX_COMPILER_ID}")
  ENDIF()
  message(WARNING "AppleClang does not support OpenMP. Please use something else for more performance.")
  SET(DEFAULT_ENABLE_OPENMP OFF)
ELSE()
  SET(DEFAULT_ENABLE_OPENMP ON)
ENDIF()

# Options
OPTION(ENABLE_OPENMP "Activate OpenMP support" ${DEFAULT_ENABLE_OPENMP})
OPTION(DISABLE_DEBUG_OUTPUT "No debug output support (faster)" OFF)
OPTION(ENABLE_MPI "MPI support" OFF)
OPTION(CONTEXT_TIMER "Activate profiling of LibLSS contexts" OFF)
OPTION(USE_NATIVE_ARCH "Activate instruction set supported by the running system" OFF)
OPTION(ENABLE_FULL_WARNINGS "Ask the compiler to produce lots of warnings" OFF)
OPTION(BUILD_PYTHON_EXTENSION "Build the Python BORG extension" OFF)

IF(ENABLE_MPI)
  find_package(MPI)
  set(EXTRA_LIB ${MPI_C_LIBRARIES})
ELSE(ENABLE_MPI)
  SET(EXTRA_LIB)
  SET(MPI_C_INCLUDE_PATH)
ENDIF(ENABLE_MPI)

IF(USE_NATIVE_ARCH)
  CHECK_CXX_COMPILER_FLAG("-march=native" COMPILER_SUPPORTS_MARCH_NATIVE)
  if(COMPILER_SUPPORTS_MARCH_NATIVE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
  endif()
endif()


include(${CMAKE_SOURCE_DIR}/external/external_build.cmake)

find_program(PYTHON_EXECUTABLE NAMES python3)
IF (NOT PYTHON_EXECUTABLE)
  cmessage(FATAL_ERROR "Python3 interpreter to compile ARES")
ENDIF()

IF (BUILD_JULIA)
  find_package(Julia)
  if (NOT JULIA_EXECUTABLE)
    cmessage(CWARNING "Julia not found, will not be built")
    set(BUILD_JULIA OFF)
  endif()
ENDIF()

IF(BUILD_PYTHON_EXTENSION)
  FetchContent_MakeAvailable(pybind11)
ENDIF()

FetchContent_MakeAvailable(r3d)

# Retrieve current git revision
git_describe(GIT_VER)

IF (DEFINED CMAKE_C_COMPILER_VERSION)
  cmessage(STATUS "C compiler version: ${CMAKE_C_COMPILER_VERSION}")
  cmessage(STATUS "C++ compiler Version: ${CMAKE_CXX_COMPILER_VERSION}")
  if (NOT ${CMAKE_C_COMPILER_VERSION} EQUAL ${CMAKE_CXX_COMPILER_VERSION})
    cmessage(FATAL_ERROR "C and C++ compilers are different. Please fix parameters.")
  ENDIF()
ELSE()
  cmessage(WARNING "Cannot check compiler versions. Proceed with cautions.")
ENDIF()

SET(CMAKE_CXX_FLAGS_PROFILE "-O3 -pg" CACHE STRING "Flags to turn on profiling for C++ compiler")
SET(CMAKE_C_FLAGS_PROFILE "-O3 -pg" CACHE STRING "Flags to turn on profiling for C compiler" )
SET(CMAKE_EXE_LINKER_FLAGS_PROFILE "-pg" CACHE STRING "Flags to turn on profiling in linker")
mark_as_advanced(CMAKE_CXX_FLAGS_PROFILE CMAKE_C_FLAGS_PROFILE CMAKE_EXE_LINKER_FLAGS_PROFILE)

find_library(ZLIB_LIBRARY z)
find_library(_pre_RT_LIBRARY rt)
if(_pre_RT_LIBRARY)
  SET(RT_LIBRARY ${_pre_RT_LIBRARY})
ENDIF()
find_library(DL_LIBRARY dl)


include_directories(
  ${Boost_INCLUDE_DIRS}
  ${GSL_INCLUDE}
  ${CMAKE_SOURCE_DIR}
  ${EIGEN_INCLUDE_DIRS}
  ${EXT_INSTALL}/include
  ${COSMOTOOL_INCLUDE}
  ${HDF5_INCLUDE_DIR}
  ${FFTW_INCLUDE_DIR}
  ${MPI_C_INCLUDE_PATH}
)

#
# OpenMP handling
#


IF(ENABLE_OPENMP)

  IF (NOT OPENMP_FOUND)
    MESSAGE(ERROR "No known compiler option for enabling OpenMP")
  ENDIF(NOT OPENMP_FOUND)

  SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
  SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
  SET(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_C_FLAGS}")

ENDIF(ENABLE_OPENMP)

IF (DISABLE_DEBUG_OUTPUT)
  add_definitions(-DLIBLSS_CONSOLE_NO_DEBUG_SUPPORT)
ENDIF (DISABLE_DEBUG_OUTPUT)

IF(ENABLE_MPI)
  add_definitions(-DARES_MPI_FFTW)
ENDIF (ENABLE_MPI)

IF (CONTEXT_TIMER)
  add_definitions(-DLIBLSS_TIMED_CONTEXT)
ENDIF (CONTEXT_TIMER)

add_definitions(-DBOOST_ENABLE_ASSERT_DEBUG_HANDLER)

SET(ARES_INCLUDE_PATH)


# Detect extra modules
#
#
file(GLOB ARES_MODULES `LIST_DIRECTORIES false RELATIVE ${CMAKE_SOURCE_DIR}/extra ${CMAKE_SOURCE_DIR}/extra/*)

# Remove spurious contaminating OSX directories
list(REMOVE_ITEM ARES_MODULES .DS_Store)

message(STATUS "ARES modules found:")
foreach(module IN LISTS ARES_MODULES)
  if (EXISTS ${CMAKE_SOURCE_DIR}/extra/${module}/DO_NOT_BUILD)
    list(REMOVE_ITEM ARES_MODULES ${module})
    cmessage(CWARNING "  ${module} (do not build)")
  else()
    message(STATUS "  ${module}")
  endif()
endforeach()

add_subdirectory(libLSS)
add_subdirectory(src)

foreach(module IN LISTS ARES_MODULES)
  if (EXISTS ${CMAKE_SOURCE_DIR}/extra/${module}/${module}.cmake)
    include(${CMAKE_SOURCE_DIR}/extra/${module}/${module}.cmake)
  endif()
endforeach()

setup_formatter(ARES_MODULES)
