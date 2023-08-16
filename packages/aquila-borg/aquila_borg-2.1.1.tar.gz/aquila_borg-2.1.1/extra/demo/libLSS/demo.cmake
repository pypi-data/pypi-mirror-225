cmessage(CWARNING "This is the demonstration module")

SET(EXTRA_DEMO ${CMAKE_SOURCE_DIR}/extra/demo)

SET(EXTRA_LIBLSS ${EXTRA_LIBLSS}
	${EXTRA_DEMO}/libLSS/demo/demo.cpp
)
