find_program(CLANG_FORMAT clang-format)

function(setup_formatter MODULES)

  if(CLANG_FORMAT)

    SET(_glob_pattern
      ${CMAKE_SOURCE_DIR}/libLSS/*.cpp
      ${CMAKE_SOURCE_DIR}/libLSS/*.hpp
    )
    foreach(module IN LISTS ${MODULES})
      set(_glob_module
        ${CMAKE_SOURCE_DIR}/extra/${module}/libLSS/*.cpp
        ${CMAKE_SOURCE_DIR}/extra/${module}/libLSS/*.hpp
      )
      SET(_glob_pattern ${_glob_pattern} ${_glob_module})

      file(GLOB_RECURSE module_sources ${_glob_module})
      add_custom_target(clangformat-${module}
        COMMAND ${CLANG_FORMAT} -style=file -i ${module_sources}
      )
    endforeach()

    file(GLOB_RECURSE ALL_SOURCE_FILES ${_glob_pattern})

    add_custom_target(clangformat
      COMMAND ${CLANG_FORMAT} -style=file -i ${ALL_SOURCE_FILES}
    )

  endif()

endfunction()
