OPTION(INTERNAL_BOOST "Use internal version of the Boost library" ON)
OPTION(INTERNAL_EIGEN "Use internal version of the Eigen library" ON)
OPTION(INTERNAL_HDF5 "Use internal HDF5" ON)
OPTION(INTERNAL_GSL "Use internal GSL" ON)
OPTION(INTERNAL_FFTW "Use internal FFTW" ON)
OPTION(STACKTRACE_USE_BACKTRACE "Use backtrace for stacktrace" ON)

message(STATUS "Compiler ID is: C -> ${CMAKE_C_COMPILER_ID}, CXX -> ${CMAKE_CXX_COMPILER_ID}")

MACRO(CHECK_CHANGE_STATE VAR)
  IF (DEFINED _PREVIOUS_${VAR})
#    message("Already defined value=${_PREVIOUS_${VAR}}")
    IF (NOT ${_PREVIOUS_${VAR}}} EQUAL ${${VAR}})
#      message("Not equal to previous state")
      foreach(loopvar ${ARGN})
#         message("Clearing ${loopvar}")
         UNSET(${loopvar} CACHE)
      endforeach()
    ENDIF (NOT ${_PREVIOUS_${VAR}}} EQUAL ${${VAR}})
  ENDIF (DEFINED _PREVIOUS_${VAR})
#  message("Marking internal ${VAR} with ${${VAR}}")
  SET(_PREVIOUS_${VAR} ${${VAR}} CACHE INTERNAL "Internal value")
ENDMACRO(CHECK_CHANGE_STATE)

CHECK_CHANGE_STATE(INTERNAL_BOOST Boost_LIBRARIES Boost_INCLUDE_DIRS)
CHECK_CHANGE_STATE(INTERNAL_GSL GSL_LIBRARY GSL_CBLAS_LIBRARY GSL_INCLUDE)
CHECK_CHANGE_STATE(INTERNAL_HDF5 HDF5_INCLUDE_DIR HDF5_LIBRARIES HDF5_CXX_LIBRARIES HDF5_DIR)


SET(BUILD_PREFIX ${CMAKE_BINARY_DIR}/external_build)
SET(EXT_INSTALL ${CMAKE_BINARY_DIR}/ext_install)

################
# BUILD CFITSIO
################

SET(CFITSIO_URL "http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-3.47.tar.gz" CACHE STRING "URL to download CFITSIO from")
mark_as_advanced(CFITSIO_URL)

ExternalProject_Add(cfitsio
  URL ${CFITSIO_URL}
  URL_HASH SHA1=5a25016dcaf12117d950e4278e10d39c6c7d33a5
  PREFIX ${BUILD_PREFIX}/cfitsio-prefix
  CONFIGURE_COMMAND ./configure --prefix=${EXT_INSTALL} --disable-curl CPPFLAGS=${CONFIGURE_CPP_FLAGS} CC=${CMAKE_C_COMPILER} CXX=${CMAKE_CXX_COMPILER}
  BUILD_IN_SOURCE 1
  BUILD_BYPRODUCTS ${EXT_INSTALL}/lib/libcfitsio.a
)


SET(CFITSIO_LIBRARY ${EXT_INSTALL}/lib/libcfitsio.a)
SET(ares_DEPS ${ares_DEPS} cfitsio)



################
# BUILD HEALPIX
################

SET(HEALPIX_URL "https://sourceforge.net/projects/healpix/files/Healpix_3.50/healpix_cxx-3.50.0.tar.gz/download" CACHE STRING "URL for Healpix")

SET(HEALPIX_BUILD ${BUILD_PREFIX}/healpix-prefix/src/healpix-build)
SET(HEALPIX_DIR ${BUILD_PREFIX}/healpix-prefix/src/healpix)

ExternalProject_Add(healpix
    DEPENDS cfitsio
    PREFIX ${BUILD_PREFIX}/healpix-prefix
    URL ${HEALPIX_URL}
    URL_HASH SHA1=c8a537e743f760dfa453cad246065d37f72fc0cb
    CONFIGURE_COMMAND ${CMAKE_COMMAND}
        -DHEALPIX_CC=${CMAKE_C_COMPILER}
        -DHEALPIX_CXX=${CMAKE_CXX_COMPILER}
        -DHEALPIX_DIR:STRING=${HEALPIX_DIR}
        -DHEALPIX_INSTALL:STRING=${EXT_INSTALL}
        -DCFITSIO_LIB:STRING=${CFITSIO_LIBRARY}
        -P ${CMAKE_SOURCE_DIR}/external/configure_healpix.cmake
    BUILD_BYPRODUCTS ${EXT_INSTALL}/lib/libhealpix_cxx.a
)
SET(HEALPIX_LIBRARIES
  ${EXT_INSTALL}/lib/libhealpix_cxx.a
  ${EXT_INSTALL}/lib/libcfitsio.a
)
SET(ares_DEPS ${ares_DEPS} healpix)

#
# Backtrace
#
SET(BACKTRACE_LIBRARY)
IF (STACKTRACE_USE_BACKTRACE)
  SET(BACKTRACE_URL "https://github.com/ianlancetaylor/libbacktrace/archive/f24e9f401fde0249ca48fa98493a672e83b0f3dc.tar.gz" CACHE STRING "URL to download backtrace from")  
  mark_as_advanced(BACKTRACE_URL)
  ExternalProject_Add(backtrace
    URL ${BACKTRACE_URL}
    URL_HASH SHA1=1a12ce8dbe94980ebf3fc7e8bd22f376e3bd21cb
    PREFIX ${BUILD_PREFIX}/backtrace-prefix
    CONFIGURE_COMMAND ./configure --prefix=${EXT_INSTALL} --with-pic CPPFLAGS=${CONFIGURE_CPP_FLAGS} CC=${CMAKE_C_COMPILER} CXX=${CMAKE_CXX_COMPILER}
    BUILD_IN_SOURCE 1
    BUILD_BYPRODUCTS ${EXT_INSTALL}/lib/libbacktrace.a
  )
  SET(ares_DEPS ${ares_DEPS} backtrace)
  SET(BACKTRACE_LIBRARY  ${EXT_INSTALL}/lib/libbacktrace.a)
ENDIF()

################
# BUILD BOOST
################
IF (INTERNAL_BOOST)
    SET(BOOST_URL "https://boostorg.jfrog.io/artifactory/main/release/1.74.0/source/boost_1_74_0.tar.bz2" CACHE STRING "URL to download Boost from")
    mark_as_advanced(BOOST_URL)

    SET(BOOST_SOURCE_DIR ${BUILD_PREFIX}/boost-prefix/src/boost)

    set(LINKER_EXTRA_FLAGS)
    message(STATUS "Compiler version is ${CMAKE_CXX_COMPILER_VERSION}, ID is ${CMAKE_CXX_COMPILER_ID}")
    string(REGEX REPLACE "^([0-9]+\\.[0-9]+).*$" "\\1" ToolsetVer "${CMAKE_CXX_COMPILER_VERSION}")
    IF(CMAKE_CXX_COMPILER_ID MATCHES "^Intel$")
       SET(b2_toolset intel)
       SET(COMPILER_EXTRA_FLAGS "-fPIC")
    elseif (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
       if (${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
         SET(b2_toolset darwin)
       else()
         SET(b2_toolset gcc)
         SET(COMPILER_EXTRA_FLAGS "-fPIC -std=gnu++14")
       endif()
       add_definitions("-Wno-unused-local-typedefs")
    elseif (CMAKE_CXX_COMPILER_ID STREQUAL "AppleClang")
       SET(b2_toolset darwin)
       SET(COMPILER_EXTRA_FLAGS "-std=c++14")
    elseif (CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
       SET(b2_toolset clang)
       SET(COMPILER_EXTRA_FLAGS "-std=c++14")
    endif()
    SET(COMPILER_EXTRA_FLAGS "${COMPILER_EXTRA_FLAGS} -I${EXT_INSTALL}/include")
    SET(LINKER_EXTRA_FLAGS "${LINKER_EXTRA_FLAGS} -L${EXT_INSTALL}/lib")
    message(STATUS "Building boost with toolset ${b2_toolset}")

    IF (STACKTRACE_USE_BACKTRACE)
       SET(BOOST_STACKTRACE ${BOOST_SOURCE_DIR}/stage/lib/libboost_stacktrace_backtrace.a)
       SET(BOOST_DEPS backtrace)
    ELSE()
       SET(BOOST_STACKTRACE ${BOOST_SOURCE_DIR}/stage/lib/libboost_stacktrace_basic.a)
       SET(BOOST_DEPS)
    ENDIF()

    SET(BOOST_LIBRARIES
        ${BOOST_SOURCE_DIR}/stage/lib/libboost_timer.a
        ${BOOST_SOURCE_DIR}/stage/lib/libboost_chrono.a
        ${BOOST_SOURCE_DIR}/stage/lib/libboost_random.a
        ${BOOST_SOURCE_DIR}/stage/lib/libboost_regex.a
        ${BOOST_SOURCE_DIR}/stage/lib/libboost_program_options.a
        ${BOOST_SOURCE_DIR}/stage/lib/libboost_system.a
        ${BOOST_STACKTRACE}
        ${BOOST_SOURCE_DIR}/stage/lib/libboost_exception.a)
    ExternalProject_Add(boost
        URL ${BOOST_URL}
        DEPENDS ${BOOST_DEPS}
	URL_HASH SHA1=f82c0d8685b4d0e3971e8e2a8f9ef1551412c125
        PREFIX ${BUILD_PREFIX}/boost-prefix
        CONFIGURE_COMMAND ${CMAKE_COMMAND}  -DTOOLSET=${b2_toolset} "-DCOMPILER:STRING=${CMAKE_CXX_COMPILER}" "-DCOMPILER_EXTRA_FLAGS=${COMPILER_EXTRA_FLAGS}" "-DINSTALL_PATH:STRING=${EXT_INSTALL}" "-DLINKER_EXTRA_FLAGS=${LINKER_EXTRA_FLAGS}" "-DSRC_DIR:STRING=${BOOST_SOURCE_DIR}" -P ${CMAKE_SOURCE_DIR}/external/configure_boost.cmake
        BUILD_IN_SOURCE 1
        BUILD_COMMAND ${BOOST_SOURCE_DIR}/b2 --with-regex -d+2 --with-exception --with-chrono --with-timer --with-program_options --with-random --with-stacktrace toolset=${b2_toolset}-cmake variant=release
        INSTALL_COMMAND echo "No install"
	BUILD_BYPRODUCTS ${BOOST_LIBRARIES}
    )
#        PATCH_COMMAND patch -p1 -d ${BOOST_SOURCE_DIR} -i ${CMAKE_SOURCE_DIR}/external/patch-boost

    SET(Boost_INCLUDE_DIRS ${BOOST_SOURCE_DIR} CACHE STRING "Boost path" FORCE)

    SET(boost_built boost)
    mark_as_advanced(Boost_INCLUDE_DIRS)
    SET(ares_DEPS ${ares_DEPS} boost)

ELSE (INTERNAL_BOOST)
    find_package(Boost 1.69 REQUIRED COMPONENTS random chrono regex system program_options timer stacktrace_basic OPTIONAL_COMPONENTS stacktrace_backtrace stacktrace_addr2line)
    if (${Boost_VERSION} VERSION_GREATER 1000)
       math(EXPR TMP_MAJOR "${Boost_VERSION} / 100000")
       math(EXPR TMP_MINOR "(${Boost_VERSION} - ${TMP_MAJOR} * 100000) / 100")
       math(EXPR TMP_PATCHLEVEL "${Boost_VERSION} - ${TMP_MAJOR} * 100000 - ${TMP_MINOR} * 100")
       set(Boost_VERSION ${TMP_MAJOR}.${TMP_MINOR}.${TMP_PATCHLEVEL})
    ENDIF()
    message(STATUS "Boost version ${Boost_VERSION}")
    if (${Boost_VERSION} VERSION_GREATER_EQUAL 1.70)
       set(BOOST_LIBRARIES Boost::headers Boost::random Boost::chrono Boost::regex Boost::system Boost::program_options Boost::timer)
       if (Boost_stacktrace_backtrace_FOUND)
          set(BOOST_LIBRARIES ${BOOST_LIBRARIES} Boost::stacktrace_backtrace)
       else()
          set(BOOST_LIBRARIES ${BOOST_LIBRARIES} Boost::stacktrace_basic)
       endif()
    else()
      SET(BOOST_LIBRARIES ${Boost_LIBRARIES})
    endif()
    SET(BOOST_ROOT)
    SET(boost_built)
ENDIF (INTERNAL_BOOST)

################
# BUILD Eigen
################
IF (INTERNAL_EIGEN)
    SET(EIGEN_URL "https://gitlab.com/libeigen/eigen/-/archive/3.3.7/eigen-3.3.7.tar.bz2"  CACHE STRING "URL to download Eigen from")
    mark_as_advanced(EIGEN_URL)

    ExternalProject_Add(eigen
        URL ${EIGEN_URL}
        URL_HASH MD5=b9e98a200d2455f06db9c661c5610496
        PREFIX ${BUILD_PREFIX}/eigen-prefix
        CMAKE_ARGS
          -DCMAKE_INSTALL_PREFIX=${EXT_INSTALL} -DEIGEN_TEST_NO_OPENGL=ON
          -DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}
          -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}
#        PATCH_COMMAND ${CMAKE_COMMAND}
#            -DBUILD_PREFIX=${BUILD_PREFIX}/eigen-prefix
#            -DPATCH_FILE=${CMAKE_SOURCE_DIR}/external/patch_eigen
#            -DSOURCE_PREFIX=${BUILD_PREFIX}/eigen-prefix/src/eigen
#            -P ${CMAKE_SOURCE_DIR}/external/check_and_apply_patch.cmake
    )
    SET(EIGEN_INCLUDE_DIRS ${EXT_INSTALL}/include/eigen3)
  SET(ares_DEPS ${ares_DEPS} eigen)
  SET(EIGEN_PATH ${EXT_INSTALL})

ELSE (INTERNAL_EIGEN)
    if(DEFINED EIGEN_PATH)
      set(_eigen_old_pkg_path $ENV{PKG_CONFIG_PATH})
      set(ENV{PKG_CONFIG_PATH} ${EIGEN_PATH}/share/pkgconfig)
    endif()
    pkg_check_modules(EIGEN NO_CMAKE_PATH NO_CMAKE_ENVIRONMENT_PATH REQUIRED eigen3)
    if(DEFINED EIGEN_PATH)
      set(ENV{PKG_CONFIG_PATH} ${_eigen_old_pkg_path})
    endif()
    IF (EIGEN_FOUND)
      IF(EIGEN_STATIC_INCLUDE_DIRS)
	SET(EIGEN_INCLUDE_DIRS ${EIGEN_STATIC_INCLUDE_DIRS})
      ENDIF()
    ELSE()
      message(FATAL_ERROR "Eigen has not been found")
    ENDIF()
ENDIF (INTERNAL_EIGEN)

################
# Build PyBind11
################

IF (BUILD_PYTHON_EXTENSION)
  SET(PYBIND11_URL "https://github.com/pybind/pybind11/archive/v2.10.3.tar.gz" CACHE STRING "URL to download Pybind11 from")
  mark_as_advanced(PYBIND11_URL)

  FetchContent_Declare(
     pybind11
     URL ${PYBIND11_URL}
     URL_HASH MD5=a093dac9dfd613a5a7c2afa50a301098
  )

ENDIF()

SET(R3D_URL "https://github.com/devonmpowell/r3d/archive/b3eef85ae5dc111d0148491772e0820406cfe0ea.zip" CACHE STRING "URL to download R3D from")
mark_as_advanced(R3D_URL)
FetchContent_Declare(
   r3d
   URL ${R3D_URL}
   URL_HASH MD5=9e3c4c7348805593539464aae149646a
)

################
# BUILD HDF5
################

if (INTERNAL_HDF5)
  SET(HDF5_URL "https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.7/src/hdf5-1.10.7.tar.gz" CACHE STRING "URL to download HDF5 from")
  mark_as_advanced(HDF5_URL)

  SET(HDF5_SOURCE_DIR ${BUILD_PREFIX}/hdf5-prefix/src/hdf5)
  SET(HDF5_BIN_DIR ${EXT_INSTALL})
  ExternalProject_Add(hdf5
    PREFIX ${BUILD_PREFIX}/hdf5-prefix
    URL ${HDF5_URL}
    URL_HASH MD5=006ed785942f4ed9a6f31556d0ef8ba5
    CMAKE_ARGS
      -DCMAKE_INSTALL_PREFIX=${EXT_INSTALL}
      -DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}
      -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}
      -DHDF5_BUILD_CPP_LIB=ON
      -DHDF5_BUILD_TOOLS=ON
      -DHDF5_BUILD_HL_LIB=ON
      BUILD_BYPRODUCTS ${EXT_INSTALL}/lib/libhdf5.a ${EXT_INSTALL}/lib/libhdf5-static.a ${EXT_INSTALL}/lib/libhdf5_cpp.a
  )
  SET(hdf5_built hdf5)
  set(HDF5_LIBRARIES ${HDF5_BIN_DIR}/lib/libhdf5.a CACHE STRING "HDF5 lib" FORCE)
  set(HDF5_CXX_LIBRARIES ${HDF5_BIN_DIR}/lib/libhdf5_cpp.a CACHE STRING "HDF5 C++ lib" FORCE)
  SET(HDF5_INCLUDE_DIR ${HDF5_BIN_DIR}/include CACHE STRING "HDF5 include path" FORCE)
  SET(CONFIGURE_LDFLAGS "${CONFIGURE_LDFLAGS} -L${HDF5_BIN_DIR}/lib")
  SET(HDF5_ROOTDIR ${HDF5_BIN_DIR})
  SET(ares_DEPS ${ares_DEPS} hdf5)
  mark_as_advanced(HDF5_LIBRARIES HDF5_CXX_LIBRARIES HDF5_INCLUDE_DIR)
else(INTERNAL_HDF5)
  mark_as_advanced(CLEAR HDF5_LIBRARIES HDF5_CXX_LIBRARIES HDF5_INCLUDE_DIR)
  find_package(HDF5 COMPONENTS CXX)
  SET(HDF5_ROOTDIR ${HDF5_BIN_DIR})
  SET(HDF5_INCLUDE_DIR ${HDF5_INCLUDE_DIRS})
endif (INTERNAL_HDF5)

##################
# Build GSL
##################

IF(INTERNAL_GSL)
  SET(GSL_URL "http://ftpmirror.gnu.org/gsl/gsl-2.3.tar.gz" CACHE STRING "URL to download GSL from ")
  mark_as_advanced(GSL_URL)

  SET(GSL_SOURCE_DIR ${BUILD_PREFIX}/gsl-prefix/src/gsl)
  ExternalProject_Add(gsl
    URL ${GSL_URL}
    PREFIX ${BUILD_PREFIX}/gsl-prefix
    CONFIGURE_COMMAND ${GSL_SOURCE_DIR}/configure
           --prefix=${EXT_INSTALL} --disable-shared
           --with-pic
           CPPFLAGS=${CONFIGURE_CPP_FLAGS} CC=${CMAKE_C_COMPILER} CXX=${CMAKE_CXX_COMPILER}
    BUILD_IN_SOURCE 1
    BUILD_BYPRODUCTS ${EXT_INSTALL}/lib/libgsl.a ${EXT_INSTALL}/lib/libgslcblas.a
  )
  SET(GSL_INTERNAL_LIBS ${EXT_INSTALL}/lib)
  SET(GSL_LIBRARY ${GSL_INTERNAL_LIBS}/libgsl.a CACHE STRING "GSL internal path" FORCE)
  SET(GSL_CBLAS_LIBRARY ${GSL_INTERNAL_LIBS}/libgslcblas.a CACHE STRING "GSL internal path" FORCE)
  set(GSL_INCLUDE ${CMAKE_BINARY_DIR}/ext_install/include CACHE STRING "GSL internal path" FORCE)
  SET(ares_DEPS ${ares_DEPS} gsl)
  mark_as_advanced(GSL_LIBRARY GSL_INCLUDE GSL_CBLAS_LIBRARY)
ELSE(INTERNAL_GSL)
  mark_as_advanced(CLEAR GSL_LIBRARY GSL_INCLUDE GSL_CBLAS_LIBRARY)
  find_library(GSL_LIBRARY gsl)
  find_library(GSL_CBLAS_LIBRARY gslcblas)
  find_path(GSL_INCLUDE NAMES gsl/gsl_blas.h)
  message(STATUS "GSL paths: ${GSL_LIBRARY} ${GSL_CBLAS_LIBRARY} ${GSL_INCLUDE}")
  if (NOT (GSL_LIBRARY OR GSL_CBLAS_LIBRARY OR GSL_INCLUDE))
    message(FATAL_ERROR "GSL has not been found")
  endif()
ENDIF(INTERNAL_GSL)


#############
# Build FFTW
#############

IF(INTERNAL_FFTW)
  SET(FFTW_URL "http://www.fftw.org/fftw-3.3.8.tar.gz" CACHE STRING "URL to download FFTW from")
  mark_as_advanced(FFTW_URL)

	SET(EXTRA_FFTW_CONF)
#	IF(HAVE_SSE)
#		SET(EXTRA_FFTW_CONF ${EXTRA_FFTW_CONF} --enable-sse)
#	ENDIF(HAVE_SSE)
#	IF(HAVE_SSE2)
#		SET(EXTRA_FFTW_CONF ${EXTRA_FFTW_CONF} --enable-sse2)
#	ENDIF(HAVE_SSE2)
#	IF(HAVE_AVX)
#		SET(EXTRA_FFTW_CONF ${EXTRA_FFTW_CONF} --enable-avx)
#	ENDIF(HAVE_AVX)
   IF(ENABLE_OPENMP)
     SET(EXTRA_FFTW_CONF ${EXTRA_FFTW_CONF} --enable-openmp)
     SET(FFTW_LIBS ${FFTW_LIBS} ${EXT_INSTALL}/lib/libfftw3_omp.a )
   ENDIF(ENABLE_OPENMP)
   IF (ENABLE_MPI)
    SET(MPI_OPT ${EXTRA_FFTW_CONF} --enable-mpi MPICC=${MPI_C_COMPILER})
    SET(FFTW_LIBS ${FFTW_LIBS} ${EXT_INSTALL}/lib/libfftw3_mpi.a )
   ENDIF(ENABLE_MPI)

   SET(EXTRA_FFTW_CONF ${EXTRA_FFTW_CONF} "CC=${CMAKE_C_COMPILER}" "CXX=${CMAKE_CXX_COMPILER}")
    IF(BUILD_PYTHON_EXTENSION)
      SET(EXTRA_FFTW_CONF ${EXTRA_FFTW_CONF} "--with-pic")
    ENDIF()
    SET(FFTW_SOURCE ${BUILD_PREFIX}/fftw-prefix/src/fftw)
    message(STATUS "Opts: ${EXTRA_FFTW_CONF}")
    ExternalProject_Add(fftw
        URL ${FFTW_URL}
        URL_HASH MD5=8aac833c943d8e90d51b697b27d4384d
        PREFIX ${BUILD_PREFIX}/fftw-prefix
        CONFIGURE_COMMAND
           ${FFTW_SOURCE}/configure
                 --prefix=${EXT_INSTALL}
                ${EXTRA_FFTW_CONF} --disable-shared ${MPI_OPT}
        BUILD_BYPRODUCTS ${FFTW_LIBS} ${EXT_INSTALL}/lib/libfftw3.a
    )
    SET(FFTW_INCLUDE_DIR ${EXT_INSTALL}/include)
    SET(FFTW_OMP_LIBRARIES ${EXT_INSTALL}/lib/libfftw3_omp.a)
    SET(FFTW_LIBRARIES ${EXT_INSTALL}/lib/libfftw3.a)
    SET(FFTW_MPI_LIBRARIES ${EXT_INSTALL}/lib/libfftw3_mpi.a)
    SET(ares_DEPS ${ares_DEPS} fftw)
ELSE(INTERNAL_FFTW)

    set(FFTW_OMP_FIND_REQUIRED ${ENABLE_OPENMP})
    SET(FFTW_NAMES fftw3)
    set(FFTW_FIND_REQUIRED YES)
    IF(ENABLE_MPI)
      set(FFTW_MPI_FIND_REQUIRED YES)
    ENDIF()
    IF(ENABLE_OPENMP)
      set(FFTW_OMP_FIND_REQUIRED YES)
    ENDIF()
    include(${CMAKE_SOURCE_DIR}/cmake/FindFFTW.cmake)
ENDIF(INTERNAL_FFTW)

IF(ENABLE_OPENMP)
  SET(FFTW_LIBRARIES ${FFTW_OMP_LIBRARIES} ${FFTW_LIBRARIES})
ENDIF(ENABLE_OPENMP)

IF(ENABLE_MPI)
  SET(FFTW_LIBRARIES ${FFTW_MPI_LIBRARIES} ${FFTW_LIBRARIES})
ENDIF(ENABLE_MPI)

MESSAGE(STATUS "Used FFTW libraries: ${FFTW_LIBRARIES}")

SET(COSMOTOOL_DIR ${CMAKE_SOURCE_DIR}/external/cosmotool)

#MESSAGE(STATUS "Cosmotool deps is ${ares_DEPS}")
SET(SPECIAL_PREFIX_PATH ${CMAKE_PREFIX_PATH})
list(INSERT SPECIAL_PREFIX_PATH 0 ${EXT_INSTALL})
ExternalProject_Add(cosmotool
  DEPENDS ${ares_DEPS}
  SOURCE_DIR ${COSMOTOOL_DIR}
  PREFIX ${BUILD_PREFIX}/cosmotool-prefix
  CMAKE_CACHE_ARGS
    -DCMAKE_INSTALL_PREFIX:STRING=${EXT_INSTALL}
    -DCMAKE_PREFIX_PATH:STRING=${SPECIAL_PREFIX_PATH}
    -DEIGEN_PATH:STRING=${EIGEN_PATH}
    -DCMAKE_MODULE_PATH:STRING=${EXT_INSTALL}/share/cmake;${CMAKE_MODULE_PATH}
    -DCMAKE_C_COMPILER:STRING=${CMAKE_C_COMPILER}
    -DCMAKE_CXX_COMPILER:STRING=${CMAKE_CXX_COMPILER}
    -DHDF5_DIR:STRING=${HDF5_ROOTDIR}/share/cmake
    -DHDF5_ROOTDIR:STRING=${HDF5_ROOTDIR}
    -DNETCDF_INCLUDE_PATH:STRING=${NETCDF_INCLUDE_PATH}
    -DNETCDFCPP_INCLUDE_PATH:STRING=${NETCDFCPP_INCLUDE_PATH}
    -DGSL_INCLUDE_PATH:STRING=${GSL_INCLUDE}
    -DGSL_LIBRARY:STRING=${GSL_LIBRARY}
    -DGSLCBLAS_LIBRARY:STRING=${GSL_CBLAS_LIBRARY}
    -DINTERNAL_GSL:BOOL=OFF
    -DINTERNAL_EIGEN:BOOL=OFF
    -DYORICK_SUPPORT:BOOL=OFF
    -DBUILD_PYTHON:BOOL=OFF
    -DENABLE_OPENMP:BOOL=${ENABLE_OPENMP}
    -DPKG_CONFIG_USE_CMAKE_PREFIX_PATH:BOOL=ON
    -DBOOST_INCLUDEDIR:STRING=${Boost_INCLUDE_DIRS}
    -DZLIB_LIBRARY:STRING=${ZLIB_LIBRARY}
    "-DCMAKE_INSTALL_DEFAULT_DIRECTORY_PERMISSIONS:STRING=${CMAKE_INSTALL_DEFAULT_DIRECTORY_PERMISSIONS}"
  BUILD_BYPRODUCTS ${EXT_INSTALL}/lib/libCosmoTool.a
  LIST_SEPARATOR ;
)

SET(COSMOTOOL_LIB ${EXT_INSTALL}/lib/libCosmoTool.a)
set(COSMOTOOL_INCLUDE ${EXT_INSTALL}/include)
SET(ares_DEPS ${ares_DEPS} cosmotool)


### CLASS

SET(CLASS_CODE_URL "https://github.com/lesgourg/class_public/archive/refs/tags/v2.9.4.tar.gz" CACHE STRING "URL for CLASS")

SET(LIBCLASS_PATH ${BUILD_PREFIX}/class-code-prefix/src/class_code/libclass.a)

IF(CMAKE_CXX_COMPILER_ID MATCHES "^Intel$")
   SET(COMPILER_EXTRA_FLAGS "-fPIC")
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
   if (${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
   else()
     SET(COMPILER_EXTRA_FLAGS "-fPIC")
   endif()
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "AppleClang")
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
endif()

if (ENABLE_OPENMP)
  SET(CLASS_OPENMP ${OpenMP_C_FLAGS})
else()
  SET(CLASS_OPENMP)
endif()

ExternalProject_Add(class_code
  PREFIX ${BUILD_PREFIX}/class-code-prefix
  URL ${CLASS_CODE_URL}
  URL_HASH SHA1=ad0c7739d23cdd04263f0030120d159f3b4e5b6e
  CONFIGURE_COMMAND echo "No configure"
  BUILD_COMMAND make CPPFLAGS=${CONFIGURE_CPP_FLAGS} CC=${CMAKE_C_COMPILER} CXX=${CMAKE_CXX_COMPILER} "CCFLAG=-D__CLASSDIR__=\\\"${BUILD_PREFIX}/class-code-prefix/src/class_code\\\" ${COMPILER_EXTRA_FLAGS} ${CMAKE_C_FLAGS} ${CMAKE_C_FLAGS_${CMAKE_BUILD_TYPE}}" OPTFLAG= OMPFLAG=${CLASS_OPENMP} libclass.a
  INSTALL_COMMAND
      ${CMAKE_COMMAND}
           -DCLASS_SOURCE_INCLUDE=${BUILD_PREFIX}/class-code-prefix/src/class_code/include
           -DCLASS_HEADER_INSTALL_PATH=${EXT_INSTALL}/include/class_code
           -P ${CMAKE_SOURCE_DIR}/external/install_class.cmake
  BUILD_IN_SOURCE 1
  BUILD_BYPRODUCTS ${LIBCLASS_PATH}
)

SET(ares_DEPS ${ares_DEPS} class_code)
