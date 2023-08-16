#+
#   ARES/HADES/BORG Package -- ./extra/borg/libLSS/julia/julia_module.jl
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
baremodule libLSS

    using Base

    module_is_setup = false
    _internal = 0

    @enum LOG LOG_STD=0 LOG_ERROR=1 LOG_WARNING=2 LOG_INFO=3 LOG_INFO_SINGLE=4 LOG_VERBOSE=5 LOG_DEBUG=6

    const CONSOLE_PRINT=1
    const STATE_NEW_INT=2
    const STATE_EDIT_INT=3
    const STATE_QUERY_INT=4
    const STATE_NEW_1D_INT=5
    const STATE_GET_1D_INT=6
    const STATE_RESIZE_1D_INT=7
    const STATE_1D_INT_AUTOSIZE=8
    const STATE_NEW_2D_INT=9
    const STATE_GET_2D_INT=10
    const STATE_RESIZE_2D_INT=11
    const STATE_2D_INT_AUTOSIZE=12
    const STATE_NEW_3D_INT=13
    const STATE_GET_3D_INT=14
    const STATE_RESIZE_3D_INT=15
    const STATE_3D_INT_AUTOSIZE=16
    const STATE_NEW_LONG=17
    const STATE_EDIT_LONG=18
    const STATE_QUERY_LONG=19
    const STATE_NEW_1D_LONG=20
    const STATE_GET_1D_LONG=21
    const STATE_RESIZE_1D_LONG=22
    const STATE_1D_LONG_AUTOSIZE=23
    const STATE_NEW_2D_LONG=24
    const STATE_GET_2D_LONG=25
    const STATE_RESIZE_2D_LONG=26
    const STATE_2D_LONG_AUTOSIZE=27
    const STATE_NEW_3D_LONG=28
    const STATE_GET_3D_LONG=29
    const STATE_RESIZE_3D_LONG=30
    const STATE_3D_LONG_AUTOSIZE=31
    const STATE_NEW_DBL=32
    const STATE_EDIT_DBL=33
    const STATE_QUERY_DBL=34
    const STATE_NEW_1D_DBL=35
    const STATE_GET_1D_DBL=36
    const STATE_RESIZE_1D_DBL=37
    const STATE_1D_DBL_AUTOSIZE=38
    const STATE_NEW_2D_DBL=39
    const STATE_GET_2D_DBL=40
    const STATE_RESIZE_2D_DBL=41
    const STATE_2D_DBL_AUTOSIZE=42
    const STATE_NEW_3D_DBL=43
    const STATE_GET_3D_DBL=44
    const STATE_RESIZE_3D_DBL=45
    const STATE_3D_DBL_AUTOSIZE=46
    const RANDOM_UNIFORM=47
    const RANDOM_GAUSSIAN=48
    const GET_GALAXY_DESCRIPTOR=49
    const CONSOLE_PROGRESS_START=50
    const CONSOLE_PROGRESS_STEP=51
    const CONSOLE_PROGRESS_END=52
    const MODEL_SET_REQUEST_IO=53
    const MODEL_INPUT_GET_REAL=54
    const MODEL_INPUT_GET_FOURIER=55
    const MODEL_OUTPUT_GET_REAL=54
    const MODEL_OUTPUT_GET_FOURIER=55

    struct DimensionSpec{N} end

    d1d = DimensionSpec{1}()
    d2d = DimensionSpec{2}()
    d3d = DimensionSpec{3}()

    export d1d, d2d, d3d

    _code_new(::Type{Cint}) = STATE_NEW_INT
    _code_new(::Type{Cdouble}) = STATE_NEW_DBL
    _code_new(::Type{Clong}) = STATE_NEW_LONG

    _code_query(::Type{Cdouble}) = STATE_QUERY_DBL
    _code_edit(::Type{Cdouble}) = STATE_EDIT_DBL

    _code_query(::Type{Clong}) = STATE_QUERY_LONG
    _code_edit(::Type{Clong}) = STATE_EDIT_LONG

    _code_query(::Type{Cint}) = STATE_QUERY_INT
    _code_edit(::Type{Cint}) = STATE_EDIT_INT

    _code_new_1d(::Type{Cint}) = STATE_NEW_1D_INT
    _code_get_1d(::Type{Cint}) = STATE_GET_1D_INT
    _code_resize_1d(::Type{Cint}) = STATE_RESIZE_1D_INT
    _code_1d_autosize(::Type{Cint}) = STATE_1D_INT_AUTOSIZE
    _code_new_2d(::Type{Cint}) = STATE_NEW_2D_INT
    _code_get_2d(::Type{Cint}) = STATE_GET_2D_INT
    _code_resize_2d(::Type{Cint}) = STATE_RESIZE_2D_INT
    _code_2d_autosize(::Type{Cint}) = STATE_2D_INT_AUTOSIZE
    _code_new_3d(::Type{Cint}) = STATE_NEW_3D_INT
    _code_get_3d(::Type{Cint}) = STATE_GET_3D_INT
    _code_resize_3d(::Type{Cint}) = STATE_RESIZE_3D_INT
    _code_3d_autosize(::Type{Cint}) = STATE_3D_INT_AUTOSIZE

    _code_new_1d(::Type{Clong}) = STATE_NEW_1D_LONG
    _code_get_1d(::Type{Clong}) = STATE_GET_1D_LONG
    _code_resize_1d(::Type{Clong}) = STATE_RESIZE_1D_LONG
    _code_1d_autosize(::Type{Clong}) = STATE_1D_LONG_AUTOSIZE
    _code_new_2d(::Type{Clong}) = STATE_NEW_2D_LONG
    _code_get_2d(::Type{Clong}) = STATE_GET_2D_LONG
    _code_resize_2d(::Type{Clong}) = STATE_RESIZE_2D_LONG
    _code_1d_autosize(::Type{Clong}) = STATE_2D_LONG_AUTOSIZE
    _code_new_3d(::Type{Clong}) = STATE_NEW_3D_LONG
    _code_get_3d(::Type{Clong}) = STATE_GET_3D_LONG
    _code_resize_3d(::Type{Clong}) = STATE_RESIZE_3D_LONG
    _code_3d_autosize(::Type{Clong}) = STATE_3D_LONG_AUTOSIZE

    _code_new_1d(::Type{Cdouble}) = STATE_NEW_1D_DBL
    _code_get_1d(::Type{Cdouble}) = STATE_GET_1D_DBL
    _code_resize_1d(::Type{Cdouble}) = STATE_RESIZE_1D_DBL
    _code_1d_autosize(::Type{Cdouble}) = STATE_1D_DBL_AUTOSIZE
    _code_new_2d(::Type{Cdouble}) = STATE_NEW_2D_DBL
    _code_get_2d(::Type{Cdouble}) = STATE_GET_2D_DBL
    _code_resize_2d(::Type{Cdouble}) = STATE_RESIZE_2D_DBL
    _code_2d_autosize(::Type{Cdouble}) = STATE_2D_DBL_AUTOSIZE
    _code_new_3d(::Type{Cdouble}) = STATE_NEW_3D_DBL
    _code_get_3d(::Type{Cdouble}) = STATE_GET_3D_DBL
    _code_resize_3d(::Type{Cdouble}) = STATE_RESIZE_3D_DBL
    _code_3d_autosize(::Type{Cdouble}) = STATE_3D_DBL_AUTOSIZE


    struct AlreadyInitialized <: Exception
    end

    Cptr = Ptr{Nothing}

    struct State
        opaque::Cptr
    end

    export State, AlreadyInitialized

    function new(state::State, element::String, value::T; synchronous::Bool=false, mcmc_save::Bool=false) where {T}
        ccall(_internal[_code_new(T)], Nothing, (Cptr, Cstring, Ref{T}, Cint, Cint), state.opaque, element, value, synchronous, mcmc_save)
    end
    put(state::State, element::String, value::T; synchronous::Bool=false) where {T} =
        ccall(_internal[_code_edit(T)], Nothing, (Cptr, Cstring, Ref{T}, Cint), state.opaque, element, value, synchronous)
    function get(state::State, element::String, ::Type{T}; synchronous::Bool=false ) where {T}
        y = Ref{T}(0)
        ccall(_internal[_code_query(T)], Nothing, (Cptr, Cstring, Ref{T}, Cint), state.opaque, element, y, synchronous)
        y[]
    end
    function new_array(state::State, element::String, size::Int, ::Type{T}, cppOrder=true; mcmc_save::Bool=false) where {T}
        ptr_array = ccall(_internal[_code_new_1d(T)], Ptr{T}, (Cptr, Cstring, Csize_t, Cint), state.opaque, element, Csize_t(size), mcmc_save)
        _array_reorder(unsafe_wrap(Array, ptr_array, size), cppOrder)
    end
    function new_array(state::State, element::String, size::NTuple{2, Int}, ::Type{T}, cppOrder=true; mcmc_save::Bool=false) where {T}
	swapped_size = _swap_order(size, cppOrder)
        ptr_array = ccall(_internal[_code_new_2d(T)], Ptr{T}, (Cptr, Cstring, Csize_t, Csize_t, Cint), state.opaque, element, swapped_size[1], swapped_size[2], mcmc_save)
        _array_reorder(unsafe_wrap(Array, ptr_array, size), cppOrder)
    end
    function new_array(state::State, element::String, size::NTuple{3, Int}, ::Type{T}, cppOrder=true; mcmc_save::Bool=false) where {T}
	swapped_size = _swap_order(size, cppOrder)
        ptr_array = ccall(_internal[_code_new_3d(T)], Ptr{T}, (Cptr, Cstring, Csize_t, Csize_t, Csize_t, Cint), state.opaque, element, swapped_size[1], swapped_size[2], swapped_size[3], mcmc_save)
        _array_reorder(unsafe_wrap(Array, ptr_array, size), cppOrder)
    end
    function get_array_1d(state::State, element::String, ::Type{T}, cppOrder=true) where {T}
        a_size = Vector{Csize_t}(undef, 1)
        ptr_array = ccall(_internal[_code_get_1d(T)], Ptr{T}, (Cptr, Cstring, Ptr{Csize_t}), state.opaque, element, a_size)
        _array_reorder(unsafe_wrap(Array, ptr_array, a_size[1]), cppOrder)
    end
    function get_array_2d(state::State, element::String, ::Type{T}, cppOrder=true) where {T}
        a_size = Vector{Csize_t}(undef, 2)
        ptr_array = ccall(_internal[_code_get_2d(T)], Ptr{T}, (Cptr, Cstring, Ptr{Csize_t}), state.opaque, element, a_size)
        _array_reorder(unsafe_wrap(Array, ptr_array, (a_size[1],a_size[2])), cppOrder)
    end
    function get_array_3d(state::State, element::String, ::Type{T}, cppOrder=true) where {T}
        a_size = Vector{Csize_t}(undef, 3)
        ptr_array = ccall(_internal[_code_get_3d(T)], Ptr{T}, (Cptr, Cstring, Ptr{Csize_t}), state.opaque, element, a_size)
        _array_reorder(unsafe_wrap(Array, ptr_array, (a_size[1],a_size[2],a_size[3])), cppOrder)
    end
    get_array(state::State, element::String, ::Type{T}, ::DimensionSpec{1}, cppOrder=true) where {T}=get_array_1d(state, element, T, cppOrder)
    get_array(state::State, element::String, ::Type{T}, ::DimensionSpec{2}, cppOrder=true) where {T}=get_array_2d(state, element, T, cppOrder)
    get_array(state::State, element::String, ::Type{T}, ::DimensionSpec{3}, cppOrder=true) where {T}=get_array_3d(state, element, T, cppOrder)

    function resize_array(state::State, element::String, size::Int, ::Type{T}, cppOrder=true) where{T}
        ptr_array = ccall(_internal[_code_resize_1d(T)], Ptr{T}, (Cptr, Cstring, Csize_t), state.opaque, element, Csize_t(size))
        _array_reorder(unsafe_wrap(Array, ptr_array, size), cppOrder)
    end
    function resize_array(state::State, element::String, size::NTuple{2, Int}, ::Type{T}; cppOrder=true) where{T}
        ptr_array = ccall(_internal[_code_resize_2d(T)], Ptr{T}, (Cptr, Cstring, Csize_t, Csize_t), state.opaque, element, Csize_t(size[1]), Csize_t(size[2]))
        _array_reorder(unsafe_wrap(Array, ptr_array, size), cppOrder)
    end
    function resize_array(state::State, element::String, size::NTuple{3, Int}, ::Type{T}; cppOrder=true) where{T}
        ptr_array = ccall(_internal[_code_resize_3d(T)], Ptr{T}, (Cptr, Cstring, Csize_t, Csize_t, Csize_t), state.opaque, element, Csize_t(size[1]), Csize_t(size[2]), Csize_t(size[3]))
        _array_reorder(unsafe_wrap(Array, ptr_array, size), cppOrder)
    end
    function autosize_array(state::State, element::String, b::Bool, ::Type{T}, ::DimensionSpec{1}) where {T}
        ccall(_internal[_code_1d_autosize(T)], Cvoid, (Cptr, Cstring, Cint), state.opaque, element, Cint(b))
    end
    function autosize_array(state::State, element::String, b::Bool, ::Type{T}, ::DimensionSpec{2}) where {T}
        ccall(_internal[_code_2d_autosize(T)], Cvoid, (Cptr, Cstring, Cint), state.opaque, element, Cint(b))
    end
    function autosize_array(state::State, element::String, b::Bool, ::Type{T}, ::DimensionSpec{3}) where {T}
        ccall(_internal[_code_3d_autosize(T)], Cvoid, (Cptr, Cstring, Cint), state.opaque, element, Cint(b))
    end

    export new, put, get, new_array, get_array_1d, get_array_2d, get_array_3d, get_array, resize_array, autosize_array

    print(level::LOG, msg::String) =
        ccall(_internal[CONSOLE_PRINT], Nothing, (Cint, Cstring), Int(level), msg)

    export print, LOG_STD, LOG_ERROR, LOG_WARNING, LOG_INFO, LOG_INFO_SINGLE, LOG_VERBOSE, LOG_DEBUG

    function progress_start(level::LOG, msg::String, steps::Int, func)
        p = ccall(_internal[CONSOLE_PROGRESS_START], Cptr, (Cint, Cstring, Cint), Int(level), msg, steps)
        for i in 1:steps
	  func(i)
	  ccall(_internal[CONSOLE_PROGRESS_STEP], Nothing, (Cptr,), p)
	end
	ccall(_internal[CONSOLE_PROGRESS_END], Nothing, (Cptr,), p)
	Nothing
    end

    # Extract "galaxy" information

    # WARNING GalaxyDescriptor struct must reflect the structure in libLSS/data/galaxies.hpp
    struct GalaxyDescriptor
       id::Clonglong
       phi::Cdouble
       theta::Cdouble
       zo::Cdouble
       m::Cdouble
       M_abs::Cdouble
       Mgal::Cdouble
       z::Cdouble
       r::Cdouble
       w::Cdouble
       final_w::Cdouble
       radius::Cdouble
       spin::Cdouble
       posx::Cdouble
       posy::Cdouble
       posz::Cdouble
       vx::Cdouble
       vy::Cdouble
       vz::Cdouble
    end

    function get_galaxy_descriptor(state::State, id)
        sz = Vector{Cint}(undef, 1)
        ptr_array = ccall(_internal[GET_GALAXY_DESCRIPTOR], Ptr{GalaxyDescriptor}, (Cptr, Cint, Cptr), state.opaque, Cint(id), sz)
        unsafe_wrap(Array, ptr_array, sz[1])
    end

    export get_galaxy_descriptor

    # Random numbers
    uniform(state::State) =
        ccall(_internal[RANDOM_UNIFORM], Cdouble, (Cptr,), state.opaque)
    gaussian(state::State) =
        ccall(_internal[RANDOM_GAUSSIAN], Cdouble, (Cptr,), state.opaque)

    export uniform, gaussian

    struct BoxModel
        L::Tuple{Float64, Float64, Float64}
        N::Tuple{UInt64, UInt64, UInt64}
    end

    _setup_state(ptr_state::Ptr{Nothing}) = State(ptr_state)

    function _setup_module(entries)
        global _internal
        global module_is_setup

        if module_is_setup
            throw(AlreadyInitialized())
        end
        _internal = entries
        module_is_setup = true

        true
    end

    struct BadGradient <: Exception
    end

    export BadGradient

    _checkBadGradient(e::BadGradient) = true
    _checkBadGradient(e) = false

    struct GhostPlanes
        opaque::Ptr{Nothing}
        access::Ptr{Nothing}
        ag_access::Ptr{Nothing}
        maxN2::UInt64
    end

    function _new_ghost_plane(ghost_obj::Ptr{Nothing}, ghost_access::Ptr{Nothing}, ghost_ag_access::Ptr{Nothing}, maxN2::Csize_t)
        return GhostPlanes(ghost_obj, ghost_access, ghost_ag_access, maxN2)
    end

    function get_ag_ghost_plane(ghosts::GhostPlanes, plane)
        return ccall(ghosts.ag_access, AbstractArray{Float64,2}, (Cptr,Csize_t,Csize_t), ghosts.opaque, plane, ghosts.maxN2)
    end

    function get_ghost_plane(ghosts::GhostPlanes, plane)
        return ccall(
            ghosts.access, AbstractArray{Float64,2},
            (Cptr,Csize_t,Csize_t), ghosts.opaque, plane, ghosts.maxN2)
    end

    export GhostPlanes, get_ag_ghost_plane, get_ghost_plane

    function _array_reorder(a::X, cppOrder::Bool) where {X<:AbstractArray{T,N}} where {T,N}
        if cppOrder
          return PermutedDimsArray(a, N:-1:1)
	else 
	  return PermutedDimsArray(a, 1:N) # To preserve type transparency
	end
    end

    function _swap_order(Ns::NTuple{M,Int}, cppOrder::Bool) where {M}
      if cppOrder
        return Ns
      else
        return reverse(Ns)
      end
    end

    abstract type ModelIO{N}
    end

    struct ModelInput{N} <: ModelIO{N} 
        opaque::Cptr
    end

    struct ModelOutput{N} <: ModelIO{N} 
        opaque::Cptr
    end

    @enum IOType IO_REAL=0 IO_FOURIER=1

    export ModelInput, ModelOutput

    function _get_opaque_model(m::ModelInput{N}) where {N<:Int}
      m.opaque
    end

    function _get_opaque_model(m::ModelOutput{N}) where {N<:Int}
      m.opaque
    end

    function _new_model_input(opaque::Cptr) where {N<:Int}
       ModelInput{N}(opaque)
    end

    function _new_model_output(opaque::Cptr) where {N<:Int}
       ModelOutput{N}(opaque)
    end

    function requestIO(m::ModelIO{N}, io::IOType) where {N<:Int}
      ccall(_internal[MODEL_SET_REQUEST_IO], Nothing, (Cptr,Cint,Cint), _get_opaque_model(m), N, Int(io))
    end

    function getReal(m::ModelInput{N}) where {N<:Int}
      ccall(_internal[MODEL_INPUT_GET_REAL], AbstractArray{Float64,N}, (Cptr,Cint), m.opaque, Int(N))
    end

    function getFourier(m::ModelInput{N}) where {N<:Int}
      ccall(_internal[MODEL_INPUT_GET_FOURIER], AbstractArray{ComplexF64,N}, (Cptr,Cint), m.opaque, Int(N))
    end

    function getReal(m::ModelOutput{N}) where {N<:Int}
      ccall(_internal[MODEL_OUTPUT_GET_REAL], AbstractArray{Float64,N}, (Cptr,Cint), m.opaque, Int(N))
    end

    function getFourier(m::ModelOutput{N}) where {N<:Int}
      ccall(_internal[MODEL_OUTPUT_GET_FOURIER], AbstractArray{ComplexF64,N}, (Cptr,Cint), m.opaque, Int(N))
    end
end
