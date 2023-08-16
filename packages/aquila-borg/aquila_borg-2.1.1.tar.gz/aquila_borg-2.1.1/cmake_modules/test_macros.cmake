SET(TEST_DIR ${CMAKE_BINARY_DIR}/_test_dir)

execute_process(COMMAND ${CMAKE_COMMAND} -E make_directory ${TEST_DIR})

macro(ADD_FAILING_TEST NAME SOURCE_FILE )
    set(NAME_BIN ${NAME}.exe)
    
    add_executable(${NAME_BIN} ${SOURCE_FILE})
    
    set_target_properties(${NAME_BIN} PROPERTIES
                      EXCLUDE_FROM_ALL TRUE
                      EXCLUDE_FROM_DEFAULT_BUILD TRUE)

    add_test(NAME ${NAME}
             COMMAND ${CMAKE_COMMAND} --build . --target ${NAME_BIN} --config $<CONFIGURATION>
             WORKING_DIRECTORY ${CMAKE_BINARY_DIR})

    set_tests_properties(${NAME} PROPERTIES WILL_FAIL TRUE)
endmacro()

macro(add_test_to_run NAME bin)
    add_test(NAME ${NAME} COMMAND ${CMAKE_CURRENT_BINARY_DIR}/${bin} WORKING_DIRECTORY ${TEST_DIR})
endmacro()

macro(add_direct_test NAME SOURCE_FILE)
    set(NAME_BIN ${NAME}_exe)
    
    add_executable(${NAME_BIN} ${SOURCE_FILE})
    target_link_libraries(${NAME_BIN} test_library_LSS LSS ${LIBS})

    add_test(NAME ${NAME} COMMAND ${CMAKE_CURRENT_BINARY_DIR}/${NAME_BIN} WORKING_DIRECTORY ${TEST_DIR})
endmacro()

macro(add_check_output_test NAME SOURCE_FILE ARG)
    set(NAME_BIN ${NAME}_exe)
    
    add_executable(${NAME_BIN} ${SOURCE_FILE})
    target_link_libraries(${NAME_BIN} test_library_LSS LSS ${LIBS})

    # The output must match
    add_test(NAME ${NAME_BIN}.output
             COMMAND ${CMAKE_COMMAND} 
                -D test_cmd=${CMAKE_CURRENT_BINARY_DIR}/${NAME_BIN}
                -D test_args:string=${ARG}
                -D output_blessed=${SOURCE_FILE}.expected
                -D output_test=${TEST_DIR}/${NAME_BIN}.out
                -P ${CMAKE_SOURCE_DIR}/cmake_modules/run_test.cmake
             WORKING_DIRECTORY ${TEST_DIR})

endmacro()

