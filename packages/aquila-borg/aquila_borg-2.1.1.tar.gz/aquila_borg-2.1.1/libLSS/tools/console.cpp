/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/console.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/cconfig.h"
#include <cstdlib>
#include <boost/stacktrace.hpp>
#include <boost/assert.hpp>
#include <boost/chrono.hpp>
#include "libLSS/tools/string_tools.hpp"
#include <fstream>
#include <iostream>
#include <map>
#include "libLSS/tools/static_init.hpp"
#include "console.hpp"
#include <CosmoTool/hdf5_array.hpp>
#include "libLSS/tools/hdf5_type.hpp"
#include "libLSS/tools/timing_db.hpp"

using boost::format;
using boost::str;
using boost::chrono::duration;
using boost::chrono::duration_cast;
using boost::chrono::system_clock;
using LibLSS::Console;
using LibLSS::details::ProgressBase;

static std::string format_duration(duration<double> &d) {
  typedef boost::chrono::hours hours;
  typedef boost::chrono::minutes minutes;
  typedef boost::chrono::seconds seconds;
  duration<long> d_int = duration_cast<duration<long>>(d);

  return str(
      format("%02d:%02d:%02d") % duration_cast<hours>(d_int).count() %
      duration_cast<minutes>(d_int % hours(1)).count() %
      duration_cast<seconds>(d_int % minutes(1)).count());
}

#ifndef NDEBUG
void boost::assertion_failed(
    char const *expr, char const *function, char const *file, long line) {
  auto &cons = Console::instance();
  std::string msg = "ASSERTION FAILED: " + std::string(expr) + " in " +
                    std::string(function) + " (" + std::string(file) + ")";
  cons.print<LibLSS::LOG_ERROR>(msg);

  ::abort();
  LibLSS::MPI_Communication::instance()->abort();
}

void boost::assertion_failed_msg(
    char const *expr, char const *msg, char const *function, char const *file,
    long line) {
  auto &cons = Console::instance();
  std::string m = "ASSERTION FAILED: " + std::string(expr) +
                  ", msg = " + std::string(msg) + " in " +
                  std::string(function) + " (" + std::string(file) + ")";
  cons.print<LibLSS::LOG_ERROR>(m);

  ::abort();
  LibLSS::MPI_Communication::instance()->abort();
}
#endif

void Console::print_stack_trace() {
  std::string s = boost::stacktrace::to_string(boost::stacktrace::stacktrace());

  print<LOG_ERROR>(LibLSS::tokenize(s, "\n"));
}

ProgressBase::ProgressBase(Console *c, const std::string &m, int num, int step)
    : numElements(num), percent(0), iLevel(c->indentLevel), step(step), msg(m),
      start(system_clock::now()), console(c) {}

void ProgressBase::destroy() {
  update(numElements);
  console->cleanProgress(this);
}

void ProgressBase::update(int i) {
  int new_percent;

  if (numElements == 0)
    return;

  current = i;
  new_percent = current * 100L / numElements;

  if (new_percent > (percent + step - 1)) {
    duration<double> elapsed = system_clock::now() - start, sec;
    int oldLevel = console->indentLevel;

    sec = elapsed * (100. - new_percent) / new_percent;

    percent = new_percent;
    console->setIndentLevel(iLevel);
    print(
        str(format("%s %d %% (ETA %s, elapsed %s)") % msg % new_percent %
            format_duration(sec) % format_duration(elapsed)));
    console->setIndentLevel(oldLevel);
  }
}

struct StatInfo {
  size_t count;
  double total_time;

  StatInfo() : count(0), total_time(0) {}
};

struct TimingInfoStore {
  CosmoTool::CosmoString name;
  StatInfo info;
};

CTOOL_STRUCT_TYPE(
    StatInfo, HDF5T_StatInfo, ((size_t, count))((double, total_time)));

CTOOL_STRUCT_TYPE(
    TimingInfoStore, HDF5T_TimingInfoStore,
    ((CosmoTool::CosmoString, name))((StatInfo, info)));

static std::map<std::string, StatInfo> timing_stats;
static bool report_timing_done = true;

namespace LibLSS {
  namespace timings {
    void record(std::string const &n, double t) {
#ifdef LIBLSS_TIMED_CONTEXT
      if (report_timing_done)
        return;
      auto &info = timing_stats[n];
      info.count++;
      info.total_time += t;
#endif
    }
  } // namespace timings
} // namespace LibLSS

#include "libLSS/ares_version.hpp"

namespace LibLSS {
  namespace details {
    namespace {
      ConsoleContextBase baseContext;
    }

    thread_local ConsoleContextBase *currentContext = &baseContext;
  } // namespace details
} // namespace LibLSS

namespace {
  using namespace LibLSS;

  static std::string g_time_file_pattern = "timing_stats_%d.txt";

  static void record_init() {
    Console::instance().print<LOG_INFO>(
        "libLSS version " + ARES_GIT_VERSION + " built-in modules " +
        ARES_BUILTIN_MODULES);
    report_timing_done = false;
  }

  static void dump_time_records(bool close) {
    if (report_timing_done)
      return;

    report_timing_done = close;
    std::string s =
        str(format(g_time_file_pattern) %
            LibLSS::MPI_Communication::instance()->rank());
    std::ofstream f(s);

    f << "ARES version " << ARES_GIT_VERSION << " modules "
      << ARES_BUILTIN_MODULES << std::endl
      << std::endl;
    f << "Cumulative timing spent in different context" << std::endl
      << "--------------------------------------------" << std::endl
      << "Context,   Total time (seconds)" << std::endl
      << std::endl;

    std::vector<std::pair<std::string, StatInfo>> sorted_timings;

    std::copy(
        timing_stats.begin(), timing_stats.end(),
        std::back_inserter(sorted_timings));
    std::sort(
        sorted_timings.begin(), sorted_timings.end(),
        [](std::pair<std::string, StatInfo> const &p1,
           std::pair<std::string, StatInfo> const &p2) {
          return p1.second.total_time > p2.second.total_time;
        });
    for (auto &n : sorted_timings) {
      f << format("% 40s\t%d\t%g") % n.first % n.second.count %
               n.second.total_time
        << std::endl;
    }
  }

  static void record_fini() { dump_time_records(true); }

  // Highest priority after console.
  LibLSS::RegisterStaticInit
      reg_record_init(record_init, record_fini, 1, "Timing database");
} // namespace

namespace LibLSS {
  namespace timings {

    void set_file_pattern(std::string const &pattern) {
      g_time_file_pattern = pattern;
    }

    void trigger_dump() { dump_time_records(false); }

    void reset() { timing_stats.clear(); }

    void load(H5_CommonFileGroup &g) {
      boost::multi_array<TimingInfoStore, 1> store;
      try {
        CosmoTool::hdf5_read_array(g, "timings", store, true);
        for (size_t i = 0; i < store.num_elements(); i++) {
          TimingInfoStore const &t = store[i];
          auto &entry = timing_stats[std::string(t.name.s)];
          entry.count += t.info.count;
          entry.total_time += t.info.total_time;
        }
      } catch (H5::FileIException const &e) {
        Console::instance().print<LOG_WARNING>(
            "No timing database in this file.");
      }
    }

    void save(H5_CommonFileGroup &g) {
      boost::multi_array<TimingInfoStore, 1> store;
      ssize_t idx = 0;
      store.resize(boost::extents[timing_stats.size()]);
      for (auto &n : timing_stats) {
        store[idx].name.s = n.first.c_str();
        store[idx].info = n.second;
        idx++;
      }
      CosmoTool::hdf5_write_array(g, "timings", store);
    }
  } // namespace timings
} // namespace LibLSS
AUTO_REGISTRATOR_IMPL(console_timing);
