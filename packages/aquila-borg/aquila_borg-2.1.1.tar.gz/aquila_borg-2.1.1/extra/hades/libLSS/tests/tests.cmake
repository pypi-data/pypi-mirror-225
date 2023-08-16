SET(EXTRA_HADES ${CMAKE_SOURCE_DIR}/extra/hades/libLSS/tests)

set(TEST_LIBRARY_SOURCES ${EXTRA_HADES}/setup_hades_test_run.cpp)

include_directories(${EXTRA_HADES})

SET(TEST_hades_LIST symplectic modelio hermiticity ghost_array )

include(${CMAKE_SOURCE_DIR}/extra/hades/scripts/gradient_tests.cmake)

hades_add_gradient_test(hades_gradients ${EXTRA_HADES}/hades_gradients.py_config)

add_test(NAME modelio COMMAND ${CURRENT_CMAKE_BINARY_DIR}/test_modelio)
