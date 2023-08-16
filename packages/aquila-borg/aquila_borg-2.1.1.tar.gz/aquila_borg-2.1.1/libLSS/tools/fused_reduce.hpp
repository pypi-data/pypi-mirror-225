/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/fused_reduce.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_FUSED_REDUCTION_HPP
#define __LIBLSS_FUSED_REDUCTION_HPP

#include <type_traits>
#include <boost/type_traits/has_trivial_constructor.hpp>

// This include file defines the reduction operation on
// virtual arrays as defined by fused_array.hpp
// The goal is to be able to combine virtual arrays and
// apply parallel reduction operation on it.
// A straightforward example is given in test_fuse_reduce.cpp
//
// r = LibLSS::reduce_sum(
//      b_fused_idx (
//          [](int i, int j)->int {return i*j;},
//          extents[N][M] )
//     );
//
// Which computes a \sum_{i=0,j=0}^{i=N-1,j=M-1} i*j, with openmp.
// However arrays can be folded in that.
//
// r = LibLSS::reduce_sum(
//      b_fused_idx (
//          [](int i, int j)->int {return i*j;},
//          extents[N][M] )
//     );

//

namespace LibLSS {

    namespace FUSE_details {
      template<std::size_t N, typename T, bool parallel>
      struct OperatorReduction {};


      // ======================
      // MAX OPERATOR REDUCTION
      template<std::size_t N, typename T, bool parallel>
      struct MaxOperatorReduction {};

      template<std::size_t N,typename T>
      struct MaxOperatorReduction<N,T,false> {
        template<typename A, typename M>
        static T reduce(const A& a, const M& m) {
          std::size_t s = a.index_bases()[0], e = a.shape()[0];
          T r = -std::numeric_limits<T>::infinity();
          for (std::size_t i = s; i < s+e; i++) {
            MaxOperatorReduction<N-1,T,false> op;
            r = std::max(r, op.reduce(a[i], m[i]));
          }
          return r;
        }
      };

      template<std::size_t N,typename T>
      struct MaxOperatorReduction<N,T,true> {
        template<typename A, typename M>
        static T reduce(const A& a, const M& m) {
          std::size_t s = a.index_bases()[0], e = a.shape()[0];
          typename boost::remove_reference<A>::type const *a_ptr = &a;
          T r = -std::numeric_limits<T>::infinity();

#pragma omp parallel for reduction(max:r)
          for (std::size_t i = s; i < s+e; i++) {
            MaxOperatorReduction<N-1,T,false> op;
            r = std::max(r, op.reduce((*a_ptr)[i], m[i]));
          }
          return r;
        }
      };

      template<typename T>
      struct MaxOperatorReduction<1,T,false> {
        template<typename A,typename M>
        static T reduce(const A& a, const M& m) {
          std::size_t s = a.index_bases()[0], e = a.shape()[0];
          T r = -std::numeric_limits<T>::infinity();
          for (std::size_t i = s; i < s+e; i++) {
            if (m[i])
              r = std::max(r, T(a[i]));
          }
          return r;
        }
      };


      template<typename T>
      struct MaxOperatorReduction<1,T,true> {
        template<typename A, typename M>
        static T reduce(const A& a, const M& m) {
          std::size_t s = a.index_bases()[0], e = a.shape()[0];
          typename boost::remove_reference<A>::type const *a_ptr = &a;
          T r = -std::numeric_limits<T>::infinity();

#pragma omp parallel for reduction(max:r)
          for (std::size_t i = s; i < s+e; i++) {
            if (m[i])
              r = std::max(r, T((*a_ptr)[i]));
          }
          return r;
        }
      };


      template<typename T, bool parallel>
      struct MaxOperatorReduction<0,T,parallel> {
        template<typename A>
        static T reduce(const A& a) {
          return a;
        }
      };

      // ===============================
      //
      // ======================
      // MIN OPERATOR REDUCTION
      template<std::size_t N, typename T, bool parallel>
      struct MinOperatorReduction {};

      template<std::size_t N,typename T>
      struct MinOperatorReduction<N,T,false> {
        template<typename A, typename M>
        static T reduce(const A& a, const M& m) {
          std::size_t s = a.index_bases()[0], e = a.shape()[0];
          T r = std::numeric_limits<T>::infinity();
          for (std::size_t i = s; i < s+e; i++) {
            MinOperatorReduction<N-1,T,false> op;
            r = std::min(r, op.reduce(a[i], m[i]));
          }
          return r;
        }
      };

      template<std::size_t N,typename T>
      struct MinOperatorReduction<N,T,true> {
        template<typename A, typename M>
        static T reduce(const A& a, const M& m) {
          std::size_t s = a.index_bases()[0], e = a.shape()[0];
          typename boost::remove_reference<A>::type const *a_ptr = &a;
          T r = std::numeric_limits<T>::infinity();

#pragma omp parallel for reduction(min:r)
          for (std::size_t i = s; i < s+e; i++) {
            MinOperatorReduction<N-1,T,false> op;
            r = std::min(r, op.reduce((*a_ptr)[i], m[i]));
          }
          return r;
        }
      };

      template<typename T>
      struct MinOperatorReduction<1,T,false> {
        template<typename A,typename M>
        static T reduce(const A& a, const M& m) {
          std::size_t s = a.index_bases()[0], e = a.shape()[0];
          T r = std::numeric_limits<T>::infinity();
          for (std::size_t i = s; i < s+e; i++) {
            if (m[i])
              r = std::min(r, T(a[i]));
          }
          return r;
        }
      };


      template<typename T>
      struct MinOperatorReduction<1,T,true> {
        template<typename A, typename M>
        static T reduce(const A& a, const M& m) {
          std::size_t s = a.index_bases()[0], e = a.shape()[0];
          typename boost::remove_reference<A>::type const *a_ptr = &a;
          T r = std::numeric_limits<T>::infinity();

#pragma omp parallel for reduction(min:r)
          for (std::size_t i = s; i < s+e; i++) {
            if (m[i])
              r = std::min(r, T((*a_ptr)[i]));
          }
          return r;
        }
      };


      template<typename T, bool parallel>
      struct MinOperatorReduction<0,T,parallel> {
        template<typename A>
        static T reduce(const A& a) {
          return a;
        }
      };

      // ===============================

      template<std::size_t N,typename T>
      struct OperatorReduction<N,T,false> {
        template<typename A, typename M>
        static T reduce(const A& a, const M& m) {
          std::size_t s = a.index_bases()[0], e = a.shape()[0];
          T r = 0;
          for (std::size_t i = s; i < s+e; i++) {
            OperatorReduction<N-1,T,false> op;
            r += op.reduce(a[i], m[i]);
          }
          return r;
        }
      };

      template<std::size_t N,typename T>
      struct OperatorReduction<N,T,true> {
        template<typename A, typename M>
        static T reduce(const A& a, const M& m) {
          std::size_t s = a.index_bases()[0], e = a.shape()[0];
          typename boost::remove_reference<A>::type const *a_ptr = &a;
          T r = 0;

#pragma omp parallel for reduction(+:r)
          for (std::size_t i = s; i < s+e; i++) {
            OperatorReduction<N-1,T,false> op;
            r += op.reduce((*a_ptr)[i], m[i]);
          }
          return r;
        }
      };


      template<typename T>
      struct OperatorReduction<1,T,false> {
        template<typename A,typename M>
        static T reduce(const A& a, const M& m) {
          std::size_t s = a.index_bases()[0], e = a.shape()[0];
          T r = 0;
          for (std::size_t i = s; i < s+e; i++) {
            if (m[i])
              r += a[i];
          }
          return r;
        }
      };


      template<typename T>
      struct OperatorReduction<1,T,true> {
        template<typename A, typename M>
        static T reduce(const A& a, const M& m) {
          std::size_t s = a.index_bases()[0], e = a.shape()[0];
          typename boost::remove_reference<A>::type const *a_ptr = &a;
          T r = 0;

#pragma omp parallel for reduction(+:r)
          for (std::size_t i = s; i < s+e; i++) {
            if (m[i])
              r += (*a_ptr)[i];
          }
          return r;
        }
      };


      template<typename T>
      struct OperatorReduction<0,T,false> {
        template<typename A>
        static T reduce(const A& a) {
          return a;
        }
      };

      template<typename T>
      struct OperatorReduction<0,T,true> {
        template<typename A>
        static T reduce(const A& a) {
          return a;
        }
      };



      template<typename T,typename InArray,typename MaskArray>
      typename std::enable_if<!std::is_same<MaskArray,bool>::value, T>::type
      reduce_min(const InArray& A, const MaskArray& mask, bool openmp=true) {
        typedef typename boost::remove_reference<InArray>::type PureArray;
        if (openmp) {
          MinOperatorReduction<InArray::dimensionality,T,true> op;
          return op.template reduce(A, mask);
        } else {
          MinOperatorReduction<InArray::dimensionality,T,false> op;
          return op.template reduce(A, mask);
        }
      }

      template<typename T,typename InArray,typename MaskArray>
      typename std::enable_if<!std::is_same<MaskArray,bool>::value, T>::type
      reduce_max(const InArray& A, const MaskArray& mask, bool openmp=true) {
        typedef typename boost::remove_reference<InArray>::type PureArray;
        if (openmp) {
          MaxOperatorReduction<InArray::dimensionality,T,true> op;
          return op.template reduce(A, mask);
        } else {
          MaxOperatorReduction<InArray::dimensionality,T,false> op;
          return op.template reduce(A, mask);
        }
      }

      template<typename T,typename InArray,typename MaskArray>
      typename std::enable_if<!std::is_same<MaskArray,bool>::value, T>::type
      reduce_sum(const InArray& A, const MaskArray& mask, bool openmp=true) {
        typedef typename boost::remove_reference<InArray>::type PureArray;
        if (openmp) {
          OperatorReduction<InArray::dimensionality,T,true> op;
          return op.template reduce(A, mask);
        } else {
          OperatorReduction<InArray::dimensionality,T,false> op;
          return op.template reduce(A, mask);
        }
      }

      struct noMaskDummy {
        template<typename... Args>
        bool operator()(Args&&... t) const {
          return true;
        }
      };

      template<typename T,typename InArray>
      T reduce_sum(const InArray& A, bool openmp=true) {
	static_assert(DetectShaped<InArray>::Shaped, "Array has no shape");
        return reduce_sum<T>(A, b_va_fused<bool,InArray::dimensionality>(noMaskDummy()), openmp);
      }

      template<typename T,typename InArray>
      T reduce_min(const InArray& A, bool openmp=true) {
	static_assert(DetectShaped<InArray>::Shaped, "Array has no shape");
        return reduce_min<T>(A, b_va_fused<bool,InArray::dimensionality>(noMaskDummy()), openmp);
      }

      template<typename T,typename InArray>
      T reduce_max(const InArray& A, bool openmp=true) {
	static_assert(DetectShaped<InArray>::Shaped, "Array has no shape");
        return reduce_max<T>(A, b_va_fused<bool,InArray::dimensionality>(noMaskDummy()), openmp);
      }


    }

    using FUSE_details::reduce_sum;
    using FUSE_details::reduce_min;
    using FUSE_details::reduce_max;
};

#endif
