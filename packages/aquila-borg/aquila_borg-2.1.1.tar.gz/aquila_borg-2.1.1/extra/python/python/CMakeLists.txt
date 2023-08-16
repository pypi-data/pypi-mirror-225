IF (BUILD_PYTHON_EXTENSION)

function(add_pyborg_doc) 
	message(STATUS "Docfiles=${docfiles}" )
	file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/pyborg_doc)
	set(generated_headers)
	foreach(filename IN LISTS ARGV)
		STRING(REGEX REPLACE "^.*/([a-zA-Z0-9_\.]*)\\.rst\$"  ${CMAKE_CURRENT_BINARY_DIR}/pyborg_doc/\\1.hpp  filename_hpp ${filename})
		add_custom_command(
			OUTPUT ${filename_hpp} 
			COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/doc/convert.py ${CMAKE_CURRENT_BINARY_DIR}/pyborg_doc ${filename}
			DEPENDS ${filename}
		)
	        set(generated_headers ${generated_headers} ${filename_hpp})
	endforeach()
	target_sources(python_borg PRIVATE ${generated_headers})
endfunction()

message(STATUS "INCLUDE_PATH=${ARES_INCLUDE_PATH}")
include_directories(
	${CMAKE_BINARY_DIR} 
	${CMAKE_CURRENT_BINARY_DIR}
	${CMAKE_SOURCE_DIR}/extra/hades 
	${CMAKE_SOURCE_DIR}/extra/borg 
	${ARES_INCLUDE_PATH} ${HDF5_INCLUDE_DIR} ${EIGEN_INCLUDE_DIRS})
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

add_library(python_borg 
   base.cpp pycosmo.cpp pyforward.cpp pyforward_borg.cpp
   pybias.cpp pyforward_all.cpp bind.cpp pyvelocity.cpp pylikelihood.cpp
   pysamplers.cpp any_wrapper.cpp
)

set_property(TARGET python_borg PROPERTY POSITION_INDEPENDENT_CODE ON)
target_link_libraries(python_borg LSS ${DEP_LIBS} pybind11::module)

add_library(_borg MODULE
   _borg.cpp
)

target_link_libraries(_borg PRIVATE python_borg LSS ${DEP_LIBS} pybind11::module)
set_target_properties(_borg PROPERTIES PREFIX "${PYTHON_MODULE_PREFIX}" SUFFIX "${PYTHON_MODULE_EXTENSION}")
IF(NOT APPLE)
  target_link_options(_borg PRIVATE "LINKER:--version-script=${CMAKE_CURRENT_SOURCE_DIR}/_borg.version")
ENDIF()

file(GLOB PYBORG_DOC_FILE doc/*.rst)
add_pyborg_doc(${PYBORG_DOC_FILE})

#
# Scripting to install the python module at the correct place. By default we install in the local folder
#

# Discover where to put packages
if (NOT PYTHON_SITE_PACKAGES)
  execute_process (
     COMMAND ${PYTHON_EXECUTABLE} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())" 
     OUTPUT_VARIABLE internal_PYTHON_SITE_PACKAGES
     OUTPUT_STRIP_TRAILING_WHITESPACE
  )
  SET(SYSTEM_PYTHON_SITE_PACKAGES 
     ${internal_PYTHON_SITE_PACKAGES} 
     CACHE PATH "Path to the target system-wide site-package where to install python modules")

  execute_process (
     COMMAND ${PYTHON_EXECUTABLE} -c "from site import USER_SITE; print(USER_SITE)" 
     OUTPUT_VARIABLE internal_PYTHON_SITE_PACKAGES 
     OUTPUT_STRIP_TRAILING_WHITESPACE
  )
  SET(USER_PYTHON_SITE_PACKAGES
     ${internal_PYTHON_SITE_PACKAGES}
     CACHE PATH "Path to the target user site-package where to install python modules")

  mark_as_advanced(USER_PYTHON_SITE_PACKAGES SYSTEM_PYTHON_SITE_PACKAGES)
endif (NOT PYTHON_SITE_PACKAGES)

message(STATUS "System python site: ${SYSTEM_PYTHON_SITE_PACKAGES}")
message(STATUS "User python site: ${USER_PYTHON_SITE_PACKAGES}")


OPTION(INSTALL_PYTHON_LOCAL "Indicates the destination of the Python installation: User or System" ON)

IF (NOT PYTHON_SITE_PACKAGES)
  IF (NOT INSTALL_PYTHON_LOCAL)
    SET(PYTHON_SITE_PACKAGES ${SYSTEM_PYTHON_SITE_PACKAGES})
  ELSE (NOT INSTALL_PYTHON_LOCAL)
    SET(PYTHON_SITE_PACKAGES ${USER_PYTHON_SITE_PACKAGES})
  ENDIF(NOT INSTALL_PYTHON_LOCAL)
ENDIF()
cmessage(STATUS "Python install location: ${PYTHON_SITE_PACKAGES}")


INSTALL(TARGETS
  _borg
  LIBRARY DESTINATION ${PYTHON_SITE_PACKAGES}/aquila_borg
)

OPTION(INSTALL_COMPATIBILITY_PYBORG "Install the borg package as a compatibility package to aquila_borg (conflict with borgbackup)" ON)
IF(INSTALL_COMPATIBILITY_PYBORG)
  INSTALL(DIRECTORY borg DESTINATION ${PYTHON_SITE_PACKAGES}
          FILES_MATCHING PATTERN "*.py")
ENDIF()
INSTALL(DIRECTORY aquila_borg DESTINATION ${PYTHON_SITE_PACKAGES}
        FILES_MATCHING PATTERN "*.py")

ENDIF()
