#+
#   ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/tests/network/TF_conv.jl
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
    #new_p = nothing
    #assign_p = nothing
    δ = nothing
    g = nothing
    s = nothing
    mask = nothing
    output = nothing
    mock = nothing
    loss = nothing
    adgrad = nothing
    wgrad = nothing

    function setup(N0, number_of_parameters)
        global p, new_p, assign_p, δ, g, s, mask, output, mock, loss, adgrad, wgrad
        p = Array{Any}(number_of_parameters)
        #new_p = Array{Any}(number_of_parameters)
        #assign_p = Array{Any}(number_of_parameters)
        for i=1:number_of_parameters
            p[i] = placeholder(Float64, shape = [])
            #p[i] = Variable(zeros(Float64, 1))
            #new_p[i] = placeholder(Float64, shape = [])
            #assign_p[i] = assign(p[i], expand_dims(new_p[i], 1))
        end
        δ = placeholder(Float64, shape = [N0, N0, N0])
        g = placeholder(Float64, shape = [N0, N0, N0])
        s = placeholder(Float64, shape = [N0, N0, N0])
        mask = placeholder(Bool, shape = [N0, N0, N0])
        output = build_network(δ, p)
        mock = output .* s
        loss = 0.5 * sum((boolean_mask(reshape(g, N0^3), reshape(mask, N0^3)) .- boolean_mask(reshape(s, N0^3), reshape(mask, N0^3)) .* boolean_mask(reshape(output, N0^3), reshape(mask, N0^3))).^2. ./(boolean_mask(reshape(s, N0^3), reshape(mask, N0^3)))) + 0.5 * sum(cast(mask, Float64))
        adgrad = gradients(loss, δ)
        wgrad = Array{Any}(number_of_parameters)
        for i=1:number_of_parameters
            wgrad[i]= gradients(loss, p[i])
        end
        run(sess, global_variables_initializer())
    end

    function build_network(input_tensor, weights)
        α = Float64(0.01)
        x = nn.conv3d(expand_dims(expand_dims(input_tensor, 4), 5), expand_dims(expand_dims(expand_dims(expand_dims(expand_dims(weights[1], 1), 2), 3), 4), 5), strides = [1, 1, 1, 1, 1], padding = "VALID")
        x = x .+ weights[2]
        x = max(α .* x, x)
        x = nn.conv3d(x, expand_dims(expand_dims(expand_dims(expand_dims(expand_dims(weights[3], 1), 2), 3), 4), 5), strides = [1, 1, 1, 1, 1], padding = "VALID")
        x = x .+ weights[4]
        x = x + expand_dims(expand_dims(input_tensor, 4), 5)
        x = max(α .* x, x)

        x_ = nn.conv3d(x, expand_dims(expand_dims(expand_dims(expand_dims(expand_dims(weights[5], 1), 2), 3), 4), 5), strides = [1, 1, 1, 1, 1], padding = "VALID")
        x_ = x_ .+ weights[6]
        x_ = max(α .* x_, x_)
        x_ = nn.conv3d(x_, expand_dims(expand_dims(expand_dims(expand_dims(expand_dims(weights[7], 1), 2), 3), 4), 5), strides = [1, 1, 1, 1, 1], padding = "VALID")
        x_ = x_ .+ weights[8]
        x_ = x_ + x
        x_ = max(α .* x_, x_)
        return squeeze(x_)
    end

    #number_of_parameters = 8
    #N0 = 32
    #setup(N0, number_of_parameters)
    #using Distributions
    #δ_ = reshape(rand(Normal(0., 1.), 32 * 32 * 32), (32, 32, 32));
    #g_ = reshape(rand(Normal(0., 1.), 32 * 32 * 32), (32, 32, 32));
    #p_ = zeros(number_of_parameters);
    #s_ = reshape(rand(0:1, 32 * 32 * 32), (32, 32, 32));
    #s_mask = s_.>0;
    #using PyPlot
    #imshow(squeeze(sum(δ_, 3), 3))
    #imshow(squeeze(sum(g_, 3), 3))
    #imshow(squeeze(sum(run(sess, output, Dict(δ=>δ_, p=>p_)), 3), (3)))
    #imshow(squeeze(sum(run(sess, mock, Dict(δ=>δ_, p=>p_, s=>s_)), 3), (3)))
    #loss_ = run(sess, loss, Dict(δ=>δ_, p=>p_, s=>s_, g=>g_, mask=>s_mask))
    #adgrad_ = run(sess, adgrad, Dict(δ=>δ_, p=>p_, s=>s_, g=>g_, mask=>s_mask))
    #wgrad_ = run(sess, wgrad, Dict(δ=>δ_, p=>p_, s=>s_, g=>g_, mask=>s_mask))

    function initialize(state::State)
        print(LOG_INFO, "Likelihood initialization in Julia")

        number_of_parameters = 8
        N0 = libLSS.get(state, "N0", Int64, synchronous=true)
        NCAT = libLSS.get(state, "NCAT", Int64, synchronous=true)
        setup(N0, number_of_parameters)
        print(LOG_VERBOSE, "Found " *repr(NCAT) * " catalogues")
        bias = libLSS.resize_array(state, "galaxy_bias_0", number_of_parameters, Float64)
        bias[:] = 0
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
            L += run(sess, loss, Dict(p=>libLSS.get_array_1d(state, "galaxy_bias_"*sc, Float64), δ=>array, g=>libLSS.get_array_3d(state, "galaxy_data_"*sc, Float64), s=>libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64), mask=>libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64).>0.))
        end

        print(LOG_VERBOSE, "Likelihood is " * repr(L))
        return L
    end

    function generate_mock_data(state::State, ghosts::GhostPlanes, array::AbstractArray{Float64,3})
        print(LOG_INFO, "Generate mock")

        sc = "0"
        data = run(sess, mock, Dict(p=>libLSS.get_array_1d(state, "galaxy_bias_"*sc, Float64), δ=>array, s=>libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64)))
        data = libLSS.get_array_3d(state, "galaxy_data_"*sc, Float64)
        print(LOG_INFO, "Shape is " * repr(size(data)) * " and " * repr(size(array)))
        print(LOG_INFO, "Number of threads " * repr(Threads.nthreads()))
        print(LOG_INFO, "Noise is not included")
        print(LOG_INFO, "Max val is " * repr(maximum(array)) * " and data " * repr(maximum(data)))
    end

    function adjoint_gradient(state::State, array::AbstractArray{Float64,3}, ghosts::GhostPlanes, ag::AbstractArray{Float64,3})
        print(LOG_VERBOSE, "Adjoint gradient in Julia")
        NCAT = libLSS.get(state, "NCAT", Int64, synchronous=true)
        ag[:,:,:] = 0
        for catalog=1:NCAT
            sc = repr(catalog - 1)
            Smask = libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64).>0.
            ag[Smask] += run(sess, adgrad, Dict(p=>libLSS.get_array_1d(state, "galaxy_bias_"*sc, Float64), δ=>array, g=>libLSS.get_array_3d(state, "galaxy_data_"*sc, Float64), s=>libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64), mask=>Smask))[Smask]
        end
    end

    function likelihood_bias(state::State, ghosts::GhostPlanes, array, catalog_id, catalog_bias)
        sc = repr(catalog_id)
        return run(sess, loss, Dict(p=>catalog_bias, δ=>array, g=>libLSS.get_array_3d(state, "galaxy_data_"*sc, Float64), s=>libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64), mask=>libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64).>0.))
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
        adjoint_gradient_bias = run(sess, wgrad, Dict(p=>catalog_bias, δ=>array, g=>libLSS.get_array_3d(state, "galaxy_data_"*sc, Float64), s=>libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64), mask=>libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64).>0.))
    end
end
