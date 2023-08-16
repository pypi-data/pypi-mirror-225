/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/console.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#ifndef __LIBLSS_CONSOLE_HPP
#define __LIBLSS_CONSOLE_HPP

// Log traits automatically available when console is loaded
#include <boost/format.hpp>
#include <boost/chrono.hpp>
#include <iostream>
#include <fstream>
#include <list>
#include <boost/chrono.hpp>
#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/log_traits.hpp"
#include "libLSS/tools/static_auto.hpp"
#include "libLSS/tools/function_name.hpp"

namespace LibLSS {

  class Console;

  namespace details {

    class ProgressBase {
    private:
      int numElements;
      int current;
      int percent;
      int iLevel;
      int step;
      std::string msg;
      boost::chrono::system_clock::time_point start;

      friend class Console;

    protected:
      Console *console;

      ProgressBase(Console *c, const std::string &m, int num, int _step);

      virtual ~ProgressBase() {}

    public:
      void destroy();

      virtual void print(const std::string &s) = 0;
      void update(int i);
    };
  }; // namespace details

  template <typename T>
  class Progress : public details::ProgressBase {
  private:
    Progress(Console *c, const std::string &m, int num, int _step)
        : ProgressBase(c, m, num, _step) {}

    friend class Console;

  public:
    virtual void print(const std::string &s);
  };

  class Console;

  namespace timings {
    void record(std::string const &n, double t);
    void trigger_dump();
    void reset();
    void set_file_pattern(std::string const &pattern);
  } // namespace timings

  namespace details {
    class ConsoleContextBase;

    extern thread_local ConsoleContextBase *currentContext;

    class ConsoleContextBase {
    protected:
      ConsoleContextBase *previousContext;
#ifdef LIBLSS_TIMED_CONTEXT
      boost::chrono::system_clock::time_point start_context;
      std::string ctx_msg, short_msg;
      void record_timing(boost::chrono::duration<double> const &timing) {
        timings::record(ctx_msg, timing.count());
      }
      void record_self_timing(
          boost::chrono::system_clock::time_point const &timing) {}
#else
      void record_timing(boost::chrono::duration<double> const &) {}
      void record_self_timing(boost::chrono::duration<double> const &) {}
#endif
    public:
#ifdef LIBLSS_TIMED_CONTEXT
      std::string const &getMessage() const { return ctx_msg; }
#else
      std::string const &getMessage() const {
        static std::string s = "";
        return s;
      }
#endif
      static inline ConsoleContextBase &current() { return *currentContext; }

      ConsoleContextBase();
      ~ConsoleContextBase();
    };

    class ConsoleContextDummy {
    public:
      std::string getMessage() const { return std::string(); }
      static inline ConsoleContextBase &current() { return *currentContext; }

      template <typename... Args>
      void print(const Args &... args) {}
      template <typename T2, typename... Args>
      void print2(const Args &... args) {}
      template <typename... Args>
      void format(Args &&... args) {}
      template <typename T2, typename... Args>
      void format2(Args &&... args) {}

      ConsoleContextDummy() {}
      ~ConsoleContextDummy() {}
    };

    template <typename T>
    class ConsoleContext : public ConsoleContextBase {
    private:
      ConsoleContext(ConsoleContext const &) {}

    public:
      ConsoleContext(std::string const &code_name);
      ConsoleContext(
          std::string const &code_name, std::string const &short_name);
      ~ConsoleContext();

      template <typename... Args>
      void format(Args &&... args);
      template <typename T2, typename... Args>
      void format2(Args &&... args);
      template <typename... Args>
      void print(const Args &... args);
      template <typename T2, typename... Args>
      void print2(const Args &... args);
    };
  } // namespace details

  using details::ConsoleContext;

  class Console {
  protected:
    typedef std::list<details::ProgressBase *> PList;

    std::ofstream outputFile;
    int verboseLevel;
    int logfileVerboseLevel;
    int indentLevel;
    bool noColor;
    typedef std::function<void(int, std::string const &)> OutputHijacker;
    OutputHijacker hijackOutput;
    std::string indentString;
    PList all_progress;

    friend class details::ProgressBase;

    template <typename T>
    friend class ConsoleContext;

    Console(int verbose = DEFAULT_LOG_LEVEL::verboseLevel, int indent = 0)
        : verboseLevel(verbose), logfileVerboseLevel(LOG_DEBUG::verboseLevel),
          indentLevel(indent), noColor(false) {}

  private:
    void cleanProgress(details::ProgressBase *b) {
      PList::iterator i = all_progress.begin();

      while (i != all_progress.end()) {
        if ((*i) == b)
          i = all_progress.erase(i);
        else
          ++i;
      }
    }

  public:
    static Console &instance() {
      static Console singleton;
      return singleton;
    }

    void setSeparateStream(OutputHijacker f) { hijackOutput = f; }

    void setNoColor(bool nc) { noColor = nc; }

    void outputToFile(const std::string &fname) {
      outputFile.close();
      outputFile.open(fname.c_str(), std::ofstream::app);
    }

    void indent() { setIndentLevel(indentLevel + 2); }

    void unindent() { setIndentLevel(indentLevel - 2); }

    void setIndentLevel(int indent) {
      indentString = "";
      for (int i = 0; i < indent / 2; i++)
        indentString += "| ";
      indentLevel = indent;
    }

    void setVerboseLevel(int verbose) { verboseLevel = verbose; }
    void setLogfileVerboseLevel(int verbose) { logfileVerboseLevel = verbose; }
    int getVerboseLevel() const {return verboseLevel;}

    template <typename T>
    void setVerboseLevel() {
      setVerboseLevel(T::verboseLevel);
    }

    template <typename T>
    void setLogfileVerboseLevel() {
      setLogfileVerboseLevel(T::verboseLevel);
    }

    template <typename T>
    bool willPrint() const {
      return verboseLevel >= T::verboseLevel;
    }

    // Fast track debug. Reduced functionality but less performance loss.
    void debug(const std::string &s) {
#ifndef LIBLSS_CONSOLE_NO_DEBUG_SUPPORT
      if (willPrint<LOG_DEBUG>())
        print<LOG_DEBUG>(s);
#endif
    }

    template <typename T>
    void print(const boost::format &fmt) {
#ifdef LIBLSS_CONSOLE_NO_DEBUG_SUPPORT
      if (T::verboseLevel >= LOG_DEBUG::verboseLevel)
        return;
#endif

      print<T>(fmt.str());
    }

    template <typename T>
    void print(std::vector<std::string> const &msg_v) {
#ifdef LIBLSS_CONSOLE_NO_DEBUG_SUPPORT
      if (T::verboseLevel >= LOG_DEBUG::verboseLevel)
        return;
#endif
      for (auto const &s : msg_v)
        print<T>(s);
    }

    static void _format_expansion(boost::format &f) {}

    template <typename A, typename... U>
    static void _format_expansion(boost::format &f, A &&a, U &&... u) {
      _format_expansion(f % a, u...);
    }

    template <typename T, typename... U>
    void format(std::string const &s, U &&... args) {
#ifdef LIBLSS_CONSOLE_NO_DEBUG_SUPPORT
      if (T::verboseLevel >= LOG_DEBUG::verboseLevel)
        return;
#endif
      boost::format f(s);
      _format_expansion(f, std::forward<U>(args)...);
      print<T>(f);
    }

    template <typename T>
    void print(const std::string &msg) {
#ifdef LIBLSS_CONSOLE_NO_DEBUG_SUPPORT
      if (T::verboseLevel >= LOG_DEBUG::verboseLevel)
        return;
#endif
      MPI_Communication *world = MPI_Communication::instance();
      bool notMainRank = ((T::mainRankOnly) && (world->rank() != 0));

      if (outputFile && T::verboseLevel <= logfileVerboseLevel) {
        std::string fullMessage = T::prefix + indentString + msg;
        outputFile << fullMessage << std::endl;
      }

      if (hijackOutput) {
        std::string fullMessage = T::prefix + indentString + msg;
        hijackOutput(T::verboseLevel, fullMessage);
      }

      if (verboseLevel < T::verboseLevel)
        return;

      std::string fullMessage_c =
          (noColor ? T::prefix : T::prefix_c) + indentString + msg;

      if (!T::mainRankOnly) {
        fullMessage_c = boost::str(
            boost::format("[% 3d/% 3d] %s") % world->rank() % world->size() %
            fullMessage_c);
      } else if (notMainRank)
        return;
      else {
        fullMessage_c = "[---/---] " + fullMessage_c;
      }

      for (int i = 0; i < T::numOutput; i++)
        if (*T::os[i])
          (*T::os[i]) << fullMessage_c << std::endl;
    }

    template <typename T>
    void print_memory(size_t n) {
      if (n < 1024L)
        print<T>(boost::format("Requesting %ld bytes") % n);
      else if (n < 1024L * 1024L)
        print<T>(boost::format("Requesting %lg kbytes") % (n / 1024.));
      else if (n < 1024L * 1024L * 1024L)
        print<T>(boost::format("Requesting %lg Mbytes") % (n / 1024. / 1024.));
      else
        print<T>(
            boost::format("Requesting %lg Gbytes") %
            (n / 1024. / 1024. / 1024.));
    }

    template <typename T>
    Progress<T> &
    start_progress(const std::string &msg, int numElements, int step = 10) {
      Progress<T> *p = new Progress<T>(this, msg, numElements, step);

      all_progress.push_back(p);
      return *p;
    }

    void print_stack_trace();

    void c_assert(bool c, const std::string &msg) {
      if (!c) {
        print<LOG_ERROR>(msg);
        print_stack_trace();
        MPI_Communication::instance()->abort();
      }
    }

    template <typename U, typename... T>
    void c_assert(bool c, const std::string &msg, U &&u, T &&... t) {
      if (!c) {
        boost::format f(msg);
        _format_expansion(f, std::forward<U>(u), std::forward<T>(t)...);
        print<LOG_ERROR>(f.str());
        MPI_Communication::instance()->abort();
      }
    }
  };

  inline details::ConsoleContextBase::ConsoleContextBase() {
    previousContext = currentContext;
    currentContext = this;
  }

  inline details::ConsoleContextBase::~ConsoleContextBase() {
    currentContext = previousContext;
  }

  template <typename T>
  details::ConsoleContext<T>::ConsoleContext(std::string const &msg)
      : ConsoleContextBase() {
#ifdef LIBLSS_TIMED_CONTEXT
    start_context = boost::chrono::system_clock::now();
    short_msg = ctx_msg = msg;
#endif
    Console &c = Console::instance();
    c.print<T>("Entering " + msg);
    c.indent();
  }

  template <typename T>
  details::ConsoleContext<T>::ConsoleContext(
      std::string const &msg, std::string const &short_msg_)
      : ConsoleContextBase() {
#ifdef LIBLSS_TIMED_CONTEXT
    start_context = boost::chrono::system_clock::now();
    ctx_msg = msg;
    short_msg = short_msg_;
    record_self_timing(start_context);
#endif
    Console &c = Console::instance();
    c.print<T>("Entering " + short_msg_);
    c.indent();
  }

  template <typename T>
  details::ConsoleContext<T>::~ConsoleContext() {
    Console &c = Console::instance();
    c.unindent();
#ifdef LIBLSS_TIMED_CONTEXT
    boost::chrono::duration<double> ctx_time =
        boost::chrono::system_clock::now() - start_context;
    c.print<T>(boost::format("Done (in %s) (ctx='%s')") % ctx_time % short_msg);
    record_timing(ctx_time);
#else
    c.print<T>("Done");
#endif
  }

  template <typename T>
  template <typename... Args>
  void details::ConsoleContext<T>::print(const Args &... args) {
#ifdef LIBLSS_CONSOLE_NO_DEBUG_SUPPORT
    if (T::verboseLevel >= LOG_DEBUG::verboseLevel)
      return;
#endif
    Console::instance().print<T>(args...);
  }

  template <typename T>
  template <typename... U>
  void details::ConsoleContext<T>::format(U &&... u) {
    Console::instance().format<T>(std::forward<U>(u)...);
  }

  template <typename T>
  template <typename T2, typename... U>
  void details::ConsoleContext<T>::format2(U &&... u) {
#ifdef LIBLSS_CONSOLE_NO_DEBUG_SUPPORT
    if (T::verboseLevel >= LOG_DEBUG::verboseLevel)
      return;
#endif
    Console::instance().format<T2>(std::forward<U>(u)...);
  }

  template <typename T>
  template <typename T2, typename... Args>
  void details::ConsoleContext<T>::print2(const Args &... args) {
/*        if (T2::verboseLevel < T::verboseLevel)
            return;*/
#ifdef LIBLSS_CONSOLE_NO_DEBUG_SUPPORT
    if (T::verboseLevel >= LOG_DEBUG::verboseLevel)
      return;
#endif
    Console::instance().print<T2>(args...);
  }

  template <typename T>
  void Progress<T>::print(const std::string &m) {
    Console::instance().print<T>(m);
  }

}; // namespace LibLSS

AUTO_REGISTRATOR_DECL(console_timing);

namespace LibLSS {
  namespace fileTools {
    namespace {

      constexpr const char *str_end(const char *str) {
        return *str ? str_end(str + 1) : str;
      }

      constexpr bool str_slant(const char *str) {
        return *str == '/' ? true : (*str ? str_slant(str + 1) : false);
      }

      constexpr const char *r_slant(const char *str) {
        return *str == '/' ? (str + 1) : r_slant(str - 1);
      }
      constexpr const char *file_name(const char *str) {
        return str_slant(str) ? r_slant(str_end(str)) : str;
      }

    } // namespace
  }   // namespace fileTools
} // namespace LibLSS

#define LIBLSS_AUTO_CONTEXT(level, name)                                       \
  LibLSS::ConsoleContext<level> name(                                          \
      std::string("[" __FILE__ "]") + LIBLSS_FUNCTION)
#define LIBLSS_AUTO_CONTEXT2(level, name, short)                               \
  LibLSS::ConsoleContext<level> name(                                          \
      std::string("[" __FILE__ "]") + LIBLSS_FUNCTION, short)
#ifdef LIBLSS_CONSOLE_NO_DEBUG_SUPPORT
#  define LIBLSS_AUTO_DEBUG_CONTEXT(name)                                      \
    LibLSS::details::ConsoleContextDummy name
#  define LIBLSS_AUTO_DEBUG_CONTEXT2(name, short)                              \
    LibLSS::details::ConsoleContextDummy name
#else
#  define LIBLSS_AUTO_DEBUG_CONTEXT(name)                                      \
    LibLSS::ConsoleContext<LOG_DEBUG> name(                                    \
        std::string("[" __FILE__ "]") + LIBLSS_FUNCTION)
#  define LIBLSS_AUTO_DEBUG_CONTEXT2(name, short)                              \
    LibLSS::ConsoleContext<LOG_DEBUG> name(                                    \
        std::string("[" __FILE__ "]") + LIBLSS_FUNCTION, short)
#endif

#endif
