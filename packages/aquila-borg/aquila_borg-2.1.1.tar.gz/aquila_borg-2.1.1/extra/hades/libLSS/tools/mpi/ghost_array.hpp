/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/tools/mpi/ghost_array.hpp
    Copyright (C) 2018-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_TOOLS_MPI_GHOST_ARRAY_HPP
#  define __LIBLSS_TOOLS_MPI_GHOST_ARRAY_HPP

#  include <set>
#  include <map>
#  include <memory>
#  include "libLSS/tools/string_tools.hpp"
#  include "libLSS/tools/uninitialized_type.hpp"
#  include "libLSS/mpi/generic_mpi.hpp"
#  include "libLSS/tools/array_tools.hpp"
#  include "libLSS/tools/string_tools.hpp"
#  include "libLSS/samplers/core/types_samplers.hpp"

namespace LibLSS {

  template <typename T>
  struct GhostArrayTypes {
    typedef LibLSS::U_Array<T, 1> U_ArrayType;
    typedef typename U_ArrayType::array_type ArrayType;

    typedef std::map<size_t, std::shared_ptr<U_ArrayType>> MapGhosts;
  };

  template <typename T>
  class GhostArray : public GhostArrayTypes<T> {
  protected:
    static constexpr bool SUPER_VERBOSE = false;
    typedef GhostArrayTypes<T> super;
    typedef typename super::ArrayType ArrayType;
    typedef typename super::U_ArrayType U_ArrayType;
    typedef typename super::MapGhosts MapGhosts;

    MPI_Communication *comm;

    std::vector<boost::multi_array<T, 1>> exchangeIndexes;

  public:
    GhostArray() {}

    /**
     * @brief 
     * 
     * We assume that localIndexes are unique.
     * 
     * @param comm_ 
     * @param localIndexes 
     */
    template <typename IndexSet>
    void setup(MPI_Communication *comm_, IndexSet &&localIndexes) {
      LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
      typedef typename std::remove_reference_t<IndexSet>::value_type indexType;
      static_assert(
          std::is_same<indexType, T>::value, "Index list must be of type T");
      int localKeys = localIndexes.size();

      comm = comm_;

      // Serialize and send to peers
      auto commSize = boost::extents[comm->size()];
      boost::multi_array<indexType, 1> linearIndexes(boost::extents[localKeys]);
      boost::multi_array<int, 1> allIndexCounts(commSize);
      boost::multi_array<int, 1> displIndexes(commSize);

      ctx.print("Transfer indexes to linear array");
      std::copy(
          localIndexes.begin(), localIndexes.end(), linearIndexes.begin());

      ctx.print("Sort");
      std::sort(linearIndexes.begin(), linearIndexes.end());

      comm->all_gather_t(&localKeys, 1, allIndexCounts.data(), 1);

      ctx.print("Compute global displacements");
      int totalIndexes = 0, previousDispl = 0;
      for (int i = 0; i < comm->size(); i++) {
        totalIndexes += allIndexCounts[i];
        displIndexes[i] = previousDispl;
        previousDispl += allIndexCounts[i];
      }

      boost::multi_array<indexType, 1> allIndexes(boost::extents[totalIndexes]);
      // FIXME: Try to reduce memory/bandwidth consumption with better distributed algorithm
      ctx.print("Gather all relevant indexes");
      comm->all_gatherv_t(
          linearIndexes.data(), localKeys, allIndexes.data(),
          allIndexCounts.data(), displIndexes.data());

      std::set<indexType> localSet;

      if (SUPER_VERBOSE)
        ctx.format("Local indexes: %s", LibLSS::to_string(localIndexes));

      ctx.print("Transfer local indexes to set for better intersection");
      std::copy(
          localIndexes.begin(), localIndexes.end(),
          std::inserter(localSet, localSet.begin()));

      exchangeIndexes.resize(comm->size());
      for (int i = 0; i < comm->size(); i++) {
        // Compute intersections with remote nodes
        std::set<indexType> otherIndexes, interIndexes;

        if (i == comm->rank())
          continue;

        for (int j = 0; j < allIndexCounts[i]; j++) {
          otherIndexes.insert(allIndexes[j + displIndexes[i]]);
        }
        if (SUPER_VERBOSE)
          ctx.format(
              "Other indexes (count=%d): %s", allIndexCounts[i],
              LibLSS::to_string(otherIndexes));

        ctx.format("Intersect with rank=%d", i);
        std::set_intersection(
            localSet.begin(), localSet.end(), otherIndexes.begin(),
            otherIndexes.end(),
            std::inserter(interIndexes, interIndexes.begin()));

        ctx.format("%d indexes in common", interIndexes.size());
        exchangeIndexes[i].resize(boost::extents[interIndexes.size()]);
        std::copy(
            interIndexes.begin(), interIndexes.end(),
            exchangeIndexes[i].begin());
      }
    }

    /**
       * @brief 
       * 
       * 
       * 
       * @tparam U 
       * @tparam boost::multi_array_ref<U, 1> 
       * @param data 
       * @param indexToIndex how to map an index (from setup) to an index in the provided array
       */
    template <typename U, typename ReductionOperation, typename IndexMapper>
    void synchronize(
        boost::multi_array_ref<U, 1> &data, IndexMapper &&mapper,
        ReductionOperation op) {
      LIBLSS_AUTO_DEBUG_CONTEXT(ctx);
      typedef LibLSS::U_Array<U, 1> TmpU;

      std::vector<std::shared_ptr<TmpU>> allTmpSend;
      std::vector<std::shared_ptr<TmpU>> allTmpRecv;
      std::vector<MPICC_Request> allReq;

      allTmpRecv.resize(comm->size());

      for (int i = 0; i < comm->size(); i++) {
        int numExchange = exchangeIndexes[i].size();
        if (numExchange == 0) {
          continue;
        }

        ctx.format("Send %d data -> %d", numExchange, i);
        {
          auto thisTmp = std::make_shared<TmpU>(boost::extents[numExchange]);
          auto &tmpData = thisTmp->get_array();

          allTmpSend.push_back(thisTmp);

#  pragma omp parallel for
          for (int j = 0; j < numExchange; j++) {
            tmpData[j] = data[mapper(exchangeIndexes[i][j])];
          }

          allReq.push_back(comm->IsendT(tmpData.data(), tmpData.size(), i, i));
        }
        ctx.format("Recv %d data <- %d", numExchange, i);
        {
          auto thisTmp = std::make_shared<TmpU>(boost::extents[numExchange]);
          auto &tmpData = thisTmp->get_array();

          allTmpRecv[i] = thisTmp;

          allReq.push_back(
              comm->IrecvT(tmpData.data(), tmpData.size(), i, comm->rank()));
        }
      }
      ctx.print("Wait IO completion");
      comm->WaitAll(allReq);

      allTmpSend.clear();

      {
        ConsoleContext<LOG_DEBUG> ctx("GhostArray local reduction");

        // Now all data are in place, we must do partial reductions
        for (int i = 0; i < comm->size(); i++) {
          if (i == comm->rank())
            continue;
          int numExchange = exchangeIndexes[i].size();
          if (numExchange == 0)
            continue;

          auto &inData = allTmpRecv[i]->get_array();

#  pragma omp parallel for
          for (int j = 0; j < numExchange; j++) {
            op(data[mapper(exchangeIndexes[i][j])], inData[j]);
          }
        }
      }
    }

    template <typename U, typename IndexMapper>
    void synchronize(
        boost::multi_array_ref<U, 1> &data, IndexMapper &&indexToIndex) {
      synchronize<U>(
          data, indexToIndex, [](auto &x, auto const &y) { x += y; });
    }
  };
} // namespace LibLSS

#endif
// ARES TAG: num_authors = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2018-2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
