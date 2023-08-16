#+
#   ARES/HADES/BORG Package -- ./extra/hmclet/example/test_like.jl
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
module julia_test
    using ..libLSS
    using NPZ

    import ..libLSS.State
    import ..libLSS.GhostPlanes, ..libLSS.get_ghost_plane
    import ..libLSS.print, ..libLSS.LOG_INFO, ..libLSS.LOG_VERBOSE, ..libLSS.LOG_DEBUG

    apply_transform(bias_tilde) = exp.(bias_tilde)
    apply_inv_transform(bias) = log.(bias)

    function initialize(state)
        print(LOG_INFO, "Likelihood initialization in Julia")

        NCAT = libLSS.get(state, "NCAT", Int64)
        print(LOG_VERBOSE, "Found " *repr(NCAT) * " catalogues")
        for catalog in 0:(NCAT-1)
#          galaxies = libLSS.get_galaxy_descriptor(state, catalog)
#          print(LOG_VERBOSE, repr(size(galaxies)))
#          all_spin = getfield.(galaxies, :spin)
          bias = libLSS.resize_array(state, "galaxy_bias_"*repr(catalog), 2, Float64)
          bias[1] = 1
          bias[2] = 0.01 
          bias .= apply_inv_transform(bias)
        end
    end


    function get_required_planes(state::State)
        print(LOG_INFO, "Check required planes")
        return Array{UInt64,1}([])
    end

    function likelihood(state::State, ghosts::GhostPlanes, array::AbstractArray{Float64,3})
        print(LOG_VERBOSE, "Likelihood evaluation in Julia")

        N0 = libLSS.get(state, "N0", Int64)
        NCAT = libLSS.get(state, "NCAT", Int64)
        L = Float64(0)
        for catalog in 0:(NCAT-1)
          sc = repr(catalog)
          b = libLSS.get_array_1d(state, "galaxy_bias_"*sc, Float64)

          L += likelihood_bias(state, ghosts, array, catalog, b)
        end

        print(LOG_VERBOSE, "Likelihood is " * repr(L))
        return L
    end

    function generate_mock_data(state::State, ghosts::GhostPlanes, array::AbstractArray{Float64,3})
        print(LOG_INFO, "Generate mock")
        NCAT = libLSS.get(state, "NCAT", Int64)

        for cat in 0:(NCAT-1)
          sc = repr(cat)
          data = libLSS.get_array_3d(state, "galaxy_data_"*sc, Float64)
          b = apply_transform(libLSS.get_array_1d(state, "galaxy_bias_"*sc, Float64))
          print(LOG_VERBOSE, "Bias for mock is $(b)")
          S = libLSS.get_array_3d(state, "galaxy_sel_window_$(sc)", Float64)
          s = size(data)
          print(LOG_INFO, "Shape is " * repr(size(data)) * " and " * repr(size(array)))
          print(LOG_INFO, "Number of threads " * repr(Threads.nthreads()))
          N0=s[1]
          N1=s[2]
          N2=s[3]
          noise = sqrt(b[2])
          print(LOG_INFO, "Noise is $(noise)")
          bias = b[1]
          for i=1:N0,j=1:N1,k=1:N2
            data[i,j,k] = S[i,j,k]*(1+bias*array[i,j,k]) + sqrt(S[i,j,k])*noise*libLSS.gaussian(state)
          end
        end
    end

    function adjoint_gradient(state::State, array::AbstractArray{Float64,3}, ghosts::GhostPlanes, ag::AbstractArray{Float64,3})
        print(LOG_VERBOSE, "Adjoint gradient in Julia")
        N0 = libLSS.get(state, "N0", Int64)
        NCAT = libLSS.get(state, "NCAT", Int64)
        L = Float64(0)
        ag[:,:,:] .= 0
        for catalog in 0:(NCAT-1)
          sc = repr(catalog)
          data = libLSS.get_array_3d(state, "galaxy_data_"*sc, Float64)
          b = apply_transform(libLSS.get_array_1d(state, "galaxy_bias_"*sc, Float64))
          S = libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64)
          noise = b[2]
          bias = b[1]
          Smask = findall(S.>0)

          ag[Smask] += -(data[Smask] .- S[Smask].*(1 .+ bias*array[Smask]))*bias/noise
        end
    end

    # 1/2 sum( (data - S (1 + b rho))^2 / (S*n) )
    # There is  a change of variable to map [-infinity, infinity] to [0, infinity]
    # y = exp(x)  (x is the bias_tilde, y is the bias params)
    # we know the function in terms of y though, but the posterior must be in terms of x
    # probability conservation:
    #    f_tilde(x) dx = f(y) dy
    #
    # f_tilde(x) = f(y) dy/dx = f(y) exp(x) -> -log(f_tilde) = -log(f) - y
    # -dlog(f_tilde(x))/dx = -dlog(f_tilde)/dy dy/dx = (-dlog(f)/dy - 1) * dy/dx
    # dy/dx = exp(x) = y


    function likelihood_bias(state::State, ghosts::GhostPlanes, array, catalog_id, catalog_bias_tilde)
        catalog_bias = apply_transform(catalog_bias_tilde)
        sc = string(catalog_id)
        print(LOG_VERBOSE,"Catalog id is " * sc * " bias is " * repr(catalog_bias))
        data = libLSS.get_array_3d(state, "galaxy_data_"*sc, Float64)
        S = libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64)
        Smask = findall(S.>0)
        noise = catalog_bias[2]
        bias = catalog_bias[1]

        prior_bias = catalog_bias_tilde[1] # Not the bias-tilde-2

        return 0.5*sum(
            (data[Smask] .- S[Smask].*(1 .+ bias.*array[Smask])).^2 ./ (S[Smask].*noise)
            ) + 0.5*size(Smask)[1]*log(noise) - prior_bias
    end

    function get_step_hint(state, catalog_id, bias_id)
        return 0.1
    end

    function log_prior_bias(state, catalog_id, bias_tilde)
        # Change of variable bias = exp(bias_tilde)
        return 0
    end

    function adjoint_bias(state::State, ghosts::GhostPlanes,
        array, catalog_id, catalog_bias_tilde, adjoint_gradient_bias)
        catalog_bias = apply_transform(catalog_bias_tilde)

        print(LOG_VERBOSE,"ADJOINT: Catalog id is $(catalog_id), bias is $(catalog_bias), bias_tilde is $(catalog_bias_tilde)")
        sc = string(catalog_id)
        data = libLSS.get_array_3d(state, "galaxy_data_"*sc, Float64)
        S = libLSS.get_array_3d(state, "galaxy_sel_window_"*sc, Float64)
        Smask = findall(S.>0)
        noise = catalog_bias[2]
        bias = catalog_bias[1]

        delta = (data[Smask] .- S[Smask].*(1 .+ bias*array[Smask]))

        adjoint_gradient_bias[1] = -sum(delta.*array[Smask]) ./noise
        adjoint_gradient_bias[2] = -0.5*sum(delta.^2 ./ (S[Smask])) /(noise^2) + 0.5 * size(Smask)[1]/noise
        adjoint_gradient_bias .*= catalog_bias

        adjoint_gradient_bias[1] -= 1  # Derivative of the prior
        print(LOG_VERBOSE,"ADJOINT: -> $(adjoint_gradient_bias)")
    end

    function fill_diagonal_mass_matrix(state::State)
        return [1e3,1e3]
#        return [1e-5,1e-5]
#        return [1e-7,1e-7]
    end

    function generate_ic(state::State)
        print(LOG_INFO, "Generate special IC for the chain")
        b = libLSS.get_array(state, "galaxy_bias_0", Float64, d1d)
        b[1] = 1.
        b[2] = 1.
#        sref = npzread("velmass_ic_500Mpc_32.npz")["arr_0"]
#        s = libLSS.get_array_3d(state, "s_field", Float64)
#        s .*= 0.01
#        startN0 = libLSS.get(state, "startN0", Int64)
#        localN0,N1,N2 = size(s)
#        print(LOG_INFO, "Dims = [$(startN0):$(startN0+localN0)]x$(N1)x$(N2)")
#        for i=1:localN0, j=1:N1,k=1:N2
#          s[i,j,k] = sref[k,j,i+startN0]
##### # 0.01*cos(2*pi*(i-1)/N)*sin(2*pi*(j-1)/N)
#        end
#        print(LOG_INFO, "DONE DONE")
    end
end
