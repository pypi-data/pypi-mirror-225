#+
#   ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/tests/test_julia.jl
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
module TestLikelihood
    using ..libLSS
    import ..libLSS.State, ..libLSS.GhostPlanes, ..libLSS.get_ghost_plane
    import ..libLSS.print, ..libLSS.LOG_INFO, ..libLSS.LOG_VERBOSE, ..libLSS.LOG_DEBUG
    import ..libLSS.BadGradient

    function initialize(state::State)
        print(LOG_VERBOSE, "Likelihood initialization in Julia")
#        bias = libLSS.resize_array(state, "galaxy_bias_0", 1, Float64)
#        bias[1] = 1

    end


    function get_required_planes(state::State)
        return Array{UInt64,1}([])
    end

    function likelihood(state::State, ghosts::GhostPlanes, array::AbstractArray{Float64,3})
        print(LOG_DEBUG, "my likelihood")
        return 0
    end

    function get_step_hint(state, catalog_id, bias_id)
        print(LOG_DEBUG, "get_step_hint")
        return 0.1
    end

    function log_prior_bias(state, catalog_id, bias_tilde)
        print(LOG_DEBUG, "log_prior_bias")
        # Change of variable bias = exp(bias_tilde)
        return sum(bias_tilde.^2)
    end

    function generate_mock_data(state::State, ghosts::GhostPlanes, array)
    end

    function likelihood_bias(state::State, ghosts::GhostPlanes, array, catalog_id, catalog_bias_tilde)
        return 0
    end

    function adjoint_gradient(state::State, array, ghosts, ag)
    end

   function adjoint_bias(state::State, ghosts::GhostPlanes,
        array, catalog_id, catalog_bias_tilde, adjoint_gradient_bias)
     print(LOG_DEBUG,"Entering ag bias")
     throw(BadGradient())
   end

end
