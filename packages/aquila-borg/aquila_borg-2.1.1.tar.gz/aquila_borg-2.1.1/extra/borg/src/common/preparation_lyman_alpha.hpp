/*+
    ARES/HADES/BORG Package -- ./extra/borg/src/common/preparation_lyman_alpha.hpp
    Copyright (C) 2020 Natalia Porqueres <n.porqueres@imperial.ac.uk>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_ARES_PREPARATION_LYMAN_ALPHA_HPP 
#define __LIBLSS_ARES_PREPARATION_LYMAN_ALPHA_HPP

#include <functional>
#include <math.h> 
#include "libLSS/tools/console.hpp"
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>
#include "libLSS/tools/ptree_translators.hpp"
#include <boost/algorithm/string.hpp>
#include "libLSS/data/lyman_alpha_qso.hpp"
#include "libLSS/data/lyman_alpha.hpp"
#include "libLSS/data/lyman_alpha_load_txt.hpp"
#include <CosmoTool/interpolate.hpp>
#include "libLSS/tools/ptree_vectors.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fused_assign.hpp"
#include "libLSS/tools/fusewrapper.hpp"
#include "libLSS/physics/projector.hpp"

namespace LibLSS_prepare {

    using namespace LibLSS;

    typedef boost::multi_array_types::extent_range range;

#ifndef SAMPLER_LYMAN_ALPHA_TYPE
#define SAMPLER_LYMAN_ALPHA_TYPE BaseLymanAlphaDescriptor
#endif

    typedef LymanAlphaSurvey<SAMPLER_LYMAN_ALPHA_TYPE> LymanAlphaSurveyType;
    typedef ObjectStateElement<LymanAlphaSurveyType,true> QSOElement;


    namespace PrepareDetail {
      boost::array<int, 3> ArrayDimensionLya(int a, int b, int c) {
        boost::array<int, 3> A;

        A[0] = a;
        A[1] = b;
        A[2] = c;
        return A;
      }

      boost::array<int, 4> ArrayDimensionLya(int a, int b, int c, int d) {
        boost::array<int, 4> A;
        A[0] = a;
        A[1] = b;
        A[2] = c;
        A[3] = d;
        return A;
      }
    
    }

    static void initializeLymanAlphaSurveyCatalog(MarkovState& state, int cat_idx)
    {   
        using PrepareDetail::ArrayDimensionLya;
        Console& cons = Console::instance();
        
        QSOElement *survey = new QSOElement();
        survey->obj = new LymanAlphaSurveyType();
        SDouble *A = new SDouble();
        SDouble *beta = new SDouble();
        SDouble *sigmodel = new SDouble();
        
        // Add a catalog in the state structure
        state.newElement(boost::format("qso_catalog_%d") % cat_idx, survey);
        //SDouble *nmean = new SDouble();
        ArrayType1d *bias = new ArrayType1d(boost::extents[0]);
        state.newElement(format("galaxy_bias_%d") % cat_idx, bias, true);
	bias->setAutoResize(true);
    }

    static void loadLymanAlpha(MarkovState& state, ptree& main_params, int cat_idx)
    {
    	ConsoleContext<LOG_INFO_SINGLE> ctx(str(boost::format("loadLymanAlpha(%d)") % cat_idx));
        QSOElement *survey = state.get<QSOElement>(boost::format("qso_catalog_%d") % cat_idx);
        ptree& params = main_params.get_child(get_catalog_group_name(cat_idx));

	    long N0 = static_cast<SLong&>(state["N0"]);
        long N1 = static_cast<SLong&>(state["N1"]);
        long N2 = static_cast<SLong&>(state["N2"]); 
            
		loadLymanAlphaFromHDF5(
                params.get<string>("datafile"),
                survey->get(), state
        );
         
        ArrayType1d::ArrayType& lya_bias = *(state.get<ArrayType1d>(format("galaxy_bias_%d") % cat_idx)->array);
        if (boost::optional<std::string> bvalue = params.get_optional<std::string>("bias")) {
            auto bias_double = string_as_vector<double>(*bvalue,", ");
            lya_bias.resize(boost::extents[bias_double.size()]);
            std::copy(bias_double.begin(), bias_double.end(), lya_bias.begin());
            string fmt_str = "Set the bias to [";
            for (int i = 0; i < lya_bias.size()-1; i++)
              fmt_str += "%lg,";
            fmt_str += "%lg]";
            auto fmt = boost::format(fmt_str);
            for (int i = 0; i < lya_bias.size()-1; i++)
              fmt = fmt % lya_bias[i];
            fmt = fmt % lya_bias[lya_bias.size()-1];
            ctx.print(fmt);
        } else {
            ctx.print("No initial fgpa values set, use A=0.35, beta=1.6 and sigma2=0.001");
            
            int Nqso = (survey->get()).NumberQSO();
            
            lya_bias.resize(boost::extents[Nqso+3]);
            lya_bias[0] = 0.35; // A
            lya_bias[1] = 1.58;  // beta
            lya_bias[2] = 1.0; 	// Fc 
            
            for(int i=3; i<lya_bias.size(); i++){
          		lya_bias[i] = 0.001;
          	}          
          	
          	/*RandomGen *rgen = state.get<RandomGen>("random_generator");
            double SNRmin = 1.4;
            double SNRmax = 10;
            double alpha = -2.7;
          
            double x0 = pow(SNRmin, alpha+1);
            double x1 = pow(SNRmax, alpha+1);
          
            for(int i=3; i<lya_bias.size(); i++){
            	double aux = (x1 - x0) * rgen->get().uniform() + x0;
                double SNR = pow(aux, 1./(alpha+1));
          		lya_bias[i] = 0.15674599604853337 / SNR;
          	}*/
        }        
    }

    void prepareLOS(MPI_Communication *comm, MarkovState& state, int cat_idx, CosmologicalParameters& cosmo_params) {

        size_t N[3];
            N[0] = static_cast<SLong&>(state["N0"]);
            N[1] = static_cast<SLong&>(state["N1"]);
            N[2] = static_cast<SLong&>(state["N2"]);
            
        double L[3], delta[3], corner[3];
        ConsoleContext<LOG_INFO_SINGLE> ctx("los preparation");
        
        ctx.print(format("Project los to voxels (catalog %d)") % cat_idx);

        L[0] = static_cast<SDouble&>(state["L0"]);
        L[1] = static_cast<SDouble&>(state["L1"]);
        L[2] = static_cast<SDouble&>(state["L2"]);

        corner[0] = static_cast<SDouble&>(state["corner0"]);
        corner[1] = static_cast<SDouble&>(state["corner1"]);
        corner[2] = static_cast<SDouble&>(state["corner2"]);
        
        LymanAlphaSurveyType& survey = state.get<QSOElement>(str(format("qso_catalog_%d") % cat_idx))->get();
        
        delta[0] = L[0] / N[0];
        delta[1] = L[1] / N[1];
        delta[2] = L[2] / N[2];
		
		double observer[3] ={0.,0.,0.};

		/*for(int i=0; i<survey.NumberQSO(); i++)
		{
			double phi = survey.getQSO()[i].phi;
			double theta = survey.getQSO()[i].theta;
			double pointing[3]={ sin(theta) * cos(phi) , sin(theta) * sin(phi) , cos(theta) };
			
			ray_tracer_mock_data(observer, survey.getQSO()[i].r, pointing, corner, delta, N, survey.getProjection()[i], cosmo_params);
		}*/
    }

/*
    static void buildGrowthFactorLya(MarkovState& state, CosmologicalParameters& cosmo_param)
    {
        Cosmology cosmo(cosmo_param);
        ArrayType::ArrayType& growth = *state.get<ArrayType>("growth_factor")->array;

        // No growth factor here
        std::fill(growth.data(), growth.data() + growth.num_elements(), 1);
    }
*/

}


#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Natalia Porqueres
// ARES TAG: email(0) = n.porqueres@imperial.ac.uk
// ARES TAG: year(0) = 2020

