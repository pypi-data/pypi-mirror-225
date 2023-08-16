/*+
    ARES/HADES/BORG Package -- ./libLSS/physics/cosmo.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_COSMO_HPP
#define __LIBLSS_COSMO_HPP

#include <string>
#include <functional>
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/tools/bisection.hpp"
#include "libLSS/tools/auto_interpolator.hpp"

namespace LibLSS {

  struct CosmologicalParameters {

    double omega_r; /* negligible radiation density */
    double omega_k; /* curvature - flat prior for everything! */
    double omega_m;
    double omega_b;
    double omega_q;
    double w;
    double n_s;
    double fnl; /* non-linearity parameter, for primordial non-Gaussianity */
    double wprime;
    double sigma8;
    double rsmooth;
    double h;
    double beta;
    double z0;
    double a0;      /* scale factor at epoch of observation usually 1*/
    double sum_mnu; /* sum of neutrino masses */

    CosmologicalParameters()
        : omega_r(0), omega_k(0), omega_m(0), omega_b(0), omega_q(0), w(0),
          n_s(0), fnl(0), wprime(0), sigma8(0), h(0), beta(0), z0(0), a0(0),
          sum_mnu(0) {}

    bool operator==(CosmologicalParameters const &p2) const {
      return omega_r == p2.omega_r && omega_k == p2.omega_k &&
             omega_m == p2.omega_m && omega_b == p2.omega_b &&
             omega_q == p2.omega_q && w == p2.w && n_s == p2.n_s &&
             wprime == p2.wprime && sigma8 == p2.sigma8 && h == p2.h &&
             sum_mnu == p2.sum_mnu;
    }
    bool operator!=(CosmologicalParameters const &p2) const {
      return !operator==(p2);
    }
  };

  static const double A_MIN = 0.;
  static const double A_MAX = 30000.;
  static const double COSMO_EPS = 1e-6;

#define LIBLSS_COSMOLOGY_INVERSE_FUNCTION(                                     \
    TARGET, ORIGINAL, RANGE_MIN, RANGE_MAX)                                    \
  double TARGET(double X) const {                                              \
    return bisection(                                                          \
        RANGE_MIN, RANGE_MAX, 1e-6, X,                                         \
        std::bind(&Cosmology::ORIGINAL, this, std::placeholders::_1));         \
  }

  class Cosmology {
  private:
    CosmologicalParameters parameters;
    double A_spec; /* Normalization of the power spectrum */
    int spec_type; /* indicates which power spectrum is currently used, and whether the normalization has to be reevaluated*/
    double norm_d_plus;
    double aux_d_plus(double a, double *result_d_plus_prime = 0) const;

    std::shared_ptr<auto_interpolator<double>> pre_com2a, pre_dplus,
        pre_dplus_prime;

  public:
    Cosmology(const CosmologicalParameters &parameters);

    void precompute_com2a();
    void precompute_d_plus();

    CosmologicalParameters const &getParameters() const { return parameters; }

    double a2z(double a) const { return 1 / a - 1; }
    double z2a(double z) const { return 1 / (1 + z); }
    double d_plus(double a) const { return aux_d_plus(a) / norm_d_plus; }

    double d2dlum(double z, double d) const { return (1 + z) * d; }

    double dlum2d(double z, double dlum) const { return dlum / (1 + z); }

    double g_plus(double a) const {
      double d_plus, d_plus_prime;

      d_plus = aux_d_plus(a, &d_plus_prime);
      return (a > COSMO_EPS) ? (a / d_plus * d_plus_prime) : 1.0;
    }

    double a2com(double a) const;
    double com2a(double com) const;

    double z2com(double z) const {
      double a = z2a(z);
      double dcom = a2com(a);
      return dcom;
    };

    double dcom_dz(double z) const;

    double com2comph(double r) const { return parameters.h * r; }
    double comph2com(double r) const { return r / parameters.h; }

    double comph2d_plus(double r) const;
    double comph2g_plus(double r) const;
    double comph2Hubble(double r) const;
    double comph2a(double r) const;

    double a2dlum(double a) const {
      double z = a2z(a);
      double dcom = a2com(a);
      return (1 + z) * dcom;
    };

    double z2dlum(double z) const {
      double a = z2a(z);
      double dcom = a2com(a);
      return (1 + z) * dcom;
    };

    LIBLSS_COSMOLOGY_INVERSE_FUNCTION(dlum2a, a2dlum, A_MIN, A_MAX);

    double a2dA(double a) const {
      double z = a2z(a);
      double dcom = a2com(a);
      return dcom / (1 + z);
    };

    double z2dA(double z) const {
      double a = z2a(z);
      double dcom = a2com(a);
      return dcom / (1 + z);
    };

    //a2dA not invertible over full redhsiftrange
    LIBLSS_COSMOLOGY_INVERSE_FUNCTION(dA2a, a2dA, 0.5, A_MAX);

    double Hubble(double a) const;
    double hNow() const { return parameters.h; }
    double k_J(double a);
    double kF_baryon(double a);
    double kSZ_kernel(double a);
    void print_cdmspec2file(std::string outputFileName);
    double power_spectrum(double k, int type);
    double transfer_function(double k);
    double power_spectrum_grav(double k, int type);
    double rho_background_matter(double a);
    double gravpot_norm();
    double return_cosmo_par(std::string cosmopar);
    double FHubble(double a) { return (parameters.h * 100 / (a * Hubble(a))); }
    double dtr(double ai, double af);
    double dtv(double ai, double af);
    double integral_d_plus(double ai, double af);
    double rho_crit();
    double mass_of_volume(double V);
  };

#undef LIBLSS_COSMOLOGY_INVERSE_FUNCTION

} // namespace LibLSS

// clang-format off
CTOOL_STRUCT_TYPE(LibLSS::CosmologicalParameters,
                  HDF5T_CosmologicalParameters,
    ((double, omega_r))
    ((double, omega_k))
    ((double, omega_m))
    ((double, omega_b))
    ((double, omega_q))
    ((double, w))
    ((double, n_s))
    ((double, fnl))
    ((double, wprime))
    ((double, sigma8))
    ((double, rsmooth))
    ((double, h))
    ((double, beta))
    ((double, z0))
    ((double, a0))
);
// clang-format on

#endif
