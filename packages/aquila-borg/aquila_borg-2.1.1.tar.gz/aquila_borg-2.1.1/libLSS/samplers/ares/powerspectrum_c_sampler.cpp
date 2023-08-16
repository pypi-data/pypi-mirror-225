/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/ares/powerspectrum_c_sampler.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <sstream>
#include <fstream>
#include <iostream>
#include <CosmoTool/algo.hpp>
#include <functional>
#include <cmath>
#include "libLSS/tools/console.hpp"
#include "libLSS/mcmc/state_element.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "libLSS/samplers/ares/powerspectrum_c_sampler.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/samplers/rgen/slice_sweep.hpp"
#include "libLSS/samplers/ares/ares_bias.hpp"

static const int ROOT = 0;
static const size_t LARGE_SCALE_MODE_COUNT=14;

using boost::format;
using namespace LibLSS;
using LibLSS::ARES::extract_bias;
namespace ph = std::placeholders;

PowerSpectrumSampler_c::PowerSpectrumSampler_c(MPI_Communication *comm0)
    : PowerSpectrumSampler_Coloring(comm0), counter_evaluations(0)
{
}

PowerSpectrumSampler_c::~PowerSpectrumSampler_c()
{
}

void PowerSpectrumSampler_c::base_init(MarkovState& state)
{
    ConsoleContext<LOG_DEBUG> ctx("base init");

    Ncatalog = state.get<SLong>("NCAT")->value;
    localNtot = localN0 * N1 * N2;

    // Create a counter reinitialized at each save that look at the number of posterior evaluation
    // required for each mode
    counter_evaluations = new IArrayType1d(boost::extents[P->array->num_elements()]);
    state.newElement("spectrum_c_eval_counter", counter_evaluations, true);
    counter_evaluations->setResetOnSave(0);
    counter_evaluations->fill(0);

    sigma_init = new ArrayType1d(boost::extents[P->array->num_elements()]);
    state.newElement("spectrum_c_init_sigma", sigma_init);
    sigma_init->fill(0);
}

void PowerSpectrumSampler_c::restore(MarkovState& state)
{
    ConsoleContext<LOG_INFO> ctx("restoration of power spectrum sampler (b)");

    ctx.print("Restoring power spectrum sampler (b)");

    restore_base(state);
    restore_coloring(state);

    base_init(state);

    init_sampler = false;
}

void PowerSpectrumSampler_c::initialize(MarkovState& state)
{
    ConsoleContext<LOG_INFO> ctx("initialization of power spectrum sampler (c)");
    Console& cons  = Console::instance();

    initialize_base(state);
    initialize_coloring(state);
    base_init(state);

    init_sampler = true;
}


double PowerSpectrumSampler_c::log_likelihood(MarkovState& state, int k, double P_trial)
{
    // Reuse system power spectrum
    //
    if (P_trial < 0)
      return -std::numeric_limits<double>::infinity();

    (*P->array)[k] = P_trial;
    update_s_field_from_x(state, (*P));

    // Now compute full likelihood
    double *s = state.get<ArrayType>("s_field")->array->data();
    double heat = state.getScalar<double>("ares_heat");

    double L = 0, loc_L = 0;
    for (int c = 0; c < Ncatalog; c++) {
      double Lc = 0;
      SelArrayType& sel_field = *state.get<SelArrayType>(format("galaxy_synthetic_sel_window_%d") % c);
      ArrayType& g_field = *state.get<ArrayType>(format("galaxy_data_%d") % c);
      double bias = extract_bias(state, c);
      double nmean = state.get<SDouble>(format("galaxy_nmean_%d") % c)->value;
      double *R = sel_field.array->data();
      double *gdata = g_field.array->data();

//#pragma omp simd aligned(s,R,gdata)
#pragma omp parallel for schedule(static) reduction(+:Lc)
      for (long i = 0; i < localNtot; i++) {
        if (R[i] <= 0)
          continue;
        Lc += CosmoTool::square(gdata[i] - nmean * R[i] * (1 + bias * s[i])) / (R[i]*nmean);
      }

      loc_L += Lc;
    }

    comm->reduce_t(&loc_L, &L, 1, MPI_SUM, ROOT);
//    if (comm->rank() == 0)
//      Console::instance().print<LOG_INFO>(format("Likelihood(P=%lg) = %lg") % P_trial % L);

//    o << format("%15.15lg %15.15lg")%P_trial %L<< std::endl;

    (*counter_evaluations->array)[k]++;
    return -0.5*heat*L - std::log(P_trial);
}

void PowerSpectrumSampler_c::sample(MarkovState& state)
{
    // Grab the messenger field
    ConsoleContext<LOG_INFO_SINGLE> ctx("sampling of power spectrum (c)");
    Console& cons = Console::instance();
    ArrayType& x_field = static_cast<ArrayType&>(state["x_field"]);
    RandomGen *rng = state.get<RandomGen>("random_generator");
    IArrayType1d::ArrayType& nmode_array = *nmode->array;
    ArrayType1d::ArrayType& P_array = *P->array;
    long localNtot = localN0*N1*N2;
    long step = state.get<SLong>("MCMC_STEP")->value;

    if (state.get<SBool>("power_sampler_c_blocked")->value)
        return;
    if ((step % 10) != 0) {
        return;
    }

    ctx.print("Fourier analysis (1)");
    copy_padded_data(*x_field.array, tmp_real);

    MFCalls::execute_r2c(analysis_plan, tmp_real, tmp_fourier);

    int *counts = key_counts->array->data();

    ArrayType1d::ArrayType& sigma_init_array = *sigma_init->array;
    if (init_sampler) {
      ctx.print("initial guess for the step for slice sampler...");
       for (long i = 0 ; i < P_array.size() ; i++) {
         if (counts[i] == 0)
           sigma_init_array[i] = 0;
         else
           sigma_init_array[i] = (P_array[i]) / std::sqrt(double(counts[i]));
       }
       init_sampler = false;
    }

    for (int i = 0; i < std::min(LARGE_SCALE_MODE_COUNT, P_array.size()); i++) {
   //   std::string fname = str(format("P_k_%d.txt") % i);
   //   std::ofstream f(fname.c_str());
      // Skip zero mode
      if (counts[i] == 0)
        continue;

      double cosmic_var = sigma_init_array[i];
      ctx.print(format("Finding P_array(k=%d / %d) cvar=%g") % i % P_array.size() % cosmic_var);

      auto posterior_fun =
             std::bind(&PowerSpectrumSampler_c::log_likelihood,
                         this, boost::ref(state), i, ph::_1);

      // We need the slice_sweep_double algo here. Cosmic var tends to quite underestimate
      // the width of the posterior
      if (cosmic_var >0)
        P_array[i] =
          slice_sweep_double(comm, rng->get(),
              posterior_fun,
              P_array[i], cosmic_var);

      comm->broadcast_t(&P_array[i], 1, ROOT);
    }

    update_s_field_from_x(state);

}
