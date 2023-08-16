module test_conv_like
    include("convHMC.jl")
    using libLSS

    import libLSS.State
    import libLSS.GhostPlanes, libLSS.get_ghost_plane
    import libLSS.print, libLSS.LOG_INFO, libLSS.LOG_VERBOSE, libLSS.LOG_DEBUG
    #import test_conv_like.convHMC.initialise

    function initialize(state::State)
        print(LOG_INFO, "Likelihood initialization in Julia")
        NCAT = libLSS.get(state, "NCAT", Int64, synchronous=true)
        print(LOG_VERBOSE, "Found " *repr(NCAT) * " catalogues")
        N0 = libLSS.get(state, "localN0", Int64, synchronous=true)
        N1 = 32
        N2 = 32

        num_layers = 1
        C0 = 3
        C1 = 3
        C2 = 3
        bias = libLSS.resize_array(state, "galaxy_bias_0", num_layers * 5 + 1, Float64)
        #bias = libLSS.resize_array(state, "galaxy_bias_0", 29, Float64)
        bias[:] = 0
        bias[1] = 1
        bias[6] = 100
        #bias[28] = 1
        #bias[29] = 100
        #bias[11] = 1
        #bias[16] = 1
        #bias[21] = 1
        #bias[26] = 100
        test_conv_like.convHMC.setup(num_layers, N0, N1, N2, 5 * num_layers, [C0, C1, C2], [N0, N1, N2], test_conv_like.convHMC.convolutional_network, test_conv_like.convHMC.get_isotropic_weights, test_conv_like.convHMC.mse)
        #test_conv_like.convHMC.setup(num_layers, N0, N1, N2, 28, [C0, C1, C2], [N0, N1, N2], test_conv_like.convHMC.convolutional_network, test_conv_like.convHMC.get_3d_conv, test_conv_like.convHMC.mse)

        #bias = libLSS.resize_array(state, "galaxy_bias_0", 2, Float64)
        #bias[1] = 100
        #bias[2] = 1
        #test_conv_like.convHMC.setup(num_layers, N0, N1, N2, 1, -99, [N0, N1, N2], test_conv_like.convHMC.no_network, test_conv_like.convHMC.get_poisson_bias, test_conv_like.convHMC.poisson_bias)
    end


    function get_required_planes(state::State)
        print(LOG_INFO, "Check required planes")
        return []
    end

    function likelihood(state::State, ghosts::GhostPlanes, array::AbstractArray{Float64,3})
        print(LOG_INFO, "Likelihood evaluation in Julia")

        NCAT = libLSS.get(state, "NCAT", Int64, synchronous=true)
        L = Float64(0)
        for catalog in 0:(NCAT-1)
          sc = repr(catalog)
          data = libLSS.get_array_3d(state, "galaxy_data_"*sc, Float64)
          params = libLSS.get_array_1d(state, "galaxy_bias_"*sc, Float64)
          S = libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64)
          Smask = S.>0
          L += test_conv_like.convHMC.evaluate(params[1:end-1], array, data, S, params[end], Smask)
        end
        print(LOG_VERBOSE, "Likelihood is " * repr(L))
        return L
    end

    function generate_mock_data(state::State, ghosts::GhostPlanes, array::AbstractArray{Float64,3})
        #sc = "0"
        #data = libLSS.get_array_3d(state, "galaxy_data_"*sc, Float64)
        #b = libLSS.get_array_1d(state, "galaxy_bias_"*sc, Float64)
        #S = libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64)
        #s = size(data)
        #print(LOG_INFO, "Shape is " * repr(size(data)) * " and " * repr(size(array)))
        #print(LOG_INFO, "Number of threads " * repr(Threads.nthreads()))
        #N0=s[1]
        #N1=s[2]
        #N2=s[3]
        #noise = sqrt(b[1])
        #bias = b[2]
        #for i=1:N0,j=1:N1,k=1:N2
        #  data[i,j,k] = S[i,j,k]*(1+bias*array[i,j,k] + noise*libLSS.gaussian(state))
        #end
        print(LOG_INFO, "Generate mock")
        params = libLSS.get_array_1d(state, "galaxy_bias_0", Float64)
        S = libLSS.get_array_3d(state, "galaxy_sel_window_0", Float64)
        data = test_conv_like.convHMC.get_field(params[1:end-1], array) .* S
        print(LOG_INFO, "Max val is " * repr(maximum(array)) * " and data " * repr(maximum(data)))
    end

    function adjoint_gradient(state::State, array::AbstractArray{Float64,3}, ghosts::GhostPlanes, ag::AbstractArray{Float64,3})
        print(LOG_VERBOSE, "Adjoint gradient in Julia")
        N0 = libLSS.get(state, "N0", Int64, synchronous=true)
        NCAT = libLSS.get(state, "NCAT", Int64, synchronous=true)
        L = Float64(0)
        ag[:, :, :] = 0
        for catalog in 0:(NCAT-1)
          sc = repr(catalog)
          data = libLSS.get_array_3d(state, "galaxy_data_"*sc, Float64)
          params = libLSS.get_array_1d(state, "galaxy_bias_0", Float64)
          S = libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64)
          Smask = S.>0
          ag += test_conv_like.convHMC.adjointGradient(params[1:end-1], array, data, S, params[end], Smask)
        end
    end
end
