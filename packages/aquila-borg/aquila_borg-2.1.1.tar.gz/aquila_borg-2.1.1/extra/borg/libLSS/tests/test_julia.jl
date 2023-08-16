#+
#   ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_julia.jl
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

    function initialize(state::State)
        print(LOG_VERBOSE, "Likelihood initialization in Julia")

        #jbias = libLSS.new_array(state, "julia_bias", 10, Float64)
        data = libLSS.get_array_3d(state, "galaxy_data_0", Float64)
        startN0 = libLSS.get(state, "startN0", Int64)
        localN0 = libLSS.get(state, "localN0", Int64)
        print(LOG_VERBOSE, "galaxy data has shape " * repr(size(data)))
        print(LOG_VERBOSE, "startN0 = " * repr(startN0) * " localN0="*repr(localN0))
    end

    function set_default_bias(state::State, catalog::Int32)
        print(LOG_VERBOSE, "Asked to fillup the default bias parameters")
    end

    function get_required_planes(state::State)
        N0 = libLSS.get(state, "N0", Int64)
        startN0 = libLSS.get(state, "startN0", Int64)
        localN0 = libLSS.get(state, "localN0", Int64)
        return Array{UInt64,1}([(startN0+N0-1)%N0, (startN0+localN0+1)%N0])
    end

    function likelihood(state::State, ghosts::GhostPlanes, array::AbstractArray{Float64,3})
        print(LOG_VERBOSE, "Likelihood evaluation in Julia")

        data = libLSS.get_array_3d(state, "galaxy_data_0", Float64)

        N0 = libLSS.get(state, "N0", Int64)
        startN0 = libLSS.get(state, "startN0", Int64)
        localN0 = libLSS.get(state, "localN0", Int64)
        plane_m1 = get_ghost_plane(ghosts, (startN0+N0-1)%N0)
        plane_p1 = get_ghost_plane(ghosts, (startN0+localN0+1)%N0)


        print(LOG_DEBUG, "Shape data " * repr(size(data)) * "; shape array " * repr(size(array)))
        print(LOG_DEBUG, "max values are " * repr(maximum(data)) * " and " * repr(maximum(array)))

        L = sum((data .- 1 .- array).^2)/100
        print(LOG_VERBOSE, "Likelihood is " * repr(L))

        return L
    end

    function generate_mock_data(state::State, ghosts::GhostPlanes, array::AbstractArray{Float64,3})
        data = libLSS.get_array_3d(state, "galaxy_data_0", Float64)
        print(LOG_INFO, "Generate mock")
        print(LOG_INFO, "Shape is " * repr(size(data)) * " and " * repr(size(array)))
        s = size(data)
        print(LOG_INFO, "Number of threads " * repr(Threads.nthreads()))

        N0=s[1]
        N1=s[2]
        N2=s[3]
        for i=1:N0,j=1:N1,k=1:N2
                data[i,j,k] = 1+array[i,j,k] + 10*libLSS.gaussian(state)
        end

        print(LOG_INFO, "Max val is " * repr(maximum(array)) * " and data " * repr(maximum(data)))
    end

    function adjoint_gradient(state::State, array::AbstractArray{Float64,3}, ghosts::GhostPlanes, ag::AbstractArray{Float64,3})
        print(LOG_VERBOSE, "Adjoint gradient in Julia")

        #ghost_plane_ag = get_ghost_plane_ag(ghosts, 0)

        data = libLSS.get_array_3d(state, "galaxy_data_0", Float64)

        ag = (data .- 1 .-array)/100;
    end
end
