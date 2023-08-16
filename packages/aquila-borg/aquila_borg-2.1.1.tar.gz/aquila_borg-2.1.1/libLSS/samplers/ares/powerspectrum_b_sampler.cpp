/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/ares/powerspectrum_b_sampler.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <CosmoTool/algo.hpp>
#include <cmath>
#include "libLSS/tools/console.hpp"
#include "libLSS/mcmc/state_element.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "libLSS/samplers/ares/powerspectrum_b_sampler.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"

using boost::format;
using namespace LibLSS;

PowerSpectrumSampler_b::PowerSpectrumSampler_b(MPI_Communication *comm0)
    : PowerSpectrumSampler_Coloring(comm0),
      tmp_fourier(0), P0_array(boost::extents[0]), P1_array(boost::extents[0]), 
      tmp_x(0), tmp_t(0), total_accepted(0), total_tried(0), flat_keys(0)
{
}

PowerSpectrumSampler_b::~PowerSpectrumSampler_b()
{
    if (tmp_fourier) {
        Console::instance().print<LOG_INFO>("Cleaning up Powerspectrum sampler (b)");
        Console::instance().print<LOG_DEBUG>(format("tmp_fourier=%p tmp_fourier=%p") % tmp_fourier % tmp_fourier_t);

        FCalls::free(tmp_fourier);   
        FCalls::free(tmp_fourier_t);   
        FCalls::destroy_plan(analysis_plan);
    }
    if (tmp_x)
        MFCalls::free(tmp_x);
    if (tmp_t)
        MFCalls::free(tmp_t);
    if (flat_keys)
        delete flat_keys;
}

void PowerSpectrumSampler_b::base_init(MarkovState& state)
{
    ConsoleContext<LOG_DEBUG> ctx("base init");
    
    ctx.print(boost::format("Allocating Fourier buffer %dx%dx%d (sz=%d)") % localN0 % N1 % N2_HC % fourierLocalSize);
    tmp_fourier = MFCalls::alloc_complex(fourierLocalSize);
    tmp_fourier_t = MFCalls::alloc_complex(fourierLocalSize);
    tmp_x = MFCalls::alloc_real(2*fourierLocalSize);
    tmp_t = MFCalls::alloc_real(2*fourierLocalSize);
    P0_array.resize(boost::extents[N_k]);
    P1_array.resize(boost::extents[N_k]);
    
    ctx.print(boost::format("Fourier buffer %p") % tmp_fourier);
    ctx.print(boost::format("Allocating plan %dx%dx%d") % N0 % N1 % N2);
    analysis_plan = MFCalls::plan_dft_r2c_3d(
                      N0, N1, N2,
                      tmp_x, 
                      tmp_fourier,
#ifdef ARES_MPI_FFTW
                      comm->comm(),
#endif
                      //FFTW_MPI_TRANSPOSED_OUT|
                      FFTW_DESTROY_INPUT|FFTW_MEASURE);

    flat_keys = new FlatIntType(keys->array->data(), boost::extents[keys->array->num_elements()] );

    state.newElement("sampler_b_accepted", new SLong());
    state.newElement("sampler_b_tried", new SLong());
}

void PowerSpectrumSampler_b::restore(MarkovState& state)
{
    ConsoleContext<LOG_INFO> ctx("restoration of power spectrum sampler (b)");
    
    ctx.print("Restoring power spectrum sampler (b)");
    
    restore_base(state);
    restore_coloring(state);

    base_init(state);
    
}

void PowerSpectrumSampler_b::initialize(MarkovState& state)
{
    ConsoleContext<LOG_INFO> ctx("initialization of power spectrum sampler (b)");
    Console& cons  = Console::instance();

    initialize_base(state);
    initialize_coloring(state);
    base_init(state);

    state.get<SLong>("sampler_b_accepted")->value = 0;
    state.get<SLong>("sampler_b_tried")->value = 0;    
    
}


void PowerSpectrumSampler_b::sample(MarkovState& state)
{
    // Grab the messenger field
    ConsoleContext<LOG_DEBUG> ctx("sampling of power spectrum (b)");
    Console& cons = Console::instance();
    ArrayType& x_field = static_cast<ArrayType&>(state["x_field"]);
    ArrayType& t_field = static_cast<ArrayType&>(state["messenger_field"]);
    RandomGen *rng = state.get<RandomGen>("random_generator");
    IArrayType1d::ArrayType& nmode_array = *nmode->array;
    ArrayType1d::ArrayType& P_array = *P->array;
    SDouble *messenger_tau = state.get<SDouble>("messenger_tau");
    double tau = messenger_tau->value;
    long localNtot = localN0*N1*N2;

    if (state.get<SBool>("power_sampler_b_blocked")->value)
        return;

#ifdef ARES_MPI_FFTW
    copy_padded_data(*x_field.array, tmp_x);
    copy_padded_data(*t_field.array, tmp_t);
#else
    ::memcpy(tmp_x, x_field.array->data(), Ntot * sizeof(MFCalls::real_type));
    ::memcpy(tmp_t, t_field.array->data(), Ntot * sizeof(MFCalls::real_type));
#endif

    ctx.print("Fourier analysis (1)");
    MFCalls::execute(analysis_plan);
    ctx.print("Fourier analysis (2)");
    MFCalls::execute_r2c(analysis_plan, tmp_t, tmp_fourier_t);
    
    ctx.print("Compute inverse-gamma parameter");

    ctx.print(boost::format("local_fourier_elements = %d") % local_fourier_elements);
    int *adjust = adjustMul->array->data();
    
    std::fill(P0_array.begin(), P0_array.end(), 0);
    std::fill(P1_array.begin(), P1_array.end(), 0);
    
//#pragma omp parallel for schedule(static)
    for (long i = 0; i < local_fourier_elements; i++) {    
        FCalls::complex_type& x_hat = tmp_fourier[i];
        FCalls::complex_type& t_hat = tmp_fourier_t[i];
        double Pelt_cross = x_hat[0]*t_hat[0] + x_hat[1]*t_hat[1];
        double Pelt_auto  = x_hat[0]*x_hat[0] + x_hat[1]*x_hat[1];
        
        // adjust increase memory bandwidth consumption. Not great...
        // OTOH it is very convenient and this loop is not the most time consuming aspect
        P0_array[ (*flat_keys)[i] ] += adjust[i] * Pelt_cross;
        P1_array[ (*flat_keys)[i] ] += adjust[i] * Pelt_auto;
    }

    // No helper function written here. Ask MPI to reduce the arrays in-place.
    comm->all_reduce_t(MPI_IN_PLACE, P0_array.data(), P0_array.num_elements(), 
                       MPI_SUM);
    comm->all_reduce_t(MPI_IN_PLACE, P1_array.data(), P1_array.num_elements(), 
                       MPI_SUM);

    int accepted = 0, tried = 0;
    double normalization = tau * Ntot;
    
    if (comm->rank() == 0) {
        ctx.print("Accumulated, now create plausible sample");
#pragma omp parallel for schedule(static) reduction(+:accepted,tried)
        for (int i = 0; i < N_k; i++) {
            if (P1_array[i] > 0) {
                double s = 1/P1_array[i];
                P0_array[i] *= s;
                P1_array[i] = sqrt(s * normalization);
            } else {
                continue;
            }
            
            double u0 = sqrt(P_array[i] * volume);
            double u1 = -1;
            double mean = P0_array[i];
            double sigma = P1_array[i];
            assert(!std::isnan(u0));
            assert(!std::isnan(mean));
            assert(!std::isnan(sigma));
            ctx.print(format(" k = %lg, mean = %lg, sigma = %lg")  % (*k->array)[i]% mean % sigma);
            if (mean < 0) mean = 0;
            while(u1 < 0) 
                u1 = mean + sigma*rng->get().gaussian(); ///NOTE: sample from truncated Gaussian
        
            double PA = u1/u0;
            if(PA>1.) 
                PA=1.;
            
            double u = rng->get().uniform();
            if (u < PA) {        
                P_array[i] = u1*u1 / volume;
                accepted++;
            }
            tried++;
        }
    }
    
    ctx.print("Broadcast data");
    P_sync.mpiBroadcast(*comm);
        
    total_accepted += accepted;
    total_tried += tried;
    
    // Force update s_field with the new P
    update_s_field_from_x(state);
    
    state.get<SLong>("sampler_b_accepted")->value = total_accepted;
    state.get<SLong>("sampler_b_tried")->value = total_tried;

    if (comm->rank() == 0)
        Console::instance().print<LOG_VERBOSE>(format("PSpec sampler (b) total acceptance ratio: %2.0f %%") % (double(total_accepted)*100/total_tried));
}


