/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/bias/downgrader.hpp
    Copyright (C) 2019-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_PHYSICS_DOWNGRADER_HPP
#  define __LIBLSS_PHYSICS_DOWNGRADER_HPP

/**
  * This header provides the implementations of a simple power law bias model.
  * A generic bias model must implement the following concept:
  *     a "selection_adaptor" functor, available from the object
  *     a "compute_density(final_density)" function accepting a virtual array and returning a tuple of virtual array.
  *     a "apply_adjoint_gradient(final_density,gradient_likelihood_array)" also accepting virtual arrays and returning a virtual array
  *     a "prepare" function which is called before the other two calls, to allow for precomputing auxiliary complex fields.
  *     a "cleanup" which allows for tearing down any auxiliary fields and memory allocated in the prepare phase.
  */
#  include <cmath>
#  include <functional>
#  include "libLSS/tools/fused_array.hpp"
#  include <tuple>
#  include "libLSS/tools/phoenix_vars.hpp"
#  include <boost/phoenix/operator.hpp>
#  include <boost/phoenix/stl/cmath.hpp>
#  include "libLSS/tools/tuple_helper.hpp"
#  include "libLSS/physics/bias/base.hpp"
#  include "libLSS/physics/bias/level_combinator.hpp"

namespace LibLSS {

  namespace bias {

    namespace detail_downgrader {
      using namespace LibLSS::Combinator;

      namespace ph = std::placeholders;

      template <size_t... l>
      struct DegradeGenerator {
        typedef Levels<double, l...> Level_t;
      };

      /**
        * Downgrader bias
        */
      template <
          typename LowerBias, typename Generator = DegradeGenerator<1, 1, 1>>
      class Downgrader {
      public:
        //  static constexpr const bool NmeanIsBias = LowerBias::NmeanIsBias;
        //  static const auto numParams = LowerBias::numParams;

        // This adaptor transforms an unselected galaxy density (with appropriate
        // auxiliary arrays) to a selected array. It must be a functor accepting two
        // parameters: a selection virtual array and a bias density virtual array.
        //  selection::SimpleAdaptor selection_adaptor;

        //  double nmean;

        //  template <typename BiasParameters>
        //  static inline void setup_default(BiasParameters &params) {
        //
        //  }

        typedef typename Generator::Level_t Level_t;
        static constexpr const bool NmeanIsBias = LowerBias::NmeanIsBias;
        static constexpr const auto numParams = LowerBias::numParams;
        ;

        decltype(
            std::declval<LowerBias>().selection_adaptor) &selection_adaptor;

        Level_t level;
        LowerBias lowerBias;

        GhostPlanes<double, 2> ghosts;
        bool needInit;
        size_t N2;
        std::shared_ptr<U_Array<double, 3>> bias_density, ag_bias_density;

        Downgrader(LikelihoodInfo const& = LikelihoodInfo())
            : needInit(true), selection_adaptor(lowerBias.selection_adaptor) {}

        template <typename Array>
        inline bool check_bias_constraints(Array &&a) {
          return lowerBias.check_bias_constraints(a);
        }

        template <typename Array>
        static inline void setup_default(Array &&a) {
          LowerBias::setup_default(a);
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
          auto &mgr = fwd_model.lo_mgr;
          LIBLSS_AUTO_CONTEXT(LOG_DEBUG, ctx);

          this->N2 = mgr->N2;

          if (needInit) {
            auto box = fwd_model.get_box_model();
            MPI_Communication *comm = mgr->getComm();
            std::tuple<ssize_t, ssize_t> bounds[Level_t::numLevel];

            for (int r = 0; r < Level_t::numLevel; r++) {
              size_t factor =
                  Combinator::const_pow(2, Level_t::numLevel - 1 - r);
              ssize_t start =
                  (mgr->N0 / factor) * comm->rank() / comm->size(); // FIXME
              ssize_t end = (mgr->N0 / factor) * (comm->rank() + 1) /
                            comm->size(); // FIXME
              bounds[r] = std::make_tuple(start, end);
              ctx.format(
                  "Factor %d for level %d (bounds=[%d - %d])", factor, r,
                  std::get<0>(bounds[r]), std::get<1>(bounds[r]));
            }

            level.allocate(
                box.N0, box.N1, box.N2, mgr->N2, mgr->startN0, mgr->localN0,
                bounds);
            level.setup(ghosts, fwd_model.communicator());

            bias_density = std::make_shared<U_Array<double, 3>>(
                mgr->extents_real_strict());
            ag_bias_density = std::make_shared<U_Array<double, 3>>(
                mgr->extents_real_strict());
            needInit = false;
          }

          lowerBias.prepare(
              fwd_model, final_density, _nmean, params, density_updated,
              _select);

          fwrap(bias_density->get_array()) =
              std::get<0>(lowerBias.compute_density(final_density));

          ghosts.synchronize(bias_density->get_array());
          // Now build the different levels from the planes.
          level.buildLevels(ghosts, bias_density->get_array());
        }

        inline void cleanup() { lowerBias.cleanup(); }

        template <typename FinalDensityArray>
        inline auto compute_density(const FinalDensityArray &array) {
          constexpr int numLevel = Level_t::numLevel;
          auto const &barray = bias_density->get_array();

          return std::make_tuple(b_fused_idx<double, 3>(
              [this, &barray, numLevel](size_t i, size_t j, size_t k) {
                double out;
                if (k >= N2 / Combinator::const_pow(2, numLevel - 1)) {
                  auto &cons = Console::instance();
                  cons.format<LOG_ERROR>(
                      "Going above limits with k=%d, numLevel=%d!", k,
                      numLevel);
                  return 0.0;
                }
                out = level.template get_density_level<Level_t::numLevel - 1>(
                    barray, i, j, k);
                if (out < 0 || out == 0 || std::isnan(out) || std::isinf(out)) {
                  auto &cons = Console::instance();
                  //cons.c_assert(!std::isnan(out[numLevel-1]), "Nan in density");
                  cons.format<LOG_ERROR>(
                      "Nan (%g) in density at %dx%dx%d", out, i, j, k);
                  MPI_Communication::instance()->abort();
                }
                return out;
              }));
        }

        // This function returns an array-like array. That array
        // depends on the existence of the final density array and the gradient likelihood array.
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
          constexpr int numLevel = Level_t::numLevel;
          BOOST_STATIC_ASSERT(
              (std::tuple_size<TupleGradientLikelihoodArray>::value == 1));
          auto &ag_array = ag_bias_density->get_array();
          auto const &grad = std::get<0>(grad_array);
          size_t startN0 = grad.index_bases()[0];
          size_t endN0 = startN0 + grad.shape()[0];
          size_t N1 = grad.shape()[1];
          size_t N2 = grad.shape()[2];

          ghosts.clear_ghosts();
          level.clear_cache();
          array::fill(ag_array, 0);

#  pragma omp parallel for collapse(3)
          for (size_t i = startN0; i < endN0; i++) {
            for (size_t j = 0; j < N1; j++) {
              for (size_t k = 0; k < N2; k++) {
                level.template push_ag_density_level<numLevel - 1>(
                    grad[i][j][k], ag_array, i, j, k);
              }
            }
          }
          level.ag_buildLevels(ghosts, ag_array);
          ghosts.synchronize_ag(ag_array);

          return lowerBias.apply_adjoint_gradient(
              array, std::make_tuple(std::cref(ag_array)));
        }
      };
    }; // namespace detail_downgrader

    using detail_downgrader::DegradeGenerator;
    /// Import the Noop class into LibLSS::bias
    using detail_downgrader::Downgrader;

  } // namespace bias

} // namespace LibLSS

#endif
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2019-2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
