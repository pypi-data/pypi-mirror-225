#include <math.h>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>         
#include <cassert>
#include <cfloat>
#include <float.h>
#include <stdlib.h>
#include <stdio.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include "libLSS/samplers/core/ran_gig.h"

#define EPSILON 1e-10

using namespace std;

/* R_zeroin2() is faster for "expensive" f(), in those typical cases where
 *             f(ax) and f(bx) are available anyway : */

double R_zeroin2(			/* An estimate of the root */
    double ax,				/* Left border | of the range	*/
    double bx,				/* Right border| the root is seeked*/
    double fa, double fb,		/* f(a), f(b) */
    double (*f)(double x, void *info),	/* Function under investigation	*/
    void *info,				/* Add'l info passed on to f	*/
    double *Tol,			/* Acceptable tolerance		*/
    int *Maxit)				/* Max # of iterations */
{
    double a,b,c, fc;			/* Abscissae, descr. see above,  f(c) */
    double tol;
    int maxit;

    a = ax;  b = bx;
    c = a;   fc = fa;
    maxit = *Maxit + 1; tol = * Tol;

    /* First test if we have found a root at an endpoint */
    if(fa == 0.0) {
	*Tol = 0.0;
	*Maxit = 0;
	return a;
    }
    if(fb ==  0.0) {
	*Tol = 0.0;
	*Maxit = 0;
	return b;
    }

    while(maxit--)		/* Main iteration loop	*/
    {
	double prev_step = b-a;		/* Distance from the last but one
					   to the last approximation	*/
	double tol_act;			/* Actual tolerance		*/
	double p;			/* Interpolation step is calcu- */
	double q;			/* lated in the form p/q; divi-
					 * sion operations is delayed
					 * until the last moment	*/
	double new_step;		/* Step at this iteration	*/

	if( fabs(fc) < fabs(fb) )
	{				/* Swap data for b to be the	*/
	    a = b;  b = c;  c = a;	/* best approximation		*/
	    fa=fb;  fb=fc;  fc=fa;
	}
	tol_act = 2.*EPSILON*fabs(b) + tol/2.;
	new_step = (c-b)/2.;

	if( fabs(new_step) <= tol_act || fb == (double)0 )
	{
	    *Maxit -= maxit;
	    *Tol = fabs(c-b);
	    return b;			/* Acceptable approx. is found	*/
	}

	/* Decide if the interpolation can be tried	*/
	if( fabs(prev_step) >= tol_act	/* If prev_step was large enough*/
	    && fabs(fa) > fabs(fb) ) {	/* and was in true direction,
					 * Interpolation may be tried	*/
	    register double t1,cb,t2;
	    cb = c-b;
	    if( a==c ) {		/* If we have only two distinct	*/
					/* points linear interpolation	*/
		t1 = fb/fa;		/* can only be applied		*/
		p = cb*t1;
		q = 1.0 - t1;
	    }
	    else {			/* Quadric inverse interpolation*/

		q = fa/fc;  t1 = fb/fc;	 t2 = fb/fa;
		p = t2 * ( cb*q*(q-t1) - (b-a)*(t1-1.0) );
		q = (q-1.0) * (t1-1.0) * (t2-1.0);
	    }
	    if( p>(double)0 )		/* p was calculated with the */
		q = -q;			/* opposite sign; make p positive */
	    else			/* and assign possible minus to	*/
		p = -p;			/* q				*/

	    if( p < (0.75*cb*q-fabs(tol_act*q)/2.) /* If b+p/q falls in [b,c]*/
		&& p < fabs(prev_step*q/2.) )	/* and isn't too large	*/
		new_step = p/q;			/* it is accepted
						 * If p/q is too large then the
						 * bisection procedure can
						 * reduce [b,c] range to more
						 * extent */
	}

	if( fabs(new_step) < tol_act) {	/* Adjust the step to be not less*/
	    if( new_step > (double)0 )	/* than tolerance		*/
		new_step = tol_act;
	    else
		new_step = -tol_act;
	}
	a = b;	fa = fb;			/* Save the previous approx. */
	b += new_step;	fb = (*f)(b, info);	/* Do step to a new approxim. */
	if( (fb > 0. && fc > 0.) || (fb < 0. && fc < 0.) ) {
	    /* Adjust c for it to have a sign opposite to that of b */
	    c = a;  fc = fa;
	}

    }
    /* failed! */
    *Tol = fabs(c-b);
    *Maxit = -1;
    return b;
}


double R_zeroin(			/* An estimate of the root */
    double ax,				/* Left border | of the range	*/
    double bx,				/* Right border| the root is seeked*/
    double (*f)(double x, void *info),	/* Function under investigation	*/
    void *info,				/* Add'l info passed on to f	*/
    double *Tol,			/* Acceptable tolerance		*/
    int *Maxit)				/* Max # of iterations */
{
    double fa = (*f)(ax, info);
    double fb = (*f)(bx, info);
    return R_zeroin2(ax, bx, fa, fb, f, info, Tol, Maxit);
}



double g(double y, void *params)
{
  double *aux = (double *)params;
  double beta=aux[0];
  double lambda=aux[1];
  double m=aux[2];
  
return(0.5*beta*y*y*y - y*y*(0.5*beta*m+lambda+1) + y*((lambda-1)*m-0.5*beta) + 0.5*beta*m);
}

double LibLSS::ran_gig(double chi, double psi, double lambda,gsl_rng * SEED)
{
// Function to generate random observations from a
// generalized inverse Gaussian distribution. The
// algorithm is based on that given by Dagpunar (1989)

  if(chi<0.) {cout << "chi can not be negative"<<endl; return 0.;}
  if(psi<0.) {cout << "psi can not be negative"<<endl; return 0.;}

  if((lambda>=0.)&&(psi==0.))
  {
    cout << "When lambda >= 0, psi must be > 0"<<endl;
    return 0.;
  }

  if((lambda<=0.)&(chi==0.))
  {
    cout <<"When lambda <= 0, chi must be > 0"<<endl;
    return 0.;
  }
 
  if(chi==0.) {cout <<"chi = 0, use rgamma"<<endl; return 0.;}
  if(psi==0.) {cout <<"algorithm only valid for psi > 0"<<endl; return 0.;}

  double alpha=sqrt(psi/chi);
  double beta=sqrt(psi*chi);

  double m=(lambda-1.+sqrt((lambda-1.)*(lambda-1.)+beta*beta))/beta;
    
  double upper = m;
  
  double params[3];
  params[0]=beta;
  params[1]=lambda;
  params[2]=m;
  
  while(g(upper,params)<=0.) upper = 2.*upper;


  double tol=1e-10;
  int maxit=10000;
    
  double yM =R_zeroin(0.,m,&g, &params,&tol,&maxit);// uniroot(g,interval=c(0,m))$root
  double yP =R_zeroin(m,upper,&g, &params,&tol,&maxit);// uniroot(g,interval=c(m,upper))$root
  
  double a = (yP-m)*exp(-0.25*beta*(yP+1./yP-m-1./m)+(log(yP) -log(m))*(0.5*(lambda-1.)) );
  double b = (yM-m)*exp(-0.25*beta*(yM+1./yM-m-1./m)+(log(yM) -log(m))*(0.5*(lambda-1.)) );
  double c = -0.25*beta*(m+1./m) + 0.5*(lambda-1.)*log(m);

  double y=0;

  while(true){
      double R1 = gsl_rng_uniform (SEED);
      double R2 = gsl_rng_uniform (SEED);
      y= m + a*R2/R1 + b*(1.-R2)/R1;
      if((y>0.) && (-log(R1)>=-0.5*(lambda-1.)*log(y)+0.25*beta*(y+1./y)+c)) break;
  }
  
  return(y/alpha);
}
