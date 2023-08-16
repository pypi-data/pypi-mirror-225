/*+
    ARES/HADES/BORG Package -- ./libLSS/data/survey_load_txt.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_GALAXY_LOAD_TXT_HPP
#define __LIBLSS_GALAXY_LOAD_TXT_HPP

#include <string>
#include <fstream>
#include <iostream>
#include <sstream>
#include <boost/format.hpp>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/errors.hpp"

namespace LibLSS {

  template <typename GalaxySurvey>
  void
  loadGalaxySurveyFromText(const std::string &fname, GalaxySurvey &survey) {
    using namespace std;
    using boost::format;
    Console &cons = Console::instance();
    long originalSize = survey.surveySize();
    string line;

    ifstream f(fname.c_str());

    if (!f) {
      error_helper<ErrorIO>(format("Cannot open file '%s'") % fname);
    }

    cons.print<LOG_STD>(format("Reading galaxy survey file '%s'") % fname);
    bool warningDefault = false;
    while (getline(f, line)) {
      istringstream ss(line);
      typename GalaxySurvey::GalaxyType g;

      ss >> g.id >> g.phi >> g.theta >> g.zo >> g.m >> g.M_abs >> g.z;
      g.Mgal = 0;
      g.r = 0;
      g.radius = 0;
      g.spin = 0;
      g.posx = g.posy = g.posz = 0;
      g.vx = g.vy = g.vz = 0;
      if (!(ss >> g.w)) {
        g.w = 1;
        warningDefault = true;
      }
      g.final_w = g.w;
      survey.addGalaxy(g);
    }
    if (warningDefault)
      cons.print<LOG_WARNING>("I used a default weight of 1");
    cons.print<LOG_STD>(
        format("Receive %d galaxies in total") %
        (survey.surveySize() - originalSize));
    survey.optimize();
  }

  template <typename GalaxySurvey>
  void loadHaloSimulationFromText(const std::string &fname, GalaxySurvey &sim) {
    using namespace std;
    using boost::format;
    Console &cons = Console::instance();
    long originalSize = sim.surveySize();
    string line;

    ifstream f(fname.c_str());

    if (!f) {
      error_helper<ErrorIO>(format("Cannot open file '%s'") % fname);
    }

    cons.print<LOG_STD>(format("Read halo catalog file '%s'") % fname);
    bool warningDefault = false;
    while (getline(f, line)) {
      istringstream ss(line);
      typename GalaxySurvey::GalaxyType h;

      ss >> h.id >> h.Mgal >> h.radius >> h.spin >> h.posx >> h.posy >>
          h.posz >> h.vx >> h.vy >> h.vz;

      if (!(ss >> h.w)) {
        h.w = 1;
        warningDefault = true;
      }
      h.final_w = h.w;
      vec2ang(
          std::array<double, 3>{h.posx, h.posy, h.posz}, h.phi, h.theta, h.r);
      sim.addGalaxy(h);
    }
    sim.optimize();
    if (warningDefault)
      cons.print<LOG_WARNING>("Use default weight of 1 for all halos");
    cons.print<LOG_STD>(
        format("Receive %d halos in total") %
        (sim.surveySize() - originalSize));
  }

} // namespace LibLSS

#endif
