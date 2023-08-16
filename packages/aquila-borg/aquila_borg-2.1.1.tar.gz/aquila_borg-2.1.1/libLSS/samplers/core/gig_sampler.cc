#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <iomanip>
#include <math.h>
#include <cassert>
#include <iostream>
#include <fstream>
#include <cfloat>
#include <string>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include "gig_sampler.hpp"

using namespace std;

using namespace LibLSS;

static double psi(double x, double alpha, double lambd)
{
 return (-alpha*(cosh(x) -1.)-lambd*(exp(x)-x-1.)); 
}

static double psi_prime(double x, double alpha,double lambd)
{
  return (-alpha*sinh(x)-lambd*(exp(x)-1.));
}

static double GIG_sampler_Devroy(double lambd, double omega,  RandomNumber& rng)
{
  double alpha=sqrt(omega*omega+lambd*lambd)-lambd;

  double psi0=psi(1.,alpha,lambd);
  double psi1=psi(-1.,alpha,lambd);

  double rho=4.;
  double t=sqrt(2.*rho/(alpha+lambd));
  rho=psi(t,alpha,lambd);

  double taux=t;
  taux=(-taux+(rho-psi(-taux,alpha,lambd))/psi_prime(-taux,alpha,lambd))*(-1.);
  taux=(-taux+(rho-psi(-taux,alpha,lambd))/psi_prime(-taux,alpha,lambd))*(-1.);
  taux=(-taux+(rho-psi(-taux,alpha,lambd))/psi_prime(-taux,alpha,lambd))*(-1.);
  taux=(-taux+(rho-psi(-taux,alpha,lambd))/psi_prime(-taux,alpha,lambd))*(-1.);
  double s=(-taux+(rho-psi(-taux,alpha,lambd))/psi_prime(-taux,alpha,lambd))*(-1.);

  double eta     = -psi(t,alpha,lambd);
  double theta   = -psi_prime(t,alpha,lambd);
  double phi     = -psi(-s,alpha,lambd);
  double xi      =  psi_prime(-s,alpha,lambd); 

  double p       =  1./xi;
  double r       =  1./theta;

  double t_prime =  t-r*eta;
  double s_prime =  s-p*phi;
  double q       =  t_prime+s_prime;

  double X=0.;
  double chi=0.;
  
  while(true)
    {
        double U=rng.uniform();
        double V=rng.uniform();
        double W=rng.uniform();
        
        if(U<q/(p+q+r))
          {
            X=-s_prime+q*V;
            chi=0.;
          }
        else if (U<(q+r)/(p+q+r))
          {
            X=t_prime+r*log(1./V);
            chi=(-eta-theta*(X-t));
          }
        else
          {
            X=-s_prime-p*log(1./V);
            chi=(-phi+xi*(X+s));
          }
        if (log(W)+chi <= (psi(X,alpha,lambd))) break;
    }
  return ((lambd/omega+sqrt(1.+lambd*lambd/omega/omega))*exp(X));
}

double LibLSS::GIG_sampler_3params(double a,double b,double p, RandomNumber& rng)
{
	///this routine provides samples of the three parameter Generalized Inverse Gaussian (GIG) distribution
	/// log(P)=-1./2.*(x*a+b*power(x,-1.)) + (p-1.)*log(x)
  
    double lambd=p;
    double omega=sqrt(b*a);

    //one only needs to draw for lambda>0 see Devroy 2014
    double X=0.;

    if(lambd>0.) 
      X=GIG_sampler_Devroy(lambd,omega,rng);
    else
      X=1./GIG_sampler_Devroy(-lambd,omega,rng);

    return sqrt(b/a)*X;
}
