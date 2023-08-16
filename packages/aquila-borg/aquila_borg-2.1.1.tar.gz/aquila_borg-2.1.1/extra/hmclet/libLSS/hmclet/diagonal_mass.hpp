/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/hmclet/diagonal_mass.hpp
    Copyright (C) 2014-2020 2019 <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HMCLET_DIAGONAL_MASS_HPP
#  define __LIBLSS_HMCLET_DIAGONAL_MASS_HPP

#  include <memory>
#  include <boost/multi_array.hpp>
#  include "libLSS/samplers/core/random_number.hpp"
#  include <CosmoTool/hdf5_array.hpp>
#  include "libLSS/tools/errors.hpp"
#  include "libLSS/hmclet/hmclet.hpp"

namespace LibLSS {

  namespace HMCLet {

    class DiagonalMassMatrix {
    protected:
      size_t numParams;
      boost::multi_array<double, 1> masses, inv_sqrt_masses, icMass, variances;
      boost::multi_array<double, 1> mean;
      size_t initialMassWeight;
      size_t numInMass;
      bool frozen;

    public:
      DiagonalMassMatrix(size_t numParams_)
          : numParams(numParams_), masses(boost::extents[numParams]),
            inv_sqrt_masses(boost::extents[numParams]),
            icMass(boost::extents[numParams]), mean(boost::extents[numParams]),
            variances(boost::extents[numParams]), numInMass(0),
            initialMassWeight(0), frozen(false) {}

      void setInitialMass(VectorType const &params);
      void freeze() { frozen = true; }
      void freezeInitial() { fwrap(icMass) = fwrap(masses); }
      void saveMass(CosmoTool::H5_CommonFileGroup &g);
      void loadMass(CosmoTool::H5_CommonFileGroup &g);
      void addMass(VectorType const &params);
      void clear();

      template <typename A>
      auto operator()(A const &q) const {
        return q * fwrap(masses);
      }

      template<typename A, typename B>
      auto operator()(A const& a, B&& b) const {
	return operator()(a);
      }

      auto sample(RandomNumber &rgen) const
          -> decltype(rgen.gaussian(fwrap(inv_sqrt_masses))) {
        return rgen.gaussian(fwrap(inv_sqrt_masses));
      }

    protected:
      void finishMass();
    };

  } // namespace HMCLet

} // namespace LibLSS

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: name(0) = 2019
