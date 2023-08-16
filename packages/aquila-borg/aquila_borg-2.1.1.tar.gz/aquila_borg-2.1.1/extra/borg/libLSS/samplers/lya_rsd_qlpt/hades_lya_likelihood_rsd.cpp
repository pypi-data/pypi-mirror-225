/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/lya_rsd_qlpt/hades_lya_likelihood_rsd.cpp
    Copyright (C) 2020 Natalia Porqueres <n.porqueres@imperial.ac.uk>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <math.h>
#include <CosmoTool/algo.hpp>
#include <cmath>
#include <Eigen/Core>
#include <boost/format.hpp>
#include <boost/bind.hpp>
#include <boost/lambda/lambda.hpp>
#include <CosmoTool/hdf5_array.hpp>
#include <CosmoTool/fourier/fft/fftw_calls.hpp>
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/samplers/core/random_number.hpp"
#include "libLSS/tools/mpi_fftw_helper.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/samplers/lya_rsd_qlpt/hades_lya_likelihood_rsd.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "libLSS/tools/hermiticity_fixup.hpp"

using namespace LibLSS;
using boost::extents;
using boost::format;

using CosmoTool::hdf5_write_array;
using CosmoTool::square;
 
using boost::c_storage_order;
typedef boost::multi_array_types::extent_range range;

typedef Eigen::Map<Eigen::ArrayXd, Eigen::Aligned> MappedArray;

typedef LymanAlphaSurvey<BaseLymanAlphaDescriptor> LymanAlphaSurveyType;
typedef ObjectStateElement<LymanAlphaSurveyType, true> QSOElement;

static const int ROOT_RANK = 0;
static const bool VERBOSE_WRITE_BORG = false;

namespace L = LibLSS::Likelihood;

BorgLyAlphaRsdLikelihood::BorgLyAlphaRsdLikelihood(LikelihoodInfo &info)
    : HadesBaseDensityLyaLikelihood(info, 3) {}

inline std::string get_qso_catalog_name(int c)
{
  return boost::str(boost::format("qso_catalog_%d") % c);
}
    
void BorgLyAlphaRsdLikelihood::initializeLikelihood(MarkovState &state) {
  super_t::initializeLikelihood(state);
  LymanAlphaSurveyType &survey =
    state.get<QSOElement>(get_qso_catalog_name(0))->get();

  initialize_ghosts(survey);
  need_init_ghosts = 0;
  
}

void BorgLyAlphaRsdLikelihood::initialize_ghosts(LymanAlphaSurveyType &survey) {
  size_t task = comm->rank();
  size_t Ntask = comm->size();
  
  size_t const startN0 = mgr->startN0, localN0 = mgr->localN0; 
  size_t const endN0 = startN0 + localN0; 
  size_t const N0 = mgr->N0, N1 = mgr->N1, N2real = mgr->N2real;

  size_t Nlos = survey.NumberQSO();

  size_t startLos = task * Nlos / Ntask;
  size_t finalLos = (task + 1) * Nlos / Ntask;
  
  Console &cons = Console::instance();

  cons.print<LOG_STD>(format("startLos %lg") % startLos);
  cons.print<LOG_STD>(format("finalLos %lg") % finalLos);

  std::vector<size_t> owned_planes(localN0);

  std::set<size_t> plane_ids;
  for (size_t i = 0; i < localN0; i++)
    owned_planes[i] = startN0 + i; 
 
  for (size_t nqso = startLos; nqso < finalLos; nqso++) {
    auto &qso = survey.getProjection()[nqso];
    for (int nlos = 0; nlos < qso.voxel_id.size(); nlos++) {
      long n0 = qso.voxel_id[nlos][0];
      if ((n0 < startN0) || (n0 > (endN0 - 1))) {
      	plane_ids.insert(n0);
      }
    }
  }
  
  cons.print<LOG_DEBUG>(format("Ghost setup : N0=%d, N1=%d, N2real=%d") % N0 % N1 % N2real);
  ghosts.setup(
      comm, plane_ids, owned_planes,
      std::array<size_t, 2>{size_t(N1), size_t(N2real)}, N0);

}

void BorgLyAlphaRsdLikelihood::setupDefaultParameters(MarkovState &state, int catalog) {
  LymanAlphaSurveyType &survey =
      state.get<QSOElement>(get_qso_catalog_name(0))->get();
  size_t Nlos = survey.NumberQSO();
  
  auto &local_bias =
      *state.formatGet<ArrayType1d>("galaxy_bias_%d", catalog)->array;
  local_bias[0] = 0.35; //A
  local_bias[1] = 1.58; //beta
  local_bias[2] = 1.0;  //F_c
  for(int i=3; i<Nlos; i++){
  	local_bias[i] = 0.1; //sigma2
  }
}

    
BorgLyAlphaRsdLikelihood::~BorgLyAlphaRsdLikelihood() {}

double
BorgLyAlphaRsdLikelihood::logLikelihoodSpecific(ArrayRef const &out_density) {
  if(need_init_ghosts==1){
    LymanAlphaSurveyType &survey =
      state->get<QSOElement>(get_qso_catalog_name(0))->get();
    initialize_ghosts(survey);
    need_init_ghosts=0;
  }
  
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  using boost::lambda::_1;
  using CosmoTool::square;
  
  typedef ArrayType::ArrayType::element ElementType;
  double LyaLikelihood = 0;

  ghosts.synchronize(out_density);

  size_t task = comm->rank();
  size_t Ntask = comm->size();
  size_t startN0 = mgr->startN0, endN0 = mgr->startN0 + mgr->localN0;  

  for (int c = 0; c < Ncat; c++) {
  	LymanAlphaSurveyType &survey =
      state->get<QSOElement>(get_qso_catalog_name(c))->get();  
  	
  	size_t Nlos = survey.NumberQSO();
    size_t startLos = task * Nlos / Ntask;
    size_t finalLos = (task +1) * Nlos / Ntask;

    auto &fgpa_bias = *(bias[c]);
    double A = fgpa_bias[0], beta = fgpa_bias[1], Fc = fgpa_bias[2];
    
    for(int nqso = startLos; nqso < finalLos; nqso++)
  	{
  		auto& qso = survey.getProjection()[nqso];
  		
  		for(int nlos=0; nlos<qso.voxel_id.size(); nlos++)
  		{
			long n0 = qso.voxel_id[nlos][0]; 
			long n1 = qso.voxel_id[nlos][1]; 
			long n2 = qso.voxel_id[nlos][2];
			
			double tau;
			
			if ((n0 < startN0) || (n0 > (endN0-1))) {
			  auto& plane = ghosts.getPlane(n0);
			  tau = plane[n1][n2];
			} else {
			  tau = out_density[n0][n1][n2];
			}
			
			
			A = 0.35;
	        beta = 1.58;
	        double sigma = 0.1;
		  
      
			double data = qso.flux[nlos];
			double flux = exp(- tau );
			
			
		    
		    if (isnan(data)) {
		      ctx.print(
		          format("data=%1%") %
		          data);
		    }
		    
		    if (isnan(fgpa_bias[nqso+3])) {
		      ctx.print(
		          format("sigma2[nqso]=%1%") % fgpa_bias[nqso+3]);
		    }
		    
		    if (isnan(log(fgpa_bias[nqso+3]))) {
		      ctx.print(
		          format("log(sigma2[nqso])=%1%") % log(fgpa_bias[nqso+3]));
		    }
		    
		    if (isnan(square(data - flux))) {
		      ctx.print(
		          format("square(data - flux)=%1%") %
		          square(data - flux));
		    }
			
			LyaLikelihood += square(data - Fc * flux) / (sigma) + log(sigma) ;
			}  	 
	} 
  }
 
  LyaLikelihood *= 0.5 ;
  // the sum over core is now performed by base_lya_likelihood.cpp
  return LyaLikelihood;
}


void BorgLyAlphaRsdLikelihood::gradientLikelihoodSpecific(
  ArrayRef const &out_density, ArrayRef &real_gradient){
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  
  if(need_init_ghosts==1){
    LymanAlphaSurveyType &survey =
      state->get<QSOElement>(get_qso_catalog_name(0))->get();
    initialize_ghosts(survey);
    need_init_ghosts=0;
  }
  
  using CosmoTool::square;
  
  size_t const startN0 = mgr->startN0, endN0 = mgr->startN0 + mgr->localN0;
  size_t const N1 = mgr->N1, N2 = mgr->N2, localN0 = mgr->localN0, N2real = mgr->N2real;

  fwrap(real_gradient) = 0;
   
  
  ghosts.synchronize(out_density);
  ghosts.clear_ghosts();

  size_t task = comm->rank();
  size_t Ntask = comm->size();

  //#pragma omp parallel for
  for (int c = 0; c < Ncat; c++) {
    
    LymanAlphaSurveyType &survey =
      state->get<QSOElement>(get_qso_catalog_name(c))->get();

    size_t Nlos = survey.NumberQSO();
    size_t startLos = task * Nlos / Ntask;
    size_t finalLos = (task + 1) * Nlos / Ntask;

	auto &fgpa_bias = *(bias[c]);
	double A = fgpa_bias[0], beta = fgpa_bias[1], Fc = fgpa_bias[2];
    
    for (int nqso = startLos; nqso < finalLos; nqso++) {
      auto &qso = survey.getProjection()[nqso];
      //#pragma omp parallel for
      for (int nlos = 0; nlos < qso.voxel_id.size(); nlos++) {
        long n0 = qso.voxel_id[nlos][0];
        long n1 = qso.voxel_id[nlos][1];
        long n2 = qso.voxel_id[nlos][2];
        double tau;
        
        if ((n0 < startN0) || (n0 > (endN0 - 1))) {
          auto &plane = ghosts.getPlane(n0);
          tau = plane[n1][n2];
        } else {
          tau = out_density[n0][n1][n2]; 
        }
		  
        double data = qso.flux[nlos];
        
        A = 0.35;
	    beta = 1.58;
	    double sigma = 0.1;
			
        double flux = exp(-tau);
        double dflux = - exp(-tau);
        
        
        //#pragma omp atomic
        if ((n0 < startN0) || (n0 > (endN0 - 1))) {
          auto &ag_plane = ghosts.ag_getPlane(n0);
          ag_plane[n1][n2] += (data - Fc * flux) * Fc * flux  / sigma; 
        } else {
          real_gradient[n0][n1][n2] += (data - Fc * flux) * Fc * flux  / sigma;
        }
      }
    }
  }
  
  ghosts.synchronize_ag(real_gradient);
  
}


void BorgLyAlphaRsdLikelihood::generateMockSpecific(
  ArrayRef const &out_density, MarkovState &state) {
  LIBLSS_AUTO_CONTEXT(LOG_INFO, ctx);
  RandomGen *rgen = state.get<RandomGen>("random_generator");
  
  if(need_init_ghosts==1){
    LymanAlphaSurveyType &survey =
      state.get<QSOElement>(get_qso_catalog_name(0))->get();
    initialize_ghosts(survey);
    need_init_ghosts=0;
  }
  
  long N0 = state.getScalar<long>("N0");
  long N1 = state.getScalar<long>("N1");
  long N2 = state.getScalar<long>("N2");
  
  ssize_t startN0 = mgr->startN0, endN0 = mgr->startN0 + mgr->localN0;
  ctx.print(format("shape is %dx%dx%d") % out_density.shape()[0] %out_density.shape()[1] %out_density.shape()[2] );
  
  ghosts.synchronize(out_density);
  
  size_t task = comm->rank();
  size_t Ntask = comm->size();  
 
  ctx.print("Now generate mock data");
  for (int c = 0; c < Ncat; c++) {

      LymanAlphaSurveyType &survey =
          state.get<QSOElement>(get_qso_catalog_name(c))->get();
      size_t Nlos = survey.NumberQSO();
      size_t startLos = task * Nlos / Ntask;
      size_t finalLos = (task + 1) * Nlos / Ntask; 

	  auto &fgpa_bias = *(bias[c]);
	  double A = fgpa_bias[0], beta = fgpa_bias[1], Fc = fgpa_bias[2];
	   
	  ctx.print(boost::format("Done lines of sight for catalog %d") % c);
      for (int nqso = startLos; nqso < finalLos; nqso++) {
        auto &qso = survey.getProjection()[nqso];
        double cont_err = pow(0.005,0.5) * rgen->get().gaussian();         
        for (int nlos = 0; nlos < qso.voxel_id.size(); nlos++) {
          long n0 = qso.voxel_id[nlos][0];
          long n1 = qso.voxel_id[nlos][1];
          long n2 = qso.voxel_id[nlos][2];
          double tau;		  
          
          if ((n0 < startN0) || (n0 > (endN0-1))) {
			  auto& plane = ghosts.getPlane(n0);
			  tau = plane[n1][n2];
		  } else {
			  tau = out_density[n0][n1][n2];
	      }
		  
		  A = 0.35;
		  beta = 1.58;
		  double sigma = 0.1;
		  qso.flux[nlos] = exp(-tau) + pow(sigma,0.5) * rgen->get().gaussian(); 	
		 
		}
      }
    }
}

void BorgLyAlphaRsdLikelihood::updateMetaParameters(MarkovState &state) {
    this->state = &state; 
	
    LIBLSS_AUTO_CONTEXT(LOG_VERBOSE, ctx);
    auto cosmo_params = state.getScalar<CosmologicalParameters>("cosmology");
	
    //initialize model uncertainty 
    model = state.get<BorgModelElement>("BORG_model")->obj; 
    ai = state.getScalar<double>("borg_a_initial"); 
	
    // Update forward model for maybe new cosmo params
    model->setCosmoParams(cosmo_params);

    // Update forward model for maybe new cosmo params 
    updateCosmology(cosmo_params);
	
	auto e_Ncat = boost::extents[Ncat];
    nmean.resize(e_Ncat);
    biasRef.resize(Ncat);
    data.resize(Ncat);
    bias.resize(Ncat);
    
    for (int c = 0; c < Ncat; c++) {
		auto &stateBias =
		    *state.get<ArrayType1d>(format("galaxy_bias_%d") % c)->array;
		if (stateBias.size() < numBiasParams) {
		  stateBias.resize(boost::extents[numBiasParams]);
		}

		bias[c] = std::make_unique<BiasArray>(boost::extents[stateBias.size()]);

		fwrap(*bias[c]) = fwrap(stateBias);
		ctx.print(format(" b0=%g") % (*bias[c])[0]);
  }
  
}  

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Natalia Porqueres
// ARES TAG: email(0) = n.porqueres@imperial.ac.uk
// ARES TAG: year(0) = 2020

