/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/tools/symplectic_integrator.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_SYMPLECTIC_INTEGRATOR_HPP
#define __LIBLSS_SYMPLECTIC_INTEGRATOR_HPP

#include <boost/multi_array.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/tools/fused_array.hpp"
#include "libLSS/tools/fusewrapper.hpp"

namespace LibLSS {

  namespace SymplecticOption {
    enum IntegratorScheme {
      SI_2A,
      SI_2B,
      SI_2C,
      SI_3A,
      SI_4B,
      SI_4C,
      SI_4D,
      SI_6A,
      CG_89
    };

    typedef boost::multi_array<double, 2> IntegratorCoefficients;

    template <int N>
    static inline void
    pushScheme(double coefs[2][N], IntegratorCoefficients &I_coefs) {
      int Ncoefs = N;

      I_coefs.resize(boost::extents[2][Ncoefs]);
      for (int i = 0; i < Ncoefs; i++) {
        I_coefs[0][i] = coefs[0][i];
        I_coefs[1][i] = coefs[1][i];
      }
    }

  }; // namespace SymplecticOption

  struct SymplecticIntegrators {
    typedef SymplecticOption::IntegratorCoefficients IntegratorCoefficients;
    typedef SymplecticOption::IntegratorScheme IntegratorScheme;
    IntegratorCoefficients I_coefs;

    SymplecticIntegrators() { setIntegratorScheme(SymplecticOption::SI_2A); }

    void setIntegratorScheme(IntegratorScheme scheme) {
      using namespace SymplecticOption;

      switch (scheme) {
      case SI_2A: {
        //si2a : standard leapfrog
        double coefs[2][2] = {{0.5, 0.5}, {0.0, 1.0}};
        pushScheme<2>(coefs, I_coefs);
        break;
      }
      case SI_2B: {
        //si2b : pseudo leapfrog
        double coefs[2][2] = {{1.0, 0.0}, {0.5, 0.5}};
        pushScheme<2>(coefs, I_coefs);
        break;
      }
      case SI_2C: {
        //si2c : optimal 2-stage
        double coefs[2][2] = {{1.0 / sqrt(2.), 1.0 - 1.0 / sqrt(2.0)},
                              {1.0 - 1.0 / sqrt(2.0), 1.0 / sqrt(2.0)}};
        pushScheme<2>(coefs, I_coefs);
        break;
      }
      case SI_3A: {
        //si3a : Ruth's third order method
        double coefs[2][3] = {{2.0 / 3.0, -2.0 / 3.0, 1.0},
                              {7.0 / 24.0, 0.75, -1.0 / 24.0}};
        pushScheme<3>(coefs, I_coefs);
        break;
      }
      case SI_4B: {
        //si4b : Calvo and Sanz-Serna's fourth order method
        double coeffs[2][4] = {{0.515352837431122936, -0.085782019412973646,
                                0.441583023616466524, 0.128846158365384185},
                               {0.134496199277431089, -0.224819803079420806,
                                0.756320000515668291, 0.334003603286321425}};
        pushScheme<4>(coeffs, I_coefs);
        break;
      }
      case SI_4C: {
        //si4c : McLachlan and Atela's optimal third order method
        double coeffs[2][5] = {{0.205177661542290, 0.403021281604210,
                                -0.12092087633891, 0.512721933192410, 0.0},
                               {0.061758858135626, 0.33897802655364,
                                0.61479130717558, -0.14054801465937,
                                0.12501982279453}};

        pushScheme<5>(coeffs, I_coefs);
        break;
      }
      case SI_4D: {
        //si4d : McLachlan and Atela's optimal third order method
        double caux = pow(2., 1. / 3.);
        double coeffs[2][4] = {
            {0.5 / (2. - caux), 0.5 * (1.0 - caux) / (2. - caux),
             0.5 * (1.0 - caux) / (2. - caux), 0.5 / (2. - caux)},
            {0.0, 1.0 / (2. - caux), -caux / (2. - caux), 1.0 / (2. - caux)}};

        pushScheme<4>(coeffs, I_coefs);
        break;
      }
      case SI_6A: {
        //si6a : Yoshida's sixth-order method
        double caux = pow(2., 1. / 3.);
        double coeffs[2][8] = {
            {0.78451361047756, 0.23557321335936, -1.1776799841789,
             1.3151863206839, 0., 0., 0., 0.},
            {0.39225680523878, 0.51004341191846, -0.47105338540976,
             0.068753168252520, 0., 0., 0., 0.}};
        coeffs[0][4] = coeffs[0][2];
        coeffs[0][5] = coeffs[0][1];
        coeffs[0][6] = coeffs[0][0];

        coeffs[1][4] = coeffs[1][3];
        coeffs[1][5] = coeffs[1][2];
        coeffs[1][6] = coeffs[1][1];
        coeffs[1][7] = coeffs[1][0];

        pushScheme<8>(coeffs, I_coefs);
        break;
      }
      case CG_89: {
        constexpr int const i = 4;
        constexpr double const n = 2.;
        double s = std::pow(2*i, 1/(n+1.));
        double coeffs[2][4*i+2];
        for (int j = 0; j < i; j++) {
          coeffs[0][2*j] = 0.5;
          coeffs[0][2*j+1] = 0.5;
          coeffs[1][2*j] = 0.;
          coeffs[1][2*j+1] = 1.;
        }
        coeffs[0][2*i] = -0.5*s;
        coeffs[0][2*i+1] = -0.5*s;
        coeffs[1][2*i] = 0;
        coeffs[1][2*i+1] = -s;
        int const base = 2*i+2;
        for (int j = 0; j < i; j++) {
          coeffs[0][base+2*j] = 0.5;
          coeffs[0][base+2*j+1] = 0.5;
          coeffs[1][base+2*j] = 0.;
          coeffs[1][base+2*j+1] = 1.;
        }
        pushScheme<4*i+2>(coeffs, I_coefs);
        break;
      }
      default:
        error_helper<ErrorBadState>("Unknown integration scheme");
        break;
      }
    }

    template <
        typename MassMatrix, typename GradientVector, typename MomentumVector,
        typename PositionVector, typename GradientFunction>
    void integrate_dense(
        const GradientFunction &gradient, MassMatrix &&masses, double epsilon,
        int Ntime, PositionVector &position, MomentumVector &momentum,
        GradientVector &tmp_gradient) {

      using boost::lambda::_1;
      using boost::lambda::_2;
      using boost::lambda::_3;
      Console &cons = Console::instance();
      Progress<LOG_INFO_SINGLE> &progress =
          cons.start_progress<LOG_INFO_SINGLE>(
              "doing Symplectic integration", Ntime, 10);

      int Ncoefs = I_coefs.shape()[1];
      for (int i_Time = 0; i_Time < Ntime; i_Time++) {

        ///the scheme depends on the chosen integrator order
        for (int n = 0; n < Ncoefs; n++) {
          double an = I_coefs[0][n] * epsilon;
          double bn = I_coefs[1][n] * epsilon;

          if (bn != 0) {
            gradient(position, tmp_gradient);
            // This is momentum update
            fwrap(momentum) = fwrap(momentum) - fwrap(tmp_gradient) * bn;
          }
          // This is position update
          fwrap(position) = fwrap(position) + masses(momentum, tmp_gradient) * an;
        }
        progress.update(i_Time);
      }

      progress.destroy();
    }

    template <
        typename MassMatrix, typename GradientVector, typename MomentumVector,
        typename PositionVector, typename GradientFunction>
    void integrate(
        const GradientFunction &gradient, MassMatrix &&masses, double epsilon,
        int Ntime, PositionVector &position, MomentumVector &momentum,
        GradientVector &tmp_gradient) {
      auto mass_op = [&masses](MomentumVector const &m, auto&) {
        return fwrap(m) * fwrap(masses);
      };
      integrate_dense(
          gradient, mass_op, epsilon, Ntime, position, momentum, tmp_gradient);
    }
  };

}; // namespace LibLSS

#endif
