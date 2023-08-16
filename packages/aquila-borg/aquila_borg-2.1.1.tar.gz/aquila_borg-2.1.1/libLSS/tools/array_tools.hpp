/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/array_tools.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_ARRAY_TOOLS_HPP
#define __LIBLSS_ARRAY_TOOLS_HPP

#include "libLSS/tools/errors.hpp"
#include "libLSS/tools/align_helper.hpp"
#include <CosmoTool/omptl/omptl>
#include <CosmoTool/omptl/omptl_algorithm>
#include <boost/lambda/lambda.hpp>
#include "libLSS/tools/fused_array.hpp"

namespace LibLSS {

    namespace array {
        typedef boost::multi_array_types::extent_range erange;
        typedef boost::multi_array_types::index_range irange;

        template<typename InArray>
        struct EigenMap {
            typedef typename InArray::element T;
            typedef Eigen::Array<T, Eigen::Dynamic, 1> E_Array;
            typedef Eigen::Map<E_Array, Eigen::Unaligned> MapArray;

            static MapArray map(InArray& a) {
              return MapArray(a.data(), a.num_elements());
            }
        };

        template<typename InArray>
        typename EigenMap<InArray>::MapArray eigen_map(InArray& a) {
            return EigenMap<InArray>::map(a);
        }


        template<typename Array>
        void fill(Array& a, typename Array::element val) {
            using boost::lambda::constant;
            typedef typename Array::element VArrayType;

            LibLSS::copy_array(a, b_fused<VArrayType,Array::dimensionality>(constant(val)));
        }

        template<typename Array>
        void density_rescale(Array& a, typename Array::element val) {
            using boost::lambda::_1;
            LibLSS::copy_array(a, b_fused<typename Array::element>(a, _1 / val - 1));//omptl::for_each(a.data(), a.data()+a.num_elements(), _1 / val - 1);
        }

        template<typename InArray, typename OutArray>
        void copyArray3d(OutArray& out, const InArray& in, bool in_padded = false)
        {
            if (!in_padded && (out.shape()[0] < in.shape()[0] ||
                out.shape()[1] < in.shape()[1] ||
                out.shape()[2] < in.shape()[2])) {
                error_helper<ErrorBadState>("Invalid copy shape in copyArray3d");
            }

            LibLSS::copy_array(out, in);
        }

        template<typename InOutArray>
        void scaleArray3d(InOutArray& out, typename InOutArray::element scale)
        {
            using boost::lambda::_1;
            LibLSS::copy_array(out, b_fused<typename InOutArray::element>(out, _1*scale));
        }

        template<typename T, size_t n>
        T product(std::array<T,n> const& d) {
          T a = T(1);
          for (size_t i = 0; i < n; i++) a *= d[i];
          return a;
        }

        template<typename Iterator, typename T = typename std::remove_reference<decltype(*std::declval<Iterator>())>::type>
        T product(Iterator b, Iterator e) {
          T a = T(1);
          while (b != e) {
             a *= *b;
             ++b;
          }
          return a;
        }

        template<typename InOutPlane>
        void scalePlane(InOutPlane plane, typename InOutPlane::element scale)
        {
          const typename InOutPlane::index *base = plane.index_bases();
          const typename InOutPlane::size_type *exts = plane.shape();
          for (long i = base[0]; i < base[0] + exts[0]; i++) {
            for (long j = base[1]; j < base[1] + exts[1]; j++) {
              plane[i][j] *= scale;
            }
          }
        }

        template<typename InOutLine>
        void scaleLine(InOutLine line, typename InOutLine::element scale)
        {
          const typename InOutLine::index *base = line.index_bases();
          const typename InOutLine::size_type *exts = line.shape();
          for (long i = base[0]; i < base[0] + exts[0]; i++) {
             line[i] *= scale;
          }
        }


        template<typename InArray, typename OutArray>
        void scaleAndCopyArray3d_rv(OutArray out, const InArray& in, typename OutArray::element scale)
        {
            using boost::format;
            long N0 = out.shape()[0],
                N1 = out.shape()[1],
                N2 = out.shape()[2];
            Console& cons = Console::instance();

            N0 = std::min(N0,long(in.shape()[0]));
            N1 = std::min(N1,long(in.shape()[1]));
            N2 = std::min(N2,long(in.shape()[2]));

            long s0 = out.index_bases()[0],
              s1 = out.index_bases()[1],
              s2 = out.index_bases()[2];
            long i_s0 = in.index_bases()[0],
              i_s1 = in.index_bases()[1],
              i_s2 = in.index_bases()[2];

            cons.print<LOG_DEBUG>(format("Copying (%d-%d, %d-%d, %d-%d) -> (%d-%d, %d-%d, %d-%d)")
                % i_s0 % (i_s0+N0) % i_s1 % (i_s1+N1) % i_s2 % (i_s2+N2) %
                  s0 % (s0+N0) % s1 % (s1+N1) % s2 % (s2+N2));

#pragma omp parallel for
            for (long n0 = 0; n0 < N0; n0++) {
                typename OutArray::reference out0 = out[s0+n0];
                typename InArray::const_reference in0 = in[i_s0+n0];
                cons.print<LOG_DEBUG>(format("Line %d") % n0);
                for (long n1 = 0; n1 < N1; n1++) {
                    typename OutArray::reference::reference out1 = out0[s1+n1];
                    typename InArray::const_reference::const_reference in1 = in0[i_s1+n1];
                    for (long n2 = 0; n2 < N2; n2++) {
                        out1[s2+n2] = in1[i_s2+n2]*scale;
                    }
                }
            }
            cons.print<LOG_DEBUG>("Done copy");
        }

        template<typename InArray, typename OutArray>
        void scaleAndCopyArray3d(OutArray& out, const InArray& in, typename OutArray::element scale, bool in_padded = false)
        {
            using boost::format;
            size_t N0 = out.shape()[0],
                N1 = out.shape()[1],
                N2 = out.shape()[2];

            if (!in_padded && (N0 < in.shape()[0] ||
                N1 < in.shape()[1] ||
                N2 < in.shape()[2])) {
                error_helper<ErrorBadState>("Invalid copy shape in scaleAndcopyArray3d");
            }
            N0 = std::min(N0,in.shape()[0]);
            N1 = std::min(N1,in.shape()[1]);
            N2 = std::min(N2,in.shape()[2]);

            ssize_t s0 = out.index_bases()[0],
              s1 = out.index_bases()[1],
              s2 = out.index_bases()[2];

            Console::instance().print<LOG_DEBUG>(format("Copying (%d-%d, %d-%d, %d-%d)") % s0 % (s0+N0) % s1 % (s1+N1) % s2 % (s2+N2));

#pragma omp parallel for
            for (size_t n0 = s0; n0 < s0+N0; n0++) {
                auto out_0 = out[n0];
                auto in_0 = in[n0];
                for (size_t n1 = s1; n1 < s1+N1; n1++) {
                    auto out_1 = out_0[n1];
                    auto in_1 = in_0[n1];
                    for (size_t n2 = s2; n2 < s2+N2; n2++) {
                        out_1[n2] = in_1[n2]*scale;
                    }
                }
            }
            Console::instance().print<LOG_DEBUG>("Done copy");
        }

        template<typename T>
        auto generate_slice(T x[6]) {
          typedef boost::multi_array_types::index_range i_range;
          return boost::indices[i_range(x[0], x[1])][i_range(x[2],x[3])][i_range(x[4],x[5])];
        }

        template<typename A, typename RangeList>
        auto slice_array(A&& a, const RangeList& rlist)
          -> decltype(a[rlist])
        {
          auto v = a[rlist];
          typedef typename std::remove_reference<A>::type A_t;
          boost::array<size_t, A_t::dimensionality> ids;
          size_t i = 0 ;

          for (auto v: rlist.ranges_) {
            ids[i] = v.get_start(a.index_bases()[i]);
            i++;
          }
          v.reindex(ids);
          return v;
        }

        namespace details {
          typedef boost::multi_array_types::extent_range range;

          template<size_t Nd>
          struct make_extent {
          template<typename E, typename IB, typename S>
            static inline auto make(E e, IB ib, S s)
            {
              return make_extent<Nd-1>::make(e[range(*ib, *ib+*s)], ib+1, s+1);
            }
          };

          template<>
          struct make_extent<0> {
            template<typename E, typename IB, typename S>
            static inline auto make(E e, IB ib, S s) { return e; }
          };
        }

        namespace star_index_detail {

          template<typename I>
          auto _make_star_indices(I indices, std::integer_sequence<size_t>) {
            return indices;
          }
  
          template<typename I, size_t N0, size_t... N1>
          auto _make_star_indices(I indices, std::integer_sequence<size_t,N0,N1...>) {
            typedef boost::multi_array_types::index_range i_range;

            return _make_star_indices(indices, std::integer_sequence<size_t,N1...>())[i_range()];
          }
  
          template<size_t N, typename I>
          auto make_star_indices(I indices) {
            return _make_star_indices(indices, std::make_integer_sequence<size_t,N>());
          }

        }
        using star_index_detail::make_star_indices;

        template<size_t N, typename IB, typename S, typename E = boost::multi_array_types::extent_gen>
        auto make_extent(IB bases, S shape, E e = E()) {
          return
            details::make_extent<N>::make(
               e, bases, shape
            );
        }

        template<typename... I>
        auto extent(I... i) {
           std::array<size_t, sizeof...(I)> s{i...}; 
           std::array<size_t, sizeof...(I)> b; 
           std::fill(b.begin(), b.end(), 0);
           return make_extent<sizeof...(I)>(b.data(), s.data());
        }

        /**
         * @brief build a new extent object from the dimensions of an existing array-like type.
         *
         * @return an extent
         */
        template<typename A, typename E = boost::multi_array_types::extent_gen>
        auto make_extent_from(A&& a, E e = E())
        {
          return make_extent<std::remove_reference<A>::type::dimensionality>(a.index_bases(), a.shape(), e);
        }

        template<typename IndexArray, typename SwapFunc>
        void reorder(const IndexArray& part_idx, SwapFunc func)
        {
            size_t numPart = part_idx.shape()[0], i = 0;
            boost::multi_array<typename IndexArray::element,1> sorter(boost::extents[numPart]);

            LibLSS::copy_array(sorter, part_idx);

            // Now that partices have been gathered back, we have to reorder them
            // to "unsort".

            while (i < numPart) {
              typename IndexArray::reference swapper = sorter[i];

              if (swapper == i) {
                i++;
                continue;
              }
              func(swapper, i);

              std::swap(sorter[i], sorter[swapper]);
            }
        }



    };

};

#endif
