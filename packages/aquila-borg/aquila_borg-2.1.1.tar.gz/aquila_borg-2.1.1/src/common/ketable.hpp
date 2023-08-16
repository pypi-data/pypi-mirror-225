/*+
    ARES/HADES/BORG Package -- ./src/common/ketable.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_KETABLE_HPP
#define __LIBLSS_KETABLE_HPP

#include <CosmoTool/interpolate.hpp>
#include <string>
#include <H5Cpp.h>

namespace LibLSS {

  class KETableCorrection {
  protected:
    bool no_correction;
    CosmoTool::Interpolate data;

  public:
    KETableCorrection() { no_correction = true; }
    KETableCorrection(const std::string &fname)
        : data(CosmoTool::buildInterpolateFromFile(fname.c_str())),
          no_correction(false) {}

    double getZCorrection(double z) {
      if (no_correction)
        return 0;
      else
        return data.compute(z);
    }

    void save(H5_CommonFileGroup &fg) {}

    void restore(H5_CommonFileGroup &fg) {}
  };
} // namespace LibLSS

#endif
