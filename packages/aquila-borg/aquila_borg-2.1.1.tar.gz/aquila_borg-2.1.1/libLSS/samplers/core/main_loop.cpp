/*+
    ARES/HADES/BORG Package -- ./libLSS/samplers/core/main_loop.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/tools/console.hpp"
#include "libLSS/samplers/core/main_loop.hpp"
#include "libLSS/tools/timing_db.hpp"

using namespace LibLSS;
using std::string;

MainLoop::MainLoop() {
  show_splash();
  mcmc_id = 0;
}

MainLoop::~MainLoop() {}

void MainLoop::show_splash() {}

void MainLoop::initialize() {
  Console &cons = Console::instance();

  cons.print<LOG_STD>("Initializing samplers");
  cons.indent();

  for (MCList::iterator i = mclist.begin(); i != mclist.end(); ++i) {
    i->first->init_markov(state);
  }
  cons.unindent();
  cons.print<LOG_STD>("Done");
}

void MainLoop::snap() {
  using boost::format;
  using boost::str;
  MPI_Communication *comm = MPI_Communication::instance();
  std::shared_ptr<H5::H5File> f;

  if (comm->rank() == 0) {
    f = std::make_shared<H5::H5File>(
        str(format("mcmc_%d.h5") % mcmc_id), H5F_ACC_TRUNC);
  }

  state.mpiSaveState(f, comm, false, true);
  mcmc_id++;
}

void MainLoop::save() {
  using boost::format;
  using boost::str;
  MPI_Communication *comm = MPI_Communication::instance();
  string fname_final = str(format("restart.h5_%d") % comm->rank());
  string fname_build = fname_final + "_build";

  {
    H5::H5File f(fname_build, H5F_ACC_TRUNC);
    state.saveState(f);
    timings::save(f);
  }
  comm->barrier();

  rename(fname_build.c_str(), fname_final.c_str());
}

void MainLoop::save_crash() {
  using boost::format;
  using boost::str;
  MPI_Communication *comm = MPI_Communication::instance();
  string fname_final = str(format("crash_file.h5_%d") % comm->rank());
  string fname_build = fname_final + "_build";

  {
    H5::H5File f(fname_build, H5F_ACC_TRUNC);
    state.saveState(f);
  }

  rename(fname_build.c_str(), fname_final.c_str());
}

void MainLoop::run() {
  ConsoleContext<LOG_STD> ctx("MainLoop::run");
  int count = 0;
  Progress<LOG_STD> progress = Console::instance().start_progress<LOG_STD>(
      "Main loop iteration", mclist.size(), 30);
  for (MCList::iterator i = mclist.begin(); i != mclist.end(); ++i) {
    int looping = i->second;
    for (int j = 0; j < looping; j++)
      i->first->sample(state);
    count++;
    progress.update(count);
  }
  progress.destroy();
}

void MainLoop::restore(const std::string &fname, bool flexible) {
  Console &cons = Console::instance();
  MPI_Communication *comm = MPI_Communication::instance();
  string fname_full =
      flexible ? fname
               : (boost::str(boost::format("%s_%d") % fname % comm->rank()));
  H5::H5File f(fname_full, 0);
  ConsoleContext<LOG_INFO> ctx("restoration of MCMC state");

  if (flexible)
    Console::instance().print<LOG_WARNING>("Using flexible mechanism");

  ctx.print("Initialize variables");
  for (MCList::iterator i = mclist.begin(); i != mclist.end(); ++i) {
    i->first->restore_markov(state);
  }

  ctx.print("Load markov state from file");
  { state.restoreState(f, flexible); }

  timings::load(f);
}
