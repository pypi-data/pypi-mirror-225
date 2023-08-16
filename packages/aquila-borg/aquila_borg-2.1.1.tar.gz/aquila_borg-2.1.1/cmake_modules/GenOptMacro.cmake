
find_program(GENGETOPT gengetopt)


macro(add_genopt _sourcelist _ggofile _basefile)

  unset(_structname)
  unset(_funcname)

  if(NOT EXISTS ${CMAKE_CURRENT_BINARY_DIR}/${_ggofile})
    set(_ggofile2 ${CMAKE_CURRENT_SOURCE_DIR}/${_ggofile})
  else(NOT EXISTS ${CMAKE_CURRENT_BINARY_DIR}/${_ggofile})
    set(_ggofile2 ${CMAKE_CURRENT_BINARY_DIR}/${_ggofile})
  endif(NOT EXISTS ${CMAKE_CURRENT_BINARY_DIR}/${_ggofile})

  set(_add_depends "")

  SET(USE_PREBUILT_IF_NECESSARY OFF)
  foreach(arg ${ARGN})
    if ("x${arg}" MATCHES "^x(STRUCTNAME|FUNCNAME|DEPENDS|PREBUILT_C|PREBUILT_H)$")
      SET(doing "${arg}")
    elseif(doing STREQUAL "STRUCTNAME")
      SET(_structname ${arg})
      unset(doing)
    elseif(doing STREQUAL "FUNCNAME")
      SET(_funcname ${arg})
      unset(doing)
    elseif(doing STREQUAL "DEPENDS")
      SET(_add_depends ${_add_depends} ${arg})
    elseif(doing STREQUAL "PREBUILT_C")
      SET(USE_PREBUILT_IF_NECESSARY ON)
      SET(_prebuilt_c ${arg})
    elseif(doing STREQUAL "PREBUILT_H")
      SET(USE_PREBUILT_IF_NECESSARY ON)
      SET(_prebuilt_h ${arg})
    endif()
  endforeach(arg ${ARGN})

  if(NOT DEFINED _structname)
    set(_structname ${_basefile})
  endif(NOT DEFINED _structname)

  if(NOT DEFINED _funcname)
    set(_funcname ${_basefile})
  endif(NOT DEFINED _funcname)
  
  set(_cfile ${CMAKE_CURRENT_BINARY_DIR}/${_basefile}.c)
  set(_hfile ${CMAKE_CURRENT_BINARY_DIR}/${_basefile}.h)

  include_directories(${CMAKE_CURRENT_BINARY_DIR})

  IF(GENGETOPT)
    add_custom_command(
      OUTPUT ${_cfile} ${_hfile}
      COMMAND ${GENGETOPT} -i ${_ggofile2} -f ${_funcname} -a ${_structname} -F ${_basefile} -C
      DEPENDS ${_ggofile2} ${_add_depends}
    )
  ELSE(GENGETOPT)
    IF(NOT USE_PREBUILT_IF_NECESSARY)
      message(FATAL_ERROR "Gengetopt has not been found and is required to build intermediate files")
    ELSE(NOT USE_PREBUILT_IF_NECESSARY)
      message(WARNING "Using prebuilt configuration parser")
      configure_file(${_prebuilt_c} ${_cfile} COPYONLY)
      configure_file(${_prebuilt_h} ${_hfile} COPYONLY)
    ENDIF(NOT USE_PREBUILT_IF_NECESSARY)
  ENDIF(GENGETOPT)

  set(${_sourcelist} ${_cfile} ${${_sourcelist}})  

endmacro(add_genopt)
