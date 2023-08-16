

function(hades_add_forward_test testnames testbase)
	set(_forward_test_cmake ${CMAKE_BINARY_DIR}/CMakeFiles/hades_forward-test_${testnames}.cmake)
	set(_base_tmp_forward_files ${CMAKE_BINARY_DIR}/CMakeFiles/forward_tests)

	if (NOT EXISTS ${_base_tmp_forward_files})
		FILE(MAKE_DIRECTORY ${_base_tmp_forward_files})
	endif()

	execute_process(
		COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_SOURCE_DIR}/extra/hades/scripts/generate_tests_forward_models_cmake.py
		 	${_forward_test_cmake} ${testbase} ${_base_tmp_forward_files}
			RESULT_VARIABLE _generate_result)
	if (NOT _generate_result EQUAL 0)
		cmessage(FATAL_ERROR "Could not automatically generate gradient tests.")
	endif()

	include(${_forward_test_cmake})
endfunction()

function(hades_add_gradient_test testnames testbase)
	set(_gradient_test_cmake ${CMAKE_BINARY_DIR}/CMakeFiles/hades_gradient_test_${testnames}.cmake)
	set(_benchmark_gradient_test_cmake ${CMAKE_BINARY_DIR}/CMakeFiles/hades_gradient_benchmark_test_${testnames}.cmake)
	set(_base_tmp_gradient_files ${CMAKE_BINARY_DIR}/CMakeFiles/gradient_tests)

	if (NOT EXISTS ${_base_tmp_gradient_files})
		FILE(MAKE_DIRECTORY ${_base_tmp_gradient_files})
	endif()

	execute_process(COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_SOURCE_DIR}/extra/hades/scripts/generate_tests_cmake.py
		 ${_gradient_test_cmake} ${testbase} ${_base_tmp_gradient_files} RESULT_VARIABLE _generate_result)
	 if (NOT _generate_result EQUAL 0)
		cmessage(FATAL_ERROR "Could not automatically generate gradient tests.")
	endif()

	execute_process(COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_SOURCE_DIR}/extra/hades/scripts/generate_benchmark_tests.py
	${_benchmark_gradient_test_cmake} ${testbase} ${_base_tmp_gradient_files} RESULT_VARIABLE _generate_result)
  if (NOT _generate_result EQUAL 0)
		cmessage(FATAL_ERROR "Could not automatically generate gradient tests.")
	endif()

	include(${_gradient_test_cmake})
	include(${_benchmark_gradient_test_cmake})
endfunction()
