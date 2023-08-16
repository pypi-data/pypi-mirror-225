/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/cpu/feature_check_other.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
namespace LibLSS {
  static inline bool check_compatibility(std::string &features) {
    features = "*UNKNOWN*";
    return true;
  }
} // namespace LibLSS
