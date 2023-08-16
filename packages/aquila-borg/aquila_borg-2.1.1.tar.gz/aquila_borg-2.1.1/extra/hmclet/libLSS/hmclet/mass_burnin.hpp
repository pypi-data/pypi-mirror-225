/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/hmclet/mass_burnin.hpp
    Copyright (C) 2014-2020 2019 <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HMCLET_DIAGONAL_MASS_BURNIN_HPP
#  define __LIBLSS_HMCLET_DIAGONAL_MASS_BURNIN_HPP

#  include <memory>
#  include <boost/multi_array.hpp>
#  include "libLSS/samplers/core/random_number.hpp"
#  include <CosmoTool/hdf5_array.hpp>
#  include "libLSS/tools/errors.hpp"
#  include "libLSS/hmclet/hmclet.hpp"

namespace LibLSS {

  namespace HMCLet {

    template <typename Matrix>
    class MassMatrixWithBurnin : public Matrix {
    protected:
      typedef Matrix super_t;
      size_t memorySize;
      size_t burninMaxIteration;
      size_t stepID;

      std::list<boost::multi_array<double, 1>> memory;

    public:
      MassMatrixWithBurnin(size_t numParams_)
          : super_t(numParams_), memorySize(50), burninMaxIteration(300),
            stepID(0) {}

      void setMemorySize(size_t sz) { memorySize = sz; }
      void setBurninMax(size_t maxIteration) {
        burninMaxIteration = maxIteration;
      }
      void saveMass(CosmoTool::H5_CommonFileGroup &g);
      void loadMass(CosmoTool::H5_CommonFileGroup &g);
      void addMass(VectorType const &params);
      void clear();
    };

  } // namespace HMCLet
} // namespace LibLSS

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: name(0) = 2019
