/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/fused_masked_assign.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_FUSED_MASKED_ASSIGNMENT_HPP
#define __LIBLSS_FUSED_MASKED_ASSIGNMENT_HPP

#include <boost/type_traits/has_trivial_constructor.hpp>

// When we can get rid of AssignFunctor
//#include "libLSS/tools/phoenix_vars.hpp"
//#include <boost/phoenix/operator.hpp>

namespace LibLSS {

    namespace FUSE_details {
      template<std::size_t N, typename BiFunctor, bool parallel>
      struct MaskedOperatorAssignment {};

      template<std::size_t N, typename BiFunctor>
      struct MaskedOperatorAssignment<N,BiFunctor,false> {
        template<typename A, typename B, typename C, typename M>
        static inline void apply(BiFunctor f, A a, const B& b, const C& c, const M& m) {
          std::size_t s = a.index_bases()[0], e = a.shape()[0];
          for (std::size_t i = s; i < s+e; i++) {
            MaskedOperatorAssignment<N-1,BiFunctor,false> op;
            op.apply(f, a[i], b[i], c[i], m[i]);
          }
        }
      };

      template<std::size_t N, typename BiFunctor>
      struct MaskedOperatorAssignment<N,BiFunctor,true> {
        template<typename A, typename B, typename C, typename M>
        static inline void apply(BiFunctor f, A&& a, const B& b, const C& c, const M& m) {
          std::size_t s = a.index_bases()[0], e = a.shape()[0];
          typename boost::remove_reference<A>::type *a_ptr = &a;
          const B *b_ptr = &b;
          const M *m_ptr = &m;
          const C *c_ptr = &c;

#pragma omp parallel for schedule(static)
          for (std::size_t i = s; i < s+e; i++) {
            MaskedOperatorAssignment<N-1,BiFunctor,false> op;
            op.apply(f, (*a_ptr)[i], (*b_ptr)[i], (*c_ptr)[i], (*m_ptr)[i]);
          }
        }
      };


      template<typename BiFunctor>
      struct MaskedOperatorAssignment<3,BiFunctor,true> {
        template<typename A, typename B, typename C, typename M>
        static inline void apply(BiFunctor f, A&& a, const B& b, const C& c, const M& m) {
          std::size_t s0 = a.index_bases()[0], e0 = a.shape()[0];
          std::size_t s1 = a.index_bases()[1], e1 = a.shape()[1];
          std::size_t s2 = a.index_bases()[2], e2 = a.shape()[2];

#pragma omp parallel for collapse(2) schedule(static)
          for (std::size_t i = s0; i < s0+e0; i++) {
            for (std::size_t j = s1; j < s1+e1; j++) {
              // Factorize memory access for the last index.
              // This does not work in all cases. It would
              // be necessary to exchange loops to order by
              // order of memory access.
              // This also means we cannot collapse the 3-loops
              auto stripe_a = a[i][j];
              auto stripe_b = b[i][j];
              auto stripe_m = m[i][j];
              auto stripe_c = c[i][j];
              for (std::size_t k = s2; k < s2+e2; k++) {
                if (stripe_m[k])
                  f( stripe_a[k], stripe_b[k] );
                else
                  f( stripe_a[k], stripe_c[k] );
              }
            }
          }
        }
      };

      template<typename BiFunctor>
      struct MaskedOperatorAssignment<2,BiFunctor,true> {
        template<typename A, typename B, typename C, typename M>
        static inline void apply(BiFunctor f, A&& a, const B& b, const C& c, const M& m) {
          std::size_t s0 = a.index_bases()[0], e0 = a.shape()[0];
          std::size_t s1 = a.index_bases()[1], e1 = a.shape()[1];

#pragma omp parallel for collapse(1) schedule(static)
          for (std::size_t i = s0; i < s0+e0; i++) {
            // Factorize memory access for the last index.
            auto stripe_a = a[i];
            auto stripe_b = b[i];
            for (std::size_t j = s1; j < s1+e1; j++) {
              if (m[i][j])
                f( a[i][j], b[i][j]);
              else
                f( a[i][j], c[i][j]);
            }
          }
        }
      };

      // Explicit specialization for one to avoid the evaluation of b if it is masked
      // that saves an eventual computation for slightly dumber compiler.
      template<typename BiFunctor>
      struct _Sub_1_MaskedOperatorAssignment {
        template<typename A, typename B, typename C, typename M>
        static inline void apply(BiFunctor f, A a, const B& b, const C& c, const M& m) {
            std::size_t s = a.index_bases()[0], e = a.shape()[0];
            for (std::size_t i = s; i < s+e; i++) {
              if (m[i])
                f(a[i], b[i]);
              else
                f(a[i], c[i]);
            }
          }
      };

      template<typename BiFunctor>
      struct MaskedOperatorAssignment<1, BiFunctor, false>: _Sub_1_MaskedOperatorAssignment<BiFunctor> {};
      template<typename BiFunctor>
      struct MaskedOperatorAssignment<1, BiFunctor, true>: _Sub_1_MaskedOperatorAssignment<BiFunctor> {};


      template<typename BiFunctor>
      struct _Sub_0_MaskedOperatorAssignment {
        template<typename A, typename B, typename C, typename M>
        static inline void apply(BiFunctor f, A& a, const B& b, const C& c, const M& m) {
          if (m)
            f(a,b);
          else
            f(a,c);
        }
      };

      template<typename BiFunctor>
      struct MaskedOperatorAssignment<0, BiFunctor, true>:  _Sub_0_MaskedOperatorAssignment<BiFunctor> {};
      template<typename BiFunctor>
      struct MaskedOperatorAssignment<0, BiFunctor, false>:  _Sub_0_MaskedOperatorAssignment<BiFunctor> {};


      struct MaskedAssignFunctor {
        template<typename T0,typename T1>
        inline void operator()(T0& a, const T1& b) {
          a = b;
        }
      };


      template<typename OutArray, typename BiFunctor, typename InArray, typename InArray2, typename MaskArray>
      inline void apply_array_masked(
          BiFunctor f, OutArray&& A, const InArray& B, const InArray2& C,
          const MaskArray& mask, bool openmp = true) {
        typedef typename boost::remove_reference<OutArray>::type PureArray;
        if (openmp) {
          MaskedOperatorAssignment<PureArray::dimensionality,BiFunctor,true> op;
          op.template apply(f, A, B, C, mask);
        } else {
          MaskedOperatorAssignment<PureArray::dimensionality,BiFunctor,false> op;
          op.template apply(f, A, B, C, mask);
        }
      }

      template<typename OutArray, typename InArray, typename InArray2, typename MaskArray>
      inline void copy_array_masked(OutArray&& A, const InArray& B, const InArray2& C,
          const MaskArray& mask, bool openmp=true) {
        MaskedAssignFunctor assigner;
        apply_array_masked(assigner, A, B, C, mask, openmp);
      }

    }

    using FUSE_details::apply_array_masked;
    using FUSE_details::copy_array_masked;

};

#endif
