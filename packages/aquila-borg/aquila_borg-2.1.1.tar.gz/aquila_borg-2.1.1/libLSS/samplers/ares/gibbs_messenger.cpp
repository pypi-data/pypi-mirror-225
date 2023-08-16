/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/ares/gibbs_messenger.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <Eigen/Core>
#include <cmath>
#include <boost/format.hpp>
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/ares/gibbs_messenger.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/samplers/ares/ares_bias.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_assign.hpp"
#include "libLSS/tools/array_tools.hpp"

using namespace LibLSS;
using boost::format;
using boost::extents;
using LibLSS::ARES::extract_bias;

typedef boost::multi_array_types::extent_range range;

typedef Eigen::Map<Eigen::ArrayXd, Eigen::Aligned> MappedArray;

/* (data,s) -> t sampler
 */

MessengerSampler::MessengerSampler(MPI_Communication * comm_)
    : comm(comm_), constrainedGeneration(true), mgr(0)
{
}

MessengerSampler::~MessengerSampler()
{
  if (mgr != 0)
    delete mgr;
}

void MessengerSampler::restore(MarkovState& state)
{
    initialize(state);
}

void MessengerSampler::initialize(MarkovState& state)
{
    ArrayType *messenger;
    Console& cons = Console::instance();

    cons.print<LOG_INFO>("Initialize Messenger sampler");
    cons.indent();

    N0 = state.get<SLong>("N0")->value;
    N1 = state.get<SLong>("N1")->value;
    N2 = state.get<SLong>("N2")->value;

    mgr = new FFTMgr(N0, N1, N2, comm);

    startN0 = mgr->startN0;
    localN0 = mgr->localN0;

    Ntot = N0*N1*N2;
    localNtot = localN0*N1*N2;

    N_k = state.get<SLong>("NUM_MODES")->value;

    rng = state.get<RandomGen>("random_generator");

    cons.print<LOG_DEBUG>("Allocating messenger field");
    messenger = new ArrayType(extents[range(startN0,startN0+localN0)][N1][N2]);
    messenger->setRealDims(ArrayDimension(N0, N1, N2));
    cons.print<LOG_DEBUG>(format("Allocated messenger_field %p") % messenger->array->data());
    cons.print<LOG_DEBUG>("Allocating messenger field");
    messenger_mask = new ArrayType(extents[range(startN0,startN0+localN0)][N1][N2]);
    messenger_mask->setRealDims(ArrayDimension(N0, N1, N2));
    cons.print<LOG_DEBUG>("Allocating mixed data field");
    data_field = new ArrayType(extents[range(startN0,startN0+localN0)][N1][N2]);
    data_field->setRealDims(ArrayDimension(N0, N1, N2));

    state.newElement("messenger_field", messenger);
    state.newElement("messenger_mask", messenger_mask);
    state.newElement("messenger_tau", messenger_tau = new SDouble());
    state.newElement("data_field", data_field);

    cons.unindent();
    cons.print<LOG_INFO>("Done");
}

void MessengerSampler::sample(MarkovState& state)
{
    ConsoleContext<LOG_DEBUG> ctx("MessengerSampler::sample");
    ArrayType& s_field = static_cast<ArrayType&>(state["s_field"]);
    ArrayType::ArrayType& m_field = *state.get<ArrayType>("messenger_field")->array;
    ArrayType& data_field = static_cast<ArrayType&>(state["data_field"]);
    // We need the 3d messenger mask/window
    ArrayType& W = *messenger_mask;
    // We need the random generator
    SDouble& tau = *messenger_tau;
    double sqrt_tau = std::sqrt(tau);

    if (constrainedGeneration) {
#pragma omp parallel
{
        auto &rng_g = rng->get();
        const auto &W_tmp = W.array->data();
        const auto &s_tmp = s_field.array->data();
        const auto &d_tmp = data_field.array->data();
        const auto &m_tmp = m_field.data();
#pragma omp for schedule(static)
        for (long i = 0; i < localNtot; i++) {
            double A = rng_g.gaussian();
            double Wi = W_tmp[i];
            double si = s_tmp[i];
            double di = d_tmp[i];
            double mu, sigma;

            if (Wi > 0) {
                mu = (si * Wi + tau * di) / (Wi + tau);
                sigma = std::sqrt( (Wi*tau) / (Wi + tau) );
            } else if (Wi < 0){
                mu = si;
                sigma = sqrt_tau;
            } else {
                mu = di;
                sigma = 0;
            }

            m_tmp[i] = mu + sigma * A;
        }
} // end of parallel region
    } else {
        for (long i = 0; i < localNtot; i++) {
            double A = rng->get().gaussian();
            double Wi = W.array->data()[i];
            double m_i = m_field.data()[i];
            double& di = data_field.array->data()[i];

            if (Wi > 0)
                di = m_i + std::sqrt(Wi)*A;
            else
                di = 0;
            Console::instance().c_assert(!std::isnan(di), "Data is a NaN");
        }
    }
}


/* t-> s sampler
 */

MessengerSignalSampler::MessengerSignalSampler(MPI_Communication* comm)
    : flat_key(0), tmp_fourier(0), tmp_fourier_m(0), tmp_m_field(0), tmp_real_field(0), analysis_plan(0), synthesis_plan(0),
      constrainedGeneration(true), comm(comm), mgr(0)
{
}

void MessengerSignalSampler::restore(MarkovState& state)
{
    initialize(state);
}

void MessengerSignalSampler::initialize(MarkovState& state)
{
    Console& cons = Console::instance();
    ConsoleContext<LOG_INFO> ctx("Messenger-Signal sampler");

    N0 = static_cast<SLong&>(state["N0"]);
    N1 = static_cast<SLong&>(state["N1"]);
    N2 = static_cast<SLong&>(state["N2"]);

    mgr = new FFTMgr(N0, N1, N2, comm);

    // This for MPI support
    startN0 = mgr->startN0;
    localN0 = mgr->localN0;
    fourierLocalSize = mgr->allocator_real.minAllocSize;

    N_k = state.get<SLong>("NUM_MODES")->value;

    L0 = static_cast<SDouble&>(state["L0"]);
    L1 = static_cast<SDouble&>(state["L1"]);
    L2 = static_cast<SDouble&>(state["L2"]);

    if (tmp_fourier) {
        error_helper<ErrorBadState>("MessengerSignalSampler has already been initialized.");
    }


    cons.print<LOG_DEBUG>("Allocating x field");
    x_field = new ArrayType(extents[range(startN0,startN0+localN0)][N1][N2]);
    x_field->setRealDims(ArrayDimension(N0, N1, N2));
    cons.print<LOG_DEBUG>("Allocating s field");
    s_field = new ArrayType(extents[range(startN0,startN0+localN0)][N1][N2]);
    s_field->setRealDims(ArrayDimension(N0, N1, N2));
    state.newElement("x_field", x_field);
    state.newElement("s_field", s_field, true);

    s_field->eigen().fill(0);
    x_field->eigen().fill(0);

    Ntot = N0*N1*N2;
    Ntot_k = N0*N1*(N2/2+1);

    localNtot = localN0*N1*N2;
    localNtot_k = localN0*N1*(N2/2+1);

    volume = L0*L1*L2;
    volNorm = volume/Ntot;

    ctx.print(format("fourierLocalSize = %d") % fourierLocalSize);
    tmp_fourier = MFCalls::alloc_complex(fourierLocalSize);
    tmp_fourier_m = MFCalls::alloc_complex(fourierLocalSize);


#ifndef ARES_MPI_FFTW
    ctx.print("Creating FFTW plans for Messenger-Signal");
    tmp_m_field = new ArrayType(boost::extents[range(startN0,startN0+localN0)][N1][N2]);
    ctx.print(format("Allocated tmp_m_field %p") % tmp_m_field->array->origin());
    analysis_plan = MFCalls::plan_dft_r2c_3d(
                      N0, N1, N2,
                      x_field->array->data(),
                      tmp_fourier,
                      FFTW_DESTROY_INPUT|FFTW_MEASURE);
    synthesis_plan = MFCalls::plan_dft_c2r_3d(
                       N0, N1, N2,
                       tmp_fourier,
                       x_field->array->data(),
                       FFTW_DESTROY_INPUT|FFTW_MEASURE);
#else
    ctx.print("Creating MPI/FFTW plans for Messenger-Signal");
    tmp_real_field = MFCalls::alloc_real(fourierLocalSize*2);
    analysis_plan = MFCalls::plan_dft_r2c_3d(
                      N0, N1, N2,
                      tmp_real_field,
                      tmp_fourier,
                      comm->comm(),
                     // FFTW_MPI_TRANSPOSED_OUT|
                      FFTW_DESTROY_INPUT|FFTW_MEASURE);
    synthesis_plan = MFCalls::plan_dft_c2r_3d(
                      N0, N1, N2,
                      tmp_fourier,
                      tmp_real_field,
                      comm->comm(),
                      //FFTW_MPI_TRANSPOSED_IN|
                      FFTW_DESTROY_INPUT|FFTW_MEASURE);
#endif
    ctx.print(format("allocated tmp_fourier(%p) tmp_fourier_m(%p) and tmp_real_field(%p)") % tmp_fourier % tmp_fourier_m% tmp_real_field);
    ctx.print("Done creating FFTW plans for Messenger-Signal");
}


MessengerSignalSampler::~MessengerSignalSampler()
{
    if (tmp_fourier) {
        Console::instance().print<LOG_INFO>("Cleaning up Messenger-Signal");

#ifdef ARES_MPI_FFTW
        delete tmp_m_field;
#endif
        if (flat_key)
            delete flat_key;
        if (tmp_fourier)
            MFCalls::free(tmp_fourier);
        if (tmp_fourier_m)
            MFCalls::free(tmp_fourier_m);
        if (tmp_real_field)
            MFCalls::free(tmp_real_field);
        if (analysis_plan)
            MFCalls::destroy_plan(analysis_plan);
        if (synthesis_plan)
            MFCalls::destroy_plan(synthesis_plan);

        if (mgr)
          delete mgr;
    }
}


void MessengerSignalSampler::sample(MarkovState& state)
{
    ConsoleContext<LOG_DEBUG> ctx("MessengerSignalSampler::sample");
    RandomGen& rng = static_cast<RandomGen&>(state["random_generator"]);
    ArrayType& m_field = *state.get<ArrayType>("messenger_field");
    ArrayType1d::ArrayType& P_info = *state.get<ArrayType1d>("powerspectrum")->array;
    SDouble& tau = static_cast<SDouble&>(state["messenger_tau"]);
    IArrayType::ArrayType& P_key = *state.get<IArrayType>("k_keys")->array; // Built by powerspec_tools

    ArrayType& x = *x_field;
    ArrayType& s = *s_field;
    double alpha = 1/std::sqrt(double(Ntot));
    Console& cons = Console::instance();

    ctx.print("Sample messenger-signal");

    if (state.get<SBool>("messenger_signal_blocked")->value && constrainedGeneration)
        return;

    // We have to initialize this lazily. k_keys is created by powerspectrum samplers.
    if (flat_key == 0) {
        IArrayType *keys = state.get<IArrayType>("k_keys");
        flat_key = new FlatIntType( keys->array->data(), boost::extents[keys->array->num_elements()] );
    }

#pragma omp parallel
{
    auto &rng_g = rng.get();
    const auto &data = x.array->data();
#pragma omp for schedule(static)
    for (long i = 0; i < localNtot; i++) {
        data[i] = rng_g.gaussian()*alpha;
    }
}
    copy_padded_data(*x.array, tmp_real_field, true);
    // This destroy the x_field. Not a problem. synthesis is regenerating it
    MFCalls::execute(analysis_plan);
#ifdef ARES_MPI_FFTW
    copy_padded_data(*m_field.array, tmp_real_field);
    MFCalls::execute_r2c(analysis_plan, tmp_real_field, tmp_fourier_m);
#else
    // This destroy the m_field. Could be annoying.
    tmp_m_field->eigen() = m_field.eigen();
    FCalls::execute_r2c(analysis_plan, m_field.array->data(), tmp_fourier_m);
#endif

    if (constrainedGeneration) {
        double scaler = 1/volNorm;
        double T = tau * volume;

        boost::multi_array<double, 1> sqrtP(boost::extents[N_k]);
        boost::multi_array<double, 1> A1(boost::extents[N_k]);
        boost::multi_array<double, 1> A2(boost::extents[N_k]);

        LibLSS::copy_array(sqrtP,
           b_fused<double>(P_info,
                  [this,scaler](double x)->double const { return x < 0 ? 0 : std::sqrt(x*volume);}
           )
        );
        LibLSS::copy_array(A1,
           b_fused<double>(P_info, sqrtP,
                           [this,scaler,T](double x,double y)->double const { return x < 0 ? 0 :  y/(T+x*volume*scaler); })
        );
        LibLSS::copy_array(A2,
           b_fused<double>(P_info,
                   [this,scaler,T](double x)->double const { return x < 0 ? 0 : std::sqrt(T/(T+x*volume*scaler)); })
        );

#pragma omp parallel for schedule(static)
        for (long i = 0; i < localNtot_k; i++) {
            long key = (*flat_key)[i];
            double color_P = sqrtP[key];
            double aux1 = A1[key];
            double aux2 = A2[key];
            MFCalls::complex_type& white_phase = tmp_fourier_m[i];
            MFCalls::complex_type& random_phase = tmp_fourier[i];
            MFCalls::complex_type& colored_phase = tmp_fourier_m[i];

            random_phase[0] = aux1 * white_phase[0] + aux2 * random_phase[0];
            random_phase[1] = aux1 * white_phase[1] + aux2 * random_phase[1];

            colored_phase[0] = color_P * random_phase[0];
            colored_phase[1] = color_P * random_phase[1];
        }
        if (startN0 == 0 && localN0 > 1) {
          tmp_fourier[0][0] = 0;
          tmp_fourier[0][1] = 0;
          tmp_fourier_m[0][0] = 0;
          tmp_fourier_m[0][1] = 0;
        }
    } else {
#pragma omp parallel for schedule(static)
        for (long i = 0; i < localNtot_k; i++) {
            double P = P_info[(*flat_key)[i]] * volume;
            double color_P = std::sqrt(P);
            MFCalls::complex_type& white_phase = tmp_fourier_m[i];
            MFCalls::complex_type& random_phase = tmp_fourier[i];
            MFCalls::complex_type& colored_phase = tmp_fourier_m[i];

            colored_phase[0] = color_P * random_phase[0];
            colored_phase[1] = color_P * random_phase[1];
        }
    }

    ctx.print("Fourier synthesis of phases");
    // Regenerate a correct x_field
    MFCalls::execute(synthesis_plan);
    copy_unpadded_data(tmp_real_field, *x.array, true);

    ctx.print("Fourier synthesis of signal");
    // Generate the colored s field
#ifdef ARES_MPI_FFTW
    MFCalls::execute_c2r(synthesis_plan, tmp_fourier_m, tmp_real_field);
    copy_unpadded_data(tmp_real_field, *s.array);
#else
    FCalls::execute_c2r(synthesis_plan, tmp_fourier_m, s.array->data());
    if (constrainedGeneration) {
        // Restore m_field
        m_field.eigen() = tmp_m_field->eigen();
    }
#endif

    // Just renormalize
    array::scaleArray3d(*s.array, 1.0/volume);
    array::scaleArray3d(*x.array, 1.0/volume);

    // Generate m_field in mock mode
    if (!constrainedGeneration) {
        double sq_tau = sqrt(tau);

        // Populate m_field
        for (long i = 0; i < localNtot; i++)
            m_field.array->data()[i] = s.array->data()[i] + rng.get().gaussian()*sq_tau;
    }

}


/*
 * (catalog,meta) -> data
 */


void CatalogProjectorSampler::initialize(MarkovState& state)
{
    Ncat = static_cast<SLong&>(state["NCAT"]);
}

void CatalogProjectorSampler::restore(MarkovState& state)
{
    Ncat = static_cast<SLong&>(state["NCAT"]);
}

void CatalogProjectorSampler::sample(MarkovState& state)
{
    RandomGen& rng = static_cast<RandomGen&>(state["random_generator"]);
    ArrayType& W = *state.get<ArrayType>("messenger_mask");
    SDouble *messenger_tau = state.get<SDouble>("messenger_tau");
    ArrayType& G = *state.get<ArrayType>("growth_factor");
    ArrayType& data_field = *state.get<ArrayType>("data_field");
    // Just do vectorized operation here
    MappedArray map_W = W.eigen();
    MappedArray growth = G.eigen();
    MappedArray map_data = data_field.eigen();
    ConsoleContext<LOG_DEBUG> ctx("regenerate_W");
    double heat = state.getScalar<double>("ares_heat");

    ctx.print("Rebuild the projected data and covariance matrix");
    // Clear up W first
    map_W.fill(0);
    if (!mockGeneration)
        map_data.fill(0);
    for (int c = 0; c < Ncat; c++) {
        ctx.print(format("Looking at catalog %d") % c);

        SelArrayType& sel_field = *state.get<SelArrayType>(format("galaxy_synthetic_sel_window_%d") % c);
        ArrayType& g_field = *state.get<ArrayType>(format("galaxy_data_%d") % c);
        double& bias = extract_bias(state, c);
        double nmean = state.get<SDouble>(format("galaxy_nmean_%d") % c)->value;
        MappedArray g_data = g_field.eigen();
        MappedArray map_sel = sel_field.eigen();

        if (!mockGeneration)
            map_data += (g_data - nmean * map_sel) * bias * growth;

        map_W += map_sel * nmean * bias*bias * growth * growth;
    }
    map_W /= heat;

    ctx.print("Finish weights");

    // Hmm... I cannot use the vectorized instruction here as it depends on the positivity of map_W[i]. Just do a loop
    double tau_inverse = 0; // This is the inverse of minimum covariance

#pragma omp parallel for schedule(static)
    for (long n = 0; n < map_W.size(); n++) {
        double& val = map_W[n];

        if (val > 0) {
            if (val > tau_inverse)
                tau_inverse = val;
            val = 1/val;
        } else
            val = 0;
    }
    ctx.print(format("Got partial_tau = %lg") % (1/tau_inverse));

    comm->all_reduce(MPI_IN_PLACE, &tau_inverse, 1, translateMPIType<double>(), MPI_MAX);
    double tau = 1/tau_inverse;

    messenger_tau->value = tau;

    if (!mockGeneration)
        map_data *= map_W;
    else {
        for (int c = 0; c < Ncat; c++) {
            SelArrayType& sel_field = *state.get<SelArrayType>(format("galaxy_synthetic_sel_window_%d") % c);
            double& bias = extract_bias(state, c);
            double nmean = state.get<SDouble>(format("galaxy_nmean_%d") % c)->value;
            MappedArray map_sel = sel_field.eigen();
            ArrayType& s_field = *state.get<ArrayType>("s_field");
            ArrayType& g_field = *state.get<ArrayType>(format("galaxy_data_%d") % c);
            MappedArray s_data = s_field.eigen();
            MappedArray g_data = g_field.eigen();
            Eigen::ArrayXd err(map_sel.size());

            ctx.print(format("Catalog %d: Generate mock data with nmean = %lg, bias = %lg")  % c % nmean % bias);

            err = map_sel * nmean;

            g_data = err*(1+bias*growth*s_data);

#pragma omp parallel for schedule(static)
            for (long i = 0; i < err.size(); i++) {
                double E = err[i];
                if (E > 0) {
                    g_data[i] += rng.get().gaussian() * sqrt(E);
                } else {
                    g_data[i] = 0;
                }
            }
        }
    }

#pragma omp parallel for schedule(static)
    for (long n = 0; n < map_W.size(); n++) {
        if (map_W[n] > 0)
            map_W[n] = std::max(double(0), map_W[n] - tau);
        else
            map_W[n] = -1;
    }
    ctx.print(format("Got tau = %lg") % tau );
}
