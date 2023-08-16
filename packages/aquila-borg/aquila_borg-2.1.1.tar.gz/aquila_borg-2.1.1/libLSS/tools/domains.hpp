/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/domains.hpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TOOLS_MPI_DOMAIN_HPP
#  define __LIBLSS_TOOLS_MPI_DOMAIN_HPP

#  include <boost/multi_array.hpp>
#  include <cstdint>
#  include <list>
#  include "libLSS/mpi/generic_mpi.hpp"
#  include <boost/optional.hpp>
#  include "libLSS/samplers/core/types_samplers.hpp"

namespace LibLSS {

  /**
   * @brief Specifies the boundary of domains
   *
   * @tparam N number of dimensions
   */
  template <size_t N>
  struct DomainSpec {
    /**
     * @brief Type defining an hypercube boundary.
     *
     * The hypercube is defined by two corners defined in an N-d space.
     * Thus we need 2 * Nd elements in that array.
     */
    typedef std::array<ssize_t, 2 * N> DomainLimit_t;

    /**
     * @brief Boundaries
     *
     * A domain is defined by a set of hypercube boundaries.
     * The assumption is that the hypercubes are disjoint.
     */
    std::vector<DomainLimit_t> domains;

    boost::optional<DomainSpec<N>> intersect(DomainSpec<N> const &other) const;
  };

  /**
   * @brief Hold the complete description of the domain on all nodes.
   *
   * Any sane description should cover completely the hypercube domain.
   *
   * @tparam N number of dimensions of the hypercube
   */
  template <size_t N>
  struct CompleteDomainSpec {
    std::vector<DomainSpec<N>> domainOnRank;
  };

  /**
   * @brief Specific task to exchange data on domains
   *
   * @tparam N
   */
  template <size_t N>
  struct DomainTask {
    typename DomainSpec<N>::DomainLimit_t slice;
    int rankIO;
    bool recv;
  };

  /**
   * @brief Todo list of tasks to complete to redistribute domain data on nodes
   *
   * @tparam N
   */
  template <size_t N>
  struct DomainTodo {
    std::list<DomainTask<N>> tasks;
  };

  /**
   * @brief Array of data for the domain
   *
   * @tparam T
   * @tparam N
   */
  template <typename T, size_t N>
  using Domain = LibLSS::multi_array_ref<T, N>;

  /**
   * @brief Gather the complete domain specification.
   *
   * This function gather the description from each tasks about their domain
   * specification and store the result in `complete`.
   * @tparam N
   * @param comm
   * @param complete
   * @param inputSpec
   */
  template <size_t N>
  void computeCompleteDomainSpec(
      MPI_Communication *comm, CompleteDomainSpec<N> &complete,
      DomainSpec<N> const &inputSpec);

  /**
   * @brief Compute the list of tasks to do to transform from one spec to another
   *
   * The algorithm must complete the list of tasks to go from `inputSpec` to `outputSpec`
   * on each node. Provided the domain does not change the list of tasks must be
   * invariant w.r.t held data.
   *
   * @tparam N
   * @param comm
   * @param inputSpec
   * @param outputSpec
   * @param todo
   */
  template <size_t N>
  void mpiDomainComputeTodo(
      MPI_Communication *comm, CompleteDomainSpec<N> const &inputSpec,
      CompleteDomainSpec<N> const &outputSpec, DomainTodo<N> &todo);

  /**
   * @brief Execute a domain redecomposition
   *
   * @tparam T
   * @tparam N
   * @param comm
   * @param inputSpec
   * @param inputDomain
   * @param outputSpec
   * @param outputDomain
   */
  template <typename T, size_t N>
  void mpiDomainRun(
      MPI_Communication *comm, Domain<T, N> const &input_domains,
      Domain<T, N> &output_domains, DomainTodo<N> const &todo);

} // namespace LibLSS

#endif
// ARES TAG: num_authors = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
