require_ares_module(hades)

SET(EXTRA_HMCLET ${CMAKE_SOURCE_DIR}/extra/hmclet)
SET(EXTRA_LIBLSS
   ${EXTRA_LIBLSS}
   ${EXTRA_HMCLET}/libLSS/hmclet/hmclet.cpp
   ${EXTRA_HMCLET}/libLSS/hmclet/hmclet_qnhmc.cpp
   ${EXTRA_HMCLET}/libLSS/hmclet/diagonal_mass.cpp
   ${EXTRA_HMCLET}/libLSS/hmclet/mass_burnin.cpp
   ${EXTRA_HMCLET}/libLSS/hmclet/dense_mass.cpp
)

IF(BUILD_JULIA)
  SET(EXTRA_LIBLSS
    ${EXTRA_LIBLSS}
    ${EXTRA_HMCLET}/libLSS/hmclet/julia_slice.cpp
    ${EXTRA_HMCLET}/libLSS/hmclet/julia_hmclet.cpp
  )
ENDIF()
