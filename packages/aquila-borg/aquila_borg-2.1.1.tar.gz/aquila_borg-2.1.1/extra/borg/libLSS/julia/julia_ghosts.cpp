/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/julia/julia_ghosts.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/julia/julia.hpp"
#include "libLSS/julia/julia_ghosts.hpp"
#include "libLSS/julia/julia_array.hpp"
#include "libLSS/tools/string_tools.hpp"

using namespace LibLSS;
using LibLSS::Julia::helpers::_r;

namespace {
  void *_get_ghost_plane(void *j_ghosts, size_t plane, size_t maxN2) {
    Julia::Object o;

    auto ghosts = (GhostPlanes<double, 2> *)j_ghosts;

    Console::instance().print<LOG_DEBUG>(
        boost::format("Get plane %d, ghosts %p") % plane % ghosts);
    auto &g_plane = ghosts->getPlane(plane);
    o.box_array(g_plane);

    return Julia::view_array<2>(o, {_r(1, g_plane.shape()[0]), _r(1, maxN2)})
        .ptr();
  }

  void *_get_ag_ghost_plane(void *j_ghosts, size_t plane, size_t maxN2) {
    Julia::Object o;

    auto ghosts = (GhostPlanes<double, 2> *)j_ghosts;

    Console::instance().print<LOG_DEBUG>(
        boost::format("Get AG plane %d, ghosts %p") % plane % ghosts);
    auto &g_plane = ghosts->ag_getPlane(plane);
    o.box_array(g_plane);

    return Julia::view_array<2>(o, {_r(1, g_plane.shape()[0]), _r(1, maxN2)})
        .ptr();
  }

} // namespace

Julia::Object
Julia::newGhostManager(GhostPlanes<double, 2> *ghosts, size_t maxN2) {
  std::vector<Object> args(4);

  Console::instance().print<LOG_DEBUG>(
      boost::format("Setup ghosts %p") % ghosts);
  args[0].box((void *)ghosts);
  args[1].box((void *)&_get_ghost_plane);
  args[2].box((void *)&_get_ag_ghost_plane);
  args[3].box(maxN2);
  return Julia::manual_invoke("libLSS._new_ghost_plane", args);
}
