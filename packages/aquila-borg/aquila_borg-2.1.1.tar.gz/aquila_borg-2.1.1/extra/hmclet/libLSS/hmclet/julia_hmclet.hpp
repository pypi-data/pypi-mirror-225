/*+
    ARES/HADES/BORG Package -- ./extra/hmclet/libLSS/hmclet/julia_hmclet.hpp
    Copyright (C) 2014-2020 2018-2019 <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_JULIA_HMCLET_HPP
#  define __LIBLSS_JULIA_HMCLET_HPP

#  include <memory>
#  include "libLSS/samplers/core/markov.hpp"
#  include "libLSS/julia/julia.hpp"
#  include "libLSS/samplers/julia/julia_likelihood.hpp"
#  include "libLSS/hmclet/hmclet.hpp"
#  include "libLSS/tools/mpi/ghost_planes.hpp"

namespace LibLSS {

  namespace JuliaHmclet {

    namespace types {
      typedef ArrayType1d::ArrayType bias_t;

      enum MatrixType {
        DIAGONAL, DENSE, QN_DIAGONAL
      };
    }

    namespace details {
      using namespace types;

      using namespace HMCLet;

      class JuliaHmcletPosterior : virtual public JointPosterior {
      protected:
        MPI_Communication *comm;
        std::string likelihood_module;
        std::string likelihood_name;
        std::string adjoint_name;
        size_t cat_id;
        Julia::Object *density;
        Julia::Object *state;
        Julia::Object *ghosts;
        size_t numBiasParams;
        std::string param_priors_name;

      public:
        JuliaHmcletPosterior(
            MPI_Communication *comm_, const std::string likelihood_module_,
            size_t cat_id_, size_t numBiasParams_)
            : comm(comm_), likelihood_module(likelihood_module_),
              likelihood_name(
                  JuliaLikelihood::likelihood_evaluate_bias(likelihood_module)),
              adjoint_name(
                  JuliaLikelihood::likelihood_adjoint_bias(likelihood_module)),
              cat_id(cat_id_), numBiasParams(numBiasParams_),
              param_priors_name(likelihood_module + ".log_prior_bias") {}
        virtual ~JuliaHmcletPosterior() {}

        // We try to save a bit of julia stack protection.
        void updateGhosts(Julia::Object &ghosts_) { ghosts = &ghosts_; }
        void updateState(Julia::Object &state_, Julia::Object &density_) {
          state = &state_;
          density = &density_;
        }
        virtual size_t getNumberOfParameters() const;
        virtual double evaluate(VectorType const &params);
        virtual void
        adjointGradient(VectorType const &params, VectorType &params_gradient);
      };

      typedef std::function<std::unique_ptr<AbstractSimpleSampler>(
          std::shared_ptr<JuliaHmcletPosterior> &, MarkovState &,
          std::string const &)>
          samplerBuilder_t;
      typedef std::function<void(
          std::unique_ptr<AbstractSimpleSampler> &, Julia::Object &)>
          massMatrixInit_t;

      class JuliaHmcletMeta : virtual public MarkovSampler {
      protected:
        MPI_Communication *comm;
        std::string module_name;
        typedef HMCLet::AbstractSimpleSampler sampler_t;
        typedef std::unique_ptr<sampler_t> SimpleSampler_p;
        typedef std::vector<SimpleSampler_p> SimpleSampler_pv;

        std::vector<std::shared_ptr<details::JuliaHmcletPosterior>> posteriors;
        SimpleSampler_pv hmcs;
        size_t Ncatalog, N0, N1, N2, N2real, localN0;
        GhostPlanes<double, 2> ghosts;
        std::shared_ptr<JuliaDensityLikelihood> likelihood;
        Defer ready_hmclet;
        MatrixType massMatrixType;
        size_t burnin;
        size_t memorySize;
        double limiter;
        bool frozen;

        massMatrixInit_t massMatrixInit;

        std::tuple<samplerBuilder_t, massMatrixInit_t> getAdequateSampler();

      public:
        JuliaHmcletMeta(
            MPI_Communication *comm, std::shared_ptr<JuliaDensityLikelihood> likelihood_,
            const std::string &likelihood_module, MatrixType massMatrixType_,
            size_t burnin, size_t memorySize, double limiter, bool frozen);
        ~JuliaHmcletMeta();

        Defer &postinit() { return ready_hmclet; }
        SimpleSampler_pv &hmclets() { return hmcs; }
        virtual void initialize(MarkovState &state);
        virtual void restore(MarkovState &state);
        virtual void sample(MarkovState &state);
      };

    } // namespace details
  }   // namespace JuliaHmclet

  using JuliaHmclet::details::JuliaHmcletMeta;
} // namespace LibLSS

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: name(0) = 2018-2019
