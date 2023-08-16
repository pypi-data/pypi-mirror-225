/*+
    ARES/HADES/BORG Package -- ./extra/python/python/pyforward_borg.cpp
    Copyright (C) 2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/

#include <memory>
#include <exception>
#include <cstddef>
#include <boost/format.hpp>
#include <pybind11/pybind11.h>
#include <CosmoTool/cosmopower.hpp>
#include <pybind11/numpy.h>

#include "libLSS/physics/cosmo.hpp"
#include "libLSS/tools/console.hpp"
#include "libLSS/physics/cosmo.hpp"

#include "pyborg.hpp"

#include "libLSS/mpi/generic_mpi.hpp"
#include "libLSS/tools/static_init.hpp"
#include "libLSS/physics/forward_model.hpp"
#include "libLSS/physics/hades_pt.hpp"
#include "libLSS/physics/hades_log.hpp"
#include "libLSS/physics/hermitic.hpp"
#include "libLSS/physics/forwards/borg_lpt.hpp"
#include "libLSS/physics/forwards/borg_2lpt.hpp"
#include "libLSS/physics/forwards/deprecated/borg_pm.hpp"
#include "libLSS/physics/forwards/transfer.hpp"
#include "libLSS/physics/forwards/downgrade.hpp"
#include "libLSS/physics/forwards/primordial.hpp"
#include "libLSS/physics/forwards/transfer_ehu.hpp"
#include "libLSS/physics/openmp_cic.hpp"
#include "pyfuse.hpp"

#include "libLSS/physics/modified_ngp.hpp"
#include "libLSS/physics/modified_ngp_smooth.hpp"

#include "pyforward.hpp"

//namespace py = pybind11;
using namespace pybind11::literals;

#include "pyborg_doc.hpp"
#include "pyborg_doc/aquila_borg.forward.models.hpp"

template <typename CIC = LibLSS::ClassicCloudInCell<double>>
void declareLpt(
    LibLSS::Python::py::module m, std::string suffix = "",
    std::string doc = "") {
  using namespace LibLSS;
  using namespace LibLSS::Python;
  std::string name = "BorgLpt" + suffix;

  py::class_<
      BorgLptModel<CIC>, ParticleBasedForwardModel,
      std::shared_ptr<BorgLptModel<CIC>>>(
      m, name.c_str(), doc.c_str(), py::multiple_inheritance())
      .def(
          py::init([](BoxModel *box, BoxModel *box_out, bool rsd, int ss,
                      double p_factor, double ai, double af, bool light_cone,
                      double light_cone_boost) {
            py::gil_scoped_release release;
            if (box_out == nullptr)
              box_out = box;
            return std::make_unique<BorgLptModel<CIC>>(
                MPI_Communication::instance(), *box, *box_out, rsd, ss,
                p_factor, ai, af, light_cone, light_cone_boost);
          }),
          "box"_a, "box_out"_a = (BoxModel *)nullptr, "rsd"_a = false,
          "supersampling"_a = 1, "particle_factor"_a = 1.1, "ai"_a = 0.1,
          "af"_a = 1.0, "lightcone"_a = false, "lightcone_boost"_a = 1.0);
}

void LibLSS::Python::pyForwardBorg(py::module m) {
  m.doc() = DOC(aquila_borg, forward, models);

  py::class_<HadesLinear, BORGForwardModel, std::shared_ptr<HadesLinear>>(
      m, "HadesLinear", DOC(aquila_borg, forward, models, HadesLinear))
      .def(
          py::init([](BoxModel *box, double ai, double af) {
            py::gil_scoped_release release;
            return std::make_unique<HadesLinear>(
                MPI_Communication::instance(), *box, *box, ai, af);
          }),
          "box"_a, "ai"_a = 0.1, "af"_a = 1.0);

  py::class_<HadesLog, BORGForwardModel, std::shared_ptr<HadesLog>>(
      m, "HadesLog", DOC(aquila_borg, forward, models, HadesLog))
      .def(
          py::init([](BoxModel *box, double ai) {
            py::gil_scoped_release release;
            return std::make_unique<HadesLog>(
                MPI_Communication::instance(), *box, ai);
          }),
          "box"_a, "ai"_a = 0.1);

  declareLpt<>(m, "", DOC(aquila_borg, forward, models, BorgLpt));
  declareLpt<OpenMPCloudInCell<double>>(
      m, "OpenMP", DOC(aquila_borg, forward, models, BorgLptOpenMP));
  declareLpt<ModifiedNGP<double, NGPGrid::Double>>(
      m, "NGP_Double", DOC(aquila_borg, forward, models, BorgLptNGP_Double));
  declareLpt<ModifiedNGP<double, NGPGrid::Quad>>(
      m, "NGP_Quad", DOC(aquila_borg, forward, models, BorgLptNGP_Quad));
  declareLpt<SmoothModifiedNGP<double, NGPGrid::Quad>>(
      m, "SmoothNGP_Quad",
      DOC(aquila_borg, forward, models, BorgLptSmoothNGP_Quad));
  py::class_<
      ForwardHermiticOperation, BORGForwardModel,
      std::shared_ptr<ForwardHermiticOperation>>(
      m, "HermiticEnforcer",
      DOC(aquila_borg, forward, models, HermiticEnforcer))
      .def(py::init([](BoxModel *box) {
        return std::make_unique<ForwardHermiticOperation>(
            MPI_Communication::instance(), *box);
      }));
  py::class_<
      ForwardPrimordial, BORGForwardModel, std::shared_ptr<ForwardPrimordial>>(
      m, "Primordial")
      .def(py::init([](BoxModel *box, double a) {
        py::gil_scoped_release release;
        return std::make_unique<ForwardPrimordial>(
            MPI_Communication::instance(), *box, a);
      }));
  py::class_<
      ForwardEisensteinHu, BORGForwardModel,
      std::shared_ptr<ForwardEisensteinHu>>(m, "EisensteinHu")
      .def(py::init([](BoxModel *box) {
        py::gil_scoped_release release;
        return std::make_unique<ForwardEisensteinHu>(
            MPI_Communication::instance(), *box);
      }));
  py::class_<
      ForwardDowngrade, BORGForwardModel, std::shared_ptr<ForwardDowngrade>>(
      m, "Downgrade")
      .def(py::init([](BoxModel *box) {
        py::gil_scoped_release release;
        return std::make_unique<ForwardDowngrade>(
            MPI_Communication::instance(), *box);
      }));

  py::class_<
      ForwardTransfer, BORGForwardModel, std::shared_ptr<ForwardTransfer>>(
      m, "Transfer", DOC(aquila_borg, forward, models, Transfer))
      .def(py::init([](BoxModel *box) {
        py::gil_scoped_release release;
        return std::make_unique<ForwardTransfer>(
            MPI_Communication::instance(), *box);
      }))
      .def(
          "setupInverseCIC", &ForwardTransfer::setupInverseCIC,
          DOC(aquila_borg, forward, models, Transfer, setupInverseCIC))
      .def(
          "setupSharpKcut", &ForwardTransfer::setupSharpKcut, "cut"_a,
          "reversed"_a = false,
          DOC(aquila_borg, forward, models, Transfer, setupSharpKcut))
      .def(
          "setTransfer",
          [](ForwardTransfer *t, py::array_t<std::complex<double>> a) {
            PyToFuseArray<std::complex<double>, 3, false> in_Tk(
                a.unchecked<3>());

            check_array_complex(a, t->lo_mgr);

            auto tmp_c = t->lo_mgr->allocate_ptr_complex_array();
            fwrap(*tmp_c) = in_Tk;

            t->setTransfer(std::move(tmp_c));
          },
          "transfer"_a,
          DOC(aquila_borg, forward, models, Transfer, setTransfer));

  py::class_<
      Borg2LPTModel<>, ParticleBasedForwardModel,
      std::shared_ptr<Borg2LPTModel<>>>(
      m, "Borg2Lpt", py::multiple_inheritance(),
      DOC(aquila_borg, forward, models, Borg2Lpt))
      .def(
          py::init([](BoxModel *box, BoxModel *box_out, bool rsd, int ss,
                      double p_factor, double ai, double af, bool light_cone) {
            py::gil_scoped_release release;
            if (box_out == nullptr)
              box_out = box;
            return std::make_unique<Borg2LPTModel<>>(
                MPI_Communication::instance(), *box, *box_out, rsd, ss,
                p_factor, ai, af, light_cone);
          }),
          "box"_a, "box_out"_a = (BoxModel *)nullptr, "rsd"_a = false,
          "supersampling"_a = 1, "particle_factor"_a = 1.1, "ai"_a = 0.1,
          "af"_a = 1.0, "lightcone"_a = false);
}
// ARES TAG: authors_num = 1
// ARES TAG: name(0) = Guilhem Lavaux
// ARES TAG: email(0) = guilhem.lavaux@iap.fr
// ARES TAG: year(0) = 2019
