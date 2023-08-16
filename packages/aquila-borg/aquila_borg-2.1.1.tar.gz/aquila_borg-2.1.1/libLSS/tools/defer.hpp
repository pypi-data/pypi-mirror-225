/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/defer.hpp
    Copyright (C) 2018-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_TOOLS_DEFER_HPP
#  define __LIBLSS_TOOLS_DEFER_HPP

#  include <functional>
#  include <vector>
#  include "libLSS/tools/console.hpp"

namespace LibLSS {

  struct DeferTypes {
    enum State { WAIT, READY, ERROR };
    typedef std::function<void()> Function;
  };

  struct DeferState : DeferTypes {
    std::vector<Function> ready_f, error_f;
    State state;

    DeferState(State s) : state(s) {}
  };

  /**
   * @brief Add Future like concept for ARES.
   * If some state is not guaranteed to exist at a given time, a Defer can be
   * added to a class. Other class may subscribe to this Defer to receive asynchronously
   * an information on the change of status of the Defer.
   */
  class Defer : public DeferTypes {
  protected:
    std::shared_ptr<DeferState> state_p;

  public:
    /**
     * @brief Construct a new Defer object
     * 
     */
    Defer() : state_p(std::make_shared<DeferState>(WAIT)) {}

    /**
     * @brief Destroy the Defer object
     * 
     */
    ~Defer() {}

    /**
     * @brief Check whether the defer is still is waiting status.
     * 
     * @return true if it is still waiting.
     * @return false if it is READY or FAIL.
     */
    bool isWaiting() const { return state_p->state == WAIT; }

    /**
     * @brief Subscribe a new functor to be called when state is becoming ready.
     * 
     * @param f Functor to be called
     */
    void ready(Function f) {
      if (state_p->state == READY) {
        f();
        return;
      } else if (state_p->state == WAIT) {
        state_p->ready_f.push_back(f);
      }
    }

    /**
     * @brief Subscribe a new functor to be called when state is becoming fail.
     * 
     * @param f Functor to be called.
     */
    void fail(Function f) {
      if (state_p->state == ERROR) {
        f();
        return;
      } else if (state_p->state == WAIT) {
        state_p->error_f.push_back(f);
      }
    }

    /**
     * @brief Submit a state change to READY.
     * 
     */
    void submit_ready() {
      if (state_p->state == READY)
        return;

      Console::instance().c_assert(
          state_p->state == WAIT, "State has already changed (in submit_ready).");
      state_p->state = READY;
      for (auto &f : state_p->ready_f) {
        f();
      }
      state_p->ready_f.clear();
    }

    /**
     * @brief Submit a state change to FAIL.
     * 
     */
    void submit_error() {
      if (state_p->state == ERROR)
        return;

      Console::instance().c_assert(
          state_p->state == WAIT, "State has already changed (in submit_error).");
      state_p->state = ERROR;
      for (auto &f : state_p->error_f) {
        f();
      }
      state_p->error_f.clear();
    }
  };

  template <typename T>
  class PromisePointer {
  private:
    typedef std::shared_ptr<T> Pointer_t;
    Pointer_t ptr;

  public:
    Defer defer;

    Pointer_t get() { return ptr; }
    PromisePointer(Pointer_t starter) : ptr(starter) {}
  };

  template <typename T>
  auto make_promise_pointer(std::shared_ptr<T> p) {
    return PromisePointer<T>(p);
  }

} // namespace LibLSS

#endif
// ARES TAG: num_authors = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2018-2020
