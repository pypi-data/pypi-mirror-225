macro(hades_register_forward_models)

    SET(_ALL_MODELS ${CMAKE_BINARY_DIR}/libLSS/physics/forwards/all_models.hpp)
    get_property(_init GLOBAL PROPERTY HADES_FORWARD_MODEL_INIT)
    if (NOT _init)
        file(WRITE ${_ALL_MODELS} "#pragma once\n")
        set_property(GLOBAL PROPERTY  HADES_FORWARD_MODEL_INIT 1)
    endif()
    foreach(model_header ${ARGN})
        cmessage(STATUS "Registering forward model ${model_header}")
        file(APPEND ${_ALL_MODELS} "#include \"${model_header}\"\n")
    endforeach()

endmacro()