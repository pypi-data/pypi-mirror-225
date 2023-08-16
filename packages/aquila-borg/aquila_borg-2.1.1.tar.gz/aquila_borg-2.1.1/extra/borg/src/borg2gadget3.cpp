/*+
    ARES/HADES/BORG Package -- ./extra/borg/src/borg2gadget3.cpp
    Copyright (C) 2016-2018 Florent Leclercq <florent.leclercq@polytechnique.org>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <iostream>
#include <boost/multi_array.hpp>
#include <boost/exception/all.hpp>
#include <boost/program_options.hpp>
#include "libLSS/tools/static_init.hpp"
#include "libLSS/tools/console.hpp"
#include "CosmoTool/hdf5_array.hpp"
#include "libLSS/tools/hdf5_scalar.hpp"
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/io/gadget3.hpp"

using namespace std;
using boost::format;
using boost::str;
using namespace LibLSS;

namespace po = boost::program_options;

static bool pathExists(hid_t id, const std::string &path) {
  return H5Lexists(id, path.c_str(), H5P_DEFAULT) > 0;
} //pathExists

static void saveTimestep(
    Console &console, string output_file, IO::arrayID_t Ids,
    IO::arrayPosition_t Pos, IO::arrayVelocity_t Vel,
    CosmologicalParameters cosmo, size_t Np, double L0, double L1, double L2) {
  console.print<LOG_INFO>(
      format("Writing Gadget HDF5 snapshot in '%s'") % output_file);
  console.indent();

  H5::H5File f_out(output_file, H5F_ACC_TRUNC);
  IO::saveGadget(f_out, Ids, Pos, Vel, cosmo, Np, L0, L1, L2);

  console.unindent();
  console.print<LOG_INFO>("Done");
} //saveTimestep

int main(int argc, char *argv[]) {
  MPI_Communication *mpi_world = setupMPI(argc, argv);
  Console &console = Console::instance();

  StaticInit::execute();

  po::options_description desc("BORG2GADGET3 allowed options");
  desc.add_options()("help,h", "produce help message")(
      "borg", po::value<string>(), "borg_forward file to convert")(
      "output", po::value<string>(), "Output file prefix (default is output)");

  po::positional_options_description p;

  po::variables_map vm;

  try {
    po::store(
        po::command_line_parser(argc, argv).options(desc).positional(p).run(),
        vm);
  } catch (const boost::exception &e) {
    console.print<LOG_ERROR>(
        format("Error while parsing command line: %s") %
        boost::diagnostic_information(e));
    // At the moment use cout
    cout << desc << endl;
    return 1;
  }
  po::notify(vm);

  if (vm.count("help")) {
    // At the moment use cout
    cout << desc << endl;
    return 1;
  }

  string output_prefix;
  if (vm.count("output") == 0) {
    output_prefix = "output";
  } else {
    output_prefix = vm["output"].as<string>();
  }

  string input_file = vm["borg"].as<string>();

  console.print<LOG_INFO>("Starting BORG2GADGET3");

  console.print<LOG_INFO>(
      format("Reading borg_forward output in '%s'") % input_file);
  console.indent();

  H5::H5File f_in(input_file, H5F_ACC_RDONLY);
  double L0 = hdf5_load_scalar<double>(f_in, "scalars/L0");
  double L1 = hdf5_load_scalar<double>(f_in, "scalars/L1");
  double L2 = hdf5_load_scalar<double>(f_in, "scalars/L2");
  size_t Np = (size_t)hdf5_load_scalar<int>(f_in, "scalars/Np");
  CosmologicalParameters cosmo =
      hdf5_load_scalar<CosmologicalParameters>(f_in, "scalars/cosmo");
  console.print<LOG_INFO>(format("L0=%g, Np=%d") % L0 % Np);

  IO::arrayID_t Ids(boost::extents[Np]);
  IO::arrayPosition_t Pos(boost::extents[Np][3]);
  IO::arrayVelocity_t Vel(boost::extents[Np][3]);

  bool all_timesteps = pathExists(f_in.getId(), "step_0");
  if (all_timesteps) {
    int timestep = 0;
    while (pathExists(f_in.getId(), str(format("step_%d") % timestep))) {
      console.print<LOG_INFO>(format("Now processing timestep %d") % timestep);

      CosmoTool::hdf5_read_array(
          f_in, str(format("step_%d/u_lagrangian_id") % timestep), Ids);
      CosmoTool::hdf5_read_array(
          f_in, str(format("step_%d/u_pos") % timestep), Pos);
      CosmoTool::hdf5_read_array(
          f_in, str(format("step_%d/u_vel") % timestep), Vel);

      string output_file = str(format("%s_%d.hdf5") % output_prefix % timestep);
      saveTimestep(console, output_file, Ids, Pos, Vel, cosmo, Np, L0, L1, L2);

      timestep++;
    }

  } else {
    console.print<LOG_INFO>(
        format("Found only one timestep in '%s'") % input_file);

    CosmoTool::hdf5_read_array(f_in, "u_lagrangian_id", Ids);
    CosmoTool::hdf5_read_array(f_in, "u_pos", Pos);
    CosmoTool::hdf5_read_array(f_in, "u_vel", Vel);

    string output_file = str(format("%s.hdf5") % output_prefix);
    saveTimestep(console, output_file, Ids, Pos, Vel, cosmo, Np, L0, L1, L2);
  }

  console.unindent();
  console.print<LOG_INFO>("Done");

  StaticInit::finalize();
  doneMPI();
  return 0;
} //main

// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Florent Leclercq
// ARES TAG: year(0) = 2016-2018
// ARES TAG: email(0) = florent.leclercq@polytechnique.org
