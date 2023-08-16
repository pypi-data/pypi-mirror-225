function(borg_add_vobs_test testnames testbase)
	set(_vobs_test_cmake ${CMAKE_BINARY_DIR}/CMakeFiles/borg_vobs_test_${testnames}.cmake)
	set(_base_tmp_vobs_files ${CMAKE_BINARY_DIR}/CMakeFiles/vobs_tests)

	if (NOT EXISTS ${_base_tmp_vobs_files})
		FILE(MAKE_DIRECTORY ${_base_tmp_vobs_files})
	endif()

	execute_process(COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_SOURCE_DIR}/extra/borg/scripts/generate_vobs_tests.py
    ${_vobs_test_cmake} ${testbase} ${_base_tmp_vobs_files} RESULT_VARIABLE _generate_result)
  if (NOT _generate_result EQUAL 0)
		cmessage(FATAL_ERROR "Could not automatically generate vobs tests.")
	endif()

	include(${_vobs_test_cmake})
endfunction()
