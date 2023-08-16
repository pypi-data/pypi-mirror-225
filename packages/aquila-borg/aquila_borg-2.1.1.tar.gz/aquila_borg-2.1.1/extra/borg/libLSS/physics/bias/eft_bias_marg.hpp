/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/physics/bias/eft_bias_marg.hpp
    Copyright (C) 2019-2021 Fabian Schmidt <fabians@mpa-garching.mpg.de>
    Copyright (C) 2019-2021 Martin Reinecke <martin@mpa-garching.mpg.de>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

/*
       Key features:
       - derives from EFTBias which implements bias fields
           \delta, \delta^2, (K_ij)^2, \laplace\delta
       - all fields are returned in real space AFTER sharp-k filter (unlike EFTBias)
       - uses same namespace detail_EFTBias
       - version to be bundled with marginalized EFT likelihood; returns fields
           individually, and takes corresponding gradients in adjoint
       - although implemented differently, Gaussian priors on bias parameters
         can still be set using "bias_prior_mean", "bias_prior_sigma" (in
         this case, prior is implemented by EFTMargLikelihood)

    This program is free software; you can redistribute it and/or modify it
    under the terms of either the CeCILL license or the GNU General Public
    license, as included with the software package.

    The text of the license is located in Licence_CeCILL_V2.1-en.txt
    and GPL.txt in the root directory of the source package.

*/
#ifndef __LIBLSS_PHYSICS_EFT_BIAS_MARG_HPP
#  define __LIBLSS_PHYSICS_EFT_BIAS_MARG_HPP

// This header provides the implementation of the LSS bias model to second order PT.

#  include <cmath>
#  include "libLSS/tools/fused_array.hpp"
#  include <tuple>
#  include "libLSS/tools/phoenix_vars.hpp"
#  include <boost/phoenix/operator.hpp>
#  include <boost/phoenix/stl/cmath.hpp>
#  include "libLSS/tools/tuple_helper.hpp"
#  include "libLSS/physics/bias/base.hpp"
#  include "libLSS/tools/fftw_allocator.hpp"
#  include "libLSS/samplers/core/powerspec_tools.hpp"

#  include "eft_bias.hpp"

namespace LibLSS {

  namespace bias {

    namespace detail_EFTBias {

      namespace ph = std::placeholders;

      using DFT_Manager = FFTW_Manager_3d<double>;
      using U_Array = Uninit_FFTW_Real_Array;
      using U_CArray = Uninit_FFTW_Complex_Array;
      using U_ArrayRef = U_Array::array_type;
      using U_CArrayRef = U_CArray::array_type;

      class EFTBiasMarg : public EFTBias<false> {
      public:
      protected:
        // EFT_kmax parameter: right now, only implemented in marginalized
        //                     likelihood
        double kmax;

        // apply sharp-k cut to field: modes with k > limit are set to zero
        // - also sets to zero \vec k==0 mode -> subtract mean
        // - version that takes real-space field 'in' and returns filtered real-space field
        void
        sharpk_filter_r2r(U_ArrayRef &in, U_CArrayRef &ctmp, double limit) {
          // FFT
          arrs->mgr.execute_r2c(arrs->analysis_plan, in.data(), ctmp.data());

          // sharp-k filter with norm
          double norm = 1.0 / (N0 * N1 * N2);
          sharpk_filter(ctmp, limit, norm);

          // iFFT
          arrs->mgr.execute_c2r(arrs->synthesis_plan, ctmp.data(), in.data());
        }

      public:
        // This adaptor transforms an unselected galaxy density (with appropriate
        // auxiliary arrays) to a selected array. It must be a functor accepting two
        // parameters: a selection virtual array and a bias density virtual array.
        // - SimpleAdaptor multiplies first returned field of compute_density with mask/selection array
        //   leaving other return values untouched
        selection::SimpleAdaptor selection_adaptor;

        EFTBiasMarg(LikelihoodInfo const &info = LikelihoodInfo())
            : EFTBias(info) {
          // get kmax
          kmax = Likelihood::query<double>(info, "EFT_kmax");
          if (!(kmax > 0. && kmax < EFT_Lambda))
            kmax = EFT_Lambda;

          ConsoleContext<LOG_DEBUG> ctx("EFTBiasMarg constructor");
          ctx.format("Lambda = %.3f, kmax = %.3f", EFT_Lambda, kmax);
        }

        template <typename Array>
        inline bool check_bias_constraints(Array &&params) {
          // enforce sigma0 within parameter limits
          return (params[5] < sigma0max && params[5] > sigma0min);
        }

        // fill bias fields in 'arrs' (base class) and apply sharp-k filter
        void prepare_bias_model_arrays(const U_ArrayRef &delta) {
          // base class preparation
          EFTBias::prepare_bias_model_arrays(delta);

          // now apply sharp-k filters
          // (sharp-k filtered density already present in arrs->deltaLambda)
          myarr<U_CArray> ctmp(
              arrs->mgr.extents_complex(), arrs->mgr.allocator_complex);

          // - also sharp-k filter delta here, since we allow for kmax != Lambda
          sharpk_filter_r2r(arrs->deltaLambda.ref, ctmp.ref, kmax);

          sharpk_filter_r2r(arrs->delta_sqr.ref, ctmp.ref, kmax);
          sharpk_filter_r2r(arrs->tidal_sqr.ref, ctmp.ref, kmax);
          sharpk_filter_r2r(arrs->laplace_delta.ref, ctmp.ref, kmax);
        }

        // Note: fwd_model and final_density arrays cannot be stored in this step. But
        // they can be used.
        // -- essentially copied from EFTbias (note that prepare_bias_model_arrays is overloaded)
        // -- should think about removing some of the code duplication here
        template <
            class ForwardModel, typename FinalDensityArray,
            typename BiasParameters, typename MetaSelect = NoSelector>
        inline void prepare(
            ForwardModel &fwd_model, const FinalDensityArray &final_density,
            double const _nmean, const BiasParameters &params,
            bool density_changed, MetaSelect _select = MetaSelect()) {
          ConsoleContext<LOG_DEBUG> ctx("EFTBiasMarg preparation");

          // allocate bias fields
          if (arrs == nullptr)
            arrs.reset(new Arrs(
                *(fwd_model.lo_mgr->getComm()), *(fwd_model.lo_mgr.get())));

          // fill variables
          N0 = arrs->mgr.N0;
          N1 = arrs->mgr.N1;
          N2 = arrs->mgr.N2;
          N2_HC = N2 / 2 + 1;
          startN0 = arrs->mgr.startN0;
          localN0 = arrs->mgr.localN0;
          L0 = fwd_model.get_box_model().L0;
          L1 = fwd_model.get_box_model().L1;
          L2 = fwd_model.get_box_model().L2;
          nmean = params[0];
          b1 = params[1];
          b2 = params[2];
          bk = params[3];
          r2 = params[4];
          sigma_0 = params[5];

          // no need to compute prior, added in EFTLikeMarg

          ctx.format("Got a box %dx%dx%d (%gx%gx%g)", N0, N1, N2, L0, L1, L2);
          if (density_changed) {
            // prepare density squared, Laplace delta, and tidal field squared
            // - note that these fields have nonzero mean, but this is removed in likelihood eft::sharpk_filter
            ctx.print("Prepare the arrays");
            prepare_bias_model_arrays(final_density);

            // compute variance of delta, delta^2, K^2 for checking
            // (note this is now AFTER sharp-k cut)
            double Md = 0., Md2 = 0., MK2 = 0.;
            double Vd = 0., Vd2 = 0., VK2 = 0.;
#  pragma omp parallel for collapse(3) reduction(+ : Md, Md2, MK2, Vd, Vd2, VK2)
            for (size_t n0 = startN0; n0 < startN0 + localN0; n0++)
              for (size_t n1 = 0; n1 < N1; n1++)
                for (size_t n2 = 0; n2 < N2; n2++) {
                  Md += arrs->deltaLambda.ref[n0][n1][n2];
                  Md2 += arrs->delta_sqr.ref[n0][n1][n2];
                  MK2 += arrs->tidal_sqr.ref[n0][n1][n2];
                  Vd += pow(arrs->deltaLambda.ref[n0][n1][n2], 2.);
                  Vd2 += pow(arrs->delta_sqr.ref[n0][n1][n2], 2.);
                  VK2 += pow(arrs->tidal_sqr.ref[n0][n1][n2], 2.);
                }
            double Md_glob = 0., Md2_glob = 0., MK2_glob = 0.;
            arrs->comm.all_reduce_t(&Md, &Md_glob, 1, MPI_SUM);
            arrs->comm.all_reduce_t(&Md2, &Md2_glob, 1, MPI_SUM);
            arrs->comm.all_reduce_t(&MK2, &MK2_glob, 1, MPI_SUM);
            Md_glob /= double(N0 * N1 * N2);
            Md2_glob /= double(N0 * N1 * N2);
            MK2_glob /= double(N0 * N1 * N2);
            double Vd_glob = 0., Vd2_glob = 0., VK2_glob = 0.;
            arrs->comm.all_reduce_t(&Vd, &Vd_glob, 1, MPI_SUM);
            arrs->comm.all_reduce_t(&Vd2, &Vd2_glob, 1, MPI_SUM);
            arrs->comm.all_reduce_t(&VK2, &VK2_glob, 1, MPI_SUM);
            Vd_glob = Vd_glob / double(N0 * N1 * N2) - Md_glob * Md_glob;
            Vd2_glob = Vd2_glob / double(N0 * N1 * N2) - Md2_glob * Md2_glob;
            VK2_glob = VK2_glob / double(N0 * N1 * N2) - MK2_glob * MK2_glob;
            ctx.format(
                "Mean of delta (AFTER), delta^2, K^2 (AFTER Eulerian "
                "sharp-k cut): %.5e, %.5e, %.5e (Lambda = %.2e)\n",
                Md_glob, Md2_glob, MK2_glob, EFT_Lambda);
            ctx.format(
                "Variance of delta (AFTER), delta^2, K^2 (AFTER Eulerian "
                "sharp-k cut): %.5e, %.5e, %.5e (Lambda = %.2e)\n",
                Vd_glob, Vd2_glob, VK2_glob, EFT_Lambda);
          }

          ctx.print("Done preparation");
        }

        // This function returns an array-like array. That array
        // depends on the existence of the final density array.
        // The return type is quite complex. Let the compiler decide.
        // The return tuple contains sigma field as well as a vector with
        //   bias fields tuple<0> = sigma, tuple<1> = biasfieldvector, with
        // 0: delta
        // 1: delta^2
        // 2: K^2
        // 3: lapl delta
        // 4: sigma
        // -- all in real space after sharp-k filter
        // -- worry about mask later
        // -- sigma0 is first element in tuple, as that is what selection is applied to
        template <typename FinalDensityArray>
        inline auto compute_density(const FinalDensityArray &array) const {
          std::vector<U_ArrayRef> bias;
          bias.push_back(arrs->deltaLambda.ref);
          bias.push_back(arrs->delta_sqr.ref);
          bias.push_back(arrs->tidal_sqr.ref);
          bias.push_back(arrs->laplace_delta.ref);

          // return the tuple of bias fields as well as sigma0
          return std::make_tuple(
              *LibLSS::constant<double, 3>(
                  sigma_0, arrs->mgr.extents_real_strict()),
              bias);
        }

        // This function returns an array-like array. That array
        // depends on the existence of the final density array and the gradient likelihood array.
        // That is the job of the caller to ensure that temporary variables are not cleared
        // before the final use.
        // The return type is quite complex. Let the compiler decide.
        // L(b_0(delta, p), b_1(delta, p), ..., b_n(delta, p))
        // Now we take a tuple of gradient and collapse this to a gradient of delta.
        //
        // grad_array contains vector of gradients of the (marginalized) likelihood
        // w.r.t the bias fields, see below
        template <
            typename FinalDensityArray, typename TupleGradientLikelihoodArray>
        auto apply_adjoint_gradient(
            const FinalDensityArray &final_density,
            TupleGradientLikelihoodArray grad_array) {
          ConsoleContext<LOG_DEBUG> ctx("EFTBiasMarg gradient computation");

          auto &grad = std::get<1>(grad_array);
          // grad is vector which contains
          // 0: dlogL/ddelta
          // 1: dlogL/ddelta^2
          // 2: dlogL/dK^2
          // 3: dlogL/d(lapl delta)
          // -- the last two we need for integration by parts

          ctx.print("Transfer the input gradient");
          // - copy of the first two fields only necessary if kmax != EFT_Lambda...
          auto dlogL_dd = grad[0];
          auto dlogL_ddelta2 = grad[1];
          // - actually, copies of the above two are not needed
          // myarr<U_Array> dlogL_dd(arrs->mgr.extents_real(),
          // 			  arrs->mgr.allocator_real);
          // myarr<U_Array> dlogL_ddelta2(arrs->mgr.extents_real(),
          // 			       arrs->mgr.allocator_real);
          // LibLSS::copy_array_rv(
          //     array::slice_array((dlogL_dd.ref), arrs->mgr.strict_range()),
          //     grad[0]);
          // LibLSS::copy_array_rv(
          //     array::slice_array((dlogL_ddelta2.ref), arrs->mgr.strict_range()),
          //     grad[1]);

          myarr<U_Array> dlogL_dK2(
              arrs->mgr.extents_real(), arrs->mgr.allocator_real);
          myarr<U_Array> dlogL_dlapl(
              arrs->mgr.extents_real(), arrs->mgr.allocator_real);
          LibLSS::copy_array_rv(
              array::slice_array((dlogL_dK2.ref), arrs->mgr.strict_range()),
              grad[2]);
          LibLSS::copy_array_rv(
              array::slice_array((dlogL_dlapl.ref), arrs->mgr.strict_range()),
              grad[3]);
          ctx.print("Data backed up");

          myarr<U_CArray> ctmp(
              arrs->mgr.extents_complex(), arrs->mgr.allocator_complex);

          // // sharp-k filter gradients at kmax
          // // - formally necessary if kmax != EFT_Lambda; however, since
          // //   dlogL/dO only has support for k < kmax, it is not necessary
          // //   in practice
          // if (kmax != EFT_Lambda)  {
          //   sharpk_filter_r2r(dlogL_dd.ref, ctmp.ref, kmax);
          //   sharpk_filter_r2r(dlogL_ddelta2.ref, ctmp.ref, kmax);
          //   sharpk_filter_r2r(dlogL_dK2.ref, ctmp.ref, kmax);
          //   sharpk_filter_r2r(dlogL_dlapl.ref, ctmp.ref, kmax);
          // }

          myarr<U_Array> tmp(
              arrs->mgr.extents_real(), arrs->mgr.allocator_real),
              // this will contain functional derivative of K^2 term:
              dK2(arrs->mgr.extents_real(), arrs->mgr.allocator_real),
              // this will contain functional derivative of \nabla^2\delta term:
              dlaplace_delta(
                  arrs->mgr.extents_real(), arrs->mgr.allocator_real);

          // Functional derivatives of fields under derivative operators are
          // treated through integration by parts. See pt_borg/notes/borg_implementation_notes.

          // derivative of K^2 term:
          // compute K^ij \Del_ij ( dlogL_dK2 K^ij )
          // - component by component and sum up
          // - notice the factor of 2 in front of off-diagonal terms
          get_density_derivative_array3d_dtidal(
              tmp.ref, dlogL_dK2.ref, arrs->tidal_01.ref, 0, 1);
          fwrap(dK2.ref) = 2 * fwrap(tmp.ref);
          get_density_derivative_array3d_dtidal(
              tmp.ref, dlogL_dK2.ref, arrs->tidal_02.ref, 0, 2);
          fwrap(dK2.ref) = fwrap(dK2.ref) + 2 * fwrap(tmp.ref);
          get_density_derivative_array3d_dtidal(
              tmp.ref, dlogL_dK2.ref, arrs->tidal_12.ref, 1, 2);
          fwrap(dK2.ref) = fwrap(dK2.ref) + 2 * fwrap(tmp.ref);
          get_density_derivative_array3d_dtidal(
              tmp.ref, dlogL_dK2.ref, arrs->tidal_00.ref, 0, 0);
          fwrap(dK2.ref) = fwrap(dK2.ref) + fwrap(tmp.ref);
          get_density_derivative_array3d_dtidal(
              tmp.ref, dlogL_dK2.ref, arrs->tidal_11.ref, 1, 1);
          fwrap(dK2.ref) = fwrap(dK2.ref) + fwrap(tmp.ref);
          get_density_derivative_array3d_dtidal(
              tmp.ref, dlogL_dK2.ref, arrs->tidal_22.ref, 2, 2);
          fwrap(dK2.ref) = fwrap(dK2.ref) + fwrap(tmp.ref);

          // derivative of \nabla^2 \delta: take Laplacian of dlogL_drho times (-1)^2
          get_density_derivative_array3d_dlaplace(
              dlaplace_delta.ref, dlogL_dlapl.ref);

          // we also need delta_Lambda (rather than deltaLambda which is filtered at k_max...)
          // - get here from final_density
          fwrap(tmp.ref) = fwrap(final_density);
          sharpk_filter_r2r(tmp.ref, ctmp.ref, EFT_Lambda);

          // now assemble total adjoint gradient
          ctx.print("Computing the gradient.");
#  pragma omp parallel for collapse(3)
          for (size_t n0 = startN0; n0 < startN0 + localN0; n0++)
            for (size_t n1 = 0; n1 < N1; n1++)
              for (size_t n2 = 0; n2 < N2; n2++) {
                arrs->dlogL_ddelta.ref[n0][n1][n2] =
                    dlogL_dd[n0][n1][n2]
                    // factor of 2 for quadratic terms from product rule
                    // - note that we use tmp = delta_Lambda for delta^2
                    + 2. * dlogL_ddelta2[n0][n1][n2] * tmp.ref[n0][n1][n2] +
                    2. * dK2.ref[n0][n1][n2] + dlaplace_delta.ref[n0][n1][n2];
              }

          // finally, apply sharp-k filter to dlogL_ddelta at EFT_Lambda
          sharpk_filter_r2r(arrs->dlogL_ddelta.ref, ctmp.ref, EFT_Lambda);

          return std::make_tuple(std::ref(arrs->dlogL_ddelta.ref));
        }
      }; // class EFTBiasMarg

    } // namespace detail_EFTBias

    using detail_EFTBias::EFTBiasMarg;

  } // namespace bias

} // namespace LibLSS

#endif
// ARES TAG: authors_num = 2
// ARES TAG: name(0) = Fabian Schmidt
// ARES TAG: year(0) = 2019-2021
// ARES TAG: email(0) = fabians@mpa-garching.mpg.de
// ARES TAG: name(1) = Martin Reinecke
// ARES TAG: year(1) = 2019-2021
// ARES TAG: email(1) = martin@mpa-garching.mpg.de
