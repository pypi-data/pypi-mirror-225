/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/hmclet/hmclet_qnhmc.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_HMCLET_QNHMCLET_HPP
#define __LIBLSS_HMCLET_QNHMCLET_HPP

#include <memory>
#include <boost/multi_array.hpp>
#include "libLSS/samplers/core/random_number.hpp"
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/tools/errors.hpp"
#include "libLSS/hmclet/hmclet.hpp"
#include "libLSS/tools/hdf5_scalar.hpp"
#include <Eigen/Core>

namespace LibLSS {

  // Implement QN-HMC algorithm
  // http://auai.org/uai2016/proceedings/papers/102.pdf
  namespace QNHMCLet {

    using HMCLet::VectorType;
    using HMCLet::JointPosterior;

    class BDense {
    protected:
      size_t numParams;
      size_t store;
      boost::multi_array<double, 2> B;
      boost::multi_array<double, 1> prev_theta, prev_grad_f;
      Eigen::VectorXd s_k, y_k;
    public:
      BDense(size_t numParams_)
        : numParams(numParams_),store(0),
        B(boost::extents[numParams][numParams]),  prev_theta(boost::extents[numParams]), prev_grad_f(boost::extents[numParams]),  s_k(numParams), y_k(numParams) {
          reset();
      }

      void reset() {
	  store = 0;
	  fwrap(prev_theta) = 0;
	  fwrap(prev_grad_f) = 0;
	  fwrap(B) = 0;
          for (size_t i = 0; i < numParams; i++)
            B[i][i] = 1e-5;
      }

      BDense(BDense const& other)
        : numParams(other.numParams), store(other.store),
        B(boost::extents[numParams][numParams]), prev_theta(boost::extents[numParams]), prev_grad_f(boost::extents[numParams]), s_k(numParams), y_k(numParams) {
        fwrap(B) = other.B;
        store = other.store;
        s_k = other.s_k;
        y_k = other.y_k;
        fwrap(prev_theta) = other.prev_theta;
        fwrap(prev_grad_f) = other.prev_grad_f;
      }

      BDense const& operator=(BDense const& other) {
        Console::instance().c_assert(numParams == other.numParams, "Invalid B matrix state");;
        //B.resize(boost::extents[numParams][numParams]);
        fwrap(B) = other.B;
        store = other.store;
        s_k = other.s_k;
        y_k = other.y_k;
        fwrap(prev_theta) = other.prev_theta;
        fwrap(prev_grad_f) = other.prev_grad_f;
        return *this;
      }

      template<typename Theta, typename Gradient>
      void addInfo(Theta const& theta, Gradient const& grad_f) {
        auto w_prev_theta = fwrap(prev_theta);
        auto w_prev_grad_f = fwrap(prev_grad_f);

        auto B_map = Eigen::Map<Eigen::MatrixXd>(B.data(), numParams, numParams);

        store++;
        if (store == 1) {
            w_prev_theta = theta;
            w_prev_grad_f = grad_f;
            return;
        }
        for (size_t i = 0; i < numParams; i++) {
          s_k(i) = theta[i] - prev_theta[i];
          y_k(i) = (grad_f[i] - prev_grad_f[i]);
        }

        double const alpha_0 = s_k.dot(y_k);
        double const alpha = 1/alpha_0;

        if (alpha_0*alpha_0 < 1e-5 * s_k.dot(s_k) * y_k.dot(y_k) ) {
//          w_prev_theta = theta;
//        w_prev_grad_f = grad_f;
          Console::instance().print<LOG_DEBUG>(
              boost::format("SKIPPED alpha = %lg, reduced = %lg" ) % alpha %
                (alpha_0/std::sqrt(s_k.dot(s_k) * y_k.dot(y_k))));
          return;
        }
        Console::instance().print<LOG_DEBUG>(
            boost::format("alpha = %lg, s_k = %lg, y_k = %lg, reduced = %lg" ) % alpha % std::sqrt(s_k.dot(s_k)) % std::sqrt(y_k.dot(y_k)) %
              (alpha_0/std::sqrt(s_k.dot(s_k) * y_k.dot(y_k))));


        auto I = Eigen::MatrixXd::Identity(numParams,numParams);
        Eigen::MatrixXd M = I - y_k * s_k.transpose() * alpha;
        Eigen::MatrixXd N = s_k *  s_k.transpose() * alpha;

        B_map = M.transpose() * B_map * M;
        B_map += N;

        w_prev_theta = theta;
        w_prev_grad_f = grad_f;
      }

      void operator()(boost::multi_array_ref<double,1>& x)
      {
        Eigen::Map<Eigen::VectorXd> m_x(x.data(), numParams);
        Eigen::Map<Eigen::MatrixXd> m_B(B.data(), numParams, numParams);
        m_x = m_B * m_x;
      }

      boost::multi_array_ref<double, 2> const& get() const { return B; }

      void save(H5_CommonFileGroup& g) {
        CosmoTool::hdf5_write_array(g, "B", B);
	CosmoTool::hdf5_write_array(g, "prev_theta", prev_theta);
	CosmoTool::hdf5_write_array(g, "prev_grad_f", prev_grad_f);
	hdf5_save_scalar(g, "store", store);
      }
      void load(H5_CommonFileGroup& g) {
        CosmoTool::hdf5_read_array(g, "B", B);
	CosmoTool::hdf5_read_array(g, "prev_theta", prev_theta);
	CosmoTool::hdf5_read_array(g, "prev_grad_f", prev_grad_f);
	store = hdf5_load_scalar<int>(g, "store");
      }
    };

    template <typename MassType, typename BMatrixType>
    class Sampler : public HMCLet::AbstractSimpleSampler {
    public:
      typedef MassType mass_t;

      Sampler(std::shared_ptr<JointPosterior> posterior);
      ~Sampler();

      virtual void
      newSample(MPI_Communication *comm, RandomNumber &rng, VectorType &params);

            virtual void calibrate(
                MPI_Communication *comm, RandomNumber &rng, size_t numSteps,
                VectorType const &initial_params, VectorType const &initial_step) {}

      mass_t &getMass() { return massMatrix; }
      BMatrixType& getB() { return B; }

      virtual void reset() {
       Console::instance().print<LOG_DEBUG>("Resetting QN-HMC"); B.reset(); 
       fwrap(momentum) = 0;
      }

    protected:
      size_t numParams;
      mass_t massMatrix;
      BMatrixType B;
      std::shared_ptr<JointPosterior> posterior;

      typedef VectorType Vector;
      boost::multi_array<double, 1> momentum;
    };

  } // namespace QNHMCLet

} // namespace LibLSS

#endif
