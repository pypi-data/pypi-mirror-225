/*+
    ARES/HADES/BORG Package -- ./libLSS/data/schechter_completeness.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_SCHECHTER_COMPLETENESS_HPP
#define __LIBLSS_SCHECHTER_COMPLETENESS_HPP

#include <cmath>
#include <functional>
#include <boost/format.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/tools/gslIntegrate.hpp"
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/data/spectro_gals.hpp"
#include "libLSS/data/galaxies.hpp"
#include "libLSS/data/projection.hpp"

namespace LibLSS {

  typedef std::function<bool(const BaseGalaxyDescriptor &)> GalaxySelector;

  struct GalaxySampleSelection {
    double bright_apparent_magnitude_cut;
    double faint_apparent_magnitude_cut;
    double bright_absolute_magnitude_cut;
    double faint_absolute_magnitude_cut;

    double zmin, zmax;
    double dmin, dmax;

    double low_mass_cut;
    double high_mass_cut;
    double small_radius_cut;
    double large_radius_cut;
    double low_spin_cut;
    double high_spin_cut;

    // This is required to satisfy C++ object layout
    // Otherwise the struct GalaxySampleSelection is not "trivial".
    std::shared_ptr<GalaxySelector> selector;
    ProjectionDataModel projection;
  };

  static inline std::shared_ptr<GalaxySelector> makeSelector(GalaxySelector f) {
    return std::make_shared<GalaxySelector>(f);
  }

  struct SchechterParameters {
    double Mstar, alpha;
  };

  namespace details {

    static inline double
    _integrand_luminosity(const SchechterParameters &params, double x) {
      return std::pow(x, params.alpha) * exp(-x);
    }

    static inline double integral_luminosity(
        const SchechterParameters &params, double x_min, double x_max) {
      return gslIntegrate(
          std::bind(_integrand_luminosity, params, std::placeholders::_1),
          x_min, x_max, 1e-8);
    }

    static inline double computeSchechterCompleteness(
        const Cosmology &cosmo, double z, double d_comoving,
        const GalaxySampleSelection &selection,
        const SchechterParameters &params,
        CorrectionFunction zcorrection = nullCorrection) {
      using boost::format;
      ConsoleContext<LOG_DEBUG> ctx("computeSchechterCompleteness");

      double d_lum = cosmo.d2dlum(z, d_comoving);
      double corr = zcorrection(z);

      double absolute_mu0 = selection.faint_apparent_magnitude_cut -
                            5 * std::log10(d_lum) - 25 - corr;
      double absolute_ml0 = selection.bright_apparent_magnitude_cut -
                            5 * std::log10(d_lum) - 25 - corr;

      double abmu =
          std::min(absolute_mu0, selection.faint_absolute_magnitude_cut);
      double abml =
          std::max(absolute_ml0, selection.bright_absolute_magnitude_cut);

      ctx.print(
          format("z = %lg d_lum = %lg abmu = %lg abml = %lg") % z % d_lum %
          abmu % abml);

      abmu = std::max(abmu, abml);

      double xl0 = std::pow(10.0, 0.4 * (params.Mstar - abmu));
      double xu0 = std::pow(10.0, 0.4 * (params.Mstar - abml));

      double xl1 = std::pow(
          10.0, 0.4 * (params.Mstar - selection.faint_absolute_magnitude_cut));
      double xu1 = std::pow(
          10.0, 0.4 * (params.Mstar - selection.bright_absolute_magnitude_cut));

      ctx.print(
          format("xl0 = %lg, xu0 = %lg, xl1 = %lg, xu1 = %lg") % xl0 % xu0 %
          xl1 % xu1);

      double Phi0 = integral_luminosity(params, xl0, xu0);
      double Phi1 = integral_luminosity(params, xl1, xu1);

      return std::max(0.0, Phi0 / Phi1);
    }

  } // namespace details

  template <typename Array>
  void buildCompletenessFromSchechterFunction(
      const Cosmology &cosmo, const GalaxySampleSelection &selection,
      const SchechterParameters &params, Array &completeness, double Dmax,
      CorrectionFunction zcorr = details::nullCorrection) {

    ConsoleContext<LOG_DEBUG> ctx("buildCompletenessFromSchechterFunction");
    long N = completeness.num_elements();
    for (long i = 1; i < N; i++) {
      double d = i * Dmax / N;
      double z = cosmo.a2z(cosmo.com2a(cosmo.comph2com(d)));

      if (z < selection.zmin || z > selection.zmax)
        completeness[i] = 0;
      else
        completeness[i] = details::computeSchechterCompleteness(
            cosmo, z, d, selection, params, zcorr);
      //ctx.print(boost::format("d = %lg, z = %lg, C = %lg") % d % z % completeness[i]);
    }
    // zero distance is hard, just copy the one next to it. If sampling is sufficient that will not matter.
    completeness[0] = completeness[1];
  }

} // namespace LibLSS

CTOOL_STRUCT_TYPE(
    LibLSS::GalaxySampleSelection, HDF5T_GalaxySampleSelection,
    ((double,
      bright_apparent_magnitude_cut))((double, faint_apparent_magnitude_cut))(
        (double, bright_absolute_magnitude_cut))(
        (double, faint_absolute_magnitude_cut))((double, zmin))((double, zmax))(
        (double, dmin))((double, dmax))((double, low_mass_cut))(
        (double, high_mass_cut))((double, small_radius_cut))(
        (double, large_radius_cut))((double, low_spin_cut))(
        (double, high_spin_cut))((LibLSS::ProjectionDataModel, projection)));

CTOOL_STRUCT_TYPE(
    LibLSS::SchechterParameters, HDF5T_SchechterParameters,
    ((double, Mstar))((double, alpha)));

#endif
