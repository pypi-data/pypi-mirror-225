/*+
    ARES/HADES/BORG Package -- ./libLSS/mcmc/global_state.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef _GLOBAL_STATE_HPP
#define _GLOBAL_STATE_HPP

#include <boost/type_traits/is_base_of.hpp>
#include <boost/format.hpp>
#include <functional>
#include <set>
#include <typeindex>
#include <algorithm>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/mcmc/state_element.hpp"

namespace LibLSS {

  /**
   * @brief This is the class that manages the dictionnary that is saved in each MCMC/Restart file.
   * 
   * It is *not* copy-constructible.
   */
  class MarkovState {
  public:
    typedef std::map<std::string, bool> SaveMap;
    typedef std::map<std::string, StateElement *> StateMap;
    typedef std::map<std::string, std::type_index> TypeMap;
    typedef std::set<std::string> Requirements;

  private:
    SaveMap save_map;
    StateMap state_map, toProcess;
    TypeMap type_map;
    std::list<std::tuple<Requirements, std::function<void()>>> postLoad;
    std::set<std::string> loaded;

  public:
    MarkovState(MarkovState const &) = delete;

    /**
     * @brief Construct a new empty Markov State object.
     * 
     */
    MarkovState() {}

    /**
     * @brief Destroy the Markov State object.
     * 
     * All the elements stored in the dictionnary will be destroyed, as the ownership
     * is given the dictionnary implicitly when the element is added to it.
     */
    ~MarkovState() {
      for (StateMap::iterator i = state_map.begin(); i != state_map.end();
           ++i) {
        Console::instance().print<LOG_VERBOSE>(
            boost::format("Destroying %s") % i->first);
        delete i->second;
      }
      save_map.clear();
    }

    template <typename T>
    static void check_class() {
      BOOST_MPL_ASSERT_MSG(
          (boost::is_base_of<StateElement, T>::value), T_is_not_a_StateElement,
          ());
    }

    /**
     * @brief Function to access by its name an element stored in the dictionnary.
     *  
     * This function makes a lookup and a dynamic cast to the specified template "StateElement".
     * It tries to find the indicated state element by name. If it fails an error is thrown.
     * A dynamic cast is then issued to ensure that the stored type is the same as the requested one.
     * 
     * @tparam T     type of the element, cast will be checked
     * @param name   string id of the element
     * @return T*    pointer to the element
     */
    template <typename T>
    T *get(const std::string &name) {
      check_class<T>();
      StateMap::iterator i = state_map.find(name);
      if (i == state_map.end() || i->second == 0) {
        error_helper<ErrorBadState>(
            boost::format("Invalid access to %s") % name);
      }
      T *ptr = dynamic_cast<T *>(i->second);
      if (ptr == 0) {
        error_helper<ErrorBadCast>(
            boost::format("Bad cast in access to %s") % name);
      }
      return ptr;
    }

    /**
     * @brief Access using a boost::format object.
     * 
     * @tparam T 
     * @param f 
     * @return T* 
     */
    template <typename T>
    T *get(const boost::format &f) {
      return get<T>(f.str());
    }

    static void _format_expansion(boost::format &f) {}

    template <typename A, typename... U>
    static void _format_expansion(boost::format &f, A &&a, U &&... u) {
      _format_expansion(f % a, u...);
    }

    template <typename T, typename... Args>
    T *formatGet(std::string const &s, Args &&... args) {
      boost::format f(s);
      _format_expansion(f, std::forward<Args>(args)...);
      return get<T>(f);
    }

    template <typename T>
    const T *get(const boost::format &f) const {
      return get<T>(f.str());
    }

    template <typename T>
    const T *get(const std::string &name) const {
      check_class<T>();
      StateMap::const_iterator i = state_map.find(name);
      if (i == state_map.end() || i->second == 0) {
        error_helper<ErrorBadState>(
            boost::format("Invalid access to %s") % name);
      }

      const T *ptr = dynamic_cast<const T *>(i->second);
      if (ptr == 0) {
        error_helper<ErrorBadCast>(
            boost::format("Bad cast in access to %s") % name);
      }
      return ptr;
    }

    /**
     * @brief Check existence of an element in the dictionnary.
     * 
     * @param name   string id of the element
     * @return true  if it exists
     * @return false if it does not exist
     */
    bool exists(const std::string &name) const {
      return state_map.find(name) != state_map.end();
    }

    /**
     * @brief Access an element through operator [] overload.
     * 
     * @param name 
     * @return StateElement& 
     */
    StateElement &operator[](const std::string &name) {
      return *get<StateElement>(name);
    }

    const StateElement &operator[](const std::string &name) const {
      return *get<StateElement>(name);
    }

    std::type_index getStoredType(const std::string &name) const {
      auto iter = type_map.find(name);
      if (iter == type_map.end())
        error_helper<ErrorBadState>(
            "Unknown entry " + name + " during type query");
      return iter->second;
    }

    /**
     * @brief Add an element in the dictionnary.
     * 
     * @param name  string id of the new element
     * @param elt   Object to add in the dictionnary. The ownership is transferred to MarkovState.
     * @param write_to_snapshot indicate, if true, that the element has to be written in mcmc files
     * @return StateElement* the same object as "elt", used to daisy chain calls.
     */
    template <typename T>
    T *newElement(
        const std::string &name, T *elt,
        const bool &write_to_snapshot = false) {
      static_assert(
          std::is_base_of<StateElement, T>::value,
          "newElement accepts only StateElement based objects");
      state_map[name] = elt;
      type_map.insert(std::pair<std::string, std::type_index>(
          name, std::type_index(typeid(T))));
      toProcess[name] = elt;
      elt->name = name;
      set_save_in_snapshot(name, write_to_snapshot);
      return elt;
    }

    /**
     * @brief Add an element in the dictionnary.
     * 
     * @param f   boost::format object used to build the string-id
     * @param elt  Object to add in the dictionnary. The ownership is transferred to MarkovState.
     * @param write_to_snapshot indicate, if true, that the element has to be written in mcmc files
     * @return StateElement* the same object as "elt", used to daisy chain calls.
     */
    template <typename T>
    T *newElement(
        const boost::format &f, T *elt, const bool &write_to_snapshot = false) {
      return newElement(f.str(), elt, write_to_snapshot);
    }

    /**
     * @brief Get the content of a series of variables into a static array
     * That function is an helper to retrieve the value of a series "variable0",
     * "variable1", ..., "variableQ" of ScalarElement of type Scalar (with Q=N-1).
     * Such a case is for the length:
     * @code
     *  double L[3];
     *  state.getScalarArray<double, 3>("L", L);
     * @endcode
     * This will retrieve L0, L1 and L2 and store their value (double float) in
     * L[0], L[1], L2].
     * 
     * @tparam Scalar inner type of the variable to be retrieved in the dictionnary 
     * @tparam N      number of elements
     * @param prefix  prefix for these variables
     * @param scalars output scalar array
     */
    template <typename Scalar, size_t N, typename ScalarArray>
    void getScalarArray(const std::string &prefix, ScalarArray &&scalars) {
      for (unsigned int i = 0; i < N; i++) {
        scalars[i] = getScalar<Scalar>(prefix + std::to_string(i));
      }
    }

    ///@deprecated
    template <typename Scalar>
    Scalar &getSyncScalar(const std::string &name) {
      return this->template get<SyncableScalarStateElement<Scalar>>(name)
          ->value;
    }

    ///@deprecated
    template <typename Scalar>
    Scalar &getSyncScalar(const boost::format &name) {
      return this->template getSyncScalar<Scalar>(name.str());
    }

    /**
     * @brief Get the value of a scalar object.
     * 
     * @tparam Scalar 
     * @param name 
     * @return Scalar& 
     */
    template <typename Scalar>
    Scalar &getScalar(const std::string &name) {
      return this->template get<ScalarStateElement<Scalar>>(name)->value;
    }

    template <typename Scalar>
    Scalar &getScalar(const boost::format &name) {
      return this->template getScalar<Scalar>(name.str());
    }

    template <typename Scalar, typename... U>
    Scalar &formatGetScalar(std::string const &name, U &&... u) {
      return this
          ->template formatGet<ScalarStateElement<Scalar>>(
              name, std::forward<U>(u)...)
          ->value;
    }

    template <typename Scalar>
    ScalarStateElement<Scalar> *newScalar(
        const std::string &name, Scalar x,
        const bool &write_to_snapshot = false) {
      ScalarStateElement<Scalar> *elt = new ScalarStateElement<Scalar>();

      elt->value = x;
      newElement(name, elt, write_to_snapshot);
      return elt;
    }

    template <typename Scalar>
    ScalarStateElement<Scalar> *newScalar(
        const boost::format &name, Scalar x,
        const bool &write_to_snapshot = false) {
      return this->newScalar(name.str(), x, write_to_snapshot);
    }

    ///@deprecated
    template <typename Scalar>
    SyncableScalarStateElement<Scalar> *newSyScalar(
        const std::string &name, Scalar x,
        const bool &write_to_snapshot = false) {
      SyncableScalarStateElement<Scalar> *elt =
          new SyncableScalarStateElement<Scalar>();

      elt->value = x;
      newElement(name, elt, write_to_snapshot);
      return elt;
    }

    ///@deprecated
    template <typename Scalar>
    SyncableScalarStateElement<Scalar> *newSyScalar(
        const boost::format &name, Scalar x,
        const bool &write_to_snapshot = false) {
      return this->newSyScalar(name.str(), x, write_to_snapshot);
    }

    ///@deprecated
    void mpiSync(MPI_Communication &comm, int root = 0) {
      namespace ph = std::placeholders;
      for (StateMap::iterator i = state_map.begin(); i != state_map.end();
           ++i) {
        i->second->syncData(std::bind(
            &MPI_Communication::broadcast, comm, ph::_1, ph::_2, ph::_3, root));
      }
    }

    void set_save_in_snapshot(const std::string &name, const bool save) {
      save_map[name] = save;
    }

    void set_save_in_snapshot(const boost::format &name, const bool save) {
      set_save_in_snapshot(name.str(), save);
    }

    bool get_save_in_snapshot(const std::string &name) {
      SaveMap::const_iterator i = save_map.find(name);
      if (i == save_map.end()) {
        error_helper<ErrorBadState>(
            boost::format("Invalid access to %s") % name);
      }
      return i->second;
    }

    bool get_save_in_snapshot(const boost::format &name) {
      return get_save_in_snapshot(name.str());
    }

    /**
     * @brief Save the full content of the dictionnary into the indicated HDF5 group.
     * 
     * @param fg HDF5 group/file to save the state in.
     */
    void saveState(H5_CommonFileGroup &fg) {
      ConsoleContext<LOG_DEBUG> ctx("saveState");
      H5::Group g_scalar = fg.createGroup("scalars");
      for (auto &&i : state_map) {
        ctx.print("Saving " + i.first);
        if (i.second->isScalar())
          i.second->saveTo(g_scalar);
        else {
          H5::Group g = fg.createGroup(i.first);
          i.second->saveTo(g);
        }
      }
    }

    /**
     * @brief Save the full content of the dictionnary into the indicated HDF5 group.
     * This is the MPI parallel variant.
     * 
     * @param fg HDF5 group/file to save the state in.
     */
    void mpiSaveState(
        std::shared_ptr<H5_CommonFileGroup> fg, MPI_Communication *comm,
        bool reassembly, const bool write_snapshot = false) {
      ConsoleContext<LOG_VERBOSE> ctx("mpiSaveState");
      H5::Group g_scalar;
      boost::optional<H5_CommonFileGroup &> g_scalar_opt;

      if (fg) {
        g_scalar = fg->createGroup("scalars");
        g_scalar_opt = g_scalar;
      }

      for (auto &&i : state_map) {
        if (write_snapshot && (!get_save_in_snapshot(i.first))) {
          ctx.print("Skip saving " + i.first);
          continue;
        }
        ctx.print("Saving " + i.first);
        if (i.second->isScalar())
          i.second->saveTo(g_scalar_opt, comm, reassembly);
        else {
          H5::Group g;
          boost::optional<H5_CommonFileGroup &> g_opt;
          if (fg) {
            g = fg->createGroup(i.first);
            g_opt = g;
          }
          i.second->saveTo(g_opt, comm, reassembly);
        }
      }
    }

    void restoreStateWithFailure(H5_CommonFileGroup &fg) {
      Console &cons = Console::instance();
      H5::Group g_scalar = fg.openGroup("scalars");
      for (StateMap::iterator i = state_map.begin(); i != state_map.end();
           ++i) {
        cons.print<LOG_VERBOSE>("Attempting to restore " + i->first);
#if H5_VERSION_GE(1, 10, 1)
        if (!g_scalar.nameExists(i->first)) {
          cons.print<LOG_WARNING>("Failure to restore");
          continue;
        }
#endif
        if (i->second->isScalar())
          // Partial is only valid for 'scalar' types.
          i->second->loadFrom(g_scalar, false);
        else {
          H5::Group g = fg.openGroup(i->first);
          i->second->loadFrom(g);
        }
      }
    }

    // Function to launch another function once all indicated requirements have been loaded from the
    // restart file.
    void subscribePostRestore(
        Requirements const &requirements, std::function<void()> f) {
      if (std::includes(
              requirements.begin(), requirements.end(), loaded.begin(),
              loaded.end())) {
        f();
        return;
      }
      postLoad.push_back(std::make_tuple(requirements, f));
    }

    void triggerPostRestore(std::string const &n) {
      loaded.insert(n);
      auto i = postLoad.begin();
      while (i != postLoad.end()) {
        auto const &req = std::get<0>(*i);
        if (!std::includes(
                req.begin(), req.end(), loaded.begin(), loaded.end())) {
          ++i;
          continue;
        }
        std::get<1> (*i)();
        auto j = i;
        ++j;
        postLoad.erase(i);
        i = j;
      }
    }

    void restoreState(
        H5_CommonFileGroup &fg, bool partial = false, bool loadSnapshot = false,
        bool acceptFailure = false) {
      Console &cons = Console::instance();
      H5::Group g_scalar = fg.openGroup("scalars");
      StateMap currentMap = state_map; // Protect against online modifications

      do {
        for (StateMap::iterator i = currentMap.begin(); i != currentMap.end();
             ++i) {
          if (loadSnapshot && !get_save_in_snapshot(i->first))
            continue;

          cons.print<LOG_VERBOSE>("Restoring " + i->first);
#if H5_VERSION_GE(1, 10, 1)
          if (acceptFailure && !g_scalar.nameExists(i->first)) {
            cons.print<LOG_WARNING>("Failure to restore. Skipping.");
            continue;
          }
#endif
          if (i->second->isScalar())
            // Partial is only valid for 'scalar' types.
            i->second->loadFrom(g_scalar, partial);
          else {
            auto g = fg.openGroup(i->first);
            i->second->loadFrom(g);
          }
          triggerPostRestore(i->first);
        }
        currentMap = toProcess;
        toProcess.clear();
      } while (currentMap.size() > 0);

      // Clear up all pending
      if (postLoad.size() > 0) {
        cons.print<LOG_ERROR>("Some post-restore triggers were not executed.");
        MPI_Communication::instance()->abort();
      }
      loaded.clear();
      postLoad.clear();
    }
  };

  /** @example example_markov_state.cpp
   *  This is an example of how to use the MarkovState class.
   */

}; // namespace LibLSS

#endif
