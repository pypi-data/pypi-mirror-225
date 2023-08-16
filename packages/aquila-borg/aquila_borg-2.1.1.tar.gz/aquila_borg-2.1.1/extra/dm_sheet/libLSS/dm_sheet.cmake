SET(EXTRA_DM_SHEET ${CMAKE_SOURCE_DIR}/extra/dm_sheet)

SET(EXTRA_LIBLSS ${EXTRA_LIBLSS}
        ${EXTRA_DM_SHEET}/libLSS/physics/dm_sheet/dm_sheet.cpp
        ${EXTRA_DM_SHEET}/libLSS/physics/velocity/velocity_sic.cpp
)
