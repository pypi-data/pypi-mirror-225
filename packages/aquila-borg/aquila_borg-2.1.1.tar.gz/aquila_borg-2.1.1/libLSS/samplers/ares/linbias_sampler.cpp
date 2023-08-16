/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/ares/linbias_sampler.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <boost/format.hpp>
#include <functional>
#include <cmath>
#include <CosmoTool/algo.hpp>
#include "libLSS/tools/errors.hpp"
#include "libLSS/samplers/core/gig_sampler.hpp"
#include "libLSS/samplers/ares/linbias_sampler.hpp"
#include "libLSS/samplers/rgen/slice_sweep.hpp"
#include "libLSS/samplers/ares/ares_bias.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "boost/lambda/lambda.hpp"

using namespace LibLSS;
using boost::format;
using LibLSS::ARES::extract_bias;
using LibLSS::ARES::ensure_bias_size;
namespace ph = std::placeholders;

void LinearBiasSampler::initialize(MarkovState& state)
{
    long N0, N1, N2;
    long localN0, startN0;

    ConsoleContext<LOG_DEBUG> ctx("initialization of LinearBiasSampler");
    // This sampler depends heavily on the rest of the model.
    // First grab the number of catalogs available in the markov chain

    Ncat = static_cast<SLong&>(state["NCAT"]);

    N0 = static_cast<SLong&>(state["N0"]);
    localN0 = static_cast<SLong&>(state["localN0"]);
    startN0 = static_cast<SLong&>(state["startN0"]);
    N1 = static_cast<SLong&>(state["N1"]);
    N2 = static_cast<SLong&>(state["N2"]);

    Ntot = N0*N1*N2;
    localNtot = localN0*N1*N2;
    // Ensure that the bias is at least size 1
    for (unsigned int c = 0; c < Ncat; c++)
      ensure_bias_size(state, c, boost::array<double,1>({1}));
}

void LinearBiasSampler::restore(MarkovState& state)
{
    ConsoleContext<LOG_DEBUG> ctx("restoration of LinearBiasSampler");
    initialize(state);
}


static inline double logPosteriorBias(double b, double mean, double dev, double heat)
{
  if (b < 0)
    return -std::numeric_limits<double>::infinity();

  double delta = (b-mean)/dev;

  return -0.5*delta*delta*heat;
}

void LinearBiasSampler::sample(MarkovState& state)
{
    ConsoleContext<LOG_DEBUG>  ctx("sampling of mean and bias");
    ArrayType& data_field = *state.get<ArrayType>("data_field");
    ArrayType& W = *state.get<ArrayType>("messenger_mask");
    double *G = state.get<ArrayType>("growth_factor")->array->data();
    double *s_field = state.get<ArrayType>("s_field")->array->data();
    RandomGen *rng = state.get<RandomGen>("random_generator");
    double heat = state.getScalar<double>("ares_heat");
    using boost::extents;
    using CosmoTool::square;

    if (state.get<SBool>("bias_sampler_blocked")->value)
        return;

    auto ext_Ncat = extents[Ncat];
    boost::multi_array<double, 1>
      alphas(ext_Ncat), betas(ext_Ncat),
      chis(ext_Ncat), psis(ext_Ncat), Npixs(ext_Ncat);

    // ---------------------------------------------------------
    // Time consuming part, do data reduction per sub-catalog
    // We are only computing alphas and betas here.
    for (int c = 0; c < Ncat; c++) {
        SelArrayType& sel_field = *state.get<SelArrayType>(format("galaxy_synthetic_sel_window_%d") % c);
        double *g_field = state.get<ArrayType>(format("galaxy_data_%d") % c)->array->data();
        double& bias = extract_bias(state, c);
        SDouble *g_nmean = state.get<SDouble>(format("galaxy_nmean_%d") % c);
        double nmean = g_nmean->value;

        const auto &sel_array = sel_field.array->data();
        double loc_alpha = 0, loc_beta = 0, loc_psi = 0, loc_chi = 0, loc_Npix = 0, alpha = 0, beta = 0;

#pragma omp parallel for schedule(dynamic, 1024) reduction(+:loc_alpha,loc_beta,loc_chi,loc_psi,loc_Npix)
        for (long i = 0; i < localNtot; i++) {
            double selection = sel_array[i];
            if (selection > 0) {
                double Nobs = g_field[i];
                double Dplus = G[i];
                double density = s_field[i];
                double aux_gamma = 1 + bias * Dplus * density;

                loc_beta += selection * nmean * Dplus * Dplus * density * density;
                loc_alpha += (Nobs - selection*nmean) * Dplus * density;
                loc_chi += Nobs*Nobs/selection;
                loc_psi += selection * aux_gamma * aux_gamma;
                loc_Npix++;
            }
        }

        // Store the partial result and continue
        alphas[c] = loc_alpha;
        betas[c] = loc_beta;
        chis[c] = loc_chi;
        psis[c] = loc_psi;
        Npixs[c] = loc_Npix;
    }

    // Final reduction
    ctx.print("Reducing result");
    comm->all_reduce_t(MPI_IN_PLACE, alphas.data(), Ncat, MPI_SUM);
    comm->all_reduce_t(MPI_IN_PLACE, betas.data(), Ncat, MPI_SUM);
    comm->all_reduce_t(MPI_IN_PLACE, chis.data(), Ncat, MPI_SUM);
    comm->all_reduce_t(MPI_IN_PLACE, psis.data(), Ncat, MPI_SUM);
    comm->all_reduce_t(MPI_IN_PLACE, Npixs.data(), Ncat, MPI_SUM);
    ctx.print("Done");

    for (int c = 0; c < Ncat; c++) {
        double& bias = extract_bias(state, c);
        double& nmean = state.get<SDouble>(format("galaxy_nmean_%d") % c)->value;

        double alpha = alphas[c], beta = betas[c];
        bool biasRef = state.get<SBool>(format("galaxy_bias_ref_%d") % c )->value;

        if (comm->rank() == 0 ) {// || comm->size() == 1 ) {    // Use another node */
          double lambda = 1 - 0.5*Npixs[c];

          nmean = GIG_sampler_3params(heat*psis[c],heat*chis[c],lambda,
                                               rng->get());

          ctx.print(format("Npix = %d, chi = %lg, psi = %lg") % Npixs[c] % chis[c] % psis[c]);
          ctx.print(format("Broadcast value -> nmean = %lg") % nmean);
        }

        if (!biasRef && comm->rank() == 0) {
            double mean_bias = alpha/beta;
            double dev_bias = sqrt(1/beta);

            Console::instance().c_assert(!std::isinf(mean_bias) && !std::isnan(mean_bias), "Mean is NaN or infinite");
            ctx.print(format("bias = %lg, mean_bias = %lg, dev_bias = %lg") % bias % mean_bias % dev_bias);
            bias = slice_sweep(rng->get(), std::bind(logPosteriorBias, ph::_1, mean_bias, dev_bias, heat), bias, dev_bias);

            Console::instance().c_assert(bias > 0, "Negative bias (0). Ouch!");
        }

        ctx.print("Sync bias");
        // Synchronize all nodes with the new bias value
        comm->broadcast_t(&bias, 1, 0);

        ctx.print("Sync nmean");
        // Synchronize all nodes with the new mean value
        comm->broadcast_t(&nmean, 1, 0 );

    }


    ///now improve sampling efficiency by performing a joint step in s,P(k) and biases
    ///NOTE: the following algorithm MUST be executed in sequence
    ///get RNG

    //only update if power-spectrum is sampled
    if (state.getScalar<bool>("power_sampler_a_blocked") && 
        state.getScalar<bool>("power_sampler_b_blocked") && 
        state.getScalar<bool>("power_sampler_c_blocked"))
        return;

    RandomGen *rgen = state.get<RandomGen>("random_generator");
    double factor = 1.;

    if (comm->rank() == 0) {
        for (int c = 0; c < Ncat; c++) {
            bool biasRef = state.get<SBool>(format("galaxy_bias_ref_%d") % c )->value;

            //Don't sample the reference bias
            if (biasRef)
              continue;

            //1) draw random bias realization (b1) for the first catalog
            double mean_bias = alphas[c]/betas[c];
            double dev_bias = sqrt(1./betas[c]);
            double& b0 = extract_bias(state, c);
            double b1=b0;

            ctx.print(boost::format("Slice sweeping[%d]: mean_bias = %lg, dev_bias = %lg") % c % mean_bias % dev_bias);
            b1 = slice_sweep(rng->get(), std::bind(logPosteriorBias, ph::_1, mean_bias, dev_bias, heat), b1, dev_bias);

            double fact_virt = b0/b1;

            //Now calculate hastings value for the all catalogs but the current one (this sum can be done in parallel)
            double dH=0.;
            for (int cc = 0; cc < Ncat; cc++) {

                if(c!=cc) {
                    double bb = extract_bias(state, cc);

                    //Note that we need to operate with the updated density field
                    //we calculate the metropolis factor of remaining likelihoods with respect to jumps in bias and density field
                    dH +=       2 * (1-fact_virt) * alphas[cc] * factor * bb -
                          (1-fact_virt*fact_virt) * betas[cc]*square(factor*bb);
              }
            }

            dH *= 0.5*heat;

            //now do Metropolis step
            double log_u = log(rgen->get().uniform());
            if (log_u <= -dH) {
                //update accepted bias
                b0 = b1;
                //also update the density factor
                //this accounts for updating the density and power-spectrum fields deterministically
                factor *= fact_virt;

    //            ctx.print(format("Sample accepted for catalog nr. %lg! New bias = %lg , New density factor = %lg") %c % b0 % factor);
            }
            //if sample is rejected then simply continue
            comm->broadcast_t(&b0, 1, 0);
        }

    } else {

      // We are not root, just gather the biases as they are updated
      for (int c = 0; c < Ncat; c++) {
        bool biasRef = state.get<SBool>(format("galaxy_bias_ref_%d") % c )->value;

        //Don't sample the reference bias
        if (!biasRef) {
          double& b0 = extract_bias(state, c);

          // Update from Root rank the value of bias
          comm->broadcast_t(&b0, 1, 0);
        }
      }

    }

    // Broadcast and gather the scaling factor
    comm->broadcast_t(&factor, 1, 0);

    //Finally we just need to rescale the density and power-spectrum fields by "factor"

    //1) scale density field in real and Fourier space
    array::scaleArray3d(*state.get<ArrayType>("s_field")->array, factor);

    //2) scale power-spectrum
    ArrayType1d::ArrayType& P_info = *state.get<ArrayType1d>("powerspectrum")->array;
    LibLSS::copy_array(P_info, b_fused<double>(P_info, (factor*factor)*boost::lambda::_1));
}
