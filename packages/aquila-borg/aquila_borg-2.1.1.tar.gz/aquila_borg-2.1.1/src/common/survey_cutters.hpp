/*+
    ARES/HADES/BORG Package -- ./src/common/survey_cutters.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __SURVEY_CUTTERS_HPP
#define __SURVEY_CUTTERS_HPP

#include <cmath>

namespace LibLSS {

  template <typename GalaxySurvey>
  class MagnitudeCutter {
  public:
    GalaxySampleSelection selection;
    GalaxySurvey *g_el;

    MagnitudeCutter(GalaxySampleSelection sel, GalaxySurvey *e)
        : selection(sel), g_el(e) {}

    virtual bool operator()(const BaseGalaxyDescriptor &g) const {
      double f = g_el->getCompleteness(g.phi, g.theta);

      bool flag = (f > 0.) && (g.m > selection.bright_apparent_magnitude_cut) &&
                  (g.m <= selection.faint_apparent_magnitude_cut) &&
                  (g.M_abs > selection.bright_absolute_magnitude_cut) &&
                  (g.M_abs <= selection.faint_absolute_magnitude_cut) &&
                  (g.z > 0);
      return flag;
    }
  };

  template <typename GalaxySurvey>
  class RedshiftMagnitudeCutter {
  public:
    GalaxySampleSelection selection;
    GalaxySurvey *g_el;

    RedshiftMagnitudeCutter(GalaxySampleSelection sel, GalaxySurvey *e)
        : selection(sel), g_el(e) {}

    bool operator()(const BaseGalaxyDescriptor &g) const {
      double f = g_el->getCompleteness(g.phi, g.theta);
      return (f > 0.) && (g.z >= selection.zmin) && (g.z < selection.zmax) &&
             (g.m > selection.bright_apparent_magnitude_cut) &&
             (g.m <= selection.faint_apparent_magnitude_cut) &&
             (g.M_abs > selection.bright_absolute_magnitude_cut) &&
             (g.M_abs <= selection.faint_absolute_magnitude_cut);
    }
  };

  template <typename GalaxySurvey>
  class DistanceCutter {
  public:
    GalaxySurvey *g_el;
    GalaxySampleSelection selection;

    DistanceCutter(GalaxySampleSelection sel, GalaxySurvey *e)
        : selection(sel), g_el(e) {}

    bool operator()(const BaseGalaxyDescriptor &g) const {
      return (g.r >= selection.dmin) && (g.r <= selection.dmax);
    }
  };

  template <typename DMSimulation>
  class MixedCutter {
  private:
    typedef std::function<bool(const BaseGalaxyDescriptor &)> Functor;
    std::list<Functor> cutter_list;

  public:
    MixedCutter() {}

    void addCutter(Functor f) { cutter_list.push_back(f); }

    bool operator()(const BaseGalaxyDescriptor &g) const {
      for (auto &c : cutter_list) {
        if (!c(g))
          return false;
      }
      return true;
    }
  };

  template <typename DMSimulation>
  class NoneCutter {
  public:
    GalaxySampleSelection selection;
    DMSimulation *h_el;

    NoneCutter(GalaxySampleSelection sel, DMSimulation *e)
        : selection(sel), h_el(e) {}

    virtual bool operator()(const BaseGalaxyDescriptor &h) const {
      return true;
    }
  };

  template <typename DMSimulation>
  class MassCutter {
  public:
    GalaxySampleSelection selection;
    DMSimulation *h_el;

    MassCutter(GalaxySampleSelection sel, DMSimulation *e)
        : selection(sel), h_el(e) {}

    virtual bool operator()(const BaseGalaxyDescriptor &h) const {
      bool massCut = (std::log10(h.Mgal) >= selection.low_mass_cut) &&
                     (std::log10(h.Mgal) < selection.high_mass_cut);
      return massCut;
    }
  };

  template <typename DMSimulation>
  class RadiusCutter {
  public:
    GalaxySampleSelection selection;
    DMSimulation *h_el;

    RadiusCutter(GalaxySampleSelection sel, DMSimulation *e)
        : selection(sel), h_el(e) {}

    virtual bool operator()(const BaseGalaxyDescriptor &h) const {
      bool radiusCut = (h.radius >= selection.small_radius_cut) &&
                       (h.radius < selection.large_radius_cut);
      return radiusCut;
    }
  };

  template <typename DMSimulation>
  class SpinCutter {
  public:
    GalaxySampleSelection selection;
    DMSimulation *h_el;

    SpinCutter(GalaxySampleSelection sel, DMSimulation *e)
        : selection(sel), h_el(e) {}

    virtual bool operator()(const BaseGalaxyDescriptor &h) const {
      bool spinCut = (h.spin >= selection.low_spin_cut) &&
                     (h.spin < selection.high_spin_cut);
      return spinCut;
    }
  };

  namespace details_cutter {
    template <typename Cutter>
    bool _internal_cutter(const BaseGalaxyDescriptor &g, const Cutter &cutter) {
      return cutter(g);
    }

    template <typename Cutter>
    GalaxySelector cutterFunction(Cutter cutter) {
      return std::bind(_internal_cutter<Cutter>, std::placeholders::_1, cutter);
    }

  }; // namespace details_cutter

  using details_cutter::cutterFunction;
}; // namespace LibLSS

#endif
