/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/ares/powerspectrum_a_sampler.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <cmath>
#include "libLSS/tools/console.hpp"
#include "libLSS/samplers/ares/powerspectrum_a_sampler.hpp"
#include "libLSS/mcmc/state_element.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"

using namespace LibLSS;

void PowerSpectrumSampler_a::base_init()
{
    ConsoleContext<LOG_DEBUG> ctx("base_init");
    
    ctx.print(boost::format("Allocating Fourier buffer %dx%dx%d") % N0 % N1 % N2_HC);
    tmp_fourier = MFCalls::alloc_complex(fourierLocalSize);
    tmp_s = MFCalls::alloc_real(2*fourierLocalSize);
    assert(tmp_fourier != 0);

    ctx.print(boost::format("Fourier buffer %p") % tmp_fourier);
    ctx.print(boost::format("Allocating plan %dx%dx%d") % N0 % N1 % N2);
    analysis_plan = MFCalls::plan_dft_r2c_3d(
                      N0, N1, N2,
                      tmp_s,
                      (FCalls::complex_type *)tmp_fourier,
#ifdef ARES_MPI_FFTW
                      comm->comm(),
#endif
                      //FFTW_MPI_TRANSPOSED_OUT|
                      FFTW_DESTROY_INPUT|FFTW_MEASURE);

    flat_keys = new FlatIntType(keys->array->data(), boost::extents[keys->array->num_elements()] );
}

void PowerSpectrumSampler_a::restore(MarkovState& state)
{
    ConsoleContext<LOG_INFO> ctx("restoration of power spectrum sampler (a)");
    
    restore_base(state);
    
    base_init();
}

void PowerSpectrumSampler_a::initialize(MarkovState& state)
{
    ConsoleContext<LOG_INFO> ctx("initialization of power spectrum sampler (a)");
     
    initialize_base(state);

    base_init();
}

PowerSpectrumSampler_a::PowerSpectrumSampler_a(MPI_Communication *comm0)
    : PowerSpectrumSampler_Base(comm0), tmp_fourier(0), flat_keys(0), tmp_s(0)
{
}


PowerSpectrumSampler_a::~PowerSpectrumSampler_a()
{
    if (tmp_fourier) {
        Console::instance().print<LOG_INFO>("Cleaning up Powerspectrum sampler (a)");

        MFCalls::free(tmp_fourier);   
        MFCalls::destroy_plan(analysis_plan);
        delete flat_keys;
    }
    if (tmp_s)
        MFCalls::free(tmp_s);
}

void PowerSpectrumSampler_a::sample(MarkovState& state)
{
    // Grab the messenger field
    ConsoleContext<LOG_DEBUG> ctx("PowerSpectrumSampler_a::sample");
    Console& cons = Console::instance();
    ArrayType& s_field = static_cast<ArrayType&>(state["s_field"]);

    //return;
    IArrayType1d::ArrayType& nmode_array = *nmode->array;
    ArrayType1d::ArrayType& P_array = *P->array;

    
    if (state.get<SBool>("power_sampler_a_blocked")->value)
        return;
    
    copy_padded_data(*s_field.array, tmp_s);
    MFCalls::execute(analysis_plan);

    ctx.print("Compute inverse-gamma parameter");

    std::fill(P_array.begin(), P_array.end(), 0);
    
    ctx.print(boost::format("N_fourier_elements = %d") % N_fourier_elements);
    int *adjust = adjustMul->array->data();
//#pragma omp parallel for schedule(static)
    for (long i = 0; i < local_fourier_elements; i++) {    
        FCalls::complex_type& m_hat = tmp_fourier[i];
        double Pelt = m_hat[0]*m_hat[0] + m_hat[1]*m_hat[1];
        
        // adjust increase memory bandwidth consumption. Not great...
        // OTOH it is very convenient and this loop is not the most time consuming aspect
        P_array[ (*flat_keys)[i] ] += adjust[i] * Pelt;
    }
    P_sync.mpiAllSum(*comm);

    ctx.print("Sample new power spectrum");
    
    const int alpha=1; ///Jeffreys prior

    // Only compute random numbers on rank==0, broadcast after
    if (comm->rank() == 0) {
#pragma omp parallel for schedule(static)
        for(long l = 0; l < N_k; l++) {
            if(nmode_array[l] > 0) {
                int beta = (2*alpha-2) + nmode_array[l];

                ///generate CHi-SQUARE sample
                double z2 = 0.;
                for(int j = 0; j < beta; j++) {
                    double aux=rgen->get().gaussian(); 

                    z2 += aux*aux;
                }
                ///calculate power-spectrum sample
                P_array[l] = (P_array[l]/z2) * volNorm / Ntot;
                
            }
        }
    }
    
    P_sync.mpiBroadcast(*comm);
}

