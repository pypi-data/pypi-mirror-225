/*+
    ARES/HADES/BORG Package -- ./libLSS/physics/class_cosmo.hpp
    Copyright (C) 2020 Jens Jasche <jens.jasche@fysik.su.se>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_CLASS_COSMO_HPP
#  define __LIBLSS_CLASS_COSMO_HPP

#  include <map>
#  include <string>
#  include <memory>
#  include "libLSS/physics/cosmo.hpp"

namespace LibLSS {

  struct OpaqueClass;

  class ClassCosmo {
  private:
    std::unique_ptr<OpaqueClass> opaque;
    typedef boost::multi_array_ref<double, 1> array_ref_1d;
    typedef boost::multi_array<double, 1> array_1d;

    size_t numInterpolationPoints;

  public:
    typedef std::map<std::string, double> DictCosmology;

    ClassCosmo(CosmologicalParameters const &params); // This is the constructor
    ~ClassCosmo();

    void setInterpolation(size_t numPoints);

    double primordial_Pk(double k);
    void updateCosmo();
    double get_Tk(double k);
    void retrieve_Tk();
    DictCosmology getCosmology();

  protected:
    void reinterpolate(array_ref_1d const &k, array_ref_1d const &Tk);
  };

} // namespace LibLSS

#endif

// ARES TAG: num_authors = 1
// ARES TAG: name(0) = Jens Jasche
// ARES TAG: email(0) = jens.jasche@fysik.su.se
// ARES TAG: year(0) = 2020
