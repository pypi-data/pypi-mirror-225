/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/fused_assign.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_FUSED_ASSIGNMENT_HPP
#define __LIBLSS_FUSED_ASSIGNMENT_HPP

#include <iostream>
#include <boost/type_traits/has_trivial_constructor.hpp>
#include "libLSS/tools/console.hpp"

// When we can get rid of AssignFunctor
//#include "libLSS/tools/phoenix_vars.hpp"
//#include <boost/phoenix/operator.hpp>

namespace LibLSS {

    namespace FUSE_details {
      template<std::size_t N, typename BiFunctor, bool parallel>
      struct OperatorAssignment {};

      template<std::size_t N, typename BiFunctor>
      struct OperatorAssignment<N,BiFunctor,false> {
        template<typename A, typename B>
        static inline void apply(BiFunctor f, A&& a, const B& b) {
          std::size_t s = a.index_bases()[0], e = a.shape()[0];
          for (std::size_t i = s; i < s+e; i++) {
            OperatorAssignment<N-1,BiFunctor,false> op;
            op.apply(f, a[i], b[i]);
          }
        }
      };


      template<typename BiFunctor>
      struct OperatorAssignment<3,BiFunctor,false> {
        template<typename A, typename B>
        static inline void apply(BiFunctor f, A&& a, const B& b) {
          auto ib = a.index_bases();
          auto sh = a.shape();
          std::size_t s0 = ib[0], e0 = s0+sh[0];
          std::size_t s1 = ib[1], e1 = s1+sh[1];
          std::size_t s2 = ib[2], e2 = s2+sh[2];
          boost::array<ssize_t, 3> i;
          for (i[0] = s0; i[0] < e0; i[0]++) {
            for (i[1] = s1; i[1] < e1; i[1]++) {
              for (i[2] = s2; i[2] < e2; i[2]++) {
                f(a(i), b(i));
              }
            }
          }
        }
      };

      template<std::size_t N, typename BiFunctor>
      struct OperatorAssignment<N,BiFunctor,true> {
        template<typename A, typename B>
        static inline void apply(BiFunctor f, A&& a, const B& b) {
          std::size_t s = a.index_bases()[0], e = a.shape()[0];
          typename boost::remove_reference<A>::type *a_ptr = &a;
          const B *b_ptr = &b;

#pragma omp parallel for schedule(static)
          for (std::size_t i = s; i < s+e; i++) {
            OperatorAssignment<N-1,BiFunctor,false> op;
            op.apply(f, (*a_ptr)[i], (*b_ptr)[i]);
          }
        }
      };


      template<typename BiFunctor>
      struct OperatorAssignment<3,BiFunctor,true> {
        template<typename A, typename B>
        static inline void apply(BiFunctor f, A&& a, const B& b) {
          auto ib = a.index_bases();
          auto sh = a.shape();
          std::size_t s0 = ib[0], e0 = s0+sh[0];
          std::size_t s1 = ib[1], e1 = s1+sh[1];
          std::size_t s2 = ib[2], e2 = s2+sh[2];
//          Console::instance().print<LOG_DEBUG>("Using optimized 3-loop collapsed omp");
          Console::instance().format<LOG_DEBUG>("Using optimized 3-loop collapsed omp, %dx%dx%d -- %dx%dx%d", s0,s1,s2,e0,e1,e2);

#pragma omp parallel for collapse(3)
          for (size_t i = s0; i < e0; i++) {
            for (size_t j = s1; j < e1; j++) {
              {
/*                boost::array<ssize_t, 3> idx;
                idx[0] = i;
                idx[1] = j;

                for (idx[2] = s2; idx[2] < e2; idx[2]++) {
                  f( a(idx), b(idx));
                }
		*/
		      for (size_t k = s2; k < e2; k++) {
			      f(a[i][j][k], b[i][j][k]);
		      }
            }
          }
        }
      }
      };

      template<typename BiFunctor>
      struct OperatorAssignment<2,BiFunctor,true> {
        template<typename A, typename B>
        static inline void apply(BiFunctor f, A&& a, const B& b) {
          std::size_t s0 = a.index_bases()[0], e0 = a.shape()[0];
          std::size_t s1 = a.index_bases()[1], e1 = a.shape()[1];

#pragma omp parallel for collapse(1) schedule(static)
          for (std::size_t i = s0; i < s0+e0; i++) {
            // Factorize memory access for the last index.
            auto stripe_a = a[i];
            auto stripe_b = b[i];
            for (std::size_t j = s1; j < s1+e1; j++) {
              f( a[i][j], b[i][j]);
            }
          }
        }
      };

      template<typename BiFunctor>
      struct OperatorAssignment<0, BiFunctor, false> {
        template<typename A, typename B>
        static inline void apply(BiFunctor f, A& a, const B& b) {
          f(a,b);
        }
      };

      template<typename BiFunctor>
      struct OperatorAssignment<0, BiFunctor, true> {
        template<typename A, typename B>
        static inline void apply(BiFunctor f, A& a, const B& b) {
          f(a,b);
        }
      };

      struct AssignFunctor {
        template<typename T0,typename T1>
        inline void operator()(T0& a, const T1& b) {
          a = b;
        }
      };


      template<typename OutArray, typename BiFunctor, typename InArray>
      inline void apply_array(BiFunctor f, OutArray A, const InArray& B, bool openmp = true) {
        typedef typename boost::remove_reference<OutArray>::type PureArray;
        if (openmp) {
          OperatorAssignment<PureArray::dimensionality,BiFunctor,true> op;
          op.template apply(f, A, B);
        } else {
          OperatorAssignment<PureArray::dimensionality,BiFunctor,false> op;
          op.template apply(f, A, B);
        }
      }

      template<typename OutArray, typename InArray>
      inline void copy_array_rv(OutArray A, const InArray& B, bool openmp=true) {
        // GCC is not yet sufficiently clever for that one. The code is suboptimal (test_fused_array timing)
        //        auto assigner = (boost::phoenix::ref(_p1)=boost::phoenix::cref(_p2));
        AssignFunctor assigner;
        apply_array<OutArray, decltype(assigner), InArray>(assigner, A, B, openmp);
      }

      template<typename OutArray, typename InArray>
      inline void copy_array(OutArray& A, const InArray& B, bool openmp=true) {
         copy_array_rv<OutArray&>(A, B, openmp);
      }

    }

    using FUSE_details::apply_array;
    using FUSE_details::copy_array;
    using FUSE_details::copy_array_rv;

};

#endif
