/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/samplers/lya/hades_lya_likelihood.cpp
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
#include "libLSS/samplers/lya/hades_lya_likelihood.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/samplers/core/powerspec_tools.hpp"
#include "libLSS/tools/hermiticity_fixup.hpp"
#include "libLSS/samplers/rgen/slice_sweep.hpp"

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

inline std::string get_qso_catalog_name(int c)
{
  return boost::str(boost::format("qso_catalog_%d") % c);
}

BorgLyAlphaLikelihood::BorgLyAlphaLikelihood(LikelihoodInfo &info)
    : HadesBaseDensityLyaLikelihood(info, 1026) {}
    
void BorgLyAlphaLikelihood::initializeLikelihood(MarkovState &state) {
  super_t::initializeLikelihood(state);
  LymanAlphaSurveyType &survey =
    state.get<QSOElement>(get_qso_catalog_name(0))->get();

  initialize_ghosts(survey);
  need_init_ghosts = 0;
  mock_data_generated = 0;
  
}

void BorgLyAlphaLikelihood::initialize_ghosts(LymanAlphaSurveyType &survey) {
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

void BorgLyAlphaLikelihood::setupDefaultParameters(MarkovState &state, int catalog) {
  LymanAlphaSurveyType &survey =
      state.get<QSOElement>(get_qso_catalog_name(0))->get();
  size_t Nlos = survey.NumberQSO();
  
  auto &local_bias =
      *state.formatGet<ArrayType1d>("galaxy_bias_%d", catalog)->array;
  local_bias[0] = 0.35; //A
  local_bias[1] = 1.58; //beta
  for(int i=2; i<Nlos; i++){
  	local_bias[i] = 0.01; //sigma2
  }
}

    
BorgLyAlphaLikelihood::~BorgLyAlphaLikelihood() {}

double
BorgLyAlphaLikelihood::logLikelihoodSpecific(ArrayRef const &out_density) {
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

  //auto coarse_density_p = mgr->allocate_array();
  //auto& coarse_density = coarse_density_p.get_array();
  
  //array::copyArray3d(coarse_density, out_density);
  //smooth(state, coarse_density, coarse_density, 0.3);
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

    auto &local_bias = *(bias[c]);
    double A = local_bias[0], beta = local_bias[1];
    double Fc = 1.;

    for(int nqso = startLos; nqso < finalLos; nqso++)
  	{
  		auto& qso = survey.getProjection()[nqso];
  		
  		for(int nlos=0; nlos<qso.voxel_id.size(); nlos++)
  		{
			long n0 = qso.voxel_id[nlos][0]; 
			long n1 = qso.voxel_id[nlos][1]; 
			long n2 = qso.voxel_id[nlos][2];
			double sigma = local_bias[nlos+2];
			
			double rho;
			
			if ((n0 < startN0) || (n0 > (endN0-1))) {
			  auto& plane = ghosts.getPlane(n0);
			  rho = plane[n1][n2];
			} else {
			  rho = out_density[n0][n1][n2];
			}
			
			double data = qso.flux[nlos];
			double flux = exp(- A * pow((1. + rho),beta) );
			
			if (isnan(rho)) {
		      ctx.print(
		          format("rho=%1%") %
		          rho);
		    }
			
			if (isnan(pow((1. + rho),beta))) {
		      ctx.print(
		          format("pow((1. + rho),beta)=%1%") %
		          pow((1. + rho),beta));
		    }
			
			if (isnan(flux)) {
		      ctx.print(
		          format("flux=%1% pow((1. + rho),beta)=%2% rho=%3%") %
		          flux % pow((1. + rho),beta) % rho);
		    }
		    
		    if (isnan(data)) {
		      ctx.print(
		          format("data=%1%") %
		          data);
		    }
		    
		    if (isnan(local_bias[nqso+2])) {
		      ctx.print(
		          format("sigma2[nqso]=%1%") % local_bias[nqso+2]);
		    }
		    
		    if (isnan(log(local_bias[nqso+2]))) {
		      ctx.print(
		          format("log(sigma2[nqso])=%1%") % log(local_bias[nqso+2]));
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
  // the sum over cores is now performed by base_likelihood.cpp
  return LyaLikelihood;
}


void BorgLyAlphaLikelihood::gradientLikelihoodSpecific(
  ArrayRef const &out_density, ArrayRef &real_gradient){
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  
  if(need_init_ghosts==1){
    LymanAlphaSurveyType &survey =
      state->get<QSOElement>(get_qso_catalog_name(0))->get();
    initialize_ghosts(survey);
    need_init_ghosts=0;
  }
  
  using CosmoTool::square;

  //auto coarse_density_p = mgr->allocate_array();
  //auto& coarse_density = coarse_density_p.get_array();
  
  //array::copyArray3d(coarse_density, out_density);
  //smooth(state, coarse_density, coarse_density, 0.3);
  
  size_t const startN0 = mgr->startN0, endN0 = mgr->startN0 + mgr->localN0;
  size_t const N1 = mgr->N1, N2 = mgr->N2, localN0 = mgr->localN0, N2real = mgr->N2real;

  fwrap(real_gradient) = 0;
   
  //auto fine_gradient_p = mgr->allocate_array();
  //auto& fine_gradient = fine_gradient_p.get_array();
  //array::fill(fine_gradient, 0);
  
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

	auto &local_bias = *(bias[c]);
    double A = local_bias[0], beta = local_bias[1];
    double Fc = 1.;
    
    for (int nqso = startLos; nqso < finalLos; nqso++) {
      auto &qso = survey.getProjection()[nqso];
      //#pragma omp parallel for
      for (int nlos = 0; nlos < qso.voxel_id.size(); nlos++) {
        long n0 = qso.voxel_id[nlos][0];
        long n1 = qso.voxel_id[nlos][1];
        long n2 = qso.voxel_id[nlos][2];
        double sigma = local_bias[nlos+2];
        double rho;
        
        if ((n0 < startN0) || (n0 > (endN0 - 1))) {
          auto &plane = ghosts.getPlane(n0);
          rho = plane[n1][n2];
        } else {
          rho = out_density[n0][n1][n2]; 
        }
		  
        if(rho<-1){
            rho = - 1 + 1e-6;
        }
        
        double data = qso.flux[nlos];
        
        
        double flux = exp(-A * pow((1. + rho), beta));
        double dflux = beta * A * pow((1. + rho), beta - 1);

        if (isnan(flux)) {
          ctx.print(
              format("A=%1% beta=%2%  sigma2[nqso] =%8% s=%3% n0=%5% n1=%6% "
                     "n2=%7% flux=%4%, density=%9%, pow=%10%, diff=%11%") %
              A % beta % rho % flux % n0 % n1 % n2 % local_bias[nqso+2] %rho %pow((1+rho),beta) %(1+rho));
          comm->abort();
        }
        if (isnan(dflux)) {
          ctx.print(
              format("A=%1% beta=%2% sigma2[nqso]=%6% s=%3% flux=%4% dflux=%5%") %
              A % beta % rho % flux % dflux % local_bias[nqso+2]);
          comm->abort();
        }

        if (local_bias[nqso+2] < 1.0e-36) {
          ctx.print(
              format("A=%1% beta=%2% sigma2[nqso]=%6% s=%3% flux=%4% dflux=%5%") %
              A % beta % rho % flux % dflux % local_bias[nqso+2]);
          comm->abort();
        }
        
        //#pragma omp atomic
        if ((n0 < startN0) || (n0 > (endN0 - 1))) {
          auto &ag_plane = ghosts.ag_getPlane(n0);
          ag_plane[n1][n2] += (data - Fc * flux) * Fc * flux * dflux / sigma; 
        } else {
          real_gradient[n0][n1][n2] += (data - Fc * flux) * Fc * flux * dflux / sigma;
        }
      }
    }
  }
  
  ghosts.synchronize_ag(real_gradient);
  
  //smooth_gradient(state, fine_gradient, real_gradient, 0.3);
  
}

void BorgLyAlphaLikelihood::smooth(MarkovState &state, Uninit_FFTW_Real_Array::array_type& in, Uninit_FFTW_Real_Array::array_type& out, double sigmaKernel)
{  
	LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
	ctx.print("BORG_LyAlpha smoothing density");
	
  	auto tmp_complex_field_p = mgr->allocate_complex_array();
    auto& tmp_complex_field = tmp_complex_field_p.get_array();
	
	long N0 = state.getScalar<long>("N0");
	long N1 = state.getScalar<long>("N1");
	long N2 = state.getScalar<long>("N2");
	long N2_HC = state.getScalar<long>("N2_HC");
	
	double L0 = state.getScalar<double>("L0");
	double L1 = state.getScalar<double>("L1");
	double L2 = state.getScalar<double>("L2");
	
	size_t const startN0 = mgr->startN0, endN0 = mgr->startN0 + mgr->localN0;
	
	MFCalls::execute_r2c(analysis_plan, in.data(), tmp_complex_field.data());
  	
  	//auto *kernel_array = tmp_complex_field;
  	
	double norm = N0*N1*N2; 
	double sigma2 = sigmaKernel * sigmaKernel;
	
	//2) Muldiply in_hat with kernel
	#pragma omp parallel for
		for (long n0 = startN0; n0 < endN0; n0++)
		  for (long n1 = 0; n1 < N1; n1++)
		     for (long n2 = 0; n2 < N2_HC; n2++){
	     	    double kk[3] = {kmode(n0, N0, L0), kmode(n1, N1, L1),
                          kmode(n2, N2, L2)}; 
                double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
		     	double kernel = exp(-0.5*ksquared/sigma2)/sqrt(2*M_PI*sigma2);
		     	
		     	//(*kernel_array)[n0][n1][n2] = kernel;
		     	tmp_complex_field[n0][n1][n2] *= kernel / norm;
		     	//tmp_complex_field[n0][n1][n2] /= norm;
		     	
		}
	
	Mgr::plan_type synthesis_plan = mgr->create_c2r_plan(tmp_complex_field.data(),out.data());
      	
	MFCalls::execute_c2r(synthesis_plan, tmp_complex_field.data(), out.data());
	
	
	/*MFCalls::execute_c2r(synthesis_plan, kernel_array->data(), tmp_real_field->data());
	H5::H5File ff(str(format("kernel_01.h5_%d") % comm->rank()), H5F_ACC_TRUNC);
    hdf5_write_array(ff, "kernel", *tmp_real_field);
	*/    
	ctx.print("Done with FFT in smooth density");
    
}

void BorgLyAlphaLikelihood::smooth(MarkovState *state, Uninit_FFTW_Real_Array::array_type& in, Uninit_FFTW_Real_Array::array_type& out, double sigmaKernel)
{  
	LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
	auto tmp_complex_field_p = mgr->allocate_complex_array();
    auto &tmp_complex_field = tmp_complex_field_p.get_array();
    
	size_t const N0 = mgr->N0, N1 = mgr->N1, N2 = mgr->N2, N2_HC = mgr->N2_HC;
	double L0 = state->getScalar<double>("L0");
	double L1 = state->getScalar<double>("L1");
	double L2 = state->getScalar<double>("L2");
	size_t const startN0 = mgr->startN0, endN0 = mgr->startN0 + mgr->localN0;	
	//1) FFT of in to F-space
	// BEWARE: in-field is destroyed!
  	
	Console::instance().print<LOG_DEBUG>("execute");   
  	MFCalls::execute_r2c(analysis_plan, in.data(), tmp_complex_field.data());
  	
	double norm = N0*N1*N2;
	double sigma2 = sigmaKernel * sigmaKernel;

	Console::instance().print<LOG_DEBUG>("enter loop");   
	//2) Muldiply in_hat with kernel
	#pragma omp parallel for
		for (long n0 = startN0; n0 < endN0; n0++)
		  for (long n1 = 0; n1 < N1; n1++)
		     for (long n2 = 0; n2 < N2_HC; n2++){
	     	    double kk[3] = {kmode(n0, N0, L0), kmode(n1, N1, L1),
                          kmode(n2, N2, L2)}; 
                double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
		     	double kernel = exp(-0.5*ksquared/sigma2)/sqrt(2*M_PI*sigma2);
		     	
		     	tmp_complex_field[n0][n1][n2] *= kernel / norm;
		     	//tmp_complex_field[n0][n1][n2] /= norm;
		     	
	}
	
	Mgr::plan_type synthesis_plan = mgr->create_c2r_plan(tmp_complex_field.data(),out.data());	
	ctx.print("execute back");   
	MFCalls::execute_c2r(synthesis_plan, tmp_complex_field.data(), out.data());
	ctx.print("Done with FFT in smooth");       
	

}


void BorgLyAlphaLikelihood::smooth_gradient(MarkovState *state, Uninit_FFTW_Real_Array::array_type& in, Uninit_FFTW_Real_Array::array_type& out, double sigmaKernel)
{   
    LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
	auto tmp_complex_field_p = mgr->allocate_complex_array();
    auto &tmp_complex_field = tmp_complex_field_p.get_array();
    
	size_t const N0 = mgr->N0, N1 = mgr->N1, N2 = mgr->N2, N2_HC = mgr->N2_HC;
	double L0 = state->getScalar<double>("L0");
	double L1 = state->getScalar<double>("L1");
	double L2 = state->getScalar<double>("L2");
	size_t const startN0 = mgr->startN0, endN0 = mgr->startN0 + mgr->localN0;	
	//1) FFT of in to F-space
	// BEWARE: in-field is destroyed!
  	
	Console::instance().print<LOG_DEBUG>("execute");   
  	MFCalls::execute_r2c(analysis_plan, in.data(), tmp_complex_field.data());
  	
  	double norm = N0*N1*N2;
	double sigma2 = sigmaKernel * sigmaKernel;
	
	Console::instance().print<LOG_DEBUG>("enter loop");   
	//2) Muldiply in_hat with kernel
	#pragma omp parallel for
		for (long n0 = startN0; n0 < endN0; n0++)
		  for (long n1 = 0; n1 < N1; n1++)
		     for (long n2 = 0; n2 < N2_HC; n2++){
	     	    double kk[3] = {kmode(n0, N0, L0), kmode(n1, N1, L1),
                          kmode(n2, N2, L2)}; 
                double ksquared = kk[0] * kk[0] + kk[1] * kk[1] + kk[2] * kk[2];
		     	double kernel = exp(-0.5*ksquared/sigma2)/sqrt(2*M_PI*sigma2);
		     	
		     	tmp_complex_field[n0][n1][n2] *= kernel / norm;
		        //tmp_complex_field[n0][n1][n2] /= norm;
	}
	
	Mgr::plan_type synthesis_plan = mgr->create_c2r_plan(tmp_complex_field.data(),out.data());	
	ctx.print("execute back");   
	MFCalls::execute_c2r(synthesis_plan, tmp_complex_field.data(), out.data());
	ctx.print("Done with FFT in smooth");   
}

void BorgLyAlphaLikelihood::generateMockSpecific(
  ArrayRef const &out_density, MarkovState &state) {
  LIBLSS_AUTO_CONTEXT(LOG_INFO, ctx);
  RandomGen *rgen = state.get<RandomGen>("random_generator");
  
  if(need_init_ghosts==1){
    LymanAlphaSurveyType &survey =
      state.get<QSOElement>(get_qso_catalog_name(0))->get();
    initialize_ghosts(survey);
    need_init_ghosts=0;
  }

  //auto coarse_density_p = mgr->allocate_array();
  //auto& coarse_density = coarse_density_p.get_array();
  //array::copyArray3d(coarse_density, out_density);
  //smooth(state, coarse_density, coarse_density, 0.3);
  
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

      auto &local_bias = *(bias[c]);
      double A = local_bias[0], beta = local_bias[1];
       
	  ctx.print(boost::format("Done lines of sight for catalog %d") % c);
      for (int nqso = startLos; nqso < finalLos; nqso++) {
        auto &qso = survey.getProjection()[nqso];
        double cont_err = pow(0.005,0.5) * rgen->get().gaussian();         
        for (int nlos = 0; nlos < qso.voxel_id.size(); nlos++) {
          long n0 = qso.voxel_id[nlos][0];
          long n1 = qso.voxel_id[nlos][1];
          long n2 = qso.voxel_id[nlos][2];
          double sigma = local_bias[nlos+2];
          
          double rho;		  
          
          if ((n0 < startN0) || (n0 > (endN0-1))) {
			  auto& plane = ghosts.getPlane(n0);
			  rho = plane[n1][n2];
		  } else {
			  rho = out_density[n0][n1][n2];
	      }
		  
		  if(rho<-1) std::cout << "WARNING: " << rho << std::endl;
		 
		  qso.flux[nlos] = exp(-A * pow((1. + rho), beta)) + pow(sigma,0.5) * rgen->get().gaussian(); // + cont_err; 	
		 
		}
      }
    }
    
    mock_data_generated = 1;
}

void BorgLyAlphaLikelihood::updateMetaParameters(MarkovState &state) {
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
  
  if(mock_data_generated)
    sampleMeta(state);
  
}  

void BorgLyAlphaLikelihood::updateBiasParameters(
    int catalog, BiasArray const &params) {
  fwrap(*bias[catalog]) = fwrap(params);
}


void BorgLyAlphaLikelihood::sampleMeta(MarkovState &state) {
  LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);
  RandomGen *rng = state.get<RandomGen>("random_generator");
    
  if (state.getScalar<bool>("bias_sampler_blocked"))
    return;

  auto const &density = *state.get<ArrayType>("BORG_final_density")->array;
  double const ares_heat = state.getScalar<double>("ares_heat");

  for (int c = 0; c < Ncat; c++) {
    auto &bias = *state.get<ArrayType1d>(format("galaxy_bias_%d") % c)->array;

    ctx.print(format("considering catalog %d") % c);

    for (int ib = 0; ib < 2; ib++) {
      bias[ib] = slice_sweep(
          comm, rng->get(),
          [&](double x) -> double {
            boost::multi_array<double, 1> loc_bias = bias;
            loc_bias[ib] = x;
            updateBiasParameters(c, loc_bias);
            return -ares_heat*logLikelihoodSpecific(density);
          },
          bias[ib], 0.001);
       updateBiasParameters(c, bias);
    }
  }
}

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Natalia Porqueres
// ARES TAG: email(0) = n.porqueres@imperial.ac.uk
// ARES TAG: year(0) = 2020

