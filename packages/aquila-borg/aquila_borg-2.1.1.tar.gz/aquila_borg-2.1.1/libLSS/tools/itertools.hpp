/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/itertools.hpp
    Copyright (C) 2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_ITERTOOLS_HPP
#define __LIBLSS_ITERTOOLS_HPP

#include <boost/iterator/counting_iterator.hpp>
#include <boost/iterator/zip_iterator.hpp>
#include <boost/tuple/tuple.hpp>

namespace LibLSS {
  namespace itertools {

    template <typename I>
    auto enumerate_base(size_t i, I j) -> decltype(boost::make_zip_iterator(
        boost::make_tuple(boost::counting_iterator<size_t>(i), j))) {
      return boost::make_zip_iterator(
          boost::make_tuple(boost::counting_iterator<size_t>(i), j));
    }

    template <typename T>
    struct Enumerate {
    public:
      T const &t;

      Enumerate(T const &t_) : t(t_) {}

      auto begin() const -> decltype(enumerate_base(0, t.begin())) {
        return enumerate_base(0, t.begin());
      }
      auto end() const -> decltype(enumerate_base(t.size(), t.end())) {
        return enumerate_base(t.size(), t.end());
      }
    };

    struct Range {
      size_t i0, i1;

      Range(size_t i0_, size_t i1_) : i0(i0_), i1(i1_) {}
      auto begin() const -> decltype(boost::counting_iterator<size_t>(i0)) {
        return boost::counting_iterator<size_t>(i0);
      }
      auto end() const -> decltype(boost::counting_iterator<size_t>(i1)) {
        return boost::counting_iterator<size_t>(i1);
      }
    };


    /**
     * This function creates a pseudo container (range container) over
     * which one can iterate upon.
     * A typical use is:
     * <code>
     *   for (size_t id: range(0, N)) { blabla; }
     * </code>
     *
     * @param i0 start of the range
     * @param i1 end of the range
     * @return a container
     */
    inline Range range(size_t i0, size_t i1) { return Range(i0, i1); }

    /**
     * This function creates a pseudo container made of a zip iterator binding
     * a range and an iterator over the provided container.
     * A typical use is:
     * <code>
     *    for (auto x: enumerate(some_vector)) {
     *       size_t id = x.get<0>();
     *       // Some stuff
     *       the_type_in_vector const& v = x.get<1>();
     *    }
     * </code>
     *
     * @param t a container
     * @return a container with an enumeration
     */
    template <typename T>
    inline Enumerate<T> enumerate(T const &t) {
      return Enumerate<T>(t);
    }



  } // namespace itertools
} // namespace LibLSS
#endif

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019
