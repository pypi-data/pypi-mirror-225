/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/hmclet/hmclet.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HMCLET_HMCLET_HPP
#define __LIBLSS_HMCLET_HMCLET_HPP

#include <memory>
#include <boost/multi_array.hpp>
#include "libLSS/samplers/core/random_number.hpp"
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/tools/errors.hpp"

namespace LibLSS {

  namespace HMCLet {

    typedef boost::multi_array_ref<double, 1> VectorType;

    LIBLSS_NEW_ERROR(ErrorBadGradient);
    LIBLSS_NEW_ERROR(ErrorBadReject);

    class JointPosterior {
    public:
      JointPosterior() {}
      virtual ~JointPosterior() {}

      virtual size_t getNumberOfParameters() const = 0;
      virtual double evaluate(VectorType const &params) = 0;
      virtual void adjointGradient(
          VectorType const &params, VectorType &params_gradient) = 0;
    };

    class AbstractSimpleSampler {
    public:
      AbstractSimpleSampler() : maxEpsilon(0.02), maxNtime(50), momentumScale(0.0) {}

      virtual void calibrate(
          MPI_Communication *comm, RandomNumber &rng, size_t numSteps,
          VectorType const &initial_params, VectorType const &initial_step) = 0;
      virtual void newSample(
          MPI_Communication *comm, RandomNumber &rng, VectorType &params) = 0;

      void setMaxEpsilon(double epsilon_) { maxEpsilon = epsilon_; }
      void setMaxNtime(size_t ntime_) { maxNtime = ntime_; }
      void setMassScaling(double scale_) { momentumScale = scale_; }

      virtual void reset() {}

      double maxEpsilon;
      double momentumScale;
      size_t maxNtime;
    };

    template <typename MassType>
    class SimpleSampler : public AbstractSimpleSampler {
    public:
      typedef MassType mass_t;

      SimpleSampler(std::shared_ptr<JointPosterior> posterior);
      ~SimpleSampler();

      virtual void calibrate(
          MPI_Communication *comm, RandomNumber &rng, size_t numSteps,
          VectorType const &initial_params, VectorType const &initial_step);
      virtual void
      newSample(MPI_Communication *comm, RandomNumber &rng, VectorType &params);

      mass_t &getMass() { return massMatrix; }

    protected:
      size_t numParams;
      mass_t massMatrix;
      std::shared_ptr<JointPosterior> posterior;
      boost::multi_array<double, 1> momentum;
    };

  } // namespace HMCLet

} // namespace LibLSS

#endif
