/*+
    ARES/HADES/BORG Package -- ./libLSS/mpi/fake_mpi/mpi_communication.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

#ifndef __CMB_FAKE_MPI_COMMUNICATION_HPP
#define __CMB_FAKE_MPI_COMMUNICATION_HPP

#include <string>
#include <exception>
#include <cstdlib>
#include <cstring>
#include <boost/multi_array.hpp>

typedef void *MPI_Comm;

namespace LibLSS {
  typedef struct {
    int MPI_ERROR;
  } MPI_Status;
  typedef int MPI_Op;

  static const void *MPI_IN_PLACE = (const void *)0;
  static MPI_Status *const MPI_STATUS_IGNORE = (MPI_Status *)1;
  static const int MPI_SUCCESS = 0;
  static const int MPI_SUM = 0;
  static const int MPI_MIN = 1;
  static const int MPI_MAX = 2;
  static const int MPI_LAND = 3; //FIXME can I assign any number?

  class MPI_Exception : public std::exception {
  public:
    MPI_Exception(int err) : errcode(err) {}

    virtual const char *what() const throw() { return err_string.c_str(); }
    int code() const { return errcode; }

    virtual ~MPI_Exception() throw() {}

  private:
    std::string err_string;
    int errcode;
  };

  class MPICC_Request {
  public:
    MPICC_Request() {}

    bool test(MPI_Status *status = MPI_STATUS_IGNORE) { return true; }

    bool is_active() const { return false; }

    void free() {}

    void wait(MPI_Status *status = MPI_STATUS_IGNORE) {}
  };

  typedef boost::multi_array<MPICC_Request, 1> RequestArray;
  typedef boost::multi_array<MPI_Status, 1> StatusArray;

  class MPICC_Window {
  public:
    void *w;

    void lock(bool) {}
    void unlock() {}

    void fence() {}
    void destroy() { delete[]((char *)w); }

    template <typename T>
    void put(int r, T v) {
      (reinterpret_cast<T *>(w))[r] = v;
    }

    template <typename T>
    T get(int r) {
      return (reinterpret_cast<T *>(w))[r];
    }

    template <typename T>
    T *get_ptr() {
      return (T *)w;
    }

    template <typename T>
    const T *get_ptr() const {
      return (const T *)w;
    }
  };

  class MPICC_Mutex {
  public:
    void acquire() {}
    void release() {}
  };

  class MPI_Communication {
  private:
    friend MPI_Communication *setupMPI(int &argc, char **&argv);
    friend MPI_Communication *setupMPI(MPI_Comm w);

    static MPI_Communication *singleton;

  public:
    typedef MPICC_Request Request;

    MPI_Communication() {}

    MPI_Communication(void*) {}

    ~MPI_Communication() {}

    static MPI_Communication *instance() { return singleton; }

    MPI_Communication *split(int color = 0, int key = 0) {
      return new MPI_Communication();
    }

    int rank() const { return 0; }

    int size() const { return 1; }

    MPI_Comm comm() { return 0; }

    void abort() { ::abort(); }

    MPICC_Mutex *new_mutex(int tag) { return new MPICC_Mutex(); }

    MPICC_Window win_create(int size, int disp_unit) {
      MPICC_Window w;

      w.w = new char[size];
      return w;
    }

    void send_recv(
        const void *sendbuf, int sendcount, MPI_Datatype sdatatype, int dest,
        int sendtag, void *recvbuf, int recvcount, MPI_Datatype rdatatype,
        int source, int recvtag, MPI_Status *s = 0) {
      if (source != 0 || dest != 0 || sendcount != recvcount ||
          recvtag != sendtag)
        throw MPI_Exception(0);
      ::memcpy(recvbuf, sendbuf, sendcount * sdatatype);
    }

    void
    send(const void *buf, int count, MPI_Datatype datatype, int dest, int tag) {
      throw MPI_Exception(0);
    }

    void recv(
        void *buf, int count, MPI_Datatype datatype, int from, int tag,
        MPI_Status *status = 0) {
      throw MPI_Exception(0);
    }

    void reduce(
        const void *sendbuf, void *recvbuf, int count, MPI_Datatype datatype,
        MPI_Op op, int root) {
      if (sendbuf != MPI_IN_PLACE)
        ::memcpy(recvbuf, sendbuf, count * datatype);
    }

    Request
    Irecv(void *buf, int count, MPI_Datatype datatype, int from, int tag) {
      Request req;

      recv(buf, count, datatype, from, tag);
      return req;
    }

    Request
    Isend(void *buf, int count, MPI_Datatype datatype, int to, int tag) {
      Request req;

      send(buf, count, datatype, to, tag);
      return req;
    }

    Request Igather(
        void const *sendbuf, int sendcount, MPI_Datatype sendtype, void *buf,
        int recvcount, MPI_Datatype recvtype, int root) {
      return Request();
    }

    template <typename T>
    Request IrecvT(T *buf, int count, int from, int tag) {
      return Irecv(buf, count, translateMPIType<T>(), from, tag);
    }

    template <typename T>
    Request IsendT(T *buf, int count, int from, int tag) {
      return Isend(buf, count, translateMPIType<T>(), from, tag);
    }

    template <typename T>
    Request
    IgatherT(T const *sendbuf, int sendcount, T *buf, int recvcount, int root) {
      return Igather(
          sendbuf, sendcount, translateMPIType<T>(), buf, recvcount,
          translateMPIType<T>(), root);
    }

    static void WaitAll(RequestArray &reqs, StatusArray &statuses) {}

    static void WaitAll(
        std::vector<Request> &reqs,
        std::vector<MPI_Status> &&statuses = std::vector<MPI_Status>()) {}

    void broadcast(
        void *sendrecbuf, int sendrec_count, MPI_Datatype sr_type, int root) {}

    void scatter(
        const void *sendbuf, int sendcount, MPI_Datatype sendtype,
        void *recvbuf, int recvcount, MPI_Datatype recvtype, int root) {
      throw MPI_Exception(0);
    }

    void all2all(
        const void *sendbuf, int sendcount, MPI_Datatype sendtype,
        void *recvbuf, int recvcount, MPI_Datatype recvtype) {
      memcpy(recvbuf, sendbuf, recvcount * recvtype);
    }

    template <typename T>
    void all2allT(const T *sendbuf, int sendcount, T *recvbuf, int recvcount) {
      all2all(
          sendbuf, sendcount, translateMPIType<T>(), recvbuf, recvcount,
          translateMPIType<T>());
    }

    void all_reduce(
        const void *sendbuf, void *recvbuf, int count, MPI_Datatype datatype,
        MPI_Op op) {
      if (sendbuf != MPI_IN_PLACE)
        ::memcpy(recvbuf, sendbuf, count * datatype);
    }

    void all_gather(
        const void *sendbuf, int sendcount, MPI_Datatype sendtype,
        void *recvbuf, int recvcount, MPI_Datatype recvtype) {
      if (sendbuf != recvbuf)
        memcpy(recvbuf, sendbuf, size_t(sendtype) * size_t(sendcount));
    }

    template <typename T>
    void
    reduce_t(const void *sendbuf, T *recvbuf, int count, MPI_Op op, int root) {
      reduce(sendbuf, recvbuf, count, translateMPIType<T>(), op, root);
    }

    template <typename T>
    void broadcast_t(T *sendrecbuf, int count, int root) {
      broadcast(sendrecbuf, count, translateMPIType<T>(), root);
    }

    template <typename T>
    void all_reduce_t(const void *sendbuf, T *recvbuf, int count, MPI_Op op) {
      all_reduce(sendbuf, recvbuf, count, translateMPIType<T>(), op);
    }

    template <typename T>
    void
    all_gather_t(const T *sendbuf, int sendcount, T *recvbuf, int recvcount) {
      all_gather(
          sendbuf, sendcount, translateMPIType<T>(), recvbuf, recvcount,
          translateMPIType<T>());
    }

    void barrier() {}

    template <typename T>
    void accum(T *target_array, const T *source_array, int count, int root) {
      if (root != 0)
        throw MPI_Exception(0);

      if (target_array != source_array)
        ::memcpy(target_array, source_array, count * sizeof(T));
    }

    template <typename T>
    void all_accum(T *ts_array, int count) {}

    template <typename T>
    void all_gather_t(T *recvbuf, int recvcount) {}

    Request Ireduce(
        const void *sendbuf, void *recvbuf, int count, MPI_Datatype datatype,
        MPI_Op op, int root) {
      return Request();
    }

    Request IallReduce(
        const void *sendbuf, void *recvbuf, int count, MPI_Datatype datatype,
        MPI_Op op) {
      return Request();
    }

    template <typename T>
    Request
    IreduceT(const void *sendbuf, T *recvbuf, int count, MPI_Op op, int root) {
      return Ireduce(sendbuf, recvbuf, count, translateMPIType<T>(), op, root);
    }

    template <typename T>
    Request IallReduceT(const void *sendbuf, T *recvbuf, int count, MPI_Op op) {
      return IallReduce(sendbuf, recvbuf, count, translateMPIType<T>(), op);
    }

    Request
    Ibroadcast(void *buffer, int count, MPI_Datatype datatype, int root) {
      return Request();
    }

    template <typename T>
    Request IbroadcastT(T *buf, int count, int root) {
      return Ibroadcast(buf, count, translateMPIType<T>(), root);
    }

    void all_gatherv(
        const void *sendbuf, int sendcount, MPI_Datatype sendtype,
        void *recvbuf, const int recvcounts[], const int displs[],
        MPI_Datatype recvtype) {
      if (sendbuf != recvbuf)
        memcpy(recvbuf, sendbuf, size_t(sendtype) * size_t(sendcount));
    };

    template <typename T>
    void all_gatherv_t(
        const T *sendbuf, int sendcount, T *recvbuf, const int *recvcounts,
        const int displs[]) {
      all_gatherv(
          sendbuf, sendcount, translateMPIType<T>(), recvbuf, recvcounts,
          displs, translateMPIType<T>());
    }

    template <typename T>
    void all_gatherv_t(T *recvbuf, const int *recvcounts, const int *displs) {}

    void all2allv(
        const void *sendbuf, const int *sendcounts, const int sdispls[],
        MPI_Datatype sendtype, void *recvbuf, const int recvcounts[],
        const int rdispls[], MPI_Datatype recvtype) {
      memcpy(recvbuf, sendbuf, recvcounts[0] * recvtype);
    }

    template <typename T>
    void all2allv_t(
        const T *sendbuf, const int *sendcounts, const int *sdispls, T *recvbuf,
        const int *recvcounts, const int *rdispls) {
      all2allv(
          sendbuf, sendcounts, sdispls, translateMPIType<T>(), recvbuf,
          recvcounts, rdispls, translateMPIType<T>());
    }

    template <typename T>
    Request Iall2allv_t(
        const T *sendbuf, const int *sendcounts, const int *sdispls,
        MPI_Datatype sendtype, T *recvbuf, const int *recvcounts,
        const int *rdispls, MPI_Datatype recvtype) {

      return Request();
    }

    template <typename T>
    Request Iall2allv_t(
        const T *sendbuf, const int *sendcounts, const int *sdispls, T *recvbuf,
        const int *recvcounts, const int *rdispls) {
      return Iall2allv(
          sendbuf, sendcounts, sdispls, translateMPIType<T>(), recvbuf,
          recvcounts, rdispls, translateMPIType<T>());
    }
  };

  inline MPI_Communication *setupMPI(int &argc, char **&argv) {
    MPI_Communication::singleton = new MPI_Communication();
    return MPI_Communication::singleton;
  }

  inline MPI_Communication *setupMPI(MPI_Comm w) {
    MPI_Communication::singleton = new MPI_Communication();
    return MPI_Communication::singleton;
  }

  inline void doneMPI() {}
}; // namespace LibLSS

#endif
