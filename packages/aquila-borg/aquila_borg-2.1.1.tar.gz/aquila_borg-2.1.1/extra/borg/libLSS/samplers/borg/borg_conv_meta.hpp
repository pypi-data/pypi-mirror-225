/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/borg/borg_conv_meta.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_BORG_CONV_META_SAMPLER_HPP
#define __LIBLSS_BORG_CONV_META_SAMPLER_HPP

#include <boost/multi_array.hpp>
#include "libLSS/samplers/core/markov.hpp"
#include "libLSS/samplers/core/types_samplers.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/samplers/ares/ares_bias.hpp"
#include "libLSS/samplers/borg/borg_conv_likelihood.hpp"

namespace LibLSS {

//TC
    namespace CNN {
        typedef boost::multi_array<double, 4> four_arr;
        typedef boost::multi_array_ref<double, 4> four_arr_ref;
        typedef boost::multi_array<double, 3> three_arr;
        typedef boost::multi_array_ref<double, 3> three_arr_ref;
	typedef boost::multi_array<double, 2> two_arr;
        typedef boost::multi_array_ref<double, 2> two_arr_ref;
        typedef boost::multi_array<double, 1> one_arr;
        typedef boost::multi_array_ref<double, 1> one_arr_ref;
    }
//TC

    class BorgConvVobsSampler: public MarkovSampler {
    protected:
        int Ncat;
        long Ntot, localNtot;
        MPI_Communication *comm;
        BORGForwardModel *model;
//TC
        //long N0, N1, N2, C0, C1, C2, tot_num_conv;
        long N0, N1, N2, tot_num_conv;
//TC
        double computeLogLikelihood(MarkovState& state,
                                    double v0,
                                    double v1,
                                    double v2);
        
    public:
        BorgConvVobsSampler(MPI_Communication *comm0) : comm(comm0) {}
        virtual ~BorgConvVobsSampler() {}
        
        virtual void initialize(MarkovState& state);
        virtual void restore(MarkovState& state);
        virtual void sample(MarkovState& state);
    };

    class BorgConvNmeanSampler: public MarkovSampler {
    protected:
        int Ncat;
        long Ntot, localNtot;
        MPI_Communication *comm;
//TC
        //long N0, N1, N2, C0, C1, C2, tot_num_conv;
        long N0, N1, N2, tot_num_conv;
//TC       
        double computeLogLikelihood(ArrayType::ArrayType& s_array, ArrayType::ArrayType& data_array, SelArrayType::ArrayType& selection, double nmean, CNN::four_arr_ref &w, CNN::one_arr_ref &b, double temp);
        
    public:
        BorgConvNmeanSampler(MPI_Communication *comm0) : comm(comm0) {}
        virtual ~BorgConvNmeanSampler() {}
        
        virtual void initialize(MarkovState& state);
        virtual void restore(MarkovState& state);
        virtual void sample(MarkovState& state);
    };
    
    class BorgConvBiasSampler: public MarkovSampler {
    protected:
        int Ncat;
        long Ntot, localNtot;
        MPI_Communication *comm;
//TC
        //long N0, N1, N2, C0, C1, C2, tot_num_conv;
        long N0, N1, N2, tot_num_conv;
//TC       
        //double computeLogLikelihood(ArrayType::ArrayType& s_array, ArrayType::ArrayType& data_array, SelArrayType::ArrayType& selection, double nmean, CNN::four_arr_ref &w, CNN::one_arr_ref &b, int layer, int conv1, int conv2, int conv3, bool bias, double sweep, double temp);
        double computeLogLikelihood(ArrayType::ArrayType& s_array, ArrayType::ArrayType& data_array, SelArrayType::ArrayType& selection, double nmean, CNN::two_arr_ref &w, CNN::one_arr_ref &b, int layer, int index, double sweep, double temp);

    public:
        BorgConvBiasSampler(MPI_Communication *comm0) : comm(comm0) {}
        virtual ~BorgConvBiasSampler() {}
        
        virtual void initialize(MarkovState& state);
        virtual void restore(MarkovState& state);
        virtual void sample(MarkovState& state);
    };
    
    namespace BORG {    
        using ARES::ensure_bias_size;

        inline void ensure_conv_bias(MarkovState& s, int c)
        {
          ensure_bias_size(s, c, boost::array<double,3>{1, 1.5, 0.4});
        }
        
        inline void extract_conv_bias(MarkovState& s, int c, double *&alpha, double *&rho, double *&epsilon)
        {
            using boost::format;
            ArrayType1d::ArrayType& a = (*s.get<ArrayType1d>(format("galaxy_bias_%d") % c)->array);
            
            alpha = &a[0];
            epsilon = &a[2];
            rho = &a[1];
        }
    
    }
};

#endif
