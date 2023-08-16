#+
#   ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/tests/network/TF_likelihood.jl
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
module network
    using libLSS

    import libLSS.State
    import libLSS.GhostPlanes, libLSS.get_ghost_plane
    import libLSS.print, libLSS.LOG_INFO, libLSS.LOG_VERBOSE, libLSS.LOG_DEBUG

    using TensorFlow

    sess = Session(Graph())
    p = nothing
    new_p = nothing
    assign_p = nothing
    δ = nothing
    g = nothing
    s = nothing
    mask = nothing
    loss = nothing
    adgrad = nothing
    wgrad = nothing

    function setup(N0, number_of_parameters)
        global p, new_p, assign_p, δ, g, s, mask, loss, adgrad, wgrad
        p = Variable(zeros(number_of_parameters))
        new_p = placeholder(Float64, shape = [number_of_parameters])
        assign_p = assign(p, new_p)
        δ = placeholder(Float64, shape = [N0, N0, N0])
        g = placeholder(Float64, shape = [N0, N0, N0])
        s = placeholder(Float64, shape = [N0, N0, N0])
        mask = placeholder(Bool, shape = [N0, N0, N0])
        loss = 0.5 * sum((boolean_mask(reshape(g, N0^3), reshape(mask, N0^3)) .- boolean_mask(reshape(s, N0^3), reshape(mask, N0^3)) .* (1. .- p[1] .* boolean_mask(reshape(δ, N0^3), reshape(mask, N0^3)))).^2. ./(boolean_mask(reshape(s, N0^3), reshape(mask, N0^3)) .* p[2])) + 0.5 * sum(cast(mask, Float64)) .* log(p[2])
        adgrad = gradients(loss, δ)
        wgrad_slice = gradients(loss, p)
        wgrad = [wgrad_slice.values, wgrad_slice.indices]
    end

    function initialize(state::State)
        print(LOG_INFO, "Likelihood initialization in Julia")

        number_of_parameters = 2
        N0 = libLSS.get(state, "N0", Int64, synchronous=true)
        NCAT = libLSS.get(state, "NCAT", Int64, synchronous=true)
        setup(N0, number_of_parameters)
        run(sess, global_variables_initializer())
        print(LOG_VERBOSE, "Found " *repr(NCAT) * " catalogues")
        bias = libLSS.resize_array(state, "galaxy_bias_0", number_of_parameters, Float64)
        bias[:] = 1
        run(sess, assign_p, Dict(new_p=>bias))
    end

    function get_required_planes(state::State)
        print(LOG_INFO, "Check required planes")
        return Array{UInt64,1}([])
    end

    function likelihood(state::State, ghosts::GhostPlanes, array::AbstractArray{Float64,3})
        print(LOG_INFO, "Likelihood evaluation in Julia")
        NCAT = libLSS.get(state, "NCAT", Int64, synchronous=true)
        L = Float64(0.)
        for catalog=1:NCAT
            sc = repr(catalog - 1)
            run(sess, assign_p, Dict(new_p=>libLSS.get_array_1d(state, "galaxy_bias_"*sc, Float64)))
            L += run(sess, loss, Dict(δ=>array, g=>libLSS.get_array_3d(state, "galaxy_data_"*sc, Float64), s=>libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64), mask=>libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64).>0.))
        end

        print(LOG_VERBOSE, "Likelihood is " * repr(L))
        return L
    end

    function generate_mock_data(state::State, ghosts::GhostPlanes, array::AbstractArray{Float64,3})
        print(LOG_INFO, "Generate mock")

        sc = "0"
        data = libLSS.get_array_3d(state, "galaxy_data_"*sc, Float64)
        b = libLSS.get_array_1d(state, "galaxy_bias_"*sc, Float64)
        S = libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64)
        s = size(data)
        print(LOG_INFO, "Shape is " * repr(size(data)) * " and " * repr(size(array)))
        print(LOG_INFO, "Number of threads " * repr(Threads.nthreads()))
        N0=s[1]
        N1=s[2]
        N2=s[3]
        noise = sqrt(b[1])
        print(LOG_INFO, "Noise is " * repr(noise))
        bias = b[2]
        for i=1:N0,j=1:N1,k=1:N2
          data[i,j,k] = S[i,j,k]*(1+bias*array[i,j,k]) + sqrt(S[i,j,k])*noise*libLSS.gaussian(state)
        end

        print(LOG_INFO, "Max val is " * repr(maximum(array)) * " and data " * repr(maximum(data)))
    end

    function adjoint_gradient(state::State, array::AbstractArray{Float64,3}, ghosts::GhostPlanes, ag::AbstractArray{Float64,3})
        print(LOG_VERBOSE, "Adjoint gradient in Julia")
        NCAT = libLSS.get(state, "NCAT", Int64, synchronous=true)
        ag[:,:,:] = 0
        for catalog=1:NCAT
            sc = repr(catalog - 1)
            run(sess, assign_p, Dict(new_p=>libLSS.get_array_1d(state, "galaxy_bias_"*sc, Float64)))
            Smask = libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64).>0.
            ag[Smask] += run(sess, adgrad, Dict(δ=>array, g=>libLSS.get_array_3d(state, "galaxy_data_"*sc, Float64), s=>libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64), mask=>Smask))[Smask]
        end
    end

    function likelihood_bias(state::State, ghosts::GhostPlanes, array, catalog_id, catalog_bias)
        sc = repr(catalog_id)
        run(sess, assign_p, Dict(new_p=>catalog_bias))
        return run(sess, loss, Dict(δ=>array, g=>libLSS.get_array_3d(state, "galaxy_data_"*sc, Float64), s=>libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64), mask=>libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64).>0.))
    end

    function get_step_hint(state, catalog_id)
        return 0.1
    end

    function log_prior_bias(state, catalog_id, bias)
        if bias[2] < 0
          return Inf
        end
        return 0
    end

    function adjoint_bias(state::State, ghosts::GhostPlanes,
        array, catalog_id, catalog_bias, adjoint_gradient_bias)
        sc = repr(catalog_id)
        run(sess, assign_p, Dict(new_p=>catalog_bias))
        error = run(sess, wgrad, Dict(δ=>array, g=>libLSS.get_array_3d(state, "galaxy_data_"*sc, Float64), s=>libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64), mask=>libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64).>0.))
        for i=1:number_of_parameters
            adjoint_gradient_bias[i] = sum(error[1][error[2] .== i])
        end
    end
end
