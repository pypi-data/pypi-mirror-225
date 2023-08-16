/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/physics/likelihoods/base.hpp
    Copyright (C) 2018 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_BORG_LIKELIHOODS_BASE_HPP
#  define __LIBLSS_BORG_LIKELIHOODS_BASE_HPP

#  include <string>
#  include <boost/any.hpp>
#  include <map>
#  include <memory>
#  include <array>
#  include "libLSS/mpi/generic_mpi.hpp"
#  include "libLSS/tools/defer.hpp"
#  include "libLSS/tools/errors.hpp"

namespace LibLSS {

  typedef std::map<std::string, boost::any> LikelihoodInfo;

  namespace Likelihood {

    typedef boost::multi_array<size_t, 1> GridSize;
    typedef boost::multi_array<double, 1> GridLengths;

    extern std::string const MPI, COLOR_MAP, DATA_GRID, GRID, MPI_GRID,
        GRID_LENGTH;

    template <typename T>
    T query(LikelihoodInfo const &info, std::string const &key) {
      auto i = info.find(key);
      if (i == info.end()) {
        error_helper<ErrorBadState>("No key " + key + " in info dictionnary");
      }
      try {
        return boost::any_cast<T>(i->second);
      } catch (boost::bad_any_cast& e) {
        error_helper<ErrorBadState>("Type incompatible in any_cast (stored=" + std::string(i->second.type().name()) + "), requested=" + std::string(typeid(T).name()));
      }
    }

    template <typename T>
    T query_default(LikelihoodInfo const &info, std::string const &key, T const& default_value) {
      auto i = info.find(key);
      if (i == info.end()) {
        return default_value;
      }
      try {
        return boost::any_cast<T>(i->second);
      } catch (boost::bad_any_cast& e) {
        error_helper<ErrorBadState>("Type incompatible in any_cast (stored=" + std::string(i->second.type().name()) + "), requested=" + std::string(typeid(T).name()));
      }
    }

    inline MPI_Communication *getMPI(LikelihoodInfo const &info) {
      return query<MPI_Communication *>(info, MPI);
    }

    template <typename T, int N>
    auto getArray(LikelihoodInfo const &info, std::string const &key) {
      return query<std::shared_ptr<boost::multi_array_ref<T, N>>>(info, key);
    }

    template <typename T, int N>
    auto getPromisedArray(LikelihoodInfo const &info, std::string const &key) {
      return query<PromisePointer<boost::multi_array_ref<T, N>>>(info, key);
    }

    template <size_t N, size_t start, size_t skip, typename T>
    auto multi_array_to_std(boost::multi_array_ref<T, 1> const &a) {
      std::array<T, N> b;
      for (size_t i = 0, j = start; i < N; i++, j += skip)
        b[i] = a[j];
      return b;
    }

    template <typename T, size_t N>
    auto diff_array(std::array<T, N> const &a, std::array<T, N> const &b) {
      std::array<T, N> c;
      for (size_t i = 0; i < N; i++)
        c[i] = a[i] - b[i];
      return c;
    }

    inline auto gridResolution(LikelihoodInfo const &info) {
      return multi_array_to_std<3, 0, 1>(query<GridSize>(info, GRID));
    }

    inline auto gridSide(LikelihoodInfo const &info) {
      auto sides = query<GridLengths>(info, GRID_LENGTH);
      auto a0 = multi_array_to_std<3, 0, 2>(sides);
      auto a1 = multi_array_to_std<3, 1, 2>(sides);

      return diff_array(a1, a0);
    }

    inline auto gridCorners(LikelihoodInfo const &info) {
      return multi_array_to_std<3, 0, 2>(query<GridLengths>(info, GRID_LENGTH));
    }

  } // namespace Likelihood

} // namespace LibLSS

#endif

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2018
