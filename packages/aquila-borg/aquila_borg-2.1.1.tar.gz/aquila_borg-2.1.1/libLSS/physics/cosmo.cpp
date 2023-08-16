/*+
    ARES/HADES/BORG Package -- ./libLSS/physics/cosmo.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <gsl/gsl_const_num.h>
#include <gsl/gsl_const_mksa.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_odeiv.h>
#include <gsl/gsl_linalg.h>
#include <gsl/gsl_integration.h>
#include <cmath>
#include <CosmoTool/algo.hpp>
#include "cosmo.hpp"
#include "libLSS/tools/gsl_error.hpp"
#include "libLSS/tools/gslIntegrate.hpp"

using namespace LibLSS;
using namespace std;
using CosmoTool::spower;
using CosmoTool::square;

#define epsabs COSMO_EPS
#define epsrel COSMO_EPS

static const int NEVAL = 1000;
static const double cosmo_Ggrav = GSL_CONST_MKSA_GRAVITATIONAL_CONSTANT;
static const double cosmo_clight =
    GSL_CONST_MKSA_SPEED_OF_LIGHT; /* speed of light in m/s */
static const double cosmo_kB =
    GSL_CONST_MKSA_BOLTZMANN; /* Boltzmann constant  in m^2 * kg /s^2 /K */
static const double cosmo_parsec = GSL_CONST_MKSA_PARSEC; /* parsec in m */
static const double cosmo_kparsec = (1.0e3 * cosmo_parsec);
static const double cosmo_mparsec = (1.0e6 * cosmo_parsec);
static const double cosmo_gparsec = (1.0e9 * cosmo_parsec);
static const double cosmo_hubble =
    (1.0e5 / cosmo_mparsec); /* Hubble constant in 1/s */
static const double cosmo_mp =
    GSL_CONST_MKSA_MASS_PROTON; /* Mass of proton kg */

static const double cosmo_Mpc_cm = (1.0e2 * cosmo_mparsec);  // cm
static const double cosmo_Mpc_m = (1.0e0 * cosmo_mparsec);   // m
static const double cosmo_Mpc_km = (1.0e-3 * cosmo_mparsec); // km
static const double cosmo_H100_s = (100. / cosmo_Mpc_km);    // s^-1

static const double cosmo_M_sun = (1.98892e33); // g

static const double cosmo_G_const_Mpc_Msun_s =
    (cosmo_M_sun * (6.673e-8) / cosmo_Mpc_cm / cosmo_Mpc_cm /
     cosmo_Mpc_cm); // Mpc^3 msun^-1 s^-2

static const double AMIN = 1e-6;

static double x_plus(double a, const CosmologicalParameters &p);

/* --- function w [dark energy eos parameter - time evolution] --- */
static double w_Q(double a, const CosmologicalParameters &p) {
  return p.w + p.wprime * (1.0 - a);
}

/* --- function aux_q --- */
static double aux_q(double a, const CosmologicalParameters &p) {
  return 3.0 / 2.0 * (1.0 - w_Q(a, p) / (1.0 + x_plus(a, p))) / a;
}

/* --- function x_plus [auxiliary function, see Linder+Jenkins MNRAS 346, 573-583 (2003) for definition] --- */
static double x_plus(double a, const CosmologicalParameters &p) {
  double aux = 3 * p.wprime * (1 - a);
  return p.omega_m / (1 - p.omega_m) * pow(a, 3 * (p.w + p.wprime)) * exp(aux);
}

/* --- function dx_plus [derivative of x_plus, dx_plus(a) = d(x_plus(a))/da] --- */
double x_plus_prime(double a, const CosmologicalParameters &p) {
  return 3 * x_plus(a, p) * w_Q(a, p) / a;
}

/* --- function aux_r --- */
static double aux_r(double a, const CosmologicalParameters &p) {
  double aux = x_plus(a, p);
  return 3.0 / 2.0 * aux / (1.0 + aux) / spower<2, double>(a);
}

/* ---  --- */
static double aux_dr(double a, const CosmologicalParameters &p) {
  double ra;

  ra = aux_r(a, p);
  return x_plus_prime(a, p) / (1.0 + x_plus(a, p)) *
             (3.0 / 2.0 / spower<2, double>(a) - ra) -
         2.0 * ra / a;
}

/* ---  --- */
static double aux_dq(double a, const CosmologicalParameters &p) {
  double xp, result;

  xp = 1.0 + x_plus(a, p);
  result = -aux_q(a, p) / a;
  result -=
      3.0 / 2.0 / a / xp * (p.wprime - w_Q(a, p) * x_plus_prime(a, p) / xp);
  result /= a;

  return result;
}

/* --- function dplus_function - defines f0 = dy1/da and f1 = dy2/da --- */
static int d_plus_function(double t, const double y[], double f[], void *data) {
  CosmologicalParameters *params = (CosmologicalParameters *)data;

  /* derivatives f_i = dy_i/dt */
  f[0] = y[1];
  f[1] = aux_r(t, *params) * y[0] - aux_q(t, *params) * y[1];

  return (GSL_SUCCESS);
}

static int d_plus_jacobian(
    double t, const double y[], double *dfdy, double dfdt[], void *data) {
  gsl_matrix_view dfdy_mat = gsl_matrix_view_array(dfdy, 2, 2);
  gsl_matrix *m = &dfdy_mat.matrix;

  CosmologicalParameters *params = (CosmologicalParameters *)data;

  /* jacobian df_i(t,y(t)) / dy_j */
  gsl_matrix_set(m, 0, 0, 0.0);
  gsl_matrix_set(m, 0, 1, 1.0);
  gsl_matrix_set(m, 1, 0, 0.0);
  gsl_matrix_set(m, 1, 1, -aux_q(t, *params));

  /* gradient df_i/dt, explicit dependence */
  dfdt[0] = 0.0;
  dfdt[1] = aux_dr(t, *params) * y[0] - aux_dq(t, *params) * y[1];

  return GSL_SUCCESS;
}

static double hubble(double a, const CosmologicalParameters &p) {
  using CosmoTool::spower;
  double result;
  double aux;

  result = p.omega_r / spower<4, double>(a);
  result += p.omega_m / spower<3, double>(a);
  result += p.omega_k / spower<2, double>(a);

  aux = -(1 + p.w + p.wprime) * log(a) + p.wprime * (a - 1);
  result += p.omega_q * exp(3 * aux);

  return p.h * 100 * sqrt(result);
}

Cosmology::Cosmology(const CosmologicalParameters &p) : parameters(p) {
  // Do a check if the cosmological parameters sum up to 1
  Console::instance().print<LOG_DEBUG>(
      "Checking the normalization of cosmological parameters");
  double sum = 0;
  sum = p.omega_r + p.omega_m + p.omega_k + p.omega_q;
  if (sum != 1.0) {
    error_helper<ErrorBadState>("omega_r + omega_m + omega_k + omega_q != 1");
  }
  norm_d_plus = aux_d_plus(1.0);
}

double Cosmology::Hubble(double a) const { return hubble(a, parameters); }

void Cosmology::precompute_d_plus() {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  double result;
  int status;
  const gsl_odeiv_step_type *T = gsl_odeiv_step_bsimp;
  gsl_odeiv_step *s = gsl_odeiv_step_alloc(T, 2);
  gsl_odeiv_control *c = gsl_odeiv_control_y_new(0.0, epsrel);
  gsl_odeiv_evolve *e = gsl_odeiv_evolve_alloc(2);
  double t = AMIN,
         habs = 1e-4; /* t = initial scale factor, h = absolute accuracy */
  // TODO: Improve the initial condition
  // If matter dominated era used to anchor the solution
  // D(a) \propto a for a->0
  // Thus D'(a) = D(a)/a
  double y_prev[2],
      y[2] = {1.0, 1.0 / AMIN}; /* initial conditions, y(0) = 1.0, y'(0) = 0 */
  const double AMAX = 1.0;

  /* result from solution of a 2nd order differential equation, transformed to a system of 2 1st order deqs */
  gsl_odeiv_system sys = {
      d_plus_function, d_plus_jacobian, 2, (void *)&parameters};

  unsigned int NUM_D = 10000;

  const double log_a_min = std::log(AMIN);
  const double log_a_max = std::log(AMAX);
  const double delta_log_a = (log_a_max - log_a_min) / (NUM_D - 1);
  auto D_data = new boost::multi_array<double, 1>(boost::extents[NUM_D + 1]);
  auto Dprime_data =
      new boost::multi_array<double, 1>(boost::extents[NUM_D + 1]);
  unsigned int j = 0;

  auto get_a = [&](unsigned int k) {
    return std::exp(log_a_min + k * delta_log_a);
  };
  double a_current = get_a(0);

  (*D_data)[0] = std::log(y[0]);
  (*Dprime_data)[0] = std::log(y[1]);

  for (j = 1; j <= NUM_D; j++) {
    a_current = get_a(j);
    while (t < a_current) {
      status = gsl_odeiv_evolve_apply(e, c, s, &sys, &t, a_current, &habs, y);
      if (status != GSL_SUCCESS) {
        error_helper<ErrorBadState>("Error during ODE integration of Dplus");
      }
    }

    (*D_data)[j] = std::log(y[0]);
    (*Dprime_data)[j] = std::log(y[1]);
  }

  gsl_odeiv_evolve_free(e);
  gsl_odeiv_control_free(c);
  gsl_odeiv_step_free(s);

  pre_dplus = std::make_shared<auto_interpolator<double>>(
      log_a_min, log_a_max, delta_log_a, 0,
      std::numeric_limits<double>::infinity(), D_data);
  pre_dplus->setThrowOnOverflow();

  pre_dplus_prime = std::make_shared<auto_interpolator<double>>(
      log_a_min, log_a_max, delta_log_a, 0,
      std::numeric_limits<double>::infinity(), Dprime_data);
  pre_dplus_prime->setThrowOnOverflow();

  norm_d_plus = std::exp((*pre_dplus)(std::log(1.0)));
}

double Cosmology::aux_d_plus(double a, double *result_d_plus_prime) const {

  if (pre_dplus && pre_dplus_prime) {
    double result = std::exp((*pre_dplus)(std::log(a)));
    if (result_d_plus_prime != 0)
      *result_d_plus_prime = std::exp((*pre_dplus_prime)(std::log(a)));
    return result;
  }

  double result;
  int status;
  const gsl_odeiv_step_type *T = gsl_odeiv_step_bsimp;
  gsl_odeiv_step *s = gsl_odeiv_step_alloc(T, 2);
  gsl_odeiv_control *c = gsl_odeiv_control_y_new(0.0, epsrel);
  gsl_odeiv_evolve *e = gsl_odeiv_evolve_alloc(2);
  double t = AMIN,
         habs = 1e-4; /* t = initial scale factor, h = absolute accuracy */
  double y[2] = {
      1.0, 1.0 / AMIN}; /* initial conditions, dy1(0)/da = 1, dy2(0)/da=0 */

  /* result from solution of a 2nd order differential equation, transformed to a system of 2 1st order deqs */
  gsl_odeiv_system sys = {
      d_plus_function, d_plus_jacobian, 2, (void *)&parameters};

  while (t < a) {
    status = gsl_odeiv_evolve_apply(e, c, s, &sys, &t, a, &habs, y);
    if (status != GSL_SUCCESS)
      break;
  }

  gsl_odeiv_evolve_free(e);
  gsl_odeiv_control_free(c);
  gsl_odeiv_step_free(s);

  result = y[0]; /* d_plus */
  if (result_d_plus_prime)
    *result_d_plus_prime = y[1]; /* d(d_plus)/da */

  return result;
}

double Cosmology::dcom_dz(double z) const {
  double result;

  double a = 1. / (z + 1.);

  result = cosmo_clight / Hubble(a) / cosmo_mparsec;

  return (result);
}

double aux_dcom(double a, void *params) {
  double result;
  const CosmologicalParameters &p = *(const CosmologicalParameters *)params;

  result = -1. / square(a) / hubble(a, p);

  double clight = cosmo_clight / 1000.; ///km/s

  return (clight * result);
}

double Cosmology::a2com(double a) const {
  double result, error;
  gsl_integration_workspace *wspace = gsl_integration_workspace_alloc(NEVAL);
  gsl_function F;

  F.function = &aux_dcom;
  F.params = (void *)&parameters;
  gsl_integration_qag(
      &F, 1.0, a, epsabs, epsrel, NEVAL, GSL_INTEG_GAUSS61, wspace, &result,
      &error);

  gsl_integration_workspace_free(wspace);

  return (result);
}

void Cosmology::precompute_com2a() {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
  if (pre_com2a)
    return;

  const unsigned int NUM_A = 10000; // TODO: benchmark precision
  const double log_a_min = std::log(1e-4);
  const double delta_log_a = std::log(1.0 / 1e-4) / NUM_A;

  boost::multi_array<double, 1> log_d(boost::extents[NUM_A]);

#pragma omp parallel for
  for (unsigned int i = 0; i < NUM_A; i++) {
    const double a = std::exp(delta_log_a * i + log_a_min);

    log_d[i] = std::log(a2com(a));
  }

  const double log_d_min = log_d[NUM_A - 1];
  const double log_d_max = log_d[0];
  const double delta_log_d = (log_d_max - log_d_min) / NUM_A;

  auto log_a = new boost::multi_array<double, 1>(boost::extents[NUM_A]);
  double current_log_d = log_d_min;
  (*log_a)[0] = delta_log_a * (NUM_A - 1) + log_a_min;
  unsigned int j = NUM_A - 1;
  for (unsigned int i = 1; i < NUM_A; i++) {
    current_log_d += delta_log_d;
    while (current_log_d > log_d[j]) {
      if (j == 0) {
        ctx.print2<LOG_ERROR>("Bad reinterpolation state.");
        MPI_Communication::instance()->abort();
      }
      j--;
    }
    Console::instance().c_assert(
        j < NUM_A - 1, "Invalid state of the reinterpolation");
    const double w = (current_log_d - log_d[j]) / (log_d[j + 1] - log_d[j]);
    (*log_a)[i] = log_a_min + delta_log_a * ((1 - w) * j + (j + 1) * w);
  }

  pre_com2a = std::make_shared<auto_interpolator<double>>(
      log_d_min, log_d_max, delta_log_d, 0,
      std::numeric_limits<double>::infinity(), log_a);
  pre_com2a->setThrowOnOverflow();
}

double Cosmology::com2a(double com) const {
  if (pre_com2a) {
    return std::exp((*pre_com2a)(std::log(com)));
  }
  return bisection(
      A_MIN, A_MAX, 1e-6, com, [this](double a) { return a2com(a); });
}

double Cosmology::comph2a(double r) const {
  double result = com2a(comph2com(r));
  return (result);
}

double Cosmology::comph2d_plus(double r) const {
  double a = com2a(comph2com(r));
  double result = d_plus(a);
  return (result);
}

double Cosmology::comph2g_plus(double r) const {
  double a = com2a(comph2com(r));
  double result = g_plus(a);
  return (result);
}

double Cosmology::comph2Hubble(double r) const {
  double a = com2a(comph2com(r));
  double result = Hubble(a);
  return (result);
}

/* --- function aux_dtr [auxiliary function for dtr] --- */
double aux_dtr(double a, void *params) {
  double result;
  const CosmologicalParameters &p = *(const CosmologicalParameters *)params;

  ///Fhubble=H0/adot
  double H0 = 100.; ///km/s/Mpc

  double FHubble = (p.h * H0 / hubble(a, p) / (a * a * a));

  result = FHubble;

  return (result);
}
/* --- function pm_time-stepping dtr --- */
double Cosmology::dtr(double ai, double af) {
  double result, error;
  gsl_integration_workspace *wspace = gsl_integration_workspace_alloc(NEVAL);
  gsl_function F;

  F.function = &aux_dtr;
  F.params = (void *)&parameters;
  gsl_integration_qag(
      &F, ai, af, epsabs, epsrel, NEVAL, GSL_INTEG_GAUSS61, wspace, &result,
      &error);

  gsl_integration_workspace_free(wspace);

  return (result);
}
/* --- end of function dtv --- */
/* --- function aux_dtv [auxiliary function for dtv] --- */
double aux_dtv(double a, void *params) {
  double result;
  const CosmologicalParameters &p = *(const CosmologicalParameters *)params;

  ///Fhubble=H0/adot
  double H0 = 100.; ///km/s/Mpc

  double FHubble = (p.h * H0 / hubble(a, p) / a / a);

  result = FHubble;

  return (result);
}
/* --- function pm_time-stepping dtv --- */
double Cosmology::dtv(double ai, double af) {
  double result, error;
  gsl_integration_workspace *wspace = gsl_integration_workspace_alloc(NEVAL);
  gsl_function F;

  F.function = &aux_dtv;
  F.params = (void *)&parameters;
  gsl_integration_qag(
      &F, ai, af, epsabs, epsrel, NEVAL, GSL_INTEG_GAUSS61, wspace, &result,
      &error);

  gsl_integration_workspace_free(wspace);

  return (result);
}
/* --- end of function dtv --- */

/* --- COLA time stepping --- */
double Cosmology::integral_d_plus(double ai, double af) {
  return gslIntegrate(
      [this](double a) -> double {
        return aux_dtv(a, &parameters) * d_plus(a);
      },
      ai, af, epsrel, NEVAL);
}
/* --- end --- */

/* --- function critical density --- */
double Cosmology::rho_crit() {
  double rho_c = 3. * pow(parameters.h * cosmo_H100_s, 2.) /
                 (8. * M_PI * cosmo_G_const_Mpc_Msun_s); //units [Msun/Mpc^3]
  //calculates the critical density in units [Msun/(Mpc h^-1)^3]
  return rho_c / parameters.h / parameters.h / parameters.h;
}
/* --- end of function critical density --- */
/* --- function mass of volume --- */
double Cosmology::mass_of_volume(double V) {
  //returns the mean mass of a volume in units[Msun]
  return rho_crit() * parameters.omega_m * V;
}
/* --- end of function mass of volume --- */
