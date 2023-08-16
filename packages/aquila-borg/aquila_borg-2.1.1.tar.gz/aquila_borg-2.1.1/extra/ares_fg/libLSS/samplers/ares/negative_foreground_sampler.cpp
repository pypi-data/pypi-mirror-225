/*+
    ARES/HADES/BORG Package -- ./extra/ares_fg/libLSS/samplers/ares/negative_foreground_sampler.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <boost/format.hpp>
#include <cmath>
#include "libLSS/tools/errors.hpp"
#include "libLSS/samplers/core/gig_sampler.hpp"
#include "libLSS/samplers/ares/negative_foreground_sampler.hpp"
#include "libLSS/samplers/ares/ares_bias.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/array_tools.hpp"
#include <boost/phoenix/core/argument.hpp>
#include <boost/phoenix/operator.hpp>
#include <CosmoTool/algo.hpp>
#include <cmath>

using namespace LibLSS;
using LibLSS::ARES::extract_bias;
//using LibLSS::ARES::extract_ares_noise;
using boost::format;
using CosmoTool::square;
using std::min;
using std::max;

using boost::extents;

typedef boost::multi_array_types::extent_range range;

// We are going to mix less here in favor of more mixing with nbar
static const int mixing_foreground = 3;
//static const int mixing_foreground = 10;

namespace LAMBDA {
  using boost::phoenix::expression::argument;

  argument<1>::type const _1 = {};
  argument<2>::type const _2 = {};
  argument<3>::type const _3 = {};
  argument<4>::type const _4 = {};
}

NegativeForegroundSampler::NegativeForegroundSampler(MPI_Communication *c, int catalog, int fg_id)
{
    this->comm = c;
    this->catalog = catalog;
    this->fg_id = fg_id;
}

void NegativeForegroundSampler::initialize(MarkovState& state)
{
    ConsoleContext<LOG_INFO> ctx("initialization of negative foreground sampler");
    N0 = static_cast<SLong&>(state["N0"]);
    localN0 = static_cast<SLong&>(state["localN0"]);
    startN0 = static_cast<SLong&>(state["startN0"]);
    N1 = static_cast<SLong&>(state["N1"]);
    N2 = static_cast<SLong&>(state["N2"]);

    Ntot = N0*N1*N2;
    localNtot = localN0*N1*N2;
    
    rng = state.get<RandomGen>("random_generator");


}

void NegativeForegroundSampler::restore(MarkovState& state)
{
    initialize(state);
    
}

void NegativeForegroundSampler::sample(MarkovState& state)
{
    ConsoleContext<LOG_DEBUG> ctx(str(format("sampling of negative foreground (catalog %d, foreground %d)") % catalog % fg_id));
    ArrayType *G = state.get<ArrayType>("growth_factor");
    ArrayType *s = state.get<ArrayType>("s_field");
    ArrayType *g_field = state.get<ArrayType>(format("galaxy_data_%d") % catalog);
    double bias = extract_bias(state, catalog);
    double nmean = state.getScalar<double>(format("galaxy_nmean_%d") % catalog);
    //double sigma = extract_ares_noise(state, catalog);
    double sigma2 = nmean;//sigma*sigma;
    SelArrayType *original_selection_grid = state.get<SelArrayType>(format("galaxy_sel_window_%d") % catalog);
    ArrayType1d *fg_coefficient = state.get<ArrayType1d>(format("catalog_foreground_coefficient_%d") % catalog);
    IArrayType1d *fg_map_id = state.get<IArrayType1d>(format("catalog_foreground_maps_%d") % catalog);
    double heat = state.getScalar<double>("ares_heat");

    if (state.getScalar<bool>("total_foreground_blocked") || state.getScalar<bool>(format("negative_foreground_%d_%d_blocked") % catalog % fg_id))
        return;

    typedef UninitializedArray<ArrayType::ArrayType> U_ArrayType;
    typedef U_ArrayType::array_type atype;
    U_ArrayType u_beta_i(extents[range(startN0,startN0+localN0)][N1][N2]);
    U_ArrayType u_gamma_i(extents[range(startN0,startN0+localN0)][N1][N2]);
    U_ArrayType u_Ai(extents[range(startN0,startN0+localN0)][N1][N2]);
    U_ArrayType u_Bi(extents[range(startN0,startN0+localN0)][N1][N2]);
    atype& beta_i = u_beta_i;
    atype& gamma_i = u_gamma_i;
    atype& Ai = u_Ai;
    atype& Bi = u_Bi;
    using LAMBDA::_1;
    using LAMBDA::_2;
    using LAMBDA::_3;
    using LAMBDA::_4;

    ArrayType *fgmap;
    int Ncoef = fg_coefficient->array->num_elements();
    SelArrayType::ArrayType::index_gen s_indices;
    atype::index_gen g_indices;
    typedef SelArrayType::ArrayType::index_range s_range;
    typedef atype::index_range g_range;
    
    LibLSS::copy_array_rv(
        gamma_i[g_indices[g_range()][g_range()][g_range()]], 
        b_fused<double>(
          (*original_selection_grid->array)[s_indices[s_range()][s_range()][s_range()]], 
          _1) );
    for (int e = 0; e < Ncoef; e++) {
        if (e == fg_id)
            continue;

        fgmap = state.get<ArrayType>(format("foreground_3d_%d") % (*fg_map_id->array)[e]);
        
        double coef = (*fg_coefficient->array)[e];
        LibLSS::copy_array(gamma_i, 
          b_fused<double>(gamma_i,  
                  *(fgmap->array), 
                  _1*(1-coef*_2)));
    }
    
    fgmap = state.get<ArrayType>(format("foreground_3d_%d") % (*fg_map_id->array)[fg_id]);
    
    // This is gamma_i in the paper
    LibLSS::copy_array(beta_i, b_fused<double>(gamma_i, *fgmap->array, _1*_2));

    // This is C_i  in the paper.
    LibLSS::copy_array(Bi, b_fused<double>(beta_i, *G->array, *s->array, _1*nmean*(1+bias*_2*_3)));
    // This is B_i in the paper appendix A
    LibLSS::copy_array(Ai, b_fused<double>(*g_field->array, gamma_i, *G->array, *s->array, _1 - _2*nmean*(1+bias*_3*_4)));
    
    long Active = 0, loc_Active = 0;
    double loc_z_g = 0, z_g = 0, w_g = 0;
    double *beta_i_data = beta_i.data();
    double *Bi_data = Bi.data();
    double *Ai_data = Ai.data();
    double *gamma_i_data = gamma_i.data();
    double loc_omega = 0, omega = 0;
    auto& fg_array = *(fgmap->array);
    
#pragma omp parallel for schedule(dynamic, 1000) collapse(3) reduction(+:loc_z_g,loc_Active) reduction(max:loc_omega)
    for (long n0 = startN0; n0 < startN0+localN0; n0++) {
      for (long n1 = 0; n1 < N1; n1++) {
        for (long n2 = 0; n2 < N2; n2++) {
          double beta = beta_i[n0][n1][n2];

          if (beta <= 0)
            continue;
          loc_z_g += square(Bi[n0][n1][n2])/beta;
          loc_Active ++;
        
          loc_omega = max(loc_omega, fg_array[n0][n1][n2]);
        }
      }
    }
    ctx.print(format("loc_omega = %lg, loc_Active=%d") % loc_omega % loc_Active);
    comm->all_reduce_t(&loc_z_g, &z_g, 1, MPI_SUM);
    comm->all_reduce_t(&loc_Active, &Active, 1, MPI_SUM);
    comm->all_reduce_t(&loc_omega, &omega, 1, MPI_MAX);
    omega = 1/omega;
    omega *= 0.9;
    
    z_g /= sigma2;

    double xi = omega - (*fg_coefficient->array)[fg_id];
    
    ctx.print(format("Got omega = %lg, xi(initial) = %lg, z_g=%lg, Active=%d") % omega % xi % z_g % Active);
    
    for (int m = 0; m < mixing_foreground; m++) {
        double w_g, loc_w_g = 0;
        
        loc_w_g = w_g = 0;
#pragma omp parallel for schedule(dynamic, 1000) reduction(+:loc_w_g) 
        for (long n = 0; n < localNtot; n++) {
            double t;
            double beta = beta_i_data[n];
            
            if (beta <= 0)
                continue;
            
            double A = Ai_data[n];
            double B = Bi_data[n];
            double gamma = gamma_i_data[n];
            
            double gammatilde = gamma - omega * beta;
            double variance_t = sigma2 * gammatilde * beta * xi / (gammatilde  + beta * xi) / heat;
            double mean_t = gammatilde / (gammatilde  + beta * xi) * (A + B*(omega-xi));

            Console::instance().c_assert(!std::isnan(mean_t), "NaN in mean");
            Console::instance().c_assert(!std::isnan(variance_t), "NaN in variance");
            if (gammatilde < 0) {
              Console::instance().print<LOG_ERROR>(format("Gammatilde = %lg") % gammatilde);
              Console::instance().c_assert(gammatilde >= 0, "gammatilde should be positive");
            }
            t = rng->get().gaussian() * sqrt(variance_t) + mean_t;
            loc_w_g += square(A + B*omega - t) / beta;            
            if (std::isnan(loc_w_g)) {
              ctx.print(format("nan detected for loc_w_g, A=%lg, B=%lg, t=%lg, n=%d, mean_t=%lg, variance_t=%lg, beta=%lg")  % A % B % t % n % mean_t % variance_t % beta);
              Console::instance().c_assert(false, "NaN in mean");
            }
        }

//        ctx.print2<LOG_DEBUG>(format("Built loc_w_g = %lg") % loc_w_g);
        comm->reduce_t(&loc_w_g, &w_g, 1, MPI_SUM, 0);
//        ctx.print2<LOG_DEBUG>(format("Built w_g = %lg") % w_g);
//

        if (comm->rank() == 0) {
//           ctx.print2<LOG_DEBUG>(format("Got w_g = %lg after reduction") % w_g);
//
           w_g /= sigma2;
           Console::instance().c_assert(!std::isnan(w_g), "NaN in mean");
           xi = GIG_sampler_3params(z_g*heat,w_g*heat,1 - 0.5*heat*Active,
                                    rng->get());
        }
        comm->broadcast_t(&xi, 1, 0);
 //       ctx.print2<LOG_DEBUG>(format("Broadcast xi = %lg") % xi);
    }
    
    ctx.print(format("xi(final) = %lg, thus alpha=%lg") % xi % (omega-xi));
    (*fg_coefficient->array)[fg_id] = omega - xi;
}
