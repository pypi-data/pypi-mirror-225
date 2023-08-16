#+
#   ARES/HADES/BORG Package -- ./extra/hmclet/example/test_like_TF.jl
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
module network
    using ..libLSS

    import ..libLSS.State
    import ..libLSS.GhostPlanes, ..libLSS.get_ghost_plane
    import ..libLSS.print, ..libLSS.LOG_INFO, ..libLSS.LOG_VERBOSE, ..libLSS.LOG_DEBUG

    using TensorFlow
    using PyPlot

    sess = Session(allow_growth = true)
    adgrad = nothing
    wgrad = nothing

    function setup(N0, N1, N2)
        global adgrad, wgrad
        p = [TensorFlow.placeholder(Float64, shape = (), name = "bias"), TensorFlow.placeholder(Float64, shape = (), name = "noise")]
        δ = TensorFlow.placeholder(Float64, shape = Int64[N0, N1, N2], name = "density")
        g = TensorFlow.placeholder(Float64, shape = Int64[N0, N1, N2], name = "galaxy")
        s = TensorFlow.placeholder(Float64, shape = Int64[N0, N1, N2], name = "selection")
        gaussian = TensorFlow.placeholder(Float64, shape = Int64[N0, N1, N2], name = "gaussian_field")
        mask = TensorFlow.placeholder(Bool, shape = Int64[N0, N1, N2], name = "mask")
        mask_ = TensorFlow.reshape(mask, N0 * N1 * N2, name = "flat_mask")
        g_ = TensorFlow.identity(TensorFlow.boolean_mask(TensorFlow.reshape(g, N0 * N1 * N2), mask_), name = "flat_masked_galaxy")
        s_ = TensorFlow.identity(TensorFlow.boolean_mask(TensorFlow.reshape(s, N0 * N1 * N2), mask_), name = "flat_masked_selection")
        output = TensorFlow.add(1., TensorFlow.multiply(p[1], δ), name = "biased_density")
        mock = TensorFlow.multiply(s, output, name = "selected_biased_density")
        mock_ = TensorFlow.identity(TensorFlow.boolean_mask(TensorFlow.reshape(mock, N0 * N1 * N2), mask_), name = "flat_masked_selected_biased_density")
        mock_galaxy = TensorFlow.add(mock, TensorFlow.multiply(TensorFlow.multiply(TensorFlow.sqrt(TensorFlow.exp(p[2])), TensorFlow.sqrt(s)), gaussian), name = "mock_galaxy")
        ms = TensorFlow.reduce_sum(TensorFlow.cast(mask, Float64), name = "number_of_voxels")
        loss = TensorFlow.identity(TensorFlow.add(TensorFlow.multiply(0.5, TensorFlow.reduce_sum(TensorFlow.square(g_ - mock_) / TensorFlow.multiply(TensorFlow.exp(p[2]), s_))), TensorFlow.multiply(0.5, TensorFlow.multiply(ms, p[2]))) - TensorFlow.exp(p[1]) - TensorFlow.exp(p[2]), name = "loss")
        adgrad = TensorFlow.gradients(loss, δ)
        wgrad = [TensorFlow.gradients(loss, p[i]) for i in range(1, length = size(p)[1])]
    end

    function initialize(state)
        print(LOG_INFO, "Likelihood initialization in Julia")
        setup(libLSS.get(state, "N0", Int64, synchronous=true), libLSS.get(state, "N1", Int64, synchronous=true), libLSS.get(state, "N2", Int64, synchronous=true))
        bias = libLSS.resize_array(state, "galaxy_bias_0", 2, Float64)
        bias[:] .= log(1.)
        print(LOG_VERBOSE, "Found " *repr(libLSS.get(state, "NCAT", Int64, synchronous=true)) * " catalogues")
    end

    function get_required_planes(state::State)
        print(LOG_INFO, "Check required planes")
        return Array{UInt64,1}([])
    end

    function likelihood(state::State, ghosts::GhostPlanes, array::AbstractArray{Float64,3})
        print(LOG_INFO, "Likelihood evaluation in Julia")
        L = Float64(0.)
        for catalog=1:libLSS.get(state, "NCAT", Int64, synchronous=true)
            L += run(sess, TensorFlow.get_tensor_by_name("loss"),
                    Dict(TensorFlow.get_tensor_by_name("bias")=>libLSS.get_array_1d(state, "galaxy_bias_"*repr(catalog - 1), Float64)[1],
                         TensorFlow.get_tensor_by_name("noise")=>libLSS.get_array_1d(state, "galaxy_bias_"*repr(catalog - 1), Float64)[2],
                         TensorFlow.get_tensor_by_name("density")=>array,
                         TensorFlow.get_tensor_by_name("galaxy")=>libLSS.get_array_3d(state, "galaxy_data_"*repr(catalog - 1), Float64),
                         TensorFlow.get_tensor_by_name("selection")=>libLSS.get_array_3d(state, "galaxy_sel_window_"*repr(catalog - 1), Float64),
                         TensorFlow.get_tensor_by_name("mask")=>libLSS.get_array_3d(state, "galaxy_sel_window_"*repr(catalog - 1), Float64).>0.))
        end
        print(LOG_VERBOSE, "Likelihood is " * repr(L))
        return L
    end

    function generate_mock_data(state::State, ghosts::GhostPlanes, array::AbstractArray{Float64,3})
        print(LOG_INFO, "Generate mock")
        for catalog in 1:libLSS.get(state, "NCAT", Int64, synchronous=true)
            gaussian_field = Array{Float64}(undef, size(array)[1], size(array)[2], size(array)[3])
            data = libLSS.get_array_3d(state, "galaxy_data_"*repr(catalog - 1), Float64)
                for i=1:size(array)[1],j=1:size(array)[2],k=1:size(array)[3]
                    gaussian_field[i,j,k] = libLSS.gaussian(state)
                end
            data[:, :, :] = run(sess, TensorFlow.get_tensor_by_name("mock_galaxy"),
                               Dict(TensorFlow.get_tensor_by_name("bias")=>libLSS.get_array_1d(state, "galaxy_bias_"*repr(catalog - 1), Float64)[1],
                                    TensorFlow.get_tensor_by_name("noise")=>libLSS.get_array_1d(state, "galaxy_bias_"*repr(catalog - 1), Float64)[2],
                                    TensorFlow.get_tensor_by_name("density")=>array,
                                    TensorFlow.get_tensor_by_name("selection")=>libLSS.get_array_3d(state, "galaxy_sel_window_"*repr(catalog - 1), Float64),
                                    TensorFlow.get_tensor_by_name("gaussian_field")=>gaussian_field))
            print(LOG_INFO, "Plotting generated mock from catalog "*repr(catalog - 1)*" as ./plots/generate_mock_data_"*repr(catalog - 1)*".png")
            imshow(dropdims(sum(data, dims = 3), dims = 3))
            colorbar()
            savefig("plots/generated_mock_data_"*repr(catalog - 1)*".png")
            close()
        end
    end

    function adjoint_gradient(state::State, array::AbstractArray{Float64,3}, ghosts::GhostPlanes, ag::AbstractArray{Float64,3})
        print(LOG_VERBOSE, "Adjoint gradient in Julia")
        ag[:,:,:] .= 0
        for catalog=1:libLSS.get(state, "NCAT", Int64, synchronous=true)
            Smask = libLSS.get_array_3d(state, "galaxy_sel_window_"*repr(catalog - 1), Float64).>0.
            ag[Smask] += run(sess, adgrad,
                Dict(TensorFlow.get_tensor_by_name("bias")=>libLSS.get_array_1d(state, "galaxy_bias_"*repr(catalog - 1), Float64)[1],
                     TensorFlow.get_tensor_by_name("noise")=>libLSS.get_array_1d(state, "galaxy_bias_"*repr(catalog - 1), Float64)[2],
                     TensorFlow.get_tensor_by_name("density")=>array, TensorFlow.get_tensor_by_name("galaxy")=>libLSS.get_array_3d(state, "galaxy_data_"*repr(catalog - 1), Float64),
                     TensorFlow.get_tensor_by_name("selection")=>libLSS.get_array_3d(state, "galaxy_sel_window_"*repr(catalog - 1), Float64),
                     TensorFlow.get_tensor_by_name("mask")=>Smask))[Smask]
        end
    end

    function likelihood_bias(state::State, ghosts::GhostPlanes, array, catalog_id, catalog_bias)
        print(LOG_VERBOSE, "Likelihood bias in Julia")
        return run(sess, TensorFlow.get_tensor_by_name("loss"),
            Dict(TensorFlow.get_tensor_by_name("bias")=>catalog_bias[1],
                 TensorFlow.get_tensor_by_name("noise")=>catalog_bias[2],
                 TensorFlow.get_tensor_by_name("density")=>array,
                 TensorFlow.get_tensor_by_name("galaxy")=>libLSS.get_array_3d(state, "galaxy_data_"*string(catalog_id), Float64),
                 TensorFlow.get_tensor_by_name("selection")=>libLSS.get_array_3d(state, "galaxy_sel_window_"*string(catalog_id), Float64),
                 TensorFlow.get_tensor_by_name("mask")=>libLSS.get_array_3d(state, "galaxy_sel_window_"*string(catalog_id), Float64) .> 0.))
    end

    function get_step_hint(state, catalog_id, bias_id)
        return 0.1
    end

    function log_prior_bias(state, catalog_id, bias_tilde)
        return 0.
    end

    function adjoint_bias(state::State, ghosts::GhostPlanes, array, catalog_id, catalog_bias, adjoint_gradient_bias)
        print(LOG_VERBOSE, "Adjoint gradient of bias in Julia")
        adjoint_gradient_bias .= run(sess, wgrad,
            Dict(TensorFlow.get_tensor_by_name("bias")=>catalog_bias[1],
                 TensorFlow.get_tensor_by_name("noise")=>catalog_bias[2],
                 TensorFlow.get_tensor_by_name("density")=>array,
                 TensorFlow.get_tensor_by_name("galaxy")=>libLSS.get_array_3d(state, "galaxy_data_"*string(catalog_id), Float64),
                 TensorFlow.get_tensor_by_name("selection")=>libLSS.get_array_3d(state, "galaxy_sel_window_"*string(catalog_id), Float64),
                 TensorFlow.get_tensor_by_name("mask")=>libLSS.get_array_3d(state, "galaxy_sel_window_"*string(catalog_id), Float64) .> 0.))
    end
end
