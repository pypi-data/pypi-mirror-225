/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/hmclet/dense_mass.hpp
    Copyright (C) 2014-2020 2019 <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HMCLET_DENSE_MASS_HPP
#  define __LIBLSS_HMCLET_DENSE_MASS_HPP

#  include <memory>
#  include <Eigen/Core>
#  include <Eigen/Cholesky>
#  include <Eigen/Eigenvalues>
#  include <boost/multi_array.hpp>
#  include "libLSS/samplers/core/random_number.hpp"
#  include <CosmoTool/hdf5_array.hpp>
#  include "libLSS/tools/errors.hpp"
#  include "libLSS/hmclet/hmclet.hpp"

namespace LibLSS {

  namespace HMCLet {

    class DenseMassMatrix {
    protected:
      size_t numParams;
      Eigen::MatrixXd finishedCovariances, icCovar, covariances;
      Eigen::LLT<Eigen::MatrixXd> lltOfCovariances;
      Eigen::VectorXd tmp_vector, mean;
      size_t initialMassWeight;
      size_t numInMass;

      boost::multi_array<double, 1> tmp_data;
      Eigen::SelfAdjointEigenSolver<Eigen::MatrixXd> es;
      double limiter;
      bool frozen;

    public:
      DenseMassMatrix(size_t numParams_)
          : numParams(numParams_), finishedCovariances(numParams, numParams),
            icCovar(numParams, numParams), covariances(numParams, numParams),
            lltOfCovariances(numParams), tmp_vector(numParams), mean(numParams),
            initialMassWeight(0), numInMass(0),
            tmp_data(boost::extents[numParams]), limiter(0.5), frozen(false) {
        icCovar.setIdentity();
        clear();
      }

      void setInitialMass(boost::multi_array_ref<double, 2> const &params);
      void freezeInitial() { icCovar = covariances; }
      void freeze() { frozen = true; }
      void setCorrelationLimiter(double limiter_) { limiter = limiter_; }
      void saveMass(CosmoTool::H5_CommonFileGroup &g);
      void loadMass(CosmoTool::H5_CommonFileGroup &g);
      void addMass(VectorType const &params);
      void clear();

      template <
          typename A, typename U = typename std::enable_if<
                          is_wrapper<A>::value, void>::type>
      auto operator()(A const &q) {
        auto tmpv = Eigen::Map<Eigen::VectorXd>(tmp_data.data(), numParams);
        for (size_t i = 0; i < numParams; i++)
          tmp_vector(i) = (*q)[i];
        tmpv.noalias() = finishedCovariances * tmp_vector;
        return fwrap(tmp_data);
      }

      auto operator()(VectorType const &q) { return operator()(fwrap(q)); }

      template <typename A, typename B>
      auto operator()(A const &a, B &&) {
        return operator()(a);
      }

      auto sample(RandomNumber &rgen) -> decltype(fwrap(tmp_data)) {
        boost::multi_array<double, 1> tmp_data2(boost::extents[numParams]);
        auto tmpv2 = Eigen::Map<Eigen::VectorXd>(tmp_data2.data(), numParams);
        auto tmpv = Eigen::Map<Eigen::VectorXd>(tmp_data.data(), numParams);
        fwrap(tmp_data2) = rgen.gaussian(fwrap(b_fused_idx<double, 1>(
            [](int) { return 1; }, boost::extents[numParams])));
        tmpv = lltOfCovariances.matrixL().solve(tmpv2);
        return fwrap(tmp_data);
      }

      void computeMainComponents() { es.compute(finishedCovariances); }

      auto components() { return es.eigenvectors(); }
      auto eigenValues() { return es.eigenvalues(); }
      Eigen::VectorXd const &getMean() const { return mean; }

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
