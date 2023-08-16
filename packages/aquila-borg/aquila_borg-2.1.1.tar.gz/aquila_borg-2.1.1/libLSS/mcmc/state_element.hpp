/*+
    ARES/HADES/BORG Package -- ./libLSS/mcmc/state_element.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef _LIBLSS_STATE_ELT_HPP
#define _LIBLSS_STATE_ELT_HPP

#include <Eigen/Core>
#include "libLSS/tools/align_helper.hpp"
#include "libLSS/mpi/generic_mpi.hpp"
#include <boost/function.hpp>
#include <boost/multi_array.hpp>
#include <boost/format.hpp>
#include <boost/lexical_cast.hpp>
#include <string>
#include <H5Cpp.h>
#include <iostream>
#include <CosmoTool/hdf5_array.hpp>
#include <map>
#include <functional>
#include "libLSS/tools/errors.hpp"
#include "libLSS/tools/memusage.hpp"
#include "libLSS/tools/hdf5_type.hpp"
#include "libLSS/tools/defer.hpp"

namespace LibLSS {

  /**
     * @brief Generic Markov Chain State element
     * This is the base class for other more strange elements
     * 
     */
  class StateElement {
  protected:
    std::string name;
    typedef std::function<void(void *, int, MPI_Datatype)> SyncFunction;
    typedef std::function<void()> NotifyFunction;

  protected:
    /**
         * @brief Construct a new State Element object
         * 
         */
    StateElement() : name("_unknown_") {}

    friend class MarkovState;
    void checkName() {
      if (name == "_unknown_") {
        std::cerr << "Name of a state element is undefined" << std::endl;
        abort();
      }
    }

  public:
    Defer deferLoad, deferInit;

    /**
     * @brief Destroy the State Element object
     * 
     */
    virtual ~StateElement();

    /**
     * @brief Register a functor get notifications when this element is finished being loaded.
     * @deprecated Use deferLoad directly
     * 
     * @param f the functor, must support copy-constructible.
     * @sa loaded
     */
    void subscribeLoaded(NotifyFunction f) { deferLoad.ready(f); }

    /**
     * @brief Send a message that the element has been loaded.
     * @deprecated Use deferLoad directly.
     * @sa subscribeLoaded
     */
    void loaded() { deferLoad.submit_ready(); }

    /**
     * @brief Get the name of this state element. This is used to store it in file.
     * 
     * @return const std::string& 
     */
    const std::string &getName() const { return name; }

    /**
     * @brief Check if this element is a scalar.
     * 
     * @return true if it is a scalar, i.e. trivially serializable
     * @return false it it is not, requires a lot more operations to (de)serialize.
     */
    virtual bool isScalar() const { return false; }

    bool updated() { return false; }

    /**
     * @brief Save the element to an HDF5 group, only one core is using the file.
     *
     */
    virtual void saveTo(
        boost::optional<H5_CommonFileGroup &> fg, MPI_Communication *comm = 0,
        bool partialSave = true) = 0;

    /**
     * @brief Save the element to an HDF5 group.
     * 
     * @param fg an HDF5 group/file
     * @param comm an MPI communicator
     * @param partialSave whether only the partial save is requested (i.e. generate restart file).
     */
    virtual void saveTo(
        H5_CommonFileGroup &fg, MPI_Communication *comm = 0,
        bool partialSave = true) {
      boost::optional<H5_CommonFileGroup &> o_fg = fg;
      saveTo(o_fg, comm, partialSave);
    }

    virtual void saveTo2(
        std::shared_ptr<H5_CommonFileGroup> fg, MPI_Communication *comm = 0,
        bool partialSave = true) {
      boost::optional<H5_CommonFileGroup &> o_fg;
      if (fg)
        o_fg = *fg;
      saveTo(o_fg, comm, partialSave);
    }

    /**
     * @brief 
     * 
     * @param fg 
     * @param partialLoad 
     */
    virtual void loadFrom(H5_CommonFileGroup &fg, bool partialLoad = true) = 0;
    virtual void syncData(SyncFunction f) = 0;
  };

  /* Generic array template class for Markov Chain state element. It supports all scalars
    * and complex derived types.
    */
  template <class AType, bool NeedReassembly = false>
  class GenericArrayStateElement : public StateElement {
  public:
    enum { Reassembly = NeedReassembly };
    typedef AType ArrayType;
    typedef typename ArrayType::element element;
    typedef typename ArrayType::index_gen index_gen;
    std::vector<hsize_t> real_dims;
    std::shared_ptr<ArrayType> array;
    bool realDimSet;
    bool resetOnSave;
    element reset_value;
    bool auto_resize;

    bool requireReassembly() const { return (bool)Reassembly == true; }
    void setResetOnSave(const element &_reset_value) {
      this->reset_value = _reset_value;
      resetOnSave = true;
    }
    void setAutoResize(bool do_resize) { auto_resize = do_resize; }

    template <typename ExtentDim>
    void setRealDims(const ExtentDim &d) {
      Console::instance().c_assert(
          d.size() == real_dims.size(), "Invalid dimension size");
      std::copy(d.begin(), d.end(), real_dims.begin());
      realDimSet = true;
    }

    GenericArrayStateElement()
        : StateElement(), real_dims(ArrayType::dimensionality),
          realDimSet(false), resetOnSave(false), auto_resize(false) {}
    virtual ~GenericArrayStateElement() {}

    virtual bool isScalar() const { return true; }

    virtual void saveTo(
        boost::optional<H5_CommonFileGroup &> fg, MPI_Communication *comm = 0,
        bool partialSave = true) {
      checkName();
      try {
        if (!requireReassembly() || partialSave) {
          ConsoleContext<LOG_DEBUG> ctx("saveTo(): saving variable " + name);
          if (partialSave || (comm != 0 && comm->rank() == 0)) {
            ctx.print("partialSave or rank==0");
            if (!fg) {
              error_helper<ErrorBadState>(
                  "saveTo() requires a valid HDF5 handle on this core.");
            }
            CosmoTool::hdf5_write_array(*fg, name, *array);
          } else {
            ctx.print("Non-root rank and not partial save. Just passthrough.");
          }
        } else {
          CosmoTool::get_hdf5_data_type<element> HT;
          Console::instance().c_assert(
              comm != 0, "Array need reassembly and no communicator given");
          Console::instance().c_assert(
              realDimSet,
              "Real dimensions of the array over communicator is not set for " +
                  this->getName());
          std::vector<hsize_t> remote_bases(ArrayType::dimensionality);
          std::vector<hsize_t> remote_dims(ArrayType::dimensionality);
          MPI_Datatype dt = translateMPIType<hsize_t>();
          MPI_Datatype et = translateMPIType<element>();

          ConsoleContext<LOG_DEBUG> ctx("reassembling of variable " + name);

          if (comm->rank() == 0) {
            if (!fg)
              error_helper<ErrorBadState>(
                  "saveTo() requires a valid HDF5 handle on this core.");

            ctx.print("Writing rank 0 data first. Dimensions = ");
            for (size_t n = 0; n < real_dims.size(); n++)
              ctx.print(boost::lexical_cast<std::string>(real_dims[n]));
            CosmoTool::hdf5_write_array(
                *fg, name, *array, HT.type(), real_dims, true, true);

            ctx.print("Grabbing other rank data");
            for (int r = 1; r < comm->size(); r++) {
              ArrayType a;

              ctx.print(boost::format("Incoming data from rank %d") % r);
              comm->recv(
                  remote_dims.data(), ArrayType::dimensionality, dt, r, 0);
              comm->recv(
                  remote_bases.data(), ArrayType::dimensionality, dt, r, 1);
              a.resize(
                  CosmoTool::hdf5_extent_gen<ArrayType::dimensionality>::build(
                      remote_dims.data()));
              a.reindex(remote_bases);
              comm->recv(a.data(), a.num_elements(), et, r, 2);
              CosmoTool::hdf5_write_array(
                  *fg, name, a, HT.type(), real_dims, false, true);
            }
          } else {
            ctx.print("Sending data");
            comm->send(array->shape(), ArrayType::dimensionality, dt, 0, 0);
            comm->send(
                array->index_bases(), ArrayType::dimensionality, dt, 0, 1);
            comm->send(array->data(), array->num_elements(), et, 0, 2);
          }
        }
        if (resetOnSave)
          fill(reset_value);
      } catch (const H5::Exception &e) {
        error_helper<ErrorIO>(e.getDetailMsg());
      }
    }

    virtual void loadFrom(H5_CommonFileGroup &fg, bool partialLoad = false) {
      checkName();
      try {
        if (!requireReassembly() || !partialLoad) {
          ConsoleContext<LOG_DEBUG> ctx("loadFrom full");
          ctx.print(
              boost::format("loadFrom(reassembly=%d,partialLoad=%d,autoresize=%"
                            "d): loading variable %s") %
              requireReassembly() % partialLoad % auto_resize % name);
          ctx.print("partialSave or rank==0");
          CosmoTool::hdf5_read_array(fg, name, *array, auto_resize);
        } else {
          Console::instance().c_assert(
              realDimSet,
              "Real dimensions of the array over communicator is not set for " +
                  this->getName());
          std::vector<hsize_t> remote_bases(ArrayType::dimensionality);
          std::vector<hsize_t> remote_dims(ArrayType::dimensionality);

          ConsoleContext<LOG_DEBUG> ctx("dissassembling of variable " + name);
          CosmoTool::hdf5_read_array(fg, name, *array, false, true);
        }
      } catch (const CosmoTool::InvalidDimensions &) {
        error_helper<ErrorBadState>(
            boost::format("Incompatible array size loading '%s'") % getName());
      } catch (const H5::GroupIException &) {
        error_helper<ErrorIO>(
            "Could not open variable " + getName() + " in state file");
      } catch (const H5::DataSetIException &error) {
        error_helper<ErrorIO>(
            "Could not open variable " + getName() + " in state file");
      }
      loaded();
    }

    virtual void syncData(SyncFunction f) {
      typename ArrayType::size_type S;
      f(array->data(), array->num_elements(),
        translateMPIType<typename AType::element>());
    }

    virtual void fill(const element &v) {
//#pragma omp simd
#pragma omp parallel for
      for (size_t i = 0; i < array->num_elements(); i++)
        array->data()[i] = v;
    }
  };

  template <
      typename T, std::size_t DIMENSIONS,
      typename Allocator = LibLSS::track_allocator<T>,
      bool NeedReassembly = false>
  class ArrayStateElement
      : public GenericArrayStateElement<
            boost::multi_array<T, DIMENSIONS, Allocator>, NeedReassembly> {
    typedef GenericArrayStateElement<
        boost::multi_array<T, DIMENSIONS, Allocator>, NeedReassembly>
        super_type;

  public:
    typedef typename super_type::ArrayType ArrayType;
    typedef typename boost::multi_array_ref<T, DIMENSIONS> RefArrayType;
    typedef typename super_type::index_gen index_gen;

    enum { AlignState = DetectAlignment<Allocator>::Align };
    typedef Eigen::Array<T, Eigen::Dynamic, 1> E_Array;
    typedef Eigen::Map<E_Array, AlignState> MapArray;

    template <typename ExtentList>
    ArrayStateElement(
        const ExtentList &extents, const Allocator &allocator = Allocator(),
        const boost::general_storage_order<DIMENSIONS> &ordering =
            boost::c_storage_order())
        : super_type() {
      this->array = std::make_shared<ArrayType>(extents, ordering, allocator);
      Console::instance().print<LOG_DEBUG>(
          std::string("Creating array which is ") +
          ((((int)AlignState == (int)Eigen::Aligned) ? "ALIGNED"
                                                     : "UNALIGNED")));
    }

    MapArray eigen() {
      return MapArray(this->array->data(), this->array->num_elements());
    }

    virtual void fill(const typename super_type::element &v) {
      eigen().fill(v);
    }

    // This is unsafe. Use it with precaution
    void unsafeSetName(const std::string &n) { this->name = n; }
  };

  template <typename T, std::size_t DIMENSIONS>
  class RefArrayStateElement
      : public GenericArrayStateElement<boost::multi_array_ref<T, DIMENSIONS>> {
  public:
    typedef boost::multi_array_ref<T, DIMENSIONS> ArrayType;
    typedef boost::multi_array_ref<T, DIMENSIONS> RefArrayType;

    template <typename ExtentList>
    RefArrayStateElement(
        T *data, const ExtentList &extents,
        const boost::general_storage_order<DIMENSIONS> &ordering =
            boost::c_storage_order())
        : StateElement() {
      this->array = std::make_shared<ArrayType>(data, extents);
    }
  };

  template <typename U>
  struct _scalar_writer {
    template <typename DT>
    static inline void write(H5::DataSet &dataset, U &v, DT dt) {
      dataset.write(&v, dt.type());
    }

    template <typename DT>
    static inline void read(H5::DataSet &dataset, U &v, DT dt) {
      dataset.read(&v, dt.type());
    }
  };

  template <>
  struct _scalar_writer<std::string> {
    template <typename DT>
    static inline void write(H5::DataSet &dataset, std::string &v, DT dt) {
      dataset.write(v, dt.type());
    }

    template <typename DT>
    static inline void read(H5::DataSet &dataset, std::string &v, DT dt) {
      dataset.read(v, dt.type());
    }
  };

  /* Generic scalar Markov State element. */
  template <typename T>
  class ScalarStateElement : public StateElement {
  public:
    T value;
    T reset_value;
    bool resetOnSave;
    bool doNotRestore;

    ScalarStateElement()
        : StateElement(), value(), reset_value(), resetOnSave(false),
          doNotRestore(false) {}
    virtual ~ScalarStateElement() {}

    void setDoNotRestore(bool doNotRestore) {
      this->doNotRestore = doNotRestore;
    }
    void setResetOnSave(const T &_reset_value) {
      this->reset_value = _reset_value;
      resetOnSave = true;
    }

    virtual void saveTo(
        boost::optional<H5_CommonFileGroup &> fg, MPI_Communication *comm = 0,
        bool partialSave = true) {
      CosmoTool::get_hdf5_data_type<T> hdf_data_type;
      std::vector<hsize_t> dimensions(1);
      dimensions[0] = 1;

      if (partialSave || (comm != 0 && comm->rank() == 0)) {
        checkName();
        H5::DataSpace dataspace(1, dimensions.data());
        H5::DataSet dataset =
            (*fg).createDataSet(name, hdf_data_type.type(), dataspace);

        _scalar_writer<T>::write(dataset, value, hdf_data_type);
        if (resetOnSave)
          value = reset_value;
      }
    }

    virtual void loadFrom(H5_CommonFileGroup &fg, bool partialLoad = true) {
      CosmoTool::get_hdf5_data_type<T> hdf_data_type;
      std::vector<hsize_t> dimensions(1);
      H5::DataSet dataset;

      if (doNotRestore) {
        return;
      }

      dimensions[0] = 1;

      checkName();
      try {
        dataset = fg.openDataSet(name);
      } catch (const H5::GroupIException &) {
        error_helper<ErrorIO>(
            "Could not find variable " + name + " in state file.");
      }
      H5::DataSpace dataspace = dataset.getSpace();
      hsize_t n;

      if (dataspace.getSimpleExtentNdims() != 1)
        error_helper<ErrorIO>("Invalid stored dimension for " + getName());

      dataspace.getSimpleExtentDims(&n);
      if (n != 1)
        error_helper<ErrorIO>("Invalid stored dimension for " + getName());

      _scalar_writer<T>::read(dataset, value, hdf_data_type);
      loaded();
    }

    operator T() { return value; }

    virtual bool isScalar() const { return true; }

    virtual void syncData(SyncFunction f) {
      error_helper<ErrorBadState>(
          "MPI synchronization not supported by this type");
    }
  };

  template <typename T>
  class SyncableScalarStateElement : public ScalarStateElement<T> {
  public:
    typedef typename ScalarStateElement<T>::SyncFunction SyncFunction;

    virtual void syncData(SyncFunction f) {
      f(&this->value, 1, translateMPIType<T>());
    }
  };

  template <typename T>
  class SharedObjectStateElement : public StateElement {
  public:
    std::shared_ptr<T> obj;

    SharedObjectStateElement() : StateElement() {}
    SharedObjectStateElement(std::shared_ptr<T> &src)
        : StateElement(), obj(src) {}
    SharedObjectStateElement(std::shared_ptr<T> &&src)
        : StateElement(), obj(src) {}
    virtual ~SharedObjectStateElement() {}

    virtual void saveTo(
        boost::optional<CosmoTool::H5_CommonFileGroup &> fg,
        MPI_Communication *comm = 0, bool partialSave = true) {
      if (fg)
        obj->save(*fg);
    }

    virtual void
    loadFrom(CosmoTool::H5_CommonFileGroup &fg, bool partialSave = true) {
      obj->restore(fg);
      loaded();
    }

    operator T &() { return *obj; }

    T &get() { return *obj; }
    const T &get() const { return *obj; }

    virtual void syncData(SyncFunction f) {}
  };

  template <typename T, bool autofree>
  class ObjectStateElement : public StateElement {
  public:
    T *obj;

    ObjectStateElement() : StateElement() {}
    ObjectStateElement(T *o) : StateElement(), obj(o) {}
    virtual ~ObjectStateElement() {
      if (autofree)
        delete obj;
    }

    virtual void saveTo(
        boost::optional<H5_CommonFileGroup &> fg, MPI_Communication *comm = 0,
        bool partialSave = true) {
      if (fg)
        obj->save(*fg);
    }

    virtual void loadFrom(H5_CommonFileGroup &fg, bool partialSave = true) {
      obj->restore(fg);
      loaded();
    }

    operator T &() { return *obj; }

    T &get() { return *obj; }
    const T &get() const { return *obj; }

    virtual void syncData(SyncFunction f) {}
  };

  template <class T>
  class TemporaryElement : public StateElement {
  protected:
    T obj;

  public:
    TemporaryElement(T const &a) : obj(a) {}
    TemporaryElement(T &&a) : obj(a) {}

    operator T &() { return obj; }

    T &get() { return obj; }
    const T &get() const { return obj; }

    virtual void saveTo(
        boost::optional<H5_CommonFileGroup &> fg, MPI_Communication *comm = 0,
        bool partialSave = true) {}

    virtual void loadFrom(H5_CommonFileGroup &fg, bool partialSave = true) {}

    virtual void syncData(SyncFunction f) {}
  };

  template <class T>
  class RandomStateElement : public StateElement {
  protected:
    std::shared_ptr<T> rng;

  public:
    RandomStateElement(T *generator, bool handover_ = false) {
      if (handover_) {
        rng = std::shared_ptr<T>(generator, [](T *a) { delete a; });
      } else {
        rng = std::shared_ptr<T>(generator, [](T *a) {});
      }
    }
    RandomStateElement(std::shared_ptr<T> generator) : rng(generator) {}
    virtual ~RandomStateElement() {}

    const T &get() const { return *rng; }
    T &get() { return *rng; }

    virtual void saveTo(
        boost::optional<H5_CommonFileGroup &> fg, MPI_Communication *comm = 0,
        bool partialSave = true) {
      if (fg)
        rng->save(*fg);
    }

    virtual void loadFrom(H5_CommonFileGroup &fg, bool partialLoad = false) {
      rng->restore(fg, partialLoad);
      loaded();
    }

    virtual void syncData(SyncFunction f) {}
  };
}; // namespace LibLSS

#endif
