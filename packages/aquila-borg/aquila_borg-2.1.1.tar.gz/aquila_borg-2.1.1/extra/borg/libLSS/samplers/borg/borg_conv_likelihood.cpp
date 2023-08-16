/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/borg/borg_conv_likelihood.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <CosmoTool/algo.hpp>
#include <cmath>
#include <Eigen/Core>
#include <boost/format.hpp>
#include <boost/bind.hpp>
#include <CosmoTool/hdf5_array.hpp>
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/samplers/borg/borg_conv_likelihood.hpp"
#include "libLSS/samplers/borg/borg_conv_meta.hpp"
#include "libLSS/tools/fused_assign.hpp"



using namespace LibLSS;
using namespace LibLSS::CNN;
using boost::format;
using boost::extents;

using CosmoTool::square;
using CosmoTool::hdf5_write_array;

using boost::c_storage_order;
typedef boost::multi_array_types::extent_range range;

typedef Eigen::Map<Eigen::ArrayXd, Eigen::Aligned> MappedArray;

static const int ROOT_RANK = 0;
static const bool VERBOSE_WRITE_BORG = false;
static const double EPSILON_VOIDS = 1e-6;

BorgConvDensitySampler::BorgConvDensitySampler(MPI_Communication *comm, int maxTime, double maxEpsilon)
    : HMCDensitySampler(comm, maxTime, maxEpsilon)
{
}

void BorgConvDensitySampler::restore(MarkovState& state)
{
    restore_HMC(state);

    xmin0 = state.get<SDouble>("corner0")->value;
    xmin1 = state.get<SDouble>("corner1")->value;
    xmin2 = state.get<SDouble>("corner2")->value;
//TC   
    tot_num_conv = state.get<SLong>("tot_num_conv")->value;
//TC
    state.newElement("BORG_vobs", vobs = new ArrayType1d(boost::extents[3]), true);    
    state.newElement("BORG_final_density", borg_final_density = new ArrayType(boost::extents[range(startN0,startN0+localN0)][N1][N2]), true);
    borg_final_density->setRealDims(ArrayDimension(N0,N1,N2));
    
    model = state.get<BorgModelElement>("BORG_model")->obj;
}

void BorgConvDensitySampler::initialize(MarkovState& state)
{
    initialize_HMC(state);
    xmin0 = state.get<SDouble>("corner0")->value;
    xmin1 = state.get<SDouble>("corner1")->value;
    xmin2 = state.get<SDouble>("corner2")->value;
//TC    
    tot_num_conv = state.get<SLong>("tot_num_conv")->value;
//TC
    state.newElement("BORG_vobs", vobs = new ArrayType1d(boost::extents[3]), true);
    
    state.newElement("BORG_final_density", borg_final_density = new ArrayType(boost::extents[range(startN0,startN0+localN0)][N1][N2]), true);
    borg_final_density->setRealDims(ArrayDimension(N0,N1,N2));
    
    (*vobs->array)[0] = 0;
    (*vobs->array)[1] = 0;
    (*vobs->array)[2] = 0;
    
    //initialize model uncertainty
    model = state.get<BorgModelElement>("BORG_model")->obj;

    for (int c = 0; c < Ncat; c++){
//TC
      auto& thing = *state.get<ArrayType1d>(format("galaxy_bias_%d") % c)->array;
      thing.resize(boost::extents[4 * tot_num_conv + tot_num_conv]);

      thing[0] = 0.1;
      thing[1] = 3.2;
      thing[2] = 1.7;
      thing[3] = 0.4;
      thing[4] = 8.1;

      thing[5] = 9.2;
      thing[6] = 6.2;
      thing[7] = 0.2;
      thing[8] = 5.4;
      thing[9] = 2.8;

      thing[10] = 3.2;
      thing[11] = 5.1;
      thing[12] = 1.1;
      thing[13] = 6.4;
      thing[14] = 2.7;

      thing[15] = 5.3;
      thing[16] = 8.5;
      thing[17] = 4.7;
      thing[18] = 2.7;
      thing[19] = 6.4;

      thing[20] = 0.2;
      thing[21] = 9.1;
      thing[22] = 4.8;
      thing[23] = 7.7;
      thing[24] = 5.1;

      //array::fill(thing, 0.);
//TC
    }
      
}

BorgConvDensitySampler::~BorgConvDensitySampler()
{
}

void BorgConvDensitySampler::saveAuxiliaryAcceptedFields(MarkovState& state)
{
  array::scaleAndCopyArray3d(*borg_final_density->array, *tmp_real_field, 1, true);
}

template<typename real_t, typename adjoint_t>
void LibLSS::CNN::conv_like_gr(real_t &&real_field, three_arr_ref &sel_array, double noise_level, three_arr_ref &g_field, four_arr_ref &w, one_arr_ref &b, int tot_num_conv, int N0, int N1, int N2, adjoint_t &&adjoint_gradient){

    double value;
    int mn, ii, nn, jj, ln, kk;
    int C = K / 2;
    double E_error = 0.;
    three_arr field(boost::extents[N0][N1][N2]);
    three_arr temp(boost::extents[N0][N1][N2]);
    four_arr gradient_field(boost::extents[tot_num_conv][N0][N1][N2]);
    three_arr the_error(boost::extents[N0][N1][N2]);
    three_arr temp_error(boost::extents[N0][N1][N2]);
    three_arr second_temp_error(boost::extents[N0][N1][N2]);

    copy_array_rv(field[boost::indices[i_range(0, N0)][i_range(0, N1)][i_range(0, N2)]], real_field);

    for (int num_conv = 0; num_conv < tot_num_conv; num_conv++){
        for (int i = 0; i < N0; i++){
            for (int j = 0; j < N1; j++){
                for (int k = 0; k < N2; k++){
                    value = 0;
                    for (int m = 0; m < K; m++){
                        mn = K - 1 - m;
                        ii = i + (m - C);
                        for (int n = 0; n < K; n++){
                            nn = K - 1 - n;
                            jj = j + (n - C);
                            for (int l = 0; l < K; l++){
                                ln = K - 1 - l;
                                kk = k + (l - C);
                                if (ii >= 0 && ii < N0 && jj >= 0 && jj < N1 && kk >= 0 && kk < N2) {
                                    value += field[ii][jj][kk] * w[num_conv][mn][nn][ln];
                                }
                            }
                        }                  
                    }
                    temp[i][j][k] = activation(value + b[num_conv]) + field[i][j][k];
                    gradient_field[num_conv][i][j][k] = activation_gr(value + b[num_conv]);
                    if (num_conv == tot_num_conv - 1){
                        temp[i][j][k] = activation(temp[i][j][k]);
                        if (sel_array[i][j][k] > 0.){
                            the_error[i][j][k] = loss_gr(sel_array[i][j][k], temp[i][j][k], g_field[i][j][k], noise_level) * activation_gr(temp[i][j][k]);
                            temp_error[i][j][k] = the_error[i][j][k] * gradient_field[num_conv][i][j][k];
                        }
                    }
                }
            }
        }
        copy_array_rv(field[boost::indices[i_range(0, N0)][i_range(0, N1)][i_range(0, N2)]], temp[boost::indices[i_range(0, N0)][i_range(0, N1)][i_range(0, N2)]]);
    }
    for (int num_conv = tot_num_conv - 1; num_conv >= 0; num_conv--){
        for (int i = 0; i < N0; i++){
            for (int j = 0; j < N1; j++){
                for (int k = 0; k < N2; k++){
                    value = 0;
                    for (int m = 0; m < K; m++){
                        mn = K - 1 - m;
                        ii = i + (m - C);
                        for (int n = 0; n < K; n++){
                            nn = K - 1 - n;
                            jj = j + (n - C);
                            for (int l = 0; l < K; l++){
                                ln = K - 1 - l;
                                kk = k + (l - C);
                                if (ii >= 0 && ii < N0 && jj >= 0 && jj < N1 && kk >= 0 && kk < N2) {
                                    value += temp_error[ii][jj][kk] * w[num_conv][mn][nn][ln];
                                }
                            }
                        }                  
                    }
                    the_error[i][j][k] = value + the_error[i][j][k];
                    if (num_conv > 0){
                        second_temp_error[i][j][k] = the_error[i][j][k] * gradient_field[num_conv - 1][i][j][k];
                    }
                }
            }
        }
        if (num_conv > 0){
            copy_array_rv(temp_error[boost::indices[i_range(0, N0)][i_range(0, N1)][i_range(0, N2)]], second_temp_error[boost::indices[i_range(0, N0)][i_range(0, N1)][i_range(0, N2)]]);
        }
    }

    LibLSS::copy_array_rv(adjoint_gradient, the_error[boost::indices[i_range(0, N0)][i_range(0, N1)][i_range(0, N2)]]);
}

template<typename real_t>
void LibLSS::CNN::conv_like_g_field(real_t &&real_field, three_arr_ref &sel_array, double noise_level, three_arr_ref &g_field, four_arr_ref &w, one_arr_ref &b, int tot_num_conv, int N0, int N1, int N2){

    double value;
    int mn, ii, nn, jj, ln, kk;
    int C = K / 2;
    three_arr field(boost::extents[N0][N1][N2]);
    three_arr temp(boost::extents[N0][N1][N2]);

    copy_array_rv(field[boost::indices[i_range(0, N0)][i_range(0, N1)][i_range(0, N2)]], real_field);

    for (int num_conv = 0; num_conv < tot_num_conv; num_conv++){
        for (int i = 0; i < N0; i++){
            for (int j = 0; j < N1; j++){
                for (int k = 0; k < N2; k++){
                    value = 0;
                    for (int m = 0; m < K; m++){
                        mn = K - 1 - m;
                        ii = i + (m - C);
                        for (int n = 0; n < K; n++){
                            nn = K - 1 - n;
                            jj = j + (n - C);
                            for (int l = 0; l < K; l++){
                                ln = K - 1 - l;
                                kk = k + (l - C);
                                if (ii >= 0 && ii < N0 && jj >= 0 && jj < N1 && kk >= 0 && kk < N2) {
                                    value += field[ii][jj][kk] * w[num_conv][mn][nn][ln];
                                }
                            }
                        }                  
                    }
                    temp[i][j][k] = activation(value + b[num_conv]) + field[i][j][k];
                    if (num_conv == tot_num_conv - 1){
                        temp[i][j][k] = activation(temp[i][j][k]);
                    } 
                }
            }
        }
        copy_array_rv(field[boost::indices[i_range(0, N0)][i_range(0, N1)][i_range(0, N2)]], temp[boost::indices[i_range(0, N0)][i_range(0, N1)][i_range(0, N2)]]);
    }
    LibLSS::copy_array(g_field, field[boost::indices[i_range(0, N0)][i_range(0, N1)][i_range(0, N2)]]);
}

HMCDensitySampler::HamiltonianType BorgConvDensitySampler::computeHamiltonian_Likelihood(MarkovState& state, CArray& s_array, bool final_call)
{

    using CosmoTool::square;
    ConsoleContext<LOG_DEBUG> ctx("BORG_CONV likelihood");
    CosmologicalParameters& cosmo_params = state.getScalar<CosmologicalParameters>("cosmology");
    Cosmology cosmo(cosmo_params);

    ArrayType::ArrayType& growth = *state.get<ArrayType>("growth_factor")->array;
    double ai = state.get<SDouble>("borg_a_initial")->value;
    double D_init=cosmo.d_plus(ai) / cosmo.d_plus(1.0); // Scale factor for initial conditions

    typedef ArrayType::ArrayType::element ElementType;
    double E = 0.;

    // Protect the input
    array::scaleAndCopyArray3d(*tmp_complex_field, s_array, D_init/volume);
    Hermiticity_fixup(*tmp_complex_field);
    
    // Simulate forward model
    //setup position and velocity arrays
    
    ArrayType::ArrayType *out_density = tmp_real_field;

    // Update forward model for maybe new cosmo params
    model->setCosmoParams(state.getScalar<CosmologicalParameters>("cosmology"));
    // Inform about the velocity of the observer
    model->setObserver(*vobs->array);
    // Compute forward model
    model->forwardModel(*tmp_complex_field, *out_density, false);
    
    if (VERBOSE_WRITE_BORG) {
        H5::H5File f("borg_density_field.h5", H5F_ACC_TRUNC);
        
        hdf5_write_array(f, "borg_density", *out_density);
    }
    
    for (int c = 0; c < Ncat; c++) {
        bool biasRef = state.get<SBool>(format("galaxy_bias_ref_%d") % c )->value;
        SelArrayType::ArrayType& sel_array = *state.get<SelArrayType>(format("galaxy_sel_window_%d") % c)->array;
        ArrayType::ArrayType& g_field = *state.get<ArrayType>(format("galaxy_data_%d") % c)->array;
        SDouble *g_nmean = state.get<SDouble>(format("galaxy_nmean_%d") % c);
        double nmean = g_nmean->value;

        ArrayType1d::ArrayType &bias_params = *state.get<ArrayType1d>(format("galaxy_bias_%d") % c)->array;
        two_arr_ref w(bias_params.data(), boost::extents[tot_num_conv][4]);
        one_arr_ref b(bias_params.data() + tot_num_conv * 4, boost::extents[tot_num_conv]);
        four_arr weights(boost::extents[tot_num_conv][3][3][3]);
        for (int num_conv = 0; num_conv < tot_num_conv; num_conv++){
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

        E += conv_like((*out_density)[model->lo_mgr->strict_range()], sel_array, nmean, g_field, weights, b, tot_num_conv, N0, N1, N2);
    }
    
    double temp=state.getScalar<double>("ares_heat");
    return E * temp;
}

void BorgConvDensitySampler::computeGradientPsi_Likelihood(MarkovState& state, CArray& s, CArrayRef& grad_array, bool accumulate)
{
    using CosmoTool::square;
    typedef CArray::element etype;

    ConsoleContext<LOG_DEBUG> ctx("BORG_CONV likelihood gradient");
    
    CosmologicalParameters& cosmo_params = state.getScalar<CosmologicalParameters>("cosmology");
    Cosmology cosmo(cosmo_params);

    ArrayType::ArrayType& growth = *state.get<ArrayType>("growth_factor")->array;
    double ai = state.get<SDouble>("borg_a_initial")->value;
    double D_init=cosmo.d_plus(ai) / cosmo.d_plus(1.0); // Scale factor for initial conditions
    double temp=state.getScalar<double>("ares_heat");
   
    // Have to protect the input array against destruction
    ctx.print(format("Scale initial conditions, D = %lg") % D_init);
    ctx.print(format("Temperature is %lg") % temp);

    array::scaleAndCopyArray3d((*tmp_complex_field), s, D_init/volume);
    Hermiticity_fixup(*tmp_complex_field);
    
    // Simulate forward model
    //setup position and velocity arrays
           
    model->setCosmoParams(state.getScalar<CosmologicalParameters>("cosmology"));
    model->setObserver(*vobs->array);
    model->forwardModel(*tmp_complex_field, *tmp_real_field, true);

    Uninit_FFTW_Real_Array real_gradient_p(extents[range(startN0,startN0+localN0)][N1][N2real], allocator_real);
    Uninit_FFTW_Real_Array::array_type& real_gradient = real_gradient_p;
    
    array::fill(real_gradient, 0);
    
// First compute the gradient in real space, and then do 
// the fourier space and use chain rule.

    for (int c = 0; c < Ncat; c++) {
        bool biasRef = state.get<SBool>(format("galaxy_bias_ref_%d") % c )->value;
        SelArrayType::ArrayType& sel_array = *state.get<SelArrayType>(format("galaxy_sel_window_%d") % c)->array;
        ArrayType::ArrayType& g_field = *state.get<ArrayType>(format("galaxy_data_%d") % c)->array;
        double nmean = state.get<SDouble>(format("galaxy_nmean_%d") % c)->value;

        ArrayType1d::ArrayType &bias_params = *state.get<ArrayType1d>(format("galaxy_bias_%d") % c)->array;
        two_arr_ref w(bias_params.data(), boost::extents[tot_num_conv][4]);
        one_arr_ref b(bias_params.data() + tot_num_conv * 4, boost::extents[tot_num_conv]);
       
        four_arr weights(boost::extents[tot_num_conv][3][3][3]);
        for (int num_conv = 0; num_conv < tot_num_conv; num_conv++){
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

        conv_like_gr((*tmp_real_field)[model->lo_mgr->strict_range()], sel_array, nmean, g_field, weights, b, tot_num_conv, N0, N1, N2, real_gradient[model->lo_mgr->strict_range()]);
    }
    
    // Now obtain the complex gradient using adjoint fft
    model->adjointModel(real_gradient);  // real_gradient is input and output.
    //undo scaling of input field
    array::scaleArray3d(real_gradient, D_init/volume);
    computeFourierSpace_GradientPsi(state, real_gradient, grad_array, accumulate);
}

void BorgConvDensitySampler::initial_density_filter(MarkovState& state)
{
    typedef CArray::element etype;

    ConsoleContext<LOG_DEBUG> ctx("BORG_CONV initial density filter");
    
    ArrayType1d::ArrayType& pspec = *state.get<ArrayType1d>("powerspectrum")->array;
    IArrayType::ArrayType& adjust_array = *state.get<IArrayType>("adjust_mode_multiplier")->array;
    IArrayType::ArrayType& key_array = *state.get<IArrayType>("k_keys")->array;  
    CArrayType::ArrayType& s_hat0 = *state.get<CArrayType>("s_hat_field")->array;
    ArrayType::ArrayType& s = *state.get<ArrayType>("s_field")->array;
    RandomGen *rgen = state.get<RandomGen>("random_generator");

    CosmologicalParameters& cosmo_params = state.getScalar<CosmologicalParameters>("cosmology");
    Cosmology cosmo(cosmo_params);

    double ai = state.get<SDouble>("borg_a_initial")->value;
    double D_init=cosmo.d_plus(ai) / cosmo.d_plus(1.0); // Scale factor for initial conditions
    
    generateRandomField(state);

    double factor=0.1;

    array::scaleAndCopyArray3d(*tmp_complex_field, s_hat0, D_init/volume);
        
    model->setCosmoParams(state.getScalar<CosmologicalParameters>("cosmology"));
    model->setObserver(*vobs->array);
    model->forwardModel(*tmp_complex_field, *tmp_real_field, false);

    //overwrite initial final density field
    Array& s_array = *state.get<ArrayType>("BORG_final_density")->array;
    array::copyArray3d(s_array, *tmp_real_field, true);
   
}

void BorgConvDensitySampler::generateMockData(MarkovState& state, bool only_forward)
{
    ConsoleContext<LOG_INFO> ctx("Borg mock data generation");

    ArrayType1d::ArrayType& pspec = *state.get<ArrayType1d>("powerspectrum")->array;
    IArrayType::ArrayType& adjust_array = *state.get<IArrayType>("adjust_mode_multiplier")->array;
    IArrayType::ArrayType& key_array = *state.get<IArrayType>("k_keys")->array;  
    CArrayType::ArrayType& s_hat0 = *state.get<CArrayType>("s_hat_field")->array;
    ArrayType::ArrayType& s = *state.get<ArrayType>("s_field")->array;
    RandomGen *rgen = state.get<RandomGen>("random_generator");

    CosmologicalParameters& cosmo_params = state.getScalar<CosmologicalParameters>("cosmology");
    Cosmology cosmo(cosmo_params);

    double ai = state.get<SDouble>("borg_a_initial")->value;
    double D_init=cosmo.d_plus(ai) / cosmo.d_plus(1.0); // Scale factor for initial conditions
    
    generateRandomField(state);

    array::scaleAndCopyArray3d(*tmp_complex_field, s_hat0, D_init/volume);
        
    model->setCosmoParams(state.getScalar<CosmologicalParameters>("cosmology"));
    model->setObserver(*vobs->array);
    model->forwardModel(*tmp_complex_field, *tmp_real_field, false);

    array::copyArray3d(*borg_final_density->array, *tmp_real_field, true);
    
    if (!only_forward) {
      for (int c = 0; c < Ncat; c++) {
        ctx.print(format("Generating mock data %d") % c);      
        SelArrayType::ArrayType& sel_array = *state.get<SelArrayType>(format("galaxy_sel_window_%d") % c)->array;
        ArrayType::ArrayType& g_field = *state.get<ArrayType>(format("galaxy_data_%d") % c)->array;
        double nmean = state.get<SDouble>(format("galaxy_nmean_%d") % c)->value;    

        ArrayType1d::ArrayType &bias_params = *state.get<ArrayType1d>(format("galaxy_bias_%d") % c)->array;
        two_arr_ref w(bias_params.data(), boost::extents[tot_num_conv][4]);
        one_arr_ref b(bias_params.data() + tot_num_conv * 4, boost::extents[tot_num_conv]);
	   
        four_arr weights(boost::extents[tot_num_conv][3][3][3]);
        for (int num_conv = 0; num_conv < tot_num_conv; num_conv++){
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

        conv_like_g_field((*borg_final_density->array)[model->lo_mgr->strict_range()], sel_array, nmean, g_field, weights, b, tot_num_conv, N0, N1, N2);
      }
    } 
    else {
      for (int c = 0; c < Ncat; c++) {
        array::copyArray3d(*state.get<ArrayType>(format("galaxy_data_%d") % c)->array, *tmp_real_field);
      }
    }
    
}
