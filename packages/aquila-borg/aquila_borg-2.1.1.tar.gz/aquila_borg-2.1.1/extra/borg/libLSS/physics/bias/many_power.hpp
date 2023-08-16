/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/bias/many_power.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHYSICS_MANY_POWER_HPP
#define __LIBLSS_PHYSICS_MANY_POWER_HPP

// This header provides the implementations of a simple power law bias model.
// A generic bias model must implement the following concept:
//     a "selection_adaptor" functor, available from the object
//     a "compute_density(final_density)" function accepting a virtual array and returning a tuple of virtual array.
//     a "apply_adjoint_gradient(final_density,gradient_likelihood_array)" also accepting virtual arrays and returning a virtual array
//     a "prepare" function which is called before the other two calls, to allow for precomputing auxiliary complex fields.
//     a "cleanup" which allows for tearing down any auxiliary fields and memory allocated in the prepare phase.

#include <cmath>
#include <functional>
#include <array>
#include "libLSS/tools/fused_array.hpp"
#include <tuple>
#include "libLSS/tools/phoenix_vars.hpp"
#include <boost/phoenix/operator.hpp>
#include <boost/phoenix/stl/cmath.hpp>
#include "libLSS/tools/tuple_helper.hpp"
#include "libLSS/physics/bias/base.hpp"
#include "libLSS/tools/mpi/ghost_planes.hpp"
#include "libLSS/tools/array_tools.hpp"
#include <boost/config.hpp>
#include "libLSS/tools/string_tools.hpp"
#include "libLSS/physics/bias/level_combinator.hpp"

namespace LibLSS {

  namespace bias {

    namespace detail_manypower {

      using namespace LibLSS::Combinator;

      template <typename LevelCombinator = Levels<double, 0>>
      struct ManyPower {

        static constexpr const bool NmeanIsBias = true;
        typedef ManyPower<LevelCombinator> Self;
        typedef LevelCombinator Levels;
        static constexpr const int numParams = LevelCombinator::numParams;
        static constexpr const int Nmax = LevelCombinator::Nmax;

        size_t startN0, localN0;

        // This adaptor transforms an unselected galaxy density (with appropriate
        // auxiliary arrays) to a selected array. It must be a functor accepting two
        // parameters: a selection virtual array and a bias density virtual array.
        selection::SimpleAdaptor selection_adaptor;

        typedef boost::multi_array<double, 2> Matrix;
        Matrix A;

        LevelCombinator combinator;
        double nmean;
        GhostPlanes<double, 2> ghosts;
        bool needInit;
        size_t N0, N1, N2;
        double prior_width;

        typedef UninitializedArray<boost::multi_array<double, 3>> U_Density_t;
        std::shared_ptr<U_Density_t> ag_density, full_density;

        ManyPower(LikelihoodInfo const &info = LikelihoodInfo()) {
          needInit = true;
          prior_width =
              Likelihood::query<double>(info, "ManyPower_prior_width");
          Console::instance().format<LOG_INFO>(
              "ManyPower running with prior_width=%g", prior_width);
        }

        template <typename BiasParameters>
        static inline void setup_default(BiasParameters &params) {
          array::fill(params, 0);
          for (uint32_t i = 0; i < Nmax; i++) {
            uint32_t q = i * (i + 1) / 2;
            Console::instance().c_assert(q < params.size(), "Problem!");
            params[q] =1;//i * (i + 3) / 2] = 1;
          }
          params[0] = 120;
          Console::instance().print<LOG_DEBUG>(
              "setup_default Nparams=" + to_string(numParams) +
              " params=" + to_string(params));
        }

        // Nota: fwd_model and final_density arrays cannot be stored in this step. But
        // they can be used.
        template <
            class ForwardModel, typename FinalDensityArray,
            typename BiasParameters, typename MetaSelect = NoSelector>
        inline void prepare(
            ForwardModel &fwd_model, const FinalDensityArray &final_density,
            double const _nmean, const BiasParameters &params,
            bool density_updated, MetaSelect _select = MetaSelect()) {
          ConsoleContext<LOG_DEBUG> ctx("prepare manypower");
          auto &mgr = fwd_model.out_mgr;
          if (needInit) {
            auto box = fwd_model.get_box_model_output();

            Console::instance().c_assert(
                params.size() >= numParams,
                "Invalid number of bias parameters (" +
                    std::to_string(params.size()) + "<" +
                    std::to_string(numParams) + ")");
            startN0 = mgr->startN0;
            localN0 = mgr->localN0;

            N0 = box.N0;
            N1 = box.N1;
            N2 = box.N2;

            // First allocate all required caches and find out
            // which planes are required here.
            combinator.allocate(N0, N1, N2, mgr->N2real, startN0, localN0);
            // Setup the ghost plane manager of our requirements.
            combinator.setup(ghosts, fwd_model.communicator());

            ag_density = std::make_shared<U_Density_t>(mgr->extents_real());
            full_density = std::make_shared<U_Density_t>(mgr->extents_real());

            needInit = false;
          }

          A.resize(boost::extents[Nmax][Nmax]);

          // Make a triangle^T triangle matrix multiplication
          std::array<double, numParams> mod_params;
          Console::instance().c_assert(
              params.size() >= mod_params.size(),
              "Input params does not have expected size");
          {
            auto iter = params.begin();
            auto iter_out = mod_params.begin();
            for (int i = 0; i < numParams; i++) {
              *iter_out = *iter;
              ++iter;
              ++iter_out;
            }
          }
          nmean = mod_params[0];
          mod_params[0] = 1;

          for (uint32_t i = 0; i < Nmax; i++) {
            for (uint32_t j = 0; j < Nmax; j++) {
              A[i][j] = 0;
              for (uint32_t k = 0; k <= std::min(i, j); k++)
                A[i][j] += mod_params[i * (i + 1) / 2 + k] *
                           mod_params[j * (j + 1) / 2 + k];
              // We ignore _nmean
            }
            ctx.print("A[" + to_string(i) + "]=" + to_string(A[i]));
          }

          if (density_updated) {
            ctx.print("Density updated. Resynchronize.");
            auto ff = full_density->get_array()[mgr->strict_range()];
            auto s = ff.shape();
            auto ib = ff.index_bases();
            auto s2 = final_density.shape();
            auto ib2 = final_density.index_bases();
            ctx.print(
                boost::format(" fd: %dx%dx%d  [%d,%d,%d] ") % s[0] % s[1] %
                s[2] % ib[0] % ib[1] % ib[2]);
            ctx.print(
                boost::format(" id: %dx%dx%d  [%d,%d,%d] ") % s2[0] % s2[1] %
                s2[2] % ib2[0] % ib2[1] % ib2[2]);
            LibLSS::copy_array_rv(
                full_density->get_array()[mgr->strict_range()],
                final_density[mgr->strict_range()]);
            // Produce the multi-level representation
            // First synchronize data.
            ghosts.synchronize(full_density->get_array());
            // Now build the different levels from the planes.
            combinator.buildLevels(ghosts, final_density);
          }
        }

        inline void cleanup() {
          Console::instance().print<LOG_DEBUG>("Cleanup ManyPower");
          // No need for cleanup
        }

        template <typename BiasParameters>
        inline double log_prior_params(const BiasParameters &params) const {
          double u = 0; // we skip the first one which should be uniform
          for (size_t i = 1; i < numParams; i++) {
            u += params[i] * params[i];
          }
          return -0.5 * u / prior_width;
        }

        template <typename AGArrayType, typename ArrayType>
        inline void gradient_density_lambda(
            ArrayType const &final_density, AGArrayType const &ag_likelihood) {
          ConsoleContext<LOG_DEBUG> ctx("many power gradient_density_lambda");
          std::array<double, LevelCombinator::Nmax> Delta, Delta_prime;
          std::array<double, LevelCombinator::numLevel> DensityLevel;
          size_t finalN0 = startN0 + localN0;
          auto &ag_array = ag_density->get_array();

          ghosts.clear_ghosts();
          combinator.clear_cache();
          array::fill(ag_array, 0);
          ctx.print("Building separate ag components");
          for (size_t i = startN0; i < finalN0; i++) {
            for (size_t j = 0; j < N1; j++) {
              for (size_t k = 0; k < N2; k++) {
                size_t idx;
                double const ag = ag_likelihood[i][j][k] * nmean;

                // Again the forward pass. We need the density at all levels.
                combinator.get_density(DensityLevel, final_density, i, j, k);

                // However we only need the gradient of the power of these density.
                // Compute gradient of the density operators
                std::array<size_t, LevelCombinator::Nmax> to_level;
                std::array<double, LevelCombinator::numLevel> ret;
                Delta_prime[0] = 0;
                Delta[0] = 1;
                to_level[0] = -1;
                idx = 1;

                for (size_t level = 0; level < LevelCombinator::numLevel;
                     level++) {
                  double const delta_level = DensityLevel[level];
                  ret[level] = 0;
                  if (LevelCombinator::getPower(level + 1) < 1)
                    continue;
                  Delta_prime[idx] = ag;
                  Delta[idx] = delta_level;
                  to_level[idx] = level;
                  idx++;
                  for (uint32_t i = 1; i < LevelCombinator::getPower(level + 1);
                       i++, idx++) {
                    Delta[idx] = Delta[idx - 1] *
                                 delta_level; // delta^(i+1) = delta^i * delta
                    Delta_prime[idx] =
                        (i + 1) * Delta[idx - 1] * ag; // (i+1) delta^i * AG
                    to_level[idx] =
                        level; // transform the index to a averaging level
                  }
                }
                auto &cons = Console::instance();
                //cons.print<LOG_DEBUG>("Delta = " + to_string(Delta));
                //cons.print<LOG_DEBUG>("DeltaPrime = " + to_string(Delta_prime));
                //cons.print<LOG_DEBUG>("to_level = " + to_string(to_level));
                cons.c_assert(idx == LevelCombinator::Nmax, "Internal error");

                // Now we need to compute the real AG. The first pass gets
                // the ag for each level.
                // i==0 and j==0 are pointing to the constant part which have
                // no equivalent level. We skip those.
                for (uint32_t q = 1; q < LevelCombinator::Nmax; q++) {
                  size_t l_q = to_level[q];
                  for (uint32_t p = 1; p < q; p++) {
                    ret[l_q] += 2 * Delta_prime[q] * Delta[p] * A[q][p];
                    ret[to_level[p]] += 2 * Delta_prime[p] * Delta[q] * A[q][p];
                  }
                  ret[l_q] += Delta_prime[q] *
                              (2 * Delta[0] * A[q][0] + 2 * Delta[q] * A[q][q]);
                }
                // Now recombine all levels to give the final AG at voxel i,j,k.
                combinator.push_ag_density(ret, ag_array, i, j, k);
              }
            }
          }

          ctx.print("Build ag levels");
          combinator.ag_buildLevels(ghosts, ag_array);

          ctx.print("Do ag synchronization");
          // Now we do global communication to reduce all planes
          ghosts.synchronize_ag(ag_array);
        }

        template <typename ArrayType>
        inline double density_lambda(
            ArrayType const &final_density, size_t i, size_t j, size_t k) {
          std::array<double, LevelCombinator::Nmax> Delta;
          std::array<double, LevelCombinator::numLevel> DensityLevel;
          size_t idx = 0;

          // If we touch padding. Go away.
          if (k >= N2)
            return 0;

          // Forward collapse
          // DensityLevel receives all the density levels corresponding to
          // the voxel i,j,k
          //        DensityLevel[0] = final_density[i][j][k];
          combinator.get_density(DensityLevel, final_density, i, j, k);

          // Now build the vector. First is just a constant.
          Delta[0] = 1;
          idx = 1;
          for (size_t level = 0; level < LevelCombinator::numLevel; level++) {
            // Each level starts with just the initial value.
            if (LevelCombinator::getPower(level + 1) >= 1)
              Delta[idx++] = DensityLevel[level];
            for (uint32_t i = 1; i < LevelCombinator::getPower(level + 1);
                 i++, idx++) {
              // Then we add power of that value.
              Delta[idx] = Delta[idx - 1] * DensityLevel[level];
            }
          }
          Console::instance().c_assert(
              idx == LevelCombinator::Nmax, "Internal error");
          // Now we have built the vector over which we need the quadratic
          // form.

          // Now compute the 2-norm with the Q-form A.
          double ret = 0;
          for (uint32_t i = 0; i < Nmax; i++) {
            for (uint32_t j = 0; j < i; j++) {
              ret += 2 * Delta[i] * Delta[j] * A[i][j];
            }
            ret += Delta[i] * Delta[i] * A[i][i];
          }
          Console::instance().c_assert(!std::isnan(ret), "NaN in density");
          Console::instance().c_assert(!std::isinf(ret), "Inf in density");
          Console::instance().c_assert(!std::isnan(nmean), "NaN in nmean");
          return ret * nmean;
        }

        inline double get_linear_bias() const { return 1; }

        template <typename Array>
        static inline bool check_bias_constraints(Array &&a) {
          bool condition = a[1] > 0;  // Ensure linear bias positive
          Console::instance().c_assert(a.size() <= numParams, "Invalid number of parameters");
//          for (int j = 0; j < Nmax; j++)
//             condition = condition && (a[j * (j + 3) / 2] > 0);
          return condition;
        }

        // This function returns a tuple of array-like arrays.
        // In practice for ManyPower we compute the content to a temporary array as there was
        // some padding/boundary issues in the past.
        template <typename FinalDensityArray>
        inline auto compute_density(const FinalDensityArray &a) {
          ConsoleContext<LOG_DEBUG> ctx("many_power compute_density");
          LibLSS::copy_array(
              full_density->get_array(),
              b_fused_idx<double, 3>(std::bind(
                  &Self::density_lambda<FinalDensityArray>, this, std::cref(a),
                  ph::_1, ph::_2, ph::_3)));
          return std::make_tuple(std::cref(full_density->get_array()));
        }

        // This function returns a tuple of array-like objects. Those arrays
        // depend on the existence of the final density array and the gradient likelihood array.
        // That is the job of the caller to ensure that temporary variables are not cleared
        // before the final use.
        // The return type is quite complex. Let the compiler decides.
        // L(b_0(delta, p), b_1(delta, p), ..., b_n(delta, p))
        // Now we take a tuple of gradient and collapse this to a gradient of delta.
        template <
            typename FinalDensityArray, typename TupleGradientLikelihoodArray>
        inline auto apply_adjoint_gradient(
            const FinalDensityArray &array,
            TupleGradientLikelihoodArray grad_array) {
          BOOST_STATIC_ASSERT(
              (std::tuple_size<TupleGradientLikelihoodArray>::value == 1));
          LIBLSS_AUTO_DEBUG_CONTEXT(ctx);

          gradient_density_lambda(array, std::get<0>(grad_array));

          return std::make_tuple(std::cref(ag_density->get_array()));
        }
      };

    } // namespace detail_manypower

    using detail_manypower::ManyPower;
    template <typename T, size_t... N>
    using ManyPowerLevels = detail_manypower::Levels<T, N...>;
  } // namespace bias

} // namespace LibLSS

#endif
