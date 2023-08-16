/*+
    ARES/HADES/BORG Package -- ./libLSS/tools/memusage.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <sys/types.h>
#include <iostream>
#include <string>
#include <map>
#include <fstream>
#include <iomanip>
#include "libLSS/tools/console.hpp"
#include "libLSS/tools/memusage.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/static_auto.hpp"
#include <boost/format.hpp>

using boost::format;

using namespace LibLSS;

static bool report_done = true;

namespace {
  std::map<std::string, AllocationDetail> allocation_stats;
  ssize_t totalAllocated = 0;

  void memreport_ini() { report_done = false; }

  void memreport_fini() {
    Console::instance().print<LOG_DEBUG>("Writing memory report");
    std::string s =
        str(format("allocation_stats_%d.txt") %
            LibLSS::MPI_Communication::instance()->rank());
    std::ofstream f(s);

    f << "Memory still allocated at the end: "
      << totalAllocated / 1024.0 / 1024.0 << " MB" << std::endl;

    f << std::endl
      << "Statistics per context (name, allocated, freed, peak)" << std::endl
      << "======================" << std::endl
      << std::endl;

    for (auto &s : allocation_stats) {
      std::string name = s.first == "" ? "*none*" : s.first;
      f << std::left << std::setw(40) << name << " "
        << s.second.allocated / (1024. * 1024.) << " "
        << s.second.freed / (1024. * 1024.) << " "
        << s.second.peak / (1024. * 1024.) << std::endl;
    }
    report_done = true;
  }

  // Highest priority after console.
  LibLSS::RegisterStaticInit reg_record_init(
      memreport_ini, memreport_fini, 1, "Memory allocated database");
} // namespace

AUTO_REGISTRATOR_IMPL(memory_alloc);

void LibLSS::report_allocation(size_t sz, const void *ptr) {
  LibLSS::Console::instance().print<LOG_DEBUG>(
      format("Allocated %d MB") % (sz / 1024. / 1024.));
  auto &ctx = details::ConsoleContextBase::current();

  std::string const &s = ctx.getMessage();
  auto &state = allocation_stats[s];

#pragma omp critical
  {
    state.allocated += sz;
    totalAllocated += sz;
    if (totalAllocated > 0)
      state.peak = std::max(state.peak, size_t(totalAllocated));
  }
}

std::map<std::string, AllocationDetail> LibLSS::memoryReport() {
  return allocation_stats;
}

void LibLSS::clearReport() { allocation_stats.clear(); }

void LibLSS::report_free(size_t sz, const void *ptr) {
  if (report_done)
    return;

  auto &ctx = details::ConsoleContextBase::current();
  assert(&ctx != 0);
  auto const &s = ctx.getMessage();
  auto &state = allocation_stats[s];

  LibLSS::Console::instance().print<LOG_DEBUG>(
      format("Freeing %d MB") % (sz / 1024. / 1024.));

#pragma omp critical
  {
    state.freed += sz;
    totalAllocated -= sz;
  }
}
