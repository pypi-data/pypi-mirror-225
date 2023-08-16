# Inspiration from https://gist.github.com/JayKickliter/06d0e7c4f84ef7ccc7a9
#

find_program(JULIA_EXECUTABLE julia DOC "Julia executable")
IF (NOT JULIA_EXECUTABLE)
  cmessage(STATUS "Julia executable has not been found")
  return()
endif()

#
# Julia version
#
execute_process(
    COMMAND ${JULIA_EXECUTABLE} --version
    OUTPUT_VARIABLE JULIA_VERSION_STRING
    RESULT_VARIABLE RESULT
)
if(RESULT EQUAL 0)
  string(REGEX REPLACE ".*([0-9]+\\.[0-9]+\\.[0-9]+).*" "\\1"
      JULIA_VERSION_STRING ${JULIA_VERSION_STRING})
  string(REGEX REPLACE  "([0-9]+)\\.([0-9]+)\\.([0-9]+)" "JULIA_VERSION_MAJOR=\\1;JULIA_VERSION_MINOR=\\2;JULIA_VERSION_FIX=\\3" JULIA_VERSION_DEFS ${JULIA_VERSION_STRING})
endif()

cmessage(STATUS "Julia version: ${JULIA_VERSION_STRING}")

#
# Julia home
#
IF (JULIA_VERSION_STRING VERSION_GREATER_EQUAL "0.7.0")
  IF (JULIA_VERSION_STRING VERSION_LESS "1.7.0")
    execute_process(
        COMMAND ${JULIA_EXECUTABLE} -E "abspath(Sys.BINDIR)"
        OUTPUT_VARIABLE JULIA_BINDIR
        RESULT_VARIABLE RESULT
    )
    if(RESULT EQUAL 0)
      string(REGEX REPLACE "\"" "" JULIA_BINDIR ${JULIA_BINDIR})
      string(STRIP "${JULIA_BINDIR}" JULIA_BINDIR)
      get_filename_component(JULIA_HOME "${JULIA_BINDIR}/../" ABSOLUTE)
    else()
      cmessage(ERROR "Cannot find JULIA_HOME")
    endif()
  ELSE()
    cmessage(ERROR "Unknown Julia version ${JULIA_VERSION}")
  ENDIF()
ELSE()
  execute_process(
      COMMAND ${JULIA_EXECUTABLE} -E "abspath(JULIA_HOME)"
      OUTPUT_VARIABLE JULIA_HOME
      RESULT_VARIABLE RESULT
  )
  if(RESULT EQUAL 0)
    string(REGEX REPLACE "\"" "" JULIA_HOME ${JULIA_HOME})
    string(STRIP "${JULIA_HOME}" JULIA_HOME)
    set(JULIA_BINDIR "${JULIA_HOME}")
  else()
    cmessage(ERROR "Cannot find JULIA_HOME")
  endif()
ENDIF()


cmessage(STATUS "Julia: Executable is ${JULIA_EXECUTABLE} (${JULIA_VERSION_STRING})")
cmessage(STATUS "Julia: HOME is ${JULIA_HOME}")
cmessage(STATUS "Julia: BINDIR is ${JULIA_BINDIR}")

#
# Check threading
#
execute_process(
    COMMAND ${JULIA_EXECUTABLE} -E "ccall(:jl_threading_enabled, Cint, ()) != 0"
    OUTPUT_VARIABLE JULIA_THREADING_STATE
    RESULT_VARIABLE RESULT
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
cmessage(STATUS "Julia: threading state is '${JULIA_THREADING_STATE}'")
if(RESULT EQUAL 0)
  string(STRIP "${JULIA_THREADING_STATE}" JULIA_THREADING_STATE)
  if (JULIA_THREADING_STATE STREQUAL "true")
    set(JULIA_DEFS "JULIA_ENABLE_THREADING=1")
  elseif(JULIA_THREADING_STATE STREQUAL "false")
    set(JULIA_DEFS "")
  else()
    cmessage(CWARNING "Julia: unknown return value of threading")
  endif()
endif()

set(JULIA_DEFS ${JULIA_DEFS};JULIA_HOME=\"${JULIA_HOME}\";JULIA_BINDIR=\"${JULIA_BINDIR}\";${JULIA_VERSION_DEFS})


#
# Julia includes
#

IF (JULIA_VERSION_STRING VERSION_GREATER_EQUAL "0.7.0")
  IF (JULIA_VERSION_STRING VERSION_LESS "1.7.0")
    execute_process(
      COMMAND ${JULIA_EXECUTABLE} -E "abspath(Sys.BINDIR, Base.INCLUDEDIR, \"julia\")"
      OUTPUT_VARIABLE JULIA_INCLUDE_DIRS
      RESULT_VARIABLE RESULT
    )
  ELSE()
    cmessage(ERROR "Unknown Julia version ${JULIA_VERSION}")
  ENDIF()
ELSE()
  execute_process(
      COMMAND ${JULIA_EXECUTABLE} -E "abspath(\"${JULIA_HOME}\", Base.INCLUDEDIR, \"julia\")"
      OUTPUT_VARIABLE JULIA_INCLUDE_DIRS
      RESULT_VARIABLE RESULT
  )
ENDIF()

if(RESULT EQUAL 0)
    string(REGEX REPLACE "\"" "" JULIA_INCLUDE_DIRS ${JULIA_INCLUDE_DIRS})
    string(STRIP "${JULIA_INCLUDE_DIRS}" JULIA_INCLUDE_DIRS)
    set(JULIA_INCLUDE_DIRS ${JULIA_INCLUDE_DIRS}
        CACHE PATH "Location of Julia include files")
ELSE()
    cmessage(ERROR "Cannot find location of Julia header files")
endif()

#
# Julia libs
#
execute_process(
    COMMAND ${JULIA_EXECUTABLE} -E "using Libdl; dirname(abspath(Libdl.dlpath(\"libjulia\")))"
    OUTPUT_VARIABLE JULIA_LIBRARY_DIR
    RESULT_VARIABLE RESULT
)
if(RESULT EQUAL 0)
    string(REGEX REPLACE "\"" "" JULIA_LIBRARY_DIR "${JULIA_LIBRARY_DIR}")
    string(STRIP "${JULIA_LIBRARY_DIR}" JULIA_LIBRARY_DIR)
    cmessage(STATUS "Julia: library dir is ${JULIA_LIBRARY_DIR}")
    set(JULIA_LIBRARY_DIRS ${JULIA_LIBRARY_DIR}
        CACHE PATH "Location of Julia lib dirs")
endif()

execute_process(
    COMMAND ${JULIA_EXECUTABLE} -E "abspath(\"${JULIA_BINDIR}\", Base.PRIVATE_LIBDIR)"
    OUTPUT_VARIABLE JULIA_PRIVATE_LIBRARY_DIR
    RESULT_VARIABLE RESULT
)
if(RESULT EQUAL 0)
    string(REGEX REPLACE "\"" "" JULIA_PRIVATE_LIBRARY_DIR "${JULIA_PRIVATE_LIBRARY_DIR}")
    string(STRIP "${JULIA_PRIVATE_LIBRARY_DIR}" JULIA_PRIVATE_LIBRARY_DIR)
    cmessage(STATUS "Julia: private library dir is ${JULIA_PRIVATE_LIBRARY_DIR}")
    set(JULIA_PRIVATE_LIBRARY_DIRS ${JULIA_PRIVATE_LIBRARY_DIR}
        CACHE PATH "Location of Julia lib dirs")

    SET(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE) 
    SET(CMAKE_INSTALL_RPATH ${CMAKE_INSTALL_RPATH} "${JULIA_PRIVATE_LIBRARY_DIRS}")
endif()


find_library( JULIA_LIBRARY
    NAMES julia.${JULIA_VERSION_STRING} julia
    PATHS ${JULIA_LIBRARY_DIRS}
    NO_DEFAULT_PATH
)
cmessage(STATUS "Julia: library is ${JULIA_LIBRARY}")

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(
    Julia
    REQUIRED_VARS   JULIA_LIBRARY JULIA_LIBRARY_DIR JULIA_PRIVATE_LIBRARY_DIR JULIA_INCLUDE_DIRS JULIA_DEFS
    VERSION_VAR     JULIA_VERSION_STRING
    FAIL_MESSAGE    "Julia not found"
)
