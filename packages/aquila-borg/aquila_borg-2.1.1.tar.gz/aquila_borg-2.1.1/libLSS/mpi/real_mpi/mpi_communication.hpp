/*+
    ARES/HADES/BORG Package -- ./libLSS/mpi/real_mpi/mpi_communication.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

#ifndef __LIBLSS_REAL_MPI_COMMUNICATION_HPP
#define __LIBLSS_REAL_MPI_COMMUNICATION_HPP

#include <boost/format.hpp>
#include <cstdlib>
#include <iostream>
#include <boost/multi_array.hpp>
#include "libLSS/tools/openmp.hpp"

namespace LibLSS {

  /**
   * @brief Wrapper class to handle MPI exceptions.
   * 
   */
  class MPI_Exception : virtual std::exception {
  public:
    /**
     * @brief Construct a new mpi exception object
     * 
     * @param err  MPI Error code
     */
    MPI_Exception(int err) {
      char s[MPI_MAX_ERROR_STRING];
      int l;

      MPI_Error_string(err, s, &l);
      err_string = s;
    }

    /**
     * @brief Return the error message
     * 
     * @return const char* 
     */
    const char *what() const throw() override { return err_string.c_str(); }

    /**
     * @brief Return the MPI error code
     * 
     * @return int 
     */
    int code() const { return errcode; }

    virtual ~MPI_Exception() throw() {}

  private:
    std::string err_string;
    int errcode;
  };

  class MPI_Communication;

  class MPICC_Request {
  public:
    MPI_Request request;
    int tofrom_rank;
    bool active;

    MPICC_Request() : active(false) {}

    void set(MPI_Request r) {
      request = r;
      active = true;
    }

    bool is_active() const { return active; }

    bool test(MPI_Status *status = MPI_STATUS_IGNORE) {
      int flag;
      int err;

      if (!active)
        return true;

      if ((err = MPI_Test(&request, &flag, status)) != MPI_SUCCESS)
        throw MPI_Exception(err);
      return flag != 0;
    }

    void free() {
      int err;

      if (!active)
        return;

      if ((err = MPI_Request_free(&request)) != MPI_SUCCESS)
        throw MPI_Exception(err);
    }

    void wait(MPI_Status *status = MPI_STATUS_IGNORE) {
      int err;

      if (!active)
        return;

      if ((err = MPI_Wait(&request, status)) != MPI_SUCCESS)
        throw MPI_Exception(err);
    }
  };

  typedef boost::multi_array<MPICC_Request, 1> RequestArray;
  typedef boost::multi_array<MPI_Status, 1> StatusArray;

  class MPICC_Window {
  public:
    MPI_Communication *Comm;
    MPI_Win win;
    void *wp;
    int size;
    int rank;

    void lock(bool shared = false) {
      int err;
      if ((err = MPI_Win_lock(
               shared ? MPI_LOCK_SHARED : MPI_LOCK_EXCLUSIVE, rank, 0, win)) !=
          MPI_SUCCESS)
        throw MPI_Exception(err);
    }

    void unlock() {
      int err;

      if ((err = MPI_Win_unlock(rank, win)) != MPI_SUCCESS)
        throw MPI_Exception(err);
    }

    void fence() { MPI_Win_fence(rank, win); }

    void destroy() {
      MPI_Win_free(&win);
      if (wp != 0)
        MPI_Free_mem(wp);
    }

    template <typename T>
    void put(int r, T v);

    template <typename T>
    T get(int r);

    template <typename T>
    T *get_ptr() {
      return (T *)wp;
    }

    template <typename T>
    const T *get_ptr() const {
      return (const T *)wp;
    }
  };

  class MPICC_Mutex {
  public:
    MPICC_Mutex(MPI_Comm comm, int tag);
    ~MPICC_Mutex();

    void acquire();
    void release();

  protected:
    MPI_Comm comm;
    MPI_Win win;
    int *lockArray;
    int host_rank;
    int mutex_tag;
  };

  /**
   * @brief Wrapper for MPI communication object.
   * 
   */
  class MPI_Communication {
  private:
    MPI_Comm comm0;
    int cur_rank, cur_size;
    bool free_on_destroy;

    friend MPI_Communication *setupMPI();
    friend MPI_Communication *setupMPI(int &argc, char **&argv);
    friend MPI_Communication *setupMPI(MPI_Comm w);

    static MPI_Communication *singleton;

  public:
    typedef MPICC_Request Request;

    /**
     * @brief Returns the world communicator.
     * 
     * @return MPI_Communication* 
     */
    static MPI_Communication *instance() { return singleton; }

    /**
     * @brief Construct a new mpi communication object based on a MPI_Comm instance.
     * 
     * @param mcomm        MPI_Comm instance
     * @param auto_free    if true, the instance will be discarded on destruction
     */
    MPI_Communication(MPI_Comm mcomm, bool auto_free = false)
        : comm0(mcomm), free_on_destroy(auto_free) {
      //      MPI_Comm_set_errhandler(comm, MPI_ERRORS_RETURN);
      MPI_Comm_rank(comm0, &cur_rank);
      MPI_Comm_size(comm0, &cur_size);
    }

    ~MPI_Communication() {
      if (free_on_destroy)
        MPI_Comm_free(&comm0);
    }

    MPI_Communication *split(int color = MPI_UNDEFINED, int key = 0) {
      MPI_Comm newcomm;
      int err;

      if ((err = MPI_Comm_split(comm0, color, key, &newcomm)) != MPI_SUCCESS)
        throw MPI_Exception(err);
      if (newcomm == MPI_COMM_NULL)
        return 0;
      return new MPI_Communication(newcomm, true);
    }

    MPICC_Mutex *new_mutex(int tag) { return new MPICC_Mutex(comm0, tag); }

    /**
     * @brief Returns the rank of the node in the communicator
     * 
     * @return int 
     */
    int rank() const { return cur_rank; }

    /**
     * @brief Returns the size of the communicator
     * 
     * @return int 
     */
    int size() const { return cur_size; }

    /**
     * @brief Returns the underlyind MPI_Comm instance
     * 
     * @return MPI_Comm 
     */
    MPI_Comm comm() { return comm0; }

    /**
     * @brief Triggers an abort action on the communication.
     * 
     * That action is generally fatal to the program.
     * 
     */
    void abort() { MPI_Abort(comm0, 99); }

    MPICC_Window win_create(int size, int disp_unit) {
      MPICC_Window w;
      int err;

      w.rank = 0;
      w.Comm = this;

      if (rank() == w.rank) {
        if ((err = MPI_Alloc_mem(size, MPI_INFO_NULL, &w.wp)) != MPI_SUCCESS)
          throw MPI_Exception(err);
      } else {
        size = 0;
        disp_unit = 1;
        w.wp = 0;
      }
      if ((err = MPI_Win_create(
               w.wp, size, disp_unit, MPI_INFO_NULL, comm0, &w.win)) !=
          MPI_SUCCESS) {
        if (w.wp != 0)
          MPI_Free_mem(w.wp);
        throw MPI_Exception(err);
      }
      MPI_Win_fence(0, w.win);
      return w;
    }

    void send_recv(
        const void *sendbuf, int sendcount, MPI_Datatype sdatatype, int dest,
        int sendtag, void *recvbuf, int recvcount, MPI_Datatype rdatatype,
        int source, int recvtag, MPI_Status *s = MPI_STATUS_IGNORE) {
      int err;
      if ((err = MPI_Sendrecv(
               (void *)sendbuf, sendcount, sdatatype, dest, sendtag, recvbuf,
               recvcount, rdatatype, source, recvtag, comm0, s)) != MPI_SUCCESS)
        throw MPI_Exception(err);
    }

    /**
     * @brief Send a buffer to another MPI task
     * 
     * @param buf         buffer holding the objects to be sent
     * @param count       number count of objects
     * @param datatype    datatypes of the objects
     * @param dest        rank of the destination
     * @param tag         tag attached to the send
     */
    void
    send(const void *buf, int count, MPI_Datatype datatype, int dest, int tag) {
      int err;
      using boost::format;
      using boost::str;

      if ((err = MPI_Send((void *)buf, count, datatype, dest, tag, comm0)) !=
          MPI_SUCCESS) {
        throw MPI_Exception(err);
      }
    }

    /**
     * @brief *Immediately* receive a buffer from another MPI task
     * 
     * This immediately triggers the reception. The receive is not
     * guaranteed till a successful wait on the return object.
     * 
     * @param buf         buffer holding the objects to be sent
     * @param count       number count of objects
     * @param datatype    datatypes of the objects
     * @param from        rank of the destination
     * @param tag         tag attached to the message
     * @return Request   the pending request
     * @see LibLSS::MPI_Communication::recv
     */
    Request
    Irecv(void *buf, int count, MPI_Datatype datatype, int from, int tag) {
      int err;
      Request req;
      MPI_Request r;

      req.tofrom_rank = from;
      if ((err = MPI_Irecv(buf, count, datatype, from, tag, comm0, &r)) !=
          MPI_SUCCESS)
        throw MPI_Exception(err);
      req.set(r);
      return req;
    }

    Request
    Isend(void *buf, int count, MPI_Datatype datatype, int to, int tag) {
      int err;
      Request req;
      MPI_Request r;

      req.tofrom_rank = to;
      if ((err = MPI_Isend(buf, count, datatype, to, tag, comm0, &r)) !=
          MPI_SUCCESS)
        throw MPI_Exception(err);

      req.set(r);
      return req;
    }

    Request IallReduce(
        const void *sendbuf, void *recvbuf, int count, MPI_Datatype datatype,
        MPI_Op op) {
      int err;
      Request req;
      MPI_Request r;

      if ((err = MPI_Iallreduce(
               sendbuf, recvbuf, count, datatype, op, comm0, &r)) !=
          MPI_SUCCESS)
        throw MPI_Exception(err);

      req.set(r);
      return req;
    }

    Request Ireduce(
        const void *sendbuf, void *recvbuf, int count, MPI_Datatype datatype,
        MPI_Op op, int root) {
      int err;
      Request req;
      MPI_Request r;

      req.tofrom_rank = root;
      if ((err = MPI_Ireduce(
               sendbuf, recvbuf, count, datatype, op, root, comm0, &r)) !=
          MPI_SUCCESS)
        throw MPI_Exception(err);

      req.set(r);
      return req;
    }

    template <typename T>
    Request IallReduceT(const void *sendbuf, T *recvbuf, int count, MPI_Op op) {
      return IallReduce(sendbuf, recvbuf, count, translateMPIType<T>(), op);
    }

    template <typename T>
    Request
    IreduceT(const void *sendbuf, T *recvbuf, int count, MPI_Op op, int root) {
      return Ireduce(sendbuf, recvbuf, count, translateMPIType<T>(), op, root);
    }

    Request
    Ibroadcast(void *buffer, int count, MPI_Datatype datatype, int root) {
      int err;
      Request req;
      MPI_Request r;

      req.tofrom_rank = root;
      if ((err = MPI_Ibcast(buffer, count, datatype, root, comm0, &r)) !=
          MPI_SUCCESS)
        throw MPI_Exception(err);

      req.set(r);
      return req;
    }

    template <typename T>
    Request IbroadcastT(T *buf, int count, int root) {
      return Ibroadcast(buf, count, translateMPIType<T>(), root);
    }

    template <typename T>
    Request IrecvT(T *buf, int count, int from, int tag) {
      return Irecv(buf, count, translateMPIType<T>(), from, tag);
    }

    template <typename T>
    Request IsendT(T *buf, int count, int from, int tag) {
      return Isend(buf, count, translateMPIType<T>(), from, tag);
    }

    static void WaitAll(
        std::vector<Request> &reqs,
        std::vector<MPI_Status> &&statuses = std::vector<MPI_Status>()) {
      boost::multi_array<MPI_Request, 1> req_array(boost::extents[reqs.size()]);

      statuses.resize(reqs.size());
      for (int i = 0; i < reqs.size(); i++)
        req_array[i] = reqs[i].request;

      MPI_Waitall(reqs.size(), req_array.data(), &statuses[0]);
    }

    static void WaitAll(RequestArray &reqs, StatusArray &statuses) {
      boost::multi_array<MPI_Request, 1> req_array(
          boost::extents[reqs.num_elements()]);
      boost::multi_array<long, 1> req_assign(
          boost::extents[reqs.num_elements()]);
      long j = 0;

      for (long i = 0; i < reqs.num_elements(); i++) {
        if (!reqs[i].is_active())
          continue;

        req_array[j] = reqs[i].request;
        req_assign[j] = i;
        j++;
      }

      MPI_Waitall(j, req_array.data(), statuses.data());

      for (long i = 0; i < j; i++) {
        if (req_assign[i] != i)
          // req_assign[i] >= i always
          statuses[req_assign[i]] = statuses[i];
      }
    }

    void recv(
        void *buf, int count, MPI_Datatype datatype, int from, int tag,
        MPI_Status *status = MPI_STATUS_IGNORE) {
      int err;
      MPI_Status my_status;
      using boost::format;
      using boost::str;
      if ((err =
               MPI_Recv(buf, count, datatype, from, tag, comm0, &my_status)) !=
          MPI_SUCCESS)
        throw MPI_Exception(err);
    }

    void reduce(
        const void *sendbuf, void *recvbuf, int count, MPI_Datatype datatype,
        MPI_Op op, int root) {
      int err;

      if ((err = MPI_Reduce(
               (void *)sendbuf, recvbuf, count, datatype, op, root, comm0)) !=
          MPI_SUCCESS)
        throw MPI_Exception(err);
    }

    void broadcast(
        void *sendrecbuf, int sendrec_count, MPI_Datatype sr_type, int root) {
      int err;

      if ((err = MPI_Bcast(sendrecbuf, sendrec_count, sr_type, root, comm0)) !=
          MPI_SUCCESS)
        throw MPI_Exception(err);
    }

    void scatter(
        const void *sendbuf, int sendcount, MPI_Datatype sendtype,
        void *recvbuf, int recvcount, MPI_Datatype recvtype, int root) {
      int err;

      if ((err = MPI_Scatter(
               (void *)sendbuf, sendcount, sendtype, recvbuf, recvcount,
               recvtype, root, comm0)) != MPI_SUCCESS)
        throw MPI_Exception(err);
    }

    void all_reduce(
        const void *sendbuf, void *recvbuf, int count, MPI_Datatype datatype,
        MPI_Op op) {
      int err;

      if ((err = MPI_Allreduce(
               (void *)sendbuf, recvbuf, count, datatype, op, comm0)) !=
          MPI_SUCCESS)
        throw MPI_Exception(err);
    }

    void all_gather(
        const void *sendbuf, int sendcount, MPI_Datatype sendtype,
        void *recvbuf, int recvcount, MPI_Datatype recvtype) {
      int err;
      if ((err = MPI_Allgather(
               (void *)sendbuf, sendcount, sendtype, recvbuf, recvcount,
               recvtype, comm0)) != MPI_SUCCESS)
        throw MPI_Exception(err);
    }

    void gather(
        const void *sendbuf, int sendcount, MPI_Datatype sendtype,
        void *recvbuf, int recvcount, MPI_Datatype recvtype, int root) {
      int err;
      if ((err = MPI_Gather(
               (void *)sendbuf, sendcount, sendtype, recvbuf, recvcount,
               recvtype, root, comm0)) != MPI_SUCCESS)
        throw MPI_Exception(err);
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

    template <typename T>
    void gather_t(
        const T *sendbuf, int sendcount, T *recvbuf, int recvcount, int root) {
      gather(
          sendbuf, sendcount, translateMPIType<T>(), recvbuf, recvcount,
          translateMPIType<T>());
    }

    Request Igather(
        void const *sendbuf, int sendcount, MPI_Datatype sendtype, void *buf,
        int recvcount, MPI_Datatype recvtype, int root) {
      int err;
      Request req;
      MPI_Request r;

      req.tofrom_rank = root;
      if ((err = MPI_Igather(
               sendbuf, sendcount, sendtype, buf, recvcount, recvtype, root,
               comm0, &r)) != MPI_SUCCESS)
        throw MPI_Exception(err);

      req.set(r);
      return req;
    }

    template <typename T>
    Request
    IgatherT(T const *sendbuf, int sendcount, T *buf, int recvcount, int root) {
      return Igather(
          sendbuf, sendcount, translateMPIType<T>(), buf, recvcount,
          translateMPIType<T>(), root);
    }

    void barrier() {
      int err;
      if ((err = MPI_Barrier(comm0)) != MPI_SUCCESS)
        throw MPI_Exception(err);
    }

    template <typename T>
    void accum(T *target_array, const T *source_array, int count, int root) {
      MPI_Datatype t = translateMPIType<T>();

      if (rank() == root) {
        T *tmp_arr = new T[count];
        for (int other = 0; other < size(); other++) {
          if (other == root)
            continue;
          recv(tmp_arr, count, t, other, 0);
          for (int j = 0; j < count; j++)
            target_array[j] += tmp_arr[j];
        }
        delete[] tmp_arr;
      } else {
        send(source_array, count, t, root, 0);
      }
    }

    void all2all(
        const void *sendbuf, int sendcount, MPI_Datatype sendtype,
        void *recvbuf, int recvcount, MPI_Datatype recvtype) {
      int err;

      if ((err = MPI_Alltoall(
               (void *)sendbuf, sendcount, sendtype, recvbuf, recvcount,
               recvtype, comm0)) != MPI_SUCCESS)
        throw MPI_Exception(err);
    }

    template <typename T>
    void all2allT(const T *sendbuf, int sendcount, T *recvbuf, int recvcount) {
      all2all(
          sendbuf, sendcount, translateMPIType<T>(), recvbuf, recvcount,
          translateMPIType<T>());
    }

    template <typename T>
    void all_accum(T *ts_array, int count) {
      MPI_Datatype t = translateMPIType<T>();

      accum(ts_array, ts_array, count, 0);
      if (rank() == 0) {
        for (int other = 1; other < size(); other++)
          send(ts_array, count, t, other, 0);
      } else
        recv(ts_array, count, t, 0, 0);
    }

    void all_gatherv(
        const void *sendbuf, int sendcount, MPI_Datatype sendtype,
        void *recvbuf, const int recvcounts[], const int displs[],
        MPI_Datatype recvtype) {
      int err;
      // Circumventing old buggy MPI implementation
      if ((err = MPI_Allgatherv(
               (void *)sendbuf, sendcount, sendtype, recvbuf,
               (int *)&recvcounts[0], (int *)&displs[0], recvtype, comm0)) !=
          MPI_SUCCESS)
        throw MPI_Exception(err);
    }

    template <typename T>
    void all_gatherv_t(
        const T *sendbuf, int sendcount, T *recvbuf, const int *recvcounts,
        const int *displs) {
      all_gatherv(
          sendbuf, sendcount, translateMPIType<T>(), recvbuf, recvcounts,
          displs, translateMPIType<T>());
    }

    //for in place gathering, automatic type translation ha problems
    template <typename T>
    void all_gather_t(T *recvbuf, int recvcount) {
      all_gather(
          MPI_IN_PLACE, 0, MPI_DATATYPE_NULL, recvbuf, recvcount,
          translateMPIType<T>());
    }

    template <typename T>
    void all_gatherv_t(T *recvbuf, const int *recvcounts, const int *displs) {
      all_gatherv(
          MPI_IN_PLACE, 0, MPI_DATATYPE_NULL, recvbuf, recvcounts, displs,
          translateMPIType<T>());
    }

    void all2allv(
        const void *sendbuf, const int *sendcounts, const int *sdispls,
        MPI_Datatype sendtype, void *recvbuf, const int *recvcounts,
        const int *rdispls, MPI_Datatype recvtype) {
      int err;
      if ((err = MPI_Alltoallv(
               sendbuf, sendcounts, sdispls, sendtype, recvbuf, recvcounts,
               rdispls, recvtype, comm0)) != MPI_SUCCESS)
        throw MPI_Exception(err);
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
      int err;
      Request req;
      MPI_Request r;

      if ((err = MPI_IAlltoallv(
               sendbuf, sendcounts, sdispls, sendtype, recvbuf, recvcounts,
               rdispls, recvtype, comm0, &r)) != MPI_SUCCESS)
        throw MPI_Exception(err);

      req.set(r);
      return req;
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

  template <typename T>
  void MPICC_Window::put(int r, T v) {
    int err;

    MPI_Datatype t = translateMPIType<T>();
    lock();
    err = MPI_Put(&v, 1, t, rank, r, 1, t, win);
    unlock();
    if (err != MPI_SUCCESS)
      throw MPI_Exception(err);
  }

  template <typename T>
  T MPICC_Window::get(int r) {
    int err;
    T v;

    v = 0;

    MPI_Datatype t = translateMPIType<T>();
    lock();
    err = MPI_Get(&v, 1, t, rank, r, 1, t, win);
    unlock();
    if (err != MPI_SUCCESS) {
      throw MPI_Exception(err);
    }

    return v;
  }

  inline MPI_Communication *setupMPI() {
    int provided;
#ifdef _OPENMP
    std::cout << "setupMPI with threads (Nthreads=" << smp_get_max_threads()
              << ")" << std::endl;
    ::MPI_Init_thread(0, 0, MPI_THREAD_FUNNELED, &provided);
    if (provided < MPI_THREAD_FUNNELED) {
      std::cerr << "Cannot mix MPI and Threads here. Please recompile with "
                   "OpenMP or MPI switched off."
                << std::endl;
      ::MPI_Abort(MPI_COMM_WORLD, 99);
    }
#else
    std::cout << "setupMPI with *NO* threads" << std::endl;
    ::MPI_Init(0, 0);
#endif
    MPI_Communication *w = new MPI_Communication(MPI_COMM_WORLD);

    MPI_Communication::singleton = w;
    return w;
  }

  inline MPI_Communication *setupMPI(int &argc, char **&argv) {
    int provided;
#ifdef _OPENMP
    std::cout << "setupMPI with threads (Nthreads=" << smp_get_max_threads()
              << ")" << std::endl;
    ::MPI_Init_thread(&argc, &argv, MPI_THREAD_FUNNELED, &provided);
    if (provided < MPI_THREAD_FUNNELED) {
      std::cerr << "Cannot mix MPI and Threads here. Please recompile with "
                   "OpenMP or MPI switched off."
                << std::endl;
      ::MPI_Abort(MPI_COMM_WORLD, 99);
    }
#else
    std::cout << "setupMPI with *NO* threads" << std::endl;
    ::MPI_Init(&argc, &argv);
#endif
    MPI_Communication *w = new MPI_Communication(MPI_COMM_WORLD);

    MPI_Communication::singleton = w;
    return w;
  }

  // This a manual setup. Be warned that no safety check is done here.
  inline MPI_Communication *setupMPI(MPI_Comm existing) {
    MPI_Communication *w = new MPI_Communication(MPI_COMM_WORLD);
    MPI_Communication::singleton = w;
    return w;
  }

  inline void doneMPI() { ::MPI_Finalize(); }

}; // namespace LibLSS

#endif
