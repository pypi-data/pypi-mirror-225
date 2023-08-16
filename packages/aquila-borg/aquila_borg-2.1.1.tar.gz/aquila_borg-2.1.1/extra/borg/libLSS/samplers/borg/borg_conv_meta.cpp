/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/borg/borg_conv_meta.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <CosmoTool/algo.hpp>
#include <boost/bind.hpp>
#include <boost/format.hpp>
#include "libLSS/tools/errors.hpp"
#include "libLSS/samplers/core/gig_sampler.hpp"
#include "libLSS/samplers/borg/borg_conv_meta.hpp"
#include "libLSS/samplers/rgen/slice_sweep.hpp"
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/samplers/borg/borg_conv_likelihood.hpp"


using namespace LibLSS;
using namespace LibLSS::CNN;
using boost::format;
namespace ph = std::placeholders;

static const double EPSILON_VOIDS = 1e-6;

void BorgConvVobsSampler::initialize(MarkovState& state)
{
    //long N0, N1, N2;
    long localN0, startN0;

    ConsoleContext<LOG_DEBUG> ctx("initialization of BorgVobsSampler");
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

    model = state.get<BorgModelElement>("BORG_model")->obj;
//TC
    //C0 = static_cast<SLong&>(state["C0"]);
    //C1 = static_cast<SLong&>(state["C1"]);
    //C2 = static_cast<SLong&>(state["C2"]);
    tot_num_conv = static_cast<SLong&>(state["tot_num_conv"]);
//TC
}

void BorgConvVobsSampler::restore(MarkovState& state)
{
    ConsoleContext<LOG_DEBUG> ctx("restoration of BorgVobsSampler");
    initialize(state);
}

double BorgConvVobsSampler::computeLogLikelihood(MarkovState& state, double v0, double v1, double v2)
{
  using CosmoTool::square;
  ConsoleContext<LOG_VERBOSE> ctx("likelihood evaluation");

  ctx.print(format("attempting vobs = { %lg,%lg,%lg }") % v0 %v1 %v2);

  //set vobs
  double vobs_ext[]={v0,v1,v2};
  double temp = state.getScalar<double>("ares_heat");

  ctx.print(format("Temperature is %lg") % temp);

  ///now calculate likelihood over all sub-cats
  typedef ArrayType::ArrayType Array;
  typedef SelArrayType::ArrayType SArray;

  Array& G = *state.get<ArrayType>("growth_factor")->array;

  Array& final_delta = *state.get<ArrayType>("BORG_final_density")->array;

  ///just calculate 3d redshift distorted field
  ///NOTE: The sampler state of the final density field needs to be overwritten
  /// with a new final density field corresponding to vobs

  model->forwardModelRsdField(final_delta, vobs_ext);

  double H=0.;

  for (int c = 0; c < Ncat; c++) {
        SArray& sel_array = *state.get<SelArrayType>(format("galaxy_sel_window_%d") % c)->array;
        Array& g_field = *state.get<ArrayType>(format("galaxy_data_%d") % c)->array;
        SDouble *g_nmean = state.get<SDouble>(format("galaxy_nmean_%d") % c);
        double nmean =g_nmean->value;
//TC
        ArrayType1d::ArrayType &bias_params = *state.get<ArrayType1d>(format("galaxy_bias_%d") % c)->array;
        //two_arr_ref w(bias_params.data(), boost::extents[tot_num_conv][1]);
        two_arr_ref w(bias_params.data(), boost::extents[tot_num_conv][4]);
        //one_arr_ref b(bias_params.data() + tot_num_conv * 1, boost::extents[tot_num_conv]);
        one_arr_ref b(bias_params.data() + tot_num_conv * 4, boost::extents[tot_num_conv]);
           
        //four_arr weights(boost::extents[tot_num_conv][1][1][1]);                                             
        four_arr weights(boost::extents[tot_num_conv][3][3][3]);     
        for (int num_conv = 0; num_conv < tot_num_conv; num_conv++){
            //weights[num_conv][0][0][0] = w[num_conv][0];
            weights[num_conv][1][1][1] = w[num_conv][0];

            weights[num_conv][0][1][1] = w[num_conv][1];
            weights[num_conv][1][0][1] = w[num_conv][1];
            weights[num_conv][1][2][1] = w[num_conv][1];
            weights[num_conv][1][1][0] = w[num_conv][1];
            weights[num_conv][1][1][2] = w[num_conv][1];
            weights[num_conv][2][1][1] = w[num_conv][1];
        
            weights[num_conv][0][1][0] = w[num_conv][2];
            weights[num_conv][0][1][2] = w[num_conv][2];
            weights[num_conv][0][0][1] = w[num_conv][2];
            weights[num_conv][0][2][1] = w[num_conv][2];
            weights[num_conv][1][0][0] = w[num_conv][2];
            weights[num_conv][1][0][2] = w[num_conv][2];
            weights[num_conv][1][2][0] = w[num_conv][2];
            weights[num_conv][1][2][2] = w[num_conv][2];
            weights[num_conv][2][1][0] = w[num_conv][2];
            weights[num_conv][2][1][2] = w[num_conv][2];
            weights[num_conv][2][0][1] = w[num_conv][2];
            weights[num_conv][2][2][1] = w[num_conv][2];
        
            weights[num_conv][0][0][0] = w[num_conv][3];
            weights[num_conv][0][2][0] = w[num_conv][3];
            weights[num_conv][0][0][2] = w[num_conv][3];
            weights[num_conv][0][2][2] = w[num_conv][3];
            weights[num_conv][2][0][0] = w[num_conv][3];
            weights[num_conv][2][2][0] = w[num_conv][3];
            weights[num_conv][2][0][2] = w[num_conv][3];
            weights[num_conv][2][2][2] = w[num_conv][3];
        }

        H += conv_like(final_delta, sel_array, nmean, g_field, weights, b, tot_num_conv, N0, N1, N2);
//TC
    }

    ctx.print(format("Hamiltonian =  %lg") % H);
    return -H * temp;
}

void BorgConvVobsSampler::sample(MarkovState& state)
{   
    ConsoleContext<LOG_DEBUG>  ctx("SAMPLE V_OBS");

    if(state.getScalar<bool>("borg_do_rsd")==true)
    {

        RandomGen *rng = state.get<RandomGen>("random_generator");

        ///why can't i just call the model of the poisson likelihood?????

        ///I don't want to do this
        ///***************************************************************************************
        using CosmoTool::square;
        CosmologicalParameters& cosmo_params = state.getScalar<CosmologicalParameters>("cosmology");
        Cosmology cosmo(cosmo_params);

        ArrayType::ArrayType& growth = *state.get<ArrayType>("growth_factor")->array;
        double ai = state.get<SDouble>("borg_a_initial")->value;
        double D_init=cosmo.d_plus(ai) / cosmo.d_plus(1.0); // Scale factor for initial conditions

        double L0 = state.getScalar<double>("L0");
        double L1 = state.getScalar<double>("L1");
        double L2 = state.getScalar<double>("L2");

        double volume = L0*L1*L2;
        double dVol = volume / (N0 * N1 * N2);

        // Simulate forward model
        Uninit_FFTW_Complex_Array tmp_complex_field(model->lo_mgr->extents_complex(), model->lo_mgr->allocator_complex);
        ArrayType::ArrayType *out_density = state.get<ArrayType>("BORG_final_density")->array;
        CArrayType::ArrayType& s_array = *state.get<CArrayType>("s_hat_field")->array;
        // Protect the input
        array::scaleAndCopyArray3d(tmp_complex_field.get_array(), s_array, D_init/volume);
        //Hermiticity_fixup(*tmp_complex_field);

        model->setCosmoParams(state.getScalar<CosmologicalParameters>("cosmology"));
        ArrayType1d::ArrayType& vobs = *state.get<ArrayType1d>("BORG_vobs")->array;
        model->setObserver(vobs);
        model->forwardModel(tmp_complex_field, *out_density, true);
        ///***************************************************************************************

        //if (state.get<SBool>("vobs_sampler_blocked")->value)
        //  return;

        ///sample 0-component of vobs
        ctx.print("Doing slice sweep vobs_0");

        vobs[0] = slice_sweep(comm, rng->get(),
                      boost::bind(&BorgConvVobsSampler::computeLogLikelihood, this, boost::ref(state), _1, vobs[1], vobs[2]),
                      vobs[0], 30.);

        ctx.print(format(" => got vobs_0=%lg") % vobs[0]);

        ///sample 1-component of vobs
        ctx.print("Doing slice sweep vobs_1");

        vobs[1] = slice_sweep(comm, rng->get(),
                      boost::bind(&BorgConvVobsSampler::computeLogLikelihood, this, boost::ref(state), vobs[0], _1, vobs[2]),
                      vobs[1], 30.);

        ctx.print(format(" => got vobs_1=%lg") % vobs[1]);

    ///sample 2-component of vobs
    ctx.print("Doing slice sweep vobs_2");


    vobs[2] = slice_sweep(comm, rng->get(),
                      boost::bind(&BorgConvVobsSampler::computeLogLikelihood, this, boost::ref(state), vobs[0], vobs[1], _1),
                      vobs[2], 30.);

        ctx.print(format(" => got vobs_2=%lg") % vobs[2]);


        //now release particles again
         model->releaseParticles();

        model->setObserver(vobs);
        model->forwardModel(tmp_complex_field, *out_density, false);
    }
}


void BorgConvNmeanSampler::initialize(MarkovState& state)
{
    //long N0, N1, N2;
    long localN0, startN0;

    ConsoleContext<LOG_DEBUG> ctx("initialization of BorgNmeanSampler");
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
//TC
    //C0 = static_cast<SLong&>(state["C0"]);
    //C1 = static_cast<SLong&>(state["C1"]);
    //C2 = static_cast<SLong&>(state["C2"]);
    tot_num_conv = static_cast<SLong&>(state["tot_num_conv"]);
//TC
}

void BorgConvNmeanSampler::restore(MarkovState& state)
{
    ConsoleContext<LOG_DEBUG> ctx("restoration of BorgNmeanSampler");
    initialize(state);
}

double BorgConvNmeanSampler::computeLogLikelihood(ArrayType::ArrayType& s_array, ArrayType::ArrayType& data_array, SelArrayType::ArrayType& selection, double nmean, four_arr_ref &w, one_arr_ref &b, double temp){
  using CosmoTool::square;
  ConsoleContext<LOG_DEBUG> ctx("likelihood evaluation");

  ctx.print(format("attempting nmean %lg") % nmean);
  if (nmean <= 0)
    return -std::numeric_limits<double>::infinity();

  if (nmean > 1000)
    return -std::numeric_limits<double>::infinity();
//TC
  double L = 0;
  L = conv_like(s_array, selection, nmean, data_array, w, b, tot_num_conv, N0, N1, N2);
//TC
  return -L * temp;
}

void BorgConvNmeanSampler::sample(MarkovState& state)
{ 
    typedef ArrayType::ArrayType Array;
    typedef SelArrayType::ArrayType SArray;
    ConsoleContext<LOG_DEBUG>  ctx("sampling of nmean ");

    Array& G = *state.get<ArrayType>("growth_factor")->array;
    Array& final_field = *state.get<ArrayType>("BORG_final_density")->array;
    RandomGen *rng = state.get<RandomGen>("random_generator");


    if (state.get<SBool>("nmean_sampler_blocked")->value)
        return;

    double temp = state.getScalar<double>("ares_heat");
    ctx.print(format("Temperature is %lg") % temp);

    for (int c = 0; c < Ncat; c++) {
        SArray& sel_array = *state.get<SelArrayType>(format("galaxy_sel_window_%d") % c)->array;
        Array& g_field = *state.get<ArrayType>(format("galaxy_data_%d") % c)->array;
        SDouble *g_nmean = state.get<SDouble>(format("galaxy_nmean_%d") % c);
//TC
        ArrayType1d::ArrayType &bias_params = *state.get<ArrayType1d>(format("galaxy_bias_%d") % c)->array;
        //two_arr_ref w(bias_params.data(), boost::extents[tot_num_conv][1]);
        two_arr_ref w(bias_params.data(), boost::extents[tot_num_conv][4]);
        //one_arr_ref b(bias_params.data() + tot_num_conv * 1, boost::extents[tot_num_conv]);
        one_arr_ref b(bias_params.data() + tot_num_conv * 4, boost::extents[tot_num_conv]);
           
        //four_arr weights(boost::extents[tot_num_conv][1][1][1]);                                             
        four_arr weights(boost::extents[tot_num_conv][3][3][3]);
        for (int num_conv = 0; num_conv < tot_num_conv; num_conv++){
            //weights[num_conv][0][0][0] = w[num_conv][0];
            weights[num_conv][1][1][1] = w[num_conv][0];

            weights[num_conv][0][1][1] = w[num_conv][1];
            weights[num_conv][1][0][1] = w[num_conv][1];
            weights[num_conv][1][2][1] = w[num_conv][1];
            weights[num_conv][1][1][0] = w[num_conv][1];
            weights[num_conv][1][1][2] = w[num_conv][1];
            weights[num_conv][2][1][1] = w[num_conv][1];
        
            weights[num_conv][0][1][0] = w[num_conv][2];
            weights[num_conv][0][1][2] = w[num_conv][2];
            weights[num_conv][0][0][1] = w[num_conv][2];
            weights[num_conv][0][2][1] = w[num_conv][2];
            weights[num_conv][1][0][0] = w[num_conv][2];
            weights[num_conv][1][0][2] = w[num_conv][2];
            weights[num_conv][1][2][0] = w[num_conv][2];
            weights[num_conv][1][2][2] = w[num_conv][2];
            weights[num_conv][2][1][0] = w[num_conv][2];
            weights[num_conv][2][1][2] = w[num_conv][2];
            weights[num_conv][2][0][1] = w[num_conv][2];
            weights[num_conv][2][2][1] = w[num_conv][2];
        
            weights[num_conv][0][0][0] = w[num_conv][3];
            weights[num_conv][0][2][0] = w[num_conv][3];
            weights[num_conv][0][0][2] = w[num_conv][3];
            weights[num_conv][0][2][2] = w[num_conv][3];
            weights[num_conv][2][0][0] = w[num_conv][3];
            weights[num_conv][2][2][0] = w[num_conv][3];
            weights[num_conv][2][0][2] = w[num_conv][3];
            weights[num_conv][2][2][2] = w[num_conv][3];
        }
//TC
        ctx.print(format("catalog %d") % c);

        ctx.print("Doing slice sweep");
//TC
        g_nmean->value = slice_sweep_double(comm, rng->get(), std::bind(&BorgConvNmeanSampler::computeLogLikelihood, this, ref(final_field), ref(g_field), ref(sel_array), ph::_1, weights, ref(b), temp), g_nmean->value, 0.1);
//TC
        ctx.print(format(" => got nmean=%lg") % g_nmean->value);
    }
}

void BorgConvBiasSampler::initialize(MarkovState& state)
{
    //long N0, N1, N2;
    long localN0, startN0;

    ConsoleContext<LOG_DEBUG> ctx("initialization of BorgConvBiasSampler");
    // This sampler depends heavily on the rest of the model.
    // First grab the number of catalogs available in the markov chain

    Ncat = static_cast<SLong&>(state["NCAT"]);

    N0 = static_cast<SLong&>(state["N0"]);
    localN0 = static_cast<SLong&>(state["localN0"]);
    startN0 = static_cast<SLong&>(state["startN0"]);
    N1 = static_cast<SLong&>(state["N1"]);
    N2 = static_cast<SLong&>(state["N2"]);

    Ntot = N0 * N1 * N2;
    localNtot = localN0 * N1 * N2;
//TC
    //C0 = static_cast<SLong&>(state["C0"]);
    //C1 = static_cast<SLong&>(state["C1"]);
    //C2 = static_cast<SLong&>(state["C2"]);
    tot_num_conv = static_cast<SLong&>(state["tot_num_conv"]);
//TC
}

void BorgConvBiasSampler::restore(MarkovState& state)
{
    ConsoleContext<LOG_DEBUG> ctx("restoration of BorgConvBiasSampler");
    initialize(state);
}


double BorgConvBiasSampler::computeLogLikelihood(ArrayType::ArrayType& s_array, ArrayType::ArrayType& data_array, SelArrayType::ArrayType& selection, double nmean, two_arr_ref &w, one_arr_ref &b, int layer, int index, double sweep, double temp)
{
  using CosmoTool::square;
  ConsoleContext<LOG_DEBUG> ctx("likelihood evaluation");

  if (index == 0)
      ctx.print(format("attempting central weight in layer %i = %lg") % layer % sweep);
  else if (index == 1)
      ctx.print(format("attempting face weights in layer %i = %lg") % layer % sweep);
  else if (index == 2)
      ctx.print(format("attempting edge weights in layer %i = %lg") % layer % sweep);
  else if (index == 3)
      ctx.print(format("attempting corner weights in layer %i = %lg") % layer % sweep);
  else
      ctx.print(format("attempting bias in layer %i = %lg") % layer % sweep);

  if (sweep <= -100)
      return -std::numeric_limits<double>::infinity();
  if (sweep > 100)
      return -std::numeric_limits<double>::infinity();

//TC
    //four_arr weights(boost::extents[tot_num_conv][1][1][1]);                                             
    four_arr weights(boost::extents[tot_num_conv][3][3][3]);
    for (int num_conv = 0; num_conv < tot_num_conv; num_conv++){
        //weights[num_conv][0][0][0] = w[num_conv][0];
        weights[num_conv][1][1][1] = w[num_conv][0];

        weights[num_conv][0][1][1] = w[num_conv][1];
        weights[num_conv][1][0][1] = w[num_conv][1];
        weights[num_conv][1][2][1] = w[num_conv][1];
        weights[num_conv][1][1][0] = w[num_conv][1];
        weights[num_conv][1][1][2] = w[num_conv][1];
        weights[num_conv][2][1][1] = w[num_conv][1];
    
        weights[num_conv][0][1][0] = w[num_conv][2];
        weights[num_conv][0][1][2] = w[num_conv][2];
        weights[num_conv][0][0][1] = w[num_conv][2];
        weights[num_conv][0][2][1] = w[num_conv][2];
        weights[num_conv][1][0][0] = w[num_conv][2];
        weights[num_conv][1][0][2] = w[num_conv][2];
        weights[num_conv][1][2][0] = w[num_conv][2];
        weights[num_conv][1][2][2] = w[num_conv][2];
        weights[num_conv][2][1][0] = w[num_conv][2];
        weights[num_conv][2][1][2] = w[num_conv][2];
        weights[num_conv][2][0][1] = w[num_conv][2];
        weights[num_conv][2][2][1] = w[num_conv][2];
    
        weights[num_conv][0][0][0] = w[num_conv][3];
        weights[num_conv][0][2][0] = w[num_conv][3];
        weights[num_conv][0][0][2] = w[num_conv][3];
        weights[num_conv][0][2][2] = w[num_conv][3];
        weights[num_conv][2][0][0] = w[num_conv][3];
        weights[num_conv][2][2][0] = w[num_conv][3];
        weights[num_conv][2][0][2] = w[num_conv][3];
        weights[num_conv][2][2][2] = w[num_conv][3];
    }


    double L = 0.;
    if (index == 0) {
        weights[layer][1][1][1] = sweep;
    }
    else if (index == 1) {
        weights[layer][0][1][1] = sweep;
        weights[layer][1][0][1] = sweep;
        weights[layer][1][2][1] = sweep;
        weights[layer][1][1][0] = sweep;
        weights[layer][1][1][2] = sweep;
        weights[layer][2][1][1] = sweep;
    }
    else if (index = 2) {
        weights[layer][0][1][0] = sweep;
        weights[layer][0][1][2] = sweep;
        weights[layer][0][0][1] = sweep;
        weights[layer][0][2][1] = sweep;
        weights[layer][1][0][0] = sweep;
        weights[layer][1][0][2] = sweep;
        weights[layer][1][2][0] = sweep;
        weights[layer][1][2][2] = sweep;
        weights[layer][2][1][0] = sweep;
        weights[layer][2][1][2] = sweep;
        weights[layer][2][0][1] = sweep;
        weights[layer][2][2][1] = sweep;
    }
    else if (index = 3) {
        weights[layer][0][0][0] = sweep;
        weights[layer][0][2][0] = sweep;
        weights[layer][0][0][2] = sweep;
        weights[layer][0][2][2] = sweep;
        weights[layer][2][0][0] = sweep;
        weights[layer][2][2][0] = sweep;
        weights[layer][2][0][2] = sweep;
        weights[layer][2][2][2] = sweep;
    }
    else {
	b[layer] = sweep;
    }

    L = conv_like(s_array, selection, nmean, data_array, weights, b, tot_num_conv, N0, N1, N2);
    ctx.print(format("L = %g") %L); 


//TC ADD PRIOR???
//  ctx.print(format("nmean = %lg, bias = %lg, rho_g = %lg, eps_g = %lg, L = %lg, loc_L=%lg") % nmean % b % rho_g % eps_g % (L) % (loc_L));
//  double prior = -0.5*(b-1)*(b-1)/4. + -0.5*(eps_g-1.5)*(eps_g-1.5)/(1.5)/(1.5) -0.5*(rho_g-0.4)*(rho_g-0.4)/1  ;
  return -L * temp; // + prior;
}

void BorgConvBiasSampler::sample(MarkovState& state)
{

    typedef ArrayType::ArrayType Array;
    typedef SelArrayType::ArrayType SArray;
    ConsoleContext<LOG_DEBUG>  ctx("sampling of bias");

    Array& G = *state.get<ArrayType>("growth_factor")->array;
    Array& final_field = *state.get<ArrayType>("BORG_final_density")->array;
    RandomGen *rng = state.get<RandomGen>("random_generator");
    double temp = state.getScalar<double>("ares_heat");

    if (state.get<SBool>("bias_sampler_blocked")->value)
        return;

    ctx.print(format("Temperature is %lg") % temp);

    for (int c = 0; c < Ncat; c++) {
        bool biasRef = state.get<SBool>(format("galaxy_bias_ref_%d") % c )->value;
        SArray& sel_array = *state.get<SelArrayType>(format("galaxy_sel_window_%d") % c)->array;
        Array& g_field = *state.get<ArrayType>(format("galaxy_data_%d") % c)->array;
        SDouble *g_nmean = state.get<SDouble>(format("galaxy_nmean_%d") % c);
       
//TC
        ArrayType1d::ArrayType &bias_params = *state.get<ArrayType1d>(format("galaxy_bias_%d") % c)->array;
        //two_arr_ref w(bias_params.data(), boost::extents[tot_num_conv][1]);
        two_arr_ref w(bias_params.data(), boost::extents[tot_num_conv][4]);
        //one_arr_ref b(bias_params.data() + tot_num_conv * 1, boost::extents[tot_num_conv]);
        one_arr_ref b(bias_params.data() + tot_num_conv * 4, boost::extents[tot_num_conv]);
//TC

        //four_arr_ref& weights = ref(w);
        two_arr_ref& weights = w;
        one_arr_ref& biases = b;

        ctx.print(format("catalog %d") % c);
        if (biasRef)
          continue;
        for (int w_scan = 0; w_scan < 4; w_scan++) {
            for(int layer = tot_num_conv - 1; layer >= 0; layer--) {
                weights[layer][w_scan] = slice_sweep_double(comm, rng->get(), std::bind(&BorgConvBiasSampler::computeLogLikelihood, this, ref(final_field), ref(g_field), ref(sel_array), g_nmean->value, ref(weights), ref(biases), layer, w_scan, ph::_1, temp), weights[layer][w_scan], 0.1);
            }
        }
        for (int layer = tot_num_conv - 1; layer >= 0; layer--) {
            biases[layer] = slice_sweep_double(comm, rng->get(), std::bind(&BorgConvBiasSampler::computeLogLikelihood, this, ref(final_field), ref(g_field), ref(sel_array), g_nmean->value, ref(weights), ref(biases), layer, 1, ph::_1, temp), biases[layer], 0.1);
	}
//TC
    }
}
