/*+
    ARES/HADES/BORG Package -- ./extra/python/python/pycosmo.cpp
    Copyright (C) 2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include <CosmoTool/cosmopower.hpp>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include "libLSS/physics/cosmo.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/physics/cosmo.hpp"
#include "libLSS/physics/class_cosmo.hpp"

#include "pyborg.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

#include "pyborg_doc.hpp"
#include "pyborg_doc/aquila_borg.cosmo.hpp"

void LibLSS::Python::pyCosmo(py::module m) {
  m.doc() = DOC(aquila_borg, cosmo);

  py::class_<CosmologicalParameters>(
      m, "CosmologicalParameters",
      DOC(aquila_borg, cosmo, CosmologicalParameters))
      .def(py::init<>([]() {
        CosmologicalParameters *cpar = new CosmologicalParameters;
        cpar->omega_r = 0.0;
        cpar->omega_k = 0.0;
        cpar->omega_m = 0.30;
        cpar->omega_q = 0.70;
        cpar->omega_b = 0.049;
        cpar->w = -1;
        cpar->n_s = 1.0;
        cpar->fnl = 0;
        cpar->wprime = 0;
        cpar->sigma8 = 0.8;
        cpar->h = 0.8;
        cpar->a0 = 1.0;
        cpar->sum_mnu = 0.0;
        return cpar;
      }))
      .def_readwrite("omega_r", &CosmologicalParameters::omega_r, DOC(aquila_borg, cosmo, CosmologicalParameters, omega_r))
      .def_readwrite("omega_k", &CosmologicalParameters::omega_k, DOC(aquila_borg, cosmo, CosmologicalParameters, omega_k))
      .def_readwrite("omega_m", &CosmologicalParameters::omega_m, DOC(aquila_borg, cosmo, CosmologicalParameters, omega_m))
      .def_readwrite("omega_b", &CosmologicalParameters::omega_b, DOC(aquila_borg, cosmo, CosmologicalParameters, omega_b))
      .def_readwrite("omega_q", &CosmologicalParameters::omega_q, DOC(aquila_borg, cosmo, CosmologicalParameters, omega_q))
      .def_readwrite("w", &CosmologicalParameters::w, DOC(aquila_borg, cosmo, CosmologicalParameters, w))
      .def_readwrite("n_s", &CosmologicalParameters::n_s, DOC(aquila_borg, cosmo, CosmologicalParameters, n_s))
      .def_readwrite("fnl", &CosmologicalParameters::fnl, DOC(aquila_borg, cosmo, CosmologicalParameters, fnl))
      .def_readwrite("wprime", &CosmologicalParameters::wprime, DOC(aquila_borg, cosmo, CosmologicalParameters, wprime))
      .def_readwrite("sigma8", &CosmologicalParameters::sigma8)
      .def_readwrite("h", &CosmologicalParameters::h, DOC(aquila_borg, cosmo, CosmologicalParameters, h))
      .def_readwrite("a0", &CosmologicalParameters::a0)
      .def_readwrite("sum_mnu", &CosmologicalParameters::sum_mnu, DOC(aquila_borg, cosmo, CosmologicalParameters, sum_mnu))
      .def(
          "__copy__",
          [](CosmologicalParameters *cpar) {
            CosmologicalParameters *newcpar = new CosmologicalParameters;
            *newcpar = *cpar;
            return newcpar;
          })
      .def(
          "__deepcopy__",
          [](CosmologicalParameters *cpar) {
            CosmologicalParameters *newcpar = new CosmologicalParameters;
            *newcpar = *cpar;
            return newcpar;
          })
      .def(
          "default",
          [](CosmologicalParameters *cpar) {
            cpar->omega_r = 0.0;
            cpar->omega_k = 0.0;
            cpar->omega_m = 0.30;
            cpar->omega_q = 0.70;
            cpar->omega_b = 0.049;
            cpar->w = -1;
            cpar->n_s = 1.0;
            cpar->fnl = 0;
            cpar->wprime = 0;
            cpar->sigma8 = 0.8;
            cpar->h = 0.8;
            cpar->a0 = 1.0;
            cpar->sum_mnu = 0;
          },
          DOC(aquila_borg, cosmo, CosmologicalParameters, default))
      .def("__repr__", [](CosmologicalParameters *m) {
        return boost::str(
            boost::format("<CosmologicalParameters: omega_r=%g, omega_k=%g, "
                          "omega_m=%g, omega_b=%g, omega_q=%g, w=%g, n_s=%g, "
                          "fnl=%g, wprime=%g, sigma8=%g, h=%g, sum_mnu=%g eV>") %
            m->omega_r % m->omega_k % m->omega_m % m->omega_b % m->omega_q %
            m->w % m->n_s % m->fnl % m->wprime % m->sigma8 % m->h % m->sum_mnu);
      });

  py::class_<Cosmology>(m, "Cosmology", DOC(aquila_borg, cosmo, Cosmology))
      .def(
          py::init([](CosmologicalParameters *params) {
            return new Cosmology(*params);
          }),
          "cosmo_params"_a)
      .def(
          "__copy__",
          [](Cosmology const &cosmo) {
            return new Cosmology(cosmo.getParameters());
          })
      .def(
          "a2z", &Cosmology::a2z, "a"_a,
          "Compute the redshift for the given scale factor")
      .def(
          "z2a", &Cosmology::z2a, "z"_a,
          "Compute the scale factor for the given redshift")
      .def(
          "d_plus", &Cosmology::d_plus, "a"_a,
          "Compute the linear growth factor at a given scale factor")
      .def("a2com", &Cosmology::a2com, "a"_a)
      .def("com2a", &Cosmology::com2a, "com"_a)
      .def("dtr", &Cosmology::dtr, "Delta t_r factor of the PM")
      .def("dtv", &Cosmology::dtv, "Delta t_v factor of the PM")
      .def("gplus", &Cosmology::g_plus)
      .def("comph2com", &Cosmology::comph2com)
      .def("com2comph", &Cosmology::com2comph);

  py::class_<ClassCosmo>(m, "ClassCosmo", DOC(aquila_borg, cosmo, ClassCosmo))
      .def(
          py::init([](CosmologicalParameters *params) {
            return new ClassCosmo(*params);
          }),
          "cosmo_params"_a)
      .def("get_Tk", py::vectorize(&ClassCosmo::get_Tk), "k"_a, DOC(aquila_borg, cosmo, ClassCosmo, get_Tk))
      .def("getCosmology", &ClassCosmo::getCosmology, DOC(aquila_borg, cosmo, ClassCosmo, getCosmology));

  py::class_<CosmoTool::CosmoPower>(
      m, "CosmoPower", DOC(aquila_borg, cosmo, CosmoPower))
      .def(
          py::init([](CosmologicalParameters *params) {
            auto cpow = new CosmoTool::CosmoPower();
            cpow->h = params->h;
            cpow->OMEGA_B = params->omega_b;
            cpow->OMEGA_C = params->omega_m - params->omega_b;
            cpow->SIGMA8 = params->sigma8;
            cpow->n = params->n_s;
            cpow->updateCosmology();
            cpow->setFunction(CosmoTool::CosmoPower::HU_WIGGLES);
            cpow->normalize();
            return cpow;
          }),
          "cosmo_params"_a)
      .def(
          "power", py::vectorize([](CosmoTool::CosmoPower *p, double k) {
            return p->power(k * p->h) * p->h * p->h * p->h;
          }),
          "k"_a,
          "Evaluate the power spectrum using Eisentein&Hu formula at a given k "
          "in h/Mpc. Returns P(k) in (Mpc/h)^3");
}
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019
