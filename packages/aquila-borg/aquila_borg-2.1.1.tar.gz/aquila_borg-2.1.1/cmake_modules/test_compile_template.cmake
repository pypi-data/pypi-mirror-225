include_directories(@TEST_INCLUDE_DIRS@)
try_compile(COMPILE_SUCCEEDED 
	 ${CMAKE_BINARY_DIR}/compile_tests 
	 @COMPILE_SOURCE@
)

if(COMPILE_SUCCEEDED)
  message("Success!")
else()
endif()
