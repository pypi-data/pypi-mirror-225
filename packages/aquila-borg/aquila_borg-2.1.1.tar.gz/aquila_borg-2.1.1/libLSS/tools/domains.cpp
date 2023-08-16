/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/domains.cpp
    Copyright (C) 2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/cconfig.h"
#include <vector>
#include <memory>
#include "libLSS/tools/console.hpp"
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/domains.hpp"
#include "libLSS/tools/array_tools.hpp"
#include "libLSS/tools/uninitialized_type.hpp"

using namespace LibLSS;

template <typename T, size_t N>
using TemporarySlice = LibLSS::U_Array<T, N>;

template <typename T, size_t N>
auto makeTempSlice(typename DomainSpec<N>::DomainLimit_t &slice) {
  std::array<ssize_t, N> bases, shapes;

  for (unsigned int i = 0; i < N; i++) {
    bases[i] = slice[2 * i];
    shapes[i] = slice[2 * i + 1];
  }
  auto ext = array::make_extent<N>(bases, shapes);
  return std::make_shared<TemporarySlice<T, N>>(ext);
}

template <typename T, size_t N>
std::shared_ptr<TemporarySlice<T, N>> extractSlice(
    Domain<T, N> const &input, typename DomainSpec<N>::DomainLimit_t &slice) {
  auto ret = makeTempSlice(slice);

  fwrap(ret->get_array()) = input;
  return ret;
}

template <typename T, size_t N>
void pushSlice(
    std::shared_ptr<TemporarySlice<T, N>> tmp_slice, Domain<T, N> &output,
    typename DomainSpec<N>::DomainLimit_t &slice) {
  //fwrap(ret->get_array()) = input;
  //return ret;
}

template <size_t N>
boost::optional<DomainSpec<N>>
DomainSpec<N>::intersect(DomainSpec<N> const &other) const {
  Console::instance().c_assert(
      domains.size() == 1,
      "Only intersect of single hypercube are supported at the moment");
  DomainSpec<N> result;

  std::array<ssize_t, N> start, end;
  for (int i = 0; i < N; i++) {
    start[i] = domains[0][2 * i];
    end[i] = domains[0][2 * i + 1];

    auto other_start = other.domains[0][2 * i];
    auto other_end = other.domains[0][2 * i + 1];

    if (end[i] < other_start || other_end < start[i])
      return boost::optional<DomainSpec<N>>();

    start[i] = std::max(start[i], other_start);
    end[i] = std::min(end[i], other_end);

    result.domains[0][2 * i] = start[i];
    result.domains[0][2 * i + 1] = end[i];
  }
  return result;
}

template <size_t N>
void LibLSS::computeCompleteDomainSpec(
    MPI_Communication *comm, CompleteDomainSpec<N> &complete,
    DomainSpec<N> const &inputSpec) {
  size_t commSize = comm->size();
  size_t rank = comm->rank();
  std::unique_ptr<int[]> domainPerNodes(new int[commSize]),
      displs(new int[commSize]);
  std::unique_ptr<ssize_t[]> tmp_domain(new ssize_t[2 * N * commSize]);
  RequestArray requests(boost::extents[commSize]);

  complete.domainOnRank.resize(commSize);

  domainPerNodes[rank] = inputSpec.domains.size();
  comm->all_gather_t(&domainPerNodes[comm->rank()], 1, domainPerNodes.get(), 1);
  // We now have the size of each input domain
  //
  // Now each node must broadcast its exact domain spec to everybody.
  {
    size_t previous = 0;
    for (size_t i = 0; i < commSize; i++) {
      complete.domainOnRank[i].domains.resize(domainPerNodes[i]);
      // Now domainPerNodes contain the number of elements for the descriptor.
      domainPerNodes[i] *= 2 * N;
      // Add to the displacement.
      displs[i] = previous + domainPerNodes[i];
    }
  }

  // Do a vector gather over the communicator
  comm->all_gatherv_t(
      &inputSpec.domains[0][0], 2 * N * domainPerNodes[rank], tmp_domain.get(),
      domainPerNodes.get(), displs.get());

  // Copy the result back in place
  for (size_t i = 0; i < commSize; i++) {
    for (int j = 0; j < domainPerNodes[i] / (2 * N); j++) {
      std::copy(
          &tmp_domain[displs[i]], &tmp_domain[displs[i] + domainPerNodes[i]],
          complete.domainOnRank[i].domains[j].begin());
    }
  }
}

template <size_t N>
void LibLSS::mpiDomainComputeTodo(
    MPI_Communication *comm, CompleteDomainSpec<N> const &inputSpec,
    CompleteDomainSpec<N> const &outputSpec, DomainTodo<N> &todo) {
  // Now that all nodes know everything. We may compute the I/O operations to achieve.
  // i.e. which nodes are peers for the current one and which slices

  // Clear up the todo list
  todo.tasks.clear();

  // We will build the tasks to execute between this node and the others based on the description.
  // First which pieces to send

  {
    auto &current_domain = inputSpec.domainOnRank[comm->rank()];

    for (int r = 0; r < comm->size(); r++) {
      //An intersection of two hypercube is still a single hybercube
      DomainTask<N> task;

      auto result = current_domain.intersect(outputSpec.domainOnRank[r]);
      if (!result)
        continue;
      task.slice = *result;
      task.recv = false;
      task.rankIO = r;
      todo.tasks.push_back(task);
    }
  }

  {
    auto &current_domain = outputSpec.domainOnRank[comm->rank()];

    for (int r = 0; r < comm->size(); r++) {
      //An intersection of two hypercube is still a single hybercube
      DomainTask<N> task;

      auto result = current_domain.intersect(inputSpec.domainOnRank[r]);
      if (!result)
        continue;
      task.slice = *result;
      task.recv = true;
      task.rankIO = r;
      todo.tasks.push_back(task);
    }
  }
}

template <typename T, size_t N>
void mpiDomainRun(
    MPI_Communication *comm, Domain<T, N> const &input_domains,
    Domain<T, N> &output_domains, DomainTodo<N> const &todo) {
  size_t numTasks = todo.tasks.size();
  std::vector<MPICC_Request> requestList(numTasks);
  std::vector<MPI_Status> statusList(numTasks);
  std::vector<std::shared_ptr<TemporarySlice<T, N>>> slices(numTasks);

  // Schedule all exchanges
  for (int t = 0; t < todo.tasks; t++) {
    auto &task = todo.tasks[t];

    if (!task.recv) {
      slices[t] = extractSlice(input_domains, task.slice);
      requestList[t] = comm->IsendT(
          slices[t]->get_array()->data(), slices[t]->get_array()->size(),
          task.rankIO, 0);
    } else {
      slices[t] = makeTempSlice(task.slice);
      requestList[t] = comm->IrecvT(
          slices[t]->get_array()->data(), slices[t]->get_array()->size(),
          task.rankIO, 0);
    }
  }

  for (int t = 0; t < todo.tasks; t++) {
    auto &task = todo.tasks[t];

    if (task.recv) {
      requestList[t].wait();
      pushSlice(output_domains, task.slice);
    }
  }
  for (int t = 0; t < todo.tasks; t++) {
    if (!todo.tasks[t].recv)
      requestList[t].wait();
  }
}

#define FORCE(N)                                                               \
  template void LibLSS::mpiDomainComputeTodo<>(                                \
      MPI_Communication * comm, DomainSpec<N> const &inputSpec,                \
      DomainSpec<N> const &outputSpec, DomainTodo<N> &todo);                   \
  template void LibLSS::computeCompleteDomainSpec<>(                           \
      MPI_Communication *, CompleteDomainSpec<N> & complete,                   \
      DomainSpec<N> const &inputSpec);

//FORCE(3);

// ARES TAG: num_authors = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: year(0) = 2020
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
