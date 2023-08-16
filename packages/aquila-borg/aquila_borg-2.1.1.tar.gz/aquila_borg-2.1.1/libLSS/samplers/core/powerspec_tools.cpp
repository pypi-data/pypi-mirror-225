/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/core/powerspec_tools.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/tools/console.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"

using namespace LibLSS;
using boost::format;
typedef boost::multi_array_types::extent_range range;


PowerSpectrumSampler_Base::~PowerSpectrumSampler_Base()
{
  if (mgr != 0)
    delete mgr;
}

bool PowerSpectrumSampler_Base::restore_base(MarkovState& state)
{
    Console& cons = Console::instance();
    ConsoleContext<LOG_INFO> ctx("power spectrum sampler (common)");
    bool build_keys;

    L0 = *state.get<SDouble>("L0");
    L1 = *state.get<SDouble>("L1");
    L2 = *state.get<SDouble>("L2");

    N0 = *state.get<SLong>("N0");
    N1 = *state.get<SLong>("N1");
    N2 = *state.get<SLong>("N2");
    N2_HC = *state.get<SLong>("N2_HC");

    // Creates a manager. Then we get access to all derived quantities
    // for parallelism.
    mgr = new FFTMgr(N0, N1, N2, comm);


    Ntot = N0*N1*N2;
    volNorm = L0*L1*L2/Ntot;
    volume = L0*L1*L2;

    ctx.print(format("Power spectrum (%dx%dx%d), box (%gx%gx%g)") % N0 % N1 % N2 % L0 % L1 % L2);

    N_k = *state.get<SLong>("NUM_MODES");
    kmin = *state.get<SDouble>("K_MIN");
    kmax = *state.get<SDouble>("K_MAX");

    startN0 = mgr->startN0;
    localN0 = mgr->localN0;
    fourierLocalSize = mgr->allocator_real.minAllocSize;

    ctx.print(format("Num modes = %d, kmin = %lg, kmax = %lg") % N_k % kmin % kmax);

    rgen = state.get<RandomGen>("random_generator");

    if (state.exists("powerspectrum")) {
        k = state.get<ArrayType1d>("k_modes");
        keys = state.get<IArrayType>("k_keys");
        nmode = state.get<IArrayType1d>("k_nmodes");
        key_counts = state.get<IArrayType1d>("key_counts");
        P_sync += (P = state.get<ArrayType1d>("powerspectrum"));
        adjustMul = state.get<IArrayType>("adjust_mode_multiplier");

        build_keys = false;
    } else {
        cons.print<LOG_DEBUG>("Allocating power spectrum array");
        P = new ArrayType1d(boost::extents[N_k]);
        cons.print<LOG_DEBUG>("Allocating number of stacked modes array");
        nmode = new IArrayType1d(boost::extents[N_k]);
        cons.print<LOG_DEBUG>("Allocating key counts array");
        key_counts = new IArrayType1d(boost::extents[N_k]);
        cons.print<LOG_DEBUG>("Allocating mode list");
        k = new ArrayType1d(boost::extents[N_k]);

        cons.print<LOG_DEBUG>("Allocating mode keys array");
        keys = new IArrayType(mgr->extents_complex());
        keys->setRealDims(ArrayDimension(N0, N1, N2_HC));
        cons.print<LOG_DEBUG>("Mode multiplier adjustment");
        adjustMul = new IArrayType(mgr->extents_complex());
        adjustMul->setRealDims(ArrayDimension(N0, N1, N2_HC));

        state.newElement("k_modes", k);
        state.newElement("k_keys", keys);
        state.newElement("k_nmodes", nmode);
        state.newElement("key_counts", key_counts);
        P_sync += state.newElement("powerspectrum", P, true);
        state.newElement("adjust_mode_multiplier", adjustMul);

        build_keys = true;
    }

    {
        ArrayType1d::ArrayType& P_array = *P->array;

        for (long i = 0; i < N_k; i++)
            P_array[i] = 1e6;
    }

    N_fourier_elements = N0*N1*N2_HC;
    local_fourier_elements = localN0*N1*N2_HC;
    ctx.print(boost::format("N0 = %d, N1 = %d, N2 = %d, N2_HC=%d, localN0=%d, startN0=%d") % N0 % N1 % N2 % N2_HC % localN0 % startN0);



    return build_keys;
}


void PowerSpectrumSampler_Base::initialize_base(MarkovState& state)
{
    Console& cons = Console::instance();
    bool build_keys;

    build_keys = restore_base(state);

    if (!build_keys) {
        cons.print<LOG_INFO>("Keys already built. Returning.");
        return;
    }

    {
        ArrayType1d::ArrayType& k_array = *k->array;
        ArrayType1d::ArrayType& P_array = *P->array;

        for (long i = 0; i < N_k; i++) {
            k_array[i] = (kmax-kmin)/N_k * double(i);
            P_array[i] = 1e-6;
        }
    }


    // Build the powerspectrum keys
    cons.print<LOG_INFO>("Building keys");
    IArrayType::ArrayType& array_key = *keys->array;
    IArrayType1d::ArrayType& nmode_array = *nmode->array;
    IArrayType1d::ArrayType& array_key_counts = *key_counts->array;
    IArrayType::ArrayType& adjust = *adjustMul->array;

    boost::array<double, 3> L = { L0, L1, L2 };

    init_helpers::initialize_powerspectrum_keys(
        *mgr, array_key, array_key_counts, adjust, nmode_array,
        L, kmin, kmax, N_k);

}




PowerSpectrumSampler_Coloring::~PowerSpectrumSampler_Coloring()
{
  if (tmp_fourier != 0) {
    MFCalls::free(tmp_fourier);
    MFCalls::free(tmp_real);
    MFCalls::destroy_plan(analysis_plan);
    MFCalls::destroy_plan(synthesis_plan);
  }
}

bool PowerSpectrumSampler_Coloring::initialize_coloring(MarkovState& state)
{
  ConsoleContext<LOG_INFO> ctx("coloring initialization");
  tmp_fourier = MFCalls::alloc_complex(fourierLocalSize);
  tmp_real = MFCalls::alloc_real(fourierLocalSize*2);

  ctx.print("Creating MPI/FFTW plans for Messenger-Signal");
  analysis_plan = MFCalls::plan_dft_r2c_3d(
                    N0, N1, N2,
                    tmp_real,
                    tmp_fourier,
#ifdef ARES_MPI_FFTW
                    comm->comm(),
#endif
                   // FFTW_MPI_TRANSPOSED_OUT|
                    FFTW_DESTROY_INPUT|FFTW_MEASURE);
  synthesis_plan = MFCalls::plan_dft_c2r_3d(
                    N0, N1, N2,
                    tmp_fourier,
                    tmp_real,
#ifdef ARES_MPI_FFTW
                    comm->comm(),
#endif
                    //FFTW_MPI_TRANSPOSED_IN|
                    FFTW_DESTROY_INPUT|FFTW_MEASURE);

  sqrt_P_info.array->resize(boost::extents[P->array->num_elements()]);
  return true;
}

bool PowerSpectrumSampler_Coloring::restore_coloring(MarkovState& state)
{
  return initialize_coloring(state);
}

void PowerSpectrumSampler_Coloring::update_s_field_from_x(MarkovState& state, const ArrayType1d& powerSpec)
{
  ConsoleContext<LOG_DEBUG> ctx("update of s_field from x_field");
  ArrayType& x_field = *state.get<ArrayType>("x_field");
  ArrayType& s_field = *state.get<ArrayType>("s_field");

  ctx.print(format("%p") % P);
  Console::instance().c_assert(powerSpec.array->num_elements() == P->array->size(), "coloring works only on similar powerspectrum as the system one");

  // Overwrite s
  ctx.print("Copying x_field");
  copy_padded_data(*x_field.array, tmp_real);
  ctx.print("Analyzing");
  MFCalls::execute_r2c(analysis_plan, tmp_real, tmp_fourier);

  long P_size = powerSpec.array->num_elements();
  for (long i = 0; i < P_size; i++) {
    (*sqrt_P_info.array)[i] = std::sqrt((*powerSpec.array)[i] * volume) / (Ntot);
  }


  int *flat_keys = keys->array->data();

  ctx.print("Coloring");
#pragma omp parallel for schedule(static)
  for (long i = 0; i < local_fourier_elements; i++) {
    double sqrt_P = (*sqrt_P_info.array)[flat_keys[i]];

    tmp_fourier[i][0] *= sqrt_P;
    tmp_fourier[i][1] *= sqrt_P;
  }

  ctx.print("Synthesis");
  MFCalls::execute_c2r(synthesis_plan, tmp_fourier, tmp_real);
  copy_unpadded_data(tmp_real, *s_field.array);
}

void PowerSpectrumSampler_Coloring::update_s_field_from_x(MarkovState& state)
{
  update_s_field_from_x(state, *P);
}
