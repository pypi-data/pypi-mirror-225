/*+
    ARES/HADES/BORG Package -- ./libLSS/physics/class_cosmo.cpp
    Copyright (C) 2020 Jens Jasche <jens.jasche@fysik.su.se>
    Copyright (C) 2021 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include <fstream>
#include <locale.h>
#include <boost/algorithm/string/trim.hpp>
#include "libLSS/tools/console.hpp"
#include "class_cosmo.hpp"
#include <class_code/class.h>
#include "libLSS/tools/errors.hpp"
#include "libLSS/tools/string_tools.hpp"
#include "libLSS/tools/auto_interpolator.hpp"

using namespace LibLSS;
using namespace std;

namespace LibLSS {
  struct OpaqueClass {
    struct precision pr;  // for precision parameters
    struct background ba; // for cosmological background
    struct thermo th;     // for thermodynamics
    struct perturbs pt;   // for source functions
    struct transfers tr;  // for transfer functions
    struct primordial pm; // for primordial spectra
    struct spectra sp;    // for output spectra
    struct nonlinear nl;  // for non-linear spectra
    struct lensing le;    // for lensed spectra
    struct output op;     // for output files
    ErrorMsg errmsg;      // for error messages

    bool bg_init, th_init, pt_init, prim_init;

    OpaqueClass() {
      bg_init = false;
      th_init = false;
      pt_init = false;
      prim_init = false;
      ba.N_ncdm = 0;
    }

    ~OpaqueClass() {
      if (ba.N_ncdm > 0)
        delete[] ba.Omega0_ncdm;
      if (bg_init)
        background_free(&ba);
      if (th_init)
        thermodynamics_free(&th);
      if (pt_init)
        perturb_free(&pt);
      if (prim_init)
        primordial_free(&pm);
    }

    LibLSS::auto_interpolator<double> interpolate_mTk;
  };
} // namespace LibLSS

ClassCosmo::ClassCosmo(CosmologicalParameters const &cosmo) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  numInterpolationPoints = 1024;
  opaque = std::make_unique<OpaqueClass>();

  std::string previous_locale = std::string(setlocale(LC_NUMERIC, 0));
  // CLASS is not safe w.r.t Locale settings. It reads table with sscanf which
  // is sensitive to the locale setup.
  setlocale(LC_NUMERIC, "C");

  try {
    // Set all class values to default
    if (input_default_params(
            &opaque->ba, &opaque->th, &opaque->pt, &opaque->tr, &opaque->pm,
            &opaque->sp, &opaque->nl, &opaque->le, &opaque->op) == _FAILURE_) {
      ctx.format2<LOG_ERROR>(
          "Error running input_default_params => %s", opaque->op.error_message);
      error_helper<ErrorBadState>("Error in CLASS");
    }

    {
      auto &pba = opaque->ba;
      double
          sigma_B; /* Stefan-Boltzmann constant in \f$ W/m^2/K^4 = Kg/K^4/s^3 \f$*/

      sigma_B =
          2. * pow(_PI_, 5) * pow(_k_B_, 4) / 15. / pow(_h_P_, 3) / pow(_c_, 2);

      double omega_cdm = cosmo.omega_m - cosmo.omega_b;
      double Omega_tot = 0;

      pba.h = cosmo.h;
      pba.H0 = pba.h * 1.e5 / _c_;
      pba.Omega0_g = (4. * sigma_B / _c_ * pow(pba.T_cmb, 4.)) /
                     (3. * _c_ * _c_ * 1.e10 * pba.h * pba.h / _Mpc_over_m_ /
                      _Mpc_over_m_ / 8. / _PI_ / _G_);
      Omega_tot += pba.Omega0_g;
      pba.Omega0_ur = 3.046 * 7. / 8. * pow(4. / 11., 4. / 3.) * pba.Omega0_g;
      Omega_tot += pba.Omega0_ur;
      pba.Omega0_idr = 0.0;
      Omega_tot += pba.Omega0_idr;
      pba.Omega0_idm_dr = 0.0;
      pba.T_idr = 0.0;
      pba.Omega0_b = cosmo.omega_b;
      Omega_tot += pba.Omega0_b;
      pba.Omega0_cdm = omega_cdm;
      Omega_tot += pba.Omega0_cdm;

      {
        // CLP parametrization
        pba.fluid_equation_of_state = CLP;
        pba.w0_fld = cosmo.w;
        pba.wa_fld = cosmo.wprime;
        pba.Omega0_fld = cosmo.omega_q;
        Omega_tot += pba.Omega0_fld;
      }
      pba.Omega0_k = cosmo.omega_k;

      pba.N_ncdm = 1;
      pba.Omega0_ncdm = new double[1];

      pba.Omega0_ncdm[0] = cosmo.sum_mnu;

      opaque->pt.alpha_idm_dr = nullptr;
      opaque->pt.beta_idr = nullptr;

      pba.Omega0_lambda = 1 - pba.Omega0_k - Omega_tot;

      pba.K = -pba.Omega0_k * pow(pba.a_today * pba.H0, 2);
      /** - Set curvature sign */
      if (pba.K > 0.)
        pba.sgnK = 1;
      else if (pba.K < 0.)
        pba.sgnK = -1;
    }

    // Set all class precision values to default
    if (input_default_precision(&opaque->pr) == _FAILURE_) {
      ctx.format2<LOG_ERROR>(
          "Error running input_default_precision => %s",
          opaque->pr.error_message);
      error_helper<ErrorBadState>("Error in CLASS");
    }
    opaque->pr.k_per_decade_for_pk = 30;

    //initialize background calculations
    if (background_init(&opaque->pr, &opaque->ba) == _FAILURE_) {
      ctx.format2<LOG_ERROR>(
          "Error running background_init => %s", opaque->ba.error_message);
      error_helper<ErrorBadState>("Error in CLASS");
    }
    opaque->bg_init = true;

    //opaque->th.thermodynamics_verbose = _TRUE_;
    if (thermodynamics_init(&opaque->pr, &opaque->ba, &opaque->th) ==
        _FAILURE_) {
      ctx.format2<LOG_ERROR>(
          "Error running thermodynamics_init => %s", opaque->th.error_message);
      error_helper<ErrorBadState>("Error in CLASS");
    }
    opaque->th_init = true;

    opaque->pt.has_perturbations = _TRUE_;
    //opaque->pt.perturbations_verbose = 1;
    opaque->pt.has_pk_matter = _TRUE_;
    opaque->pt.has_density_transfers = _TRUE_;
    opaque->pt.has_cls = _FALSE_;
    //opaque->pt.k_max_for_pk = ;

    if (perturb_init(&opaque->pr, &opaque->ba, &opaque->th, &opaque->pt) ==
        _FAILURE_) {
      ctx.format2<LOG_ERROR>(
          "Error running perturb_init => %s", opaque->pt.error_message);
      error_helper<ErrorBadState>("Error in CLASS");
    }
    opaque->pt_init = true;

    if (primordial_init(&opaque->pr, &opaque->pt, &opaque->pm) == _FAILURE_) {
      ctx.format2<LOG_ERROR>(
          "Error running primordial_init => %s", opaque->pm.error_message);
      error_helper<ErrorBadState>("Error in CLASS");
    }
    opaque->prim_init = true;

    retrieve_Tk();
  } catch (std::exception &e) {
    setlocale(LC_NUMERIC, previous_locale.c_str());
    throw;
  }
  setlocale(LC_NUMERIC, previous_locale.c_str());
}

double ClassCosmo::primordial_Pk(double k) {
  //Input: wavenumber k in 1/Mpc (linear mode)
  //Output: primordial spectra P(k) in \f$Mpc^3\f$ (linear mode)

  double output;

  primordial_spectrum_at_k(
      &opaque->pm,
      0, //choose scalar mode
      linear, k, &output);

  return output;
}

double ClassCosmo::get_Tk(double k) {
  return -std::exp(opaque->interpolate_mTk(std::log(k)));
}

void ClassCosmo::retrieve_Tk() {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  char *c_titles;
  std::string titles;
  double const output_redshift = 0;

  // Query the available columns
  c_titles = new char[_MAXTITLESTRINGLENGTH_];
  std::fill(c_titles, c_titles + _MAXTITLESTRINGLENGTH_, 0);
  if (perturb_output_titles(&opaque->ba, &opaque->pt, class_format, c_titles) ==
      _FAILURE_) {
    delete[] c_titles;
    ctx.format2<LOG_ERROR>(
        "Error running perturb_output_titles => %s", opaque->pt.error_message);
    error_helper<ErrorBadState>("Error in CLASS");
  }
  titles = c_titles;
  delete[] c_titles;

  // Retrieve relevant data
  auto names = LibLSS::tokenize(boost::algorithm::trim_copy(titles), "\t");
  ctx.print(LibLSS::to_string(names));
  auto index_md = opaque->pt.index_md_scalars;
  auto number_of_titles = names.size();
  auto number_of_ic = opaque->pt.ic_size[index_md];
  auto timesteps = opaque->pt.k_size[index_md];
  auto size_ic_data = timesteps * number_of_titles;
  auto ic_num = opaque->pt.ic_size[index_md];

  auto data = new double[size_ic_data * ic_num];

  if (perturb_output_data(
          &opaque->ba, &opaque->pt, class_format, output_redshift,
          number_of_titles, data) == _FAILURE_) {
    delete[] data;
    ctx.format2<LOG_ERROR>(
        "Error running perturb_output_data => %s", opaque->pt.error_message);
    error_helper<ErrorBadState>("Error in CLASS");
  }

  // Adiabatic mode is referenced at opaque->pt.index_ic_ad
  auto index_ic = opaque->pt.index_ic_ad;
  auto result_k = std::find(names.begin(), names.end(), "k (h/Mpc)");
  Console::instance().c_assert(
      result_k != names.end(), "Invalid returned arrays for k from CLASS");
  auto k_title = std::distance(names.begin(), result_k);
  auto result = std::find(names.begin(), names.end(), "d_tot");
  Console::instance().c_assert(
      result != names.end(), "Invalid returned arrays from CLASS");
  auto mTk_title = std::distance(names.begin(), result);

  ctx.format("k_title=%d, mTk_title=%d", k_title, mTk_title);

  auto get_data = [&](size_t step, size_t title) {
    return data[index_ic * size_ic_data + step * number_of_titles + title];
  };

  array_1d k, Tk;

  k.resize(boost::extents[timesteps]);
  Tk.resize(boost::extents[timesteps]);

  for (size_t step = 0; step < timesteps; step++) {
    Tk[step] = -get_data(
        step, mTk_title); // Laplacian between density and potential is negative
    k[step] = get_data(step, k_title);
  }

  reinterpolate(k, Tk);

  delete[] data;
}

ClassCosmo::~ClassCosmo() {}

void ClassCosmo::reinterpolate(array_ref_1d const &k, array_ref_1d const &Tk) {
  LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

  double k_min = opaque->pt.k_min / opaque->ba.h;
  double k_max = opaque->pt.k_max / opaque->ba.h;

  double delta_ln_k = std::log(k_max / k_min) / (numInterpolationPoints + 1);
  double log_k_min = std::log(k_min);
  double log_k_max = std::log(k_max);
  size_t i_in_k = 0;

  auto newTk =
      new boost::multi_array<double, 1>(boost::extents[numInterpolationPoints]);

  ctx.format(
      "numInterpolationPoints = %d, k.size() = %d, k_min=%g, k_max=%g",
      numInterpolationPoints, k.size(), k_min, k_max);
  for (size_t i = 0; i < numInterpolationPoints; i++) {
    double target_k = std::exp(delta_ln_k * i + log_k_min);
    while (k[i_in_k] < target_k && i_in_k < k.size()) {
      i_in_k++;
    }

    Console::instance().c_assert(i_in_k < k.size(), "Bad reinterpolation");
    if (i_in_k == 0 && k[i_in_k] == k_min) {
      (*newTk)[i] = std::log(Tk[0]);
    } else if (k[i_in_k - 1] == 0) {
      (*newTk)[i] =
          std::log(Tk[i_in_k]) / std::log(k[i_in_k]) * std::log(target_k);
    } else {
      double alpha = std::log(target_k / k[i_in_k - 1]) /
                     std::log(k[i_in_k] / k[i_in_k - 1]);
      Console::instance().c_assert(
          alpha > 0 && alpha < 1, "Bad alpha for interpolation");
      (*newTk)[i] =
          std::log(Tk[i_in_k - 1]) * (1 - alpha) + std::log(Tk[i_in_k]) * alpha;
    }
  }

  opaque->interpolate_mTk = LibLSS::auto_interpolator<double>(
      log_k_min, log_k_max, delta_ln_k, std::log(Tk[0]), 0.0, newTk);
  opaque->interpolate_mTk.setThrowOnOverflow();
}

void ClassCosmo::updateCosmo() {
  //ba.h = 0.67556;
  auto &ba = opaque->ba;
  auto &pba = opaque->ba;

  ba.H0 = pba.h * 1.e5 / _c_;
  ba.T_cmb = 2.7255;
  ba.Omega0_b = 0.022032 / pow(pba.h, 2);
  ba.Omega0_cdm = 0.12038 / pow(pba.h, 2);
  ba.Omega0_dcdmdr = 0.0;
  ba.Omega0_dcdm = 0.0;
  ba.Gamma_dcdm = 0.0;
  ba.N_ncdm = 0;
  ba.Omega0_ncdm_tot = 0.;
  ba.ksi_ncdm_default = 0.;
  ba.ksi_ncdm = NULL;

  ba.Omega0_scf = 0.; // Scalar field defaults
  ba.attractor_ic_scf = _TRUE_;
  ba.scf_parameters = NULL;
  ba.scf_parameters_size = 0;
  ba.scf_tuning_index = 0;

  ba.Omega0_k = 0.;
  ba.K = 0.;
  ba.sgnK = 0;
  ba.Omega0_lambda = 1. - pba.Omega0_k - pba.Omega0_g - pba.Omega0_ur -
                     pba.Omega0_b - pba.Omega0_cdm - pba.Omega0_ncdm_tot -
                     pba.Omega0_dcdmdr - pba.Omega0_idm_dr - pba.Omega0_idr;
  ba.Omega0_fld = 0.;
  ba.w0_fld = -1.;
  ba.wa_fld = 0.;
  ba.Omega_EDE = 0.;
  ba.cs2_fld = 1.;

  ba.shooting_failed = _FALSE_;
}

ClassCosmo::DictCosmology ClassCosmo::getCosmology() {

  DictCosmology state;

  state["Omega_g"] = opaque->ba.Omega0_g;
  state["Omega_m"] = opaque->ba.Omega0_m;
  state["N_ncdm"] = opaque->ba.N_ncdm;
  state[lssfmt::format("Omega0_ncdm_%d", 0)] = opaque->ba.Omega0_ncdm[0];
  state["Omega_k"] = opaque->ba.Omega0_k;
  state["Omega_lambda"] = opaque->ba.Omega0_lambda;
  state["Omega_m"] = opaque->ba.Omega0_m;

  return state;
}

void ClassCosmo::setInterpolation(size_t numPoints) {
  numInterpolationPoints = numPoints;
}

// ARES TAG: num_authors = 2
// ARES TAG: name(0) = Jens Jasche
// ARES TAG: email(0) = jens.jasche@fysik.su.se
// ARES TAG: year(0) = 2020
// ARES TAG: name(1) = Guilhem Lavaux
// ARES TAG: email(1) = guilhem.lavaux@iap.fr
// ARES TAG: year(1) = 2021
