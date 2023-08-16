/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/borg/borg_conv_likelihood.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_BORG_CONV_DENSITY_HPP
#define __LIBLSS_BORG_CONV_DENSITY_HPP

#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/mcmc/global_state.hpp"
#include "libLSS/tools/fftw_allocator.hpp"
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/tools/fused_assign.hpp"
namespace LibLSS {
    namespace CNN {
	typedef boost::multi_array<double, 4> four_arr;
	typedef boost::multi_array_ref<double, 4> four_arr_ref;
	typedef boost::multi_array<double, 3> three_arr;
	typedef boost::multi_array_ref<double, 3> three_arr_ref;
	typedef boost::multi_array<double, 2> two_arr;
	typedef boost::multi_array_ref<double, 2> two_arr_ref;
	typedef boost::multi_array<double, 1> one_arr;
	typedef boost::multi_array_ref<double, 1> one_arr_ref;
	typedef boost::multi_array_types::index_range i_range;

        static inline double activation(double value){
            if (value >= 0.) {
                return value;
            }
            else {
                return 0.0;
            }
            //return std::log(1. + std::exp(value));
        }
        
        static inline double activation_gr(double value){
            if (value >= 0.) {
               return 1.;
            }
            else {
               return 0.0;
            }
            //return 1. / (1. + std::exp(-value));
        }

        static inline double loss(double selection, double field, double galaxy, double noise){
            return 0.5 * CosmoTool::square(selection * field - galaxy) / (noise * selection) + 0.5 * std::log(noise);//GAUSSIAN 
            //double lambda = selection * noise * field;
            //return lambda - galaxy * std::log(lambda);
      }

        static inline double loss_gr(double selection, double field, double galaxy, double noise){
            return (selection * field - galaxy) / noise;//GAUSSIAN 
            //double lambda = selection * noise * field;
            //return 1. - galaxy / lambda;
        }

        static constexpr int K = 3;

	template<typename real_t>
        double conv_like(real_t &&real_field, three_arr_ref &sel_array, double noise_level, three_arr_ref &g_field, four_arr_ref &w, one_arr_ref &b, int tot_num_conv, int N0, int N1, int N2){
        
            double value;
            int mn, ii, nn, jj, ln, kk;
            int C = K / 2;
            double E = 0.;
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
                                if (sel_array[i][j][k] > 0.){
                                    E += loss(sel_array[i][j][k], temp[i][j][k], g_field[i][j][k], noise_level);
                                }
                            }
                        }
                    }
                }
                copy_array_rv(field[boost::indices[i_range(0, N0)][i_range(0, N1)][i_range(0, N2)]], temp[boost::indices[i_range(0, N0)][i_range(0, N1)][i_range(0, N2)]]);
            }
            return E;
        }

	template<typename real_t, typename adjoint_t>
        void conv_like_gr(real_t &&real_field, three_arr_ref &sel_array, double noise_level, three_arr_ref &g_field, four_arr_ref &w, one_arr_ref &b, int tot_num_conv, int N0, int N1, int N2, adjoint_t &&adjoint_gradient);

	template<typename real_t>
        void conv_like_g_field(real_t &&real_field, three_arr_ref &sel_array, double noise_level, three_arr_ref &g_field, four_arr_ref &w, one_arr_ref &b, int tot_num_conv, int N0, int N1, int N2);
    }    

    class BorgConvDensitySampler: public HMCDensitySampler {
    protected:
        double xmin0, xmin1, xmin2;
        ArrayType1d *vobs;
        ArrayType *borg_final_density;

	int tot_num_conv;

        BORGForwardModel *model;
        
        virtual void initial_density_filter(MarkovState& state);

        virtual HamiltonianType computeHamiltonian_Likelihood(MarkovState& state, CArray& s_array, bool final_call);
        virtual void computeGradientPsi_Likelihood(MarkovState& state, CArray& s, CArrayRef& grad_array, bool accumulate);

    public:
        BorgConvDensitySampler(MPI_Communication* comm, int maxTime, double maxEpsilon);
        virtual ~BorgConvDensitySampler();

        void generateMockData(MarkovState& state, bool only_forward);
        virtual void generateMockData(MarkovState& state) { generateMockData(state, false); }
        
        virtual void restore(MarkovState& state);
        virtual void initialize(MarkovState& state);
        
        virtual void saveAuxiliaryAcceptedFields(MarkovState& state);
  
    };

};

#endif
