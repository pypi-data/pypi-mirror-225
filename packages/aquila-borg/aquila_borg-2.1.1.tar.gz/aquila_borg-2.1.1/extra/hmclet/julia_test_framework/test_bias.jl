#
# This is a very drafty test framework for julia likelihood.
# It allows to avoid running a full BORG machine to test the basics
# of the likelihood.
#

JULIA_LIKELIHOOD="sim_run_quadratic.jl"

module libLSS

    using HDF5

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

        function GalaxyDescriptor(c::HDF5.HDF5Compound{11})
            new(c.data[1], #id
                0, 0, 0, 0, 0,  #phi, theta, zo, m, M_abs
                c.data[2], 0, 0, c.data[11], #Mgal, z, r, w
                c.data[11], #final_w
                c.data[3], #radius
                c.data[4], #spin
                c.data[5],c.data[6], c.data[7],  #posxyz
                c.data[8], c.data[8], c.data[10] #velxyz
                )
        end
    end

    struct DimensionSpec{N} end

    d1d = DimensionSpec{1}()
    d2d = DimensionSpec{2}()
    d3d = DimensionSpec{3}()

    struct State
        info::Dict{String,Any}
        descriptors::Dict{Int,Array{GalaxyDescriptor,1}}
        function State()
            new(Dict{String,Any}(), Dict{Int,Array{GalaxyDescriptor,1}}())
        end
    end

    struct GhostPlanes end

#    function get_ghost_plane()
#    end

    function get(state::State, name::String, ::Type{T}; synchronous=false) where {T}
        return T(state.info[name])
    end

    function autosize_array(state::State, name::String, ::Bool, ::Type{T}, ::DimensionSpec{N})  where{T,N}
    end

    function resize_array(state::State, name::String, N::Int, ::Type{T}, cppOrder=true) where {T}
        a = Array{T,1}(undef, N)
        L = min(N, length(state.info[name]))
        a[1:L] .= state.info[name][1:L]
        state.info[name] = a
        return a
    end

    function new_array(state::State, name::String, N::Int, ::Type{T}, cppOrder=true) where {T}
        a = Array{T,1}(undef, N)
        state.info[name] = a
        return a
    end

    function get_galaxy_descriptor(state::State, catalog::Int)
        state.descriptors[catalog]
    end

    @enum LOG_LEVEL LOG_INFO=0 LOG_VERBOSE=1 LOG_DEBUG=2 LOG_ERROR=3

    function uniform(state::State)
        rand(Float64)
    end

    function get_array(state::State, name::String, ::Type{T}, ::DimensionSpec{N}) where {T,N}
        return state.info[name]
    end

    struct BadGradient <: Exception end

    function prefix(id::LOG_LEVEL)
        if id == LOG_INFO
            return "INFO   "
        elseif id == LOG_VERBOSE
            return "VERBOSE"
        elseif id == LOG_DEBUG
            return "DEBUG "
        elseif id == LOG_ERROR
            return "ERROR "
        end
        return "WEIRD"
    end

    function print(id, text)
        println("[$(prefix(id))] $(text)")
    end


end

include(JULIA_LIKELIHOOD)

using HDF5
using NPZ

state = libLSS.State()

state.info["NCAT"] = 1
state.info["startN0"] = 0
state.info["localN0"] = 32
state.info["N0"] = 32
state.info["N1"] = 32
state.info["N2"] = 32
state.info["MCMC_STEP"] = 1

state.info["halo_rnd"] = npzread("rnd.npy")

data = h5read("halo_full.h5", "data")
state.descriptors[0] = libLSS.GalaxyDescriptor.(data)
libLSS.new_array(state, "galaxy_bias_0", 1, Float64)
ghosts = libLSS.GhostPlanes()

lkl_julia.initialize(state)

primary_pars = libLSS.get(state, "galaxy_bias_0", Array{Float64,1})
#primary_pars=[-0.184885, -10.9406, 0.201633, -2.0811, 26.0899, 0.425483, 0.933645]
#primary_pars=[-1.40152, -1.81401, 3.15168, 2.19131, 31.4598, 1.03612, -0.403347,-0.576611, -37.0138, 4.32735, -8.23236, -0.374622]
#primary_pars=[-1.5537, -2.00498, -10.4029, 2.09403, 30.367, 0.0492851, 0.682411, -1.19255, -7.96303, 2.81621, 31.0215, -1.71585]
#primary_pars=[-5.07158, -5.40877, -22.1815, 6.7823, 11.8081 , 6.26203, -80.481, -0.635414, -194.427, 1.07606, 116.867, -3.16294]

#primary_pars = [-3.85992, -4.13413, -16.7243, 4.96438, 19.1427, 3.14645, -0.886257, -0.843103, -151.239, 1.7652, 109.884, -2.72664]
#primary_pars = [-3.89838, -4.16932, -16.8285, 5.01234, 18.9541, 3.19879, -0.870979, -0.837335, -151.525, 1.74808, 113.346, -2.75558]
##++
primary_pars = [-3.89838, -4.16932, -16.8285, 5.01234, 18.9541, 3.19879, -0.870979, -0.837335, -151.525, 1.74808, 111.346, -2.75558]
##++
#primary_pars = [-2.80186, -3.16606, -13.8643, 3.6514, 24.3226, 1.6907, -1.30828, -1.00266, -239.525, 2.23281, -15.442, -1.67615]

density = Array{Float64, 3}(undef, 32, 32, 32)
u = sin.((0:1:31).*2pi/32)*0.8
density .= reshape(u, :, 1, 1).*reshape(u, 1, 1, :).*reshape(u, 1, :, 1)

Lref=lkl_julia.likelihood_bias(state, ghosts, density, 0, primary_pars)

ag_bias = Array{Float64,1}(undef, size(primary_pars))
lkl_julia.adjoint_bias(state, ghosts, density, 0, primary_pars, ag_bias)
@time lkl_julia.adjoint_bias(state, ghosts, density, 0, primary_pars, ag_bias)


if true 
ag_bias2 = Array{Float64,1}(undef, size(primary_pars))
for i in 1:length(primary_pars)
    prim2 = deepcopy(primary_pars)
    dx = 0.00001*abs(prim2[i])
    prim2[i] += dx
    ag_bias2[i] = lkl_julia.likelihood_bias(state, ghosts, density, 0, prim2)
    prim2[i] = primary_pars[i] - dx
    ag_bias2[i] -= lkl_julia.likelihood_bias(state, ghosts, density, 0, prim2)
    ag_bias2[i] /= (2dx)
end
println(" Numeric is $(ag_bias2)")
end
println(" Analytic is $(ag_bias)")
